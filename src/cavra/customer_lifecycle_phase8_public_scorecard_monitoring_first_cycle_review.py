from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIRST_CYCLE_REVIEW_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIRST_CYCLE_REVIEW_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.result.v1"
)

REQUIRED_FIRST_CYCLE_OWNER_REFS = {
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

REQUIRED_FIRST_CYCLE_CONTRACT_FIELDS = {
    "first_cycle_review_ref",
    "source_monitoring_activation_closeout_ref",
    "cycle_window_ref",
    "findings_triage_ref",
    "alert_review_ref",
    "snapshot_archive_ref",
    "public_status_refresh_ref",
    "followup_owner_assignment_ref",
    "next_cycle_schedule_ref",
    "redaction_status",
}

REQUIRED_CYCLE_WINDOW_REFS = {
    "first_cycle_started_ref",
    "first_cycle_completed_ref",
    "review_window_ref",
    "reviewer_owner_ref",
}

REQUIRED_FINDINGS_TRIAGE_REFS = {
    "findings_register_review_ref",
    "blocker_triage_ref",
    "drift_triage_ref",
    "accepted_risk_triage_ref",
}

REQUIRED_ALERT_REVIEW_REFS = {
    "operations_alert_review_ref",
    "security_alert_review_ref",
    "communications_alert_review_ref",
    "executive_escalation_review_ref",
}

REQUIRED_SNAPSHOT_ARCHIVE_REFS = {
    "first_cycle_health_snapshot_ref",
    "first_cycle_link_snapshot_ref",
    "first_cycle_redaction_snapshot_ref",
    "first_cycle_archive_snapshot_ref",
    "immutable_cycle_archive_ref",
}

REQUIRED_PUBLIC_STATUS_REFRESH_REFS = {
    "public_scorecard_refresh_ref",
    "public_status_page_refresh_ref",
    "readme_status_refresh_ref",
    "wiki_status_refresh_ref",
}

REQUIRED_FOLLOWUP_OWNER_REFS = {
    "broken_link_followup_owner_ref",
    "stale_scorecard_followup_owner_ref",
    "archive_drift_followup_owner_ref",
    "redaction_regression_followup_owner_ref",
}

REQUIRED_NEXT_CYCLE_SCHEDULE_REFS = {
    "next_weekly_health_review_ref",
    "next_monthly_audit_review_ref",
    "next_quarterly_scorecard_refresh_ref",
    "next_cycle_owner_ack_ref",
}

REQUIRED_CI_GATES = {
    "source_monitoring_activation_closeout_validation",
    "cycle_window_validation",
    "findings_triage_validation",
    "alert_review_validation",
    "snapshot_archive_validation",
    "public_status_refresh_validation",
    "followup_owner_validation",
    "next_cycle_schedule_validation",
}

REQUIRED_FIRST_CYCLE_CONTROLS = {
    "monitoring_activation_closeout_ready",
    "first_cycle_completed",
    "findings_triaged",
    "alerts_reviewed",
    "snapshots_archived",
    "public_status_refreshed",
    "followup_owners_assigned",
    "next_cycle_scheduled",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_FIRST_CYCLE_FIELDS = {
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
    "raw_cycle",
    "raw_evidence",
    "raw_finding",
    "raw_health",
    "raw_link_check",
    "raw_monitor",
    "raw_page",
    "raw_public_status",
    "raw_redaction",
    "raw_review",
    "raw_score",
    "raw_scorecard",
    "raw_snapshot",
    "raw_status",
    "raw_triage",
    "recipient_email",
    "remediation_detail",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
    monitoring_activation_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    monitoring_activation_closeout = (
        monitoring_activation_closeout_packet
        or build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    monitoring_activation_closeout_result = (
        validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
            monitoring_activation_closeout,
            require_live=evidence_mode == "live",
        )
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIRST_CYCLE_REVIEW_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "monitoring_first_cycle_review_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review"
        ),
        "monitoring_activation_closeout_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout/r7"
        ),
        "monitoring_activation_closeout_result": monitoring_activation_closeout_result,
        "first_cycle_owner_refs": {
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
        "first_cycle_contract": {
            "first_cycle_review_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/review",
            "source_monitoring_activation_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/source-activation-closeout"
            ),
            "cycle_window_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/cycle-window",
            "findings_triage_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/findings-triage",
            "alert_review_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/alert-review",
            "snapshot_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/snapshot-archive"
            ),
            "public_status_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/public-status-refresh"
            ),
            "followup_owner_assignment_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/followup-owner-assignment"
            ),
            "next_cycle_schedule_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/next-cycle-schedule"
            ),
            "redaction_status": "sanitized",
        },
        "cycle_window_refs": {
            "first_cycle_started_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/cycle/started",
            "first_cycle_completed_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/cycle/completed"
            ),
            "review_window_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/cycle/review-window",
            "reviewer_owner_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/cycle/reviewer",
        },
        "findings_triage_refs": {
            "findings_register_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/findings/register-review"
            ),
            "blocker_triage_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/findings/blockers",
            "drift_triage_ref": f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/findings/drift",
            "accepted_risk_triage_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/findings/accepted-risk"
            ),
        },
        "alert_review_refs": {
            "operations_alert_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/alerts/operations"
            ),
            "security_alert_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/alerts/security"
            ),
            "communications_alert_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/alerts/communications"
            ),
            "executive_escalation_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/alerts/executive"
            ),
        },
        "snapshot_archive_refs": {
            "first_cycle_health_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/snapshot/health"
            ),
            "first_cycle_link_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/snapshot/link-health"
            ),
            "first_cycle_redaction_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/snapshot/redaction"
            ),
            "first_cycle_archive_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/snapshot/archive"
            ),
            "immutable_cycle_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/snapshot/immutable"
            ),
        },
        "public_status_refresh_refs": {
            "public_scorecard_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/status/scorecard-refresh"
            ),
            "public_status_page_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/status/page-refresh"
            ),
            "readme_status_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/status/readme-refresh"
            ),
            "wiki_status_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/status/wiki-refresh"
            ),
        },
        "followup_owner_refs": {
            "broken_link_followup_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/followup/broken-link-owner"
            ),
            "stale_scorecard_followup_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/followup/stale-scorecard-owner"
            ),
            "archive_drift_followup_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/followup/archive-drift-owner"
            ),
            "redaction_regression_followup_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/followup/redaction-owner"
            ),
        },
        "next_cycle_schedule_refs": {
            "next_weekly_health_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/next/weekly-health"
            ),
            "next_monthly_audit_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/next/monthly-audit"
            ),
            "next_quarterly_scorecard_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/next/quarterly-refresh"
            ),
            "next_cycle_owner_ack_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/next/owner-ack"
            ),
        },
        "ci_gate_coverage": {
            "source_monitoring_activation_closeout_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-first-cycle-review/source-activation-validation"
            ),
            "cycle_window_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-first-cycle-review/cycle-window-validation"
            ),
            "findings_triage_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-first-cycle-review/findings-triage-validation"
            ),
            "alert_review_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-first-cycle-review/alert-review-validation"
            ),
            "snapshot_archive_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-first-cycle-review/snapshot-archive-validation"
            ),
            "public_status_refresh_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-first-cycle-review/public-status-validation"
            ),
            "followup_owner_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-first-cycle-review/followup-owner-validation"
            ),
            "next_cycle_schedule_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-first-cycle-review/next-cycle-validation"
            ),
        },
        "first_cycle_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/source-activation-closeout",
            f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/cycle-window",
            f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/findings-triage",
            f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/alert-review",
            f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/snapshot-archive",
            f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/public-status-refresh",
            f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/followup-owner-assignment",
            f"{prefix}://phase8/public-scorecard-monitoring-first-cycle-review/next-cycle-schedule",
        ],
        "first_cycle_controls": {
            "monitoring_activation_closeout_ready": monitoring_activation_closeout_result["blocker_count"] == 0,
            "first_cycle_completed": True,
            "findings_triaged": True,
            "alerts_reviewed": True,
            "snapshots_archived": True,
            "public_status_refreshed": True,
            "followup_owners_assigned": True,
            "next_cycle_scheduled": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIRST_CYCLE_REVIEW_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard monitoring first-cycle review schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("monitoring_activation_closeout_ref"), checks, "monitoring_activation_closeout_ref")
    _check_monitoring_activation_closeout_result(
        packet.get("monitoring_activation_closeout_result", {}),
        checks,
        require_live=require_live,
    )
    _check_required_refs(
        packet.get("first_cycle_owner_refs", {}),
        REQUIRED_FIRST_CYCLE_OWNER_REFS,
        checks,
        "first_cycle_owner_refs",
    )
    _check_first_cycle_contract(packet.get("first_cycle_contract", {}), checks)
    _check_required_refs(packet.get("cycle_window_refs", {}), REQUIRED_CYCLE_WINDOW_REFS, checks, "cycle_window_refs")
    _check_required_refs(
        packet.get("findings_triage_refs", {}),
        REQUIRED_FINDINGS_TRIAGE_REFS,
        checks,
        "findings_triage_refs",
    )
    _check_required_refs(packet.get("alert_review_refs", {}), REQUIRED_ALERT_REVIEW_REFS, checks, "alert_review_refs")
    _check_required_refs(
        packet.get("snapshot_archive_refs", {}),
        REQUIRED_SNAPSHOT_ARCHIVE_REFS,
        checks,
        "snapshot_archive_refs",
    )
    _check_required_refs(
        packet.get("public_status_refresh_refs", {}),
        REQUIRED_PUBLIC_STATUS_REFRESH_REFS,
        checks,
        "public_status_refresh_refs",
    )
    _check_required_refs(packet.get("followup_owner_refs", {}), REQUIRED_FOLLOWUP_OWNER_REFS, checks, "followup_owner_refs")
    _check_required_refs(
        packet.get("next_cycle_schedule_refs", {}),
        REQUIRED_NEXT_CYCLE_SCHEDULE_REFS,
        checks,
        "next_cycle_schedule_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("first_cycle_evidence_refs", []), checks, "first_cycle_evidence_refs", min_count=8)
    _check_controls(packet.get("first_cycle_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_first_cycle_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard monitoring first-cycle review contains sanitized refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_FIRST_CYCLE_REVIEW_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.live.sanitized.example.json",
        "sample_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 monitoring first-cycle review supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 monitoring first-cycle review validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "First-cycle review requires evidence_mode=live and sanitized=true.")


def _check_monitoring_activation_closeout_result(
    result: Any,
    checks: list[dict[str, str]],
    *,
    require_live: bool,
) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "monitoring_activation_closeout_result",
            "blocker",
            "monitoring_activation_closeout_result must be an object.",
        )
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(
            checks,
            "monitoring_activation_closeout_result",
            "pass",
            "Source public scorecard monitoring activation closeout is ready.",
        )
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "monitoring_activation_closeout_result",
            "warn",
            "Source public scorecard monitoring activation closeout validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "monitoring_activation_closeout_result",
            "blocker",
            "Source public scorecard monitoring activation closeout is not ready.",
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


def _check_first_cycle_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "first_cycle_contract", "blocker", "first_cycle_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_FIRST_CYCLE_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_FIRST_CYCLE_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "first_cycle_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard monitoring first-cycle review contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard monitoring first-cycle review contract invalid: "
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
        _add_check(checks, "first_cycle_controls", "blocker", "first_cycle_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_FIRST_CYCLE_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "first_cycle_controls",
        "pass" if not missing else "blocker",
        "Public scorecard monitoring first-cycle review controls are explicit."
        if not missing
        else f"Public scorecard monitoring first-cycle review controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_first_cycle_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_FIRST_CYCLE_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_first_cycle_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_first_cycle_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
