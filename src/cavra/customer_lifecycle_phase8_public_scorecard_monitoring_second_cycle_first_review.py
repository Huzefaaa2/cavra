from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_SECOND_CYCLE_FIRST_REVIEW_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_SECOND_CYCLE_FIRST_REVIEW_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.result.v1"
)

REQUIRED_SECOND_CYCLE_FIRST_REVIEW_OWNER_REFS = {
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

REQUIRED_SECOND_CYCLE_FIRST_REVIEW_CONTRACT_FIELDS = {
    "second_cycle_first_review_ref",
    "source_second_cycle_activation_closeout_ref",
    "review_window_ref",
    "findings_triage_ref",
    "signal_review_ref",
    "snapshot_archive_ref",
    "public_status_refresh_ref",
    "followup_owner_assignment_ref",
    "next_review_schedule_ref",
    "redaction_status",
}

REQUIRED_REVIEW_WINDOW_REFS = {
    "review_window_start_ref",
    "review_window_end_ref",
    "review_attendance_ref",
    "review_minutes_summary_ref",
}

REQUIRED_FINDINGS_TRIAGE_REFS = {
    "new_findings_register_ref",
    "critical_findings_disposition_ref",
    "accepted_findings_boundary_ref",
    "deferred_findings_register_ref",
}

REQUIRED_SIGNAL_REVIEW_REFS = {
    "scorecard_health_signal_review_ref",
    "link_health_signal_review_ref",
    "archive_freshness_signal_review_ref",
    "redaction_posture_signal_review_ref",
}

REQUIRED_SNAPSHOT_ARCHIVE_REFS = {
    "first_review_snapshot_manifest_ref",
    "signal_snapshot_archive_ref",
    "findings_triage_archive_ref",
    "public_status_snapshot_archive_ref",
    "immutable_first_review_archive_ref",
}

REQUIRED_PUBLIC_STATUS_REFRESH_REFS = {
    "public_scorecard_refresh_ref",
    "public_status_summary_refresh_ref",
    "readme_status_refresh_ref",
    "wiki_status_refresh_ref",
}

REQUIRED_FOLLOWUP_OWNER_REFS = {
    "followup_owner_register_ref",
    "security_followup_owner_ref",
    "operations_followup_owner_ref",
    "communications_followup_owner_ref",
}

REQUIRED_NEXT_REVIEW_SCHEDULE_REFS = {
    "next_review_window_ref",
    "next_review_agenda_ref",
    "next_review_owner_ref",
    "next_review_reminder_ref",
}

REQUIRED_CI_GATES = {
    "source_second_cycle_activation_closeout_validation",
    "review_window_validation",
    "findings_triage_validation",
    "signal_review_validation",
    "snapshot_archive_validation",
    "public_status_refresh_validation",
    "followup_owner_assignment_validation",
    "next_review_schedule_validation",
}

REQUIRED_SECOND_CYCLE_FIRST_REVIEW_CONTROLS = {
    "second_cycle_activation_closeout_ready",
    "review_window_completed",
    "findings_triaged",
    "signals_reviewed",
    "snapshots_archived",
    "public_status_refreshed",
    "followup_owners_assigned",
    "next_review_scheduled",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_SECOND_CYCLE_FIRST_REVIEW_FIELDS = {
    "accepted_finding_detail",
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
    "raw_finding",
    "raw_followup",
    "raw_health",
    "raw_link_check",
    "raw_minutes",
    "raw_monitor",
    "raw_public_status",
    "raw_redaction",
    "raw_review",
    "raw_risk",
    "raw_schedule",
    "raw_score",
    "raw_scorecard",
    "raw_signal",
    "raw_snapshot",
    "raw_status",
    "recipient_email",
    "remediation_detail",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
    second_cycle_activation_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    second_cycle_activation_closeout = (
        second_cycle_activation_closeout_packet
        or build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    second_cycle_activation_closeout_result = (
        validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
            second_cycle_activation_closeout,
            require_live=evidence_mode == "live",
        )
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_SECOND_CYCLE_FIRST_REVIEW_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "monitoring_second_cycle_first_review_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review"
        ),
        "second_cycle_activation_closeout_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout/r7"
        ),
        "second_cycle_activation_closeout_result": second_cycle_activation_closeout_result,
        "second_cycle_first_review_owner_refs": {
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
        "second_cycle_first_review_contract": {
            "second_cycle_first_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/review"
            ),
            "source_second_cycle_activation_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/source-activation"
            ),
            "review_window_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/review-window"
            ),
            "findings_triage_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/findings-triage"
            ),
            "signal_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/signal-review"
            ),
            "snapshot_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/snapshot-archive"
            ),
            "public_status_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/public-status-refresh"
            ),
            "followup_owner_assignment_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/followup-owners"
            ),
            "next_review_schedule_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/next-review"
            ),
            "redaction_status": "sanitized",
        },
        "review_window_refs": {
            "review_window_start_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/window/start"
            ),
            "review_window_end_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/window/end"
            ),
            "review_attendance_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/window/attendance"
            ),
            "review_minutes_summary_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/window/minutes-summary"
            ),
        },
        "findings_triage_refs": {
            "new_findings_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/findings/register"
            ),
            "critical_findings_disposition_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/findings/critical-disposition"
            ),
            "accepted_findings_boundary_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/findings/accepted-boundary"
            ),
            "deferred_findings_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/findings/deferred"
            ),
        },
        "signal_review_refs": {
            "scorecard_health_signal_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/signals/scorecard-health"
            ),
            "link_health_signal_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/signals/link-health"
            ),
            "archive_freshness_signal_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/signals/archive-freshness"
            ),
            "redaction_posture_signal_review_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/signals/redaction-posture"
            ),
        },
        "snapshot_archive_refs": {
            "first_review_snapshot_manifest_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/archive/manifest"
            ),
            "signal_snapshot_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/archive/signals"
            ),
            "findings_triage_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/archive/findings"
            ),
            "public_status_snapshot_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/archive/public-status"
            ),
            "immutable_first_review_archive_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/archive/immutable"
            ),
        },
        "public_status_refresh_refs": {
            "public_scorecard_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/public/scorecard-refresh"
            ),
            "public_status_summary_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/public/summary-refresh"
            ),
            "readme_status_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/public/readme-refresh"
            ),
            "wiki_status_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/public/wiki-refresh"
            ),
        },
        "followup_owner_refs": {
            "followup_owner_register_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/followup/register"
            ),
            "security_followup_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/followup/security"
            ),
            "operations_followup_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/followup/operations"
            ),
            "communications_followup_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/followup/communications"
            ),
        },
        "next_review_schedule_refs": {
            "next_review_window_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/next/window"
            ),
            "next_review_agenda_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/next/agenda"
            ),
            "next_review_owner_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/next/owner"
            ),
            "next_review_reminder_ref": (
                f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/next/reminder"
            ),
        },
        "ci_gate_coverage": {
            "source_second_cycle_activation_closeout_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-second-cycle-first-review/source-validation"
            ),
            "review_window_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-second-cycle-first-review/window-validation"
            ),
            "findings_triage_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-second-cycle-first-review/findings-validation"
            ),
            "signal_review_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-second-cycle-first-review/signal-validation"
            ),
            "snapshot_archive_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-second-cycle-first-review/archive-validation"
            ),
            "public_status_refresh_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-second-cycle-first-review/public-status-validation"
            ),
            "followup_owner_assignment_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-second-cycle-first-review/followup-validation"
            ),
            "next_review_schedule_validation": (
                f"{prefix}://ci/phase8/public-scorecard-monitoring-second-cycle-first-review/next-review-validation"
            ),
        },
        "second_cycle_first_review_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/source-activation",
            f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/review-window",
            f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/findings-triage",
            f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/signal-review",
            f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/snapshot-archive",
            f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/public-status-refresh",
            f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/followup-owners",
            f"{prefix}://phase8/public-scorecard-monitoring-second-cycle-first-review/next-review",
        ],
        "second_cycle_first_review_controls": {
            "second_cycle_activation_closeout_ready": second_cycle_activation_closeout_result["blocker_count"] == 0,
            "review_window_completed": True,
            "findings_triaged": True,
            "signals_reviewed": True,
            "snapshots_archived": True,
            "public_status_refreshed": True,
            "followup_owners_assigned": True,
            "next_review_scheduled": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_SECOND_CYCLE_FIRST_REVIEW_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard monitoring second-cycle first review schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(
        packet.get("second_cycle_activation_closeout_ref"),
        checks,
        "second_cycle_activation_closeout_ref",
    )
    _check_second_cycle_activation_closeout_result(
        packet.get("second_cycle_activation_closeout_result", {}),
        checks,
        require_live=require_live,
    )
    _check_required_refs(
        packet.get("second_cycle_first_review_owner_refs", {}),
        REQUIRED_SECOND_CYCLE_FIRST_REVIEW_OWNER_REFS,
        checks,
        "second_cycle_first_review_owner_refs",
    )
    _check_second_cycle_first_review_contract(packet.get("second_cycle_first_review_contract", {}), checks)
    _check_required_refs(packet.get("review_window_refs", {}), REQUIRED_REVIEW_WINDOW_REFS, checks, "review_window_refs")
    _check_required_refs(
        packet.get("findings_triage_refs", {}),
        REQUIRED_FINDINGS_TRIAGE_REFS,
        checks,
        "findings_triage_refs",
    )
    _check_required_refs(packet.get("signal_review_refs", {}), REQUIRED_SIGNAL_REVIEW_REFS, checks, "signal_review_refs")
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
    _check_required_refs(
        packet.get("followup_owner_refs", {}),
        REQUIRED_FOLLOWUP_OWNER_REFS,
        checks,
        "followup_owner_refs",
    )
    _check_required_refs(
        packet.get("next_review_schedule_refs", {}),
        REQUIRED_NEXT_REVIEW_SCHEDULE_REFS,
        checks,
        "next_review_schedule_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(
        packet.get("second_cycle_first_review_evidence_refs", []),
        checks,
        "second_cycle_first_review_evidence_refs",
        min_count=8,
    )
    _check_controls(packet.get("second_cycle_first_review_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_second_cycle_first_review_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard monitoring second-cycle first review contains sanitized refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_MONITORING_SECOND_CYCLE_FIRST_REVIEW_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
        sample
    )
    live_result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.live.sanitized.example.json",
        "sample_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 second-cycle first review supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 second-cycle first review validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Second-cycle first review requires evidence_mode=live and sanitized=true.",
        )


def _check_second_cycle_activation_closeout_result(
    result: Any,
    checks: list[dict[str, str]],
    *,
    require_live: bool,
) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "second_cycle_activation_closeout_result",
            "blocker",
            "second_cycle_activation_closeout_result must be an object.",
        )
        return
    ready = (
        result.get(
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"
        )
        is True
    )
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(
            checks,
            "second_cycle_activation_closeout_result",
            "pass",
            "Source second-cycle activation closeout is ready.",
        )
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "second_cycle_activation_closeout_result",
            "warn",
            "Source second-cycle activation closeout validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "second_cycle_activation_closeout_result",
            "blocker",
            "Source second-cycle activation closeout is not ready.",
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


def _check_second_cycle_first_review_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(
            checks,
            "second_cycle_first_review_contract",
            "blocker",
            "second_cycle_first_review_contract must be an object.",
        )
        return
    missing = sorted(field for field in REQUIRED_SECOND_CYCLE_FIRST_REVIEW_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_SECOND_CYCLE_FIRST_REVIEW_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "second_cycle_first_review_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard second-cycle first review contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard second-cycle first review contract invalid: "
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
            "second_cycle_first_review_controls",
            "blocker",
            "second_cycle_first_review_controls must be an object.",
        )
        return
    missing = sorted(
        control for control in REQUIRED_SECOND_CYCLE_FIRST_REVIEW_CONTROLS if controls.get(control) is not True
    )
    _add_check(
        checks,
        "second_cycle_first_review_controls",
        "pass" if not missing else "blocker",
        "Public scorecard second-cycle first review controls are explicit."
        if not missing
        else f"Public scorecard second-cycle first review controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_second_cycle_first_review_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_SECOND_CYCLE_FIRST_REVIEW_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_second_cycle_first_review_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_second_cycle_first_review_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
