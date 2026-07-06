from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_DRIFT_REMEDIATION_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_DRIFT_REMEDIATION_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout.result.v1"
)

REQUIRED_DRIFT_REMEDIATION_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
    "web_owner_ref",
    "compliance_owner_ref",
    "audit_owner_ref",
    "operations_owner_ref",
}

REQUIRED_DRIFT_REMEDIATION_CONTRACT_FIELDS = {
    "drift_remediation_closeout_ref",
    "source_first_cycle_review_ref",
    "drift_register_ref",
    "remediation_disposition_ref",
    "accepted_risk_ref",
    "public_status_update_ref",
    "next_cycle_blocker_clearance_ref",
    "remediation_archive_ref",
    "owner_acknowledgement_ref",
    "redaction_status",
}

REQUIRED_DRIFT_REGISTER_REFS = {
    "broken_link_drift_ref",
    "stale_scorecard_drift_ref",
    "archive_freshness_drift_ref",
    "redaction_posture_drift_ref",
}

REQUIRED_REMEDIATION_DISPOSITION_REFS = {
    "remediated_item_register_ref",
    "accepted_risk_register_ref",
    "deferred_item_register_ref",
    "no_open_critical_drift_ref",
}

REQUIRED_ACCEPTED_RISK_REFS = {
    "accepted_risk_owner_ref",
    "accepted_risk_expiry_ref",
    "accepted_risk_review_ref",
    "accepted_risk_public_boundary_ref",
}

REQUIRED_PUBLIC_STATUS_UPDATE_REFS = {
    "public_scorecard_update_ref",
    "public_status_summary_update_ref",
    "readme_status_update_ref",
    "wiki_status_update_ref",
}

REQUIRED_BLOCKER_CLEARANCE_REFS = {
    "next_cycle_blocker_register_ref",
    "blocker_clearance_owner_ref",
    "no_unassigned_blockers_ref",
    "next_cycle_go_ref",
}

REQUIRED_REMEDIATION_ARCHIVE_REFS = {
    "drift_remediation_manifest_ref",
    "first_cycle_review_archive_ref",
    "remediation_disposition_archive_ref",
    "public_status_update_archive_ref",
    "immutable_remediation_archive_ref",
}

REQUIRED_OWNER_ACK_REFS = {
    "operations_owner_ack_ref",
    "security_owner_ack_ref",
    "communications_owner_ack_ref",
    "audit_owner_ack_ref",
}

REQUIRED_CI_GATES = {
    "source_first_cycle_review_validation",
    "drift_register_validation",
    "remediation_disposition_validation",
    "accepted_risk_validation",
    "public_status_update_validation",
    "next_cycle_blocker_clearance_validation",
    "remediation_archive_validation",
    "owner_acknowledgement_validation",
}

REQUIRED_DRIFT_REMEDIATION_CONTROLS = {
    "first_cycle_review_ready",
    "drift_items_registered",
    "drift_items_dispositioned",
    "critical_drift_cleared",
    "accepted_risks_owned",
    "public_status_updated",
    "next_cycle_blockers_cleared",
    "remediation_archive_complete",
    "owner_acknowledgements_complete",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_DRIFT_REMEDIATION_FIELDS = {
    "alert_payload",
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_health_score",
    "customer_name",
    "customer_score",
    "customer_status",
    "finding_detail",
    "legal_terms",
    "monitor_payload",
    "private_note",
    "pricing",
    "raw_alert",
    "raw_archive",
    "raw_audit",
    "raw_blocker",
    "raw_contract",
    "raw_drift",
    "raw_evidence",
    "raw_finding",
    "raw_health",
    "raw_link_check",
    "raw_monitor",
    "raw_public_status",
    "raw_redaction",
    "raw_remediation",
    "raw_review",
    "raw_risk",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "recipient_email",
    "remediation_detail",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
    first_cycle_review_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    first_cycle_review = (
        first_cycle_review_packet
        or build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    first_cycle_review_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        first_cycle_review,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_DRIFT_REMEDIATION_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "monitoring_drift_remediation_closeout_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout"
        ),
        "first_cycle_review_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review/r7"
        ),
        "first_cycle_review_result": first_cycle_review_result,
        "drift_remediation_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "web_owner_ref": f"{prefix}://owner/web-platform",
            "compliance_owner_ref": f"{prefix}://owner/compliance",
            "audit_owner_ref": f"{prefix}://owner/audit",
            "operations_owner_ref": f"{prefix}://owner/operations",
        },
        "drift_remediation_contract": {
            "drift_remediation_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/closeout"
            ),
            "source_first_cycle_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/source-first-cycle-review"
            ),
            "drift_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/drift-register"
            ),
            "remediation_disposition_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/remediation-disposition"
            ),
            "accepted_risk_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/accepted-risk"
            ),
            "public_status_update_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/public-status-update"
            ),
            "next_cycle_blocker_clearance_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/next-cycle-blockers"
            ),
            "remediation_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/archive"
            ),
            "owner_acknowledgement_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/owner-acknowledgement"
            ),
            "redaction_status": "sanitized",
        },
        "drift_register_refs": {
            "broken_link_drift_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/drift/broken-link"
            ),
            "stale_scorecard_drift_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/drift/stale-scorecard"
            ),
            "archive_freshness_drift_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/drift/archive-freshness"
            ),
            "redaction_posture_drift_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/drift/redaction-posture"
            ),
        },
        "remediation_disposition_refs": {
            "remediated_item_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/disposition/remediated"
            ),
            "accepted_risk_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/disposition/accepted-risk"
            ),
            "deferred_item_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/disposition/deferred"
            ),
            "no_open_critical_drift_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/disposition/no-critical-drift"
            ),
        },
        "accepted_risk_refs": {
            "accepted_risk_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/risk/owner"
            ),
            "accepted_risk_expiry_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/risk/expiry"
            ),
            "accepted_risk_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/risk/review"
            ),
            "accepted_risk_public_boundary_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/risk/public-boundary"
            ),
        },
        "public_status_update_refs": {
            "public_scorecard_update_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/status/scorecard"
            ),
            "public_status_summary_update_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/status/summary"
            ),
            "readme_status_update_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/status/readme"
            ),
            "wiki_status_update_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/status/wiki"
            ),
        },
        "blocker_clearance_refs": {
            "next_cycle_blocker_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/blockers/register"
            ),
            "blocker_clearance_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/blockers/owner"
            ),
            "no_unassigned_blockers_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/blockers/no-unassigned"
            ),
            "next_cycle_go_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/blockers/next-cycle-go"
            ),
        },
        "remediation_archive_refs": {
            "drift_remediation_manifest_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/archive/manifest"
            ),
            "first_cycle_review_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/archive/first-cycle-review"
            ),
            "remediation_disposition_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/archive/disposition"
            ),
            "public_status_update_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/archive/public-status"
            ),
            "immutable_remediation_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/archive/immutable"
            ),
        },
        "owner_acknowledgement_refs": {
            "operations_owner_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/ack/operations"
            ),
            "security_owner_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/ack/security"
            ),
            "communications_owner_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/ack/communications"
            ),
            "audit_owner_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/ack/audit"
            ),
        },
        "ci_gate_coverage": {
            "source_first_cycle_review_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-drift-remediation-closeout/source-first-cycle-validation"
            ),
            "drift_register_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-drift-remediation-closeout/drift-register-validation"
            ),
            "remediation_disposition_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-drift-remediation-closeout/disposition-validation"
            ),
            "accepted_risk_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-drift-remediation-closeout/risk-validation"
            ),
            "public_status_update_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-drift-remediation-closeout/public-status-validation"
            ),
            "next_cycle_blocker_clearance_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-drift-remediation-closeout/blocker-validation"
            ),
            "remediation_archive_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-drift-remediation-closeout/archive-validation"
            ),
            "owner_acknowledgement_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-drift-remediation-closeout/owner-ack-validation"
            ),
        },
        "drift_remediation_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/source-first-cycle-review",
            f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/drift-register",
            f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/remediation-disposition",
            f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/accepted-risk",
            f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/public-status-update",
            f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/blocker-clearance",
            f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/remediation-archive",
            f"{prefix}://phase8/public-scorecard-monitoring-drift-remediation-closeout/owner-acknowledgement",
        ],
        "drift_remediation_controls": {
            "first_cycle_review_ready": first_cycle_review_result["blocker_count"] == 0,
            "drift_items_registered": True,
            "drift_items_dispositioned": True,
            "critical_drift_cleared": True,
            "accepted_risks_owned": True,
            "public_status_updated": True,
            "next_cycle_blockers_cleared": True,
            "remediation_archive_complete": True,
            "owner_acknowledgements_complete": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_DRIFT_REMEDIATION_CLOSEOUT_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard monitoring drift remediation closeout schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("first_cycle_review_ref"), checks, "first_cycle_review_ref")
    _check_first_cycle_review_result(packet.get("first_cycle_review_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("drift_remediation_owner_refs", {}),
        REQUIRED_DRIFT_REMEDIATION_OWNER_REFS,
        checks,
        "drift_remediation_owner_refs",
    )
    _check_drift_remediation_contract(packet.get("drift_remediation_contract", {}), checks)
    _check_required_refs(packet.get("drift_register_refs", {}), REQUIRED_DRIFT_REGISTER_REFS, checks, "drift_register_refs")
    _check_required_refs(
        packet.get("remediation_disposition_refs", {}),
        REQUIRED_REMEDIATION_DISPOSITION_REFS,
        checks,
        "remediation_disposition_refs",
    )
    _check_required_refs(packet.get("accepted_risk_refs", {}), REQUIRED_ACCEPTED_RISK_REFS, checks, "accepted_risk_refs")
    _check_required_refs(
        packet.get("public_status_update_refs", {}),
        REQUIRED_PUBLIC_STATUS_UPDATE_REFS,
        checks,
        "public_status_update_refs",
    )
    _check_required_refs(
        packet.get("blocker_clearance_refs", {}),
        REQUIRED_BLOCKER_CLEARANCE_REFS,
        checks,
        "blocker_clearance_refs",
    )
    _check_required_refs(
        packet.get("remediation_archive_refs", {}),
        REQUIRED_REMEDIATION_ARCHIVE_REFS,
        checks,
        "remediation_archive_refs",
    )
    _check_required_refs(
        packet.get("owner_acknowledgement_refs", {}),
        REQUIRED_OWNER_ACK_REFS,
        checks,
        "owner_acknowledgement_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(
        packet.get("drift_remediation_evidence_refs", []),
        checks,
        "drift_remediation_evidence_refs",
        min_count=8,
    )
    _check_controls(packet.get("drift_remediation_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_drift_remediation_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard monitoring drift remediation closeout contains sanitized refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_DRIFT_REMEDIATION_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
        sample
    )
    live_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout.live.sanitized.example.json",
        "sample_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout.live.sanitized.result.json",
    }
    payloads = {
        "sample": sample,
        "live_sanitized_example": live,
        "sample_result": sample_result,
        "live_result": live_result,
    }
    for key, path in written.items():
        path.write_text(json.dumps(payloads[key], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 drift remediation closeout supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 drift remediation closeout validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Drift remediation closeout requires evidence_mode=live and sanitized=true.")


def _check_first_cycle_review_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "first_cycle_review_result", "blocker", "first_cycle_review_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "first_cycle_review_result", "pass", "Source first-cycle review is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "first_cycle_review_result",
            "warn",
            "Source first-cycle review validates shape but is not live.",
        )
    else:
        _add_check(checks, "first_cycle_review_result", "blocker", "Source first-cycle review is not ready.")


def _check_required_refs(payload: Any, required: set[str], checks: list[dict[str, str]], name: str) -> None:
    if not isinstance(payload, dict):
        _add_check(checks, name, "blocker", f"{name} must be an object.")
        return
    missing = sorted(field for field in required if not payload.get(field))
    unsafe = sorted(field for field, value in payload.items() if value and not _is_safe_ref(value))
    if not missing and not unsafe:
        _add_check(checks, name, "pass", f"{name} are present and sanitized.")
    else:
        problems = []
        if missing:
            problems.append(f"missing refs: {', '.join(missing)}")
        if unsafe:
            problems.append(f"unsafe refs: {', '.join(unsafe)}")
        _add_check(checks, name, "blocker", f"{name} are invalid: {'; '.join(problems)}.")


def _check_drift_remediation_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "drift_remediation_contract", "blocker", "drift_remediation_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_DRIFT_REMEDIATION_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_DRIFT_REMEDIATION_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "drift_remediation_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard drift remediation closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard drift remediation closeout contract invalid: "
            f"missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}."
        ),
    )


def _check_ref_list(refs: Any, checks: list[dict[str, str]], name: str, *, min_count: int) -> None:
    if not isinstance(refs, list) or len(refs) < min_count:
        _add_check(checks, name, "blocker", f"{name} must contain at least {min_count} refs.")
        return
    unsafe = [str(ref) for ref in refs if not _is_safe_ref(ref)]
    _add_check(
        checks,
        name,
        "pass" if not unsafe else "blocker",
        f"{name} are sanitized." if not unsafe else f"{name} are unsafe: {', '.join(unsafe)}.",
    )


def _check_ci_gate_coverage(coverage: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(coverage, dict):
        _add_check(checks, "ci_gate_coverage", "blocker", "ci_gate_coverage must be an object.")
        return
    missing = sorted(gate for gate in REQUIRED_CI_GATES if not coverage.get(gate))
    unsafe = sorted(gate for gate, value in coverage.items() if value and not _is_safe_ref(value))
    _add_check(
        checks,
        "ci_gate_coverage",
        "pass" if not missing and not unsafe else "blocker",
        "CI gate coverage refs are complete."
        if not missing and not unsafe
        else f"CI gate coverage invalid: missing {', '.join(missing) or 'none'}; unsafe {', '.join(unsafe) or 'none'}.",
    )


def _check_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "drift_remediation_controls", "blocker", "drift_remediation_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_DRIFT_REMEDIATION_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "drift_remediation_controls",
        "pass" if not missing else "blocker",
        "Public scorecard drift remediation closeout controls are explicit."
        if not missing
        else f"Public scorecard drift remediation closeout controls missing or false: {', '.join(missing)}.",
    )


def _check_safe_ref(value: Any, checks: list[dict[str, str]], name: str) -> None:
    _add_check(
        checks,
        name,
        "pass" if _is_safe_ref(value) else "blocker",
        f"{name} is a sanitized reference." if _is_safe_ref(value) else f"{name} must be a sanitized reference.",
    )


def _prefix(evidence_mode: str) -> str:
    return "sample" if evidence_mode == "sample" else "evidence"


def _is_safe_ref(value: Any) -> bool:
    text = str(value)
    return any(text.startswith(prefix) for prefix in ALLOWED_REF_PREFIXES)


def _find_forbidden_phase8_drift_remediation_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_DRIFT_REMEDIATION_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_drift_remediation_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_drift_remediation_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
