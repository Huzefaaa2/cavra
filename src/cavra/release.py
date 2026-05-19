from __future__ import annotations

import base64
import hashlib
import json
import re
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ReleaseVerificationError(ValueError):
    pass


@dataclass(frozen=True)
class ReleaseVerificationResult:
    package_dir: Path
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    verified_artifacts: list[str] = field(default_factory=list)
    verified_provenance: list[str] = field(default_factory=list)
    verified_signatures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_dir": str(self.package_dir),
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "verified_artifacts": self.verified_artifacts,
            "verified_provenance": self.verified_provenance,
            "verified_signatures": self.verified_signatures,
        }


@dataclass(frozen=True)
class AirgapBundleVerificationResult:
    bundle_path: Path
    package_dir: Path | None
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    verified_members: list[str] = field(default_factory=list)
    verified_bootstrap: list[str] = field(default_factory=list)
    release_verification: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_path": str(self.bundle_path),
            "package_dir": str(self.package_dir) if self.package_dir else None,
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "verified_members": self.verified_members,
            "verified_bootstrap": self.verified_bootstrap,
            "release_verification": self.release_verification,
        }


@dataclass(frozen=True)
class ReleaseUpgradeValidationResult:
    previous_package_dir: Path
    candidate_package_dir: Path
    valid: bool
    previous_version: str | None = None
    candidate_version: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    verified_previous: dict[str, Any] | None = None
    verified_candidate: dict[str, Any] | None = None
    artifact_changes: dict[str, list[str]] = field(default_factory=dict)
    control_changes: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "previous_package_dir": str(self.previous_package_dir),
            "candidate_package_dir": str(self.candidate_package_dir),
            "valid": self.valid,
            "previous_version": self.previous_version,
            "candidate_version": self.candidate_version,
            "errors": self.errors,
            "warnings": self.warnings,
            "verified_previous": self.verified_previous,
            "verified_candidate": self.verified_candidate,
            "artifact_changes": self.artifact_changes,
            "control_changes": self.control_changes,
        }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_go_release_package(
    package_dir: Path,
    *,
    require_signatures: bool = True,
    require_provenance: bool = True,
) -> ReleaseVerificationResult:
    package_dir = package_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    verified_artifacts: list[str] = []
    verified_provenance: list[str] = []
    verified_signatures: list[str] = []

    if not package_dir.exists() or not package_dir.is_dir():
        return ReleaseVerificationResult(
            package_dir=package_dir,
            valid=False,
            errors=[f"package directory does not exist: {package_dir}"],
        )

    evidence_path = package_dir / "release-evidence.json"
    evidence: dict[str, Any] = {}
    if not evidence_path.exists():
        errors.append("missing release-evidence.json")
    else:
        try:
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid release-evidence.json: {exc}")
        else:
            if evidence.get("schema_version") != "cavra.go-release.evidence.v1":
                errors.append("release-evidence.json has an invalid schema_version")

    checksums_path = package_dir / "checksums.txt"
    expected_checksums: dict[str, str] = {}
    if not checksums_path.exists():
        errors.append("missing checksums.txt")
    else:
        try:
            expected_checksums = _parse_checksums(checksums_path)
        except ReleaseVerificationError as exc:
            errors.append(str(exc))
        for relative_path, expected_sha256 in expected_checksums.items():
            artifact_path = _safe_package_path(package_dir, relative_path)
            if artifact_path is None:
                errors.append(f"checksum path escapes package directory: {relative_path}")
                continue
            if not artifact_path.exists() or not artifact_path.is_file():
                errors.append(f"checksum artifact is missing: {relative_path}")
                continue
            actual_sha256 = sha256_file(artifact_path)
            if actual_sha256 != expected_sha256:
                errors.append(f"checksum mismatch for {relative_path}")
            else:
                verified_artifacts.append(relative_path)

    evidence_artifacts = {
        str(artifact.get("relative_path"))
        for artifact in evidence.get("artifacts", [])
        if isinstance(artifact, dict) and artifact.get("relative_path")
    }
    missing_from_checksums = sorted(evidence_artifacts - {"checksums.txt"} - set(expected_checksums))
    if missing_from_checksums:
        errors.extend(f"evidence artifact missing from checksums.txt: {path}" for path in missing_from_checksums)

    provenance_path = package_dir / "cavra-runtime.provenance.intoto.json"
    if require_provenance and not provenance_path.exists():
        errors.append("missing cavra-runtime.provenance.intoto.json")
    if provenance_path.exists():
        try:
            verified_provenance = verify_go_release_provenance(provenance_path, package_dir, expected_checksums, evidence)
        except ReleaseVerificationError as exc:
            errors.append(str(exc))
    elif not require_provenance:
        warnings.append("package has no SLSA provenance statement")

    signature_paths = sorted(package_dir.rglob("*.sig.json"))
    if require_signatures and not signature_paths:
        errors.append("no detached signature files found")
    for signature_path in signature_paths:
        try:
            subject = verify_go_release_signature(signature_path, package_dir)
        except ReleaseVerificationError as exc:
            errors.append(str(exc))
        else:
            verified_signatures.append(subject)

    if require_signatures and evidence:
        required_subjects = evidence_artifacts | {"release-evidence.json"}
        signed_subjects = set(verified_signatures)
        unsigned_subjects = sorted(required_subjects - signed_subjects)
        errors.extend(f"missing detached signature for {subject}" for subject in unsigned_subjects)
    elif not signature_paths:
        warnings.append("package has no detached signature files")

    return ReleaseVerificationResult(
        package_dir=package_dir,
        valid=not errors,
        errors=errors,
        warnings=warnings,
        verified_artifacts=sorted(verified_artifacts),
        verified_provenance=sorted(verified_provenance),
        verified_signatures=sorted(verified_signatures),
    )


def verify_go_airgap_bundle(
    bundle_path: Path,
    *,
    extract_dir: Path | None = None,
    require_signatures: bool = True,
    require_provenance: bool = True,
    require_bootstrap: bool = True,
) -> AirgapBundleVerificationResult:
    bundle_path = bundle_path.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    verified_members: list[str] = []
    verified_bootstrap: list[str] = []
    package_dir: Path | None = None
    release_result: ReleaseVerificationResult | None = None
    bootstrap_checked = False

    if not bundle_path.exists() or not bundle_path.is_file():
        return AirgapBundleVerificationResult(
            bundle_path=bundle_path,
            package_dir=None,
            valid=False,
            errors=[f"air-gapped bundle does not exist: {bundle_path}"],
        )
    if not zipfile.is_zipfile(bundle_path):
        return AirgapBundleVerificationResult(
            bundle_path=bundle_path,
            package_dir=None,
            valid=False,
            errors=[f"air-gapped bundle is not a zip archive: {bundle_path}"],
        )

    try:
        with zipfile.ZipFile(bundle_path) as archive:
            members = archive.infolist()
            unsafe_members = [member.filename for member in members if _unsafe_zip_member(member.filename)]
            if unsafe_members:
                errors.extend(f"unsafe archive member path: {member}" for member in sorted(unsafe_members))
            else:
                verified_members = sorted(member.filename for member in members if not member.is_dir())
            top_level = sorted({member.filename.split("/", 1)[0] for member in members if member.filename and "/" in member.filename})
            if len(top_level) != 1 or not top_level[0].startswith("go-runtime-"):
                errors.append("air-gapped bundle must contain exactly one go-runtime-* package directory")
            if not errors:
                if extract_dir:
                    target_root = extract_dir.resolve()
                    target_root.mkdir(parents=True, exist_ok=True)
                    archive.extractall(target_root)
                    package_dir = target_root / top_level[0]
                    release_result = _verify_extracted_airgap_package(
                        package_dir,
                        require_signatures=require_signatures,
                        require_provenance=require_provenance,
                        require_bootstrap=require_bootstrap,
                    )
                    verified_bootstrap = _verify_airgap_bootstrap(package_dir, require_bootstrap)
                    bootstrap_checked = True
                else:
                    with tempfile.TemporaryDirectory(prefix="cavra-airgap-") as temporary:
                        target_root = Path(temporary)
                        archive.extractall(target_root)
                        package_dir = target_root / top_level[0]
                        release_result = _verify_extracted_airgap_package(
                            package_dir,
                            require_signatures=require_signatures,
                            require_provenance=require_provenance,
                            require_bootstrap=require_bootstrap,
                        )
                        verified_bootstrap = _verify_airgap_bootstrap(package_dir, require_bootstrap)
                        bootstrap_checked = True
    except zipfile.BadZipFile as exc:
        errors.append(f"invalid air-gapped zip archive: {exc}")
    except ReleaseVerificationError as exc:
        errors.append(str(exc))

    if release_result:
        errors.extend(release_result.errors)
        warnings.extend(release_result.warnings)
        if not bootstrap_checked:
            try:
                verified_bootstrap = _verify_airgap_bootstrap(package_dir, require_bootstrap)
            except ReleaseVerificationError as exc:
                errors.append(str(exc))

    return AirgapBundleVerificationResult(
        bundle_path=bundle_path,
        package_dir=package_dir,
        valid=not errors,
        errors=errors,
        warnings=warnings,
        verified_members=verified_members,
        verified_bootstrap=sorted(verified_bootstrap),
        release_verification=release_result.to_dict() if release_result else None,
    )


def validate_go_release_upgrade(
    previous_package_dir: Path,
    candidate_package_dir: Path,
    *,
    require_signatures: bool = True,
    require_provenance: bool = True,
    allow_same_version: bool = False,
) -> ReleaseUpgradeValidationResult:
    previous_package_dir = previous_package_dir.resolve()
    candidate_package_dir = candidate_package_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    previous_result = verify_go_release_package(
        previous_package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    candidate_result = verify_go_release_package(
        candidate_package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    errors.extend(f"previous package: {error}" for error in previous_result.errors)
    errors.extend(f"candidate package: {error}" for error in candidate_result.errors)
    warnings.extend(f"previous package: {warning}" for warning in previous_result.warnings)
    warnings.extend(f"candidate package: {warning}" for warning in candidate_result.warnings)

    previous_evidence = _load_release_evidence(previous_package_dir, errors, "previous")
    candidate_evidence = _load_release_evidence(candidate_package_dir, errors, "candidate")
    previous_version = _evidence_string(previous_evidence, "version")
    candidate_version = _evidence_string(candidate_evidence, "version")

    if previous_version and candidate_version:
        comparison = _compare_release_versions(candidate_version, previous_version)
        if comparison is None:
            warnings.append(
                f"could not parse release versions for ordering: previous={previous_version}, candidate={candidate_version}"
            )
        elif comparison < 0:
            errors.append(f"candidate version {candidate_version} is older than previous version {previous_version}")
        elif comparison == 0 and not allow_same_version:
            errors.append(
                f"candidate version {candidate_version} must be newer than previous version {previous_version}"
            )

    previous_artifacts = _artifact_map(previous_evidence)
    candidate_artifacts = _artifact_map(candidate_evidence)
    previous_kinds = set(previous_artifacts)
    candidate_kinds = set(candidate_artifacts)
    removed_kinds = sorted(previous_kinds - candidate_kinds)
    added_kinds = sorted(candidate_kinds - previous_kinds)
    if removed_kinds:
        errors.extend(f"candidate removed release artifact kind: {kind}" for kind in removed_kinds)

    previous_binaries = _binary_targets(previous_artifacts.get("go-binary", []), previous_version)
    candidate_binaries = _binary_targets(candidate_artifacts.get("go-binary", []), candidate_version)
    missing_binaries = sorted(set(previous_binaries) - set(candidate_binaries))
    added_binaries = sorted(set(candidate_binaries) - set(previous_binaries))
    if missing_binaries:
        errors.extend(f"candidate removed Go runtime binary target: {binary}" for binary in missing_binaries)

    previous_controls = _evidence_list(previous_evidence, "controls")
    candidate_controls = _evidence_list(candidate_evidence, "controls")
    removed_controls = sorted(set(previous_controls) - set(candidate_controls))
    added_controls = sorted(set(candidate_controls) - set(previous_controls))
    if removed_controls:
        errors.extend(f"candidate removed release control: {control}" for control in removed_controls)

    previous_commit = _evidence_string(previous_evidence, "commit")
    candidate_commit = _evidence_string(candidate_evidence, "commit")
    if previous_commit and candidate_commit and previous_commit == candidate_commit:
        warnings.append("candidate package uses the same commit as the previous package")

    return ReleaseUpgradeValidationResult(
        previous_package_dir=previous_package_dir,
        candidate_package_dir=candidate_package_dir,
        valid=not errors,
        previous_version=previous_version,
        candidate_version=candidate_version,
        errors=errors,
        warnings=warnings,
        verified_previous=previous_result.to_dict(),
        verified_candidate=candidate_result.to_dict(),
        artifact_changes={
            "added_kinds": added_kinds,
            "removed_kinds": removed_kinds,
            "added_binaries": added_binaries,
            "removed_binaries": missing_binaries,
        },
        control_changes={
            "added": added_controls,
            "removed": removed_controls,
        },
    )


def _verify_airgap_bootstrap(package_dir: Path | None, require_bootstrap: bool) -> list[str]:
    bootstrap_path = package_dir / "offline-trust-root-bootstrap.json" if package_dir else None
    if bootstrap_path and bootstrap_path.exists():
        return verify_offline_trust_bootstrap(bootstrap_path, package_dir)
    if require_bootstrap:
        raise ReleaseVerificationError("missing offline-trust-root-bootstrap.json")
    return []


def verify_offline_trust_bootstrap(bootstrap_path: Path, package_dir: Path) -> list[str]:
    try:
        payload = json.loads(bootstrap_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid offline trust bootstrap JSON: {exc}") from exc
    if payload.get("schema_version") != "cavra.offline-trust-bootstrap.v1":
        raise ReleaseVerificationError("offline trust bootstrap has an invalid schema_version")
    if payload.get("mode") != "air_gapped":
        raise ReleaseVerificationError("offline trust bootstrap mode must be air_gapped")
    required_files = payload.get("required_files")
    if not isinstance(required_files, list) or not required_files:
        raise ReleaseVerificationError("offline trust bootstrap is missing required_files")
    verified: list[str] = []
    for relative_path in required_files:
        if not isinstance(relative_path, str):
            raise ReleaseVerificationError("offline trust bootstrap required_files must be strings")
        path = _safe_package_path(package_dir, relative_path)
        if path is None or not path.exists() or not path.is_file():
            raise ReleaseVerificationError(f"offline bootstrap required file is missing: {relative_path}")
        verified.append(relative_path)
    commands = payload.get("verification_commands")
    if not isinstance(commands, list) or not commands:
        raise ReleaseVerificationError("offline trust bootstrap is missing verification_commands")
    if not any("cavra release verify-go-package" in str(command) for command in commands):
        raise ReleaseVerificationError("offline trust bootstrap must include cavra release verify-go-package guidance")
    if not any("cavra release verify-airgap-bundle" in str(command) for command in commands):
        raise ReleaseVerificationError("offline trust bootstrap must include cavra release verify-airgap-bundle guidance")
    return verified


def verify_go_release_provenance(
    provenance_path: Path,
    package_dir: Path,
    expected_checksums: dict[str, str],
    evidence: dict[str, Any],
) -> list[str]:
    try:
        payload = json.loads(provenance_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid SLSA provenance JSON: {exc}") from exc
    if payload.get("_type") != "https://in-toto.io/Statement/v1":
        raise ReleaseVerificationError("SLSA provenance has an invalid _type")
    if payload.get("predicateType") != "https://slsa.dev/provenance/v1":
        raise ReleaseVerificationError("SLSA provenance has an invalid predicateType")
    predicate = payload.get("predicate")
    if not isinstance(predicate, dict):
        raise ReleaseVerificationError("SLSA provenance is missing predicate")
    build_definition = predicate.get("buildDefinition")
    run_details = predicate.get("runDetails")
    if not isinstance(build_definition, dict) or not isinstance(run_details, dict):
        raise ReleaseVerificationError("SLSA provenance is missing buildDefinition or runDetails")
    if not build_definition.get("buildType"):
        raise ReleaseVerificationError("SLSA provenance is missing buildType")
    builder = run_details.get("builder")
    if not isinstance(builder, dict) or not builder.get("id"):
        raise ReleaseVerificationError("SLSA provenance is missing builder.id")

    external_parameters = build_definition.get("externalParameters")
    if not isinstance(external_parameters, dict):
        raise ReleaseVerificationError("SLSA provenance is missing externalParameters")
    if evidence and external_parameters.get("version") != evidence.get("version"):
        raise ReleaseVerificationError("SLSA provenance version does not match release evidence")
    if evidence and external_parameters.get("ref") != evidence.get("ref"):
        raise ReleaseVerificationError("SLSA provenance ref does not match release evidence")

    subjects = payload.get("subject")
    if not isinstance(subjects, list) or not subjects:
        raise ReleaseVerificationError("SLSA provenance has no subjects")
    verified_subjects: list[str] = []
    for subject in subjects:
        if not isinstance(subject, dict):
            raise ReleaseVerificationError("SLSA provenance subject is invalid")
        name = str(subject.get("name", ""))
        digest = subject.get("digest")
        if not isinstance(digest, dict) or not digest.get("sha256"):
            raise ReleaseVerificationError(f"SLSA provenance subject {name or 'unknown'} is missing sha256")
        subject_path = _safe_package_path(package_dir, name)
        if subject_path is None or not subject_path.exists() or not subject_path.is_file():
            raise ReleaseVerificationError(f"SLSA provenance subject is missing: {name}")
        actual_sha256 = sha256_file(subject_path)
        expected_sha256 = str(digest["sha256"]).lower()
        if actual_sha256 != expected_sha256:
            raise ReleaseVerificationError(f"SLSA provenance digest mismatch for {name}")
        checksum_sha256 = expected_checksums.get(name)
        if checksum_sha256 and checksum_sha256 != expected_sha256:
            raise ReleaseVerificationError(f"SLSA provenance subject disagrees with checksums.txt: {name}")
        verified_subjects.append(name)
    return verified_subjects


def _verify_extracted_airgap_package(
    package_dir: Path,
    *,
    require_signatures: bool,
    require_provenance: bool,
    require_bootstrap: bool,
) -> ReleaseVerificationResult:
    result = verify_go_release_package(
        package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    if require_bootstrap and "offline-trust-root-bootstrap.json" not in result.verified_artifacts:
        return ReleaseVerificationResult(
            package_dir=result.package_dir,
            valid=False,
            errors=[*result.errors, "offline-trust-root-bootstrap.json is missing from checksums.txt"],
            warnings=result.warnings,
            verified_artifacts=result.verified_artifacts,
            verified_provenance=result.verified_provenance,
            verified_signatures=result.verified_signatures,
        )
    return result


def verify_go_release_signature(signature_path: Path, package_dir: Path) -> str:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import serialization
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install cryptography to verify Go release signatures.") from exc

    try:
        payload = json.loads(signature_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid signature JSON {signature_path.name}: {exc}") from exc

    subject = str(payload.get("subject", ""))
    subject_path = _safe_package_path(package_dir, subject)
    if not subject or subject_path is None:
        raise ReleaseVerificationError(f"signature {signature_path.name} has an invalid subject")
    if not subject_path.exists() or not subject_path.is_file():
        raise ReleaseVerificationError(f"signature subject is missing: {subject}")
    if payload.get("schema_version") != "cavra.go-release.signature.v1":
        raise ReleaseVerificationError(f"signature {signature_path.name} has an invalid schema_version")
    if payload.get("algorithm") != "Ed25519":
        raise ReleaseVerificationError(f"signature {signature_path.name} uses an unsupported algorithm")

    public_key_pem = str(payload.get("public_key_pem", "")).encode("utf-8")
    if not public_key_pem:
        raise ReleaseVerificationError(f"signature {signature_path.name} is missing public_key_pem")
    if hashlib.sha256(public_key_pem).hexdigest() != payload.get("public_key_sha256"):
        raise ReleaseVerificationError(f"signature {signature_path.name} public key fingerprint mismatch")

    expected_sha256 = str(payload.get("subject_sha256", ""))
    if sha256_file(subject_path) != expected_sha256:
        raise ReleaseVerificationError(f"signature subject checksum mismatch: {subject}")

    try:
        signature = base64.b64decode(str(payload.get("value", "")), validate=True)
    except ValueError as exc:
        raise ReleaseVerificationError(f"signature {signature_path.name} has invalid base64") from exc

    public_key = serialization.load_pem_public_key(public_key_pem)
    try:
        public_key.verify(signature, subject_path.read_bytes())
    except InvalidSignature as exc:
        raise ReleaseVerificationError(f"invalid Ed25519 signature for {subject}") from exc
    return subject


def _parse_checksums(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ReleaseVerificationError(f"invalid checksums.txt line {line_number}")
        digest, relative_path = parts[0], parts[1].strip()
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest.lower()):
            raise ReleaseVerificationError(f"invalid sha256 digest on checksums.txt line {line_number}")
        checksums[relative_path] = digest.lower()
    return checksums


def _safe_package_path(package_dir: Path, relative_path: str) -> Path | None:
    if not relative_path or relative_path.startswith("/"):
        return None
    path = (package_dir / relative_path).resolve()
    try:
        path.relative_to(package_dir.resolve())
    except ValueError:
        return None
    return path


def _unsafe_zip_member(name: str) -> bool:
    if not name or name.startswith("/") or name.startswith("\\"):
        return True
    parts = Path(name).parts
    return any(part == ".." for part in parts)


def _load_release_evidence(package_dir: Path, errors: list[str], label: str) -> dict[str, Any]:
    evidence_path = package_dir / "release-evidence.json"
    if not evidence_path.exists():
        errors.append(f"{label} package is missing release-evidence.json")
        return {}
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{label} package has invalid release-evidence.json: {exc}")
        return {}
    if not isinstance(evidence, dict):
        errors.append(f"{label} package release-evidence.json must contain an object")
        return {}
    if evidence.get("schema_version") != "cavra.go-release.evidence.v1":
        errors.append(f"{label} package release-evidence.json has an invalid schema_version")
    return evidence


def _evidence_string(evidence: dict[str, Any], key: str) -> str | None:
    value = evidence.get(key)
    return value if isinstance(value, str) and value else None


def _evidence_list(evidence: dict[str, Any], key: str) -> list[str]:
    values = evidence.get(key)
    if not isinstance(values, list):
        return []
    return sorted(str(value) for value in values if isinstance(value, str) and value)


def _artifact_map(evidence: dict[str, Any]) -> dict[str, list[str]]:
    artifacts: dict[str, list[str]] = {}
    for artifact in evidence.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        kind = artifact.get("kind")
        relative_path = artifact.get("relative_path")
        if isinstance(kind, str) and kind and isinstance(relative_path, str) and relative_path:
            artifacts.setdefault(kind, []).append(relative_path)
    return {kind: sorted(paths) for kind, paths in artifacts.items()}


def _binary_targets(paths: list[str], version: str | None) -> list[str]:
    targets: list[str] = []
    for path in paths:
        name = Path(path).name
        suffix = ".exe" if name.endswith(".exe") else ""
        stem = name.removesuffix(suffix)
        prefix = f"cavra-runtime_{version}_" if version else ""
        if prefix and stem.startswith(prefix):
            targets.append(stem.removeprefix(prefix) + suffix)
        else:
            targets.append(path)
    return sorted(targets)


_SEMVER_PATTERN = re.compile(r"^v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<pre>[0-9A-Za-z.-]+))?(?:\+.*)?$")


def _compare_release_versions(candidate: str, previous: str) -> int | None:
    candidate_match = _SEMVER_PATTERN.match(candidate)
    previous_match = _SEMVER_PATTERN.match(previous)
    if not candidate_match or not previous_match:
        return None
    candidate_core = tuple(int(candidate_match.group(part)) for part in ("major", "minor", "patch"))
    previous_core = tuple(int(previous_match.group(part)) for part in ("major", "minor", "patch"))
    if candidate_core > previous_core:
        return 1
    if candidate_core < previous_core:
        return -1
    candidate_pre = candidate_match.group("pre") or ""
    previous_pre = previous_match.group("pre") or ""
    if candidate_pre == previous_pre:
        return 0
    if not candidate_pre:
        return 1
    if not previous_pre:
        return -1
    candidate_parts = _pre_release_parts(candidate_pre)
    previous_parts = _pre_release_parts(previous_pre)
    if candidate_parts > previous_parts:
        return 1
    if candidate_parts < previous_parts:
        return -1
    return 0


def _pre_release_parts(value: str) -> tuple[tuple[int, int | str], ...]:
    parts: list[tuple[int, int | str]] = []
    for part in value.split("."):
        if part.isdigit():
            parts.append((0, int(part)))
        else:
            parts.append((1, part))
    return tuple(parts)
