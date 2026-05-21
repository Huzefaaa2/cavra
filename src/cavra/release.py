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
from datetime import datetime, timedelta, timezone
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
class EndpointInventoryIngestionResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    inventory_id: str | None = None
    provider: str | None = None
    inventory: dict[str, Any] | None = None
    ingestion: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "inventory_id": self.inventory_id,
            "provider": self.provider,
            "inventory": self.inventory,
            "ingestion": self.ingestion,
            "files": self.files,
        }


@dataclass(frozen=True)
class EndpointInventoryFreshnessResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    report_id: str | None = None
    alert_level: str | None = None
    report: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "report_id": self.report_id,
            "alert_level": self.alert_level,
            "report": self.report,
            "files": self.files,
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
class EndpointReconciliationAutomationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    automation_id: str | None = None
    reconciliation_id: str | None = None
    request_id: str | None = None
    automation: dict[str, Any] | None = None
    reconciliation: dict[str, Any] | None = None
    remediation_request: dict[str, Any] | None = None
    approval: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "automation_id": self.automation_id,
            "reconciliation_id": self.reconciliation_id,
            "request_id": self.request_id,
            "automation": self.automation,
            "reconciliation": self.reconciliation,
            "remediation_request": self.remediation_request,
            "approval": self.approval,
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
class EndpointRemediationHandoffResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    handoff_id: str | None = None
    request_id: str | None = None
    providers: list[str] = field(default_factory=list)
    handoff: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "handoff_id": self.handoff_id,
            "request_id": self.request_id,
            "providers": self.providers,
            "handoff": self.handoff,
            "files": self.files,
        }


@dataclass(frozen=True)
class EndpointRemediationHandoffStatusResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    status_id: str | None = None
    handoff_id: str | None = None
    provider: str | None = None
    status: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "status_id": self.status_id,
            "handoff_id": self.handoff_id,
            "provider": self.provider,
            "status": self.status,
            "files": self.files,
        }


@dataclass(frozen=True)
class EndpointRemediationSlaReportResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    report_id: str | None = None
    report: dict[str, Any] | None = None
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "report_id": self.report_id,
            "report": self.report,
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

    ci_runner_bundles_path = package_dir / "cavra-runtime.ci-runner-bundles.json"
    if not ci_runner_bundles_path.exists():
        errors.append("missing cavra-runtime.ci-runner-bundles.json")
    else:
        try:
            verify_go_ci_runner_bundles(ci_runner_bundles_path, package_dir, expected_checksums, evidence)
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


def ingest_endpoint_inventory(
    provider: str,
    inventory_payload: dict[str, Any],
    *,
    output_dir: Path | None = None,
    channel: str | None = None,
    observed_at: str | None = None,
    source: str | None = None,
) -> EndpointInventoryIngestionResult:
    errors: list[str] = []
    warnings: list[str] = []
    provider = provider.lower().strip()
    if provider not in {"jamf", "intune", "linux", "edr"}:
        errors.append("provider must be one of: jamf, intune, linux, edr")
    if not isinstance(inventory_payload, dict):
        errors.append("inventory payload must be a JSON object")
    if errors:
        return EndpointInventoryIngestionResult(valid=False, errors=errors, warnings=warnings, provider=provider)

    raw_items = _endpoint_inventory_source_items(provider, inventory_payload)
    if not raw_items:
        warnings.append(f"no endpoint records found for provider {provider}")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(raw_items, start=1):
        endpoint = _normalize_endpoint_inventory_item(provider, item, index=index)
        normalized.append(endpoint)
        if endpoint.get("deployment_target") == "unknown-target":
            warnings.append(f"endpoint {endpoint['endpoint_id']} did not include a deployment target")
    created_at = datetime.now(timezone.utc).isoformat()
    observed_at = observed_at or str(inventory_payload.get("observed_at") or inventory_payload.get("generated_at") or created_at)
    inventory = {
        "schema_version": "cavra.endpoint-observations.v1",
        "product": "CAVRA",
        "provider": provider,
        "channel": channel or inventory_payload.get("channel"),
        "observed_at": observed_at,
        "endpoints": normalized,
        "source": source,
    }
    inventory_id = _endpoint_inventory_ingestion_id(provider, inventory)
    ingestion = {
        "schema_version": "cavra.endpoint-inventory-ingestion.v1",
        "product": "CAVRA",
        "inventory_id": inventory_id,
        "provider": provider,
        "created_at": created_at,
        "observed_at": observed_at,
        "channel": inventory.get("channel"),
        "source": source,
        "source_schema_version": inventory_payload.get("schema_version"),
        "endpoint_count": len(normalized),
        "deployment_targets": sorted({str(item.get("deployment_target")) for item in normalized if item.get("deployment_target")}),
        "missing_target_count": sum(1 for item in normalized if item.get("deployment_target") == "unknown-target"),
        "version_count": sum(1 for item in normalized if item.get("installed_version")),
        "checksum_count": sum(1 for item in normalized if item.get("binary_sha256")),
        "inventory": inventory,
        "controls": [
            "provider-export-normalized",
            "no-connector-credentials-stored",
            "canonical-endpoint-observation-schema-emitted",
            "reconciliation-ready-inventory-generated",
        ],
        "warnings": warnings,
    }
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        inventory_path = output_dir / "endpoint-inventory.json"
        ingestion_path = output_dir / "endpoint-inventory-ingestion.json"
        summary_path = output_dir / "endpoint-inventory-ingestion.md"
        _write_release_json(inventory_path, inventory)
        _write_release_json(ingestion_path, ingestion)
        summary_path.write_text(_endpoint_inventory_ingestion_markdown_summary(ingestion), encoding="utf-8")
        checksums_path = output_dir / "checksums.txt"
        checksums_path.write_text(
            "\n".join(
                f"{sha256_file(path)}  {path.name}" for path in [inventory_path, ingestion_path, summary_path]
            )
            + "\n",
            encoding="utf-8",
        )
        files = [inventory_path.name, ingestion_path.name, summary_path.name, checksums_path.name]
    return EndpointInventoryIngestionResult(
        valid=True,
        warnings=warnings,
        inventory_id=inventory_id,
        provider=provider,
        inventory=inventory,
        ingestion=ingestion,
        files=files,
    )


def build_endpoint_inventory_ingestion_metadata(
    ingestion: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    metadata = {
        "session_id": ingestion.get("inventory_id"),
        "created_at": ingestion.get("created_at"),
        "signer": "endpoint-inventory-ingestion",
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 0,
        "metadata_kind": "endpoint-inventory-ingestion",
        "inventory_id": ingestion.get("inventory_id"),
        "provider": ingestion.get("provider"),
        "channel": ingestion.get("channel"),
        "observed_at": ingestion.get("observed_at"),
        "endpoint_count": ingestion.get("endpoint_count", 0),
        "deployment_targets": ingestion.get("deployment_targets", []),
        "missing_target_count": ingestion.get("missing_target_count", 0),
        "version_count": ingestion.get("version_count", 0),
        "checksum_count": ingestion.get("checksum_count", 0),
        "warnings": ingestion.get("warnings", []),
        "inventory": ingestion.get("inventory", {}),
        "ingestion": ingestion,
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def filter_endpoint_inventory_ingestion_history(
    items: list[dict[str, Any]],
    *,
    provider: str | None = None,
    channel: str | None = None,
    deployment_target: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [item for item in items if item.get("metadata_kind") == "endpoint-inventory-ingestion"]
    if provider:
        filtered = [item for item in filtered if item.get("provider") == provider]
    if channel:
        filtered = [item for item in filtered if item.get("channel") == channel]
    if deployment_target:
        filtered = [
            item
            for item in filtered
            if deployment_target in {str(value) for value in item.get("deployment_targets", [])}
        ]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_inventory_ingestion.history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_inventory_ingestion_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_inventory_ingestion_history(items, limit=500)["items"]
    providers: dict[str, dict[str, Any]] = {}
    for item in history:
        provider = str(item.get("provider") or "unknown")
        summary = providers.setdefault(
            provider,
            {"provider": provider, "ingestions": 0, "endpoint_count": 0, "missing_target_count": 0, "last_observed_at": None},
        )
        summary["ingestions"] += 1
        summary["endpoint_count"] += int(item.get("endpoint_count") or 0)
        summary["missing_target_count"] += int(item.get("missing_target_count") or 0)
        summary["last_observed_at"] = max(str(summary.get("last_observed_at") or ""), str(item.get("observed_at") or ""))
    missing = sum(int(item.get("missing_target_count") or 0) for item in history)
    return {
        "schema_version": "cavra.endpoint_inventory_ingestion.dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": "warning" if missing else "healthy",
        "total_ingestions": len(history),
        "endpoint_count": sum(int(item.get("endpoint_count") or 0) for item in history),
        "missing_target_count": missing,
        "providers": sorted(providers.values(), key=lambda item: item["provider"]),
        "latest": history[:10],
    }


def evaluate_endpoint_inventory_freshness(
    ingestion_items: list[dict[str, Any]],
    *,
    output_dir: Path | None = None,
    provider: str | None = None,
    channel: str | None = None,
    deployment_target: str | None = None,
    max_age_hours: int = 24,
    critical_age_hours: int = 48,
    now: datetime | None = None,
) -> EndpointInventoryFreshnessResult:
    errors: list[str] = []
    warnings: list[str] = []
    max_age_hours = max(1, max_age_hours)
    critical_age_hours = max(max_age_hours, critical_age_hours)
    now = now or datetime.now(timezone.utc)
    history = filter_endpoint_inventory_ingestion_history(
        ingestion_items,
        provider=provider,
        channel=channel,
        deployment_target=deployment_target,
        limit=500,
    )["items"]
    latest_by_scope: dict[tuple[str, str, str], dict[str, Any]] = {}
    for item in history:
        provider_key = str(item.get("provider") or "unknown")
        channel_key = str(item.get("channel") or "unassigned")
        targets = [str(value) for value in item.get("deployment_targets", [])] or ["unknown-target"]
        for target in targets:
            scope = (provider_key, channel_key, target)
            previous = latest_by_scope.get(scope)
            if previous is None or str(item.get("observed_at") or "") > str(previous.get("observed_at") or ""):
                latest_by_scope[scope] = item
    alerts: list[dict[str, Any]] = []
    latest_ingestions: list[dict[str, Any]] = []
    for scope, item in sorted(latest_by_scope.items()):
        provider_key, channel_key, target = scope
        observed_at = str(item.get("observed_at") or item.get("created_at") or "")
        observed = _parse_release_datetime(observed_at)
        age_hours = None
        severity = "healthy"
        if observed is None:
            severity = "warning"
            message = f"Endpoint inventory timestamp is invalid for {provider_key}/{channel_key}/{target}."
        else:
            age_hours = round(max(0.0, (now - observed).total_seconds() / 3600), 2)
            if age_hours >= critical_age_hours:
                severity = "critical"
            elif age_hours >= max_age_hours:
                severity = "warning"
            message = (
                f"Latest endpoint inventory for {provider_key}/{channel_key}/{target} is {age_hours}h old."
                if severity != "healthy"
                else f"Latest endpoint inventory for {provider_key}/{channel_key}/{target} is within SLA."
            )
        latest_entry = {
            "inventory_id": item.get("inventory_id"),
            "provider": provider_key,
            "channel": channel_key,
            "deployment_target": target,
            "observed_at": observed_at,
            "age_hours": age_hours,
            "severity": severity,
            "endpoint_count": item.get("endpoint_count", 0),
            "missing_target_count": item.get("missing_target_count", 0),
        }
        latest_ingestions.append(latest_entry)
        if severity in {"warning", "critical"}:
            alerts.append(
                {
                    "severity": severity,
                    "inventory_id": item.get("inventory_id"),
                    "provider": provider_key,
                    "channel": channel_key,
                    "deployment_target": target,
                    "observed_at": observed_at,
                    "age_hours": age_hours,
                    "message": message,
                }
            )
        if int(item.get("missing_target_count") or 0) > 0:
            alerts.append(
                {
                    "severity": "warning",
                    "inventory_id": item.get("inventory_id"),
                    "provider": provider_key,
                    "channel": channel_key,
                    "deployment_target": target,
                    "message": f"Endpoint inventory {item.get('inventory_id')} includes endpoints with missing deployment targets.",
                }
            )
    if not latest_by_scope:
        warnings.append("no endpoint inventory ingestion records matched the freshness scope")
    critical_count = sum(1 for item in alerts if item.get("severity") == "critical")
    warning_count = sum(1 for item in alerts if item.get("severity") == "warning")
    alert_level = "critical" if critical_count else "warning" if warning_count else "healthy"
    created_at = now.isoformat()
    report = {
        "schema_version": "cavra.endpoint-inventory-freshness.v1",
        "product": "CAVRA",
        "report_id": _endpoint_inventory_freshness_report_id(
            history,
            provider=provider,
            channel=channel,
            deployment_target=deployment_target,
            max_age_hours=max_age_hours,
            critical_age_hours=critical_age_hours,
            created_at=created_at,
        ),
        "created_at": created_at,
        "alert_level": alert_level,
        "max_age_hours": max_age_hours,
        "critical_age_hours": critical_age_hours,
        "scope": {
            "provider": provider,
            "channel": channel,
            "deployment_target": deployment_target,
        },
        "summary": {
            "scope_count": len(latest_by_scope),
            "ingestion_count": len(history),
            "healthy_count": sum(1 for item in latest_ingestions if item.get("severity") == "healthy"),
            "warning_count": warning_count,
            "critical_count": critical_count,
            "missing_target_count": sum(int(item.get("missing_target_count") or 0) for item in history),
        },
        "latest_ingestions": latest_ingestions,
        "alerts": alerts,
        "controls": [
            "endpoint-inventory-age-compared-to-sla",
            "latest-ingestion-selected-by-provider-channel-target",
            "public-safe-alert-metadata-only",
            "private-connectors-required-for-source-refresh",
        ],
        "warnings": warnings,
    }
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        report_path = output_dir / "endpoint-inventory-freshness.json"
        summary_path = output_dir / "endpoint-inventory-freshness.md"
        _write_release_json(report_path, report)
        summary_path.write_text(_endpoint_inventory_freshness_markdown_summary(report), encoding="utf-8")
        checksums_path = output_dir / "checksums.txt"
        checksums_path.write_text(
            "\n".join(f"{sha256_file(path)}  {path.name}" for path in [report_path, summary_path]) + "\n",
            encoding="utf-8",
        )
        files = [report_path.name, summary_path.name, checksums_path.name]
    return EndpointInventoryFreshnessResult(
        valid=not errors,
        errors=errors,
        warnings=warnings,
        report_id=report["report_id"],
        alert_level=alert_level,
        report=report,
        files=files,
    )


def build_endpoint_inventory_freshness_metadata(
    report: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    metadata = {
        "session_id": report.get("report_id"),
        "created_at": report.get("created_at"),
        "signer": "endpoint-inventory-freshness",
        "decision_count": 0,
        "blocked_count": int(summary.get("critical_count") or 0),
        "approval_required_count": 0,
        "metadata_kind": "endpoint-inventory-freshness-report",
        "report_id": report.get("report_id"),
        "alert_level": report.get("alert_level"),
        "max_age_hours": report.get("max_age_hours"),
        "critical_age_hours": report.get("critical_age_hours"),
        "scope": report.get("scope", {}),
        "summary": summary,
        "alert_count": len(report.get("alerts", [])),
        "warning_count": summary.get("warning_count", 0),
        "critical_count": summary.get("critical_count", 0),
        "latest_ingestions": report.get("latest_ingestions", []),
        "alerts": report.get("alerts", []),
        "report": report,
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def filter_endpoint_inventory_freshness_history(
    items: list[dict[str, Any]],
    *,
    alert_level: str | None = None,
    provider: str | None = None,
    channel: str | None = None,
    deployment_target: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [item for item in items if item.get("metadata_kind") == "endpoint-inventory-freshness-report"]
    if alert_level:
        filtered = [item for item in filtered if item.get("alert_level") == alert_level]
    if provider:
        filtered = [
            item
            for item in filtered
            if any(entry.get("provider") == provider for entry in item.get("latest_ingestions", []))
        ]
    if channel:
        filtered = [
            item
            for item in filtered
            if any(entry.get("channel") == channel for entry in item.get("latest_ingestions", []))
        ]
    if deployment_target:
        filtered = [
            item
            for item in filtered
            if any(entry.get("deployment_target") == deployment_target for entry in item.get("latest_ingestions", []))
        ]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_inventory_freshness.history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_inventory_freshness_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_inventory_freshness_history(items, limit=500)["items"]
    critical = sum(int(item.get("critical_count") or 0) for item in history)
    warning = sum(int(item.get("warning_count") or 0) for item in history)
    alerts = [
        alert
        for item in history
        for alert in item.get("alerts", [])
        if isinstance(alert, dict)
    ]
    alert_level = "critical" if critical else "warning" if warning else "healthy"
    return {
        "schema_version": "cavra.endpoint_inventory_freshness.dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "report_count": len(history),
        "warning_count": warning,
        "critical_count": critical,
        "alert_count": len(alerts),
        "alerts": alerts[:25],
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


def automate_endpoint_reconciliation_from_ingestion(
    desired_manifest: dict[str, Any],
    ingestion_record: dict[str, Any],
    *,
    package_dir: Path | None = None,
    output_dir: Path | None = None,
    stale_after_hours: int = 24,
    require_package_verification: bool = False,
    remediation_strategy: str = "mixed",
    requested_by: str = "release-agent",
    approver_group: str = "Endpoint Change Advisory Board",
    ttl_hours: int = 24,
) -> EndpointReconciliationAutomationResult:
    errors: list[str] = []
    warnings: list[str] = []
    observed_inventory = _inventory_from_ingestion_record(ingestion_record)
    if observed_inventory is None:
        errors.append("ingestion record must be endpoint-inventory-ingestion metadata, ingestion payload, or endpoint observations")
    if errors:
        return EndpointReconciliationAutomationResult(valid=False, errors=errors, warnings=warnings)
    reconciliation_output = output_dir / "reconciliation" if output_dir else None
    reconciliation = reconcile_managed_endpoint_deployment(
        desired_manifest,
        observed_inventory,
        package_dir=package_dir,
        output_dir=reconciliation_output,
        stale_after_hours=stale_after_hours,
        require_package_verification=require_package_verification,
    )
    if not reconciliation.valid or reconciliation.report is None:
        return EndpointReconciliationAutomationResult(
            valid=False,
            errors=reconciliation.errors,
            warnings=[*warnings, *reconciliation.warnings],
            reconciliation_id=reconciliation.reconciliation_id,
            reconciliation=reconciliation.report,
        )
    remediation_result = None
    if reconciliation.drift_status == "drift_detected":
        remediation_output = output_dir / "remediation-request" if output_dir else None
        remediation_result = create_endpoint_drift_remediation_request(
            reconciliation.report,
            output_dir=remediation_output,
            strategy=remediation_strategy,
            requested_by=requested_by,
            approver_group=approver_group,
            ttl_hours=ttl_hours,
        )
        if not remediation_result.valid:
            errors.extend(remediation_result.errors)
            warnings.extend(remediation_result.warnings)
    created_at = datetime.now(timezone.utc).isoformat()
    automation_id = _endpoint_reconciliation_automation_id(
        desired_manifest,
        ingestion_record,
        reconciliation.report,
        remediation_result.request if remediation_result else None,
    )
    automation = {
        "schema_version": "cavra.endpoint-reconciliation-automation.v1",
        "product": "CAVRA",
        "automation_id": automation_id,
        "created_at": created_at,
        "requested_by": requested_by,
        "reconciliation_id": reconciliation.reconciliation_id,
        "drift_status": reconciliation.drift_status,
        "alert_level": reconciliation.report.get("alert_level"),
        "release": reconciliation.report.get("release", {}),
        "channel": reconciliation.report.get("channel"),
        "inventory_id": ingestion_record.get("inventory_id") or ingestion_record.get("session_id"),
        "provider": ingestion_record.get("provider") or observed_inventory.get("provider"),
        "observed_at": observed_inventory.get("observed_at"),
        "remediation_request_id": remediation_result.request.get("request_id") if remediation_result and remediation_result.request else None,
        "approval_id": remediation_result.approval.get("approval_id") if remediation_result and remediation_result.approval else None,
        "approval_state": remediation_result.approval.get("state") if remediation_result and remediation_result.approval else None,
        "summary": reconciliation.report.get("summary", {}),
        "controls": [
            "inventory-ingestion-reconciled-against-signed-manifest",
            "drift-opens-approval-bound-remediation-request",
            "automation-records-governance-evidence-only",
            "private-connectors-required-for-endpoint-mutation",
        ],
        "evidence_refs": [
            f"endpoint-reconciliation://{reconciliation.reconciliation_id}",
            *(
                [f"endpoint-remediation-request://{remediation_result.request['request_id']}"]
                if remediation_result and remediation_result.request
                else []
            ),
            *([f"approval://{remediation_result.approval['approval_id']}"] if remediation_result and remediation_result.approval else []),
        ],
        "reconciliation_report": reconciliation.report,
        "remediation_request": remediation_result.request if remediation_result else None,
    }
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        automation_path = output_dir / "endpoint-reconciliation-automation.json"
        summary_path = output_dir / "endpoint-reconciliation-automation.md"
        _write_release_json(automation_path, automation)
        summary_path.write_text(_endpoint_reconciliation_automation_markdown_summary(automation), encoding="utf-8")
        checksums_path = output_dir / "checksums.txt"
        checksum_targets = [automation_path, summary_path]
        checksums_path.write_text(
            "\n".join(f"{sha256_file(path)}  {path.name}" for path in checksum_targets) + "\n",
            encoding="utf-8",
        )
        files = [
            "endpoint-reconciliation-automation.json",
            "endpoint-reconciliation-automation.md",
            "checksums.txt",
            *[f"reconciliation/{item}" for item in reconciliation.files],
            *([f"remediation-request/{item}" for item in remediation_result.files] if remediation_result else []),
        ]
    return EndpointReconciliationAutomationResult(
        valid=not errors,
        errors=errors,
        warnings=warnings,
        automation_id=automation_id,
        reconciliation_id=reconciliation.reconciliation_id,
        request_id=automation.get("remediation_request_id"),
        automation=automation,
        reconciliation=reconciliation.report,
        remediation_request=remediation_result.request if remediation_result else None,
        approval=remediation_result.approval if remediation_result else None,
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


def build_endpoint_remediation_handoff(
    remediation_request: dict[str, Any],
    *,
    output_dir: Path | None = None,
    providers: list[str] | None = None,
    requested_by: str = "release-manager",
    delivery_mode: str = "manual",
) -> EndpointRemediationHandoffResult:
    errors: list[str] = []
    warnings: list[str] = []
    if remediation_request.get("schema_version") != "cavra.endpoint-drift-remediation-request.v1":
        errors.append("remediation request has an invalid schema_version")
    request_id = str(remediation_request.get("request_id") or "")
    reconciliation_id = str(remediation_request.get("reconciliation_id") or "")
    if not request_id:
        errors.append("remediation request must include request_id")
    if not reconciliation_id:
        errors.append("remediation request must include reconciliation_id")
    selected_providers = _normalize_endpoint_remediation_handoff_providers(providers)
    if not selected_providers:
        errors.append("provider must be one of: jira, servicenow, slack, teams, private_queue, all")
    actions = [item for item in remediation_request.get("actions", []) if isinstance(item, dict)]
    if not actions:
        warnings.append("remediation request contains no actions")
    if errors:
        return EndpointRemediationHandoffResult(
            valid=False,
            errors=errors,
            warnings=warnings,
            request_id=request_id or None,
            providers=selected_providers,
        )
    created_at = datetime.now(timezone.utc).isoformat()
    approval = remediation_request.get("approval", {}) if isinstance(remediation_request.get("approval"), dict) else {}
    request_canonical = json.dumps(remediation_request, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    request_sha256 = hashlib.sha256(request_canonical).hexdigest()
    handoff_id = _endpoint_remediation_handoff_id(request_id, selected_providers, request_sha256)
    provider_payloads = {
        provider: _endpoint_remediation_provider_payload(provider, remediation_request, actions, handoff_id=handoff_id)
        for provider in selected_providers
    }
    handoff = {
        "schema_version": "cavra.endpoint-remediation-handoff.v1",
        "product": "CAVRA",
        "handoff_id": handoff_id,
        "request_id": request_id,
        "reconciliation_id": reconciliation_id,
        "created_at": created_at,
        "requested_by": requested_by,
        "delivery_mode": delivery_mode,
        "providers": selected_providers,
        "provider_count": len(selected_providers),
        "action_count": len(actions),
        "approval_id": approval.get("approval_id"),
        "approval_state": approval.get("state"),
        "approval_required": approval.get("state") != "approved",
        "release": remediation_request.get("release", {}),
        "channel": remediation_request.get("channel"),
        "strategy": remediation_request.get("strategy"),
        "alert_level": remediation_request.get("alert_level"),
        "summary": remediation_request.get("summary", {}),
        "payloads": provider_payloads,
        "controls": [
            "handoff-payloads-derived-from-remediation-request",
            "approval-id-preserved-for-downstream-gates",
            "public-package-contains-no-connector-credentials",
            "private-connectors-required-for-endpoint-mutation",
        ],
        "evidence_refs": [
            f"endpoint-remediation-request://{request_id}",
            f"endpoint-reconciliation://{reconciliation_id}",
            *([f"approval://{approval.get('approval_id')}"] if approval.get("approval_id") else []),
        ],
        "request_sha256": request_sha256,
        "remediation_request": remediation_request,
    }
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        handoff_path = output_dir / "endpoint-remediation-handoff.json"
        summary_path = output_dir / "endpoint-remediation-handoff.md"
        _write_release_json(handoff_path, handoff)
        summary_path.write_text(_endpoint_remediation_handoff_markdown_summary(handoff), encoding="utf-8")
        provider_paths: list[Path] = []
        for provider, payload in provider_payloads.items():
            provider_path = output_dir / f"{provider.replace('_', '-')}-handoff.json"
            _write_release_json(provider_path, payload)
            provider_paths.append(provider_path)
        checksums_path = output_dir / "checksums.txt"
        checksum_targets = [handoff_path, summary_path, *provider_paths]
        checksums_path.write_text(
            "\n".join(f"{sha256_file(path)}  {path.name}" for path in checksum_targets) + "\n",
            encoding="utf-8",
        )
        files = [handoff_path.name, summary_path.name, *[path.name for path in provider_paths], checksums_path.name]
    return EndpointRemediationHandoffResult(
        valid=True,
        warnings=warnings,
        handoff_id=handoff_id,
        request_id=request_id,
        providers=selected_providers,
        handoff=handoff,
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


def build_endpoint_remediation_handoff_metadata(
    handoff: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    metadata = {
        "session_id": handoff.get("handoff_id"),
        "created_at": handoff.get("created_at"),
        "signer": handoff.get("requested_by", "release-manager"),
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 1 if handoff.get("approval_required") else 0,
        "metadata_kind": "endpoint-remediation-handoff",
        "handoff_id": handoff.get("handoff_id"),
        "request_id": handoff.get("request_id"),
        "reconciliation_id": handoff.get("reconciliation_id"),
        "approval_id": handoff.get("approval_id"),
        "approval_state": handoff.get("approval_state"),
        "providers": handoff.get("providers", []),
        "provider_count": handoff.get("provider_count", 0),
        "action_count": handoff.get("action_count", 0),
        "strategy": handoff.get("strategy"),
        "alert_level": handoff.get("alert_level"),
        "release": handoff.get("release", {}),
        "channel": handoff.get("channel"),
        "delivery_mode": handoff.get("delivery_mode"),
        "handoff": handoff,
        "evidence_refs": handoff.get("evidence_refs", []),
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def record_endpoint_remediation_handoff_status(
    handoff: dict[str, Any],
    *,
    provider: str,
    status: str,
    external_ref: str | None = None,
    external_url: str | None = None,
    callback_payload: dict[str, Any] | None = None,
    recorded_by: str = "release-manager",
    notes: str | None = None,
    output_dir: Path | None = None,
) -> EndpointRemediationHandoffStatusResult:
    errors: list[str] = []
    warnings: list[str] = []
    if handoff.get("schema_version") != "cavra.endpoint-remediation-handoff.v1":
        errors.append("handoff has an invalid schema_version")
    handoff_id = str(handoff.get("handoff_id") or "")
    request_id = str(handoff.get("request_id") or "")
    reconciliation_id = str(handoff.get("reconciliation_id") or "")
    provider_key = str(provider).strip().lower().replace("-", "_")
    allowed_providers = set(_normalize_endpoint_remediation_handoff_providers(["all"]))
    if not handoff_id:
        errors.append("handoff must include handoff_id")
    if provider_key not in allowed_providers:
        errors.append("provider must be one of: jira, servicenow, slack, teams, private_queue")
    if provider_key and provider_key not in {str(value) for value in handoff.get("providers", [])}:
        errors.append("provider is not present in the handoff package")
    status_key = str(status).strip().lower().replace("-", "_")
    allowed_statuses = {
        "queued",
        "delivered",
        "acknowledged",
        "in_progress",
        "blocked",
        "completed",
        "failed",
        "cancelled",
    }
    if status_key not in allowed_statuses:
        errors.append("status must be one of: queued, delivered, acknowledged, in_progress, blocked, completed, failed, cancelled")
    payload = callback_payload if isinstance(callback_payload, dict) else {}
    if callback_payload and not isinstance(callback_payload, dict):
        warnings.append("callback_payload ignored because it is not a JSON object")
    if errors:
        return EndpointRemediationHandoffStatusResult(
            valid=False,
            errors=errors,
            warnings=warnings,
            handoff_id=handoff_id or None,
            provider=provider_key or None,
        )
    recorded_at = datetime.now(timezone.utc).isoformat()
    status_id = _endpoint_remediation_handoff_status_id(
        handoff_id,
        provider_key,
        status_key,
        external_ref,
        recorded_at,
    )
    status_record = {
        "schema_version": "cavra.endpoint-remediation-handoff-status.v1",
        "product": "CAVRA",
        "status_id": status_id,
        "handoff_id": handoff_id,
        "request_id": request_id,
        "reconciliation_id": reconciliation_id,
        "provider": provider_key,
        "status": status_key,
        "recorded_at": recorded_at,
        "recorded_by": recorded_by,
        "external_ref": external_ref,
        "external_url": external_url,
        "notes": notes,
        "approval_id": handoff.get("approval_id"),
        "approval_state": handoff.get("approval_state"),
        "action_count": handoff.get("action_count", 0),
        "delivery_mode": handoff.get("delivery_mode"),
        "release": handoff.get("release", {}),
        "channel": handoff.get("channel"),
        "callback_payload": _redact_endpoint_handoff_callback_payload(payload),
        "controls": [
            "status-derived-from-provider-callback-or-operator-update",
            "external-reference-preserved-for-audit-correlation",
            "public-status-record-contains-no-connector-credentials",
            "endpoint-mutation-remains-private-connector-responsibility",
        ],
        "evidence_refs": [
            f"endpoint-remediation-handoff://{handoff_id}",
            f"endpoint-remediation-request://{request_id}",
            f"endpoint-reconciliation://{reconciliation_id}",
            *([f"approval://{handoff.get('approval_id')}"] if handoff.get("approval_id") else []),
            *([f"external://{provider_key}/{external_ref}"] if external_ref else []),
        ],
        "handoff_sha256": hashlib.sha256(
            json.dumps(handoff, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        ).hexdigest(),
    }
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        status_path = output_dir / "endpoint-remediation-handoff-status.json"
        summary_path = output_dir / "endpoint-remediation-handoff-status.md"
        _write_release_json(status_path, status_record)
        summary_path.write_text(_endpoint_remediation_handoff_status_markdown_summary(status_record), encoding="utf-8")
        checksums_path = output_dir / "checksums.txt"
        checksums_path.write_text(
            "\n".join(f"{sha256_file(path)}  {path.name}" for path in [status_path, summary_path]) + "\n",
            encoding="utf-8",
        )
        files = [status_path.name, summary_path.name, checksums_path.name]
    return EndpointRemediationHandoffStatusResult(
        valid=True,
        warnings=warnings,
        status_id=status_id,
        handoff_id=handoff_id,
        provider=provider_key,
        status=status_record,
        files=files,
    )


def build_endpoint_remediation_handoff_status_metadata(
    status: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    metadata = {
        "session_id": status.get("status_id"),
        "created_at": status.get("recorded_at"),
        "signer": status.get("recorded_by", "release-manager"),
        "decision_count": 0,
        "blocked_count": 1 if status.get("status") in {"blocked", "failed"} else 0,
        "approval_required_count": 1 if status.get("approval_state") == "pending" else 0,
        "metadata_kind": "endpoint-remediation-handoff-status",
        "status_id": status.get("status_id"),
        "handoff_id": status.get("handoff_id"),
        "request_id": status.get("request_id"),
        "reconciliation_id": status.get("reconciliation_id"),
        "provider": status.get("provider"),
        "handoff_status": status.get("status"),
        "external_ref": status.get("external_ref"),
        "external_url": status.get("external_url"),
        "approval_id": status.get("approval_id"),
        "approval_state": status.get("approval_state"),
        "action_count": status.get("action_count", 0),
        "release": status.get("release", {}),
        "channel": status.get("channel"),
        "status_record": status,
        "evidence_refs": status.get("evidence_refs", []),
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def filter_endpoint_remediation_handoff_history(
    items: list[dict[str, Any]],
    *,
    provider: str | None = None,
    approval_state: str | None = None,
    request_id: str | None = None,
    reconciliation_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [item for item in items if item.get("metadata_kind") == "endpoint-remediation-handoff"]
    if provider:
        filtered = [item for item in filtered if provider in {str(value) for value in item.get("providers", [])}]
    if approval_state:
        filtered = [item for item in filtered if item.get("approval_state") == approval_state]
    if request_id:
        filtered = [item for item in filtered if item.get("request_id") == request_id]
    if reconciliation_id:
        filtered = [item for item in filtered if item.get("reconciliation_id") == reconciliation_id]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_handoff.history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def filter_endpoint_remediation_handoff_status_history(
    items: list[dict[str, Any]],
    *,
    provider: str | None = None,
    handoff_status: str | None = None,
    handoff_id: str | None = None,
    request_id: str | None = None,
    external_ref: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [item for item in items if item.get("metadata_kind") == "endpoint-remediation-handoff-status"]
    if provider:
        filtered = [item for item in filtered if item.get("provider") == provider]
    if handoff_status:
        status_key = handoff_status.strip().lower().replace("-", "_")
        filtered = [item for item in filtered if item.get("handoff_status") == status_key]
    if handoff_id:
        filtered = [item for item in filtered if item.get("handoff_id") == handoff_id]
    if request_id:
        filtered = [item for item in filtered if item.get("request_id") == request_id]
    if external_ref:
        filtered = [item for item in filtered if item.get("external_ref") == external_ref]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_handoff_status.history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_remediation_handoff_status_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_remediation_handoff_status_history(items, limit=500)["items"]
    providers: dict[str, int] = {}
    statuses: dict[str, int] = {}
    latest_by_handoff_provider: dict[str, dict[str, Any]] = {}
    for item in history:
        provider = str(item.get("provider") or "unknown")
        status = str(item.get("handoff_status") or "unknown")
        providers[provider] = providers.get(provider, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
        key = f"{item.get('handoff_id')}::{provider}"
        current = latest_by_handoff_provider.get(key)
        if current is None or str(item.get("created_at", "")) > str(current.get("created_at", "")):
            latest_by_handoff_provider[key] = item
    latest_statuses = list(latest_by_handoff_provider.values())
    failed = [item for item in latest_statuses if item.get("handoff_status") == "failed"]
    blocked = [item for item in latest_statuses if item.get("handoff_status") == "blocked"]
    completed = [item for item in latest_statuses if item.get("handoff_status") == "completed"]
    in_progress = [
        item
        for item in latest_statuses
        if item.get("handoff_status") in {"queued", "delivered", "acknowledged", "in_progress"}
    ]
    alert_level = "critical" if failed or blocked else "warning" if in_progress else "healthy"
    return {
        "schema_version": "cavra.endpoint_remediation_handoff_status.dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "status_event_count": len(history),
        "tracked_handoff_provider_count": len(latest_by_handoff_provider),
        "completed_count": len(completed),
        "in_progress_count": len(in_progress),
        "blocked_count": len(blocked),
        "failed_count": len(failed),
        "provider_count": len(providers),
        "providers": providers,
        "statuses": statuses,
        "latest": history[:10],
    }


def build_endpoint_remediation_sla_report(
    handoff_items: list[dict[str, Any]],
    status_items: list[dict[str, Any]],
    *,
    warning_hours: int = 24,
    critical_hours: int = 48,
    generated_by: str = "release-manager",
    output_dir: Path | None = None,
    now: datetime | None = None,
) -> EndpointRemediationSlaReportResult:
    errors: list[str] = []
    warnings: list[str] = []
    warning_hours = max(1, int(warning_hours))
    critical_hours = max(1, int(critical_hours))
    if warning_hours > critical_hours:
        errors.append("warning_hours must be less than or equal to critical_hours")
    handoffs = [item for item in handoff_items if item.get("metadata_kind") == "endpoint-remediation-handoff"]
    statuses = [item for item in status_items if item.get("metadata_kind") == "endpoint-remediation-handoff-status"]
    if not handoffs:
        warnings.append("no endpoint remediation handoff metadata found")
    if errors:
        return EndpointRemediationSlaReportResult(valid=False, errors=errors, warnings=warnings)
    now = now or datetime.now(timezone.utc)
    latest_status: dict[tuple[str, str], dict[str, Any]] = {}
    for item in statuses:
        handoff_id = str(item.get("handoff_id") or "")
        provider = str(item.get("provider") or "")
        if not handoff_id or not provider:
            continue
        key = (handoff_id, provider)
        current = latest_status.get(key)
        if current is None or str(item.get("created_at", "")) > str(current.get("created_at", "")):
            latest_status[key] = item
    work_items: list[dict[str, Any]] = []
    for handoff_item in handoffs:
        handoff_id = str(handoff_item.get("handoff_id") or handoff_item.get("session_id") or "")
        created_at = _parse_release_datetime(handoff_item.get("created_at")) or now
        providers = [str(provider) for provider in handoff_item.get("providers", [])]
        for provider in providers:
            status_item = latest_status.get((handoff_id, provider))
            state = str(status_item.get("handoff_status") if status_item else "not_started")
            status_at = _parse_release_datetime(status_item.get("created_at")) if status_item else None
            terminal = state in {"completed", "cancelled"}
            end_at = status_at if terminal and status_at else now
            age_hours = max(0.0, (end_at - created_at).total_seconds() / 3600)
            severity = "healthy"
            sla_state = "met"
            if state in {"failed", "blocked"}:
                severity = "critical"
                sla_state = "breached"
            elif not terminal and age_hours >= critical_hours:
                severity = "critical"
                sla_state = "breached"
            elif not terminal and age_hours >= warning_hours:
                severity = "warning"
                sla_state = "at_risk"
            overdue_hours = 0.0
            if sla_state == "breached":
                overdue_hours = max(0.0, age_hours - critical_hours)
            elif sla_state == "at_risk":
                overdue_hours = max(0.0, age_hours - warning_hours)
            work_items.append(
                {
                    "handoff_id": handoff_id,
                    "request_id": handoff_item.get("request_id"),
                    "reconciliation_id": handoff_item.get("reconciliation_id"),
                    "provider": provider,
                    "status": state,
                    "severity": severity,
                    "sla_state": sla_state,
                    "age_hours": round(age_hours, 2),
                    "overdue_hours": round(overdue_hours, 2),
                    "warning_hours": warning_hours,
                    "critical_hours": critical_hours,
                    "created_at": handoff_item.get("created_at"),
                    "latest_status_at": status_item.get("created_at") if status_item else None,
                    "external_ref": status_item.get("external_ref") if status_item else None,
                    "external_url": status_item.get("external_url") if status_item else None,
                    "approval_id": handoff_item.get("approval_id"),
                    "approval_state": handoff_item.get("approval_state"),
                    "action_count": handoff_item.get("action_count", 0),
                    "release": handoff_item.get("release", {}),
                    "channel": handoff_item.get("channel"),
                    "recommended_action": _endpoint_remediation_sla_recommended_action(state, severity),
                }
            )
    breached = [item for item in work_items if item["sla_state"] == "breached"]
    at_risk = [item for item in work_items if item["sla_state"] == "at_risk"]
    completed = [item for item in work_items if item["status"] == "completed"]
    alert_level = "critical" if breached else "warning" if at_risk else "healthy"
    generated_at = now.isoformat()
    report_id = _endpoint_remediation_sla_report_id(generated_at, warning_hours, critical_hours, work_items)
    escalations = [_endpoint_remediation_sla_escalation(item) for item in [*breached, *at_risk]]
    report = {
        "schema_version": "cavra.endpoint-remediation-sla-report.v1",
        "product": "CAVRA",
        "report_id": report_id,
        "generated_at": generated_at,
        "generated_by": generated_by,
        "warning_hours": warning_hours,
        "critical_hours": critical_hours,
        "alert_level": alert_level,
        "executive_summary": {
            "tracked_work_item_count": len(work_items),
            "completed_count": len(completed),
            "at_risk_count": len(at_risk),
            "breached_count": len(breached),
            "completion_rate": round((len(completed) / len(work_items)) if work_items else 0.0, 4),
            "critical_provider_count": len({item["provider"] for item in breached}),
            "release_channels": sorted({str(item.get("channel")) for item in work_items if item.get("channel")}),
        },
        "work_items": sorted(work_items, key=lambda item: (item["severity"], item["age_hours"]), reverse=True),
        "escalations": escalations,
        "escalation_payloads": _endpoint_remediation_sla_escalation_payloads(report_id, escalations),
        "controls": [
            "sla-report-derived-from-public-handoff-and-status-metadata",
            "escalation-payloads-contain-no-connector-credentials",
            "executive-summary-avoids-private-endpoint-mutation-details",
            "private-connectors-remain-responsible-for-endpoint-changes",
        ],
        "evidence_refs": [
            *[f"endpoint-remediation-handoff://{item.get('handoff_id')}" for item in handoffs if item.get("handoff_id")],
            *[
                f"endpoint-remediation-handoff-status://{item.get('status_id')}"
                for item in statuses
                if item.get("status_id")
            ],
        ],
    }
    files: list[str] = []
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        report_path = output_dir / "endpoint-remediation-sla-report.json"
        summary_path = output_dir / "endpoint-remediation-sla-report.md"
        _write_release_json(report_path, report)
        summary_path.write_text(_endpoint_remediation_sla_report_markdown_summary(report), encoding="utf-8")
        checksums_path = output_dir / "checksums.txt"
        checksums_path.write_text(
            "\n".join(f"{sha256_file(path)}  {path.name}" for path in [report_path, summary_path]) + "\n",
            encoding="utf-8",
        )
        files = [report_path.name, summary_path.name, checksums_path.name]
    return EndpointRemediationSlaReportResult(
        valid=True,
        warnings=warnings,
        report_id=report_id,
        report=report,
        files=files,
    )


def build_endpoint_remediation_sla_report_metadata(
    report: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    summary = report.get("executive_summary", {}) if isinstance(report.get("executive_summary"), dict) else {}
    metadata = {
        "session_id": report.get("report_id"),
        "created_at": report.get("generated_at"),
        "signer": report.get("generated_by", "release-manager"),
        "decision_count": int(summary.get("tracked_work_item_count") or 0),
        "blocked_count": int(summary.get("breached_count") or 0),
        "approval_required_count": int(summary.get("at_risk_count") or 0),
        "metadata_kind": "endpoint-remediation-sla-report",
        "report_id": report.get("report_id"),
        "alert_level": report.get("alert_level"),
        "warning_hours": report.get("warning_hours"),
        "critical_hours": report.get("critical_hours"),
        "tracked_work_item_count": summary.get("tracked_work_item_count", 0),
        "completed_count": summary.get("completed_count", 0),
        "at_risk_count": summary.get("at_risk_count", 0),
        "breached_count": summary.get("breached_count", 0),
        "completion_rate": summary.get("completion_rate", 0),
        "critical_provider_count": summary.get("critical_provider_count", 0),
        "release_channels": summary.get("release_channels", []),
        "escalation_count": len(report.get("escalations", [])),
        "report": report,
        "evidence_refs": report.get("evidence_refs", []),
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def build_endpoint_remediation_sla_notification_event(
    report: dict[str, Any],
    *,
    generated_by: str = "release-manager",
    max_escalations: int = 10,
) -> dict[str, Any]:
    """Build a public-safe connector event from an endpoint remediation SLA report."""
    summary = report.get("executive_summary", {}) if isinstance(report.get("executive_summary"), dict) else {}
    escalations = [item for item in report.get("escalations", []) if isinstance(item, dict)]
    max_escalations = max(1, min(int(max_escalations), 50))
    selected_escalations = escalations[:max_escalations]
    report_id = str(report.get("report_id") or "endpoint-remediation-sla")
    alert_level = str(report.get("alert_level") or "healthy")
    breached_count = int(summary.get("breached_count") or 0)
    at_risk_count = int(summary.get("at_risk_count") or 0)
    tracked_count = int(summary.get("tracked_work_item_count") or 0)
    completion_rate = summary.get("completion_rate", 0)
    title = f"CAVRA endpoint remediation SLA {alert_level}: {report_id}"
    message = (
        f"{breached_count} breached and {at_risk_count} at-risk endpoint remediation "
        f"handoffs across {tracked_count} tracked work items."
    )
    description = _endpoint_remediation_sla_notification_description(
        report_id,
        alert_level,
        summary,
        selected_escalations,
    )
    event = {
        "schema_version": "cavra.endpoint_remediation_sla.notification.v1",
        "product": "CAVRA",
        "event_type": "cavra.endpoint_remediation_sla.notification",
        "session_id": report_id,
        "report_id": report_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": generated_by,
        "source_report_generated_at": report.get("generated_at"),
        "alert_level": alert_level,
        "max_severity": "critical" if breached_count else "warning" if at_risk_count else "low",
        "blocked_count": breached_count,
        "approval_required_count": at_risk_count,
        "decision_count": tracked_count,
        "completion_rate": completion_rate,
        "summary": {
            "tracked_work_item_count": tracked_count,
            "completed_count": int(summary.get("completed_count") or 0),
            "at_risk_count": at_risk_count,
            "breached_count": breached_count,
            "critical_provider_count": int(summary.get("critical_provider_count") or 0),
            "release_channels": summary.get("release_channels", []),
        },
        "escalations": selected_escalations,
        "omitted_escalation_count": max(0, len(escalations) - len(selected_escalations)),
        "controls": [
            "notification-derived-from-public-sla-report",
            "connector-delivery-evidence-redacts-secrets",
            "no-endpoint-mutation-performed-by-public-notification-event",
            "private-connectors-remain-responsible-for-ticket-or-chat-side-effects",
        ],
        "evidence_refs": report.get("evidence_refs", []),
    }
    event["provider_payloads"] = {
        "webhook": event | {"provider": "webhook"},
        "slack": _endpoint_remediation_sla_slack_payload(title, message, selected_escalations),
        "teams": _endpoint_remediation_sla_teams_payload(title, message, alert_level, selected_escalations),
        "jira": _endpoint_remediation_sla_jira_payload(title, description, alert_level),
        "servicenow": _endpoint_remediation_sla_servicenow_payload(title, description, report_id, alert_level),
    }
    return event


def build_endpoint_remediation_sla_notification_plan(
    report: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
    delivery_items: list[dict[str, Any]] | None = None,
    requested_provider: str = "all",
    available_providers: list[str] | None = None,
    generated_by: str = "release-manager",
    suppression_window_minutes: int | None = None,
    force: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Plan SLA notification routing and duplicate suppression from public metadata."""
    now = now or datetime.now(timezone.utc)
    policy = policy or {}
    summary = report.get("executive_summary", {}) if isinstance(report.get("executive_summary"), dict) else {}
    report_id = str(report.get("report_id") or "endpoint-remediation-sla")
    alert_level = str(report.get("alert_level") or "healthy")
    available = _normalize_endpoint_remediation_sla_notification_providers(available_providers or [])
    matched_rules = _endpoint_remediation_sla_matching_rules(report, policy)
    eligible = _endpoint_remediation_sla_policy_providers(
        report,
        policy,
        matched_rules,
        requested_provider=requested_provider,
        available_providers=available,
    )
    if not eligible:
        eligible = available or ["webhook"]
    window = _endpoint_remediation_sla_suppression_window(
        policy,
        matched_rules,
        override=suppression_window_minutes,
    )
    delivery_items = delivery_items or []
    suppressed = [] if force else _endpoint_remediation_sla_suppressed_providers(
        report_id,
        eligible,
        delivery_items,
        now=now,
        suppression_window_minutes=window,
    )
    suppressed_names = {str(item["provider"]) for item in suppressed}
    selected = [provider for provider in eligible if provider not in suppressed_names]
    route_by_provider = _endpoint_remediation_sla_route_map(matched_rules)
    routes = []
    for provider in eligible:
        route = route_by_provider.get(provider, {})
        routes.append(
            {
                "provider": provider,
                "selected": provider in selected,
                "suppressed": provider in suppressed_names,
                "rule_ids": route.get("rule_ids", []),
                "owner": route.get("owner") or policy.get("owner") or "release-governance",
                "acknowledgement_required": bool(route.get("acknowledgement_required", alert_level in {"critical", "warning"})),
                "suppression_window_minutes": window,
            }
        )
    generated_at = now.isoformat()
    material = json.dumps(
        {
            "report_id": report_id,
            "generated_at": generated_at,
            "eligible": eligible,
            "selected": selected,
            "suppressed": suppressed,
        },
        sort_keys=True,
    )
    plan_id = f"erslan-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.notification_plan.v1",
        "product": "CAVRA",
        "plan_id": plan_id,
        "report_id": report_id,
        "generated_at": generated_at,
        "generated_by": generated_by,
        "alert_level": alert_level,
        "summary": {
            "tracked_work_item_count": int(summary.get("tracked_work_item_count") or 0),
            "completed_count": int(summary.get("completed_count") or 0),
            "at_risk_count": int(summary.get("at_risk_count") or 0),
            "breached_count": int(summary.get("breached_count") or 0),
            "release_channels": summary.get("release_channels", []),
        },
        "requested_provider": requested_provider,
        "eligible_providers": eligible,
        "selected_providers": selected,
        "suppressed_providers": suppressed,
        "suppression_window_minutes": window,
        "force": force,
        "routes": routes,
        "matched_rule_ids": [str(rule.get("rule_id") or rule.get("name")) for rule in matched_rules],
        "acknowledgement_required_providers": [
            route["provider"] for route in routes if route["selected"] and route["acknowledgement_required"]
        ],
        "controls": [
            "routing-derived-from-public-sla-policy",
            "duplicate-suppression-uses-redacted-delivery-metadata",
            "acknowledgements-record-human-or-automation-review",
            "no-connector-credentials-stored-in-plan",
        ],
    }


def build_endpoint_remediation_sla_notification_plan_metadata(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": plan.get("plan_id"),
        "created_at": plan.get("generated_at"),
        "signer": plan.get("generated_by", "release-manager"),
        "decision_count": len(plan.get("eligible_providers", [])),
        "blocked_count": len(plan.get("suppressed_providers", [])),
        "approval_required_count": len(plan.get("acknowledgement_required_providers", [])),
        "metadata_kind": "endpoint-remediation-sla-notification-plan",
        "plan_id": plan.get("plan_id"),
        "report_id": plan.get("report_id"),
        "alert_level": plan.get("alert_level"),
        "selected_providers": plan.get("selected_providers", []),
        "suppressed_providers": [item.get("provider") for item in plan.get("suppressed_providers", [])],
        "suppressed_provider_count": len(plan.get("suppressed_providers", [])),
        "acknowledgement_required_providers": plan.get("acknowledgement_required_providers", []),
        "suppression_window_minutes": plan.get("suppression_window_minutes"),
        "notification_plan": plan,
    }


def acknowledge_endpoint_remediation_sla_notification(
    report_id: str,
    *,
    provider: str,
    acknowledged_by: str,
    acknowledgement_state: str = "acknowledged",
    external_ref: str | None = None,
    notes: str | None = None,
    plan_id: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    state = acknowledgement_state.strip().lower().replace("-", "_")
    allowed = {"acknowledged", "dismissed", "escalated", "resolved"}
    if state not in allowed:
        raise ValueError("acknowledgement_state must be one of: acknowledged, dismissed, escalated, resolved")
    normalized_provider = _normalize_endpoint_remediation_sla_notification_providers([provider])
    if not normalized_provider:
        raise ValueError("provider must be one of: webhook, slack, teams, jira, servicenow")
    provider = normalized_provider[0]
    now = now or datetime.now(timezone.utc)
    acknowledged_at = now.isoformat()
    material = f"{report_id}|{provider}|{state}|{acknowledged_by}|{acknowledged_at}"
    ack_id = f"erslaack-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.notification_ack.v1",
        "product": "CAVRA",
        "acknowledgement_id": ack_id,
        "report_id": report_id,
        "plan_id": plan_id,
        "provider": provider,
        "acknowledgement_state": state,
        "acknowledged_by": acknowledged_by,
        "acknowledged_at": acknowledged_at,
        "external_ref": external_ref,
        "notes": notes,
        "controls": [
            "acknowledgement-records-review-only",
            "no-provider-token-or-secret-stored",
            "endpoint-mutation-remains-private-connector-responsibility",
        ],
    }


def build_endpoint_remediation_sla_notification_ack_metadata(acknowledgement: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": acknowledgement.get("acknowledgement_id"),
        "created_at": acknowledgement.get("acknowledged_at"),
        "signer": acknowledgement.get("acknowledged_by", "release-manager"),
        "decision_count": 1,
        "blocked_count": 0,
        "approval_required_count": 0,
        "metadata_kind": "endpoint-remediation-sla-notification-ack",
        "acknowledgement_id": acknowledgement.get("acknowledgement_id"),
        "report_id": acknowledgement.get("report_id"),
        "plan_id": acknowledgement.get("plan_id"),
        "provider": acknowledgement.get("provider"),
        "acknowledgement_state": acknowledgement.get("acknowledgement_state"),
        "external_ref": acknowledgement.get("external_ref"),
        "acknowledgement": acknowledgement,
    }


def filter_endpoint_remediation_sla_notification_history(
    items: list[dict[str, Any]],
    *,
    report_id: str | None = None,
    provider: str | None = None,
    metadata_kind: str | None = None,
    acknowledgement_state: str | None = None,
    suppressed: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    allowed_kinds = {
        "endpoint-remediation-sla-notification-plan",
        "endpoint-remediation-sla-notification-ack",
        "release-connector-delivery",
    }
    filtered = [
        item
        for item in items
        if item.get("metadata_kind") in allowed_kinds
        and (
            item.get("metadata_kind") != "release-connector-delivery"
            or item.get("connector_delivery_source") == "endpoint_remediation_sla_notification"
        )
    ]
    if metadata_kind:
        filtered = [item for item in filtered if item.get("metadata_kind") == metadata_kind]
    if report_id:
        filtered = [
            item
            for item in filtered
            if item.get("report_id") == report_id or item.get("event_id") == report_id
        ]
    if provider:
        provider_key = provider.strip().lower().replace("-", "_")
        filtered = [
            item
            for item in filtered
            if item.get("provider") == provider_key
            or provider_key in {str(value) for value in item.get("providers", [])}
            or provider_key in {str(value) for value in item.get("selected_providers", [])}
            or provider_key in {str(value) for value in item.get("suppressed_providers", [])}
        ]
    if acknowledgement_state:
        state = acknowledgement_state.strip().lower().replace("-", "_")
        filtered = [item for item in filtered if item.get("acknowledgement_state") == state]
    if suppressed is not None:
        filtered = [
            item
            for item in filtered
            if (len(item.get("suppressed_providers", [])) > 0) is suppressed
        ]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_sla.notification_history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_remediation_sla_notification_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_remediation_sla_notification_history(items, limit=500)["items"]
    plans = [item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-notification-plan"]
    deliveries = [item for item in history if item.get("metadata_kind") == "release-connector-delivery"]
    acknowledgements = [
        item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-notification-ack"
    ]
    latest_plan_by_report: dict[str, dict[str, Any]] = {}
    for plan in plans:
        report_id = str(plan.get("report_id") or "")
        if not report_id:
            continue
        current = latest_plan_by_report.get(report_id)
        candidate_plan = plan.get("notification_plan") if isinstance(plan.get("notification_plan"), dict) else plan
        current_plan = current.get("notification_plan") if current and isinstance(current.get("notification_plan"), dict) else current
        candidate_has_required = bool(plan.get("acknowledgement_required_providers"))
        candidate_selected_providers = plan.get("selected_providers") or candidate_plan.get("selected_providers", [])
        candidate_has_selected = any(
            bool(route.get("selected")) for route in candidate_plan.get("routes", []) if isinstance(route, dict)
        ) or bool(candidate_selected_providers)
        current_has_required = bool(current and current.get("acknowledgement_required_providers"))
        current_selected_providers = (current or {}).get("selected_providers") or (
            current_plan.get("selected_providers", []) if current_plan else []
        )
        current_has_selected = bool(
            current_plan
            and any(bool(route.get("selected")) for route in current_plan.get("routes", []) if isinstance(route, dict))
        ) or bool(current_selected_providers)
        if (
            current is None
            or (candidate_has_required and not current_has_required)
            or (candidate_has_selected and not current_has_selected)
            or (
                candidate_has_required == current_has_required
                and candidate_has_selected == current_has_selected
                and str(plan.get("created_at", "")) > str(current.get("created_at", ""))
            )
        ):
            latest_plan_by_report[report_id] = plan
    acknowledged = {
        (str(item.get("report_id")), str(item.get("provider")))
        for item in acknowledgements
        if item.get("acknowledgement_state") in {"acknowledged", "resolved"}
    }
    outstanding = []
    for plan in latest_plan_by_report.values():
        for provider in plan.get("acknowledgement_required_providers", []):
            key = (str(plan.get("report_id")), str(provider))
            if key not in acknowledged:
                outstanding.append({"report_id": key[0], "provider": key[1], "plan_id": plan.get("plan_id")})
    failed_deliveries = [item for item in deliveries if not item.get("delivery_success")]
    suppressed_count = sum(len(item.get("suppressed_providers", [])) for item in plans)
    alert_level = "critical" if failed_deliveries or outstanding else "warning" if suppressed_count else "healthy"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.notification_dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "plan_count": len(plans),
        "delivery_count": len(deliveries),
        "failed_delivery_count": len(failed_deliveries),
        "acknowledgement_count": len(acknowledgements),
        "outstanding_acknowledgement_count": len(outstanding),
        "suppressed_provider_count": suppressed_count,
        "outstanding_acknowledgements": outstanding[:20],
        "latest": history[:10],
    }


def build_endpoint_remediation_sla_escalation_plan(
    items: list[dict[str, Any]],
    *,
    policy: dict[str, Any] | None = None,
    generated_by: str = "release-manager",
    now: datetime | None = None,
) -> dict[str, Any]:
    """Build owner SLO and escalation-ladder status from public notification metadata."""
    now = now or datetime.now(timezone.utc)
    policy = policy or {}
    history = filter_endpoint_remediation_sla_notification_history(items, limit=500)["items"]
    plans = [item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-notification-plan"]
    acknowledgements = [
        item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-notification-ack"
    ]
    latest_plan_by_report: dict[str, dict[str, Any]] = {}
    for plan in plans:
        report_id = str(plan.get("report_id") or "")
        if not report_id:
            continue
        current = latest_plan_by_report.get(report_id)
        if current is None or str(plan.get("created_at", "")) > str(current.get("created_at", "")):
            latest_plan_by_report[report_id] = plan
    latest_ack_by_route: dict[tuple[str, str], dict[str, Any]] = {}
    for acknowledgement in acknowledgements:
        key = (str(acknowledgement.get("report_id") or ""), str(acknowledgement.get("provider") or ""))
        if not key[0] or not key[1]:
            continue
        current = latest_ack_by_route.get(key)
        if current is None or str(acknowledgement.get("created_at", "")) > str(current.get("created_at", "")):
            latest_ack_by_route[key] = acknowledgement
    deliveries = [
        item
        for item in history
        if item.get("metadata_kind") == "release-connector-delivery"
        and item.get("connector_delivery_source") == "endpoint_remediation_sla_notification"
    ]
    for delivery in deliveries:
        report_id = str(delivery.get("event_id") or delivery.get("report_id") or "")
        providers = [str(provider) for provider in delivery.get("providers", []) if provider]
        if not report_id or not providers:
            continue
        current = latest_plan_by_report.get(report_id)
        current_plan = current.get("notification_plan") if current and isinstance(current.get("notification_plan"), dict) else current
        current_has_selected = bool(
            current_plan
            and any(bool(route.get("selected")) for route in current_plan.get("routes", []) if isinstance(route, dict))
        ) or bool((current or {}).get("selected_providers") or (current_plan.get("selected_providers", []) if current_plan else []))
        if current_has_selected:
            continue
        latest_plan_by_report[report_id] = {
            "metadata_kind": "endpoint-remediation-sla-notification-plan",
            "session_id": f"synthetic-{delivery.get('session_id', report_id)}",
            "created_at": delivery.get("created_at"),
            "report_id": report_id,
            "plan_id": delivery.get("session_id"),
            "selected_providers": providers,
            "acknowledgement_required_providers": providers if policy else [],
            "notification_plan": {
                "report_id": report_id,
                "generated_at": delivery.get("created_at"),
                "plan_id": delivery.get("session_id"),
                "alert_level": delivery.get("alert_level", "unknown"),
                "selected_providers": providers,
                "acknowledgement_required_providers": providers if policy else [],
                "routes": [
                    {
                        "provider": provider,
                        "selected": True,
                        "owner": policy.get("owner") or "release-governance",
                        "acknowledgement_required": bool(policy),
                    }
                    for provider in providers
                ],
            },
        }
    route_statuses: list[dict[str, Any]] = []
    for plan_metadata in latest_plan_by_report.values():
        plan = plan_metadata.get("notification_plan") if isinstance(plan_metadata.get("notification_plan"), dict) else plan_metadata
        report_id = str(plan.get("report_id") or plan_metadata.get("report_id") or "")
        alert_level = str(plan.get("alert_level") or plan_metadata.get("alert_level") or "healthy")
        created_at = _parse_release_datetime(plan.get("generated_at") or plan_metadata.get("created_at")) or now
        age_minutes = max(0.0, (now - created_at).total_seconds() / 60)
        required = {str(provider) for provider in plan.get("acknowledgement_required_providers", [])}
        routes = plan.get("routes", []) if isinstance(plan.get("routes"), list) else []
        if not routes:
            selected_providers = plan.get("selected_providers") or plan_metadata.get("selected_providers", [])
            routes = [
                {
                    "provider": provider,
                    "selected": True,
                    "owner": policy.get("owner") or "release-governance",
                    "acknowledgement_required": provider in required,
                }
                for provider in selected_providers
            ]
        for route in routes:
            provider = str(route.get("provider") or "")
            if not provider or not bool(route.get("selected")):
                continue
            if provider not in required and not policy:
                continue
            owner = str(route.get("owner") or policy.get("owner") or "release-governance")
            owner_slo = _endpoint_remediation_sla_owner_slo(policy, owner, alert_level, provider)
            acknowledgement = latest_ack_by_route.get((report_id, provider), {})
            state = str(acknowledgement.get("acknowledgement_state") or "pending")
            acknowledged = state in {"acknowledged", "resolved"}
            resolved = state == "resolved"
            acknowledgement_due_at = created_at + timedelta(minutes=owner_slo["acknowledgement_minutes"])
            resolution_due_at = created_at + timedelta(minutes=owner_slo["resolution_minutes"])
            ack_state = "met" if acknowledged else _endpoint_remediation_sla_slo_state(
                age_minutes,
                owner_slo["acknowledgement_minutes"],
            )
            resolution_state = "met" if resolved else _endpoint_remediation_sla_slo_state(
                age_minutes,
                owner_slo["resolution_minutes"],
            )
            escalation = _endpoint_remediation_sla_ladder_level(
                policy,
                age_minutes=age_minutes,
                owner=owner,
                alert_level=alert_level,
                provider=provider,
            )
            active = ack_state == "breached" or resolution_state == "breached" or bool(escalation)
            route_statuses.append(
                {
                    "report_id": report_id,
                    "plan_id": plan.get("plan_id") or plan_metadata.get("plan_id"),
                    "provider": provider,
                    "owner": owner,
                    "alert_level": alert_level,
                    "age_minutes": round(age_minutes, 2),
                    "acknowledgement_state": state,
                    "acknowledgement_slo_state": ack_state,
                    "resolution_slo_state": resolution_state,
                    "acknowledgement_minutes": owner_slo["acknowledgement_minutes"],
                    "resolution_minutes": owner_slo["resolution_minutes"],
                    "acknowledgement_due_at": acknowledgement_due_at.isoformat(),
                    "resolution_due_at": resolution_due_at.isoformat(),
                    "acknowledgement_id": acknowledgement.get("acknowledgement_id"),
                    "escalation_level": escalation.get("level") if escalation else None,
                    "escalation_after_minutes": escalation.get("after_minutes") if escalation else None,
                    "escalation_action": escalation.get("action") if escalation else None,
                    "escalation_providers": escalation.get("providers", []) if escalation else [],
                    "active_escalation": active,
                    "recommended_action": _endpoint_remediation_sla_escalation_ladder_action(
                        owner,
                        provider,
                        ack_state,
                        resolution_state,
                        escalation,
                    ),
                }
            )
    active_escalations = [item for item in route_statuses if item["active_escalation"]]
    owner_summary: dict[str, dict[str, Any]] = {}
    for item in route_statuses:
        owner = str(item["owner"])
        summary = owner_summary.setdefault(
            owner,
            {
                "owner": owner,
                "route_count": 0,
                "active_escalation_count": 0,
                "acknowledgement_breach_count": 0,
                "resolution_breach_count": 0,
                "providers": set(),
            },
        )
        summary["route_count"] += 1
        summary["active_escalation_count"] += 1 if item["active_escalation"] else 0
        summary["acknowledgement_breach_count"] += 1 if item["acknowledgement_slo_state"] == "breached" else 0
        summary["resolution_breach_count"] += 1 if item["resolution_slo_state"] == "breached" else 0
        summary["providers"].add(item["provider"])
    owners = []
    for summary in owner_summary.values():
        summary["providers"] = sorted(summary["providers"])
        owners.append(summary)
    generated_at = now.isoformat()
    material = json.dumps(
        {
            "generated_at": generated_at,
            "route_statuses": route_statuses,
        },
        sort_keys=True,
    )
    plan_id = f"erslaesc-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_plan.v1",
        "product": "CAVRA",
        "plan_id": plan_id,
        "generated_at": generated_at,
        "generated_by": generated_by,
        "alert_level": "critical" if active_escalations else "healthy",
        "route_count": len(route_statuses),
        "active_escalation_count": len(active_escalations),
        "acknowledgement_breach_count": len(
            [item for item in route_statuses if item["acknowledgement_slo_state"] == "breached"]
        ),
        "resolution_breach_count": len(
            [item for item in route_statuses if item["resolution_slo_state"] == "breached"]
        ),
        "owner_count": len(owners),
        "owners": sorted(owners, key=lambda item: (-int(item["active_escalation_count"]), str(item["owner"]))),
        "route_statuses": sorted(
            route_statuses,
            key=lambda item: (not item["active_escalation"], str(item["owner"]), str(item["provider"])),
        ),
        "controls": [
            "escalation-plan-derived-from-public-notification-metadata",
            "owner-slos-contain-no-connector-secrets",
            "private-connectors-remain-responsible-for-ticket-chat-or-pager-side-effects",
            "acknowledgement-and-resolution-slo-states-are-audit-metadata-only",
        ],
    }


def build_endpoint_remediation_sla_escalation_plan_metadata(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": plan.get("plan_id"),
        "created_at": plan.get("generated_at"),
        "signer": plan.get("generated_by", "release-manager"),
        "decision_count": int(plan.get("route_count") or 0),
        "blocked_count": int(plan.get("active_escalation_count") or 0),
        "approval_required_count": int(plan.get("acknowledgement_breach_count") or 0),
        "metadata_kind": "endpoint-remediation-sla-escalation-plan",
        "plan_id": plan.get("plan_id"),
        "alert_level": plan.get("alert_level"),
        "route_count": plan.get("route_count", 0),
        "active_escalation_count": plan.get("active_escalation_count", 0),
        "acknowledgement_breach_count": plan.get("acknowledgement_breach_count", 0),
        "resolution_breach_count": plan.get("resolution_breach_count", 0),
        "owner_count": plan.get("owner_count", 0),
        "owners": [item.get("owner") for item in plan.get("owners", []) if item.get("owner")],
        "escalation_plan": plan,
    }


def filter_endpoint_remediation_sla_escalation_history(
    items: list[dict[str, Any]],
    *,
    owner: str | None = None,
    provider: str | None = None,
    alert_level: str | None = None,
    active_only: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [
        item for item in items if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-plan"
    ]
    if alert_level:
        filtered = [item for item in filtered if item.get("alert_level") == alert_level]
    if owner or provider or active_only:
        owner_key = owner.strip().lower() if owner else None
        provider_key = provider.strip().lower().replace("-", "_") if provider else None
        filtered_by_route = []
        for item in filtered:
            plan = item.get("escalation_plan") if isinstance(item.get("escalation_plan"), dict) else item
            routes = plan.get("route_statuses", []) if isinstance(plan.get("route_statuses"), list) else []
            if owner_key:
                routes = [route for route in routes if str(route.get("owner", "")).lower() == owner_key]
            if provider_key:
                routes = [route for route in routes if str(route.get("provider", "")).lower() == provider_key]
            if active_only:
                routes = [route for route in routes if bool(route.get("active_escalation"))]
            if routes:
                filtered_by_route.append(item | {"matched_route_statuses": routes})
        filtered = filtered_by_route
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_remediation_sla_escalation_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_remediation_sla_escalation_history(items, limit=500)["items"]
    latest = history[0] if history else {}
    plan = latest.get("escalation_plan") if isinstance(latest.get("escalation_plan"), dict) else latest
    route_statuses = plan.get("route_statuses", []) if isinstance(plan.get("route_statuses"), list) else []
    active = [item for item in route_statuses if bool(item.get("active_escalation"))]
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": "critical" if active else "healthy",
        "plan_count": len(history),
        "route_count": len(route_statuses),
        "active_escalation_count": len(active),
        "acknowledgement_breach_count": len(
            [item for item in route_statuses if item.get("acknowledgement_slo_state") == "breached"]
        ),
        "resolution_breach_count": len(
            [item for item in route_statuses if item.get("resolution_slo_state") == "breached"]
        ),
        "owner_count": len({str(item.get("owner")) for item in route_statuses if item.get("owner")}),
        "owners": plan.get("owners", []),
        "active_escalations": active[:20],
        "latest": history[:10],
    }


def build_endpoint_remediation_sla_escalation_delivery_event(
    plan: dict[str, Any],
    *,
    generated_by: str = "release-manager",
    max_routes: int = 20,
) -> dict[str, Any]:
    """Build a public-safe connector event for active endpoint remediation SLA escalations."""
    max_routes = max(1, min(int(max_routes), 100))
    route_statuses = plan.get("route_statuses", []) if isinstance(plan.get("route_statuses"), list) else []
    active_routes = [item for item in route_statuses if isinstance(item, dict) and item.get("active_escalation")]
    selected_routes = active_routes[:max_routes]
    plan_id = str(plan.get("plan_id") or "endpoint-remediation-sla-escalation")
    owner_count = len({str(item.get("owner")) for item in selected_routes if item.get("owner")})
    provider_count = len({str(item.get("provider")) for item in selected_routes if item.get("provider")})
    ack_breach_count = len([item for item in selected_routes if item.get("acknowledgement_slo_state") == "breached"])
    resolution_breach_count = len([item for item in selected_routes if item.get("resolution_slo_state") == "breached"])
    alert_level = "critical" if selected_routes else "healthy"
    title = f"CAVRA endpoint remediation SLA escalation: {plan_id}"
    message = (
        f"{len(selected_routes)} active escalation routes across {owner_count} owners "
        f"and {provider_count} providers require review."
    )
    description = _endpoint_remediation_sla_escalation_delivery_description(
        plan_id,
        selected_routes,
        omitted_route_count=max(0, len(active_routes) - len(selected_routes)),
    )
    event = {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_delivery.v1",
        "product": "CAVRA",
        "event_type": "cavra.endpoint_remediation_sla.escalation_delivery",
        "session_id": plan_id,
        "plan_id": plan_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": generated_by,
        "source_plan_generated_at": plan.get("generated_at"),
        "alert_level": alert_level,
        "max_severity": "critical" if selected_routes else "low",
        "blocked_count": len(selected_routes),
        "approval_required_count": ack_breach_count + resolution_breach_count,
        "decision_count": int(plan.get("route_count") or len(route_statuses)),
        "summary": {
            "route_count": int(plan.get("route_count") or len(route_statuses)),
            "active_escalation_count": len(active_routes),
            "selected_route_count": len(selected_routes),
            "owner_count": owner_count,
            "provider_count": provider_count,
            "acknowledgement_breach_count": ack_breach_count,
            "resolution_breach_count": resolution_breach_count,
            "omitted_route_count": max(0, len(active_routes) - len(selected_routes)),
        },
        "routes": selected_routes,
        "omitted_route_count": max(0, len(active_routes) - len(selected_routes)),
        "controls": [
            "escalation-delivery-derived-from-public-escalation-plan",
            "connector-delivery-evidence-redacts-secrets",
            "owner-review-records-close-the-loop-before-private-remediation",
            "no-endpoint-mutation-performed-by-public-escalation-event",
        ],
    }
    event["provider_payloads"] = {
        "webhook": event | {"provider": "webhook"},
        "slack": _endpoint_remediation_sla_escalation_slack_payload(title, message, selected_routes),
        "teams": _endpoint_remediation_sla_escalation_teams_payload(title, message, alert_level, selected_routes),
        "jira": _endpoint_remediation_sla_jira_payload(title, description, alert_level),
        "servicenow": _endpoint_remediation_sla_servicenow_payload(title, description, plan_id, alert_level),
    }
    return event


def review_endpoint_remediation_sla_escalation(
    plan_id: str,
    *,
    report_id: str,
    provider: str,
    owner: str,
    reviewed_by: str,
    review_state: str = "accepted",
    external_ref: str | None = None,
    notes: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    state = review_state.strip().lower().replace("-", "_")
    allowed = {"accepted", "deferred", "resolved", "false_positive", "escalated"}
    if state not in allowed:
        raise ValueError("review_state must be one of: accepted, deferred, resolved, false_positive, escalated")
    normalized_provider = _normalize_endpoint_remediation_sla_notification_providers([provider])
    if not normalized_provider:
        raise ValueError("provider must be one of: webhook, slack, teams, jira, servicenow")
    if not plan_id:
        raise ValueError("plan_id is required")
    if not report_id:
        raise ValueError("report_id is required")
    if not owner:
        raise ValueError("owner is required")
    if not reviewed_by:
        raise ValueError("reviewed_by is required")
    now = now or datetime.now(timezone.utc)
    reviewed_at = now.isoformat()
    provider = normalized_provider[0]
    material = f"{plan_id}|{report_id}|{provider}|{owner}|{state}|{reviewed_by}|{reviewed_at}"
    review_id = f"erslaescr-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_review.v1",
        "product": "CAVRA",
        "review_id": review_id,
        "plan_id": plan_id,
        "report_id": report_id,
        "provider": provider,
        "owner": owner,
        "reviewed_by": reviewed_by,
        "review_state": state,
        "reviewed_at": reviewed_at,
        "external_ref": external_ref,
        "notes": notes,
        "controls": [
            "owner-review-records-audit-closure-only",
            "no-provider-token-or-secret-stored",
            "private-connectors-remain-responsible-for-ticket-chat-or-pager-side-effects",
        ],
    }


def build_endpoint_remediation_sla_escalation_review_metadata(review: dict[str, Any]) -> dict[str, Any]:
    unresolved = review.get("review_state") in {"accepted", "deferred", "escalated"}
    return {
        "session_id": review.get("review_id"),
        "created_at": review.get("reviewed_at"),
        "signer": review.get("reviewed_by", "release-manager"),
        "decision_count": 1,
        "blocked_count": 1 if review.get("review_state") == "escalated" else 0,
        "approval_required_count": 1 if unresolved else 0,
        "metadata_kind": "endpoint-remediation-sla-escalation-review",
        "review_id": review.get("review_id"),
        "plan_id": review.get("plan_id"),
        "report_id": review.get("report_id"),
        "provider": review.get("provider"),
        "owner": review.get("owner"),
        "review_state": review.get("review_state"),
        "external_ref": review.get("external_ref"),
        "review": review,
    }


def filter_endpoint_remediation_sla_escalation_action_history(
    items: list[dict[str, Any]],
    *,
    plan_id: str | None = None,
    owner: str | None = None,
    provider: str | None = None,
    metadata_kind: str | None = None,
    review_state: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    allowed_kinds = {
        "endpoint-remediation-sla-escalation-plan",
        "endpoint-remediation-sla-escalation-review",
        "endpoint-remediation-sla-escalation-recurrence-plan",
        "endpoint-remediation-sla-escalation-suppression-audit",
        "endpoint-remediation-sla-escalation-recurrence-retry-plan",
        "endpoint-remediation-sla-escalation-owner-digest",
        "endpoint-remediation-sla-escalation-suppression-trend",
        "endpoint-remediation-sla-escalation-recurrence-automation-run",
        "release-connector-delivery",
    }
    filtered = [
        item
        for item in items
        if item.get("metadata_kind") in allowed_kinds
        and (
            item.get("metadata_kind") != "release-connector-delivery"
            or item.get("connector_delivery_source")
            in {
                "endpoint_remediation_sla_escalation_delivery",
                "endpoint_remediation_sla_escalation_recurrence_delivery",
                "endpoint_remediation_sla_escalation_owner_digest",
            }
        )
    ]
    if metadata_kind:
        filtered = [item for item in filtered if item.get("metadata_kind") == metadata_kind]
    if plan_id:
        filtered = [
            item
            for item in filtered
            if item.get("plan_id") == plan_id
            or item.get("event_id") == plan_id
            or item.get("session_id") == plan_id
        ]
    if provider:
        provider_key = provider.strip().lower().replace("-", "_")
        filtered = [
            item
            for item in filtered
            if item.get("provider") == provider_key
            or provider_key in {str(value) for value in item.get("providers", [])}
            or _endpoint_remediation_sla_escalation_item_has_route(item, provider=provider_key)
        ]
    if owner:
        owner_key = owner.strip().lower()
        filtered = [
            item
            for item in filtered
            if str(item.get("owner", "")).lower() == owner_key
            or _endpoint_remediation_sla_escalation_item_has_route(item, owner=owner_key)
        ]
    if review_state:
        state = review_state.strip().lower().replace("-", "_")
        filtered = [item for item in filtered if item.get("review_state") == state]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_action_history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_remediation_sla_escalation_action_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_remediation_sla_escalation_action_history(items, limit=500)["items"]
    plans = [item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-plan"]
    deliveries = [item for item in history if item.get("metadata_kind") == "release-connector-delivery"]
    reviews = [item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-review"]
    recurrences = [
        item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-plan"
    ]
    suppression_audits = [
        item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-suppression-audit"
    ]
    retry_plans = [
        item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-retry-plan"
    ]
    owner_digests = [
        item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-owner-digest"
    ]
    suppression_trends = [
        item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-suppression-trend"
    ]
    automation_runs = [
        item
        for item in history
        if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-automation-run"
    ]
    failed_deliveries = [item for item in deliveries if not item.get("delivery_success")]
    unresolved_reviews = [item for item in reviews if item.get("review_state") in {"accepted", "deferred", "escalated"}]
    active_escalation_count = 0
    owners: set[str] = set()
    for item in plans:
        plan = item.get("escalation_plan") if isinstance(item.get("escalation_plan"), dict) else item
        routes = plan.get("route_statuses", []) if isinstance(plan.get("route_statuses"), list) else []
        active_escalation_count += len([route for route in routes if route.get("active_escalation")])
        owners.update(str(route.get("owner")) for route in routes if route.get("owner"))
    alert_level = "critical" if failed_deliveries or active_escalation_count else "warning" if unresolved_reviews else "healthy"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_action_dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "plan_count": len(plans),
        "delivery_count": len(deliveries),
        "failed_delivery_count": len(failed_deliveries),
        "owner_review_count": len(reviews),
        "unresolved_review_count": len(unresolved_reviews),
        "recurrence_plan_count": len(recurrences),
        "recurrence_suppressed_count": sum(int(item.get("suppressed_route_count") or 0) for item in recurrences),
        "suppression_audit_count": len(suppression_audits),
        "recurrence_retry_plan_count": len(retry_plans),
        "owner_digest_count": len(owner_digests),
        "suppression_trend_count": len(suppression_trends),
        "recurrence_automation_run_count": len(automation_runs),
        "active_escalation_count": active_escalation_count,
        "owner_count": len(owners),
        "latest": history[:10],
    }


def build_endpoint_remediation_sla_escalation_recurrence_plan(
    items: list[dict[str, Any]],
    *,
    policy: dict[str, Any] | None = None,
    generated_by: str = "release-manager",
    now: datetime | None = None,
) -> dict[str, Any]:
    """Plan recurring escalation follow-up with maintenance-window and owner-calendar suppression."""
    now = now or datetime.now(timezone.utc)
    policy = policy or {}
    history = filter_endpoint_remediation_sla_escalation_action_history(items, limit=500)["items"]
    plans = [item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-plan"]
    latest_plan_metadata = plans[0] if plans else {}
    latest_plan = (
        latest_plan_metadata.get("escalation_plan")
        if isinstance(latest_plan_metadata.get("escalation_plan"), dict)
        else latest_plan_metadata
    )
    plan_id = str(latest_plan.get("plan_id") or latest_plan_metadata.get("plan_id") or "endpoint-remediation-sla-escalation")
    route_statuses = latest_plan.get("route_statuses", []) if isinstance(latest_plan.get("route_statuses"), list) else []
    active_routes = [route for route in route_statuses if isinstance(route, dict) and route.get("active_escalation")]
    interval_minutes = max(
        1,
        int(policy.get("recurrence_interval_minutes", policy.get("default_recurrence_minutes", 60)) or 60),
    )
    max_recurrences = max(1, int(policy.get("max_recurrences_per_route", policy.get("max_recurrences", 3)) or 3))
    deliveries = [
        item
        for item in history
        if item.get("metadata_kind") == "release-connector-delivery"
        and item.get("connector_delivery_source") == "endpoint_remediation_sla_escalation_delivery"
        and item.get("event_id") == plan_id
    ]
    delivery_count = len(deliveries)
    latest_delivery_at = _latest_release_created_at(deliveries)
    recurrence_count = delivery_count
    reviews = [item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-review"]
    latest_review_by_route = _endpoint_remediation_sla_latest_review_by_route(reviews)
    route_decisions: list[dict[str, Any]] = []
    for route in active_routes:
        owner = str(route.get("owner") or "release-governance")
        provider = str(route.get("provider") or "")
        report_id = str(route.get("report_id") or "")
        route_plan_id = str(route.get("plan_id") or plan_id)
        route_key = _endpoint_remediation_sla_route_key(route_plan_id, report_id, provider, owner)
        latest_review = latest_review_by_route.get(route_key, {})
        review_state = str(latest_review.get("review_state") or "")
        maintenance_window = _endpoint_remediation_sla_matching_maintenance_window(
            policy,
            now=now,
            plan_id=route_plan_id,
            report_id=report_id,
            provider=provider,
            owner=owner,
        )
        owner_availability = _endpoint_remediation_sla_owner_availability(policy, owner, now=now)
        next_delivery_at = (
            (latest_delivery_at + timedelta(minutes=interval_minutes)).isoformat()
            if latest_delivery_at is not None
            else now.isoformat()
        )
        action = "deliver"
        reason = "active escalation is ready for recurring delivery"
        if review_state in {"resolved", "false_positive"}:
            action = "suppress"
            reason = f"owner review state is {review_state}"
        elif maintenance_window:
            action = "suppress"
            reason = "matching maintenance window is active"
        elif not owner_availability["available"]:
            action = "suppress"
            reason = owner_availability["reason"]
        elif recurrence_count >= max_recurrences:
            action = "suppress"
            reason = f"maximum recurrence count {max_recurrences} reached"
        elif latest_delivery_at is not None and now < latest_delivery_at + timedelta(minutes=interval_minutes):
            action = "wait"
            reason = f"recurrence interval {interval_minutes} minutes has not elapsed"
        route_decisions.append(
            {
                "route_key": route_key,
                "plan_id": route_plan_id,
                "report_id": report_id,
                "provider": provider,
                "owner": owner,
                "action": action,
                "reason": reason,
                "review_state": review_state or None,
                "latest_review_id": latest_review.get("review_id"),
                "recurrence_count": recurrence_count,
                "max_recurrences": max_recurrences,
                "recurrence_interval_minutes": interval_minutes,
                "latest_delivery_at": latest_delivery_at.isoformat() if latest_delivery_at else None,
                "next_delivery_at": next_delivery_at,
                "maintenance_window": maintenance_window,
                "owner_availability": owner_availability,
                "recommended_action": route.get("recommended_action"),
            }
        )
    deliverable = [item for item in route_decisions if item["action"] == "deliver"]
    waiting = [item for item in route_decisions if item["action"] == "wait"]
    suppressed = [item for item in route_decisions if item["action"] == "suppress"]
    generated_at = now.isoformat()
    material = json.dumps(
        {
            "generated_at": generated_at,
            "plan_id": plan_id,
            "route_decisions": route_decisions,
        },
        sort_keys=True,
    )
    recurrence_plan_id = f"erslaescrp-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_plan.v1",
        "product": "CAVRA",
        "recurrence_plan_id": recurrence_plan_id,
        "plan_id": plan_id,
        "generated_at": generated_at,
        "generated_by": generated_by,
        "alert_level": "critical" if deliverable else "warning" if waiting else "healthy",
        "route_count": len(route_decisions),
        "deliverable_route_count": len(deliverable),
        "waiting_route_count": len(waiting),
        "suppressed_route_count": len(suppressed),
        "maintenance_suppressed_count": len([item for item in suppressed if item.get("maintenance_window")]),
        "calendar_suppressed_count": len(
            [item for item in suppressed if not item.get("owner_availability", {}).get("available", True)]
        ),
        "recurrence_interval_minutes": interval_minutes,
        "max_recurrences_per_route": max_recurrences,
        "route_decisions": route_decisions,
        "controls": [
            "recurrence-plan-derived-from-public-escalation-action-metadata",
            "maintenance-windows-contain-no-provider-credentials",
            "owner-calendars-are-public-safe-availability-metadata",
            "suppression-decisions-do-not-perform-endpoint-mutation",
        ],
    }


def build_endpoint_remediation_sla_escalation_recurrence_plan_metadata(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": plan.get("recurrence_plan_id"),
        "created_at": plan.get("generated_at"),
        "signer": plan.get("generated_by", "release-manager"),
        "decision_count": int(plan.get("route_count") or 0),
        "blocked_count": int(plan.get("suppressed_route_count") or 0),
        "approval_required_count": int(plan.get("deliverable_route_count") or 0),
        "metadata_kind": "endpoint-remediation-sla-escalation-recurrence-plan",
        "recurrence_plan_id": plan.get("recurrence_plan_id"),
        "plan_id": plan.get("plan_id"),
        "alert_level": plan.get("alert_level"),
        "route_count": plan.get("route_count", 0),
        "deliverable_route_count": plan.get("deliverable_route_count", 0),
        "waiting_route_count": plan.get("waiting_route_count", 0),
        "suppressed_route_count": plan.get("suppressed_route_count", 0),
        "maintenance_suppressed_count": plan.get("maintenance_suppressed_count", 0),
        "calendar_suppressed_count": plan.get("calendar_suppressed_count", 0),
        "recurrence_plan": plan,
    }


def filter_endpoint_remediation_sla_escalation_recurrence_history(
    items: list[dict[str, Any]],
    *,
    plan_id: str | None = None,
    owner: str | None = None,
    provider: str | None = None,
    action: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [
        item for item in items if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-plan"
    ]
    if plan_id:
        filtered = [item for item in filtered if item.get("plan_id") == plan_id or item.get("session_id") == plan_id]
    if owner or provider or action:
        owner_key = owner.strip().lower() if owner else None
        provider_key = provider.strip().lower().replace("-", "_") if provider else None
        action_key = action.strip().lower() if action else None
        matched = []
        for item in filtered:
            plan = item.get("recurrence_plan") if isinstance(item.get("recurrence_plan"), dict) else item
            decisions = plan.get("route_decisions", []) if isinstance(plan.get("route_decisions"), list) else []
            if owner_key:
                decisions = [decision for decision in decisions if str(decision.get("owner", "")).lower() == owner_key]
            if provider_key:
                decisions = [decision for decision in decisions if str(decision.get("provider", "")).lower() == provider_key]
            if action_key:
                decisions = [decision for decision in decisions if str(decision.get("action", "")).lower() == action_key]
            if decisions:
                matched.append(item | {"matched_route_decisions": decisions})
        filtered = matched
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_remediation_sla_escalation_recurrence_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_remediation_sla_escalation_recurrence_history(items, limit=500)["items"]
    latest = history[0] if history else {}
    plan = latest.get("recurrence_plan") if isinstance(latest.get("recurrence_plan"), dict) else latest
    decisions = plan.get("route_decisions", []) if isinstance(plan.get("route_decisions"), list) else []
    deliverable = [item for item in decisions if item.get("action") == "deliver"]
    waiting = [item for item in decisions if item.get("action") == "wait"]
    suppressed = [item for item in decisions if item.get("action") == "suppress"]
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": "critical" if deliverable else "warning" if waiting else "healthy",
        "plan_count": len(history),
        "route_count": len(decisions),
        "deliverable_route_count": len(deliverable),
        "waiting_route_count": len(waiting),
        "suppressed_route_count": len(suppressed),
        "maintenance_suppressed_count": len([item for item in suppressed if item.get("maintenance_window")]),
        "calendar_suppressed_count": len(
            [item for item in suppressed if not item.get("owner_availability", {}).get("available", True)]
        ),
        "owners": sorted({str(item.get("owner")) for item in decisions if item.get("owner")}),
        "latest": history[:10],
    }


def build_endpoint_remediation_sla_escalation_recurrence_delivery_event(
    recurrence_plan: dict[str, Any],
    *,
    generated_by: str = "release-manager",
    max_routes: int = 50,
) -> dict[str, Any]:
    """Build a connector event from deliverable recurrence routes only."""
    max_routes = max(1, min(int(max_routes), 200))
    decisions = recurrence_plan.get("route_decisions", []) if isinstance(recurrence_plan.get("route_decisions"), list) else []
    deliverable = [item for item in decisions if isinstance(item, dict) and item.get("action") == "deliver"]
    selected = deliverable[:max_routes]
    recurrence_plan_id = str(recurrence_plan.get("recurrence_plan_id") or "endpoint-remediation-sla-recurrence")
    plan_id = str(recurrence_plan.get("plan_id") or "")
    owner_count = len({str(item.get("owner")) for item in selected if item.get("owner")})
    provider_count = len({str(item.get("provider")) for item in selected if item.get("provider")})
    title = f"CAVRA endpoint remediation recurrence batch: {recurrence_plan_id}"
    message = f"{len(selected)} deliverable recurrence routes across {owner_count} owners and {provider_count} providers."
    description = _endpoint_remediation_sla_recurrence_delivery_description(
        recurrence_plan_id,
        selected,
        omitted_route_count=max(0, len(deliverable) - len(selected)),
    )
    event = {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_delivery.v1",
        "product": "CAVRA",
        "event_type": "cavra.endpoint_remediation_sla.escalation_recurrence_delivery",
        "session_id": recurrence_plan_id,
        "recurrence_plan_id": recurrence_plan_id,
        "plan_id": plan_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": generated_by,
        "source_plan_generated_at": recurrence_plan.get("generated_at"),
        "alert_level": "critical" if selected else "healthy",
        "max_severity": "critical" if selected else "low",
        "blocked_count": len(selected),
        "approval_required_count": len(selected),
        "decision_count": int(recurrence_plan.get("route_count") or len(decisions)),
        "summary": {
            "deliverable_route_count": len(deliverable),
            "selected_route_count": len(selected),
            "suppressed_route_count": int(recurrence_plan.get("suppressed_route_count") or 0),
            "waiting_route_count": int(recurrence_plan.get("waiting_route_count") or 0),
            "owner_count": owner_count,
            "provider_count": provider_count,
            "omitted_route_count": max(0, len(deliverable) - len(selected)),
        },
        "routes": selected,
        "omitted_route_count": max(0, len(deliverable) - len(selected)),
        "controls": [
            "recurrence-delivery-derived-from-public-recurrence-plan",
            "only-deliverable-routes-included",
            "suppressed-and-waiting-routes-excluded-from-delivery-batch",
            "connector-delivery-evidence-redacts-secrets",
            "no-endpoint-mutation-performed-by-public-recurrence-event",
        ],
    }
    event["provider_payloads"] = {
        "webhook": event | {"provider": "webhook"},
        "slack": _endpoint_remediation_sla_escalation_slack_payload(title, message, selected),
        "teams": _endpoint_remediation_sla_escalation_teams_payload(title, message, event["alert_level"], selected),
        "jira": _endpoint_remediation_sla_jira_payload(title, description, event["alert_level"]),
        "servicenow": _endpoint_remediation_sla_servicenow_payload(
            title,
            description,
            recurrence_plan_id,
            event["alert_level"],
        ),
    }
    return event


def build_endpoint_remediation_sla_escalation_suppression_audit(
    recurrence_plan: dict[str, Any],
    *,
    generated_by: str = "release-manager",
) -> dict[str, Any]:
    decisions = recurrence_plan.get("route_decisions", []) if isinstance(recurrence_plan.get("route_decisions"), list) else []
    suppressed = [item for item in decisions if isinstance(item, dict) and item.get("action") == "suppress"]
    waiting = [item for item in decisions if isinstance(item, dict) and item.get("action") == "wait"]
    deliverable = [item for item in decisions if isinstance(item, dict) and item.get("action") == "deliver"]
    generated_at = datetime.now(timezone.utc).isoformat()
    recurrence_plan_id = str(recurrence_plan.get("recurrence_plan_id") or "endpoint-remediation-sla-recurrence")
    material = json.dumps(
        {
            "recurrence_plan_id": recurrence_plan_id,
            "generated_at": generated_at,
            "suppressed": suppressed,
            "waiting": waiting,
        },
        sort_keys=True,
    )
    audit_id = f"erslaescaudit-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_suppression_audit.v1",
        "product": "CAVRA",
        "audit_id": audit_id,
        "recurrence_plan_id": recurrence_plan_id,
        "plan_id": recurrence_plan.get("plan_id"),
        "generated_at": generated_at,
        "generated_by": generated_by,
        "alert_level": "warning" if suppressed or waiting else "healthy",
        "summary": {
            "route_count": len(decisions),
            "deliverable_route_count": len(deliverable),
            "suppressed_route_count": len(suppressed),
            "waiting_route_count": len(waiting),
            "maintenance_suppressed_count": len([item for item in suppressed if item.get("maintenance_window")]),
            "calendar_suppressed_count": len(
                [item for item in suppressed if not item.get("owner_availability", {}).get("available", True)]
            ),
            "max_recurrence_suppressed_count": len(
                [item for item in suppressed if "maximum recurrence count" in str(item.get("reason") or "")]
            ),
            "interval_wait_count": len(waiting),
        },
        "suppressed_routes": suppressed,
        "waiting_routes": waiting,
        "deliverable_routes": deliverable,
        "controls": [
            "suppression-audit-derived-from-public-recurrence-plan",
            "maintenance-and-calendar-suppression-reasons-recorded",
            "connector-secrets-not-included",
            "audit-export-does-not-perform-delivery-or-endpoint-mutation",
        ],
    }


def build_endpoint_remediation_sla_escalation_suppression_audit_metadata(
    audit: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    summary = audit.get("summary", {}) if isinstance(audit.get("summary"), dict) else {}
    metadata = {
        "session_id": audit.get("audit_id"),
        "created_at": audit.get("generated_at"),
        "signer": audit.get("generated_by", "release-manager"),
        "decision_count": int(summary.get("route_count") or 0),
        "blocked_count": int(summary.get("suppressed_route_count") or 0),
        "approval_required_count": int(summary.get("waiting_route_count") or 0),
        "metadata_kind": "endpoint-remediation-sla-escalation-suppression-audit",
        "audit_id": audit.get("audit_id"),
        "recurrence_plan_id": audit.get("recurrence_plan_id"),
        "plan_id": audit.get("plan_id"),
        "alert_level": audit.get("alert_level"),
        "suppressed_route_count": summary.get("suppressed_route_count", 0),
        "waiting_route_count": summary.get("waiting_route_count", 0),
        "maintenance_suppressed_count": summary.get("maintenance_suppressed_count", 0),
        "calendar_suppressed_count": summary.get("calendar_suppressed_count", 0),
        "suppression_audit": audit,
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def build_endpoint_remediation_sla_escalation_recurrence_retry_plan(
    items: list[dict[str, Any]],
    *,
    policy: dict[str, Any] | None = None,
    generated_by: str = "release-manager",
    now: datetime | None = None,
) -> dict[str, Any]:
    """Plan safe retries for failed recurrence delivery batches."""
    now = now or datetime.now(timezone.utc)
    policy = policy or {}
    max_retry_attempts = max(1, int(policy.get("max_retry_attempts", policy.get("max_retries", 3)) or 3))
    retry_delay_minutes = max(1, int(policy.get("retry_delay_minutes", policy.get("delay_minutes", 15)) or 15))
    backoff_multiplier = max(1.0, float(policy.get("backoff_multiplier", policy.get("multiplier", 2.0)) or 2.0))
    history = filter_endpoint_remediation_sla_escalation_action_history(items, limit=500)["items"]
    recurrence_by_id = _endpoint_remediation_sla_recurrence_plan_by_id(history)
    failed_deliveries = [
        item
        for item in history
        if item.get("metadata_kind") == "release-connector-delivery"
        and item.get("connector_delivery_source") == "endpoint_remediation_sla_escalation_recurrence_delivery"
        and not item.get("delivery_success")
    ]
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in failed_deliveries:
        recurrence_plan_id = str(item.get("event_id") or item.get("session_id") or "")
        if not recurrence_plan_id:
            continue
        failed_providers = [str(provider) for provider in item.get("failed_providers", []) if provider]
        if not failed_providers:
            failed_providers = [str(provider) for provider in item.get("providers", []) if provider]
        for provider in failed_providers:
            grouped.setdefault((recurrence_plan_id, provider), []).append(item)

    retry_decisions: list[dict[str, Any]] = []
    for (recurrence_plan_id, provider), failures in sorted(grouped.items()):
        failures = sorted(failures, key=lambda item: str(item.get("created_at", "")), reverse=True)
        latest = failures[0]
        retry_count = len(failures)
        delay = retry_delay_minutes * (backoff_multiplier ** max(0, retry_count - 1))
        latest_at = _parse_release_datetime(latest.get("created_at"))
        next_retry_at = (latest_at + timedelta(minutes=delay)).isoformat() if latest_at else now.isoformat()
        action = "retry"
        reason = "failed recurrence delivery is eligible for retry"
        if retry_count >= max_retry_attempts:
            action = "suppress"
            reason = f"maximum retry attempts {max_retry_attempts} reached"
        elif latest_at is not None and now < latest_at + timedelta(minutes=delay):
            action = "wait"
            reason = f"retry delay {int(delay)} minutes has not elapsed"
        source_plan = recurrence_by_id.get(recurrence_plan_id, {})
        matching_routes = _endpoint_remediation_sla_routes_for_provider(source_plan, provider)
        retry_decisions.append(
            {
                "recurrence_plan_id": recurrence_plan_id,
                "plan_id": source_plan.get("plan_id") or latest.get("plan_id"),
                "provider": provider,
                "action": action,
                "reason": reason,
                "retry_count": retry_count,
                "max_retry_attempts": max_retry_attempts,
                "retry_delay_minutes": int(delay),
                "latest_delivery_id": latest.get("session_id"),
                "latest_delivery_at": latest.get("created_at"),
                "next_retry_at": next_retry_at,
                "failed_status_codes": latest.get("status_codes", []),
                "route_count": len(matching_routes),
                "routes": matching_routes,
            }
        )

    retryable = [item for item in retry_decisions if item["action"] == "retry"]
    waiting = [item for item in retry_decisions if item["action"] == "wait"]
    suppressed = [item for item in retry_decisions if item["action"] == "suppress"]
    generated_at = now.isoformat()
    material = json.dumps(
        {
            "generated_at": generated_at,
            "retry_decisions": retry_decisions,
        },
        sort_keys=True,
    )
    retry_plan_id = f"erslaescrtry-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_retry_plan.v1",
        "product": "CAVRA",
        "retry_plan_id": retry_plan_id,
        "generated_at": generated_at,
        "generated_by": generated_by,
        "alert_level": "critical" if retryable else "warning" if waiting else "healthy",
        "decision_count": len(retry_decisions),
        "retryable_count": len(retryable),
        "waiting_count": len(waiting),
        "suppressed_count": len(suppressed),
        "max_retry_attempts": max_retry_attempts,
        "base_retry_delay_minutes": retry_delay_minutes,
        "backoff_multiplier": backoff_multiplier,
        "retry_decisions": retry_decisions,
        "controls": [
            "retry-plan-derived-from-redacted-recurrence-delivery-metadata",
            "retry-policy-contains-no-provider-credentials",
            "failed-provider-selection-preserves-delivery-evidence",
            "public-retry-plan-does-not-perform-endpoint-mutation",
        ],
    }


def build_endpoint_remediation_sla_escalation_recurrence_retry_plan_metadata(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": plan.get("retry_plan_id"),
        "created_at": plan.get("generated_at"),
        "signer": plan.get("generated_by", "release-manager"),
        "decision_count": int(plan.get("decision_count") or 0),
        "blocked_count": int(plan.get("suppressed_count") or 0),
        "approval_required_count": int(plan.get("retryable_count") or 0),
        "metadata_kind": "endpoint-remediation-sla-escalation-recurrence-retry-plan",
        "retry_plan_id": plan.get("retry_plan_id"),
        "alert_level": plan.get("alert_level"),
        "retryable_count": plan.get("retryable_count", 0),
        "waiting_count": plan.get("waiting_count", 0),
        "suppressed_count": plan.get("suppressed_count", 0),
        "retry_plan": plan,
    }


def build_endpoint_remediation_sla_escalation_owner_digest_event(
    recurrence_plan: dict[str, Any],
    *,
    retry_plan: dict[str, Any] | None = None,
    generated_by: str = "release-manager",
) -> dict[str, Any]:
    """Build an owner digest event from unresolved recurrence and retry routes."""
    decisions = recurrence_plan.get("route_decisions", []) if isinstance(recurrence_plan.get("route_decisions"), list) else []
    unresolved = [
        item
        for item in decisions
        if isinstance(item, dict) and item.get("action") in {"deliver", "wait"}
    ]
    retry_decisions = (
        retry_plan.get("retry_decisions", [])
        if isinstance(retry_plan, dict) and isinstance(retry_plan.get("retry_decisions"), list)
        else []
    )
    owners: dict[str, dict[str, Any]] = {}
    for route in unresolved:
        owner = str(route.get("owner") or "release-governance")
        provider = str(route.get("provider") or "unknown")
        entry = owners.setdefault(owner, {"owner": owner, "route_count": 0, "providers": {}, "routes": []})
        entry["route_count"] += 1
        entry["providers"][provider] = int(entry["providers"].get(provider, 0)) + 1
        entry["routes"].append(route)
    for decision in retry_decisions:
        if not isinstance(decision, dict) or decision.get("action") not in {"retry", "wait"}:
            continue
        for route in decision.get("routes", []) if isinstance(decision.get("routes"), list) else []:
            owner = str(route.get("owner") or "release-governance")
            provider = str(decision.get("provider") or route.get("provider") or "unknown")
            entry = owners.setdefault(owner, {"owner": owner, "route_count": 0, "providers": {}, "routes": []})
            entry.setdefault("retry_count", 0)
            entry["retry_count"] = int(entry.get("retry_count") or 0) + 1
            entry["providers"][provider] = int(entry["providers"].get(provider, 0)) + 1
    owner_summaries = []
    for owner, entry in sorted(owners.items()):
        owner_summaries.append(
            {
                "owner": owner,
                "route_count": int(entry.get("route_count") or 0),
                "retry_count": int(entry.get("retry_count") or 0),
                "providers": dict(sorted(entry.get("providers", {}).items())),
                "routes": entry.get("routes", [])[:25],
            }
        )
    recurrence_plan_id = str(recurrence_plan.get("recurrence_plan_id") or "endpoint-remediation-sla-recurrence")
    generated_at = datetime.now(timezone.utc).isoformat()
    digest_id = f"erslaescdigest-{hashlib.sha256(f'{recurrence_plan_id}|{generated_at}'.encode('utf-8')).hexdigest()[:16]}"
    title = f"CAVRA endpoint remediation owner digest: {recurrence_plan_id}"
    message = f"{len(unresolved)} unresolved recurrence routes across {len(owner_summaries)} owners."
    description = _endpoint_remediation_sla_owner_digest_description(recurrence_plan_id, owner_summaries)
    event = {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_owner_digest.v1",
        "product": "CAVRA",
        "event_type": "cavra.endpoint_remediation_sla.escalation_owner_digest",
        "session_id": digest_id,
        "digest_id": digest_id,
        "recurrence_plan_id": recurrence_plan_id,
        "retry_plan_id": retry_plan.get("retry_plan_id") if isinstance(retry_plan, dict) else None,
        "plan_id": recurrence_plan.get("plan_id"),
        "generated_at": generated_at,
        "generated_by": generated_by,
        "alert_level": "critical" if unresolved else "healthy",
        "blocked_count": len(unresolved),
        "approval_required_count": len(unresolved),
        "summary": {
            "owner_count": len(owner_summaries),
            "unresolved_route_count": len(unresolved),
            "retryable_count": int(retry_plan.get("retryable_count") or 0) if isinstance(retry_plan, dict) else 0,
            "waiting_retry_count": int(retry_plan.get("waiting_count") or 0) if isinstance(retry_plan, dict) else 0,
        },
        "owners": owner_summaries,
        "controls": [
            "owner-digest-derived-from-public-recurrence-and-retry-metadata",
            "digest-notification-contains-no-provider-credentials",
            "digest-routes-are-summary-only-and-do-not-mutate-endpoints",
        ],
    }
    event["provider_payloads"] = {
        "webhook": event | {"provider": "webhook"},
        "slack": _endpoint_remediation_sla_owner_digest_slack_payload(title, message, owner_summaries),
        "teams": _endpoint_remediation_sla_owner_digest_teams_payload(title, message, event["alert_level"], owner_summaries),
        "jira": _endpoint_remediation_sla_jira_payload(title, description, event["alert_level"]),
        "servicenow": _endpoint_remediation_sla_servicenow_payload(
            title,
            description,
            digest_id,
            event["alert_level"],
        ),
    }
    return event


def build_endpoint_remediation_sla_escalation_owner_digest_metadata(event: dict[str, Any]) -> dict[str, Any]:
    summary = event.get("summary", {}) if isinstance(event.get("summary"), dict) else {}
    return {
        "session_id": event.get("digest_id") or event.get("session_id"),
        "created_at": event.get("generated_at"),
        "signer": event.get("generated_by", "release-manager"),
        "decision_count": int(summary.get("unresolved_route_count") or 0),
        "blocked_count": int(event.get("blocked_count") or 0),
        "approval_required_count": int(event.get("approval_required_count") or 0),
        "metadata_kind": "endpoint-remediation-sla-escalation-owner-digest",
        "digest_id": event.get("digest_id"),
        "recurrence_plan_id": event.get("recurrence_plan_id"),
        "retry_plan_id": event.get("retry_plan_id"),
        "plan_id": event.get("plan_id"),
        "owner_count": summary.get("owner_count", 0),
        "unresolved_route_count": summary.get("unresolved_route_count", 0),
        "owner_digest": event,
    }


def build_endpoint_remediation_sla_escalation_suppression_trends(
    items: list[dict[str, Any]],
    *,
    generated_by: str = "release-manager",
) -> dict[str, Any]:
    """Summarize suppression and wait reasons across recurrence plans and audits."""
    history = filter_endpoint_remediation_sla_escalation_action_history(items, limit=500)["items"]
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in history:
        if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-plan":
            plan = item.get("recurrence_plan") if isinstance(item.get("recurrence_plan"), dict) else item
            created_at = str(item.get("created_at") or plan.get("generated_at") or "")
            for decision in plan.get("route_decisions", []) if isinstance(plan.get("route_decisions"), list) else []:
                if not isinstance(decision, dict) or decision.get("action") not in {"suppress", "wait"}:
                    continue
                key = f"{item.get('session_id')}|{decision.get('route_key')}|{decision.get('action')}"
                if key in seen:
                    continue
                seen.add(key)
                rows.append(_endpoint_remediation_sla_suppression_trend_row(decision, created_at))
        elif item.get("metadata_kind") == "endpoint-remediation-sla-escalation-suppression-audit":
            audit = item.get("suppression_audit") if isinstance(item.get("suppression_audit"), dict) else item
            created_at = str(item.get("created_at") or audit.get("generated_at") or "")
            for action, key_name in (("suppress", "suppressed_routes"), ("wait", "waiting_routes")):
                for decision in audit.get(key_name, []) if isinstance(audit.get(key_name), list) else []:
                    if not isinstance(decision, dict):
                        continue
                    key = f"{item.get('session_id')}|{decision.get('route_key')}|{action}"
                    if key in seen:
                        continue
                    seen.add(key)
                    rows.append(_endpoint_remediation_sla_suppression_trend_row(decision | {"action": action}, created_at))

    categories: dict[str, int] = {}
    owners: dict[str, int] = {}
    providers: dict[str, int] = {}
    for row in rows:
        categories[row["category"]] = categories.get(row["category"], 0) + 1
        owners[row["owner"]] = owners.get(row["owner"], 0) + 1
        providers[row["provider"]] = providers.get(row["provider"], 0) + 1
    generated_at = datetime.now(timezone.utc).isoformat()
    material = json.dumps({"generated_at": generated_at, "rows": rows}, sort_keys=True)
    trend_id = f"erslaesctrend-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_suppression_trend.v1",
        "product": "CAVRA",
        "trend_id": trend_id,
        "generated_at": generated_at,
        "generated_by": generated_by,
        "alert_level": "warning" if rows else "healthy",
        "suppression_event_count": len(rows),
        "category_counts": dict(sorted(categories.items())),
        "owner_counts": dict(sorted(owners.items())),
        "provider_counts": dict(sorted(providers.items())),
        "latest_events": sorted(rows, key=lambda row: row.get("created_at", ""), reverse=True)[:25],
        "controls": [
            "suppression-trends-derived-from-public-recurrence-and-audit-metadata",
            "trend-report-contains-no-connector-credentials",
            "trend-report-does-not-perform-delivery-or-endpoint-mutation",
        ],
    }


def build_endpoint_remediation_sla_escalation_suppression_trend_metadata(trend: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": trend.get("trend_id"),
        "created_at": trend.get("generated_at"),
        "signer": trend.get("generated_by", "release-manager"),
        "decision_count": int(trend.get("suppression_event_count") or 0),
        "blocked_count": int(trend.get("suppression_event_count") or 0),
        "approval_required_count": 0,
        "metadata_kind": "endpoint-remediation-sla-escalation-suppression-trend",
        "trend_id": trend.get("trend_id"),
        "alert_level": trend.get("alert_level"),
        "suppression_event_count": trend.get("suppression_event_count", 0),
        "category_counts": trend.get("category_counts", {}),
        "suppression_trend": trend,
    }


def build_endpoint_remediation_sla_escalation_recurrence_automation_run(
    items: list[dict[str, Any]],
    *,
    retry_policy: dict[str, Any] | None = None,
    schedule: dict[str, Any] | None = None,
    generated_by: str = "release-manager",
    dry_run: bool = True,
    max_digest_plans: int = 5,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Plan a scheduled recurrence automation pass without embedding connector credentials."""
    now = now or datetime.now(timezone.utc)
    schedule = schedule or {}
    interval_minutes = max(1, int(schedule.get("interval_minutes", schedule.get("schedule_interval_minutes", 60)) or 60))
    window_start = _floor_release_datetime(now, interval_minutes)
    window_end = window_start + timedelta(minutes=interval_minutes)
    max_digest_plans = max(1, min(int(max_digest_plans or 5), 25))
    history = filter_endpoint_remediation_sla_escalation_action_history(items, limit=500)["items"]
    recurrence_items = [
        item for item in history if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-plan"
    ]
    recurrence_items = sorted(recurrence_items, key=lambda item: str(item.get("created_at", "")), reverse=True)
    retry_plan = build_endpoint_remediation_sla_escalation_recurrence_retry_plan(
        history,
        policy=retry_policy,
        generated_by=generated_by,
        now=now,
    )
    suppression_trend = build_endpoint_remediation_sla_escalation_suppression_trends(history, generated_by=generated_by)
    owner_digest_events: list[dict[str, Any]] = []
    for item in recurrence_items[:max_digest_plans]:
        recurrence_plan = item.get("recurrence_plan") if isinstance(item.get("recurrence_plan"), dict) else item
        if not isinstance(recurrence_plan, dict):
            continue
        event = build_endpoint_remediation_sla_escalation_owner_digest_event(
            recurrence_plan,
            retry_plan=retry_plan,
            generated_by=generated_by,
        )
        if event.get("owners"):
            owner_digest_events.append(event)

    follow_up_actions = _endpoint_remediation_sla_recurrence_follow_up_actions(
        retry_plan,
        owner_digest_events,
        suppression_trend,
    )
    material = json.dumps(
        {
            "window_start": window_start.isoformat(),
            "generated_by": generated_by,
            "dry_run": dry_run,
            "recurrence_plan_ids": [item.get("recurrence_plan_id") or item.get("session_id") for item in recurrence_items],
            "failed_delivery_ids": [
                item.get("session_id")
                for item in history
                if item.get("metadata_kind") == "release-connector-delivery"
                and item.get("connector_delivery_source") == "endpoint_remediation_sla_escalation_recurrence_delivery"
                and not item.get("delivery_success")
            ],
        },
        sort_keys=True,
    )
    run_id = f"erslaescauto-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_run.v1",
        "product": "CAVRA",
        "run_id": run_id,
        "generated_at": now.isoformat(),
        "generated_by": generated_by,
        "dry_run": bool(dry_run),
        "schedule": {
            "interval_minutes": interval_minutes,
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "enabled": bool(schedule.get("enabled", True)),
        },
        "summary": {
            "recurrence_plan_count": len(recurrence_items),
            "retry_plan_count": 1,
            "retryable_count": int(retry_plan.get("retryable_count") or 0),
            "waiting_retry_count": int(retry_plan.get("waiting_count") or 0),
            "suppressed_retry_count": int(retry_plan.get("suppressed_count") or 0),
            "owner_digest_count": len(owner_digest_events),
            "owner_digest_route_count": sum(
                int(event.get("summary", {}).get("unresolved_route_count") or 0)
                for event in owner_digest_events
                if isinstance(event.get("summary"), dict)
            ),
            "suppression_event_count": int(suppression_trend.get("suppression_event_count") or 0),
            "follow_up_action_count": len(follow_up_actions),
        },
        "retry_plan": retry_plan,
        "owner_digest_events": owner_digest_events,
        "suppression_trend": suppression_trend,
        "follow_up_actions": follow_up_actions,
        "controls": [
            "automation-run-derived-from-public-recurrence-metadata",
            "scheduled-worker-run-contains-no-connector-secrets",
            "dry-run-default-prevents-accidental-notification-delivery",
            "idempotency-key-derived-from-schedule-window-and-input-metadata",
        ],
    }


def build_endpoint_remediation_sla_escalation_recurrence_automation_run_metadata(
    run: dict[str, Any],
) -> dict[str, Any]:
    summary = run.get("summary", {}) if isinstance(run.get("summary"), dict) else {}
    return {
        "session_id": run.get("run_id"),
        "created_at": run.get("generated_at"),
        "signer": run.get("generated_by", "release-manager"),
        "decision_count": int(summary.get("follow_up_action_count") or 0),
        "blocked_count": int(summary.get("suppressed_retry_count") or 0),
        "approval_required_count": int(summary.get("owner_digest_count") or 0),
        "metadata_kind": "endpoint-remediation-sla-escalation-recurrence-automation-run",
        "run_id": run.get("run_id"),
        "dry_run": bool(run.get("dry_run", True)),
        "retryable_count": summary.get("retryable_count", 0),
        "owner_digest_count": summary.get("owner_digest_count", 0),
        "suppression_event_count": summary.get("suppression_event_count", 0),
        "automation_run": run,
    }


def filter_endpoint_remediation_sla_escalation_recurrence_automation_history(
    items: list[dict[str, Any]],
    *,
    dry_run: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [
        item
        for item in items
        if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-automation-run"
    ]
    if dry_run is not None:
        filtered = [item for item in filtered if bool(item.get("dry_run", True)) is dry_run]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_remediation_sla_escalation_recurrence_automation_dashboard(
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    runs = filter_endpoint_remediation_sla_escalation_recurrence_automation_history(items, limit=500)["items"]
    retryable_count = 0
    owner_digest_count = 0
    suppression_event_count = 0
    dry_run_count = 0
    executed_count = 0
    for item in runs:
        run = item.get("automation_run") if isinstance(item.get("automation_run"), dict) else item
        summary = run.get("summary", {}) if isinstance(run.get("summary"), dict) else {}
        retryable_count += int(summary.get("retryable_count") or item.get("retryable_count") or 0)
        owner_digest_count += int(summary.get("owner_digest_count") or item.get("owner_digest_count") or 0)
        suppression_event_count += int(summary.get("suppression_event_count") or item.get("suppression_event_count") or 0)
        if item.get("dry_run", True):
            dry_run_count += 1
        else:
            executed_count += 1
    alert_level = "critical" if retryable_count else "warning" if owner_digest_count or suppression_event_count else "healthy"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "run_count": len(runs),
        "dry_run_count": dry_run_count,
        "executed_count": executed_count,
        "retryable_count": retryable_count,
        "owner_digest_count": owner_digest_count,
        "suppression_event_count": suppression_event_count,
        "latest": runs[:10],
    }


def build_endpoint_remediation_sla_escalation_recurrence_automation_health(
    items: list[dict[str, Any]],
    *,
    expected_interval_minutes: int = 30,
    stale_metadata_minutes: int = 120,
    now: datetime | None = None,
) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    expected_interval_minutes = max(1, int(expected_interval_minutes or 30))
    stale_metadata_minutes = max(expected_interval_minutes, int(stale_metadata_minutes or expected_interval_minutes * 4))
    missed_after_minutes = expected_interval_minutes * 2
    runs = filter_endpoint_remediation_sla_escalation_recurrence_automation_history(items, limit=500)["items"]
    latest_run = runs[0] if runs else {}
    latest_run_at = _parse_release_datetime(latest_run.get("created_at") or latest_run.get("generated_at"))
    latest_run_age_minutes = (
        int((now - latest_run_at).total_seconds() // 60)
        if latest_run_at is not None and now >= latest_run_at
        else None
    )
    missed_run_count = 1 if latest_run_at is None or (latest_run_age_minutes or 0) > missed_after_minutes else 0
    disabled_schedule_count = 0
    failed_job_count = 0
    for item in runs:
        run = item.get("automation_run") if isinstance(item.get("automation_run"), dict) else item
        schedule = run.get("schedule", {}) if isinstance(run.get("schedule"), dict) else {}
        status = str(run.get("status") or item.get("status") or "").lower()
        if schedule.get("enabled") is False:
            disabled_schedule_count += 1
        if status in {"failed", "error", "timeout", "cancelled"}:
            failed_job_count += 1
    metadata_kinds = {
        "endpoint-remediation-sla-escalation-recurrence-plan": "recurrence_plan",
        "endpoint-remediation-sla-escalation-recurrence-retry-plan": "retry_plan",
        "endpoint-remediation-sla-escalation-owner-digest": "owner_digest",
        "endpoint-remediation-sla-escalation-suppression-trend": "suppression_trend",
    }
    stale_metadata: list[dict[str, Any]] = []
    for metadata_kind, label in metadata_kinds.items():
        kind_items = [item for item in items if item.get("metadata_kind") == metadata_kind]
        latest = max(kind_items, key=lambda item: str(item.get("created_at", "")), default={})
        latest_at = _parse_release_datetime(latest.get("created_at"))
        if latest_at is None:
            stale_metadata.append({"kind": label, "metadata_kind": metadata_kind, "state": "missing", "age_minutes": None})
            continue
        age_minutes = int((now - latest_at).total_seconds() // 60) if now >= latest_at else 0
        if age_minutes > stale_metadata_minutes:
            stale_metadata.append(
                {
                    "kind": label,
                    "metadata_kind": metadata_kind,
                    "state": "stale",
                    "age_minutes": age_minutes,
                    "latest_id": latest.get("session_id") or latest.get("run_id"),
                }
            )
    connector_failures = [
        item
        for item in items
        if item.get("metadata_kind") == "release-connector-delivery"
        and item.get("connector_delivery_source") == "endpoint_remediation_sla_escalation_owner_digest"
        and not item.get("delivery_success")
    ]
    alerts: list[dict[str, Any]] = []
    if missed_run_count:
        alerts.append(
            {
                "severity": "critical",
                "category": "missed_run",
                "message": "No recurrence automation worker run has completed inside the expected schedule window.",
            }
        )
    if failed_job_count:
        alerts.append(
            {
                "severity": "critical",
                "category": "failed_job",
                "message": f"{failed_job_count} recurrence automation worker runs reported a failed status.",
            }
        )
    if connector_failures:
        alerts.append(
            {
                "severity": "critical",
                "category": "connector_failure",
                "message": f"{len(connector_failures)} owner digest connector deliveries failed.",
            }
        )
    if stale_metadata:
        alerts.append(
            {
                "severity": "warning",
                "category": "stale_metadata",
                "message": f"{len(stale_metadata)} recurrence metadata categories are missing or stale.",
            }
        )
    if disabled_schedule_count:
        alerts.append(
            {
                "severity": "warning",
                "category": "disabled_schedule",
                "message": f"{disabled_schedule_count} recurrence automation runs reported disabled schedules.",
            }
        )
    alert_level = "critical" if any(alert["severity"] == "critical" for alert in alerts) else "warning" if alerts else "healthy"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_health.v1",
        "product": "CAVRA",
        "generated_at": now.isoformat(),
        "alert_level": alert_level,
        "expected_interval_minutes": expected_interval_minutes,
        "missed_after_minutes": missed_after_minutes,
        "stale_metadata_minutes": stale_metadata_minutes,
        "run_count": len(runs),
        "missed_run_count": missed_run_count,
        "failed_job_count": failed_job_count,
        "disabled_schedule_count": disabled_schedule_count,
        "stale_metadata_count": len(stale_metadata),
        "connector_delivery_failure_count": len(connector_failures),
        "latest_run_id": latest_run.get("run_id") or latest_run.get("session_id"),
        "latest_run_at": latest_run_at.isoformat() if latest_run_at else None,
        "latest_run_age_minutes": latest_run_age_minutes,
        "stale_metadata": stale_metadata,
        "failed_deliveries": connector_failures[:10],
        "alerts": alerts,
        "recommendations": [
            "Verify the scheduler is enabled and running at the expected interval.",
            "Review the latest dry-run payload before enabling guarded execute mode.",
            "Check connector delivery evidence when owner digest delivery failures are reported.",
            "Refresh recurrence plans, retry plans, owner digests, and suppression trends when metadata is stale.",
        ],
        "latest": runs[:10],
    }


def build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_event(
    health: dict[str, Any],
    *,
    generated_by: str = "release-manager",
    max_alerts: int = 20,
) -> dict[str, Any]:
    """Build a public-safe connector event from recurrence automation health."""
    max_alerts = max(1, min(int(max_alerts), 100))
    alert_level = str(health.get("alert_level") or "healthy")
    health_id = _endpoint_remediation_sla_recurrence_automation_health_id(health)
    alerts = [item for item in health.get("alerts", []) if isinstance(item, dict)]
    selected_alerts = alerts[:max_alerts]
    title = f"CAVRA recurrence automation health {alert_level}: {health_id}"
    message = (
        f"{int(health.get('missed_run_count') or 0)} missed runs, "
        f"{int(health.get('failed_job_count') or 0)} failed jobs, "
        f"{int(health.get('stale_metadata_count') or 0)} stale metadata categories, and "
        f"{int(health.get('connector_delivery_failure_count') or 0)} connector delivery failures."
    )
    description = _endpoint_remediation_sla_recurrence_automation_health_alert_description(
        health_id,
        health,
        selected_alerts,
        omitted_alert_count=max(0, len(alerts) - len(selected_alerts)),
    )
    event = {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_health_alert.v1",
        "product": "CAVRA",
        "event_type": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_health_alert",
        "session_id": health_id,
        "health_id": health_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": generated_by,
        "source_health_generated_at": health.get("generated_at"),
        "alert_level": alert_level,
        "max_severity": "critical" if alert_level == "critical" else "warning" if alert_level == "warning" else "low",
        "blocked_count": int(health.get("missed_run_count") or 0)
        + int(health.get("failed_job_count") or 0)
        + int(health.get("connector_delivery_failure_count") or 0),
        "approval_required_count": len(selected_alerts),
        "decision_count": int(health.get("run_count") or 0),
        "summary": {
            "run_count": int(health.get("run_count") or 0),
            "missed_run_count": int(health.get("missed_run_count") or 0),
            "failed_job_count": int(health.get("failed_job_count") or 0),
            "disabled_schedule_count": int(health.get("disabled_schedule_count") or 0),
            "stale_metadata_count": int(health.get("stale_metadata_count") or 0),
            "connector_delivery_failure_count": int(health.get("connector_delivery_failure_count") or 0),
            "latest_run_id": health.get("latest_run_id"),
            "latest_run_age_minutes": health.get("latest_run_age_minutes"),
            "omitted_alert_count": max(0, len(alerts) - len(selected_alerts)),
        },
        "alerts": selected_alerts,
        "omitted_alert_count": max(0, len(alerts) - len(selected_alerts)),
        "recommendations": health.get("recommendations", []),
        "controls": [
            "health-alert-derived-from-public-recurrence-automation-health",
            "connector-delivery-evidence-redacts-secrets",
            "acknowledgements-record-review-only",
            "private-connectors-remain-responsible-for-ticket-or-chat-side-effects",
        ],
    }
    event["provider_payloads"] = {
        "webhook": event | {"provider": "webhook"},
        "slack": _endpoint_remediation_sla_recurrence_automation_health_slack_payload(title, message, selected_alerts),
        "teams": _endpoint_remediation_sla_recurrence_automation_health_teams_payload(
            title,
            message,
            alert_level,
            selected_alerts,
        ),
        "jira": _endpoint_remediation_sla_jira_payload(title, description, alert_level),
        "servicenow": _endpoint_remediation_sla_servicenow_payload(title, description, health_id, alert_level),
    }
    return event


def build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_plan(
    health: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
    delivery_items: list[dict[str, Any]] | None = None,
    requested_provider: str = "all",
    available_providers: list[str] | None = None,
    generated_by: str = "release-manager",
    suppression_window_minutes: int | None = None,
    force: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Plan recurrence automation health alert delivery and duplicate suppression."""
    now = now or datetime.now(timezone.utc)
    policy = policy or {}
    health_id = _endpoint_remediation_sla_recurrence_automation_health_id(health)
    alert_level = str(health.get("alert_level") or "healthy")
    available = _normalize_endpoint_remediation_sla_notification_providers(available_providers or [])
    matched_rules = _endpoint_remediation_sla_recurrence_automation_health_matching_rules(health, policy)
    eligible = _endpoint_remediation_sla_recurrence_automation_health_policy_providers(
        health,
        policy,
        matched_rules,
        requested_provider=requested_provider,
        available_providers=available,
    )
    if not eligible:
        eligible = available or ["webhook"]
    window = _endpoint_remediation_sla_suppression_window(
        policy,
        matched_rules,
        override=suppression_window_minutes,
    )
    delivery_items = delivery_items or []
    suppressed = [] if force else _endpoint_remediation_sla_recurrence_automation_health_suppressed_providers(
        health_id,
        eligible,
        delivery_items,
        now=now,
        suppression_window_minutes=window,
    )
    suppressed_names = {str(item["provider"]) for item in suppressed}
    selected = [provider for provider in eligible if provider not in suppressed_names and alert_level != "healthy"]
    route_by_provider = _endpoint_remediation_sla_route_map(matched_rules)
    routes = []
    for provider in eligible:
        route = route_by_provider.get(provider, {})
        routes.append(
            {
                "provider": provider,
                "selected": provider in selected,
                "suppressed": provider in suppressed_names,
                "rule_ids": route.get("rule_ids", []),
                "owner": route.get("owner") or policy.get("owner") or "release-governance",
                "acknowledgement_required": bool(
                    route.get("acknowledgement_required", alert_level in {"critical", "warning"})
                ),
                "suppression_window_minutes": window,
            }
        )
    generated_at = now.isoformat()
    material = json.dumps(
        {
            "health_id": health_id,
            "generated_at": generated_at,
            "eligible": eligible,
            "selected": selected,
            "suppressed": suppressed,
        },
        sort_keys=True,
    )
    plan_id = f"erslahalert-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_health_alert_plan.v1",
        "product": "CAVRA",
        "plan_id": plan_id,
        "health_id": health_id,
        "generated_at": generated_at,
        "generated_by": generated_by,
        "source_health_generated_at": health.get("generated_at"),
        "alert_level": alert_level,
        "summary": {
            "run_count": int(health.get("run_count") or 0),
            "missed_run_count": int(health.get("missed_run_count") or 0),
            "failed_job_count": int(health.get("failed_job_count") or 0),
            "stale_metadata_count": int(health.get("stale_metadata_count") or 0),
            "connector_delivery_failure_count": int(health.get("connector_delivery_failure_count") or 0),
            "alert_count": len([item for item in health.get("alerts", []) if isinstance(item, dict)]),
        },
        "requested_provider": requested_provider,
        "eligible_providers": eligible,
        "selected_providers": selected,
        "suppressed_providers": suppressed,
        "suppression_window_minutes": window,
        "force": force,
        "routes": routes,
        "matched_rule_ids": [str(rule.get("rule_id") or rule.get("name")) for rule in matched_rules],
        "acknowledgement_required_providers": [
            route["provider"] for route in routes if route["selected"] and route["acknowledgement_required"]
        ],
        "controls": [
            "health-alert-routing-derived-from-public-health-metadata",
            "duplicate-suppression-uses-redacted-delivery-metadata",
            "acknowledgements-record-human-or-automation-review",
            "no-connector-credentials-stored-in-health-alert-plan",
        ],
    }


def build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_plan_metadata(
    plan: dict[str, Any],
) -> dict[str, Any]:
    return {
        "session_id": plan.get("plan_id"),
        "created_at": plan.get("generated_at"),
        "signer": plan.get("generated_by", "release-manager"),
        "decision_count": len(plan.get("eligible_providers", [])),
        "blocked_count": len(plan.get("suppressed_providers", [])),
        "approval_required_count": len(plan.get("acknowledgement_required_providers", [])),
        "metadata_kind": "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan",
        "plan_id": plan.get("plan_id"),
        "health_id": plan.get("health_id"),
        "alert_level": plan.get("alert_level"),
        "selected_providers": plan.get("selected_providers", []),
        "suppressed_providers": [item.get("provider") for item in plan.get("suppressed_providers", [])],
        "suppressed_provider_count": len(plan.get("suppressed_providers", [])),
        "acknowledgement_required_providers": plan.get("acknowledgement_required_providers", []),
        "suppression_window_minutes": plan.get("suppression_window_minutes"),
        "health_alert_plan": plan,
    }


def acknowledge_endpoint_remediation_sla_escalation_recurrence_automation_health_alert(
    health_id: str,
    *,
    provider: str,
    acknowledged_by: str,
    acknowledgement_state: str = "acknowledged",
    external_ref: str | None = None,
    notes: str | None = None,
    plan_id: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    state = acknowledgement_state.strip().lower().replace("-", "_")
    allowed = {"acknowledged", "dismissed", "escalated", "resolved"}
    if state not in allowed:
        raise ValueError("acknowledgement_state must be one of: acknowledged, dismissed, escalated, resolved")
    normalized_provider = _normalize_endpoint_remediation_sla_notification_providers([provider])
    if not normalized_provider:
        raise ValueError("provider must be one of: webhook, slack, teams, jira, servicenow")
    provider = normalized_provider[0]
    now = now or datetime.now(timezone.utc)
    acknowledged_at = now.isoformat()
    material = f"{health_id}|{provider}|{state}|{acknowledged_by}|{acknowledged_at}"
    ack_id = f"erslahack-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_health_alert_ack.v1",
        "product": "CAVRA",
        "acknowledgement_id": ack_id,
        "health_id": health_id,
        "plan_id": plan_id,
        "provider": provider,
        "acknowledgement_state": state,
        "acknowledged_by": acknowledged_by,
        "acknowledged_at": acknowledged_at,
        "external_ref": external_ref,
        "notes": notes,
        "controls": [
            "health-alert-acknowledgement-records-review-only",
            "no-provider-token-or-secret-stored",
            "recurrence-automation-recovery-remains-operator-or-private-connector-responsibility",
        ],
    }


def build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_ack_metadata(
    acknowledgement: dict[str, Any],
) -> dict[str, Any]:
    return {
        "session_id": acknowledgement.get("acknowledgement_id"),
        "created_at": acknowledgement.get("acknowledged_at"),
        "signer": acknowledgement.get("acknowledged_by", "release-manager"),
        "decision_count": 1,
        "blocked_count": 0,
        "approval_required_count": 0,
        "metadata_kind": "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack",
        "acknowledgement_id": acknowledgement.get("acknowledgement_id"),
        "health_id": acknowledgement.get("health_id"),
        "plan_id": acknowledgement.get("plan_id"),
        "provider": acknowledgement.get("provider"),
        "acknowledgement_state": acknowledgement.get("acknowledgement_state"),
        "external_ref": acknowledgement.get("external_ref"),
        "acknowledgement": acknowledgement,
    }


def filter_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_history(
    items: list[dict[str, Any]],
    *,
    health_id: str | None = None,
    provider: str | None = None,
    metadata_kind: str | None = None,
    acknowledgement_state: str | None = None,
    suppressed: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    allowed_kinds = {
        "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan",
        "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack",
        "release-connector-delivery",
    }
    filtered = [
        item
        for item in items
        if item.get("metadata_kind") in allowed_kinds
        and (
            item.get("metadata_kind") != "release-connector-delivery"
            or item.get("connector_delivery_source")
            == "endpoint_remediation_sla_escalation_recurrence_automation_health_alert"
        )
    ]
    if metadata_kind:
        filtered = [item for item in filtered if item.get("metadata_kind") == metadata_kind]
    if health_id:
        filtered = [
            item
            for item in filtered
            if item.get("health_id") == health_id or item.get("event_id") == health_id or item.get("session_id") == health_id
        ]
    if provider:
        provider_key = provider.strip().lower().replace("-", "_")
        filtered = [
            item
            for item in filtered
            if item.get("provider") == provider_key
            or provider_key in {str(value) for value in item.get("providers", [])}
            or provider_key in {str(value) for value in item.get("selected_providers", [])}
            or provider_key in {str(value) for value in item.get("suppressed_providers", [])}
        ]
    if acknowledgement_state:
        state = acknowledgement_state.strip().lower().replace("-", "_")
        filtered = [item for item in filtered if item.get("acknowledgement_state") == state]
    if suppressed is not None:
        filtered = [
            item
            for item in filtered
            if (len(item.get("suppressed_providers", [])) > 0) is suppressed
        ]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_health_alert_history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_dashboard(
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    history = filter_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_history(items, limit=500)[
        "items"
    ]
    plans = [
        item
        for item in history
        if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan"
    ]
    deliveries = [item for item in history if item.get("metadata_kind") == "release-connector-delivery"]
    acknowledgements = [
        item
        for item in history
        if item.get("metadata_kind") == "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack"
    ]
    latest_plan_by_health: dict[str, dict[str, Any]] = {}
    for plan in plans:
        health_id = str(plan.get("health_id") or "")
        if not health_id:
            continue
        current = latest_plan_by_health.get(health_id)
        if current is None or str(plan.get("created_at", "")) > str(current.get("created_at", "")):
            latest_plan_by_health[health_id] = plan
    acknowledged = {
        (str(item.get("health_id")), str(item.get("provider")))
        for item in acknowledgements
        if item.get("acknowledgement_state") in {"acknowledged", "resolved"}
    }
    outstanding = []
    for plan in latest_plan_by_health.values():
        for provider in plan.get("acknowledgement_required_providers", []):
            key = (str(plan.get("health_id")), str(provider))
            if key not in acknowledged:
                outstanding.append({"health_id": key[0], "provider": key[1], "plan_id": plan.get("plan_id")})
    failed_deliveries = [item for item in deliveries if not item.get("delivery_success")]
    suppressed_count = sum(len(item.get("suppressed_providers", [])) for item in plans)
    alert_level = "critical" if failed_deliveries or outstanding else "warning" if suppressed_count else "healthy"
    return {
        "schema_version": "cavra.endpoint_remediation_sla.escalation_recurrence_automation_health_alert_dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "plan_count": len(plans),
        "delivery_count": len(deliveries),
        "failed_delivery_count": len(failed_deliveries),
        "acknowledgement_count": len(acknowledgements),
        "outstanding_acknowledgement_count": len(outstanding),
        "suppressed_provider_count": suppressed_count,
        "outstanding_acknowledgements": outstanding[:20],
        "latest": history[:10],
    }


def export_endpoint_remediation_sla_escalation_suppression_audit(
    recurrence_plan: dict[str, Any],
    output_dir: Path,
    *,
    generated_by: str = "release-manager",
) -> ReleaseAuditExportResult:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    audit = build_endpoint_remediation_sla_escalation_suppression_audit(
        recurrence_plan,
        generated_by=generated_by,
    )
    files = [
        _write_release_json(output_dir / "endpoint-remediation-sla-escalation-suppression-audit.json", audit),
    ]
    summary_path = output_dir / "endpoint-remediation-sla-escalation-suppression-audit.md"
    summary_path.write_text(_endpoint_remediation_sla_suppression_audit_markdown(audit), encoding="utf-8")
    files.append(summary_path)
    checksums_path = output_dir / "checksums.txt"
    checksums_path.write_text(
        "\n".join(f"{sha256_file(path)}  {path.name}" for path in files) + "\n",
        encoding="utf-8",
    )
    files.append(checksums_path)
    return ReleaseAuditExportResult(output_dir=output_dir, files=files)


def filter_endpoint_remediation_sla_report_history(
    items: list[dict[str, Any]],
    *,
    alert_level: str | None = None,
    min_breached: int | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [item for item in items if item.get("metadata_kind") == "endpoint-remediation-sla-report"]
    if alert_level:
        filtered = [item for item in filtered if item.get("alert_level") == alert_level]
    if min_breached is not None:
        filtered = [item for item in filtered if int(item.get("breached_count") or 0) >= min_breached]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_remediation_sla_report.history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_remediation_sla_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_remediation_sla_report_history(items, limit=500)["items"]
    latest = history[0] if history else {}
    critical_reports = [item for item in history if item.get("alert_level") == "critical"]
    warning_reports = [item for item in history if item.get("alert_level") == "warning"]
    return {
        "schema_version": "cavra.endpoint_remediation_sla_report.dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": latest.get("alert_level", "healthy"),
        "report_count": len(history),
        "critical_report_count": len(critical_reports),
        "warning_report_count": len(warning_reports),
        "latest_report_id": latest.get("report_id"),
        "tracked_work_item_count": latest.get("tracked_work_item_count", 0),
        "completed_count": latest.get("completed_count", 0),
        "at_risk_count": latest.get("at_risk_count", 0),
        "breached_count": latest.get("breached_count", 0),
        "completion_rate": latest.get("completion_rate", 0),
        "escalation_count": latest.get("escalation_count", 0),
        "latest": history[:10],
    }


def build_endpoint_remediation_handoff_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_remediation_handoff_history(items, limit=500)["items"]
    providers: dict[str, int] = {}
    for item in history:
        for provider in item.get("providers", []):
            provider_key = str(provider)
            providers[provider_key] = providers.get(provider_key, 0) + 1
    pending = [item for item in history if item.get("approval_state") == "pending"]
    alert_level = "warning" if pending else "healthy"
    return {
        "schema_version": "cavra.endpoint_remediation_handoff.dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "handoff_count": len(history),
        "pending_approval_count": len(pending),
        "provider_count": len(providers),
        "action_count": sum(int(item.get("action_count") or 0) for item in history),
        "providers": providers,
        "latest": history[:10],
    }


def build_endpoint_reconciliation_automation_metadata(
    automation: dict[str, Any],
    *,
    bundle_dir: Path | None = None,
) -> dict[str, Any]:
    summary = automation.get("summary", {}) if isinstance(automation.get("summary"), dict) else {}
    metadata = {
        "session_id": automation.get("automation_id"),
        "created_at": automation.get("created_at"),
        "signer": automation.get("requested_by", "release-agent"),
        "decision_count": 1 if automation.get("approval_id") else 0,
        "blocked_count": int(summary.get("drifted_endpoint_count") or 0) + int(summary.get("missing_target_count") or 0),
        "approval_required_count": 1 if automation.get("approval_state") == "pending" else 0,
        "metadata_kind": "endpoint-reconciliation-automation",
        "automation_id": automation.get("automation_id"),
        "reconciliation_id": automation.get("reconciliation_id"),
        "request_id": automation.get("remediation_request_id"),
        "approval_id": automation.get("approval_id"),
        "approval_state": automation.get("approval_state"),
        "drift_status": automation.get("drift_status"),
        "alert_level": automation.get("alert_level"),
        "release": automation.get("release", {}),
        "channel": automation.get("channel"),
        "inventory_id": automation.get("inventory_id"),
        "provider": automation.get("provider"),
        "observed_at": automation.get("observed_at"),
        "summary": summary,
        "automation": automation,
        "evidence_refs": automation.get("evidence_refs", []),
    }
    if bundle_dir:
        metadata["bundle_dir"] = str(bundle_dir)
    return metadata


def filter_endpoint_reconciliation_automation_history(
    items: list[dict[str, Any]],
    *,
    drift_status: str | None = None,
    alert_level: str | None = None,
    approval_state: str | None = None,
    provider: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = [item for item in items if item.get("metadata_kind") == "endpoint-reconciliation-automation"]
    if drift_status:
        filtered = [item for item in filtered if item.get("drift_status") == drift_status]
    if alert_level:
        filtered = [item for item in filtered if item.get("alert_level") == alert_level]
    if approval_state:
        filtered = [item for item in filtered if item.get("approval_state") == approval_state]
    if provider:
        filtered = [item for item in filtered if item.get("provider") == provider]
    filtered = sorted(filtered, key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {
        "schema_version": "cavra.endpoint_reconciliation_automation.history.v1",
        "product": "CAVRA",
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def build_endpoint_reconciliation_automation_dashboard(items: list[dict[str, Any]]) -> dict[str, Any]:
    history = filter_endpoint_reconciliation_automation_history(items, limit=500)["items"]
    pending = [item for item in history if item.get("approval_state") == "pending"]
    critical = [item for item in history if item.get("alert_level") == "critical"]
    warning = [item for item in history if item.get("alert_level") == "warning"]
    alert_level = "critical" if critical or pending else "warning" if warning else "healthy"
    return {
        "schema_version": "cavra.endpoint_reconciliation_automation.dashboard.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alert_level": alert_level,
        "automation_count": len(history),
        "pending_approval_count": len(pending),
        "drift_detected_count": sum(1 for item in history if item.get("drift_status") == "drift_detected"),
        "request_count": sum(1 for item in history if item.get("request_id")),
        "latest": history[:10],
    }


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


def verify_go_ci_runner_bundles(
    runner_bundles_path: Path,
    package_dir: Path,
    expected_checksums: dict[str, str],
    evidence: dict[str, Any],
) -> list[str]:
    try:
        payload = json.loads(runner_bundles_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid CI runner bundle JSON: {exc}") from exc
    if payload.get("schema_version") != "cavra.go-runtime.ci-runner-bundles.v1":
        raise ReleaseVerificationError("CI runner bundle metadata has an invalid schema_version")
    if evidence and payload.get("version") != evidence.get("version"):
        raise ReleaseVerificationError("CI runner bundle metadata version does not match release evidence")
    if payload.get("source_metadata") != "cavra-runtime.endpoint-deployment.json":
        raise ReleaseVerificationError("CI runner bundle metadata must reference cavra-runtime.endpoint-deployment.json")

    endpoint_deployment_path = package_dir / "cavra-runtime.endpoint-deployment.json"
    try:
        endpoint_deployment = json.loads(endpoint_deployment_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ReleaseVerificationError("CI runner bundle metadata cannot load endpoint deployment metadata") from exc
    except json.JSONDecodeError as exc:
        raise ReleaseVerificationError(f"invalid endpoint deployment JSON for CI runner bundles: {exc}") from exc
    deployment_targets = {
        str(target.get("id")): target
        for target in endpoint_deployment.get("deployment_targets", [])
        if isinstance(target, dict) and target.get("id")
    }

    runner_script = payload.get("runner_script")
    if not isinstance(runner_script, dict):
        raise ReleaseVerificationError("CI runner bundle metadata is missing runner_script")
    _verify_runner_file(package_dir, expected_checksums, runner_script, "runner_script")
    if "CAVRA_RELEASE_GOVERNANCE_REQUEST" not in runner_script.get("required_environment", []):
        raise ReleaseVerificationError("CI runner script metadata must require CAVRA_RELEASE_GOVERNANCE_REQUEST")

    github_action = payload.get("github_action")
    if not isinstance(github_action, dict):
        raise ReleaseVerificationError("CI runner bundle metadata is missing github_action")
    _verify_runner_file(package_dir, expected_checksums, github_action, "github_action")

    controls = payload.get("controls")
    if not isinstance(controls, list) or "verified-signed-runtime-before-runner-use" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing signed runtime verification control")
    if "runner-authentication-claims-signed" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing runner authentication control")
    if "runner-authentication-oidc-verified" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing runner OIDC verification control")
    if "runner-oidc-provider-token-acquisition" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing provider OIDC token acquisition control")
    if "daemon-evidence-stream-hmac-signed" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing signed evidence stream control")
    if "daemon-evidence-stream-verifier-cli" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing daemon evidence verifier control")
    if "evidence-verification-artifact-published" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing evidence verification artifact control")
    if "runner-evidence-key-custody-documented" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing key custody documentation control")
    if "blocking-decision-fails-closed-by-default" not in controls:
        raise ReleaseVerificationError("CI runner bundle metadata is missing fail-closed decision control")

    bundles = payload.get("runner_bundles")
    if not isinstance(bundles, list) or not bundles:
        raise ReleaseVerificationError("CI runner bundle metadata has no runner_bundles")
    verified: list[str] = []
    for bundle in bundles:
        if not isinstance(bundle, dict):
            raise ReleaseVerificationError("CI runner bundle entry is invalid")
        platform = str(bundle.get("platform", ""))
        deployment_target = str(bundle.get("deployment_target", ""))
        if not platform or not deployment_target:
            raise ReleaseVerificationError("CI runner bundle entry is missing platform or deployment_target")
        target = deployment_targets.get(deployment_target)
        if not target:
            raise ReleaseVerificationError(f"CI runner bundle references unknown deployment target: {deployment_target}")
        if target.get("surface") != "ci-runner":
            raise ReleaseVerificationError(f"CI runner bundle target is not a CI runner: {deployment_target}")
        binary = str(bundle.get("runtime_binary", ""))
        if binary != target.get("binary"):
            raise ReleaseVerificationError(f"CI runner bundle binary does not match endpoint deployment: {deployment_target}")
        binary_path = _safe_package_path(package_dir, binary)
        if binary_path is None or not binary_path.exists() or not binary_path.is_file():
            raise ReleaseVerificationError(f"CI runner bundle binary is missing: {binary}")
        expected_sha256 = str(bundle.get("runtime_binary_sha256", "")).lower()
        if sha256_file(binary_path) != expected_sha256:
            raise ReleaseVerificationError(f"CI runner bundle digest mismatch for {binary}")
        checksum_sha256 = expected_checksums.get(binary)
        if checksum_sha256 and checksum_sha256 != expected_sha256:
            raise ReleaseVerificationError(f"CI runner bundle disagrees with checksums.txt: {binary}")
        wrapper = str(bundle.get("reusable_wrapper", ""))
        wrapper_path = _safe_package_path(package_dir, wrapper)
        if wrapper_path is None or not wrapper_path.exists() or not wrapper_path.is_file():
            raise ReleaseVerificationError(f"CI runner bundle wrapper is missing: {wrapper}")
        commands = "\n".join(str(command) for command in bundle.get("verification_commands", []))
        if "cavra release verify-go-package" not in commands:
            raise ReleaseVerificationError(f"CI runner bundle is missing package verification guidance: {platform}")
        if "gh attestation verify" not in commands:
            raise ReleaseVerificationError(f"CI runner bundle is missing keyless attestation guidance: {platform}")
        outputs = bundle.get("required_outputs")
        if not isinstance(outputs, list) or not outputs:
            raise ReleaseVerificationError(f"CI runner bundle is missing required outputs: {platform}")
        if not any("release-governance-evidence.jsonl" in str(output) for output in outputs):
            raise ReleaseVerificationError(f"CI runner bundle is missing daemon evidence output: {platform}")
        verified.append(deployment_target)
    return sorted(verified)


def _verify_runner_file(
    package_dir: Path,
    expected_checksums: dict[str, str],
    item: dict[str, Any],
    label: str,
) -> None:
    relative_path = str(item.get("path", ""))
    path = _safe_package_path(package_dir, relative_path)
    if path is None or not path.exists() or not path.is_file():
        raise ReleaseVerificationError(f"CI runner {label} is missing: {relative_path}")
    expected_sha256 = str(item.get("sha256", "")).lower()
    if sha256_file(path) != expected_sha256:
        raise ReleaseVerificationError(f"CI runner {label} digest mismatch: {relative_path}")
    checksum_sha256 = expected_checksums.get(relative_path)
    if checksum_sha256 and checksum_sha256 != expected_sha256:
        raise ReleaseVerificationError(f"CI runner {label} disagrees with checksums.txt: {relative_path}")


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


def _endpoint_remediation_handoff_id(request_id: str, providers: list[str], request_sha256: str) -> str:
    material = json.dumps(
        {"request_id": request_id, "providers": sorted(providers), "request_sha256": request_sha256},
        sort_keys=True,
    )
    return f"erh_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_remediation_handoff_status_id(
    handoff_id: str,
    provider: str,
    status: str,
    external_ref: str | None,
    recorded_at: str,
) -> str:
    material = json.dumps(
        {
            "handoff_id": handoff_id,
            "provider": provider,
            "status": status,
            "external_ref": external_ref,
            "recorded_at": recorded_at,
        },
        sort_keys=True,
    )
    return f"erhs_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_remediation_sla_report_id(
    generated_at: str,
    warning_hours: int,
    critical_hours: int,
    work_items: list[dict[str, Any]],
) -> str:
    material = json.dumps(
        {
            "generated_at": generated_at,
            "warning_hours": warning_hours,
            "critical_hours": critical_hours,
            "work_items": [
                {
                    "handoff_id": item.get("handoff_id"),
                    "provider": item.get("provider"),
                    "status": item.get("status"),
                    "severity": item.get("severity"),
                }
                for item in work_items
            ],
        },
        sort_keys=True,
        default=str,
    )
    return f"ersla_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_inventory_freshness_report_id(
    items: list[dict[str, Any]],
    *,
    provider: str | None,
    channel: str | None,
    deployment_target: str | None,
    max_age_hours: int,
    critical_age_hours: int,
    created_at: str,
) -> str:
    material = json.dumps(
        {
            "scope": {
                "provider": provider,
                "channel": channel,
                "deployment_target": deployment_target,
            },
            "max_age_hours": max_age_hours,
            "critical_age_hours": critical_age_hours,
            "created_at": created_at,
            "inventory_ids": sorted(str(item.get("inventory_id") or item.get("session_id")) for item in items),
        },
        sort_keys=True,
        default=str,
    )
    return f"eif_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_reconciliation_automation_id(
    desired_manifest: dict[str, Any],
    ingestion_record: dict[str, Any],
    reconciliation_report: dict[str, Any],
    remediation_request: dict[str, Any] | None,
) -> str:
    material = json.dumps(
        {
            "version": desired_manifest.get("version"),
            "commit": desired_manifest.get("commit"),
            "inventory_id": ingestion_record.get("inventory_id") or ingestion_record.get("session_id"),
            "reconciliation_id": reconciliation_report.get("reconciliation_id"),
            "request_id": remediation_request.get("request_id") if remediation_request else None,
        },
        sort_keys=True,
        default=str,
    )
    return f"era_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:12]}"


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


def _endpoint_inventory_source_items(provider: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    provider_keys = {
        "jamf": ("computers", "devices", "endpoints", "items", "results"),
        "intune": ("devices", "managedDevices", "value", "endpoints", "items"),
        "linux": ("endpoints", "hosts", "nodes", "items", "devices"),
        "edr": ("assets", "devices", "endpoints", "hosts", "items", "resources"),
    }
    for key in provider_keys.get(provider, ()):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    if payload.get("schema_version") == "cavra.endpoint-observations.v1":
        endpoints = payload.get("endpoints", [])
        return [item for item in endpoints if isinstance(item, dict)]
    return []


def _normalize_endpoint_inventory_item(provider: str, item: dict[str, Any], *, index: int) -> dict[str, Any]:
    runtime = item.get("cavra") if isinstance(item.get("cavra"), dict) else {}
    if not runtime and isinstance(item.get("runtime"), dict):
        runtime = item["runtime"]
    endpoint_id = _first_endpoint_value(
        item,
        runtime,
        "endpoint_id",
        "device_id",
        "deviceId",
        "id",
        "udid",
        "serial_number",
        "serialNumber",
        "computer_id",
        "hostname",
        "name",
        "deviceName",
        default=f"{provider}-endpoint-{index}",
    )
    deployment_target = _first_endpoint_value(
        item,
        runtime,
        "deployment_target",
        "target_id",
        "target",
        "assignment",
        "policy_name",
        "policyName",
        "smart_group",
        "group",
        "collection",
        "deploymentGroup",
        default="unknown-target",
    )
    installed_version = _first_endpoint_value(
        item,
        runtime,
        "installed_version",
        "runtime_version",
        "cavra_version",
        "version",
        "app_version",
        "applicationVersion",
        "detectedVersion",
    )
    binary_sha256 = _first_endpoint_value(
        item,
        runtime,
        "binary_sha256",
        "installed_binary_sha256",
        "runtime_sha256",
        "cavra_sha256",
        "sha256",
        "checksum",
        "fileHash",
    )
    last_seen_at = _first_endpoint_value(
        item,
        runtime,
        "last_seen_at",
        "lastSeen",
        "last_contact_time",
        "lastContactTime",
        "lastCheckInDateTime",
        "report_date",
        "updated_at",
        "check_in_time",
    )
    normalized = {
        "endpoint_id": str(endpoint_id),
        "deployment_target": str(deployment_target),
        "installed_version": installed_version,
        "binary_sha256": binary_sha256,
        "last_seen_at": last_seen_at,
        "provider": provider,
        "hostname": _first_endpoint_value(item, runtime, "hostname", "computerName", "deviceName", "name"),
        "serial_number": _first_endpoint_value(item, runtime, "serial_number", "serialNumber", "serial"),
        "os": _first_endpoint_value(item, runtime, "os", "operatingSystem", "platform"),
        "management_state": _first_endpoint_value(item, runtime, "management_state", "managed", "complianceState", "status"),
    }
    return {key: value for key, value in normalized.items() if value is not None}


def _first_endpoint_value(
    item: dict[str, Any],
    runtime: dict[str, Any],
    *keys: str,
    default: Any = None,
) -> Any:
    for key in keys:
        for source in (item, runtime):
            value = source.get(key)
            if value not in (None, ""):
                return value
    return default


def _endpoint_inventory_ingestion_id(provider: str, inventory: dict[str, Any]) -> str:
    material = json.dumps(
        {
            "provider": provider,
            "channel": inventory.get("channel"),
            "observed_at": inventory.get("observed_at"),
            "endpoints": inventory.get("endpoints", []),
        },
        sort_keys=True,
        default=str,
    )
    return f"eii_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:12]}"


def _endpoint_inventory_ingestion_markdown_summary(ingestion: dict[str, Any]) -> str:
    lines = [
        "# Endpoint Inventory Ingestion",
        "",
        f"- Inventory ID: `{ingestion.get('inventory_id')}`",
        f"- Provider: `{ingestion.get('provider')}`",
        f"- Channel: `{ingestion.get('channel') or 'n/a'}`",
        f"- Observed at: `{ingestion.get('observed_at')}`",
        f"- Endpoints: {ingestion.get('endpoint_count', 0)}",
        f"- Missing targets: {ingestion.get('missing_target_count', 0)}",
        "",
        "## Deployment Targets",
    ]
    targets = ingestion.get("deployment_targets", [])
    if not targets:
        lines.append("- No deployment targets reported.")
    for target in targets:
        lines.append(f"- `{target}`")
    warnings = ingestion.get("warnings", [])
    if warnings:
        lines.extend(["", "## Warnings"])
        lines.extend(f"- {warning}" for warning in warnings)
    return "\n".join(lines) + "\n"


def _endpoint_inventory_freshness_markdown_summary(report: dict[str, Any]) -> str:
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    lines = [
        "# Endpoint Inventory Freshness",
        "",
        f"- Report ID: `{report.get('report_id')}`",
        f"- Alert level: `{report.get('alert_level')}`",
        f"- Warning SLA hours: {report.get('max_age_hours')}",
        f"- Critical SLA hours: {report.get('critical_age_hours')}",
        f"- Ingestion records: {summary.get('ingestion_count', 0)}",
        f"- Warning alerts: {summary.get('warning_count', 0)}",
        f"- Critical alerts: {summary.get('critical_count', 0)}",
        "",
        "## Alerts",
    ]
    alerts = [item for item in report.get("alerts", []) if isinstance(item, dict)]
    if not alerts:
        lines.append("- No endpoint inventory freshness alerts.")
    for alert in alerts:
        lines.append(
            f"- `{alert.get('severity')}` `{alert.get('provider')}` `{alert.get('channel')}` "
            f"`{alert.get('deployment_target')}` - {alert.get('message')}"
        )
    return "\n".join(lines) + "\n"


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
    observed = _parse_release_datetime(last_seen_at)
    if observed is None:
        return True
    return (now - observed).total_seconds() > stale_after_hours * 3600


def _parse_release_datetime(raw: object) -> datetime | None:
    if raw in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _floor_release_datetime(value: datetime, interval_minutes: int) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    value = value.astimezone(timezone.utc)
    interval_seconds = max(1, interval_minutes) * 60
    floored = int(value.timestamp()) // interval_seconds * interval_seconds
    return datetime.fromtimestamp(floored, timezone.utc)


def _inventory_from_ingestion_record(record: dict[str, Any]) -> dict[str, Any] | None:
    if record.get("schema_version") == "cavra.endpoint-observations.v1":
        return record
    if record.get("schema_version") == "cavra.endpoint-inventory-ingestion.v1":
        inventory = record.get("inventory")
        return inventory if isinstance(inventory, dict) else None
    if record.get("metadata_kind") == "endpoint-inventory-ingestion":
        inventory = record.get("inventory")
        if isinstance(inventory, dict):
            return inventory
        ingestion = record.get("ingestion")
        if isinstance(ingestion, dict) and isinstance(ingestion.get("inventory"), dict):
            return ingestion["inventory"]
    return None


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


def _endpoint_reconciliation_automation_markdown_summary(automation: dict[str, Any]) -> str:
    summary = automation.get("summary", {}) if isinstance(automation.get("summary"), dict) else {}
    lines = [
        "# Endpoint Reconciliation Automation",
        "",
        f"- Automation ID: `{automation.get('automation_id')}`",
        f"- Reconciliation ID: `{automation.get('reconciliation_id')}`",
        f"- Drift status: `{automation.get('drift_status')}`",
        f"- Alert level: `{automation.get('alert_level')}`",
        f"- Remediation request: `{automation.get('remediation_request_id') or 'not required'}`",
        f"- Approval: `{automation.get('approval_id') or 'not required'}`",
        f"- Drifted endpoints: {summary.get('drifted_endpoint_count', 0)}",
        f"- Missing targets: {summary.get('missing_target_count', 0)}",
        "",
        "## Controls",
    ]
    for control in automation.get("controls", []):
        lines.append(f"- `{control}`")
    return "\n".join(lines) + "\n"


def _endpoint_remediation_handoff_markdown_summary(handoff: dict[str, Any]) -> str:
    lines = [
        "# Endpoint Remediation Handoff",
        "",
        f"- Handoff ID: `{handoff.get('handoff_id')}`",
        f"- Request ID: `{handoff.get('request_id')}`",
        f"- Reconciliation ID: `{handoff.get('reconciliation_id')}`",
        f"- Approval: `{handoff.get('approval_id') or 'n/a'}` `{handoff.get('approval_state') or 'unknown'}`",
        f"- Providers: `{', '.join(handoff.get('providers', []))}`",
        f"- Actions: {handoff.get('action_count', 0)}",
        "",
        "## Controls",
    ]
    for control in handoff.get("controls", []):
        lines.append(f"- `{control}`")
    return "\n".join(lines) + "\n"


def _endpoint_remediation_handoff_status_markdown_summary(status: dict[str, Any]) -> str:
    lines = [
        "# Endpoint Remediation Handoff Status",
        "",
        f"- Status ID: `{status.get('status_id')}`",
        f"- Handoff ID: `{status.get('handoff_id')}`",
        f"- Request ID: `{status.get('request_id')}`",
        f"- Provider: `{status.get('provider')}`",
        f"- Status: `{status.get('status')}`",
        f"- External reference: `{status.get('external_ref') or 'n/a'}`",
        f"- Recorded by: `{status.get('recorded_by')}`",
        "",
        "## Controls",
    ]
    for control in status.get("controls", []):
        lines.append(f"- `{control}`")
    return "\n".join(lines) + "\n"


def _redact_endpoint_handoff_callback_payload(payload: dict[str, Any]) -> dict[str, Any]:
    sensitive_markers = ("authorization", "token", "secret", "password", "api_key", "apikey", "webhook")

    def redact(value: Any, key: str = "") -> Any:
        if any(marker in key.lower() for marker in sensitive_markers):
            return "[redacted]"
        if isinstance(value, dict):
            return {str(child_key): redact(child_value, str(child_key)) for child_key, child_value in value.items()}
        if isinstance(value, list):
            return [redact(item, key) for item in value]
        return value

    return redact(payload)


def _endpoint_remediation_sla_recommended_action(status: str, severity: str) -> str:
    if status == "not_started":
        return "Confirm that the handoff was accepted by the provider or private connector queue."
    if status in {"failed", "blocked"}:
        return "Escalate to endpoint operations and release governance for manual recovery review."
    if severity == "critical":
        return "Escalate overdue remediation to the release owner and change advisory board."
    if severity == "warning":
        return "Notify provider owner before the remediation handoff breaches SLA."
    if status == "completed":
        return "Retain completion evidence with the release governance record."
    return "Continue monitoring provider callback status."


def _endpoint_remediation_sla_escalation(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "severity": item.get("severity"),
        "handoff_id": item.get("handoff_id"),
        "request_id": item.get("request_id"),
        "provider": item.get("provider"),
        "status": item.get("status"),
        "age_hours": item.get("age_hours"),
        "overdue_hours": item.get("overdue_hours"),
        "external_ref": item.get("external_ref"),
        "external_url": item.get("external_url"),
        "recommended_action": item.get("recommended_action"),
    }


def _endpoint_remediation_sla_escalation_payloads(
    report_id: str,
    escalations: list[dict[str, Any]],
) -> dict[str, Any]:
    critical_count = len([item for item in escalations if item.get("severity") == "critical"])
    warning_count = len([item for item in escalations if item.get("severity") == "warning"])
    title = f"CAVRA endpoint remediation SLA report {report_id}"
    text = f"{critical_count} breached and {warning_count} at-risk endpoint remediation handoffs require review."
    return {
        "slack": {
            "text": title,
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*{title}*\n{text}"}},
                {"type": "context", "elements": [{"type": "mrkdwn", "text": "Generated from public CAVRA evidence metadata."}]},
            ],
        },
        "teams": {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title,
            "themeColor": "DC2626" if critical_count else "D97706",
            "title": title,
            "text": text,
        },
        "jira": {
            "issue": {
                "project": {"key": "CAVRA"},
                "issuetype": {"name": "Task"},
                "summary": title,
                "description": text,
                "labels": ["cavra", "endpoint-remediation", "sla"],
            }
        },
        "executive_summary": {
            "report_id": report_id,
            "critical_count": critical_count,
            "warning_count": warning_count,
            "message": text,
        },
    }


def _endpoint_remediation_sla_report_markdown_summary(report: dict[str, Any]) -> str:
    summary = report.get("executive_summary", {}) if isinstance(report.get("executive_summary"), dict) else {}
    lines = [
        "# Endpoint Remediation SLA Report",
        "",
        f"- Report ID: `{report.get('report_id')}`",
        f"- Alert level: `{report.get('alert_level')}`",
        f"- Tracked work items: {summary.get('tracked_work_item_count', 0)}",
        f"- Completed: {summary.get('completed_count', 0)}",
        f"- At risk: {summary.get('at_risk_count', 0)}",
        f"- Breached: {summary.get('breached_count', 0)}",
        "",
        "## Escalations",
    ]
    escalations = report.get("escalations", [])
    if not escalations:
        lines.append("- No SLA escalations.")
    for item in escalations:
        lines.append(
            "- "
            f"`{item.get('severity')}` `{item.get('provider')}` `{item.get('handoff_id')}` "
            f"{item.get('recommended_action')}"
        )
    lines.append("")
    lines.append("## Controls")
    for control in report.get("controls", []):
        lines.append(f"- `{control}`")
    return "\n".join(lines) + "\n"


def _normalize_endpoint_remediation_sla_notification_providers(providers: list[str] | None) -> list[str]:
    allowed = {"webhook", "slack", "teams", "jira", "servicenow"}
    selected: set[str] = set()
    for provider in providers or []:
        for raw in str(provider).split(","):
            value = raw.strip().lower().replace("-", "_")
            if value in allowed:
                selected.add(value)
    return sorted(selected)


def _endpoint_remediation_sla_matching_rules(report: dict[str, Any], policy: dict[str, Any]) -> list[dict[str, Any]]:
    rules = policy.get("rules") or policy.get("notification_routing") or []
    if not isinstance(rules, list):
        return []
    summary = report.get("executive_summary", {}) if isinstance(report.get("executive_summary"), dict) else {}
    alert_level = str(report.get("alert_level") or "healthy")
    release_channels = {str(channel) for channel in summary.get("release_channels", [])}
    breached_count = int(summary.get("breached_count") or 0)
    at_risk_count = int(summary.get("at_risk_count") or 0)
    matched = []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        alert_levels = {str(value) for value in rule.get("alert_levels", [])}
        if alert_levels and alert_level not in alert_levels:
            continue
        channels = {str(value) for value in rule.get("channels", [])}
        if channels and release_channels and not channels.intersection(release_channels):
            continue
        if breached_count < int(rule.get("min_breached", 0) or 0):
            continue
        if at_risk_count < int(rule.get("min_at_risk", 0) or 0):
            continue
        matched.append(rule)
    return matched


def _endpoint_remediation_sla_recurrence_automation_health_matching_rules(
    health: dict[str, Any],
    policy: dict[str, Any],
) -> list[dict[str, Any]]:
    rules = policy.get("rules") or policy.get("health_alert_routing") or policy.get("notification_routing") or []
    if not isinstance(rules, list):
        return []
    alert_level = str(health.get("alert_level") or "healthy")
    categories = {str(item.get("category")) for item in health.get("alerts", []) if isinstance(item, dict)}
    missed = int(health.get("missed_run_count") or 0)
    failed = int(health.get("failed_job_count") or 0)
    stale = int(health.get("stale_metadata_count") or 0)
    connector_failures = int(health.get("connector_delivery_failure_count") or 0)
    matched = []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        alert_levels = {str(value) for value in rule.get("alert_levels", [])}
        if alert_levels and alert_level not in alert_levels:
            continue
        rule_categories = {str(value) for value in rule.get("categories", rule.get("alert_categories", []))}
        if rule_categories and not rule_categories.intersection(categories):
            continue
        if missed < int(rule.get("min_missed_runs", 0) or 0):
            continue
        if failed < int(rule.get("min_failed_jobs", 0) or 0):
            continue
        if stale < int(rule.get("min_stale_metadata", 0) or 0):
            continue
        if connector_failures < int(rule.get("min_connector_failures", 0) or 0):
            continue
        matched.append(rule)
    return matched


def _endpoint_remediation_sla_policy_providers(
    report: dict[str, Any],
    policy: dict[str, Any],
    matched_rules: list[dict[str, Any]],
    *,
    requested_provider: str,
    available_providers: list[str],
) -> list[str]:
    requested = requested_provider.strip().lower().replace("-", "_")
    if requested != "all":
        return _normalize_endpoint_remediation_sla_notification_providers([requested])
    providers: list[str] = []
    for rule in matched_rules:
        providers.extend(_normalize_endpoint_remediation_sla_notification_providers(rule.get("providers", [])))
    if not providers:
        providers.extend(_normalize_endpoint_remediation_sla_notification_providers(policy.get("default_providers", [])))
    if not providers:
        providers.extend(available_providers)
    if not providers:
        alert_level = str(report.get("alert_level") or "healthy")
        providers.extend(["jira", "servicenow", "slack", "teams"] if alert_level == "critical" else ["slack", "teams"])
    return sorted(set(providers))


def _endpoint_remediation_sla_recurrence_automation_health_policy_providers(
    health: dict[str, Any],
    policy: dict[str, Any],
    matched_rules: list[dict[str, Any]],
    *,
    requested_provider: str,
    available_providers: list[str],
) -> list[str]:
    requested = requested_provider.strip().lower().replace("-", "_")
    if requested != "all":
        return _normalize_endpoint_remediation_sla_notification_providers([requested])
    providers: list[str] = []
    for rule in matched_rules:
        providers.extend(_normalize_endpoint_remediation_sla_notification_providers(rule.get("providers", [])))
    if not providers:
        providers.extend(_normalize_endpoint_remediation_sla_notification_providers(policy.get("default_providers", [])))
    if not providers:
        providers.extend(available_providers)
    if not providers:
        alert_level = str(health.get("alert_level") or "healthy")
        providers.extend(["jira", "slack", "teams"] if alert_level == "critical" else ["slack", "teams"])
    return sorted(set(providers))


def _endpoint_remediation_sla_suppression_window(
    policy: dict[str, Any],
    matched_rules: list[dict[str, Any]],
    *,
    override: int | None,
) -> int:
    if override is not None:
        return max(0, int(override))
    windows = [
        int(rule.get("suppression_window_minutes"))
        for rule in matched_rules
        if rule.get("suppression_window_minutes") is not None
    ]
    if windows:
        return max(0, max(windows))
    return max(0, int(policy.get("suppression_window_minutes", 60) or 0))


def _endpoint_remediation_sla_suppressed_providers(
    report_id: str,
    providers: list[str],
    delivery_items: list[dict[str, Any]],
    *,
    now: datetime,
    suppression_window_minutes: int,
) -> list[dict[str, Any]]:
    if suppression_window_minutes <= 0:
        return []
    cutoff = now - timedelta(minutes=suppression_window_minutes)
    suppressed: list[dict[str, Any]] = []
    for provider in providers:
        latest: dict[str, Any] | None = None
        for item in delivery_items:
            if item.get("metadata_kind") != "release-connector-delivery":
                continue
            if item.get("connector_delivery_source") != "endpoint_remediation_sla_notification":
                continue
            if item.get("event_id") != report_id:
                continue
            if provider not in {str(value) for value in item.get("providers", [])}:
                continue
            created_at = _parse_release_datetime(item.get("created_at"))
            if created_at is None or created_at < cutoff:
                continue
            if latest is None or str(item.get("created_at", "")) > str(latest.get("created_at", "")):
                latest = item
        if latest:
            suppressed.append(
                {
                    "provider": provider,
                    "last_delivery_at": latest.get("created_at"),
                    "last_delivery_id": latest.get("session_id"),
                    "reason": f"delivery exists within {suppression_window_minutes} minute suppression window",
                }
            )
    return suppressed


def _endpoint_remediation_sla_recurrence_automation_health_suppressed_providers(
    health_id: str,
    providers: list[str],
    delivery_items: list[dict[str, Any]],
    *,
    now: datetime,
    suppression_window_minutes: int,
) -> list[dict[str, Any]]:
    if suppression_window_minutes <= 0:
        return []
    cutoff = now - timedelta(minutes=suppression_window_minutes)
    suppressed: list[dict[str, Any]] = []
    for provider in providers:
        latest: dict[str, Any] | None = None
        for item in delivery_items:
            if item.get("metadata_kind") != "release-connector-delivery":
                continue
            if (
                item.get("connector_delivery_source")
                != "endpoint_remediation_sla_escalation_recurrence_automation_health_alert"
            ):
                continue
            if item.get("event_id") != health_id:
                continue
            if provider not in {str(value) for value in item.get("providers", [])}:
                continue
            created_at = _parse_release_datetime(item.get("created_at"))
            if created_at is None or created_at < cutoff:
                continue
            if latest is None or str(item.get("created_at", "")) > str(latest.get("created_at", "")):
                latest = item
        if latest:
            suppressed.append(
                {
                    "provider": provider,
                    "last_delivery_at": latest.get("created_at"),
                    "last_delivery_id": latest.get("session_id"),
                    "reason": f"delivery exists within {suppression_window_minutes} minute suppression window",
                }
            )
    return suppressed


def _endpoint_remediation_sla_route_map(matched_rules: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    route_by_provider: dict[str, dict[str, Any]] = {}
    for rule in matched_rules:
        rule_id = str(rule.get("rule_id") or rule.get("name") or "unnamed")
        owner = rule.get("owner")
        ack_required = bool(rule.get("acknowledgement_required", rule.get("ack_required", True)))
        for provider in _normalize_endpoint_remediation_sla_notification_providers(rule.get("providers", [])):
            route = route_by_provider.setdefault(
                provider,
                {"rule_ids": [], "owner": owner, "acknowledgement_required": ack_required},
            )
            route["rule_ids"].append(rule_id)
            if owner:
                route["owner"] = owner
            route["acknowledgement_required"] = route["acknowledgement_required"] or ack_required
    return route_by_provider


def _endpoint_remediation_sla_owner_slo(
    policy: dict[str, Any],
    owner: str,
    alert_level: str,
    provider: str,
) -> dict[str, int]:
    defaults = policy.get("default_slo") if isinstance(policy.get("default_slo"), dict) else {}
    ack_minutes = int(defaults.get("acknowledgement_minutes", defaults.get("ack_minutes", 60)) or 60)
    resolution_minutes = int(defaults.get("resolution_minutes", 240) or 240)
    owner_rules = policy.get("owner_slos", policy.get("service_level_objectives", {}))
    candidates: list[dict[str, Any]] = []
    if isinstance(owner_rules, dict):
        owner_rule = owner_rules.get(owner)
        if isinstance(owner_rule, dict):
            candidates.append(owner_rule)
    elif isinstance(owner_rules, list):
        for rule in owner_rules:
            if not isinstance(rule, dict):
                continue
            owners = {str(value) for value in rule.get("owners", [])}
            providers = {str(value).lower().replace("-", "_") for value in rule.get("providers", [])}
            levels = {str(value) for value in rule.get("alert_levels", [])}
            if owners and owner not in owners:
                continue
            if providers and provider not in providers:
                continue
            if levels and alert_level not in levels:
                continue
            candidates.append(rule)
    for candidate in candidates:
        ack_minutes = int(candidate.get("acknowledgement_minutes", candidate.get("ack_minutes", ack_minutes)) or ack_minutes)
        resolution_minutes = int(candidate.get("resolution_minutes", resolution_minutes) or resolution_minutes)
    return {
        "acknowledgement_minutes": max(1, ack_minutes),
        "resolution_minutes": max(1, resolution_minutes),
    }


def _endpoint_remediation_sla_slo_state(age_minutes: float, target_minutes: int) -> str:
    if age_minutes > target_minutes:
        return "breached"
    if age_minutes >= target_minutes * 0.8:
        return "at_risk"
    return "within_slo"


def _endpoint_remediation_sla_ladder_level(
    policy: dict[str, Any],
    *,
    age_minutes: float,
    owner: str,
    alert_level: str,
    provider: str,
) -> dict[str, Any]:
    ladder = policy.get("ladders", policy.get("escalation_ladders", []))
    if not isinstance(ladder, list):
        ladder = [
            {"level": "owner", "after_minutes": 60, "providers": ["slack"], "action": "Notify remediation owner."},
            {"level": "release-governance", "after_minutes": 240, "providers": ["jira"], "action": "Escalate to release governance."},
        ]
    selected: dict[str, Any] = {}
    for raw in ladder:
        if not isinstance(raw, dict):
            continue
        owners = {str(value) for value in raw.get("owners", [])}
        providers = {str(value).lower().replace("-", "_") for value in raw.get("route_providers", raw.get("match_providers", []))}
        levels = {str(value) for value in raw.get("alert_levels", [])}
        after_minutes = int(raw.get("after_minutes", raw.get("after", 0)) or 0)
        if owners and owner not in owners:
            continue
        if providers and provider not in providers:
            continue
        if levels and alert_level not in levels:
            continue
        if age_minutes < after_minutes:
            continue
        if not selected or after_minutes >= int(selected.get("after_minutes", 0) or 0):
            selected = {
                "level": str(raw.get("level") or raw.get("name") or "owner"),
                "after_minutes": after_minutes,
                "providers": _normalize_endpoint_remediation_sla_notification_providers(raw.get("providers", [])),
                "action": str(raw.get("action") or "Escalate unacknowledged endpoint remediation SLA notification."),
            }
    return selected


def _endpoint_remediation_sla_escalation_ladder_action(
    owner: str,
    provider: str,
    acknowledgement_state: str,
    resolution_state: str,
    escalation: dict[str, Any],
) -> str:
    if escalation:
        return str(escalation.get("action") or f"Escalate {provider} route to {owner}.")
    if acknowledgement_state == "breached":
        return f"Escalate unacknowledged {provider} notification to {owner}."
    if resolution_state == "breached":
        return f"Escalate unresolved {provider} notification to {owner}."
    if acknowledgement_state == "at_risk" or resolution_state == "at_risk":
        return f"Warn {owner} that {provider} remediation notification is approaching SLO."
    return "No escalation required."


def _endpoint_remediation_sla_escalation_item_has_route(
    item: dict[str, Any],
    *,
    owner: str | None = None,
    provider: str | None = None,
) -> bool:
    plan = item.get("escalation_plan") if isinstance(item.get("escalation_plan"), dict) else item
    routes = plan.get("route_statuses", []) if isinstance(plan.get("route_statuses"), list) else []
    for route in routes:
        if not isinstance(route, dict):
            continue
        if owner and str(route.get("owner", "")).lower() != owner:
            continue
        if provider and str(route.get("provider", "")).lower() != provider:
            continue
        return True
    return False


def _endpoint_remediation_sla_route_key(plan_id: str, report_id: str, provider: str, owner: str) -> str:
    material = "|".join([plan_id, report_id, provider, owner])
    return f"erslaroute-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"


def _endpoint_remediation_sla_latest_review_by_route(reviews: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for review in reviews:
        key = _endpoint_remediation_sla_route_key(
            str(review.get("plan_id") or ""),
            str(review.get("report_id") or ""),
            str(review.get("provider") or ""),
            str(review.get("owner") or ""),
        )
        current = latest.get(key)
        if current is None or str(review.get("created_at", "")) > str(current.get("created_at", "")):
            latest[key] = review
    return latest


def _latest_release_created_at(items: list[dict[str, Any]]) -> datetime | None:
    latest: datetime | None = None
    for item in items:
        parsed = _parse_release_datetime(item.get("created_at"))
        if parsed is not None and (latest is None or parsed > latest):
            latest = parsed
    return latest


def _endpoint_remediation_sla_matching_maintenance_window(
    policy: dict[str, Any],
    *,
    now: datetime,
    plan_id: str,
    report_id: str,
    provider: str,
    owner: str,
) -> dict[str, Any] | None:
    windows = policy.get("maintenance_windows", policy.get("suppression_windows", []))
    if not isinstance(windows, list):
        return None
    for raw in windows:
        if not isinstance(raw, dict):
            continue
        start = _parse_release_datetime(raw.get("start_at") or raw.get("starts_at"))
        end = _parse_release_datetime(raw.get("end_at") or raw.get("ends_at"))
        if start is None or end is None or not (start <= now <= end):
            continue
        if not _endpoint_remediation_sla_window_matches(raw, plan_id=plan_id, report_id=report_id, provider=provider, owner=owner):
            continue
        return {
            "window_id": str(raw.get("window_id") or raw.get("id") or "maintenance-window"),
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "reason": raw.get("reason") or raw.get("description") or "maintenance window",
        }
    return None


def _endpoint_remediation_sla_window_matches(
    window: dict[str, Any],
    *,
    plan_id: str,
    report_id: str,
    provider: str,
    owner: str,
) -> bool:
    matchers = {
        "plan_ids": plan_id,
        "report_ids": report_id,
        "providers": provider,
        "owners": owner,
    }
    for matcher_field, value in matchers.items():
        configured = {str(item).lower() for item in window.get(matcher_field, [])}
        if configured and str(value).lower() not in configured:
            return False
    return True


def _endpoint_remediation_sla_owner_availability(
    policy: dict[str, Any],
    owner: str,
    *,
    now: datetime,
) -> dict[str, Any]:
    calendar = _endpoint_remediation_sla_owner_calendar(policy, owner)
    if not calendar:
        return {"available": True, "reason": "no owner calendar configured"}
    unavailable = _endpoint_remediation_sla_calendar_unavailable_window(calendar, now)
    if unavailable:
        return {"available": False, "reason": "owner unavailable window is active", "window": unavailable}
    business_hours = calendar.get("business_hours", calendar.get("availability_windows", []))
    if not business_hours:
        return {"available": True, "reason": "no business-hours restriction configured"}
    if _endpoint_remediation_sla_in_business_hours(business_hours, now):
        return {"available": True, "reason": "owner calendar is available"}
    return {"available": False, "reason": "owner calendar is outside business hours"}


def _endpoint_remediation_sla_owner_calendar(policy: dict[str, Any], owner: str) -> dict[str, Any]:
    calendars = policy.get("owner_calendars", policy.get("calendars", {}))
    if isinstance(calendars, dict):
        value = calendars.get(owner) or calendars.get(owner.lower())
        return value if isinstance(value, dict) else {}
    if isinstance(calendars, list):
        for item in calendars:
            if not isinstance(item, dict):
                continue
            owners = {str(value).lower() for value in item.get("owners", [])}
            if not owners or owner.lower() in owners:
                return item
    return {}


def _endpoint_remediation_sla_calendar_unavailable_window(
    calendar: dict[str, Any],
    now: datetime,
) -> dict[str, Any] | None:
    for raw in calendar.get("unavailable_windows", calendar.get("out_of_office", [])):
        if not isinstance(raw, dict):
            continue
        start = _parse_release_datetime(raw.get("start_at") or raw.get("starts_at"))
        end = _parse_release_datetime(raw.get("end_at") or raw.get("ends_at"))
        if start is None or end is None or not (start <= now <= end):
            continue
        return {
            "window_id": str(raw.get("window_id") or raw.get("id") or "owner-unavailable"),
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "reason": raw.get("reason") or "owner unavailable",
        }
    return None


def _endpoint_remediation_sla_in_business_hours(windows: Any, now: datetime) -> bool:
    if not isinstance(windows, list):
        return False
    day = now.strftime("%a").lower()[:3]
    current_minutes = now.hour * 60 + now.minute
    for raw in windows:
        if not isinstance(raw, dict):
            continue
        days = {str(value).lower()[:3] for value in raw.get("days", raw.get("weekdays", []))}
        if days and day not in days:
            continue
        start = _parse_hhmm_minutes(str(raw.get("start") or raw.get("start_time") or "00:00"))
        end = _parse_hhmm_minutes(str(raw.get("end") or raw.get("end_time") or "23:59"))
        if start <= current_minutes <= end:
            return True
    return False


def _parse_hhmm_minutes(value: str) -> int:
    match = re.match(r"^(\d{1,2}):(\d{2})$", value.strip())
    if not match:
        return 0
    hours = max(0, min(int(match.group(1)), 23))
    minutes = max(0, min(int(match.group(2)), 59))
    return hours * 60 + minutes


def _endpoint_remediation_sla_escalation_delivery_description(
    plan_id: str,
    routes: list[dict[str, Any]],
    *,
    omitted_route_count: int,
) -> str:
    lines = [
        f"CAVRA endpoint remediation SLA escalation plan {plan_id} has active owner review routes.",
        "",
        "Routes:",
    ]
    if not routes:
        lines.append("- No active escalation routes.")
    for item in routes:
        lines.append(
            "- "
            f"owner={item.get('owner')} provider={item.get('provider')} report={item.get('report_id')} "
            f"ack={item.get('acknowledgement_slo_state')} resolution={item.get('resolution_slo_state')} "
            f"action={item.get('recommended_action')}"
        )
    if omitted_route_count:
        lines.append(f"- {omitted_route_count} additional routes omitted from connector payload.")
    lines.extend(
        [
            "",
            "This escalation is generated from public CAVRA evidence metadata. Endpoint mutation and private connector execution remain outside the Community Edition repository.",
        ]
    )
    return "\n".join(lines)


def _endpoint_remediation_sla_recurrence_delivery_description(
    recurrence_plan_id: str,
    routes: list[dict[str, Any]],
    *,
    omitted_route_count: int,
) -> str:
    lines = [
        f"CAVRA endpoint remediation SLA recurrence plan {recurrence_plan_id} has deliverable routes.",
        "",
        "Deliverable routes:",
    ]
    if not routes:
        lines.append("- No deliverable recurrence routes.")
    for item in routes:
        lines.append(
            "- "
            f"owner={item.get('owner')} provider={item.get('provider')} report={item.get('report_id')} "
            f"recurrences={item.get('recurrence_count')}/{item.get('max_recurrences')} "
            f"next={item.get('next_delivery_at')} action={item.get('recommended_action')}"
        )
    if omitted_route_count:
        lines.append(f"- {omitted_route_count} additional deliverable routes omitted from connector payload.")
    lines.extend(
        [
            "",
            "This recurrence batch is generated from public CAVRA recurrence metadata. Suppressed routes are excluded from delivery and explained in the suppression audit export.",
        ]
    )
    return "\n".join(lines)


def _endpoint_remediation_sla_recurrence_automation_health_id(health: dict[str, Any]) -> str:
    raw = str(health.get("health_id") or health.get("session_id") or "")
    if raw:
        return raw
    material = json.dumps(
        {
            "generated_at": health.get("generated_at"),
            "latest_run_id": health.get("latest_run_id"),
            "alert_level": health.get("alert_level"),
            "missed_run_count": health.get("missed_run_count"),
            "failed_job_count": health.get("failed_job_count"),
            "connector_delivery_failure_count": health.get("connector_delivery_failure_count"),
        },
        sort_keys=True,
    )
    return f"erslah-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}"


def _endpoint_remediation_sla_recurrence_automation_health_alert_description(
    health_id: str,
    health: dict[str, Any],
    alerts: list[dict[str, Any]],
    *,
    omitted_alert_count: int,
) -> str:
    lines = [
        f"CAVRA recurrence automation health alert {health_id} is {health.get('alert_level', 'unknown')}.",
        "",
        f"Expected interval minutes: {health.get('expected_interval_minutes', 0)}",
        f"Missed runs: {health.get('missed_run_count', 0)}",
        f"Failed jobs: {health.get('failed_job_count', 0)}",
        f"Stale metadata categories: {health.get('stale_metadata_count', 0)}",
        f"Connector delivery failures: {health.get('connector_delivery_failure_count', 0)}",
        f"Latest run age minutes: {health.get('latest_run_age_minutes', 'none')}",
        "",
        "Alerts:",
    ]
    if not alerts:
        lines.append("- No active recurrence automation health alerts.")
    for item in alerts:
        lines.append("- " f"{item.get('severity')} {item.get('category')}: {item.get('message')}")
    if omitted_alert_count:
        lines.append(f"- {omitted_alert_count} additional alerts omitted from this delivery payload.")
    lines.extend(
        [
            "",
            "This alert is generated from public CAVRA recurrence automation health metadata. Scheduler recovery, ticket creation, and private queue execution remain outside the Community Edition repository.",
        ]
    )
    return "\n".join(lines)


def _endpoint_remediation_sla_owner_digest_description(
    recurrence_plan_id: str,
    owners: list[dict[str, Any]],
) -> str:
    lines = [
        f"CAVRA endpoint remediation owner digest for recurrence plan {recurrence_plan_id}.",
        "",
        "Owner summaries:",
    ]
    if not owners:
        lines.append("- No unresolved recurrence routes.")
    for item in owners:
        providers = ", ".join(f"{provider}={count}" for provider, count in item.get("providers", {}).items())
        lines.append(
            "- "
            f"owner={item.get('owner')} unresolved_routes={item.get('route_count', 0)} "
            f"retry_routes={item.get('retry_count', 0)} providers={providers or 'none'}"
        )
    lines.extend(
        [
            "",
            "This digest is generated from public CAVRA recurrence and retry metadata. Connector credentials and private endpoint mutation logic are not included.",
        ]
    )
    return "\n".join(lines)


def _endpoint_remediation_sla_owner_digest_slack_payload(
    title: str,
    message: str,
    owners: list[dict[str, Any]],
) -> dict[str, Any]:
    fields = []
    for item in owners[:10]:
        provider_text = ", ".join(f"{provider}: {count}" for provider, count in item.get("providers", {}).items())
        fields.append(
            {
                "type": "mrkdwn",
                "text": f"*{item.get('owner')}*\\nRoutes: {item.get('route_count', 0)}\\nRetries: {item.get('retry_count', 0)}\\n{provider_text}",
            }
        )
    return {
        "text": f"{title}\n{message}",
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": title[:150]}},
            {"type": "section", "text": {"type": "mrkdwn", "text": message}},
            {"type": "section", "fields": fields or [{"type": "mrkdwn", "text": "No unresolved recurrence routes."}]},
        ],
    }


def _endpoint_remediation_sla_owner_digest_teams_payload(
    title: str,
    message: str,
    alert_level: str,
    owners: list[dict[str, Any]],
) -> dict[str, Any]:
    facts = [
        {
            "name": str(item.get("owner")),
            "value": f"routes={item.get('route_count', 0)} retries={item.get('retry_count', 0)}",
        }
        for item in owners[:20]
    ]
    return {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": title,
        "themeColor": "DC2626" if alert_level == "critical" else "D97706" if alert_level == "warning" else "2E7D32",
        "title": title,
        "text": message,
        "sections": [{"facts": facts or [{"name": "status", "value": "No unresolved recurrence routes."}]}],
    }


def _endpoint_remediation_sla_recurrence_plan_by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    plans: dict[str, dict[str, Any]] = {}
    for item in items:
        if item.get("metadata_kind") != "endpoint-remediation-sla-escalation-recurrence-plan":
            continue
        plan = item.get("recurrence_plan") if isinstance(item.get("recurrence_plan"), dict) else item
        recurrence_plan_id = str(plan.get("recurrence_plan_id") or item.get("recurrence_plan_id") or item.get("session_id") or "")
        if recurrence_plan_id and recurrence_plan_id not in plans:
            plans[recurrence_plan_id] = plan
    return plans


def _endpoint_remediation_sla_routes_for_provider(plan: dict[str, Any], provider: str) -> list[dict[str, Any]]:
    decisions = plan.get("route_decisions", []) if isinstance(plan.get("route_decisions"), list) else []
    return [
        item
        for item in decisions
        if isinstance(item, dict)
        and str(item.get("provider") or "").lower().replace("-", "_") == provider.lower().replace("-", "_")
        and item.get("action") == "deliver"
    ]


def _endpoint_remediation_sla_suppression_trend_row(decision: dict[str, Any], created_at: str) -> dict[str, Any]:
    reason = str(decision.get("reason") or "")
    category = _endpoint_remediation_sla_suppression_category(decision)
    return {
        "created_at": created_at,
        "route_key": decision.get("route_key"),
        "plan_id": decision.get("plan_id"),
        "report_id": decision.get("report_id"),
        "owner": str(decision.get("owner") or "unknown"),
        "provider": str(decision.get("provider") or "unknown"),
        "action": decision.get("action"),
        "category": category,
        "reason": reason,
    }


def _endpoint_remediation_sla_recurrence_follow_up_actions(
    retry_plan: dict[str, Any],
    owner_digest_events: list[dict[str, Any]],
    suppression_trend: dict[str, Any],
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for decision in retry_plan.get("retry_decisions", []) if isinstance(retry_plan.get("retry_decisions"), list) else []:
        if not isinstance(decision, dict):
            continue
        action = str(decision.get("action") or "wait")
        actions.append(
            {
                "kind": "recurrence_retry",
                "action": action,
                "recurrence_plan_id": decision.get("recurrence_plan_id"),
                "provider": decision.get("provider"),
                "reason": decision.get("reason"),
                "next_retry_at": decision.get("next_retry_at"),
                "delivery_id": decision.get("latest_delivery_id"),
            }
        )
    for event in owner_digest_events:
        summary = event.get("summary", {}) if isinstance(event.get("summary"), dict) else {}
        actions.append(
            {
                "kind": "owner_digest",
                "action": "deliver",
                "digest_id": event.get("digest_id"),
                "recurrence_plan_id": event.get("recurrence_plan_id"),
                "owner_count": summary.get("owner_count", 0),
                "unresolved_route_count": summary.get("unresolved_route_count", 0),
            }
        )
    for event in suppression_trend.get("latest_events", []) if isinstance(suppression_trend.get("latest_events"), list) else []:
        if not isinstance(event, dict):
            continue
        actions.append(
            {
                "kind": "suppression_trend",
                "action": "review",
                "category": event.get("category"),
                "owner": event.get("owner"),
                "provider": event.get("provider"),
                "reason": event.get("reason"),
            }
        )
    return actions


def _endpoint_remediation_sla_suppression_category(decision: dict[str, Any]) -> str:
    reason = str(decision.get("reason") or "").lower()
    if decision.get("maintenance_window"):
        return "maintenance_window"
    if isinstance(decision.get("owner_availability"), dict) and not decision.get("owner_availability", {}).get("available", True):
        return "owner_calendar"
    if "maximum recurrence" in reason:
        return "maximum_recurrence"
    if "retry" in reason and "maximum" in reason:
        return "maximum_retry"
    if "interval" in reason:
        return "recurrence_interval_wait"
    if "review state" in reason or "resolved" in reason or "false_positive" in reason:
        return "owner_review"
    if decision.get("action") == "wait":
        return "wait"
    return "other"


def _endpoint_remediation_sla_suppression_audit_markdown(audit: dict[str, Any]) -> str:
    summary = audit.get("summary", {}) if isinstance(audit.get("summary"), dict) else {}
    lines = [
        "# Endpoint Remediation SLA Escalation Suppression Audit",
        "",
        f"- Audit ID: `{audit.get('audit_id')}`",
        f"- Recurrence plan ID: `{audit.get('recurrence_plan_id')}`",
        f"- Generated at: `{audit.get('generated_at')}`",
        f"- Suppressed routes: {summary.get('suppressed_route_count', 0)}",
        f"- Waiting routes: {summary.get('waiting_route_count', 0)}",
        f"- Maintenance suppressed: {summary.get('maintenance_suppressed_count', 0)}",
        f"- Calendar suppressed: {summary.get('calendar_suppressed_count', 0)}",
        "",
        "## Suppressed Routes",
    ]
    suppressed = audit.get("suppressed_routes", []) if isinstance(audit.get("suppressed_routes"), list) else []
    if not suppressed:
        lines.append("- No suppressed routes.")
    for item in suppressed:
        lines.append(
            "- "
            f"`{item.get('owner')}` `{item.get('provider')}` `{item.get('report_id')}` "
            f"{item.get('reason')}"
        )
    waiting = audit.get("waiting_routes", []) if isinstance(audit.get("waiting_routes"), list) else []
    lines.extend(["", "## Waiting Routes"])
    if not waiting:
        lines.append("- No waiting routes.")
    for item in waiting:
        lines.append(
            "- "
            f"`{item.get('owner')}` `{item.get('provider')}` `{item.get('report_id')}` "
            f"{item.get('reason')}"
        )
    lines.extend(["", "## Controls"])
    for control in audit.get("controls", []):
        lines.append(f"- `{control}`")
    return "\n".join(lines) + "\n"


def _endpoint_remediation_sla_escalation_slack_payload(
    title: str,
    message: str,
    routes: list[dict[str, Any]],
) -> dict[str, Any]:
    fields = [
        {
            "type": "mrkdwn",
            "text": (
                f"*{item.get('owner', 'owner')}* `{item.get('provider')}` "
                f"`{item.get('report_id')}` {item.get('acknowledgement_slo_state')}/"
                f"{item.get('resolution_slo_state')}"
            ),
        }
        for item in routes[:8]
    ]
    blocks: list[dict[str, Any]] = [
        {"type": "header", "text": {"type": "plain_text", "text": title[:150]}},
        {"type": "section", "text": {"type": "mrkdwn", "text": message}},
    ]
    if fields:
        blocks.append({"type": "section", "fields": fields})
    blocks.append(
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "Generated from public CAVRA endpoint remediation escalation evidence."}],
        }
    )
    return {"text": title, "blocks": blocks}


def _endpoint_remediation_sla_escalation_teams_payload(
    title: str,
    message: str,
    alert_level: str,
    routes: list[dict[str, Any]],
) -> dict[str, Any]:
    facts = [
        {
            "name": str(item.get("owner") or "owner"),
            "value": f"{item.get('provider')} {item.get('report_id')} {item.get('recommended_action')}",
        }
        for item in routes[:8]
    ]
    return {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": title,
        "themeColor": "DC2626" if alert_level == "critical" else "2E7D32",
        "sections": [
            {
                "activityTitle": title,
                "activitySubtitle": message,
                "facts": facts,
            }
        ],
    }


def _endpoint_remediation_sla_recurrence_automation_health_slack_payload(
    title: str,
    message: str,
    alerts: list[dict[str, Any]],
) -> dict[str, Any]:
    fields = [
        {
            "type": "mrkdwn",
            "text": f"*{item.get('severity', 'unknown').title()}* `{item.get('category')}` {item.get('message')}",
        }
        for item in alerts[:8]
    ]
    blocks: list[dict[str, Any]] = [
        {"type": "header", "text": {"type": "plain_text", "text": title[:150]}},
        {"type": "section", "text": {"type": "mrkdwn", "text": message}},
    ]
    if fields:
        blocks.append({"type": "section", "fields": fields})
    blocks.append(
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "Generated from public CAVRA recurrence automation health evidence."}],
        }
    )
    return {"text": title, "blocks": blocks}


def _endpoint_remediation_sla_recurrence_automation_health_teams_payload(
    title: str,
    message: str,
    alert_level: str,
    alerts: list[dict[str, Any]],
) -> dict[str, Any]:
    facts = [
        {
            "name": str(item.get("category") or "alert"),
            "value": f"{item.get('severity')} {item.get('message')}",
        }
        for item in alerts[:8]
    ]
    return {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": title,
        "themeColor": "DC2626" if alert_level == "critical" else "D97706" if alert_level == "warning" else "2E7D32",
        "sections": [
            {
                "activityTitle": title,
                "activitySubtitle": message,
                "facts": facts,
            }
        ],
    }


def _endpoint_remediation_sla_notification_description(
    report_id: str,
    alert_level: str,
    summary: dict[str, Any],
    escalations: list[dict[str, Any]],
) -> str:
    lines = [
        f"CAVRA endpoint remediation SLA report {report_id} is {alert_level}.",
        "",
        f"Tracked work items: {summary.get('tracked_work_item_count', 0)}",
        f"Completed: {summary.get('completed_count', 0)}",
        f"At risk: {summary.get('at_risk_count', 0)}",
        f"Breached: {summary.get('breached_count', 0)}",
        f"Critical providers: {summary.get('critical_provider_count', 0)}",
        "",
        "Escalations:",
    ]
    if not escalations:
        lines.append("- No active SLA escalations.")
    for item in escalations:
        lines.append(
            "- "
            f"{item.get('severity')} provider={item.get('provider')} handoff={item.get('handoff_id')} "
            f"status={item.get('status')} action={item.get('recommended_action')}"
        )
    lines.extend(
        [
            "",
            "This notification is generated from public CAVRA SLA metadata. Endpoint mutation and private connector execution remain outside the Community Edition repository.",
        ]
    )
    return "\n".join(lines)


def _endpoint_remediation_sla_slack_payload(
    title: str,
    message: str,
    escalations: list[dict[str, Any]],
) -> dict[str, Any]:
    fields = [
        {
            "type": "mrkdwn",
            "text": f"*{item.get('severity', 'unknown').title()}* `{item.get('provider')}` `{item.get('handoff_id')}`",
        }
        for item in escalations[:8]
    ]
    blocks: list[dict[str, Any]] = [
        {"type": "header", "text": {"type": "plain_text", "text": title[:150]}},
        {"type": "section", "text": {"type": "mrkdwn", "text": message}},
    ]
    if fields:
        blocks.append({"type": "section", "fields": fields})
    blocks.append(
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "Generated from public CAVRA endpoint remediation SLA evidence."}],
        }
    )
    return {"text": title, "blocks": blocks}


def _endpoint_remediation_sla_teams_payload(
    title: str,
    message: str,
    alert_level: str,
    escalations: list[dict[str, Any]],
) -> dict[str, Any]:
    facts = [
        {
            "name": str(item.get("provider") or "provider"),
            "value": f"{item.get('severity')} {item.get('handoff_id')} {item.get('status')}",
        }
        for item in escalations[:8]
    ]
    return {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": title,
        "themeColor": "DC2626" if alert_level == "critical" else "D97706" if alert_level == "warning" else "2E7D32",
        "sections": [
            {
                "activityTitle": title,
                "activitySubtitle": message,
                "facts": facts,
            }
        ],
    }


def _endpoint_remediation_sla_jira_payload(title: str, description: str, alert_level: str) -> dict[str, Any]:
    return {
        "fields": {
            "summary": title,
            "description": description,
            "labels": ["cavra", "endpoint-remediation", "sla", alert_level],
        }
    }


def _endpoint_remediation_sla_servicenow_payload(
    title: str,
    description: str,
    report_id: str,
    alert_level: str,
) -> dict[str, Any]:
    return {
        "short_description": title,
        "description": description,
        "category": "software",
        "subcategory": "endpoint_runtime",
        "impact": "1" if alert_level == "critical" else "2" if alert_level == "warning" else "3",
        "urgency": "1" if alert_level == "critical" else "2",
        "correlation_id": report_id,
    }


def _normalize_endpoint_remediation_handoff_providers(providers: list[str] | None) -> list[str]:
    allowed = {"jira", "servicenow", "slack", "teams", "private_queue"}
    selected: set[str] = set()
    for provider in providers or ["all"]:
        for raw in str(provider).split(","):
            value = raw.strip().lower().replace("-", "_")
            if not value:
                continue
            if value == "all":
                selected.update(allowed)
            elif value in allowed:
                selected.add(value)
    return sorted(selected)


def _endpoint_remediation_provider_payload(
    provider: str,
    remediation_request: dict[str, Any],
    actions: list[dict[str, Any]],
    *,
    handoff_id: str,
) -> dict[str, Any]:
    request_id = str(remediation_request.get("request_id") or "")
    reconciliation_id = str(remediation_request.get("reconciliation_id") or "")
    approval = remediation_request.get("approval", {}) if isinstance(remediation_request.get("approval"), dict) else {}
    summary = remediation_request.get("summary", {}) if isinstance(remediation_request.get("summary"), dict) else {}
    base = {
        "schema_version": f"cavra.endpoint-remediation-handoff.{provider}.v1",
        "product": "CAVRA",
        "handoff_id": handoff_id,
        "provider": provider,
        "request_id": request_id,
        "reconciliation_id": reconciliation_id,
        "approval_id": approval.get("approval_id"),
        "approval_state": approval.get("state"),
        "action_count": len(actions),
        "strategy": remediation_request.get("strategy"),
        "release": remediation_request.get("release", {}),
        "channel": remediation_request.get("channel"),
        "summary": summary,
        "actions": actions,
        "execution_guard": {
            "requires_approved_approval": True,
            "approval_id": approval.get("approval_id"),
            "private_connector_must_recheck_approval": True,
        },
    }
    title = f"CAVRA endpoint remediation {request_id}"
    text = (
        f"CAVRA detected endpoint drift for reconciliation {reconciliation_id}. "
        f"{len(actions)} remediation actions are prepared. Approval {approval.get('approval_id')} is {approval.get('state')}."
    )
    if provider == "jira":
        return base | {
            "issue": {
                "project": {"key": "CAVRA"},
                "issuetype": {"name": "Task"},
                "summary": title,
                "description": text,
                "labels": ["cavra", "endpoint-remediation", str(remediation_request.get("strategy") or "mixed")],
            }
        }
    if provider == "servicenow":
        return base | {
            "change_request": {
                "short_description": title,
                "description": text,
                "category": "software",
                "subcategory": "endpoint_runtime",
                "impact": "2" if remediation_request.get("alert_level") == "critical" else "3",
                "urgency": "2",
                "correlation_id": handoff_id,
                "u_cavra_request_id": request_id,
                "u_cavra_approval_id": approval.get("approval_id"),
            }
        }
    if provider == "slack":
        return base | {
            "message": {
                "text": title,
                "blocks": [
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"*{title}*\n{text}"}},
                    {"type": "context", "elements": [{"type": "mrkdwn", "text": f"Handoff `{handoff_id}`"}]},
                ],
            }
        }
    if provider == "teams":
        return base | {
            "message_card": {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": title,
                "themeColor": "D97706" if remediation_request.get("alert_level") == "warning" else "DC2626",
                "title": title,
                "text": text,
            }
        }
    return base | {
        "queue_event": {
            "event_type": "cavra.endpoint_remediation_handoff",
            "dedupe_key": handoff_id,
            "status": "ready_for_private_connector",
            "work_items": [
                {
                    "action_id": action.get("action_id"),
                    "action_type": action.get("action_type"),
                    "provider": action.get("provider"),
                    "deployment_target": action.get("deployment_target"),
                    "endpoint_id": action.get("endpoint_id"),
                    "requires_approval_id": approval.get("approval_id"),
                }
                for action in actions
            ],
        }
    }


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
