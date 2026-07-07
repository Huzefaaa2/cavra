from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_THIRD_CYCLE_READINESS_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-third-cycle-readiness.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_THIRD_CYCLE_READINESS_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-third-cycle-readiness.result.v1"
)

REQUIRED_THIRD_CYCLE_OWNER_REFS = {
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

REQUIRED_THIRD_CYCLE_CONTRACT_FIELDS = {
    "third_cycle_readiness_ref",
    "source_second_cycle_drift_remediation_closeout_ref",
    "remediated_state_ref",
    "accepted_risk_boundary_ref",
    "public_surface_currency_ref",
    "monitoring_input_ref",
    "third_cycle_blocker_status_ref",
    "third_cycle_schedule_ref",
    "owner_readiness_ack_ref",
    "redaction_status",
}

REQUIRED_REMEDIATED_STATE_REFS = {
    "remediated_drift_snapshot_ref",
    "no_open_critical_drift_ref",
    "deferred_items_register_ref",
    "remediation_owner_ref",
}

REQUIRED_ACCEPTED_RISK_BOUNDARY_REFS = {
    "accepted_risk_register_ref",
    "accepted_risk_expiry_review_ref",
    "risk_owner_ack_ref",
    "public_boundary_assertion_ref",
}

REQUIRED_PUBLIC_SURFACE_CURRENCY_REFS = {
    "public_scorecard_current_ref",
    "public_status_summary_current_ref",
    "readme_status_current_ref",
    "wiki_status_current_ref",
}

REQUIRED_MONITORING_INPUT_REFS = {
    "scorecard_health_input_ref",
    "link_health_input_ref",
    "archive_freshness_input_ref",
    "redaction_posture_input_ref",
}

REQUIRED_THIRD_CYCLE_BLOCKER_REFS = {
    "blocker_register_ref",
    "no_unassigned_blockers_ref",
    "no_unresolved_critical_blockers_ref",
    "third_cycle_go_ref",
}

REQUIRED_THIRD_CYCLE_SCHEDULE_REFS = {
    "third_cycle_start_ref",
    "weekly_review_schedule_ref",
    "monthly_audit_schedule_ref",
    "quarterly_refresh_schedule_ref",
}

REQUIRED_OWNER_READINESS_ACK_REFS = {
    "operations_readiness_ack_ref",
    "security_readiness_ack_ref",
    "communications_readiness_ack_ref",
    "audit_readiness_ack_ref",
}

REQUIRED_CI_GATES = {
    "source_second_cycle_drift_remediation_closeout_validation",
    "remediated_state_validation",
    "accepted_risk_boundary_validation",
    "public_surface_currency_validation",
    "monitoring_input_validation",
    "third_cycle_blocker_validation",
    "third_cycle_schedule_validation",
    "owner_readiness_ack_validation",
}

REQUIRED_THIRD_CYCLE_CONTROLS = {
    "second_cycle_drift_remediation_closeout_ready",
    "remediated_state_ready",
    "accepted_risks_bounded",
    "public_surfaces_current",
    "monitoring_inputs_ready",
    "third_cycle_blockers_cleared",
    "third_cycle_scheduled",
    "owner_readiness_acknowledged",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_THIRD_CYCLE_READINESS_FIELDS = {
    "accepted_risk_detail",
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
    "raw_accepted_risk",
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
    "raw_monitoring_input",
    "raw_public_status",
    "raw_public_surface",
    "raw_readiness",
    "raw_redaction",
    "raw_remediated_state",
    "raw_remediation",
    "raw_review",
    "raw_risk",
    "raw_schedule",
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


def build_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness_packet(
    second_cycle_drift_remediation_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    second_cycle_drift_remediation_closeout = (
        second_cycle_drift_remediation_closeout_packet
        or build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    second_cycle_drift_remediation_closeout_result = (
        validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
            second_cycle_drift_remediation_closeout,
            require_live=evidence_mode == "live",
        )
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_THIRD_CYCLE_READINESS_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "monitoring_third_cycle_readiness_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-monitoring-third-cycle-readiness"
        ),
        "second_cycle_drift_remediation_closeout_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout/r7"
        ),
        "second_cycle_drift_remediation_closeout_result": second_cycle_drift_remediation_closeout_result,
        "third_cycle_owner_refs": {
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
        "third_cycle_readiness_contract": {
            "third_cycle_readiness_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/readiness"
            ),
            "source_second_cycle_drift_remediation_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/source-drift-remediation"
            ),
            "remediated_state_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/remediated-state"
            ),
            "accepted_risk_boundary_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/accepted-risk-boundary"
            ),
            "public_surface_currency_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/public-surface-currency"
            ),
            "monitoring_input_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/monitoring-input"
            ),
            "third_cycle_blocker_status_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/blocker-status"
            ),
            "third_cycle_schedule_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/schedule"
            ),
            "owner_readiness_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/owner-readiness"
            ),
            "redaction_status": "sanitized",
        },
        "remediated_state_refs": {
            "remediated_drift_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/state/remediated-drift"
            ),
            "no_open_critical_drift_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/state/no-critical-drift"
            ),
            "deferred_items_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/state/deferred-items"
            ),
            "remediation_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/state/remediation-owner"
            ),
        },
        "accepted_risk_boundary_refs": {
            "accepted_risk_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/risk/register"
            ),
            "accepted_risk_expiry_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/risk/expiry-review"
            ),
            "risk_owner_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/risk/owner-ack"
            ),
            "public_boundary_assertion_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/risk/public-boundary"
            ),
        },
        "public_surface_currency_refs": {
            "public_scorecard_current_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/public/scorecard-current"
            ),
            "public_status_summary_current_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/public/summary-current"
            ),
            "readme_status_current_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/public/readme-current"
            ),
            "wiki_status_current_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/public/wiki-current"
            ),
        },
        "monitoring_input_refs": {
            "scorecard_health_input_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/input/scorecard-health"
            ),
            "link_health_input_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/input/link-health"
            ),
            "archive_freshness_input_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/input/archive-freshness"
            ),
            "redaction_posture_input_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/input/redaction-posture"
            ),
        },
        "third_cycle_blocker_refs": {
            "blocker_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/blocker/register"
            ),
            "no_unassigned_blockers_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/blocker/no-unassigned"
            ),
            "no_unresolved_critical_blockers_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/blocker/no-critical"
            ),
            "third_cycle_go_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/blocker/go"
            ),
        },
        "third_cycle_schedule_refs": {
            "third_cycle_start_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/schedule/start"
            ),
            "weekly_review_schedule_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/schedule/weekly-review"
            ),
            "monthly_audit_schedule_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/schedule/monthly-audit"
            ),
            "quarterly_refresh_schedule_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/schedule/quarterly-refresh"
            ),
        },
        "owner_readiness_ack_refs": {
            "operations_readiness_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/ack/operations"
            ),
            "security_readiness_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/ack/security"
            ),
            "communications_readiness_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/ack/communications"
            ),
            "audit_readiness_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/ack/audit"
            ),
        },
        "ci_gate_coverage": {
            "source_second_cycle_drift_remediation_closeout_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-third-cycle-readiness/source-validation"
            ),
            "remediated_state_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-third-cycle-readiness/state-validation"
            ),
            "accepted_risk_boundary_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-third-cycle-readiness/risk-validation"
            ),
            "public_surface_currency_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-third-cycle-readiness/public-surface-validation"
            ),
            "monitoring_input_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-third-cycle-readiness/input-validation"
            ),
            "third_cycle_blocker_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-third-cycle-readiness/blocker-validation"
            ),
            "third_cycle_schedule_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-third-cycle-readiness/schedule-validation"
            ),
            "owner_readiness_ack_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-third-cycle-readiness/owner-ack-validation"
            ),
        },
        "third_cycle_readiness_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/source-drift-remediation",
            f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/remediated-state",
            f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/accepted-risk-boundary",
            f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/public-surface-currency",
            f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/monitoring-input",
            f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/blocker-status",
            f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/schedule",
            f"{prefix}://phase8/public-scorecard-monitoring-third-cycle-readiness/owner-readiness",
        ],
        "third_cycle_readiness_controls": {
            "second_cycle_drift_remediation_closeout_ready": second_cycle_drift_remediation_closeout_result["blocker_count"] == 0,
            "remediated_state_ready": True,
            "accepted_risks_bounded": True,
            "public_surfaces_current": True,
            "monitoring_inputs_ready": True,
            "third_cycle_blockers_cleared": True,
            "third_cycle_scheduled": True,
            "owner_readiness_acknowledged": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_THIRD_CYCLE_READINESS_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard monitoring third-cycle readiness schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("second_cycle_drift_remediation_closeout_ref"), checks, "second_cycle_drift_remediation_closeout_ref")
    _check_second_cycle_drift_remediation_closeout_result(
        packet.get("second_cycle_drift_remediation_closeout_result", {}),
        checks,
        require_live=require_live,
    )
    _check_required_refs(
        packet.get("third_cycle_owner_refs", {}),
        REQUIRED_THIRD_CYCLE_OWNER_REFS,
        checks,
        "third_cycle_owner_refs",
    )
    _check_third_cycle_readiness_contract(packet.get("third_cycle_readiness_contract", {}), checks)
    _check_required_refs(
        packet.get("remediated_state_refs", {}),
        REQUIRED_REMEDIATED_STATE_REFS,
        checks,
        "remediated_state_refs",
    )
    _check_required_refs(
        packet.get("accepted_risk_boundary_refs", {}),
        REQUIRED_ACCEPTED_RISK_BOUNDARY_REFS,
        checks,
        "accepted_risk_boundary_refs",
    )
    _check_required_refs(
        packet.get("public_surface_currency_refs", {}),
        REQUIRED_PUBLIC_SURFACE_CURRENCY_REFS,
        checks,
        "public_surface_currency_refs",
    )
    _check_required_refs(
        packet.get("monitoring_input_refs", {}),
        REQUIRED_MONITORING_INPUT_REFS,
        checks,
        "monitoring_input_refs",
    )
    _check_required_refs(
        packet.get("third_cycle_blocker_refs", {}),
        REQUIRED_THIRD_CYCLE_BLOCKER_REFS,
        checks,
        "third_cycle_blocker_refs",
    )
    _check_required_refs(
        packet.get("third_cycle_schedule_refs", {}),
        REQUIRED_THIRD_CYCLE_SCHEDULE_REFS,
        checks,
        "third_cycle_schedule_refs",
    )
    _check_required_refs(
        packet.get("owner_readiness_ack_refs", {}),
        REQUIRED_OWNER_READINESS_ACK_REFS,
        checks,
        "owner_readiness_ack_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(
        packet.get("third_cycle_readiness_evidence_refs", []),
        checks,
        "third_cycle_readiness_evidence_refs",
        min_count=8,
    )
    _check_controls(packet.get("third_cycle_readiness_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_third_cycle_readiness_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard monitoring third-cycle readiness contains sanitized refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_THIRD_CYCLE_READINESS_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness_packet(
        sample
    )
    live_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-third-cycle-readiness.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-third-cycle-readiness.live.sanitized.example.json",
        "sample_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-third-cycle-readiness.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-third-cycle-readiness.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-third-cycle-readiness.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_third_cycle_readiness"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 third-cycle readiness supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 third-cycle readiness validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Third-cycle readiness requires evidence_mode=live and sanitized=true.",
        )


def _check_second_cycle_drift_remediation_closeout_result(
    result: Any,
    checks: list[dict[str, str]],
    *,
    require_live: bool,
) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "second_cycle_drift_remediation_closeout_result",
            "blocker",
            "second_cycle_drift_remediation_closeout_result must be an object.",
        )
        return
    ready = (
        result.get(
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"
        )
        is True
    )
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(
            checks,
            "second_cycle_drift_remediation_closeout_result",
            "pass",
            "Source second-cycle drift remediation closeout is ready.",
        )
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "second_cycle_drift_remediation_closeout_result",
            "warn",
            "Source second-cycle drift remediation closeout validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "second_cycle_drift_remediation_closeout_result",
            "blocker",
            "Source second-cycle drift remediation closeout is not ready.",
        )


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


def _check_third_cycle_readiness_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(
            checks,
            "third_cycle_readiness_contract",
            "blocker",
            "third_cycle_readiness_contract must be an object.",
        )
        return
    missing = sorted(field for field in REQUIRED_THIRD_CYCLE_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_THIRD_CYCLE_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "third_cycle_readiness_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard third-cycle readiness contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard third-cycle readiness contract invalid: "
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
        _add_check(
            checks,
            "third_cycle_readiness_controls",
            "blocker",
            "third_cycle_readiness_controls must be an object.",
        )
        return
    missing = sorted(control for control in REQUIRED_THIRD_CYCLE_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "third_cycle_readiness_controls",
        "pass" if not missing else "blocker",
        "Public scorecard third-cycle readiness controls are explicit."
        if not missing
        else f"Public scorecard third-cycle readiness controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_third_cycle_readiness_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_THIRD_CYCLE_READINESS_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_third_cycle_readiness_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_third_cycle_readiness_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
