from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_ACTIVATION_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_ACTIVATION_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout.result.v1"
)

REQUIRED_ACTIVATION_OWNER_REFS = {
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

REQUIRED_ACTIVATION_CONTRACT_FIELDS = {
    "monitoring_activation_closeout_ref",
    "source_continuous_monitoring_readiness_ref",
    "scorecard_health_activation_ref",
    "link_health_activation_ref",
    "archive_freshness_activation_ref",
    "redaction_posture_activation_ref",
    "alert_route_activation_ref",
    "review_cadence_start_ref",
    "first_monitor_snapshot_ref",
    "escalation_ownership_acceptance_ref",
    "redaction_status",
}

REQUIRED_ACTIVATED_MONITOR_REFS = {
    "scorecard_health_monitor_active_ref",
    "link_health_monitor_active_ref",
    "archive_freshness_monitor_active_ref",
    "redaction_posture_monitor_active_ref",
    "public_boundary_monitor_active_ref",
}

REQUIRED_ALERT_ROUTE_REFS = {
    "operations_alert_route_active_ref",
    "security_alert_route_active_ref",
    "communications_alert_route_active_ref",
    "executive_escalation_route_active_ref",
}

REQUIRED_CADENCE_START_REFS = {
    "weekly_health_review_started_ref",
    "monthly_audit_review_scheduled_ref",
    "quarterly_scorecard_refresh_scheduled_ref",
    "cadence_owner_ack_ref",
}

REQUIRED_FIRST_SNAPSHOT_REFS = {
    "scorecard_health_snapshot_ref",
    "link_health_snapshot_ref",
    "archive_freshness_snapshot_ref",
    "redaction_posture_snapshot_ref",
    "immutable_snapshot_archive_ref",
}

REQUIRED_ESCALATION_ACCEPTANCE_REFS = {
    "broken_link_owner_acceptance_ref",
    "stale_scorecard_owner_acceptance_ref",
    "archive_drift_owner_acceptance_ref",
    "redaction_regression_owner_acceptance_ref",
}

REQUIRED_OPERATIONAL_CLOSEOUT_REFS = {
    "monitoring_runbook_ref",
    "oncall_rotation_ref",
    "public_status_update_ref",
    "audit_handoff_ref",
}

REQUIRED_CI_GATES = {
    "source_continuous_monitoring_readiness_validation",
    "monitor_activation_validation",
    "alert_route_activation_validation",
    "cadence_start_validation",
    "snapshot_archive_validation",
    "escalation_acceptance_validation",
    "operational_closeout_validation",
    "redaction_boundary_validation",
}

REQUIRED_ACTIVATION_CONTROLS = {
    "continuous_monitoring_readiness_ready",
    "monitors_activated",
    "alert_routes_activated",
    "review_cadence_started",
    "first_monitor_snapshot_archived",
    "escalation_ownership_accepted",
    "operational_closeout_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_MONITORING_ACTIVATION_FIELDS = {
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
    "raw_contract",
    "raw_evidence",
    "raw_health",
    "raw_link_check",
    "raw_monitor",
    "raw_oncall",
    "raw_redaction",
    "raw_review",
    "raw_route",
    "raw_runbook",
    "raw_score",
    "raw_scorecard",
    "raw_snapshot",
    "raw_status",
    "recipient_email",
    "remediation_detail",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
    continuous_monitoring_readiness_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    continuous_monitoring_readiness = (
        continuous_monitoring_readiness_packet
        or build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    continuous_monitoring_readiness_result = (
        validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
            continuous_monitoring_readiness,
            require_live=evidence_mode == "live",
        )
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_ACTIVATION_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "monitoring_activation_closeout_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout"
        ),
        "continuous_monitoring_readiness_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness/r7"
        ),
        "continuous_monitoring_readiness_result": continuous_monitoring_readiness_result,
        "activation_owner_refs": {
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
        "activation_contract": {
            "monitoring_activation_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/closeout"
            ),
            "source_continuous_monitoring_readiness_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/source-readiness"
            ),
            "scorecard_health_activation_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/scorecard-health-activation"
            ),
            "link_health_activation_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/link-health-activation"
            ),
            "archive_freshness_activation_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/archive-freshness-activation"
            ),
            "redaction_posture_activation_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/redaction-posture-activation"
            ),
            "alert_route_activation_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/alert-route-activation"
            ),
            "review_cadence_start_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/review-cadence-start"
            ),
            "first_monitor_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/first-monitor-snapshot"
            ),
            "escalation_ownership_acceptance_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/escalation-ownership"
            ),
            "redaction_status": "sanitized",
        },
        "activated_monitor_refs": {
            "scorecard_health_monitor_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/monitor/scorecard-health-active"
            ),
            "link_health_monitor_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/monitor/link-health-active"
            ),
            "archive_freshness_monitor_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/monitor/archive-freshness-active"
            ),
            "redaction_posture_monitor_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/monitor/redaction-posture-active"
            ),
            "public_boundary_monitor_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/monitor/public-boundary-active"
            ),
        },
        "alert_route_refs": {
            "operations_alert_route_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/alert/operations-active"
            ),
            "security_alert_route_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/alert/security-active"
            ),
            "communications_alert_route_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/alert/communications-active"
            ),
            "executive_escalation_route_active_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/alert/executive-active"
            ),
        },
        "cadence_start_refs": {
            "weekly_health_review_started_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/cadence/weekly-started"
            ),
            "monthly_audit_review_scheduled_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/cadence/monthly-scheduled"
            ),
            "quarterly_scorecard_refresh_scheduled_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/cadence/quarterly-scheduled"
            ),
            "cadence_owner_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/cadence/owner-ack"
            ),
        },
        "first_snapshot_refs": {
            "scorecard_health_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/snapshot/scorecard-health"
            ),
            "link_health_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/snapshot/link-health"
            ),
            "archive_freshness_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/snapshot/archive-freshness"
            ),
            "redaction_posture_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/snapshot/redaction-posture"
            ),
            "immutable_snapshot_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/snapshot/immutable-archive"
            ),
        },
        "escalation_acceptance_refs": {
            "broken_link_owner_acceptance_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/escalation/broken-link-owner"
            ),
            "stale_scorecard_owner_acceptance_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/escalation/stale-scorecard-owner"
            ),
            "archive_drift_owner_acceptance_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/escalation/archive-drift-owner"
            ),
            "redaction_regression_owner_acceptance_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/escalation/redaction-owner"
            ),
        },
        "operational_closeout_refs": {
            "monitoring_runbook_ref": f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/runbook",
            "oncall_rotation_ref": f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/oncall",
            "public_status_update_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/public-status-update"
            ),
            "audit_handoff_ref": f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/audit-handoff",
        },
        "ci_gate_coverage": {
            "source_continuous_monitoring_readiness_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-activation-closeout/source-readiness-validation"
            ),
            "monitor_activation_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-activation-closeout/monitor-activation-validation"
            ),
            "alert_route_activation_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-activation-closeout/alert-route-validation"
            ),
            "cadence_start_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-activation-closeout/cadence-start-validation"
            ),
            "snapshot_archive_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-activation-closeout/snapshot-validation"
            ),
            "escalation_acceptance_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-activation-closeout/escalation-validation"
            ),
            "operational_closeout_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-activation-closeout/operational-closeout-validation"
            ),
            "redaction_boundary_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-activation-closeout/redaction-boundary-validation"
            ),
        },
        "activation_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/source-readiness",
            f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/activated-monitors",
            f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/alert-routes",
            f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/cadence-start",
            f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/first-snapshot",
            f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/escalation-acceptance",
            f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/operational-closeout",
            f"{prefix}://phase8/public-scorecard-monitoring-activation-closeout/redaction-boundary",
        ],
        "activation_controls": {
            "continuous_monitoring_readiness_ready": continuous_monitoring_readiness_result["blocker_count"] == 0,
            "monitors_activated": True,
            "alert_routes_activated": True,
            "review_cadence_started": True,
            "first_monitor_snapshot_archived": True,
            "escalation_ownership_accepted": True,
            "operational_closeout_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_ACTIVATION_CLOSEOUT_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard monitoring activation closeout schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("continuous_monitoring_readiness_ref"), checks, "continuous_monitoring_readiness_ref")
    _check_continuous_monitoring_readiness_result(
        packet.get("continuous_monitoring_readiness_result", {}),
        checks,
        require_live=require_live,
    )
    _check_required_refs(packet.get("activation_owner_refs", {}), REQUIRED_ACTIVATION_OWNER_REFS, checks, "activation_owner_refs")
    _check_activation_contract(packet.get("activation_contract", {}), checks)
    _check_required_refs(
        packet.get("activated_monitor_refs", {}),
        REQUIRED_ACTIVATED_MONITOR_REFS,
        checks,
        "activated_monitor_refs",
    )
    _check_required_refs(packet.get("alert_route_refs", {}), REQUIRED_ALERT_ROUTE_REFS, checks, "alert_route_refs")
    _check_required_refs(packet.get("cadence_start_refs", {}), REQUIRED_CADENCE_START_REFS, checks, "cadence_start_refs")
    _check_required_refs(packet.get("first_snapshot_refs", {}), REQUIRED_FIRST_SNAPSHOT_REFS, checks, "first_snapshot_refs")
    _check_required_refs(
        packet.get("escalation_acceptance_refs", {}),
        REQUIRED_ESCALATION_ACCEPTANCE_REFS,
        checks,
        "escalation_acceptance_refs",
    )
    _check_required_refs(
        packet.get("operational_closeout_refs", {}),
        REQUIRED_OPERATIONAL_CLOSEOUT_REFS,
        checks,
        "operational_closeout_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("activation_evidence_refs", []), checks, "activation_evidence_refs", min_count=8)
    _check_controls(packet.get("activation_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_monitoring_activation_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard monitoring activation closeout contains sanitized refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_ACTIVATION_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout.live.sanitized.example.json",
        "sample_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 monitoring activation closeout supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 monitoring activation closeout validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Activation closeout requires evidence_mode=live and sanitized=true.")


def _check_continuous_monitoring_readiness_result(
    result: Any,
    checks: list[dict[str, str]],
    *,
    require_live: bool,
) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "continuous_monitoring_readiness_result",
            "blocker",
            "continuous_monitoring_readiness_result must be an object.",
        )
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(
            checks,
            "continuous_monitoring_readiness_result",
            "pass",
            "Source public scorecard continuous monitoring readiness is ready.",
        )
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "continuous_monitoring_readiness_result",
            "warn",
            "Source public scorecard continuous monitoring readiness validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "continuous_monitoring_readiness_result",
            "blocker",
            "Source public scorecard continuous monitoring readiness is not ready.",
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


def _check_activation_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "activation_contract", "blocker", "activation_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_ACTIVATION_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_ACTIVATION_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "activation_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard monitoring activation closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard monitoring activation closeout contract invalid: "
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
        _add_check(checks, "activation_controls", "blocker", "activation_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_ACTIVATION_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "activation_controls",
        "pass" if not missing else "blocker",
        "Public scorecard monitoring activation closeout controls are explicit."
        if not missing
        else f"Public scorecard monitoring activation closeout controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_monitoring_activation_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_MONITORING_ACTIVATION_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_monitoring_activation_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_monitoring_activation_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
