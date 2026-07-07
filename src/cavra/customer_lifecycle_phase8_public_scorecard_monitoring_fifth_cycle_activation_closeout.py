from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_readiness_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIFTH_CYCLE_ACTIVATION_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-activation-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIFTH_CYCLE_ACTIVATION_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-activation-closeout.result.v1"
)

REQUIRED_FIFTH_CYCLE_ACTIVATION_OWNER_REFS = {
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

REQUIRED_FIFTH_CYCLE_ACTIVATION_CONTRACT_FIELDS = {
    "fifth_cycle_activation_closeout_ref",
    "source_fifth_cycle_readiness_ref",
    "cycle_start_ref",
    "initial_signal_capture_ref",
    "monitor_run_ref",
    "alert_route_check_ref",
    "evidence_archive_ref",
    "owner_activation_ack_ref",
    "redaction_status",
}

REQUIRED_CYCLE_START_REFS = {
    "activation_window_ref",
    "fifth_cycle_start_decision_ref",
    "operating_calendar_ref",
    "review_cadence_start_ref",
}

REQUIRED_INITIAL_SIGNAL_REFS = {
    "scorecard_health_signal_ref",
    "link_health_signal_ref",
    "archive_freshness_signal_ref",
    "redaction_posture_signal_ref",
}

REQUIRED_MONITOR_RUN_REFS = {
    "scorecard_monitor_run_ref",
    "link_monitor_run_ref",
    "archive_monitor_run_ref",
    "redaction_monitor_run_ref",
}

REQUIRED_ALERT_ROUTE_CHECK_REFS = {
    "alert_route_smoke_test_ref",
    "escalation_route_ack_ref",
    "on_call_ack_ref",
    "no_dead_route_ref",
}

REQUIRED_ACTIVATION_ARCHIVE_REFS = {
    "activation_manifest_ref",
    "initial_signal_archive_ref",
    "monitor_run_archive_ref",
    "alert_route_archive_ref",
    "immutable_activation_archive_ref",
}

REQUIRED_OWNER_ACTIVATION_ACK_REFS = {
    "operations_activation_ack_ref",
    "security_activation_ack_ref",
    "communications_activation_ack_ref",
    "audit_activation_ack_ref",
}

REQUIRED_CI_GATES = {
    "source_fifth_cycle_readiness_validation",
    "cycle_start_validation",
    "initial_signal_capture_validation",
    "monitor_run_validation",
    "alert_route_check_validation",
    "evidence_archive_validation",
    "owner_activation_ack_validation",
    "public_safe_activation_validation",
}

REQUIRED_FIFTH_CYCLE_ACTIVATION_CONTROLS = {
    "fifth_cycle_readiness_ready",
    "cycle_started",
    "initial_signals_captured",
    "monitors_ran",
    "alert_routes_checked",
    "activation_archive_complete",
    "owner_activation_acknowledged",
    "public_safe_activation_confirmed",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_FIFTH_CYCLE_ACTIVATION_FIELDS = {
    "accepted_risk_detail",
    "alert_payload",
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_health_score",
    "customer_name",
    "customer_score",
    "customer_status",
    "escalation_detail",
    "finding_detail",
    "legal_terms",
    "monitor_payload",
    "private_note",
    "pricing",
    "raw_activation",
    "raw_alert",
    "raw_alert_route",
    "raw_archive",
    "raw_audit",
    "raw_blocker",
    "raw_contract",
    "raw_drift",
    "raw_evidence",
    "raw_escalation",
    "raw_finding",
    "raw_health",
    "raw_link_check",
    "raw_monitor",
    "raw_monitor_run",
    "raw_on_call",
    "raw_public_status",
    "raw_readiness",
    "raw_redaction",
    "raw_remediation",
    "raw_review",
    "raw_risk",
    "raw_schedule",
    "raw_score",
    "raw_scorecard",
    "raw_signal",
    "raw_status",
    "recipient_email",
    "remediation_detail",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout_packet(
    fifth_cycle_readiness_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    fifth_cycle_readiness = (
        fifth_cycle_readiness_packet
        or build_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_readiness_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    fifth_cycle_readiness_result = (
        validate_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_readiness_packet(
            fifth_cycle_readiness,
            require_live=evidence_mode == "live",
        )
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIFTH_CYCLE_ACTIVATION_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "monitoring_fifth_cycle_activation_closeout_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-activation-closeout"
        ),
        "fifth_cycle_readiness_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-readiness/r7"
        ),
        "fifth_cycle_readiness_result": fifth_cycle_readiness_result,
        "fifth_cycle_activation_owner_refs": {
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
        "fifth_cycle_activation_contract": {
            "fifth_cycle_activation_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/closeout"
            ),
            "source_fifth_cycle_readiness_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/source-readiness"
            ),
            "cycle_start_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/cycle-start"
            ),
            "initial_signal_capture_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/initial-signals"
            ),
            "monitor_run_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/monitor-run"
            ),
            "alert_route_check_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/alert-routes"
            ),
            "evidence_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/archive"
            ),
            "owner_activation_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/owner-activation"
            ),
            "redaction_status": "sanitized",
        },
        "cycle_start_refs": {
            "activation_window_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/start/window"
            ),
            "fifth_cycle_start_decision_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/start/decision"
            ),
            "operating_calendar_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/start/calendar"
            ),
            "review_cadence_start_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/start/cadence"
            ),
        },
        "initial_signal_refs": {
            "scorecard_health_signal_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/signal/scorecard-health"
            ),
            "link_health_signal_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/signal/link-health"
            ),
            "archive_freshness_signal_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/signal/archive-freshness"
            ),
            "redaction_posture_signal_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/signal/redaction-posture"
            ),
        },
        "monitor_run_refs": {
            "scorecard_monitor_run_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/monitor/scorecard"
            ),
            "link_monitor_run_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/monitor/link"
            ),
            "archive_monitor_run_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/monitor/archive"
            ),
            "redaction_monitor_run_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/monitor/redaction"
            ),
        },
        "alert_route_check_refs": {
            "alert_route_smoke_test_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/alert/smoke-test"
            ),
            "escalation_route_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/alert/escalation-ack"
            ),
            "on_call_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/alert/on-call-ack"
            ),
            "no_dead_route_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/alert/no-dead-route"
            ),
        },
        "activation_archive_refs": {
            "activation_manifest_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/archive/manifest"
            ),
            "initial_signal_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/archive/initial-signals"
            ),
            "monitor_run_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/archive/monitor-runs"
            ),
            "alert_route_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/archive/alert-routes"
            ),
            "immutable_activation_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/archive/immutable"
            ),
        },
        "owner_activation_ack_refs": {
            "operations_activation_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/ack/operations"
            ),
            "security_activation_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/ack/security"
            ),
            "communications_activation_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/ack/communications"
            ),
            "audit_activation_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/ack/audit"
            ),
        },
        "ci_gate_coverage": {
            "source_fifth_cycle_readiness_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/source-validation"
            ),
            "cycle_start_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/cycle-start-validation"
            ),
            "initial_signal_capture_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/signal-validation"
            ),
            "monitor_run_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/monitor-validation"
            ),
            "alert_route_check_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/alert-route-validation"
            ),
            "evidence_archive_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/archive-validation"
            ),
            "owner_activation_ack_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/owner-ack-validation"
            ),
            "public_safe_activation_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/public-safe-validation"
            ),
        },
        "fifth_cycle_activation_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/source-readiness",
            f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/cycle-start",
            f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/initial-signals",
            f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/monitor-runs",
            f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/alert-routes",
            f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/archive",
            f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/owner-activation",
            f"{prefix}://phase8/public-scorecard-monitoring-fifth-cycle-activation-closeout/public-safe-closeout",
        ],
        "fifth_cycle_activation_controls": {
            "fifth_cycle_readiness_ready": fifth_cycle_readiness_result["blocker_count"] == 0,
            "cycle_started": True,
            "initial_signals_captured": True,
            "monitors_ran": True,
            "alert_routes_checked": True,
            "activation_archive_complete": True,
            "owner_activation_acknowledged": True,
            "public_safe_activation_confirmed": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIFTH_CYCLE_ACTIVATION_CLOSEOUT_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard monitoring fifth-cycle activation closeout schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("fifth_cycle_readiness_ref"), checks, "fifth_cycle_readiness_ref")
    _check_fifth_cycle_readiness_result(
        packet.get("fifth_cycle_readiness_result", {}),
        checks,
        require_live=require_live,
    )
    _check_required_refs(
        packet.get("fifth_cycle_activation_owner_refs", {}),
        REQUIRED_FIFTH_CYCLE_ACTIVATION_OWNER_REFS,
        checks,
        "fifth_cycle_activation_owner_refs",
    )
    _check_fifth_cycle_activation_contract(packet.get("fifth_cycle_activation_contract", {}), checks)
    _check_required_refs(
        packet.get("cycle_start_refs", {}),
        REQUIRED_CYCLE_START_REFS,
        checks,
        "cycle_start_refs",
    )
    _check_required_refs(
        packet.get("initial_signal_refs", {}),
        REQUIRED_INITIAL_SIGNAL_REFS,
        checks,
        "initial_signal_refs",
    )
    _check_required_refs(
        packet.get("monitor_run_refs", {}),
        REQUIRED_MONITOR_RUN_REFS,
        checks,
        "monitor_run_refs",
    )
    _check_required_refs(
        packet.get("alert_route_check_refs", {}),
        REQUIRED_ALERT_ROUTE_CHECK_REFS,
        checks,
        "alert_route_check_refs",
    )
    _check_required_refs(
        packet.get("activation_archive_refs", {}),
        REQUIRED_ACTIVATION_ARCHIVE_REFS,
        checks,
        "activation_archive_refs",
    )
    _check_required_refs(
        packet.get("owner_activation_ack_refs", {}),
        REQUIRED_OWNER_ACTIVATION_ACK_REFS,
        checks,
        "owner_activation_ack_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(
        packet.get("fifth_cycle_activation_evidence_refs", []),
        checks,
        "fifth_cycle_activation_evidence_refs",
        min_count=8,
    )
    _check_controls(packet.get("fifth_cycle_activation_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_fifth_cycle_activation_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard monitoring fifth-cycle activation closeout contains sanitized refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIFTH_CYCLE_ACTIVATION_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout_packet(
        sample
    )
    live_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-activation-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-activation-closeout.live.sanitized.example.json",
        "sample_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-activation-closeout.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-activation-closeout.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-fifth-cycle-activation-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_activation_closeout"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 fifth-cycle activation closeout supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 fifth-cycle activation validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Fifth-cycle activation closeout requires evidence_mode=live and sanitized=true.",
        )


def _check_fifth_cycle_readiness_result(
    result: Any,
    checks: list[dict[str, str]],
    *,
    require_live: bool,
) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "fifth_cycle_readiness_result",
            "blocker",
            "fifth_cycle_readiness_result must be an object.",
        )
        return
    ready = (
        result.get(
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fifth_cycle_readiness"
        )
        is True
    )
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "fifth_cycle_readiness_result", "pass", "Source fifth-cycle readiness is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "fifth_cycle_readiness_result",
            "warn",
            "Source fifth-cycle readiness validates shape but is not live.",
        )
    else:
        _add_check(checks, "fifth_cycle_readiness_result", "blocker", "Source fifth-cycle readiness is not ready.")


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


def _check_fifth_cycle_activation_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(
            checks,
            "fifth_cycle_activation_contract",
            "blocker",
            "fifth_cycle_activation_contract must be an object.",
        )
        return
    missing = sorted(field for field in REQUIRED_FIFTH_CYCLE_ACTIVATION_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_FIFTH_CYCLE_ACTIVATION_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "fifth_cycle_activation_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard fifth-cycle activation closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard fifth-cycle activation closeout contract invalid: "
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
            "fifth_cycle_activation_controls",
            "blocker",
            "fifth_cycle_activation_controls must be an object.",
        )
        return
    missing = sorted(
        control for control in REQUIRED_FIFTH_CYCLE_ACTIVATION_CONTROLS if controls.get(control) is not True
    )
    _add_check(
        checks,
        "fifth_cycle_activation_controls",
        "pass" if not missing else "blocker",
        "Public scorecard fifth-cycle activation closeout controls are explicit."
        if not missing
        else f"Public scorecard fifth-cycle activation closeout controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_fifth_cycle_activation_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_FIFTH_CYCLE_ACTIVATION_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_fifth_cycle_activation_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_fifth_cycle_activation_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
