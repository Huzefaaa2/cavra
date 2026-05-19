from __future__ import annotations

import base64
import hashlib
import json
import os
import platform
import re
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.approvals import create_approval_request


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


@dataclass(frozen=True)
class InstallerSmokeValidationResult:
    package_dir: Path
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    verified_targets: list[str] = field(default_factory=list)
    executed_targets: list[str] = field(default_factory=list)
    package_verification: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_dir": str(self.package_dir),
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "verified_targets": self.verified_targets,
            "executed_targets": self.executed_targets,
            "package_verification": self.package_verification,
        }


@dataclass(frozen=True)
class ManagedEndpointRolloutEvidenceResult:
    output_dir: Path
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rollout_id: str | None = None
    deployment_targets: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    package_verification: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_dir": str(self.output_dir),
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "rollout_id": self.rollout_id,
            "deployment_targets": self.deployment_targets,
            "files": self.files,
            "package_verification": self.package_verification,
        }


@dataclass(frozen=True)
class ManagedEndpointRolloutVerificationResult:
    rollout_dir: Path
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rollout_id: str | None = None
    verified_artifacts: list[str] = field(default_factory=list)
    deployment_targets: list[str] = field(default_factory=list)
    metadata: dict[str, Any] | None = None
    package_verification: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollout_dir": str(self.rollout_dir),
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "rollout_id": self.rollout_id,
            "verified_artifacts": self.verified_artifacts,
            "deployment_targets": self.deployment_targets,
            "metadata": self.metadata,
            "package_verification": self.package_verification,
        }


@dataclass(frozen=True)
class ManagedEndpointRolloutPromotionRequestResult:
    rollout_dir: Path
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rollout_id: str | None = None
    request: dict[str, Any] | None = None
    approval: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollout_dir": str(self.rollout_dir),
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "rollout_id": self.rollout_id,
            "request": self.request,
            "approval": self.approval,
            "files": self.files,
        }


@dataclass(frozen=True)
class ManagedEndpointRolloutPromotionExecutionResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rollout_id: str | None = None
    execution: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "rollout_id": self.rollout_id,
            "execution": self.execution,
            "files": self.files,
        }


@dataclass(frozen=True)
class ManagedEndpointRolloutRollbackExecutionResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rollout_id: str | None = None
    rollback: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "rollout_id": self.rollout_id,
            "rollback": self.rollback,
            "files": self.files,
        }


@dataclass(frozen=True)
class ReleaseChannelPromotionRequestResult:
    package_dir: Path
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    channel: str | None = None
    request: dict[str, Any] | None = None
    approval: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_dir": str(self.package_dir),
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "channel": self.channel,
            "request": self.request,
            "approval": self.approval,
            "files": self.files,
        }


@dataclass(frozen=True)
class EndpointManagementExportResult:
    package_dir: Path
    output_dir: Path
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    channel: str | None = None
    providers: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    manifest: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_dir": str(self.package_dir),
            "output_dir": str(self.output_dir),
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "channel": self.channel,
            "providers": self.providers,
            "files": self.files,
            "manifest": self.manifest,
        }


@dataclass(frozen=True)
class EndpointManagementPublicationEventResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    publication_id: str | None = None
    export_id: str | None = None
    providers: list[str] = field(default_factory=list)
    event: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "publication_id": self.publication_id,
            "export_id": self.export_id,
            "providers": self.providers,
            "event": self.event,
        }


@dataclass(frozen=True)
class ManagedEndpointReconciliationResult:
    package_dir: Path | None
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    reconciliation_id: str | None = None
    drift_status: str | None = None
    report: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_dir": str(self.package_dir) if self.package_dir else None,
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "reconciliation_id": self.reconciliation_id,
            "drift_status": self.drift_status,
            "report": self.report,
            "files": self.files,
        }


@dataclass(frozen=True)
class EndpointDriftRemediationRequestResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    reconciliation_id: str | None = None
    request: dict[str, Any] | None = None
    approval: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "reconciliation_id": self.reconciliation_id,
            "request": self.request,
            "approval": self.approval,
            "files": self.files,
        }


@dataclass(frozen=True)
class EndpointDriftRemediationExecutionResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    reconciliation_id: str | None = None
    execution: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "reconciliation_id": self.reconciliation_id,
            "execution": self.execution,
            "files": self.files,
        }


@dataclass(frozen=True)
class ReleaseAuditExportResult:
    output_dir: Path
    files: list[Path]

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_dir": str(self.output_dir),
            "files": [str(path) for path in self.files],
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

    installer_metadata_path = package_dir / "cavra-runtime.installers.json"
    if not installer_metadata_path.exists():
        errors.append("missing cavra-runtime.installers.json")
    else:
        try:
            verify_go_installer_metadata(installer_metadata_path, package_dir, expected_checksums, evidence)
        except ReleaseVerificationError as exc:
            errors.append(str(exc))

    endpoint_deployment_path = package_dir / "cavra-runtime.endpoint-deployment.json"
    if not endpoint_deployment_path.exists():
        errors.append("missing cavra-runtime.endpoint-deployment.json")
    else:
        try:
            verify_managed_endpoint_deployment(endpoint_deployment_path, package_dir, expected_checksums, evidence)
        except ReleaseVerificationError as exc:
            errors.append(str(exc))

    channel_manifest_path = package_dir / "cavra-runtime.channels.json"
    updater_policy_path = package_dir / "cavra-runtime.updater-policy.json"
    if not channel_manifest_path.exists():
        errors.append("missing cavra-runtime.channels.json")
    if not updater_policy_path.exists():
        errors.append("missing cavra-runtime.updater-policy.json")
    if channel_manifest_path.exists() and updater_policy_path.exists():
        try:
            verify_release_channel_manifest(channel_manifest_path, package_dir, expected_checksums, evidence)
            verify_workstation_updater_policy(updater_policy_path, channel_manifest_path, evidence)
        except ReleaseVerificationError as exc:
            errors.append(str(exc))

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


def smoke_test_go_installers(
    package_dir: Path,
    *,
    require_signatures: bool = True,
    require_provenance: bool = True,
    execute_native: bool = True,
    timeout_seconds: float = 5.0,
) -> InstallerSmokeValidationResult:
    package_dir = package_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    verified_targets: list[str] = []
    executed_targets: list[str] = []

    package_result = verify_go_release_package(
        package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    errors.extend(package_result.errors)
    warnings.extend(package_result.warnings)

    installer_metadata_path = package_dir / "cavra-runtime.installers.json"
    metadata: dict[str, Any] = {}
    if installer_metadata_path.exists():
        try:
            metadata = json.loads(installer_metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid installer metadata JSON: {exc}")
    else:
        errors.append("missing cavra-runtime.installers.json")

    targets = metadata.get("targets", [])
    if isinstance(targets, list):
        for target in targets:
            if not isinstance(target, dict):
                errors.append("installer smoke target is invalid")
                continue
            target_name = str(target.get("target", ""))
            binary = str(target.get("binary", ""))
            binary_path = _safe_package_path(package_dir, binary)
            if not target_name:
                errors.append("installer smoke target is missing target name")
                continue
            if binary_path is None or not binary_path.exists():
                errors.append(f"installer smoke binary is missing: {binary}")
                continue
            if not target.get("install_path") or not target.get("install_command"):
                errors.append(f"installer smoke target is missing install command guidance: {target_name}")
                continue
            verified_targets.append(target_name)
    elif metadata:
        errors.append("installer metadata targets must be a list")

    if execute_native and isinstance(targets, list):
        native_target = _current_installer_target()
        native = next((target for target in targets if isinstance(target, dict) and target.get("target") == native_target), None)
        if native is None:
            warnings.append(f"no installer metadata target matches current platform: {native_target}")
        else:
            binary_path = _safe_package_path(package_dir, str(native.get("binary", "")))
            if binary_path is None or not binary_path.exists():
                errors.append(f"native installer smoke binary is missing for {native_target}")
            else:
                try:
                    _execute_go_runtime_smoke(binary_path, timeout_seconds=timeout_seconds)
                except ReleaseVerificationError as exc:
                    errors.append(str(exc))
                else:
                    executed_targets.append(native_target)

    return InstallerSmokeValidationResult(
        package_dir=package_dir,
        valid=not errors,
        errors=errors,
        warnings=warnings,
        verified_targets=sorted(set(verified_targets)),
        executed_targets=sorted(set(executed_targets)),
        package_verification=package_result.to_dict(),
    )


def capture_managed_endpoint_rollout_evidence(
    package_dir: Path,
    output_dir: Path,
    *,
    deployment_ids: list[str] | None = None,
    environment: str = "production",
    rollout_id: str | None = None,
    rollout_ring: str = "staging",
    status: str = "planned",
    actor: str = "release-manager",
    change_record: str = "unassigned",
    require_signatures: bool = True,
    require_provenance: bool = True,
) -> ManagedEndpointRolloutEvidenceResult:
    package_dir = package_dir.resolve()
    output_dir = output_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    package_result = verify_go_release_package(
        package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    errors.extend(package_result.errors)
    warnings.extend(package_result.warnings)
    if status not in {"planned", "staged", "succeeded", "failed", "rolled_back"}:
        errors.append(f"unsupported rollout status: {status}")

    endpoint_deployment_path = package_dir / "cavra-runtime.endpoint-deployment.json"
    release_evidence_path = package_dir / "release-evidence.json"
    endpoint_deployment: dict[str, Any] = {}
    release_evidence: dict[str, Any] = {}
    if endpoint_deployment_path.exists():
        try:
            endpoint_deployment = json.loads(endpoint_deployment_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid endpoint deployment JSON: {exc}")
    else:
        errors.append("missing cavra-runtime.endpoint-deployment.json")
    if release_evidence_path.exists():
        try:
            release_evidence = json.loads(release_evidence_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid release-evidence.json: {exc}")
    else:
        errors.append("missing release-evidence.json")

    deployment_targets = endpoint_deployment.get("deployment_targets", [])
    if not isinstance(deployment_targets, list) or not deployment_targets:
        errors.append("endpoint deployment metadata has no deployment_targets")
        deployment_targets = []
    requested_ids = set(deployment_ids or [])
    selected_targets = [
        target
        for target in deployment_targets
        if isinstance(target, dict) and (not requested_ids or str(target.get("id", "")) in requested_ids)
    ]
    selected_ids = {str(target.get("id", "")) for target in selected_targets}
    missing_ids = sorted(requested_ids - selected_ids)
    errors.extend(f"unknown endpoint deployment target: {deployment_id}" for deployment_id in missing_ids)
    if not selected_targets and not errors:
        errors.append("no endpoint deployment targets selected")

    if errors:
        return ManagedEndpointRolloutEvidenceResult(
            output_dir=output_dir,
            valid=False,
            errors=errors,
            warnings=warnings,
            rollout_id=rollout_id,
            package_verification=package_result.to_dict(),
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    resolved_rollout_id = rollout_id or _default_rollout_id(environment, release_evidence)
    evidence_path = output_dir / "managed-endpoint-rollout-evidence.json"
    summary_path = output_dir / "managed-endpoint-rollout-evidence.md"
    checksums_path = output_dir / "checksums.txt"
    now = datetime.now(timezone.utc).isoformat()
    selected_payloads = [_rollout_target_payload(target) for target in selected_targets]
    payload = {
        "schema_version": "cavra.go-runtime.endpoint-rollout-evidence.v1",
        "product": "CAVRA",
        "component": "go-enforcement-plane",
        "rollout_id": resolved_rollout_id,
        "environment": environment,
        "rollout_ring": rollout_ring,
        "status": status,
        "actor": actor,
        "change_record": change_record,
        "created_at": now,
        "package_dir": str(package_dir),
        "release": {
            "version": release_evidence.get("version"),
            "commit": release_evidence.get("commit"),
            "ref": release_evidence.get("ref"),
            "repository": endpoint_deployment.get("repository") or release_evidence.get("repository"),
        },
        "source_artifacts": {
            "endpoint_deployment": {
                "path": "cavra-runtime.endpoint-deployment.json",
                "sha256": sha256_file(endpoint_deployment_path),
            },
            "release_evidence": {
                "path": "release-evidence.json",
                "sha256": sha256_file(release_evidence_path),
            },
        },
        "deployment_targets": selected_payloads,
        "controls": [
            "signed-package-verified-before-rollout",
            "endpoint-deployment-manifest-reviewed",
            "rollout-change-record-linked",
            "rollback-plan-captured",
            "rollout-evidence-checksummed",
        ],
        "package_verification": package_result.to_dict(),
    }
    _write_release_json(evidence_path, payload)
    summary_path.write_text(_rollout_markdown_summary(payload), encoding="utf-8")
    checksum_lines = [
        f"{sha256_file(evidence_path)}  {evidence_path.name}",
        f"{sha256_file(summary_path)}  {summary_path.name}",
    ]
    checksums_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    files = [evidence_path.name, summary_path.name, checksums_path.name]
    return ManagedEndpointRolloutEvidenceResult(
        output_dir=output_dir,
        valid=True,
        warnings=warnings,
        rollout_id=resolved_rollout_id,
        deployment_targets=sorted(str(target["id"]) for target in selected_payloads),
        files=files,
        package_verification=package_result.to_dict(),
    )


def verify_managed_endpoint_rollout_evidence(
    rollout_dir: Path,
    *,
    package_dir: Path | None = None,
    require_package_verification: bool = True,
    require_signatures: bool = True,
    require_provenance: bool = True,
) -> ManagedEndpointRolloutVerificationResult:
    rollout_dir = rollout_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    verified_artifacts: list[str] = []
    package_result: ReleaseVerificationResult | None = None
    evidence_path = rollout_dir / "managed-endpoint-rollout-evidence.json"
    checksums_path = rollout_dir / "checksums.txt"
    payload: dict[str, Any] = {}

    if not rollout_dir.exists() or not rollout_dir.is_dir():
        return ManagedEndpointRolloutVerificationResult(
            rollout_dir=rollout_dir,
            valid=False,
            errors=[f"rollout evidence directory does not exist: {rollout_dir}"],
        )
    if not evidence_path.exists():
        errors.append("missing managed-endpoint-rollout-evidence.json")
    else:
        try:
            payload = json.loads(evidence_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid rollout evidence JSON: {exc}")
        else:
            if payload.get("schema_version") != "cavra.go-runtime.endpoint-rollout-evidence.v1":
                errors.append("rollout evidence has an invalid schema_version")
            if not payload.get("rollout_id"):
                errors.append("rollout evidence is missing rollout_id")
            if not payload.get("change_record"):
                errors.append("rollout evidence is missing change_record")
            if payload.get("status") not in {"planned", "staged", "succeeded", "failed", "rolled_back"}:
                errors.append("rollout evidence has an invalid status")

    if not checksums_path.exists():
        errors.append("missing checksums.txt")
    else:
        try:
            checksums = _parse_checksums(checksums_path)
        except ReleaseVerificationError as exc:
            errors.append(str(exc))
            checksums = {}
        for relative_path, expected_sha256 in checksums.items():
            artifact_path = _safe_package_path(rollout_dir, relative_path)
            if artifact_path is None:
                errors.append(f"rollout checksum path escapes directory: {relative_path}")
                continue
            if not artifact_path.exists() or not artifact_path.is_file():
                errors.append(f"rollout checksum artifact is missing: {relative_path}")
                continue
            if sha256_file(artifact_path) != expected_sha256:
                errors.append(f"rollout checksum mismatch for {relative_path}")
            else:
                verified_artifacts.append(relative_path)

    if payload:
        deployment_targets = payload.get("deployment_targets", [])
        if not isinstance(deployment_targets, list) or not deployment_targets:
            errors.append("rollout evidence has no deployment_targets")
        controls = payload.get("controls", [])
        if not isinstance(controls, list) or "rollout-evidence-checksummed" not in controls:
            errors.append("rollout evidence is missing checksum control")

        resolved_package_dir = package_dir.resolve() if package_dir else _rollout_package_dir(payload)
        if resolved_package_dir:
            source_artifacts = payload.get("source_artifacts", {})
            if isinstance(source_artifacts, dict):
                for artifact_name, artifact in source_artifacts.items():
                    if not isinstance(artifact, dict):
                        errors.append(f"rollout source artifact is invalid: {artifact_name}")
                        continue
                    relative_path = str(artifact.get("path", ""))
                    expected_sha256 = str(artifact.get("sha256", "")).lower()
                    artifact_path = _safe_package_path(resolved_package_dir, relative_path)
                    if artifact_path is None or not artifact_path.exists() or not artifact_path.is_file():
                        errors.append(f"rollout source artifact is missing: {relative_path}")
                        continue
                    if sha256_file(artifact_path) != expected_sha256:
                        errors.append(f"rollout source artifact checksum mismatch: {relative_path}")
            else:
                errors.append("rollout evidence source_artifacts must be an object")
            if require_package_verification:
                package_result = verify_go_release_package(
                    resolved_package_dir,
                    require_signatures=require_signatures,
                    require_provenance=require_provenance,
                )
                errors.extend(f"release package: {error}" for error in package_result.errors)
                warnings.extend(f"release package: {warning}" for warning in package_result.warnings)
        elif require_package_verification:
            errors.append("rollout evidence package_dir is missing or invalid")

    metadata = build_managed_endpoint_rollout_metadata(rollout_dir, payload) if payload else None
    return ManagedEndpointRolloutVerificationResult(
        rollout_dir=rollout_dir,
        valid=not errors,
        errors=errors,
        warnings=warnings,
        rollout_id=str(payload.get("rollout_id")) if payload.get("rollout_id") else None,
        verified_artifacts=sorted(verified_artifacts),
        deployment_targets=sorted(
            str(target.get("id"))
            for target in payload.get("deployment_targets", [])
            if isinstance(target, dict) and target.get("id")
        ),
        metadata=metadata,
        package_verification=package_result.to_dict() if package_result else None,
    )


def build_managed_endpoint_rollout_metadata(rollout_dir: Path, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    rollout_dir = rollout_dir.resolve()
    evidence_path = rollout_dir / "managed-endpoint-rollout-evidence.json"
    data = payload or json.loads(evidence_path.read_text(encoding="utf-8"))
    rollout_id = str(data.get("rollout_id") or "")
    targets = [target for target in data.get("deployment_targets", []) if isinstance(target, dict)]
    release = data.get("release", {}) if isinstance(data.get("release"), dict) else {}
    return {
        "schema_version": "cavra.evidence.metadata.v1",
        "product": "CAVRA",
        "session_id": rollout_id,
        "bundle_dir": str(rollout_dir),
        "created_at": data.get("created_at"),
        "signer": data.get("actor"),
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 0,
        "metadata_kind": "managed-endpoint-rollout",
        "rollout_id": rollout_id,
        "environment": data.get("environment"),
        "rollout_ring": data.get("rollout_ring"),
        "rollout_status": data.get("status"),
        "change_record": data.get("change_record"),
        "release": release,
        "deployment_target_count": len(targets),
        "deployment_targets": sorted(str(target.get("id")) for target in targets if target.get("id")),
        "artifact_sha256": sha256_file(evidence_path) if evidence_path.exists() else None,
    }


def create_managed_endpoint_rollout_promotion_request(
    rollout_dir: Path,
    *,
    output_dir: Path | None = None,
    target_ring: str = "production",
    requested_by: str = "release-manager",
    approver_group: str = "Change Advisory Board",
    ttl_hours: int = 24,
    signing_key_pem: str | None = None,
    signer: str = "release-manager",
    package_dir: Path | None = None,
    require_package_verification: bool = True,
    require_signatures: bool = True,
    require_provenance: bool = True,
) -> ManagedEndpointRolloutPromotionRequestResult:
    rollout_dir = rollout_dir.resolve()
    verification = verify_managed_endpoint_rollout_evidence(
        rollout_dir,
        package_dir=package_dir,
        require_package_verification=require_package_verification,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    errors = list(verification.errors)
    warnings = list(verification.warnings)
    evidence_path = rollout_dir / "managed-endpoint-rollout-evidence.json"
    evidence: dict[str, Any] = {}
    if evidence_path.exists():
        try:
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid rollout evidence JSON: {exc}")
    else:
        errors.append("missing managed-endpoint-rollout-evidence.json")
    rollout_id = str(evidence.get("rollout_id") or verification.rollout_id or "")
    rollout_status = str(evidence.get("status") or "")
    if verification.valid and rollout_status not in {"staged", "succeeded"}:
        errors.append("rollout promotion requires staged or succeeded rollout evidence")
    signing_key_pem = signing_key_pem or os.environ.get("CAVRA_ROLLOUT_PROMOTION_SIGNING_KEY") or os.environ.get(
        "CAVRA_GO_RELEASE_SIGNING_KEY"
    )
    if not signing_key_pem:
        errors.append("rollout promotion request signing key is required")
    if errors:
        return ManagedEndpointRolloutPromotionRequestResult(
            rollout_dir=rollout_dir,
            valid=False,
            errors=errors,
            warnings=warnings,
            rollout_id=rollout_id or None,
        )

    request_id = _promotion_request_id(rollout_id, target_ring)
    release = evidence.get("release", {}) if isinstance(evidence.get("release"), dict) else {}
    deployment_targets = [
        str(target.get("id"))
        for target in evidence.get("deployment_targets", [])
        if isinstance(target, dict) and target.get("id")
    ]
    rollback_evidence_refs = _rollback_evidence_refs(rollout_id, evidence.get("deployment_targets", []))
    decision = {
        "decision_id": f"{request_id}:decision",
        "session_id": rollout_id,
        "correlation_id": request_id,
        "action_type": "release_promote_endpoint_rollout",
        "target": f"{rollout_id}->{target_ring}",
        "decision": "require_approval",
        "severity": "high",
        "rule_id": "release.rollout.promotion.require_approval",
        "reason": "Managed endpoint rollout promotion requires signed approval.",
        "actor": requested_by,
        "policy_pack": "cavra-release-integrity",
        "repository": release.get("repository"),
        "evidence_refs": [
            f"rollout://{rollout_id}",
            f"evidence://{rollout_id}/managed-endpoint-rollout-evidence.json",
            f"change://{evidence.get('change_record', 'unassigned')}",
        ],
        "metadata": {
            "rollout_id": rollout_id,
            "current_ring": evidence.get("rollout_ring"),
            "target_ring": target_ring,
            "environment": evidence.get("environment"),
            "rollout_status": rollout_status,
            "change_record": evidence.get("change_record"),
            "deployment_targets": sorted(deployment_targets),
            "verified_artifacts": verification.verified_artifacts,
            "release": release,
        },
    }
    approval = create_approval_request(
        decision,
        approver_group=approver_group,
        requested_by=requested_by,
        ttl_hours=ttl_hours,
    )
    request_payload = {
        "schema_version": "cavra.go-runtime.endpoint-rollout-promotion-request.v1",
        "product": "CAVRA",
        "request_id": request_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "rollout_id": rollout_id,
        "environment": evidence.get("environment"),
        "current_ring": evidence.get("rollout_ring"),
        "target_ring": target_ring,
        "rollout_status": rollout_status,
        "change_record": evidence.get("change_record"),
        "release": release,
        "deployment_targets": sorted(deployment_targets),
        "rollback_evidence_refs": rollback_evidence_refs,
        "verified_artifacts": verification.verified_artifacts,
        "approval": approval,
    }
    request_payload["signature"] = _sign_json_payload_ed25519(request_payload, signing_key_pem, signer=signer)
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        request_path = output_dir / "rollout-promotion-approval-request.json"
        summary_path = output_dir / "rollout-promotion-approval-request.md"
        _write_release_json(request_path, request_payload)
        summary_path.write_text(_promotion_request_markdown_summary(request_payload), encoding="utf-8")
        files = [request_path.name, summary_path.name]
    return ManagedEndpointRolloutPromotionRequestResult(
        rollout_dir=rollout_dir,
        valid=True,
        warnings=warnings,
        rollout_id=rollout_id,
        request=request_payload,
        approval=approval,
        files=files,
    )


def create_release_channel_promotion_request(
    package_dir: Path,
    *,
    output_dir: Path | None = None,
    channel: str = "stable",
    target_ring: str = "enterprise",
    requested_by: str = "release-manager",
    approver_group: str = "Endpoint Change Advisory Board",
    ttl_hours: int = 24,
    signing_key_pem: str | None = None,
    signer: str = "release-manager",
    require_signatures: bool = True,
    require_provenance: bool = True,
) -> ReleaseChannelPromotionRequestResult:
    package_dir = package_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    package_result = verify_go_release_package(
        package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    errors.extend(package_result.errors)
    warnings.extend(package_result.warnings)
    channel_manifest_path = package_dir / "cavra-runtime.channels.json"
    updater_policy_path = package_dir / "cavra-runtime.updater-policy.json"
    release_evidence_path = package_dir / "release-evidence.json"
    try:
        channel_manifest = load_release_channel_manifest(channel_manifest_path)
        channel_payload = _select_release_channel(channel_manifest, channel)
    except (OSError, ReleaseVerificationError, ValueError) as exc:
        errors.append(str(exc))
        channel_manifest = {}
        channel_payload = {}
    try:
        updater_policy = load_workstation_updater_policy(updater_policy_path)
        channel_policy = _select_updater_channel_policy(updater_policy, channel)
    except (OSError, ReleaseVerificationError, ValueError) as exc:
        errors.append(str(exc))
        updater_policy = {}
        channel_policy = {}
    try:
        release_evidence = json.loads(release_evidence_path.read_text(encoding="utf-8"))
    except OSError as exc:
        errors.append(f"missing release-evidence.json: {exc}")
        release_evidence = {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid release-evidence.json: {exc}")
        release_evidence = {}
    if channel_payload and channel_payload.get("approval_required") is not True:
        errors.append(f"release channel {channel} must require approval before promotion")
    if channel_payload and channel_payload.get("auto_update") is not False:
        errors.append(f"release channel {channel} must disable auto_update before promotion")
    if channel_policy and channel_policy.get("approval_required") is not True:
        errors.append(f"updater policy channel {channel} must require approval before promotion")
    signing_key_pem = signing_key_pem or os.environ.get("CAVRA_RELEASE_CHANNEL_SIGNING_KEY") or os.environ.get(
        "CAVRA_GO_RELEASE_SIGNING_KEY"
    )
    if not signing_key_pem:
        errors.append("release channel promotion request signing key is required")
    if errors:
        return ReleaseChannelPromotionRequestResult(
            package_dir=package_dir,
            valid=False,
            errors=errors,
            warnings=warnings,
            channel=channel,
        )

    request_id = _release_channel_promotion_id(channel, str(release_evidence.get("version")), target_ring)
    workstation_targets = [
        target for target in channel_payload.get("workstation_targets", []) if isinstance(target, dict)
    ]
    decision = {
        "decision_id": f"{request_id}:decision",
        "session_id": f"release-channel:{channel}:{release_evidence.get('version')}",
        "correlation_id": request_id,
        "action_type": "release_promote_channel_manifest",
        "target": f"{channel}->{target_ring}",
        "decision": "require_approval",
        "severity": "high",
        "rule_id": "release.channel.promotion.require_approval",
        "reason": "Release channel promotion requires signed package verification and endpoint change approval.",
        "actor": requested_by,
        "policy_pack": "cavra-release-integrity",
        "repository": release_evidence.get("repository") or channel_manifest.get("repository"),
        "evidence_refs": [
            "artifact://cavra-runtime.channels.json",
            "artifact://cavra-runtime.updater-policy.json",
            "artifact://release-evidence.json",
        ],
        "metadata": {
            "channel": channel,
            "target_ring": target_ring,
            "version": release_evidence.get("version"),
            "commit": release_evidence.get("commit"),
            "workstation_targets": sorted(str(target.get("id")) for target in workstation_targets if target.get("id")),
            "updater_policy_controls": channel_policy.get("hold_conditions", []),
            "package_verification": package_result.to_dict(),
        },
    }
    approval = create_approval_request(
        decision,
        approver_group=approver_group,
        requested_by=requested_by,
        ttl_hours=ttl_hours,
    )
    request_payload = {
        "schema_version": "cavra.go-runtime.release-channel-promotion-request.v1",
        "product": "CAVRA",
        "component": "go-enforcement-plane",
        "request_id": request_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "channel": channel,
        "target_ring": target_ring,
        "release": {
            "version": release_evidence.get("version") or channel_manifest.get("version"),
            "commit": release_evidence.get("commit") or channel_manifest.get("commit"),
            "ref": release_evidence.get("ref"),
            "repository": release_evidence.get("repository") or channel_manifest.get("repository"),
        },
        "channel_manifest": {
            "path": "cavra-runtime.channels.json",
            "sha256": sha256_file(channel_manifest_path),
            "channel": channel_payload,
        },
        "updater_policy": {
            "path": "cavra-runtime.updater-policy.json",
            "sha256": sha256_file(updater_policy_path),
            "policy": channel_policy,
        },
        "workstation_targets": workstation_targets,
        "controls": [
            "release-package-verified",
            "channel-manifest-approval-required",
            "updater-policy-approval-required",
            "endpoint-export-bundle-required-before-publish",
            "rollback-package-reference-required",
        ],
        "approval": approval,
    }
    request_payload["signature"] = _sign_json_payload_ed25519(
        request_payload,
        signing_key_pem,
        signer=signer,
        signature_schema="cavra.release-channel-promotion.signature.v1",
    )
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        request_path = output_dir / "release-channel-promotion-request.json"
        summary_path = output_dir / "release-channel-promotion-request.md"
        _write_release_json(request_path, request_payload)
        summary_path.write_text(_release_channel_promotion_markdown_summary(request_payload), encoding="utf-8")
        files = [request_path.name, summary_path.name]
    return ReleaseChannelPromotionRequestResult(
        package_dir=package_dir,
        valid=True,
        warnings=warnings,
        channel=channel,
        request=request_payload,
        approval=approval,
        files=files,
    )


def export_endpoint_management_bundles(
    package_dir: Path,
    output_dir: Path,
    *,
    channel: str = "stable",
    provider: str = "all",
    promotion_request: dict[str, Any] | None = None,
    require_signatures: bool = True,
    require_provenance: bool = True,
) -> EndpointManagementExportResult:
    package_dir = package_dir.resolve()
    output_dir = output_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    package_result = verify_go_release_package(
        package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    errors.extend(package_result.errors)
    warnings.extend(package_result.warnings)
    try:
        channel_manifest = load_release_channel_manifest(package_dir / "cavra-runtime.channels.json")
        channel_payload = _select_release_channel(channel_manifest, channel)
    except (OSError, ReleaseVerificationError, ValueError) as exc:
        errors.append(str(exc))
        channel_manifest = {}
        channel_payload = {}
    try:
        updater_policy = load_workstation_updater_policy(package_dir / "cavra-runtime.updater-policy.json")
        channel_policy = _select_updater_channel_policy(updater_policy, channel)
    except (OSError, ReleaseVerificationError, ValueError) as exc:
        errors.append(str(exc))
        channel_policy = {}
    if promotion_request:
        try:
            verify_release_channel_promotion_request_signature(promotion_request)
        except (ReleaseVerificationError, RuntimeError) as exc:
            errors.append(str(exc))
        if promotion_request.get("channel") != channel:
            errors.append("promotion request channel does not match export channel")
    selected_providers = _endpoint_export_providers(provider)
    if not selected_providers:
        errors.append(f"unsupported endpoint-management export provider: {provider}")
    workstation_targets = [
        target for target in channel_payload.get("workstation_targets", []) if isinstance(target, dict)
    ]
    if not workstation_targets and not errors:
        errors.append(f"release channel {channel} has no workstation targets")
    if errors:
        return EndpointManagementExportResult(
            package_dir=package_dir,
            output_dir=output_dir,
            valid=False,
            errors=errors,
            warnings=warnings,
            channel=channel,
            providers=selected_providers,
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    provider_targets: dict[str, list[dict[str, Any]]] = {name: [] for name in selected_providers}
    for target in workstation_targets:
        provider_name = _endpoint_provider_for_target(target)
        if provider_name not in provider_targets:
            continue
        provider_targets[provider_name].append(target)
    for provider_name, targets in provider_targets.items():
        if not targets:
            continue
        if provider_name == "jamf":
            files.extend(_write_jamf_export(output_dir, channel, targets, channel_policy))
        elif provider_name == "intune":
            files.extend(_write_intune_export(output_dir, channel, targets, channel_policy))
        elif provider_name == "linux":
            files.extend(_write_linux_export(output_dir, channel, targets, channel_policy))
    manifest = {
        "schema_version": "cavra.endpoint-management-export.v1",
        "product": "CAVRA",
        "component": "go-enforcement-plane",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "channel": channel,
        "provider": provider,
        "providers": sorted(provider for provider, targets in provider_targets.items() if targets),
        "package_dir": str(package_dir),
        "release": {
            "version": channel_manifest.get("version"),
            "commit": channel_manifest.get("commit"),
            "repository": channel_manifest.get("repository"),
        },
        "approval": {
            "required": True,
            "request_id": promotion_request.get("request_id") if promotion_request else None,
            "approval_id": (
                promotion_request.get("approval", {}).get("approval_id")
                if isinstance(promotion_request.get("approval") if promotion_request else None, dict)
                else None
            ),
        },
        "controls": [
            "release-package-verified-before-export",
            "channel-promotion-approval-required-before-publish",
            "endpoint-tool-import-review-required",
            "rollback-package-reference-required",
        ],
        "package_verification": package_result.to_dict(),
        "files": [path.name for path in files],
    }
    manifest_path = output_dir / "endpoint-management-export-manifest.json"
    summary_path = output_dir / "endpoint-management-export-manifest.md"
    _write_release_json(manifest_path, manifest)
    summary_path.write_text(_endpoint_export_markdown_summary(manifest), encoding="utf-8")
    files.extend([manifest_path, summary_path])
    checksums_path = output_dir / "checksums.txt"
    checksums_path.write_text(
        "\n".join(f"{sha256_file(path)}  {path.name}" for path in sorted(files)) + "\n",
        encoding="utf-8",
    )
    files.append(checksums_path)
    return EndpointManagementExportResult(
        package_dir=package_dir,
        output_dir=output_dir,
        valid=True,
        warnings=warnings,
        channel=channel,
        providers=manifest["providers"],
        files=[path.name for path in files],
        manifest=manifest,
    )


def build_release_channel_promotion_request_metadata(
    request: dict[str, Any],
    *,
    package_dir: Path | None = None,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    approval = request.get("approval", {}) if isinstance(request.get("approval"), dict) else {}
    signature = request.get("signature", {}) if isinstance(request.get("signature"), dict) else {}
    release = request.get("release", {}) if isinstance(request.get("release"), dict) else {}
    targets = [target for target in request.get("workstation_targets", []) if isinstance(target, dict)]
    approval_id = approval.get("approval_id")
    metadata = {
        "session_id": request.get("request_id"),
        "created_at": request.get("created_at"),
        "signer": signature.get("signer", "release-manager"),
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 1,
        "metadata_kind": "release-channel-promotion-request",
        "request_id": request.get("request_id"),
        "channel": request.get("channel"),
        "target_ring": request.get("target_ring"),
        "approval_id": approval_id,
        "approval_state": approval.get("state"),
        "release": release,
        "deployment_targets": sorted(str(target.get("id")) for target in targets if target.get("id")),
        "endpoint_management_tools": sorted(
            {str(target.get("management_tool")) for target in targets if target.get("management_tool")}
        ),
        "controls": request.get("controls", []),
        "evidence_refs": [
            "artifact://cavra-runtime.channels.json",
            "artifact://cavra-runtime.updater-policy.json",
            f"approval://{approval_id}",
        ],
        "audit_links": {
            "channel_manifest": "artifact://cavra-runtime.channels.json",
            "updater_policy": "artifact://cavra-runtime.updater-policy.json",
            "approval": f"approval://{approval_id}",
        },
        "request": request,
    }
    if package_dir:
        metadata["package_dir"] = str(package_dir)
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def build_endpoint_management_export_metadata(
    manifest: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    approval = manifest.get("approval", {}) if isinstance(manifest.get("approval"), dict) else {}
    release = manifest.get("release", {}) if isinstance(manifest.get("release"), dict) else {}
    channel = str(manifest.get("channel") or "unknown")
    version = str(release.get("version") or "unknown")
    providers = sorted(str(provider) for provider in manifest.get("providers", []) if isinstance(provider, str))
    approval_id = approval.get("approval_id")
    request_id = approval.get("request_id")
    digest_material = f"{channel}:{version}:{','.join(providers)}:{approval_id}"
    digest = hashlib.sha256(digest_material.encode("utf-8")).hexdigest()[:12]
    export_id = f"eme_{digest}"
    metadata = {
        "session_id": export_id,
        "created_at": manifest.get("created_at"),
        "signer": "release-manager",
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 1 if approval.get("required") else 0,
        "metadata_kind": "endpoint-management-export",
        "export_id": export_id,
        "channel": channel,
        "provider": manifest.get("provider"),
        "providers": providers,
        "approval_id": approval_id,
        "approval_state": "pending" if approval.get("required") and approval.get("approval_id") else None,
        "request_id": request_id,
        "release": release,
        "files": manifest.get("files", []),
        "controls": manifest.get("controls", []),
        "package_dir": manifest.get("package_dir"),
        "evidence_refs": [
            f"release-channel-promotion://{request_id}",
            f"approval://{approval_id}",
        ],
        "audit_links": {
            "channel_promotion_request": f"release-channel-promotion://{request_id}",
            "approval": f"approval://{approval_id}",
        },
        "manifest": manifest,
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def build_endpoint_management_export_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    provider_counts: dict[str, int] = {}
    channel_counts: dict[str, int] = {}
    pending_approval = 0
    file_count = 0
    for item in items:
        for provider in item.get("providers", []) or []:
            provider_key = str(provider)
            provider_counts[provider_key] = provider_counts.get(provider_key, 0) + 1
        channel = str(item.get("channel") or "unknown")
        channel_counts[channel] = channel_counts.get(channel, 0) + 1
        file_count += len(item.get("files", []) or [])
        if item.get("approval_required_count") and item.get("approval_state") != "approved":
            pending_approval += 1
    return {
        "schema_version": "cavra.endpoint_management.export_dashboard.v1",
        "product": "CAVRA",
        "total_exports": len(items),
        "pending_approval_exports": pending_approval,
        "total_files": file_count,
        "providers": provider_counts,
        "channels": channel_counts,
        "alert_level": "warning" if pending_approval else "healthy",
        "latest": items[:10],
    }


def build_endpoint_management_publication_event(
    manifest: dict[str, Any],
    *,
    export_dir: Path | None = None,
    export_id: str | None = None,
    provider: str = "all",
    requested_by: str = "release-manager",
) -> EndpointManagementPublicationEventResult:
    errors: list[str] = []
    warnings: list[str] = []
    if manifest.get("schema_version") != "cavra.endpoint-management-export.v1":
        errors.append("endpoint-management export manifest has an invalid schema_version")
    manifest_providers = sorted(str(item) for item in manifest.get("providers", []) if isinstance(item, str))
    if not manifest_providers:
        errors.append("endpoint-management export manifest has no providers")
    selected_providers = manifest_providers if provider == "all" else [provider]
    unsupported = sorted(set(selected_providers) - {"jamf", "intune", "linux"})
    if unsupported:
        errors.append(f"unsupported endpoint-management publication provider: {', '.join(unsupported)}")
    missing_from_export = sorted(set(selected_providers) - set(manifest_providers))
    if missing_from_export:
        errors.append(f"provider not present in endpoint export: {', '.join(missing_from_export)}")
    if errors:
        return EndpointManagementPublicationEventResult(valid=False, errors=errors, warnings=warnings)

    export_id = export_id or _endpoint_management_export_id(manifest)
    publication_id = _endpoint_management_publication_id(manifest, selected_providers, export_id)
    release = manifest.get("release", {}) if isinstance(manifest.get("release"), dict) else {}
    approval = manifest.get("approval", {}) if isinstance(manifest.get("approval"), dict) else {}
    artifacts, provider_payloads, artifact_errors = _endpoint_management_publication_artifacts(
        manifest,
        selected_providers,
        export_dir=export_dir,
    )
    errors.extend(artifact_errors)
    if errors:
        return EndpointManagementPublicationEventResult(
            valid=False,
            errors=errors,
            warnings=warnings,
            publication_id=publication_id,
            export_id=export_id,
            providers=selected_providers,
        )
    event = {
        "schema_version": "cavra.endpoint-management-publication.v1",
        "product": "CAVRA",
        "event_type": "cavra.endpoint_management_export_publication",
        "event_id": publication_id,
        "publication_id": publication_id,
        "export_id": export_id,
        "session_id": export_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "requested_by": requested_by,
        "channel": manifest.get("channel"),
        "provider": provider,
        "providers": selected_providers,
        "release": release,
        "approval": {
            "required": approval.get("required"),
            "approval_id": approval.get("approval_id"),
            "request_id": approval.get("request_id"),
        },
        "controls": [
            "endpoint-export-metadata-indexed",
            "endpoint-export-artifacts-checksummed",
            "endpoint-publication-provider-selected",
            "endpoint-publication-delivery-recorded",
        ],
        "artifacts": artifacts,
        "provider_payloads": provider_payloads,
        "manifest": manifest,
    }
    return EndpointManagementPublicationEventResult(
        valid=True,
        warnings=warnings,
        publication_id=publication_id,
        export_id=export_id,
        providers=selected_providers,
        event=event,
    )


def build_endpoint_management_publication_metadata(
    delivery: dict[str, Any],
    event: dict[str, Any],
    *,
    delivery_evidence: Path | str | None = None,
) -> dict[str, Any]:
    deliveries = [item for item in delivery.get("deliveries", []) if isinstance(item, dict)]
    providers = [str(item.get("provider")) for item in deliveries if item.get("provider")]
    failed_providers = [str(item.get("provider")) for item in deliveries if item.get("provider") and not item.get("success")]
    metadata = {
        "session_id": _endpoint_management_publication_delivery_id(delivery),
        "created_at": delivery.get("generated_at") or datetime.now(timezone.utc).isoformat(),
        "signer": "endpoint-management-publication",
        "decision_count": 0,
        "blocked_count": len(failed_providers),
        "approval_required_count": 0,
        "metadata_kind": "endpoint-management-publication-delivery",
        "event_id": delivery.get("event_id"),
        "event_type": delivery.get("event_type", "cavra.endpoint_management_export_publication"),
        "publication_id": event.get("publication_id"),
        "export_id": event.get("export_id"),
        "channel": event.get("channel"),
        "release": event.get("release", {}),
        "approval_id": (event.get("approval") or {}).get("approval_id") if isinstance(event.get("approval"), dict) else None,
        "delivery_success": bool(delivery.get("success")),
        "providers": providers,
        "failed_providers": failed_providers,
        "attempt_count": sum(int(item.get("attempt_count") or 0) for item in deliveries),
        "max_attempt_count": max([int(item.get("attempt_count") or 0) for item in deliveries] or [0]),
        "status_codes": [item.get("status_code") for item in deliveries],
        "artifacts": event.get("artifacts", []),
        "delivery": delivery,
        "event": event,
    }
    if delivery_evidence:
        metadata["delivery_evidence"] = str(delivery_evidence)
    return metadata


def filter_endpoint_management_publication_history(
    items: list[dict[str, Any]],
    *,
    provider: str | None = None,
    export_id: str | None = None,
    channel: str | None = None,
    success: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [item for item in items if item.get("metadata_kind") == "endpoint-management-publication-delivery"]
    if provider:
        filtered = [item for item in filtered if provider in {str(value) for value in item.get("providers", [])}]
    if export_id:
        filtered = [item for item in filtered if item.get("export_id") == export_id]
    if channel:
        filtered = [item for item in filtered if item.get("channel") == channel]
    if success is not None:
        filtered = [item for item in filtered if bool(item.get("delivery_success")) is success]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_management.publication_history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_management_publication_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_management_publication_history(items, limit=500)["items"]
    providers: dict[str, dict[str, Any]] = {}
    successes = 0
    alerts: list[dict[str, Any]] = []
    for item in history:
        if item.get("delivery_success"):
            successes += 1
        for provider in item.get("providers", []):
            provider_key = str(provider)
            summary = providers.setdefault(
                provider_key,
                {"provider": provider_key, "total": 0, "success": 0, "failed": 0, "attempt_count": 0, "last_delivery_at": None},
            )
            summary["total"] += 1
            summary["attempt_count"] += int(item.get("attempt_count") or 0)
            summary["last_delivery_at"] = max(str(summary.get("last_delivery_at") or ""), str(item.get("created_at") or ""))
            if item.get("delivery_success") and provider_key not in {str(value) for value in item.get("failed_providers", [])}:
                summary["success"] += 1
            else:
                summary["failed"] += 1
        if not item.get("delivery_success"):
            alerts.append(
                {
                    "severity": "warning",
                    "event_id": item.get("event_id"),
                    "export_id": item.get("export_id"),
                    "failed_providers": item.get("failed_providers", []),
                    "message": f"Endpoint-management publication failed for {item.get('export_id')}.",
                }
            )
    alert_level = "healthy" if not alerts else "warning"
    return {
        "schema_version": "cavra.endpoint_management.publication_dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "total_publications": len(history),
        "successful_publications": successes,
        "failed_publications": len(history) - successes,
        "success_rate": round(successes / len(history), 4) if history else 0.0,
        "providers": sorted(providers.values(), key=lambda item: item["provider"]),
        "alerts": alerts,
        "latest": history[:10],
    }


def reconcile_managed_endpoint_deployment(
    desired_manifest: dict[str, Any],
    observed_inventory: dict[str, Any],
    *,
    package_dir: Path | None = None,
    output_dir: Path | None = None,
    stale_after_hours: int = 24,
    require_package_verification: bool = True,
) -> ManagedEndpointReconciliationResult:
    errors: list[str] = []
    warnings: list[str] = []
    package_result = None
    if desired_manifest.get("schema_version") != "cavra.go-runtime.endpoint-deployment.v1":
        errors.append("endpoint deployment manifest has an invalid schema_version")
    if observed_inventory.get("schema_version") != "cavra.endpoint-observations.v1":
        errors.append("observed endpoint inventory has an invalid schema_version")
    if package_dir and require_package_verification:
        package_result = verify_go_release_package(package_dir)
        errors.extend(package_result.errors)
        warnings.extend(package_result.warnings)
    desired_targets = [
        target for target in desired_manifest.get("deployment_targets", []) if isinstance(target, dict) and target.get("id")
    ]
    observations = [
        endpoint for endpoint in observed_inventory.get("endpoints", []) if isinstance(endpoint, dict)
    ]
    if not desired_targets:
        errors.append("endpoint deployment manifest has no deployment_targets")
    if errors:
        return ManagedEndpointReconciliationResult(
            package_dir=package_dir,
            valid=False,
            errors=errors,
            warnings=warnings,
        )

    report = _managed_endpoint_reconciliation_report(
        desired_manifest,
        observed_inventory,
        desired_targets,
        observations,
        stale_after_hours=max(1, stale_after_hours),
        package_verification=package_result.to_dict() if package_result else None,
    )
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        report_path = output_dir / "managed-endpoint-reconciliation.json"
        summary_path = output_dir / "managed-endpoint-reconciliation.md"
        _write_release_json(report_path, report)
        summary_path.write_text(_managed_endpoint_reconciliation_markdown_summary(report), encoding="utf-8")
        checksums_path = output_dir / "checksums.txt"
        checksums_path.write_text(
            "\n".join(f"{sha256_file(path)}  {path.name}" for path in [report_path, summary_path]) + "\n",
            encoding="utf-8",
        )
        files = [report_path.name, summary_path.name, checksums_path.name]
    return ManagedEndpointReconciliationResult(
        package_dir=package_dir,
        valid=True,
        warnings=warnings,
        reconciliation_id=report["reconciliation_id"],
        drift_status=report["drift_status"],
        report=report,
        files=files,
    )


def build_managed_endpoint_reconciliation_metadata(
    report: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    metadata = {
        "session_id": report.get("reconciliation_id"),
        "created_at": report.get("created_at"),
        "signer": "endpoint-reconciliation",
        "decision_count": 0,
        "blocked_count": int(summary.get("drifted_endpoint_count") or 0) + int(summary.get("missing_target_count") or 0),
        "approval_required_count": 0,
        "metadata_kind": "managed-endpoint-reconciliation",
        "reconciliation_id": report.get("reconciliation_id"),
        "drift_status": report.get("drift_status"),
        "alert_level": report.get("alert_level"),
        "release": report.get("release", {}),
        "observed_at": report.get("observed_at"),
        "channel": report.get("channel"),
        "desired_target_count": summary.get("desired_target_count", 0),
        "observed_endpoint_count": summary.get("observed_endpoint_count", 0),
        "compliant_endpoint_count": summary.get("compliant_endpoint_count", 0),
        "drifted_endpoint_count": summary.get("drifted_endpoint_count", 0),
        "missing_target_count": summary.get("missing_target_count", 0),
        "unknown_target_count": summary.get("unknown_target_count", 0),
        "stale_endpoint_count": summary.get("stale_endpoint_count", 0),
        "deployment_targets": report.get("deployment_targets", []),
        "drift_items": report.get("drift_items", []),
        "report": report,
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def filter_managed_endpoint_reconciliation_history(
    items: list[dict[str, Any]],
    *,
    drift_status: str | None = None,
    alert_level: str | None = None,
    deployment_target: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [item for item in items if item.get("metadata_kind") == "managed-endpoint-reconciliation"]
    if drift_status:
        filtered = [item for item in filtered if item.get("drift_status") == drift_status]
    if alert_level:
        filtered = [item for item in filtered if item.get("alert_level") == alert_level]
    if deployment_target:
        filtered = [
            item
            for item in filtered
            if deployment_target in {str(value) for value in item.get("deployment_targets", [])}
        ]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_reconciliation.history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_managed_endpoint_reconciliation_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_managed_endpoint_reconciliation_history(items, limit=500)["items"]
    latest = history[:10]
    drifted = sum(int(item.get("drifted_endpoint_count") or 0) for item in history)
    missing = sum(int(item.get("missing_target_count") or 0) for item in history)
    stale = sum(int(item.get("stale_endpoint_count") or 0) for item in history)
    compliant = sum(int(item.get("compliant_endpoint_count") or 0) for item in history)
    alerts = [
        {
            "severity": item.get("alert_level", "warning"),
            "reconciliation_id": item.get("reconciliation_id"),
            "message": f"Endpoint reconciliation found {item.get('drifted_endpoint_count', 0)} drifted endpoints and {item.get('missing_target_count', 0)} missing targets.",
        }
        for item in history
        if item.get("alert_level") in {"warning", "critical"}
    ]
    alert_level = "critical" if any(item.get("severity") == "critical" for item in alerts) else "warning" if alerts else "healthy"
    return {
        "schema_version": "cavra.endpoint_reconciliation.dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "total_reconciliations": len(history),
        "compliant_endpoint_count": compliant,
        "drifted_endpoint_count": drifted,
        "missing_target_count": missing,
        "stale_endpoint_count": stale,
        "alerts": alerts[:25],
        "latest": latest,
    }


def create_endpoint_drift_remediation_request(
    reconciliation_report: dict[str, Any],
    *,
    output_dir: Path | None = None,
    strategy: str = "mixed",
    requested_by: str = "release-manager",
    approver_group: str = "Endpoint Change Advisory Board",
    ttl_hours: int = 24,
) -> EndpointDriftRemediationRequestResult:
    errors: list[str] = []
    warnings: list[str] = []
    reconciliation_id = str(reconciliation_report.get("reconciliation_id") or "")
    if reconciliation_report.get("schema_version") != "cavra.endpoint-reconciliation.v1":
        errors.append("reconciliation report has an invalid schema_version")
    if not reconciliation_id:
        errors.append("reconciliation report must include reconciliation_id")
    if strategy not in {"mixed", "republish", "rollback"}:
        errors.append("strategy must be one of: mixed, republish, rollback")
    drift_items = [item for item in reconciliation_report.get("drift_items", []) if isinstance(item, dict)]
    if not drift_items:
        warnings.append("reconciliation report has no drift items; remediation request will contain no actions")
    if errors:
        return EndpointDriftRemediationRequestResult(
            valid=False,
            errors=errors,
            warnings=warnings,
            reconciliation_id=reconciliation_id or None,
        )

    actions = _endpoint_drift_remediation_actions(reconciliation_report, strategy=strategy)
    request_id = _endpoint_remediation_request_id(reconciliation_id, actions, strategy)
    created_at = datetime.now(timezone.utc).isoformat()
    summary = reconciliation_report.get("summary", {}) if isinstance(reconciliation_report.get("summary"), dict) else {}
    decision = {
        "decision_id": f"{request_id}:decision",
        "session_id": reconciliation_id,
        "correlation_id": request_id,
        "decision": "require_approval",
        "action_type": "endpoint_drift_remediation",
        "rule_id": "release.endpoint_remediation.require_approval",
        "severity": reconciliation_report.get("alert_level", "warning"),
        "target": reconciliation_id,
        "reason": "Endpoint drift remediation requires approval before republish, rollback, or inventory refresh actions are executed.",
        "metadata": {
            "request_id": request_id,
            "reconciliation_id": reconciliation_id,
            "strategy": strategy,
            "action_count": len(actions),
            "drift_status": reconciliation_report.get("drift_status"),
            "drifted_endpoint_count": summary.get("drifted_endpoint_count", 0),
            "missing_target_count": summary.get("missing_target_count", 0),
            "stale_endpoint_count": summary.get("stale_endpoint_count", 0),
        },
        "evidence_refs": [f"endpoint-reconciliation://{reconciliation_id}"],
    }
    approval = create_approval_request(
        decision,
        approver_group=approver_group,
        requested_by=requested_by,
        ttl_hours=ttl_hours,
    )
    report_canonical = json.dumps(reconciliation_report, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    request_payload = {
        "schema_version": "cavra.endpoint-drift-remediation-request.v1",
        "product": "CAVRA",
        "request_id": request_id,
        "reconciliation_id": reconciliation_id,
        "created_at": created_at,
        "requested_by": requested_by,
        "strategy": strategy,
        "drift_status": reconciliation_report.get("drift_status"),
        "alert_level": reconciliation_report.get("alert_level"),
        "release": reconciliation_report.get("release", {}),
        "channel": reconciliation_report.get("channel"),
        "summary": summary,
        "action_count": len(actions),
        "actions": actions,
        "approval": {
            "approval_id": approval["approval_id"],
            "state": approval["state"],
            "approver_group": approval["approver_group"],
            "decision_id": approval["decision_id"],
        },
        "controls": [
            "endpoint-drift-actions-derived-from-reconciliation",
            "approval-required-before-remediation",
            "public-repo-records-governance-only",
            "private-connectors-required-for-endpoint-mutation",
        ],
        "evidence_refs": [
            f"endpoint-reconciliation://{reconciliation_id}",
            f"approval://{approval['approval_id']}",
        ],
        "reconciliation_sha256": hashlib.sha256(report_canonical).hexdigest(),
        "reconciliation_report": reconciliation_report,
    }
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        request_path = output_dir / "endpoint-remediation-request.json"
        summary_path = output_dir / "endpoint-remediation-request.md"
        _write_release_json(request_path, request_payload)
        summary_path.write_text(_endpoint_remediation_request_markdown_summary(request_payload), encoding="utf-8")
        files = [request_path.name, summary_path.name]
    return EndpointDriftRemediationRequestResult(
        valid=True,
        warnings=warnings,
        reconciliation_id=reconciliation_id,
        request=request_payload,
        approval=approval,
        files=files,
    )


def execute_endpoint_drift_remediation(
    remediation_request: dict[str, Any],
    approval: dict[str, Any],
    *,
    output_dir: Path | None = None,
    executed_by: str = "release-manager",
    execution_environment: str | None = None,
    notes: str | None = None,
) -> EndpointDriftRemediationExecutionResult:
    errors: list[str] = []
    warnings: list[str] = []
    if remediation_request.get("schema_version") != "cavra.endpoint-drift-remediation-request.v1":
        errors.append("remediation request has an invalid schema_version")
    request_id = str(remediation_request.get("request_id") or "")
    reconciliation_id = str(remediation_request.get("reconciliation_id") or "")
    approval_id = str(approval.get("approval_id") or "")
    if not request_id:
        errors.append("remediation request must include request_id")
    if not reconciliation_id:
        errors.append("remediation request must include reconciliation_id")
    request_approval = remediation_request.get("approval", {})
    request_approval_id = str(request_approval.get("approval_id") if isinstance(request_approval, dict) else "")
    if not approval_id:
        errors.append("approval record must include approval_id")
    if request_approval_id and approval_id and request_approval_id != approval_id:
        errors.append("approval record does not match remediation request approval_id")
    if approval.get("state") != "approved":
        errors.append("endpoint drift remediation requires an approved approval record")
    if approval.get("decision_id") != f"{request_id}:decision":
        errors.append("approval decision_id does not match remediation request")
    if approval.get("session_id") != reconciliation_id:
        errors.append("approval session_id does not match reconciliation_id")
    decision = approval.get("decision", {})
    if not isinstance(decision, dict):
        errors.append("approval decision payload is invalid")
        decision = {}
    if decision.get("action_type") != "endpoint_drift_remediation":
        errors.append("approval decision action_type does not authorize endpoint drift remediation")
    metadata = decision.get("metadata", {}) if isinstance(decision.get("metadata"), dict) else {}
    if metadata.get("request_id") and metadata.get("request_id") != request_id:
        errors.append("approval request_id does not match remediation request")
    if metadata.get("reconciliation_id") and metadata.get("reconciliation_id") != reconciliation_id:
        errors.append("approval reconciliation_id does not match remediation request")
    actions = [item for item in remediation_request.get("actions", []) if isinstance(item, dict)]
    if not actions:
        warnings.append("remediation request contains no actions")
    if errors:
        return EndpointDriftRemediationExecutionResult(
            valid=False,
            errors=errors,
            warnings=warnings,
            reconciliation_id=reconciliation_id or None,
        )

    request_canonical = json.dumps(remediation_request, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    execution_id = _endpoint_remediation_execution_id(request_id, approval_id)
    action_results = [_endpoint_remediation_action_result(action) for action in actions]
    execution = {
        "schema_version": "cavra.endpoint-drift-remediation-execution.v1",
        "product": "CAVRA",
        "execution_id": execution_id,
        "request_id": request_id,
        "approval_id": approval_id,
        "reconciliation_id": reconciliation_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "executed_by": executed_by,
        "execution_environment": execution_environment,
        "execution_status": "recorded",
        "strategy": remediation_request.get("strategy"),
        "release": remediation_request.get("release", {}),
        "channel": remediation_request.get("channel"),
        "action_results": action_results,
        "approval": {
            "approval_id": approval_id,
            "state": approval.get("state"),
            "approver_group": approval.get("approver_group"),
            "decided_by": approval.get("decided_by"),
            "decided_at": approval.get("decided_at"),
            "decision_reason": approval.get("decision_reason"),
        },
        "controls": [
            "approval-state-approved",
            "approval-bound-to-reconciliation",
            "remediation-request-digest-recorded",
            "public-execution-record-does-not-mutate-endpoints",
        ],
        "request_sha256": hashlib.sha256(request_canonical).hexdigest(),
        "evidence_refs": [
            f"endpoint-reconciliation://{reconciliation_id}",
            f"endpoint-remediation-request://{request_id}",
            f"approval://{approval_id}",
        ],
    }
    if notes:
        execution["notes"] = notes
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        execution_path = output_dir / "endpoint-remediation-execution.json"
        summary_path = output_dir / "endpoint-remediation-execution.md"
        _write_release_json(execution_path, execution)
        summary_path.write_text(_endpoint_remediation_execution_markdown_summary(execution), encoding="utf-8")
        files = [execution_path.name, summary_path.name]
    return EndpointDriftRemediationExecutionResult(
        valid=True,
        warnings=warnings,
        reconciliation_id=reconciliation_id,
        execution=execution,
        files=files,
    )


def build_endpoint_drift_remediation_request_metadata(
    request: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    approval = request.get("approval", {}) if isinstance(request.get("approval"), dict) else {}
    summary = request.get("summary", {}) if isinstance(request.get("summary"), dict) else {}
    metadata = {
        "session_id": request.get("request_id"),
        "created_at": request.get("created_at"),
        "signer": request.get("requested_by", "release-manager"),
        "decision_count": 1,
        "blocked_count": 0,
        "approval_required_count": 1,
        "metadata_kind": "endpoint-drift-remediation-request",
        "request_id": request.get("request_id"),
        "reconciliation_id": request.get("reconciliation_id"),
        "drift_status": request.get("drift_status"),
        "alert_level": request.get("alert_level"),
        "strategy": request.get("strategy"),
        "action_count": request.get("action_count", len(request.get("actions", []))),
        "approval_id": approval.get("approval_id"),
        "approval_state": approval.get("state"),
        "release": request.get("release", {}),
        "channel": request.get("channel"),
        "drifted_endpoint_count": summary.get("drifted_endpoint_count", 0),
        "missing_target_count": summary.get("missing_target_count", 0),
        "stale_endpoint_count": summary.get("stale_endpoint_count", 0),
        "actions": request.get("actions", []),
        "request": request,
        "evidence_refs": request.get("evidence_refs", []),
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def build_endpoint_drift_remediation_execution_metadata(
    execution: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    approval = execution.get("approval", {}) if isinstance(execution.get("approval"), dict) else {}
    action_results = [item for item in execution.get("action_results", []) if isinstance(item, dict)]
    metadata = {
        "session_id": execution.get("execution_id"),
        "created_at": execution.get("created_at"),
        "signer": execution.get("executed_by", "release-manager"),
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 0,
        "metadata_kind": "endpoint-drift-remediation-execution",
        "execution_id": execution.get("execution_id"),
        "request_id": execution.get("request_id"),
        "reconciliation_id": execution.get("reconciliation_id"),
        "execution_status": execution.get("execution_status"),
        "strategy": execution.get("strategy"),
        "action_count": len(action_results),
        "approval_id": execution.get("approval_id"),
        "approval_state": approval.get("state"),
        "release": execution.get("release", {}),
        "channel": execution.get("channel"),
        "action_results": action_results,
        "execution": execution,
        "evidence_refs": execution.get("evidence_refs", []),
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def filter_endpoint_drift_remediation_history(
    items: list[dict[str, Any]],
    *,
    metadata_kind: str | None = None,
    reconciliation_id: str | None = None,
    approval_state: str | None = None,
    execution_status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    allowed_kinds = {"endpoint-drift-remediation-request", "endpoint-drift-remediation-execution"}
    filtered = [item for item in items if item.get("metadata_kind") in allowed_kinds]
    if metadata_kind:
        filtered = [item for item in filtered if item.get("metadata_kind") == metadata_kind]
    if reconciliation_id:
        filtered = [item for item in filtered if item.get("reconciliation_id") == reconciliation_id]
    if approval_state:
        filtered = [item for item in filtered if item.get("approval_state") == approval_state]
    if execution_status:
        filtered = [item for item in filtered if item.get("execution_status") == execution_status]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_drift_remediation.history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_drift_remediation_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_drift_remediation_history(items, limit=500)["items"]
    requests = [item for item in history if item.get("metadata_kind") == "endpoint-drift-remediation-request"]
    executions = [item for item in history if item.get("metadata_kind") == "endpoint-drift-remediation-execution"]
    pending = [item for item in requests if item.get("approval_state") == "pending"]
    approved_executions = [item for item in executions if item.get("approval_state") == "approved"]
    action_count = sum(int(item.get("action_count") or 0) for item in requests)
    alert_level = "critical" if pending else "warning" if requests and not approved_executions else "healthy"
    return {
        "schema_version": "cavra.endpoint_drift_remediation.dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "request_count": len(requests),
        "execution_count": len(executions),
        "pending_approval_count": len(pending),
        "approved_execution_count": len(approved_executions),
        "planned_action_count": action_count,
        "latest": history[:10],
    }


def create_managed_endpoint_rollout_promotion_execution(
    promotion_request: dict[str, Any],
    approval: dict[str, Any],
    *,
    output_dir: Path | None = None,
    executed_by: str = "release-manager",
    execution_environment: str | None = None,
    notes: str | None = None,
) -> ManagedEndpointRolloutPromotionExecutionResult:
    errors: list[str] = []
    warnings: list[str] = []
    if promotion_request.get("schema_version") != "cavra.go-runtime.endpoint-rollout-promotion-request.v1":
        errors.append("promotion request has an invalid schema_version")
    try:
        verify_rollout_promotion_request_signature(promotion_request)
    except (ReleaseVerificationError, RuntimeError) as exc:
        errors.append(str(exc))
    approval_id = str(approval.get("approval_id") or "")
    request_approval = promotion_request.get("approval", {})
    request_approval_id = str(request_approval.get("approval_id") if isinstance(request_approval, dict) else "")
    if not approval_id:
        errors.append("approval record must include approval_id")
    if request_approval_id and approval_id and request_approval_id != approval_id:
        errors.append("approval record does not match promotion request approval_id")
    if approval.get("state") != "approved":
        errors.append("rollout promotion execution requires an approved approval record")
    if approval.get("decision_id") != f"{promotion_request.get('request_id')}:decision":
        errors.append("approval decision_id does not match promotion request")
    if approval.get("session_id") != promotion_request.get("rollout_id"):
        errors.append("approval session_id does not match rollout_id")
    decision = approval.get("decision", {})
    if not isinstance(decision, dict):
        errors.append("approval decision payload is invalid")
        decision = {}
    if decision.get("action_type") != "release_promote_endpoint_rollout":
        errors.append("approval decision action_type does not authorize rollout promotion")
    metadata = decision.get("metadata", {}) if isinstance(decision.get("metadata"), dict) else {}
    if metadata.get("target_ring") and metadata.get("target_ring") != promotion_request.get("target_ring"):
        errors.append("approval target ring does not match promotion request")
    if metadata.get("current_ring") and metadata.get("current_ring") != promotion_request.get("current_ring"):
        errors.append("approval current ring does not match promotion request")
    rollout_id = str(promotion_request.get("rollout_id") or "")
    if errors:
        return ManagedEndpointRolloutPromotionExecutionResult(
            valid=False,
            errors=errors,
            warnings=warnings,
            rollout_id=rollout_id or None,
        )

    request_canonical = json.dumps(promotion_request, sort_keys=True, separators=(",", ":")).encode("utf-8")
    request_sha256 = hashlib.sha256(request_canonical).hexdigest()
    execution_id = _promotion_execution_id(str(promotion_request.get("request_id")), approval_id)
    execution = {
        "schema_version": "cavra.go-runtime.endpoint-rollout-promotion-execution.v1",
        "product": "CAVRA",
        "execution_id": execution_id,
        "request_id": promotion_request.get("request_id"),
        "approval_id": approval_id,
        "rollout_id": rollout_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "executed_by": executed_by,
        "execution_environment": execution_environment or promotion_request.get("environment"),
        "execution_status": "executed",
        "change_record": promotion_request.get("change_record"),
        "release": promotion_request.get("release", {}),
        "deployment_targets": sorted(str(target) for target in promotion_request.get("deployment_targets", [])),
        "ring_advancement": {
            "from": promotion_request.get("current_ring"),
            "to": promotion_request.get("target_ring"),
            "previous_rollout_status": promotion_request.get("rollout_status"),
            "new_rollout_status": "promoted",
        },
        "approval": {
            "approval_id": approval_id,
            "state": approval.get("state"),
            "approver_group": approval.get("approver_group"),
            "decided_by": approval.get("decided_by"),
            "decided_at": approval.get("decided_at"),
            "decision_reason": approval.get("decision_reason"),
        },
        "controls": [
            "promotion-request-signature-verified",
            "approval-state-approved",
            "approval-bound-to-rollout",
            "ring-advancement-recorded",
        ],
        "request_sha256": request_sha256,
        "evidence_refs": [
            f"rollout://{rollout_id}",
            f"promotion-request://{promotion_request.get('request_id')}",
            f"approval://{approval_id}",
            f"change://{promotion_request.get('change_record', 'unassigned')}",
        ],
        "rollback_evidence_refs": promotion_request.get("rollback_evidence_refs", []),
    }
    if notes:
        execution["notes"] = notes
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        execution_path = output_dir / "rollout-promotion-execution.json"
        summary_path = output_dir / "rollout-promotion-execution.md"
        _write_release_json(execution_path, execution)
        summary_path.write_text(_promotion_execution_markdown_summary(execution), encoding="utf-8")
        files = [execution_path.name, summary_path.name]
    return ManagedEndpointRolloutPromotionExecutionResult(
        valid=True,
        warnings=warnings,
        rollout_id=rollout_id,
        execution=execution,
        files=files,
    )


def build_managed_endpoint_rollout_promotion_execution_metadata(
    execution: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    ring = execution.get("ring_advancement", {}) if isinstance(execution.get("ring_advancement"), dict) else {}
    approval = execution.get("approval", {}) if isinstance(execution.get("approval"), dict) else {}
    metadata = {
        "session_id": execution.get("execution_id"),
        "created_at": execution.get("created_at"),
        "signer": execution.get("executed_by", "release-manager"),
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 0,
        "metadata_kind": "rollout-promotion-execution",
        "rollout_id": execution.get("rollout_id"),
        "rollout_status": ring.get("new_rollout_status"),
        "promotion_execution_status": execution.get("execution_status"),
        "environment": execution.get("execution_environment"),
        "deployment_targets": execution.get("deployment_targets", []),
        "current_ring": ring.get("from"),
        "target_ring": ring.get("to"),
        "approval_id": execution.get("approval_id"),
        "approval_state": approval.get("state"),
        "request_id": execution.get("request_id"),
        "change_record": execution.get("change_record"),
        "release": execution.get("release", {}),
        "evidence_refs": execution.get("evidence_refs", []),
        "rollback_evidence_refs": execution.get("rollback_evidence_refs", []),
        "audit_links": {
            "rollout": f"rollout://{execution.get('rollout_id')}",
            "promotion_request": f"promotion-request://{execution.get('request_id')}",
            "approval": f"approval://{execution.get('approval_id')}",
            "change": f"change://{execution.get('change_record', 'unassigned')}",
        },
        "execution": execution,
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def create_managed_endpoint_rollout_rollback_execution(
    promotion_execution: dict[str, Any],
    approval: dict[str, Any],
    *,
    output_dir: Path | None = None,
    executed_by: str = "release-manager",
    rollback_reason: str = "Rollback approved from promotion execution audit.",
    execution_environment: str | None = None,
    notes: str | None = None,
) -> ManagedEndpointRolloutRollbackExecutionResult:
    errors: list[str] = []
    warnings: list[str] = []
    if promotion_execution.get("schema_version") != "cavra.go-runtime.endpoint-rollout-promotion-execution.v1":
        errors.append("promotion execution has an invalid schema_version")
    if promotion_execution.get("execution_status") != "executed":
        errors.append("rollback execution requires an executed promotion record")
    rollback_refs = promotion_execution.get("rollback_evidence_refs")
    if not isinstance(rollback_refs, list) or not rollback_refs:
        errors.append("rollback execution requires rollback evidence references")
    approval_id = str(approval.get("approval_id") or "")
    if not approval_id:
        errors.append("approval record must include approval_id")
    if approval.get("state") != "approved":
        errors.append("rollout rollback execution requires an approved approval record")
    if approval.get("session_id") != promotion_execution.get("rollout_id"):
        errors.append("approval session_id does not match rollout_id")
    decision = approval.get("decision", {})
    if not isinstance(decision, dict):
        errors.append("approval decision payload is invalid")
        decision = {}
    if decision.get("action_type") != "release_rollback_endpoint_rollout":
        errors.append("approval decision action_type does not authorize rollout rollback")
    metadata = decision.get("metadata", {}) if isinstance(decision.get("metadata"), dict) else {}
    if metadata.get("promotion_execution_id") and metadata.get("promotion_execution_id") != promotion_execution.get("execution_id"):
        errors.append("approval promotion_execution_id does not match promotion execution")
    if metadata.get("target_ring"):
        ring = promotion_execution.get("ring_advancement", {})
        if not isinstance(ring, dict) or metadata.get("target_ring") != ring.get("to"):
            errors.append("approval target ring does not match promoted ring")
    rollout_id = str(promotion_execution.get("rollout_id") or "")
    if errors:
        return ManagedEndpointRolloutRollbackExecutionResult(
            valid=False,
            errors=errors,
            warnings=warnings,
            rollout_id=rollout_id or None,
        )

    execution_canonical = json.dumps(promotion_execution, sort_keys=True, separators=(",", ":")).encode("utf-8")
    execution_sha256 = hashlib.sha256(execution_canonical).hexdigest()
    ring = promotion_execution.get("ring_advancement", {}) if isinstance(promotion_execution.get("ring_advancement"), dict) else {}
    rollback_id = _rollback_execution_id(str(promotion_execution.get("execution_id")), approval_id)
    rollback = {
        "schema_version": "cavra.go-runtime.endpoint-rollout-rollback-execution.v1",
        "product": "CAVRA",
        "rollback_id": rollback_id,
        "promotion_execution_id": promotion_execution.get("execution_id"),
        "approval_id": approval_id,
        "rollout_id": rollout_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "executed_by": executed_by,
        "execution_environment": execution_environment or promotion_execution.get("execution_environment"),
        "rollback_status": "executed",
        "rollback_reason": rollback_reason,
        "change_record": promotion_execution.get("change_record"),
        "release": promotion_execution.get("release", {}),
        "deployment_targets": sorted(str(target) for target in promotion_execution.get("deployment_targets", [])),
        "ring_rollback": {
            "from": ring.get("to"),
            "to": ring.get("from"),
            "previous_rollout_status": ring.get("new_rollout_status"),
            "new_rollout_status": "rolled_back",
        },
        "approval": {
            "approval_id": approval_id,
            "state": approval.get("state"),
            "approver_group": approval.get("approver_group"),
            "decided_by": approval.get("decided_by"),
            "decided_at": approval.get("decided_at"),
            "decision_reason": approval.get("decision_reason"),
        },
        "controls": [
            "rollback-approval-state-approved",
            "rollback-bound-to-promotion-execution",
            "rollback-evidence-references-present",
            "ring-rollback-recorded",
        ],
        "promotion_execution_sha256": execution_sha256,
        "evidence_refs": [
            f"rollout://{rollout_id}",
            f"promotion-execution://{promotion_execution.get('execution_id')}",
            f"approval://{approval_id}",
            f"change://{promotion_execution.get('change_record', 'unassigned')}",
        ],
        "rollback_evidence_refs": rollback_refs,
    }
    if notes:
        rollback["notes"] = notes
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        rollback_path = output_dir / "rollout-rollback-execution.json"
        summary_path = output_dir / "rollout-rollback-execution.md"
        _write_release_json(rollback_path, rollback)
        summary_path.write_text(_rollback_execution_markdown_summary(rollback), encoding="utf-8")
        files = [rollback_path.name, summary_path.name]
    return ManagedEndpointRolloutRollbackExecutionResult(
        valid=True,
        warnings=warnings,
        rollout_id=rollout_id,
        rollback=rollback,
        files=files,
    )


def build_managed_endpoint_rollout_rollback_execution_metadata(
    rollback: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    ring = rollback.get("ring_rollback", {}) if isinstance(rollback.get("ring_rollback"), dict) else {}
    approval = rollback.get("approval", {}) if isinstance(rollback.get("approval"), dict) else {}
    metadata = {
        "session_id": rollback.get("rollback_id"),
        "created_at": rollback.get("created_at"),
        "signer": rollback.get("executed_by", "release-manager"),
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 0,
        "metadata_kind": "rollout-rollback-execution",
        "rollout_id": rollback.get("rollout_id"),
        "rollout_status": ring.get("new_rollout_status"),
        "rollback_execution_status": rollback.get("rollback_status"),
        "environment": rollback.get("execution_environment"),
        "deployment_targets": rollback.get("deployment_targets", []),
        "current_ring": ring.get("from"),
        "target_ring": ring.get("to"),
        "approval_id": rollback.get("approval_id"),
        "approval_state": approval.get("state"),
        "promotion_execution_id": rollback.get("promotion_execution_id"),
        "change_record": rollback.get("change_record"),
        "release": rollback.get("release", {}),
        "evidence_refs": rollback.get("evidence_refs", []),
        "rollback_evidence_refs": rollback.get("rollback_evidence_refs", []),
        "audit_links": {
            "rollout": f"rollout://{rollback.get('rollout_id')}",
            "promotion_execution": f"promotion-execution://{rollback.get('promotion_execution_id')}",
            "approval": f"approval://{rollback.get('approval_id')}",
            "change": f"change://{rollback.get('change_record', 'unassigned')}",
        },
        "rollback": rollback,
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def export_rollout_promotion_execution_audit(
    promotion_execution: dict[str, Any],
    output_dir: Path,
    *,
    provider: str = "all",
    splunk_index: str = "cavra",
    datadog_service: str = "cavra",
    itsm_project_key: str = "CAVRA",
) -> ReleaseAuditExportResult:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    providers = {"splunk", "sentinel", "datadog", "webhook", "jira", "servicenow"} if provider == "all" else {provider}
    unknown = providers - {"splunk", "sentinel", "datadog", "webhook", "jira", "servicenow"}
    if unknown:
        raise ValueError(f"unknown rollout audit export provider: {', '.join(sorted(unknown))}")
    event = build_rollout_promotion_execution_audit_event(promotion_execution)
    files: list[Path] = []
    files.append(_write_release_json(output_dir / "promotion-execution-audit-event.json", event))
    if "splunk" in providers:
        files.append(_write_release_json(output_dir / "splunk-hec-events.json", {"events": [_promotion_splunk_event(event, splunk_index)]}))
    if "sentinel" in providers:
        files.append(_write_release_json(output_dir / "sentinel-log-analytics.json", {"records": [_promotion_sentinel_event(event)]}))
    if "datadog" in providers:
        files.append(_write_release_json(output_dir / "datadog-events.json", {"events": [_promotion_datadog_event(event, datadog_service)]}))
    if "webhook" in providers:
        files.append(_write_release_json(output_dir / "webhook-payload.json", _promotion_webhook_payload(event)))
    if "jira" in providers:
        files.append(_write_release_json(output_dir / "jira-issue.json", _promotion_jira_issue(event, itsm_project_key)))
    if "servicenow" in providers:
        files.append(_write_release_json(output_dir / "servicenow-change-task.json", _promotion_servicenow_task(event)))
    return ReleaseAuditExportResult(output_dir=output_dir, files=files)


def build_rollout_promotion_execution_audit_event(promotion_execution: dict[str, Any]) -> dict[str, Any]:
    if promotion_execution.get("schema_version") != "cavra.go-runtime.endpoint-rollout-promotion-execution.v1":
        raise ValueError("promotion execution has an invalid schema_version")
    ring = promotion_execution.get("ring_advancement", {}) if isinstance(promotion_execution.get("ring_advancement"), dict) else {}
    approval = promotion_execution.get("approval", {}) if isinstance(promotion_execution.get("approval"), dict) else {}
    rollback_refs = promotion_execution.get("rollback_evidence_refs", [])
    return {
        "schema_version": "cavra.rollout-promotion.audit-event.v1",
        "event_type": "cavra.rollout_promotion_execution",
        "product": "CAVRA",
        "timestamp": promotion_execution.get("created_at") or datetime.now(timezone.utc).isoformat(),
        "severity": "high",
        "execution_id": promotion_execution.get("execution_id"),
        "rollout_id": promotion_execution.get("rollout_id"),
        "request_id": promotion_execution.get("request_id"),
        "approval_id": promotion_execution.get("approval_id"),
        "approval_state": approval.get("state"),
        "change_record": promotion_execution.get("change_record"),
        "execution_status": promotion_execution.get("execution_status"),
        "environment": promotion_execution.get("execution_environment"),
        "current_ring": ring.get("from"),
        "target_ring": ring.get("to"),
        "release": promotion_execution.get("release", {}),
        "deployment_targets": promotion_execution.get("deployment_targets", []),
        "rollback_evidence_refs": rollback_refs,
        "rollback_reference_count": len(rollback_refs) if isinstance(rollback_refs, list) else 0,
        "audit_links": {
            "rollout": f"rollout://{promotion_execution.get('rollout_id')}",
            "promotion_request": f"promotion-request://{promotion_execution.get('request_id')}",
            "promotion_execution": f"promotion-execution://{promotion_execution.get('execution_id')}",
            "approval": f"approval://{promotion_execution.get('approval_id')}",
            "change": f"change://{promotion_execution.get('change_record', 'unassigned')}",
        },
        "controls": promotion_execution.get("controls", []),
        "raw_execution": promotion_execution,
    }


def build_rollout_rollback_execution_audit_event(rollback_execution: dict[str, Any]) -> dict[str, Any]:
    if rollback_execution.get("schema_version") != "cavra.go-runtime.endpoint-rollout-rollback-execution.v1":
        raise ValueError("rollback execution has an invalid schema_version")
    ring = rollback_execution.get("ring_rollback", {}) if isinstance(rollback_execution.get("ring_rollback"), dict) else {}
    approval = rollback_execution.get("approval", {}) if isinstance(rollback_execution.get("approval"), dict) else {}
    rollback_refs = rollback_execution.get("rollback_evidence_refs", [])
    return {
        "schema_version": "cavra.rollout-rollback.audit-event.v1",
        "event_type": "cavra.rollout_rollback_execution",
        "product": "CAVRA",
        "timestamp": rollback_execution.get("created_at") or datetime.now(timezone.utc).isoformat(),
        "severity": "critical",
        "rollback_id": rollback_execution.get("rollback_id"),
        "promotion_execution_id": rollback_execution.get("promotion_execution_id"),
        "rollout_id": rollback_execution.get("rollout_id"),
        "approval_id": rollback_execution.get("approval_id"),
        "approval_state": approval.get("state"),
        "change_record": rollback_execution.get("change_record"),
        "rollback_status": rollback_execution.get("rollback_status"),
        "rollback_reason": rollback_execution.get("rollback_reason"),
        "environment": rollback_execution.get("execution_environment"),
        "current_ring": ring.get("from"),
        "target_ring": ring.get("to"),
        "release": rollback_execution.get("release", {}),
        "deployment_targets": rollback_execution.get("deployment_targets", []),
        "rollback_evidence_refs": rollback_refs,
        "rollback_reference_count": len(rollback_refs) if isinstance(rollback_refs, list) else 0,
        "audit_links": {
            "rollout": f"rollout://{rollback_execution.get('rollout_id')}",
            "promotion_execution": f"promotion-execution://{rollback_execution.get('promotion_execution_id')}",
            "rollback_execution": f"rollback-execution://{rollback_execution.get('rollback_id')}",
            "approval": f"approval://{rollback_execution.get('approval_id')}",
            "change": f"change://{rollback_execution.get('change_record', 'unassigned')}",
        },
        "controls": rollback_execution.get("controls", []),
        "raw_rollback": rollback_execution,
    }


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


def verify_go_installer_metadata(
    installer_metadata_path: Path,
    package_dir: Path,
    expected_checksums: dict[str, str],
    evidence: dict[str, Any],
) -> list[str]:
    try:
        payload = json.loads(installer_metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid installer metadata JSON: {exc}") from exc
    if payload.get("schema_version") != "cavra.go-runtime.installers.v1":
        raise ReleaseVerificationError("installer metadata has an invalid schema_version")
    if evidence and payload.get("version") != evidence.get("version"):
        raise ReleaseVerificationError("installer metadata version does not match release evidence")
    targets = payload.get("targets")
    if not isinstance(targets, list) or not targets:
        raise ReleaseVerificationError("installer metadata has no targets")
    verified: list[str] = []
    seen_targets: set[str] = set()
    for target in targets:
        if not isinstance(target, dict):
            raise ReleaseVerificationError("installer metadata target is invalid")
        target_name = str(target.get("target", ""))
        if not target_name or target_name in seen_targets:
            raise ReleaseVerificationError(f"installer metadata target is missing or duplicated: {target_name or 'unknown'}")
        seen_targets.add(target_name)
        binary = str(target.get("binary", ""))
        binary_path = _safe_package_path(package_dir, binary)
        if binary_path is None or not binary_path.exists() or not binary_path.is_file():
            raise ReleaseVerificationError(f"installer metadata binary is missing: {binary}")
        actual_sha256 = sha256_file(binary_path)
        expected_sha256 = str(target.get("binary_sha256", "")).lower()
        if actual_sha256 != expected_sha256:
            raise ReleaseVerificationError(f"installer metadata digest mismatch for {binary}")
        checksum_sha256 = expected_checksums.get(binary)
        if checksum_sha256 and checksum_sha256 != expected_sha256:
            raise ReleaseVerificationError(f"installer metadata disagrees with checksums.txt: {binary}")
        if not target.get("install_path") or not target.get("install_method"):
            raise ReleaseVerificationError(f"installer metadata target is missing install guidance: {target_name}")
        if "sha256sum -c checksums.txt" not in str(target.get("verification_command", "")):
            raise ReleaseVerificationError(f"installer metadata target is missing checksum verification guidance: {target_name}")
        verified.append(binary)
    return sorted(verified)


def verify_managed_endpoint_deployment(
    endpoint_deployment_path: Path,
    package_dir: Path,
    expected_checksums: dict[str, str],
    evidence: dict[str, Any],
) -> list[str]:
    try:
        payload = json.loads(endpoint_deployment_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid endpoint deployment JSON: {exc}") from exc
    if payload.get("schema_version") != "cavra.go-runtime.endpoint-deployment.v1":
        raise ReleaseVerificationError("endpoint deployment metadata has an invalid schema_version")
    if evidence and payload.get("version") != evidence.get("version"):
        raise ReleaseVerificationError("endpoint deployment version does not match release evidence")
    if payload.get("source_metadata") != "cavra-runtime.installers.json":
        raise ReleaseVerificationError("endpoint deployment metadata must reference cavra-runtime.installers.json")

    installers_path = package_dir / "cavra-runtime.installers.json"
    try:
        installers = json.loads(installers_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ReleaseVerificationError("endpoint deployment metadata cannot load installer metadata") from exc
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid installer metadata JSON for endpoint deployment: {exc}") from exc
    installer_targets = {
        str(target.get("target")): target
        for target in installers.get("targets", [])
        if isinstance(target, dict) and target.get("target")
    }

    deployment_targets = payload.get("deployment_targets")
    if not isinstance(deployment_targets, list) or not deployment_targets:
        raise ReleaseVerificationError("endpoint deployment metadata has no deployment_targets")
    controls = payload.get("controls")
    if not isinstance(controls, list) or "smoke-installers-before-rollout" not in controls:
        raise ReleaseVerificationError("endpoint deployment metadata is missing smoke installer rollout control")

    verified: list[str] = []
    seen_ids: set[str] = set()
    for deployment in deployment_targets:
        if not isinstance(deployment, dict):
            raise ReleaseVerificationError("endpoint deployment target is invalid")
        deployment_id = str(deployment.get("id", ""))
        if not deployment_id or deployment_id in seen_ids:
            raise ReleaseVerificationError(f"endpoint deployment target is missing or duplicated: {deployment_id or 'unknown'}")
        seen_ids.add(deployment_id)
        installer_target = str(deployment.get("installer_target", ""))
        installer = installer_targets.get(installer_target)
        if not installer:
            raise ReleaseVerificationError(f"endpoint deployment target references unknown installer target: {installer_target}")
        binary = str(deployment.get("binary", ""))
        if binary != installer.get("binary"):
            raise ReleaseVerificationError(f"endpoint deployment binary does not match installer metadata: {deployment_id}")
        binary_path = _safe_package_path(package_dir, binary)
        if binary_path is None or not binary_path.exists() or not binary_path.is_file():
            raise ReleaseVerificationError(f"endpoint deployment binary is missing: {binary}")
        expected_sha256 = str(deployment.get("binary_sha256", "")).lower()
        if sha256_file(binary_path) != expected_sha256:
            raise ReleaseVerificationError(f"endpoint deployment digest mismatch for {binary}")
        checksum_sha256 = expected_checksums.get(binary)
        if checksum_sha256 and checksum_sha256 != expected_sha256:
            raise ReleaseVerificationError(f"endpoint deployment disagrees with checksums.txt: {binary}")
        required_fields = ("surface", "platform", "deployment_channel", "management_tool", "install_path", "install_command")
        if any(not deployment.get(field) for field in required_fields):
            raise ReleaseVerificationError(f"endpoint deployment target is missing deployment guidance: {deployment_id}")
        commands = deployment.get("verification_commands")
        if not isinstance(commands, list) or not commands:
            raise ReleaseVerificationError(f"endpoint deployment target is missing verification commands: {deployment_id}")
        command_text = "\n".join(str(command) for command in commands)
        if "cavra release verify-go-package" not in command_text:
            raise ReleaseVerificationError(f"endpoint deployment target is missing package verification guidance: {deployment_id}")
        if "cavra release smoke-installers" not in command_text:
            raise ReleaseVerificationError(f"endpoint deployment target is missing smoke installer guidance: {deployment_id}")
        verified.append(deployment_id)
    return sorted(verified)


def verify_release_channel_manifest(
    channel_manifest_path: Path,
    package_dir: Path,
    expected_checksums: dict[str, str],
    evidence: dict[str, Any],
) -> list[str]:
    payload = load_release_channel_manifest(channel_manifest_path)
    if evidence and payload.get("version") != evidence.get("version"):
        raise ReleaseVerificationError("channel manifest version does not match release evidence")
    if payload.get("source_metadata") != "cavra-runtime.endpoint-deployment.json":
        raise ReleaseVerificationError("channel manifest must reference cavra-runtime.endpoint-deployment.json")
    if payload.get("updater_policy") != "cavra-runtime.updater-policy.json":
        raise ReleaseVerificationError("channel manifest must reference cavra-runtime.updater-policy.json")
    channels = payload.get("channels")
    if not isinstance(channels, list) or not channels:
        raise ReleaseVerificationError("channel manifest has no channels")
    verified_channels: list[str] = []
    seen: set[str] = set()
    for channel in channels:
        if not isinstance(channel, dict):
            raise ReleaseVerificationError("channel manifest channel is invalid")
        channel_name = str(channel.get("channel", ""))
        if not channel_name or channel_name in seen:
            raise ReleaseVerificationError(f"channel manifest channel is missing or duplicated: {channel_name or 'unknown'}")
        seen.add(channel_name)
        if channel.get("auto_update") is not False or channel.get("approval_required") is not True:
            raise ReleaseVerificationError(f"channel {channel_name} must require approval and disable auto_update")
        controls = channel.get("controls")
        if not isinstance(controls, list) or "verify-go-package-before-channel-publish" not in controls:
            raise ReleaseVerificationError(f"channel {channel_name} is missing package verification controls")
        targets = channel.get("workstation_targets")
        if not isinstance(targets, list) or not targets:
            raise ReleaseVerificationError(f"channel {channel_name} has no workstation targets")
        commands = "\n".join(str(command) for command in channel.get("verification_commands", []))
        if "cavra release verify-go-package" not in commands:
            raise ReleaseVerificationError(f"channel {channel_name} is missing package verification command")
        if "cavra release smoke-installers" not in commands:
            raise ReleaseVerificationError(f"channel {channel_name} is missing installer smoke command")
        for target in targets:
            if not isinstance(target, dict):
                raise ReleaseVerificationError(f"channel {channel_name} workstation target is invalid")
            binary = str(target.get("binary", ""))
            binary_path = _safe_package_path(package_dir, binary)
            if binary_path is None or not binary_path.exists() or not binary_path.is_file():
                raise ReleaseVerificationError(f"channel {channel_name} binary is missing: {binary}")
            expected_sha256 = str(target.get("binary_sha256", "")).lower()
            if sha256_file(binary_path) != expected_sha256:
                raise ReleaseVerificationError(f"channel {channel_name} digest mismatch for {binary}")
            checksum_sha256 = expected_checksums.get(binary)
            if checksum_sha256 and checksum_sha256 != expected_sha256:
                raise ReleaseVerificationError(f"channel {channel_name} disagrees with checksums.txt: {binary}")
            required_fields = ("id", "platform", "installer_target", "deployment_channel", "management_tool")
            if any(not target.get(field) for field in required_fields):
                raise ReleaseVerificationError(f"channel {channel_name} target is missing deployment guidance")
        verified_channels.append(channel_name)
    return sorted(verified_channels)


def verify_workstation_updater_policy(
    updater_policy_path: Path,
    channel_manifest_path: Path,
    evidence: dict[str, Any],
) -> list[str]:
    policy = load_workstation_updater_policy(updater_policy_path)
    channel_manifest = load_release_channel_manifest(channel_manifest_path)
    if evidence and policy.get("version") != evidence.get("version"):
        raise ReleaseVerificationError("updater policy version does not match release evidence")
    if policy.get("source_channel_manifest") != "cavra-runtime.channels.json":
        raise ReleaseVerificationError("updater policy must reference cavra-runtime.channels.json")
    if policy.get("default_auto_update") is not False:
        raise ReleaseVerificationError("updater policy must disable default_auto_update")
    controls = policy.get("controls")
    if not isinstance(controls, list) or "manual-approval-before-auto-update" not in controls:
        raise ReleaseVerificationError("updater policy is missing manual approval control")
    policies = policy.get("policies")
    if not isinstance(policies, list) or not policies:
        raise ReleaseVerificationError("updater policy has no channel policies")
    manifest_channels = {
        str(channel.get("channel"))
        for channel in channel_manifest.get("channels", [])
        if isinstance(channel, dict) and channel.get("channel")
    }
    policy_channels = {str(item.get("channel")) for item in policies if isinstance(item, dict) and item.get("channel")}
    if policy_channels != manifest_channels:
        raise ReleaseVerificationError("updater policy channels must match channel manifest channels")
    verified: list[str] = []
    for item in policies:
        if not isinstance(item, dict):
            raise ReleaseVerificationError("updater channel policy is invalid")
        channel = str(item.get("channel", ""))
        if channel not in manifest_channels:
            raise ReleaseVerificationError(f"updater policy references unknown channel: {channel or 'unknown'}")
        if item.get("auto_update") is not False or item.get("approval_required") is not True:
            raise ReleaseVerificationError(f"updater policy channel {channel} must require approval and disable auto_update")
        rings = item.get("rollout_rings")
        if not isinstance(rings, list) or not rings:
            raise ReleaseVerificationError(f"updater policy channel {channel} has no rollout rings")
        rollback = item.get("rollback")
        if not isinstance(rollback, dict) or rollback.get("required") is not True:
            raise ReleaseVerificationError(f"updater policy channel {channel} must require rollback")
        verified.append(channel)
    return sorted(verified)


def load_release_channel_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid channel manifest JSON: {exc}") from exc
    if payload.get("schema_version") != "cavra.go-runtime.channels.v1":
        raise ReleaseVerificationError("channel manifest has an invalid schema_version")
    return payload


def load_workstation_updater_policy(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid updater policy JSON: {exc}") from exc
    if payload.get("schema_version") != "cavra.go-runtime.updater-policy.v1":
        raise ReleaseVerificationError("updater policy has an invalid schema_version")
    return payload


def _write_release_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _rollout_package_dir(payload: dict[str, Any]) -> Path | None:
    raw_package_dir = payload.get("package_dir")
    if not isinstance(raw_package_dir, str) or not raw_package_dir:
        return None
    package_dir = Path(raw_package_dir).expanduser().resolve()
    if not package_dir.exists() or not package_dir.is_dir():
        return None
    return package_dir


def _default_rollout_id(environment: str, release_evidence: dict[str, Any]) -> str:
    version = str(release_evidence.get("version") or "unknown").replace("/", "-")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{environment}-{version}-{timestamp}"


def _rollout_target_payload(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": target.get("id"),
        "surface": target.get("surface"),
        "platform": target.get("platform"),
        "installer_target": target.get("installer_target"),
        "binary": target.get("binary"),
        "binary_sha256": target.get("binary_sha256"),
        "deployment_channel": target.get("deployment_channel"),
        "management_tool": target.get("management_tool"),
        "install_path": target.get("install_path"),
        "rollout_gate": target.get("rollout_gate"),
        "verification_commands": target.get("verification_commands", []),
        "rollback_steps": target.get("rollback_steps", []),
        "evidence_required": target.get("evidence_required", []),
    }


def _rollout_markdown_summary(payload: dict[str, Any]) -> str:
    release = payload["release"]
    lines = [
        "# CAVRA Managed Endpoint Rollout Evidence",
        "",
        f"Rollout ID: `{payload['rollout_id']}`",
        f"Environment: `{payload['environment']}`",
        f"Ring: `{payload['rollout_ring']}`",
        f"Status: `{payload['status']}`",
        f"Change record: `{payload['change_record']}`",
        f"Version: `{release.get('version')}`",
        f"Commit: `{release.get('commit')}`",
        "",
        "## Deployment Targets",
        "",
    ]
    for target in payload["deployment_targets"]:
        lines.append(
            f"- `{target['id']}` `{target['surface']}` `{target['installer_target']}` via `{target['deployment_channel']}`"
        )
    lines.extend(["", "## Controls", ""])
    for control in payload["controls"]:
        lines.append(f"- `{control}`")
    lines.extend(["", "## Source Artifacts", ""])
    for artifact in payload["source_artifacts"].values():
        lines.append(f"- `{artifact['path']}` `{artifact['sha256']}`")
    return "\n".join(lines) + "\n"


def _promotion_request_id(rollout_id: str, target_ring: str) -> str:
    digest = hashlib.sha256(f"{rollout_id}:{target_ring}".encode("utf-8")).hexdigest()[:12]
    return f"rpr_{digest}"


def _release_channel_promotion_id(channel: str, version: str, target_ring: str) -> str:
    digest = hashlib.sha256(f"{channel}:{version}:{target_ring}".encode("utf-8")).hexdigest()[:12]
    return f"rcp_{digest}"


def _promotion_execution_id(request_id: str, approval_id: str) -> str:
    digest = hashlib.sha256(f"{request_id}:{approval_id}".encode("utf-8")).hexdigest()[:12]
    return f"rpe_{digest}"


def _rollback_execution_id(promotion_execution_id: str, approval_id: str) -> str:
    digest = hashlib.sha256(f"{promotion_execution_id}:{approval_id}".encode("utf-8")).hexdigest()[:12]
    return f"rre_{digest}"


def _endpoint_remediation_request_id(reconciliation_id: str, actions: list[dict[str, Any]], strategy: str) -> str:
    material = json.dumps(
        {"reconciliation_id": reconciliation_id, "strategy": strategy, "actions": actions},
        sort_keys=True,
        default=str,
    )
    return f"err_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_remediation_execution_id(request_id: str, approval_id: str) -> str:
    digest = hashlib.sha256(f"{request_id}:{approval_id}".encode("utf-8")).hexdigest()[:12]
    return f"ere_{digest}"


def _rollback_evidence_refs(rollout_id: str, deployment_targets: Any) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    if not isinstance(deployment_targets, list):
        return refs
    for target in deployment_targets:
        if not isinstance(target, dict):
            continue
        target_id = str(target.get("id") or "unknown-target")
        for index, step in enumerate(target.get("rollback_steps", []) or [], start=1):
            refs.append(
                {
                    "target": target_id,
                    "ref": f"rollback://{rollout_id}/{target_id}/{index}",
                    "step": str(step),
                }
            )
    return refs


def _managed_endpoint_reconciliation_report(
    desired_manifest: dict[str, Any],
    observed_inventory: dict[str, Any],
    desired_targets: list[dict[str, Any]],
    observations: list[dict[str, Any]],
    *,
    stale_after_hours: int,
    package_verification: dict[str, Any] | None,
) -> dict[str, Any]:
    created_at = datetime.now(timezone.utc).isoformat()
    release = {
        "version": desired_manifest.get("version"),
        "commit": desired_manifest.get("commit"),
        "repository": desired_manifest.get("repository"),
    }
    desired_by_id = {str(target["id"]): target for target in desired_targets}
    observed_by_target: dict[str, list[dict[str, Any]]] = {}
    for endpoint in observations:
        target_id = str(endpoint.get("deployment_target") or endpoint.get("target_id") or "")
        if target_id:
            observed_by_target.setdefault(target_id, []).append(endpoint)
    drift_items: list[dict[str, Any]] = []
    compliant = 0
    stale = 0
    now = datetime.now(timezone.utc)
    for target_id, target in sorted(desired_by_id.items()):
        target_observations = observed_by_target.get(target_id, [])
        if not target_observations:
            drift_items.append(
                {
                    "type": "missing_observation",
                    "severity": "critical",
                    "deployment_target": target_id,
                    "expected_version": release.get("version"),
                    "expected_binary_sha256": target.get("binary_sha256"),
                    "message": f"No observed endpoints reported for deployment target {target_id}.",
                }
            )
            continue
        for endpoint in target_observations:
            endpoint_id = str(endpoint.get("endpoint_id") or endpoint.get("id") or "unknown-endpoint")
            endpoint_drift: list[str] = []
            observed_version = endpoint.get("installed_version") or endpoint.get("version")
            observed_sha256 = endpoint.get("binary_sha256") or endpoint.get("installed_binary_sha256")
            if release.get("version") and observed_version and observed_version != release.get("version"):
                endpoint_drift.append("version_drift")
            if target.get("binary_sha256") and observed_sha256 and observed_sha256 != target.get("binary_sha256"):
                endpoint_drift.append("binary_drift")
            last_seen_at = str(endpoint.get("last_seen_at") or "")
            if _endpoint_observation_is_stale(last_seen_at, now=now, stale_after_hours=stale_after_hours):
                endpoint_drift.append("stale_observation")
                stale += 1
            if endpoint_drift:
                drift_items.append(
                    {
                        "type": ",".join(endpoint_drift),
                        "severity": "critical" if {"version_drift", "binary_drift"} & set(endpoint_drift) else "warning",
                        "endpoint_id": endpoint_id,
                        "deployment_target": target_id,
                        "expected_version": release.get("version"),
                        "observed_version": observed_version,
                        "expected_binary_sha256": target.get("binary_sha256"),
                        "observed_binary_sha256": observed_sha256,
                        "last_seen_at": last_seen_at,
                        "message": f"Endpoint {endpoint_id} is not aligned with deployment target {target_id}.",
                    }
                )
            else:
                compliant += 1
    unknown_targets = sorted(set(observed_by_target) - set(desired_by_id))
    for target_id in unknown_targets:
        for endpoint in observed_by_target[target_id]:
            drift_items.append(
                {
                    "type": "unknown_deployment_target",
                    "severity": "warning",
                    "endpoint_id": str(endpoint.get("endpoint_id") or endpoint.get("id") or "unknown-endpoint"),
                    "deployment_target": target_id,
                    "observed_version": endpoint.get("installed_version") or endpoint.get("version"),
                    "message": f"Endpoint reported deployment target {target_id}, which is not in the signed manifest.",
                }
            )
    missing_target_count = sum(1 for item in drift_items if item.get("type") == "missing_observation")
    drifted_endpoint_count = sum(1 for item in drift_items if item.get("endpoint_id") and item.get("severity") == "critical")
    alert_level = "critical" if drifted_endpoint_count or missing_target_count else "warning" if stale or unknown_targets else "healthy"
    drift_status = "drift_detected" if alert_level in {"critical", "warning"} else "aligned"
    observed_at = observed_inventory.get("observed_at") or created_at
    reconciliation_id = _managed_endpoint_reconciliation_id(desired_manifest, observed_inventory, observed_at)
    return {
        "schema_version": "cavra.endpoint-reconciliation.v1",
        "product": "CAVRA",
        "component": "go-enforcement-plane",
        "reconciliation_id": reconciliation_id,
        "created_at": created_at,
        "observed_at": observed_at,
        "drift_status": drift_status,
        "alert_level": alert_level,
        "release": release,
        "channel": observed_inventory.get("channel"),
        "deployment_targets": sorted(desired_by_id),
        "summary": {
            "desired_target_count": len(desired_targets),
            "observed_endpoint_count": len(observations),
            "compliant_endpoint_count": compliant,
            "drifted_endpoint_count": drifted_endpoint_count,
            "missing_target_count": missing_target_count,
            "unknown_target_count": len(unknown_targets),
            "stale_endpoint_count": stale,
        },
        "desired_manifest": desired_manifest,
        "observed_inventory": observed_inventory,
        "drift_items": drift_items,
        "controls": [
            "signed-endpoint-deployment-manifest-compared",
            "observed-endpoint-inventory-normalized",
            "runtime-version-drift-detected",
            "binary-checksum-drift-detected",
            "stale-endpoint-observations-flagged",
        ],
        "package_verification": package_verification,
    }


def _managed_endpoint_reconciliation_id(
    desired_manifest: dict[str, Any],
    observed_inventory: dict[str, Any],
    observed_at: object,
) -> str:
    material = json.dumps(
        {
            "version": desired_manifest.get("version"),
            "commit": desired_manifest.get("commit"),
            "observed_at": observed_at,
            "endpoints": observed_inventory.get("endpoints", []),
        },
        sort_keys=True,
        default=str,
    )
    return f"mer_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_observation_is_stale(last_seen_at: str, *, now: datetime, stale_after_hours: int) -> bool:
    if not last_seen_at:
        return False
    try:
        observed = datetime.fromisoformat(last_seen_at.replace("Z", "+00:00"))
    except ValueError:
        return True
    if observed.tzinfo is None:
        observed = observed.replace(tzinfo=timezone.utc)
    return (now - observed).total_seconds() > stale_after_hours * 3600


def _managed_endpoint_reconciliation_markdown_summary(report: dict[str, Any]) -> str:
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    lines = [
        "# Managed Endpoint Reconciliation",
        "",
        f"- Reconciliation ID: `{report.get('reconciliation_id')}`",
        f"- Status: `{report.get('drift_status')}`",
        f"- Alert level: `{report.get('alert_level')}`",
        f"- Desired targets: {summary.get('desired_target_count', 0)}",
        f"- Observed endpoints: {summary.get('observed_endpoint_count', 0)}",
        f"- Compliant endpoints: {summary.get('compliant_endpoint_count', 0)}",
        f"- Drifted endpoints: {summary.get('drifted_endpoint_count', 0)}",
        f"- Missing targets: {summary.get('missing_target_count', 0)}",
        f"- Stale endpoints: {summary.get('stale_endpoint_count', 0)}",
        "",
        "## Drift Items",
    ]
    drift_items = [item for item in report.get("drift_items", []) if isinstance(item, dict)]
    if not drift_items:
        lines.append("- No drift detected.")
    for item in drift_items:
        lines.append(
            f"- `{item.get('severity')}` `{item.get('type')}` target `{item.get('deployment_target')}` "
            f"endpoint `{item.get('endpoint_id', 'n/a')}`: {item.get('message')}"
        )
    return "\n".join(lines) + "\n"


def _endpoint_drift_remediation_actions(report: dict[str, Any], *, strategy: str) -> list[dict[str, Any]]:
    desired_manifest = report.get("desired_manifest", {}) if isinstance(report.get("desired_manifest"), dict) else {}
    targets = desired_manifest.get("deployment_targets", [])
    targets_by_id = {str(target.get("id")): target for target in targets if isinstance(target, dict) and target.get("id")}
    actions: list[dict[str, Any]] = []
    for index, item in enumerate(report.get("drift_items", []) or [], start=1):
        if not isinstance(item, dict):
            continue
        drift_type = str(item.get("type") or "unknown")
        target_id = str(item.get("deployment_target") or "unknown-target")
        target = targets_by_id.get(target_id, {})
        provider = _endpoint_provider_for_target(target) if target else "unknown"
        action_type = _endpoint_remediation_action_type(drift_type, strategy)
        action_material = f"{report.get('reconciliation_id')}:{index}:{drift_type}:{target_id}:{item.get('endpoint_id')}"
        action_id = f"era_{hashlib.sha256(action_material.encode('utf-8')).hexdigest()[:12]}"
        actions.append(
            {
                "action_id": action_id,
                "action_type": action_type,
                "deployment_target": target_id,
                "endpoint_id": item.get("endpoint_id"),
                "provider": provider,
                "severity": item.get("severity", "warning"),
                "drift_type": drift_type,
                "expected_version": item.get("expected_version"),
                "observed_version": item.get("observed_version"),
                "expected_binary_sha256": item.get("expected_binary_sha256"),
                "observed_binary_sha256": item.get("observed_binary_sha256"),
                "execution_mode": "manual_or_private_connector",
                "requires_approval": True,
                "message": item.get("message"),
                "rationale": _endpoint_remediation_rationale(action_type, item),
            }
        )
    return actions


def _endpoint_remediation_action_type(drift_type: str, strategy: str) -> str:
    drift_parts = {part.strip() for part in drift_type.split(",") if part.strip()}
    if "missing_observation" in drift_parts:
        return "republish_endpoint_export"
    if "unknown_deployment_target" in drift_parts:
        return "review_unknown_endpoint_target"
    if "stale_observation" in drift_parts and not {"version_drift", "binary_drift"} & drift_parts:
        return "refresh_endpoint_inventory"
    if {"version_drift", "binary_drift"} & drift_parts:
        if strategy == "rollback":
            return "rollback_runtime"
        if strategy == "republish":
            return "republish_endpoint_export"
        return "republish_or_rollback_runtime"
    return "review_endpoint_drift"


def _endpoint_remediation_rationale(action_type: str, item: dict[str, Any]) -> str:
    if action_type == "republish_endpoint_export":
        return "Republish the governed endpoint-management export for the target and verify the next inventory observation."
    if action_type == "rollback_runtime":
        return "Rollback the runtime on the affected endpoint or target to the last approved deployment state."
    if action_type == "refresh_endpoint_inventory":
        return "Refresh endpoint inventory before mutating deployment state because the observation is stale."
    if action_type == "review_unknown_endpoint_target":
        return "Review or quarantine the endpoint target because it is not present in the signed deployment manifest."
    return str(item.get("message") or "Review the drift item before remediation.")


def _endpoint_remediation_action_result(action: dict[str, Any]) -> dict[str, Any]:
    return {
        "action_id": action.get("action_id"),
        "action_type": action.get("action_type"),
        "deployment_target": action.get("deployment_target"),
        "endpoint_id": action.get("endpoint_id"),
        "provider": action.get("provider"),
        "status": "queued_for_private_connector_or_manual_execution",
        "public_boundary": "Community Edition records approval and evidence only; endpoint mutation requires private connector implementation.",
        "evidence_ref": f"endpoint-remediation-action://{action.get('action_id')}",
    }


def _endpoint_remediation_request_markdown_summary(request: dict[str, Any]) -> str:
    approval = request.get("approval", {}) if isinstance(request.get("approval"), dict) else {}
    lines = [
        "# Endpoint Drift Remediation Request",
        "",
        f"- Request ID: `{request.get('request_id')}`",
        f"- Reconciliation ID: `{request.get('reconciliation_id')}`",
        f"- Strategy: `{request.get('strategy')}`",
        f"- Approval ID: `{approval.get('approval_id')}`",
        f"- Approval state: `{approval.get('state')}`",
        f"- Action count: {request.get('action_count', 0)}",
        "",
        "## Actions",
    ]
    actions = [item for item in request.get("actions", []) if isinstance(item, dict)]
    if not actions:
        lines.append("- No remediation actions were planned.")
    for action in actions:
        lines.append(
            f"- `{action.get('action_type')}` target `{action.get('deployment_target')}` "
            f"endpoint `{action.get('endpoint_id', 'n/a')}`: {action.get('rationale')}"
        )
    lines.extend(
        [
            "",
            "Community Edition records the approved remediation plan. Endpoint mutation is performed by private connectors or an operator runbook.",
        ]
    )
    return "\n".join(lines) + "\n"


def _endpoint_remediation_execution_markdown_summary(execution: dict[str, Any]) -> str:
    approval = execution.get("approval", {}) if isinstance(execution.get("approval"), dict) else {}
    lines = [
        "# Endpoint Drift Remediation Execution",
        "",
        f"- Execution ID: `{execution.get('execution_id')}`",
        f"- Request ID: `{execution.get('request_id')}`",
        f"- Reconciliation ID: `{execution.get('reconciliation_id')}`",
        f"- Status: `{execution.get('execution_status')}`",
        f"- Approval ID: `{approval.get('approval_id')}`",
        f"- Approved by: `{approval.get('decided_by')}`",
        "",
        "## Action Results",
    ]
    results = [item for item in execution.get("action_results", []) if isinstance(item, dict)]
    if not results:
        lines.append("- No remediation actions were recorded.")
    for result in results:
        lines.append(
            f"- `{result.get('status')}` `{result.get('action_type')}` target `{result.get('deployment_target')}` "
            f"endpoint `{result.get('endpoint_id', 'n/a')}`"
        )
    return "\n".join(lines) + "\n"


def _select_release_channel(channel_manifest: dict[str, Any], channel: str) -> dict[str, Any]:
    for item in channel_manifest.get("channels", []):
        if isinstance(item, dict) and item.get("channel") == channel:
            return item
    raise ReleaseVerificationError(f"release channel not found: {channel}")


def _select_updater_channel_policy(updater_policy: dict[str, Any], channel: str) -> dict[str, Any]:
    for item in updater_policy.get("policies", []):
        if isinstance(item, dict) and item.get("channel") == channel:
            return item
    raise ReleaseVerificationError(f"updater policy channel not found: {channel}")


def _endpoint_export_providers(provider: str) -> list[str]:
    providers = {"jamf", "intune", "linux"}
    if provider == "all":
        return sorted(providers)
    normalized = provider.lower()
    return [normalized] if normalized in providers else []


def _endpoint_management_export_id(manifest: dict[str, Any]) -> str:
    approval = manifest.get("approval", {}) if isinstance(manifest.get("approval"), dict) else {}
    release = manifest.get("release", {}) if isinstance(manifest.get("release"), dict) else {}
    channel = str(manifest.get("channel") or "unknown")
    version = str(release.get("version") or "unknown")
    providers = sorted(str(provider) for provider in manifest.get("providers", []) if isinstance(provider, str))
    digest_material = f"{channel}:{version}:{','.join(providers)}:{approval.get('approval_id')}"
    return f"eme_{hashlib.sha256(digest_material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_management_publication_id(
    manifest: dict[str, Any],
    providers: list[str],
    export_id: str,
) -> str:
    channel = str(manifest.get("channel") or "unknown")
    release = manifest.get("release", {}) if isinstance(manifest.get("release"), dict) else {}
    digest_material = f"{export_id}:{channel}:{release.get('version')}:{','.join(sorted(providers))}"
    return f"emp_{hashlib.sha256(digest_material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_management_publication_delivery_id(delivery: dict[str, Any]) -> str:
    event_id = str(delivery.get("event_id") or delivery.get("session_id") or "endpoint-publication")
    generated_at = str(delivery.get("generated_at") or datetime.now(timezone.utc).isoformat())
    providers = ",".join(str(item.get("provider")) for item in delivery.get("deliveries", []) if isinstance(item, dict))
    digest = hashlib.sha256(f"{event_id}|{generated_at}|{providers}".encode("utf-8")).hexdigest()[:12]
    return f"epd-{_release_slug(event_id) or 'endpoint-publication'}-{digest}"


def _endpoint_management_publication_artifacts(
    manifest: dict[str, Any],
    providers: list[str],
    *,
    export_dir: Path | None,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[str]]:
    artifact_names = {"endpoint-management-export-manifest.json", "endpoint-management-export-manifest.md", "checksums.txt"}
    for provider in providers:
        artifact_names.update(_endpoint_publication_provider_artifacts(provider))
    checksums: dict[str, str] = {}
    errors: list[str] = []
    if export_dir:
        export_dir = export_dir.resolve()
        checksums_path = export_dir / "checksums.txt"
        if not checksums_path.exists():
            errors.append("endpoint-management export checksums.txt is missing")
        else:
            try:
                checksums = _parse_checksums(checksums_path)
            except ReleaseVerificationError as exc:
                errors.append(str(exc))
    artifacts: list[dict[str, Any]] = []
    provider_payloads: dict[str, dict[str, Any]] = {}
    for artifact_name in sorted(artifact_names):
        item: dict[str, Any] = {"artifact": artifact_name}
        if export_dir:
            path = _safe_package_path(export_dir, artifact_name)
            if path is None:
                errors.append(f"endpoint export artifact path escapes export directory: {artifact_name}")
                continue
            if not path.exists() or not path.is_file():
                errors.append(f"endpoint export artifact is missing: {artifact_name}")
                continue
            actual_sha256 = sha256_file(path)
            expected_sha256 = checksums.get(artifact_name)
            if artifact_name != "checksums.txt":
                if not expected_sha256:
                    errors.append(f"endpoint export artifact missing from checksums.txt: {artifact_name}")
                elif actual_sha256 != expected_sha256:
                    errors.append(f"endpoint export artifact checksum mismatch: {artifact_name}")
            item |= {"sha256": actual_sha256, "bytes": path.stat().st_size}
        artifacts.append(item)
    for provider in providers:
        payload_path = _endpoint_publication_provider_payload_path(provider)
        if not export_dir:
            provider_payloads[provider] = {
                "schema_version": f"cavra.endpoint-management.{provider}.publication.v1",
                "provider": provider,
                "manifest": manifest,
            }
            continue
        provider_payloads[provider] = _load_endpoint_publication_provider_payload(export_dir / payload_path, provider, manifest)
    return artifacts, provider_payloads, errors


def _endpoint_publication_provider_artifacts(provider: str) -> list[str]:
    if provider == "jamf":
        return ["jamf-policy.json"]
    if provider == "intune":
        return ["intune-win32-app.json"]
    if provider == "linux":
        return ["linux-fleet-manifest.json", "linux-install-cavra-runtime.sh"]
    return []


def _endpoint_publication_provider_payload_path(provider: str) -> str:
    if provider == "jamf":
        return "jamf-policy.json"
    if provider == "intune":
        return "intune-win32-app.json"
    if provider == "linux":
        return "linux-fleet-manifest.json"
    return "endpoint-management-export-manifest.json"


def _load_endpoint_publication_provider_payload(path: Path, provider: str, manifest: dict[str, Any]) -> dict[str, Any]:
    if path.suffix == ".json" and path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return payload | {"publication_context": {"provider": provider, "channel": manifest.get("channel")}}
    return {
        "schema_version": f"cavra.endpoint-management.{provider}.publication.v1",
        "provider": provider,
        "manifest": manifest,
    }


def _release_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _endpoint_provider_for_target(target: dict[str, Any]) -> str:
    management_tool = str(target.get("management_tool", "")).lower()
    deployment_channel = str(target.get("deployment_channel", "")).lower()
    os_name = str(target.get("os", "")).lower()
    if "jamf" in management_tool or "jamf" in deployment_channel:
        return "jamf"
    if "intune" in management_tool or "intune" in deployment_channel:
        return "intune"
    if os_name == "linux" or "linux" in management_tool:
        return "linux"
    return "unknown"


def _write_jamf_export(
    output_dir: Path,
    channel: str,
    targets: list[dict[str, Any]],
    channel_policy: dict[str, Any],
) -> list[Path]:
    payload = {
        "schema_version": "cavra.endpoint-management.jamf.v1",
        "provider": "jamf",
        "channel": channel,
        "policy_name": f"CAVRA Go Runtime {channel}",
        "trigger": f"cavra-runtime-{channel}",
        "approval_required": True,
        "rollback_required": True,
        "soak_hours": _first_ring_soak_hours(channel_policy),
        "targets": [_endpoint_target_export(target) for target in targets],
        "install_script": [
            "#!/bin/bash",
            "set -euo pipefail",
            "install -m 0755 cavra-runtime /usr/local/bin/cavra-runtime",
            "sha256sum -c checksums.txt",
        ],
    }
    path = output_dir / "jamf-policy.json"
    _write_release_json(path, payload)
    return [path]


def _write_intune_export(
    output_dir: Path,
    channel: str,
    targets: list[dict[str, Any]],
    channel_policy: dict[str, Any],
) -> list[Path]:
    payload = {
        "schema_version": "cavra.endpoint-management.intune.v1",
        "provider": "intune",
        "channel": channel,
        "display_name": f"CAVRA Go Runtime {channel}",
        "install_behavior": "system",
        "approval_required": True,
        "rollback_required": True,
        "soak_hours": _first_ring_soak_hours(channel_policy),
        "targets": [_endpoint_target_export(target) for target in targets],
        "install_command": "powershell.exe -ExecutionPolicy Bypass -File install-cavra-runtime.ps1",
        "uninstall_command": "powershell.exe -ExecutionPolicy Bypass -File rollback-cavra-runtime.ps1",
        "detection_rule": {
            "type": "file_sha256",
            "path": "%ProgramFiles%\\CAVRA\\cavra-runtime.exe",
            "sha256_values": sorted(str(target.get("binary_sha256")) for target in targets if target.get("binary_sha256")),
        },
    }
    path = output_dir / "intune-win32-app.json"
    _write_release_json(path, payload)
    return [path]


def _write_linux_export(
    output_dir: Path,
    channel: str,
    targets: list[dict[str, Any]],
    channel_policy: dict[str, Any],
) -> list[Path]:
    manifest = {
        "schema_version": "cavra.endpoint-management.linux.v1",
        "provider": "linux",
        "channel": channel,
        "approval_required": True,
        "rollback_required": True,
        "soak_hours": _first_ring_soak_hours(channel_policy),
        "targets": [_endpoint_target_export(target) for target in targets],
    }
    manifest_path = output_dir / "linux-fleet-manifest.json"
    script_path = output_dir / "linux-install-cavra-runtime.sh"
    _write_release_json(manifest_path, manifest)
    script_path.write_text(
        "\n".join(
            [
                "#!/bin/sh",
                "set -eu",
                "install -m 0755 cavra-runtime /usr/local/bin/cavra-runtime",
                "sha256sum -c checksums.txt",
                "systemctl restart cavra-runtime.service 2>/dev/null || true",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return [manifest_path, script_path]


def _endpoint_target_export(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": target.get("id"),
        "platform": target.get("platform"),
        "os": target.get("os"),
        "arch": target.get("arch"),
        "installer_target": target.get("installer_target"),
        "binary": target.get("binary"),
        "binary_sha256": target.get("binary_sha256"),
        "deployment_channel": target.get("deployment_channel"),
        "management_tool": target.get("management_tool"),
    }


def _first_ring_soak_hours(channel_policy: dict[str, Any]) -> int | None:
    rings = channel_policy.get("rollout_rings")
    if not isinstance(rings, list) or not rings:
        return None
    first = rings[0]
    if not isinstance(first, dict):
        return None
    value = first.get("soak_hours")
    return int(value) if isinstance(value, int) else None


def _sign_json_payload_ed25519(
    payload: dict[str, Any],
    private_key_pem: str,
    *,
    signer: str,
    signature_schema: str = "cavra.rollout-promotion.signature.v1",
) -> dict[str, Any]:
    try:
        from cryptography.hazmat.primitives import serialization
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install cryptography to sign rollout promotion requests.") from exc
    unsigned = {key: value for key, value in payload.items() if key != "signature"}
    canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")
    private_key = serialization.load_pem_private_key(private_key_pem.encode("utf-8"), password=None)
    signature = private_key.sign(canonical)
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    public_key_sha256 = hashlib.sha256(public_key).hexdigest()
    return {
        "schema_version": signature_schema,
        "algorithm": "Ed25519",
        "signer": signer,
        "key_id": public_key_sha256[:16],
        "public_key_sha256": public_key_sha256,
        "public_key_pem": public_key.decode("utf-8"),
        "payload_sha256": hashlib.sha256(canonical).hexdigest(),
        "value": base64.b64encode(signature).decode("ascii"),
    }


def verify_rollout_promotion_request_signature(payload: dict[str, Any]) -> None:
    _verify_json_payload_ed25519(
        payload,
        expected_schema="cavra.rollout-promotion.signature.v1",
        label="rollout promotion request",
    )


def verify_release_channel_promotion_request_signature(payload: dict[str, Any]) -> None:
    _verify_json_payload_ed25519(
        payload,
        expected_schema="cavra.release-channel-promotion.signature.v1",
        label="release channel promotion request",
    )


def _verify_json_payload_ed25519(payload: dict[str, Any], *, expected_schema: str, label: str) -> None:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import serialization
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(f"Install cryptography to verify {label} signatures.") from exc
    signature = payload.get("signature")
    if not isinstance(signature, dict):
        raise ReleaseVerificationError(f"{label} is missing signature")
    if signature.get("schema_version") != expected_schema:
        raise ReleaseVerificationError(f"{label} signature has an invalid schema_version")
    if signature.get("algorithm") != "Ed25519":
        raise ReleaseVerificationError(f"{label} signature must use Ed25519")
    public_key_pem = str(signature.get("public_key_pem", "")).encode("utf-8")
    if not public_key_pem:
        raise ReleaseVerificationError(f"{label} signature is missing public_key_pem")
    if hashlib.sha256(public_key_pem).hexdigest() != signature.get("public_key_sha256"):
        raise ReleaseVerificationError(f"{label} public key fingerprint mismatch")
    unsigned = {key: value for key, value in payload.items() if key != "signature"}
    canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if hashlib.sha256(canonical).hexdigest() != signature.get("payload_sha256"):
        raise ReleaseVerificationError(f"{label} payload digest mismatch")
    try:
        value = base64.b64decode(str(signature.get("value", "")), validate=True)
    except ValueError as exc:
        raise ReleaseVerificationError(f"{label} signature has invalid base64") from exc
    public_key = serialization.load_pem_public_key(public_key_pem)
    try:
        public_key.verify(value, canonical)
    except InvalidSignature as exc:
        raise ReleaseVerificationError(f"{label} signature is invalid") from exc


def _promotion_request_markdown_summary(payload: dict[str, Any]) -> str:
    approval = payload.get("approval", {})
    release = payload.get("release", {})
    lines = [
        "# CAVRA Rollout Promotion Approval Request",
        "",
        f"Request ID: `{payload.get('request_id')}`",
        f"Rollout ID: `{payload.get('rollout_id')}`",
        f"Current ring: `{payload.get('current_ring')}`",
        f"Target ring: `{payload.get('target_ring')}`",
        f"Status: `{payload.get('rollout_status')}`",
        f"Change record: `{payload.get('change_record')}`",
        f"Version: `{release.get('version')}`",
        f"Approval ID: `{approval.get('approval_id')}`",
        f"Approver group: `{approval.get('approver_group')}`",
        "",
        "## Deployment Targets",
        "",
    ]
    for target in payload.get("deployment_targets", []):
        lines.append(f"- `{target}`")
    lines.extend(["", "## Verified Artifacts", ""])
    for artifact in payload.get("verified_artifacts", []):
        lines.append(f"- `{artifact}`")
    lines.extend(
        [
            "",
            "## Signature",
            "",
            f"Algorithm: `{payload.get('signature', {}).get('algorithm')}`",
            f"Signer: `{payload.get('signature', {}).get('signer')}`",
            f"Payload SHA-256: `{payload.get('signature', {}).get('payload_sha256')}`",
        ]
    )
    return "\n".join(lines) + "\n"


def _release_channel_promotion_markdown_summary(payload: dict[str, Any]) -> str:
    approval = payload.get("approval", {})
    release = payload.get("release", {})
    channel_manifest = payload.get("channel_manifest", {})
    updater_policy = payload.get("updater_policy", {})
    lines = [
        "# CAVRA Release Channel Promotion Request",
        "",
        f"Request ID: `{payload.get('request_id')}`",
        f"Channel: `{payload.get('channel')}`",
        f"Target ring: `{payload.get('target_ring')}`",
        f"Version: `{release.get('version')}`",
        f"Commit: `{release.get('commit')}`",
        f"Approval ID: `{approval.get('approval_id')}`",
        f"Approver group: `{approval.get('approver_group')}`",
        "",
        "## Source Artifacts",
        "",
        f"- `{channel_manifest.get('path')}` `{channel_manifest.get('sha256')}`",
        f"- `{updater_policy.get('path')}` `{updater_policy.get('sha256')}`",
        "",
        "## Workstation Targets",
        "",
    ]
    for target in payload.get("workstation_targets", []):
        if isinstance(target, dict):
            lines.append(f"- `{target.get('id')}` `{target.get('management_tool')}` `{target.get('binary')}`")
    lines.extend(["", "## Controls", ""])
    for control in payload.get("controls", []):
        lines.append(f"- `{control}`")
    lines.extend(
        [
            "",
            "## Signature",
            "",
            f"Algorithm: `{payload.get('signature', {}).get('algorithm')}`",
            f"Signer: `{payload.get('signature', {}).get('signer')}`",
            f"Payload SHA-256: `{payload.get('signature', {}).get('payload_sha256')}`",
        ]
    )
    return "\n".join(lines) + "\n"


def _endpoint_export_markdown_summary(payload: dict[str, Any]) -> str:
    release = payload.get("release", {})
    approval = payload.get("approval", {})
    lines = [
        "# CAVRA Endpoint Management Export Bundle",
        "",
        f"Channel: `{payload.get('channel')}`",
        f"Version: `{release.get('version')}`",
        f"Commit: `{release.get('commit')}`",
        f"Approval required: `{approval.get('required')}`",
        f"Approval ID: `{approval.get('approval_id') or 'not-linked'}`",
        "",
        "## Providers",
        "",
    ]
    for provider in payload.get("providers", []):
        lines.append(f"- `{provider}`")
    lines.extend(["", "## Files", ""])
    for filename in payload.get("files", []):
        lines.append(f"- `{filename}`")
    lines.extend(["", "## Controls", ""])
    for control in payload.get("controls", []):
        lines.append(f"- `{control}`")
    return "\n".join(lines) + "\n"


def _promotion_execution_markdown_summary(payload: dict[str, Any]) -> str:
    release = payload.get("release", {})
    ring = payload.get("ring_advancement", {})
    approval = payload.get("approval", {})
    lines = [
        "# CAVRA Rollout Promotion Execution",
        "",
        f"Execution ID: `{payload.get('execution_id')}`",
        f"Request ID: `{payload.get('request_id')}`",
        f"Approval ID: `{payload.get('approval_id')}`",
        f"Rollout ID: `{payload.get('rollout_id')}`",
        f"Version: `{release.get('version')}`",
        f"Ring advancement: `{ring.get('from')}` -> `{ring.get('to')}`",
        f"Execution status: `{payload.get('execution_status')}`",
        f"Executed by: `{payload.get('executed_by')}`",
        f"Approved by: `{approval.get('decided_by')}`",
        "",
        "## Controls",
        "",
    ]
    for control in payload.get("controls", []):
        lines.append(f"- `{control}`")
    lines.extend(["", "## Deployment Targets", ""])
    for target in payload.get("deployment_targets", []):
        lines.append(f"- `{target}`")
    lines.extend(["", "## Evidence", "", f"Promotion request SHA-256: `{payload.get('request_sha256')}`"])
    return "\n".join(lines) + "\n"


def _rollback_execution_markdown_summary(payload: dict[str, Any]) -> str:
    release = payload.get("release", {})
    ring = payload.get("ring_rollback", {})
    approval = payload.get("approval", {})
    lines = [
        "# CAVRA Rollout Rollback Execution",
        "",
        f"Rollback ID: `{payload.get('rollback_id')}`",
        f"Promotion execution ID: `{payload.get('promotion_execution_id')}`",
        f"Approval ID: `{payload.get('approval_id')}`",
        f"Rollout ID: `{payload.get('rollout_id')}`",
        f"Version: `{release.get('version')}`",
        f"Ring rollback: `{ring.get('from')}` -> `{ring.get('to')}`",
        f"Rollback status: `{payload.get('rollback_status')}`",
        f"Executed by: `{payload.get('executed_by')}`",
        f"Approved by: `{approval.get('decided_by')}`",
        f"Reason: `{payload.get('rollback_reason')}`",
        "",
        "## Controls",
        "",
    ]
    for control in payload.get("controls", []):
        lines.append(f"- `{control}`")
    lines.extend(["", "## Deployment Targets", ""])
    for target in payload.get("deployment_targets", []):
        lines.append(f"- `{target}`")
    lines.extend(["", "## Rollback Evidence", ""])
    for ref in payload.get("rollback_evidence_refs", []):
        if isinstance(ref, dict):
            lines.append(f"- `{ref.get('target')}` `{ref.get('ref')}`: {ref.get('step')}")
    lines.extend(["", f"Promotion execution SHA-256: `{payload.get('promotion_execution_sha256')}`"])
    return "\n".join(lines) + "\n"


def _promotion_splunk_event(event: dict[str, Any], index: str) -> dict[str, Any]:
    return {
        "time": _promotion_event_epoch(event),
        "host": "cavra",
        "source": "cavra:release",
        "sourcetype": "cavra:rollout-promotion:json",
        "index": index,
        "event": event,
    }


def _promotion_sentinel_event(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "TimeGenerated": event.get("timestamp"),
        "SourceSystem": "CAVRA",
        "EventName": event.get("event_type"),
        "ProductName": "CAVRA",
        "ExecutionId": event.get("execution_id"),
        "RolloutId": event.get("rollout_id"),
        "ApprovalState": event.get("approval_state"),
        "ExecutionStatus": event.get("execution_status"),
        "Severity": event.get("severity", "high"),
        "RawEvent": event,
    }


def _promotion_datadog_event(event: dict[str, Any], service: str) -> dict[str, Any]:
    return {
        "ddsource": "cavra",
        "service": service,
        "status": "warning",
        "message": (
            f"CAVRA rollout promotion {event.get('execution_id')} moved "
            f"{event.get('rollout_id')} to {event.get('target_ring')}."
        ),
        "tags": [
            "product:cavra",
            f"rollout_id:{event.get('rollout_id')}",
            f"execution_id:{event.get('execution_id')}",
            f"approval_state:{event.get('approval_state')}",
            f"target_ring:{event.get('target_ring')}",
        ],
        "attributes": event,
    }


def _promotion_webhook_payload(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "cavra.webhook.rollout-promotion.v1",
        "product": "CAVRA",
        "event_type": event.get("event_type"),
        "timestamp": event.get("timestamp"),
        "payload": event,
    }


def _promotion_jira_issue(event: dict[str, Any], project_key: str) -> dict[str, Any]:
    return {
        "fields": {
            "project": {"key": project_key},
            "summary": f"CAVRA rollout promotion audit: {event.get('rollout_id')} -> {event.get('target_ring')}",
            "issuetype": {"name": "Task"},
            "labels": ["cavra", "rollout-promotion", "audit"],
            "description": (
                f"Promotion execution: {event.get('execution_id')}\n"
                f"Rollout: {event.get('rollout_id')}\n"
                f"Approval: {event.get('approval_id')} ({event.get('approval_state')})\n"
                f"Change: {event.get('change_record')}\n"
                f"Rollback refs: {event.get('rollback_reference_count')}"
            ),
        },
        "cavra_event": event,
    }


def _promotion_servicenow_task(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "short_description": f"CAVRA rollout promotion audit for {event.get('rollout_id')}",
        "description": (
            f"Promotion execution {event.get('execution_id')} moved "
            f"{event.get('current_ring')} to {event.get('target_ring')}."
        ),
        "category": "software",
        "subcategory": "release",
        "impact": "2",
        "urgency": "2",
        "correlation_id": event.get("execution_id"),
        "change_request": event.get("change_record"),
        "u_cavra_event": event,
    }


def _promotion_event_epoch(event: dict[str, Any]) -> float:
    raw = str(event.get("timestamp") or "")
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return datetime.now(timezone.utc).timestamp()


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


def _current_installer_target() -> str:
    system = platform.system().lower()
    os_name = {"darwin": "darwin", "linux": "linux", "windows": "windows"}.get(system, system)
    machine = platform.machine().lower()
    arch = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
    }.get(machine, machine)
    return f"{os_name}/{arch}"


def _execute_go_runtime_smoke(binary_path: Path, *, timeout_seconds: float) -> None:
    request = {
        "session_id": "installer-smoke",
        "action_type": "git_operation",
        "operation": "status",
        "target": "feature/installer-smoke",
    }
    try:
        completed = subprocess.run(
            [str(binary_path)],
            input=json.dumps(request),
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except OSError as exc:
        raise ReleaseVerificationError(f"installer smoke execution failed for {binary_path.name}: {exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise ReleaseVerificationError(f"installer smoke execution timed out for {binary_path.name}") from exc
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        raise ReleaseVerificationError(f"installer smoke execution failed for {binary_path.name}: {stderr or completed.returncode}")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"installer smoke output is not valid JSON for {binary_path.name}: {exc}") from exc
    if payload.get("decision") not in {"allow", "block", "require_approval", "warn", "audit_only", "allow_with_attestation"}:
        raise ReleaseVerificationError(f"installer smoke output has an invalid decision for {binary_path.name}")
