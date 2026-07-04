from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


ENTERPRISE_EVIDENCE_CUSTODY_SCHEMA = "cavra.evidence.custody.v1"
ENTERPRISE_EVIDENCE_CUSTODY_READINESS_SCHEMA = "cavra.evidence.custody.readiness.v1"

SUPPORTED_SIGNING_PROVIDERS = {
    "aws_kms",
    "azure_key_vault",
    "gcp_cloud_kms",
    "hashicorp_vault_transit",
    "pkcs11_hsm",
    "managed_hsm",
}
SUPPORTED_ALGORITHMS = {"Ed25519", "ECDSA_P256_SHA256", "RSA_PSS_SHA256"}
SUPPORTED_CUSTODY_BOUNDARIES = {"cloud_kms", "managed_hsm", "hsm", "vault_transit", "pkcs11"}
REQUIRED_VERIFIER_COMMANDS = {
    "cavra evidence verify",
    "cavra evidence verify-attestation",
}


def build_enterprise_evidence_custody_contract() -> dict[str, Any]:
    return {
        "schema_version": "cavra.evidence.custody.contract.v1",
        "product": "CAVRA",
        "purpose": "Enterprise KMS/HSM evidence signing, key custody, rotation, revocation, and independent verification contract.",
        "supported_signing_providers": sorted(SUPPORTED_SIGNING_PROVIDERS),
        "supported_algorithms": sorted(SUPPORTED_ALGORITHMS),
        "required_controls": [
            "signing key is KMS/HSM/Vault backed",
            "private key export is disabled",
            "dual-control custody is required",
            "rotation cadence is at most 90 days",
            "rotation has overlap and historical verification retention",
            "emergency revocation drill is tested",
            "public trust roots are distributed to independent verifiers",
            "sample or live evidence bundle verification has passed",
        ],
        "default_rotation_cadence_days": 90,
        "minimum_rotation_overlap_days": 7,
        "required_verifier_commands": sorted(REQUIRED_VERIFIER_COMMANDS),
    }


def build_enterprise_evidence_custody_readiness(
    packet: dict[str, Any] | None = None,
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    if packet is None:
        return {
            "schema_version": ENTERPRISE_EVIDENCE_CUSTODY_READINESS_SCHEMA,
            "product": "CAVRA",
            "evidence_mode": "contract",
            "ready_for_enterprise_evidence_custody_contract": True,
            "ready_for_enterprise_live_evidence_custody": False,
            "status": "ready_with_warnings",
            "blocker_count": 0,
            "warning_count": 1,
            "checks": [
                {
                    "name": "evidence_packet",
                    "status": "warn",
                    "message": "Enterprise evidence custody contract is available, but no sample or live packet was supplied.",
                }
            ],
        }
    return validate_enterprise_evidence_custody_packet(packet, require_live=require_live)


def validate_enterprise_evidence_custody_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_signing_provider(packet.get("signing_provider", {}), checks)
    _check_custody_policy(packet.get("custody_policy", {}), checks)
    _check_rotation(packet.get("rotation", {}), checks)
    _check_trust_roots(packet.get("trust_roots", {}), checks)
    _check_independent_verifier(packet.get("independent_verifier", {}), checks)
    _check_audit_evidence(packet.get("audit_evidence", {}), checks)

    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": ENTERPRISE_EVIDENCE_CUSTODY_READINESS_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_enterprise_evidence_custody_contract": contract_ready,
        "ready_for_enterprise_live_evidence_custody": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if packet.get("schema_version") == ENTERPRISE_EVIDENCE_CUSTODY_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Evidence custody packet schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Packet must use cavra.evidence.custody.v1.")


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    evidence_mode = packet.get("evidence_mode")
    if evidence_mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live evidence custody packet supplied.")
    elif evidence_mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample evidence custody packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live evidence custody validation requires evidence_mode=live.")


def _check_signing_provider(provider: dict[str, Any], checks: list[dict[str, str]]) -> None:
    provider_type = provider.get("type")
    algorithm = provider.get("algorithm")
    no_export = provider.get("private_key_exportable") is False
    external_signing = provider.get("external_signing_enforced") is True
    key_ref = bool(provider.get("key_ref") or provider.get("key_id"))
    if (
        provider_type in SUPPORTED_SIGNING_PROVIDERS
        and algorithm in SUPPORTED_ALGORITHMS
        and no_export
        and external_signing
        and key_ref
    ):
        _add_check(
            checks,
            "signing_provider",
            "pass",
            f"Signing provider {provider_type} uses {algorithm} with non-exportable external signing.",
        )
        return
    missing: list[str] = []
    if provider_type not in SUPPORTED_SIGNING_PROVIDERS:
        missing.append("supported provider")
    if algorithm not in SUPPORTED_ALGORITHMS:
        missing.append("supported algorithm")
    if not no_export:
        missing.append("private_key_exportable=false")
    if not external_signing:
        missing.append("external_signing_enforced=true")
    if not key_ref:
        missing.append("key_ref/key_id")
    _add_check(checks, "signing_provider", "blocker", f"Signing provider is missing: {', '.join(missing)}.")


def _check_custody_policy(policy: dict[str, Any], checks: list[dict[str, str]]) -> None:
    owners = [owner for owner in policy.get("owners", []) if owner]
    boundary = policy.get("custody_boundary")
    controls = {
        "dual_control_required": policy.get("dual_control_required") is True,
        "separation_of_duties": policy.get("separation_of_duties") is True,
        "break_glass_process": policy.get("break_glass_process") is True,
        "private_key_export_allowed_false": policy.get("private_key_export_allowed") is False,
    }
    if len(owners) >= 2 and boundary in SUPPORTED_CUSTODY_BOUNDARIES and all(controls.values()):
        _add_check(checks, "custody_policy", "pass", "Dual-control custody policy and non-export boundary are defined.")
        return
    missing = [name for name, ok in controls.items() if not ok]
    if len(owners) < 2:
        missing.append("at least two owners")
    if boundary not in SUPPORTED_CUSTODY_BOUNDARIES:
        missing.append("supported custody_boundary")
    _add_check(checks, "custody_policy", "blocker", f"Custody policy is missing: {', '.join(missing)}.")


def _check_rotation(rotation: dict[str, Any], checks: list[dict[str, str]]) -> None:
    cadence = _as_int(rotation.get("cadence_days"))
    overlap = _as_int(rotation.get("overlap_days"))
    previous_retained = rotation.get("previous_key_retained_for_verification") is True
    emergency_tested = rotation.get("emergency_revocation_tested") is True
    evidence_ref = bool(rotation.get("latest_rotation_evidence_ref"))
    next_due = bool(rotation.get("next_rotation_due_at"))
    if (
        cadence is not None
        and cadence <= 90
        and overlap is not None
        and overlap >= 7
        and previous_retained
        and emergency_tested
        and evidence_ref
        and next_due
    ):
        _add_check(checks, "rotation_policy", "pass", f"Rotation cadence {cadence} days and overlap {overlap} days meet policy.")
        return
    missing: list[str] = []
    if cadence is None or cadence > 90:
        missing.append("cadence_days<=90")
    if overlap is None or overlap < 7:
        missing.append("overlap_days>=7")
    if not previous_retained:
        missing.append("previous_key_retained_for_verification=true")
    if not emergency_tested:
        missing.append("emergency_revocation_tested=true")
    if not evidence_ref:
        missing.append("latest_rotation_evidence_ref")
    if not next_due:
        missing.append("next_rotation_due_at")
    _add_check(checks, "rotation_policy", "blocker", f"Rotation policy is missing: {', '.join(missing)}.")


def _check_trust_roots(trust_roots: dict[str, Any], checks: list[dict[str, str]]) -> None:
    active = [key for key in trust_roots.get("active_key_ids", []) if key]
    retired = [key for key in trust_roots.get("retired_key_ids", []) if key]
    revoked = trust_roots.get("revoked_key_ids", [])
    distribution_ref = bool(trust_roots.get("distribution_package_ref"))
    checksum_verified = trust_roots.get("distribution_checksum_verified") is True
    verifier_access = trust_roots.get("verifier_access_confirmed") is True
    revoked_list_declared = isinstance(revoked, list)
    if active and retired and distribution_ref and checksum_verified and verifier_access and revoked_list_declared:
        _add_check(checks, "trust_roots", "pass", "Active, retired, and verifier-distributed trust roots are recorded.")
        return
    missing: list[str] = []
    if not active:
        missing.append("active_key_ids")
    if not retired:
        missing.append("retired_key_ids")
    if not distribution_ref:
        missing.append("distribution_package_ref")
    if not checksum_verified:
        missing.append("distribution_checksum_verified=true")
    if not verifier_access:
        missing.append("verifier_access_confirmed=true")
    if not revoked_list_declared:
        missing.append("revoked_key_ids list")
    _add_check(checks, "trust_roots", "blocker", f"Trust-root distribution is missing: {', '.join(missing)}.")


def _check_independent_verifier(verifier: dict[str, Any], checks: list[dict[str, str]]) -> None:
    commands = {str(command) for command in verifier.get("commands", [])}
    has_required_command = all(any(required in command for command in commands) for required in REQUIRED_VERIFIER_COMMANDS)
    if (
        verifier.get("enabled") is True
        and verifier.get("offline_verification_supported") is True
        and verifier.get("sample_bundle_verified") is True
        and verifier.get("attestation_verified") is True
        and bool(verifier.get("latest_verification_evidence_ref"))
        and has_required_command
    ):
        _add_check(checks, "independent_verifier", "pass", "Independent verifier can validate bundles and attestations offline.")
        return
    missing: list[str] = []
    for key in (
        "enabled",
        "offline_verification_supported",
        "sample_bundle_verified",
        "attestation_verified",
    ):
        if verifier.get(key) is not True:
            missing.append(f"{key}=true")
    if not verifier.get("latest_verification_evidence_ref"):
        missing.append("latest_verification_evidence_ref")
    if not has_required_command:
        missing.append("required verifier commands")
    _add_check(checks, "independent_verifier", "blocker", f"Independent verifier is missing: {', '.join(missing)}.")


def _check_audit_evidence(audit: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = {
        "custody_review_ref": audit.get("custody_review_ref"),
        "rotation_approval_ref": audit.get("rotation_approval_ref"),
        "revocation_drill_ref": audit.get("revocation_drill_ref"),
        "verifier_handoff_ref": audit.get("verifier_handoff_ref"),
    }
    missing = [name for name, value in required.items() if not value]
    if not missing:
        _add_check(checks, "audit_evidence", "pass", "Custody, rotation, revocation, and verifier handoff evidence refs are present.")
        return
    _add_check(checks, "audit_evidence", "blocker", f"Audit evidence is missing: {', '.join(missing)}.")


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()
