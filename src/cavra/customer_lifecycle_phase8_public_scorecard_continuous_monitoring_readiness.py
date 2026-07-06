from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_audit_review_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_CONTINUOUS_MONITORING_READINESS_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_CONTINUOUS_MONITORING_READINESS_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness.result.v1"
)

REQUIRED_MONITORING_OWNER_REFS = {
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

REQUIRED_MONITORING_CONTRACT_FIELDS = {
    "continuous_monitoring_readiness_ref",
    "source_audit_review_closeout_ref",
    "scorecard_health_monitor_ref",
    "link_health_monitor_ref",
    "archive_freshness_monitor_ref",
    "redaction_posture_monitor_ref",
    "alert_routing_ref",
    "review_cadence_ref",
    "escalation_readiness_ref",
    "redaction_status",
}

REQUIRED_SCORECARD_HEALTH_REFS = {
    "public_scorecard_availability_ref",
    "public_scorecard_freshness_ref",
    "public_scorecard_schema_ref",
    "public_scorecard_owner_ref",
}

REQUIRED_LINK_HEALTH_REFS = {
    "product_website_link_monitor_ref",
    "readme_link_monitor_ref",
    "wiki_link_monitor_ref",
    "trial_field_guide_link_monitor_ref",
    "sandbox_link_monitor_ref",
}

REQUIRED_ARCHIVE_FRESHNESS_REFS = {
    "audit_archive_freshness_ref",
    "scorecard_snapshot_freshness_ref",
    "evidence_room_freshness_ref",
    "immutable_archive_freshness_ref",
}

REQUIRED_REDACTION_POSTURE_REFS = {
    "private_material_monitor_ref",
    "customer_identity_monitor_ref",
    "commercial_terms_monitor_ref",
    "public_boundary_monitor_ref",
}

REQUIRED_ALERT_ROUTING_REFS = {
    "operations_alert_ref",
    "security_alert_ref",
    "communications_alert_ref",
    "executive_escalation_ref",
}

REQUIRED_REVIEW_CADENCE_REFS = {
    "weekly_health_review_ref",
    "monthly_audit_review_ref",
    "quarterly_scorecard_refresh_ref",
    "cadence_owner_ref",
}

REQUIRED_ESCALATION_REFS = {
    "broken_link_escalation_ref",
    "stale_scorecard_escalation_ref",
    "archive_drift_escalation_ref",
    "redaction_regression_escalation_ref",
}

REQUIRED_CI_GATES = {
    "source_audit_review_closeout_validation",
    "scorecard_health_monitor_validation",
    "link_health_monitor_validation",
    "archive_freshness_monitor_validation",
    "redaction_posture_monitor_validation",
    "alert_routing_validation",
    "review_cadence_validation",
    "escalation_readiness_validation",
}

REQUIRED_MONITORING_CONTROLS = {
    "audit_review_closeout_ready",
    "scorecard_health_monitors_defined",
    "link_health_monitors_defined",
    "archive_freshness_monitors_defined",
    "redaction_posture_monitors_defined",
    "alert_routing_defined",
    "review_cadence_defined",
    "escalation_readiness_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_CONTINUOUS_MONITORING_FIELDS = {
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
    "raw_redaction",
    "raw_review",
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


def build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
    audit_review_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    audit_review_closeout = (
        audit_review_closeout_packet
        or build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    audit_review_closeout_result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        audit_review_closeout,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_CONTINUOUS_MONITORING_READINESS_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "continuous_monitoring_readiness_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness"
        ),
        "audit_review_closeout_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-audit-review-closeout/r7"
        ),
        "audit_review_closeout_result": audit_review_closeout_result,
        "monitoring_owner_refs": {
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
        "monitoring_contract": {
            "continuous_monitoring_readiness_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/readiness"
            ),
            "source_audit_review_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/source-audit-review-closeout"
            ),
            "scorecard_health_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/scorecard-health-monitor"
            ),
            "link_health_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/link-health-monitor"
            ),
            "archive_freshness_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/archive-freshness-monitor"
            ),
            "redaction_posture_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/redaction-posture-monitor"
            ),
            "alert_routing_ref": f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/alert-routing",
            "review_cadence_ref": f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/review-cadence",
            "escalation_readiness_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/escalation-readiness"
            ),
            "redaction_status": "sanitized",
        },
        "scorecard_health_refs": {
            "public_scorecard_availability_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/scorecard/availability"
            ),
            "public_scorecard_freshness_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/scorecard/freshness"
            ),
            "public_scorecard_schema_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/scorecard/schema"
            ),
            "public_scorecard_owner_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/scorecard/owner"
            ),
        },
        "link_health_refs": {
            "product_website_link_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/link/product-website"
            ),
            "readme_link_monitor_ref": f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/link/readme",
            "wiki_link_monitor_ref": f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/link/wiki",
            "trial_field_guide_link_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/link/trial-field-guide"
            ),
            "sandbox_link_monitor_ref": f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/link/sandbox",
        },
        "archive_freshness_refs": {
            "audit_archive_freshness_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/archive/audit"
            ),
            "scorecard_snapshot_freshness_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/archive/scorecard-snapshot"
            ),
            "evidence_room_freshness_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/archive/evidence-room"
            ),
            "immutable_archive_freshness_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/archive/immutable"
            ),
        },
        "redaction_posture_refs": {
            "private_material_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/redaction/private-material"
            ),
            "customer_identity_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/redaction/customer-identity"
            ),
            "commercial_terms_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/redaction/commercial-terms"
            ),
            "public_boundary_monitor_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/redaction/public-boundary"
            ),
        },
        "alert_routing_refs": {
            "operations_alert_ref": f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/alert/operations",
            "security_alert_ref": f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/alert/security",
            "communications_alert_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/alert/communications"
            ),
            "executive_escalation_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/alert/executive-escalation"
            ),
        },
        "review_cadence_refs": {
            "weekly_health_review_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/cadence/weekly-health"
            ),
            "monthly_audit_review_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/cadence/monthly-audit"
            ),
            "quarterly_scorecard_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/cadence/quarterly-refresh"
            ),
            "cadence_owner_ref": f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/cadence/owner",
        },
        "escalation_readiness_refs": {
            "broken_link_escalation_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/escalation/broken-link"
            ),
            "stale_scorecard_escalation_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/escalation/stale-scorecard"
            ),
            "archive_drift_escalation_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/escalation/archive-drift"
            ),
            "redaction_regression_escalation_ref": (
                f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/escalation/redaction-regression"
            ),
        },
        "ci_gate_coverage": {
            "source_audit_review_closeout_validation": (
                f"{prefix}://ci/phase8/public-scorecard-continuous-monitoring-readiness/source-audit-review-closeout-validation"
            ),
            "scorecard_health_monitor_validation": (
                f"{prefix}://ci/phase8/public-scorecard-continuous-monitoring-readiness/scorecard-health-validation"
            ),
            "link_health_monitor_validation": (
                f"{prefix}://ci/phase8/public-scorecard-continuous-monitoring-readiness/link-health-validation"
            ),
            "archive_freshness_monitor_validation": (
                f"{prefix}://ci/phase8/public-scorecard-continuous-monitoring-readiness/archive-freshness-validation"
            ),
            "redaction_posture_monitor_validation": (
                f"{prefix}://ci/phase8/public-scorecard-continuous-monitoring-readiness/redaction-posture-validation"
            ),
            "alert_routing_validation": (
                f"{prefix}://ci/phase8/public-scorecard-continuous-monitoring-readiness/alert-routing-validation"
            ),
            "review_cadence_validation": (
                f"{prefix}://ci/phase8/public-scorecard-continuous-monitoring-readiness/review-cadence-validation"
            ),
            "escalation_readiness_validation": (
                f"{prefix}://ci/phase8/public-scorecard-continuous-monitoring-readiness/escalation-readiness-validation"
            ),
        },
        "monitoring_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/source-audit-review-closeout",
            f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/scorecard-health",
            f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/link-health",
            f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/archive-freshness",
            f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/redaction-posture",
            f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/alert-routing",
            f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/review-cadence",
            f"{prefix}://phase8/public-scorecard-continuous-monitoring-readiness/escalation-readiness",
        ],
        "monitoring_controls": {
            "audit_review_closeout_ready": audit_review_closeout_result["blocker_count"] == 0,
            "scorecard_health_monitors_defined": True,
            "link_health_monitors_defined": True,
            "archive_freshness_monitors_defined": True,
            "redaction_posture_monitors_defined": True,
            "alert_routing_defined": True,
            "review_cadence_defined": True,
            "escalation_readiness_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_CONTINUOUS_MONITORING_READINESS_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard continuous monitoring readiness schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("audit_review_closeout_ref"), checks, "audit_review_closeout_ref")
    _check_audit_review_closeout_result(packet.get("audit_review_closeout_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("monitoring_owner_refs", {}), REQUIRED_MONITORING_OWNER_REFS, checks, "monitoring_owner_refs")
    _check_monitoring_contract(packet.get("monitoring_contract", {}), checks)
    _check_required_refs(packet.get("scorecard_health_refs", {}), REQUIRED_SCORECARD_HEALTH_REFS, checks, "scorecard_health_refs")
    _check_required_refs(packet.get("link_health_refs", {}), REQUIRED_LINK_HEALTH_REFS, checks, "link_health_refs")
    _check_required_refs(
        packet.get("archive_freshness_refs", {}),
        REQUIRED_ARCHIVE_FRESHNESS_REFS,
        checks,
        "archive_freshness_refs",
    )
    _check_required_refs(
        packet.get("redaction_posture_refs", {}),
        REQUIRED_REDACTION_POSTURE_REFS,
        checks,
        "redaction_posture_refs",
    )
    _check_required_refs(packet.get("alert_routing_refs", {}), REQUIRED_ALERT_ROUTING_REFS, checks, "alert_routing_refs")
    _check_required_refs(packet.get("review_cadence_refs", {}), REQUIRED_REVIEW_CADENCE_REFS, checks, "review_cadence_refs")
    _check_required_refs(
        packet.get("escalation_readiness_refs", {}),
        REQUIRED_ESCALATION_REFS,
        checks,
        "escalation_readiness_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("monitoring_evidence_refs", []), checks, "monitoring_evidence_refs", min_count=8)
    _check_controls(packet.get("monitoring_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_continuous_monitoring_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard continuous monitoring readiness contains sanitized refs and public-safe monitor refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_CONTINUOUS_MONITORING_READINESS_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness.live.sanitized.example.json",
        "sample_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(
            checks,
            "evidence_mode",
            "pass",
            "Live sanitized Phase 8 public scorecard continuous monitoring readiness supplied.",
        )
    elif mode == "sample" and not require_live:
        _add_check(
            checks,
            "evidence_mode",
            "warn",
            "Sample Phase 8 public scorecard continuous monitoring readiness validates shape only.",
        )
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Continuous monitoring readiness requires evidence_mode=live and sanitized=true.",
        )


def _check_audit_review_closeout_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "audit_review_closeout_result", "blocker", "audit_review_closeout_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "audit_review_closeout_result", "pass", "Source public scorecard audit review closeout is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "audit_review_closeout_result",
            "warn",
            "Source public scorecard audit review closeout validates shape but is not live.",
        )
    else:
        _add_check(checks, "audit_review_closeout_result", "blocker", "Source public scorecard audit review closeout is not ready.")


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


def _check_monitoring_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "monitoring_contract", "blocker", "monitoring_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_MONITORING_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_MONITORING_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "monitoring_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard continuous monitoring readiness contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard continuous monitoring readiness contract invalid: "
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
        _add_check(checks, "monitoring_controls", "blocker", "monitoring_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_MONITORING_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "monitoring_controls",
        "pass" if not missing else "blocker",
        "Public scorecard continuous monitoring readiness controls are explicit."
        if not missing
        else f"Public scorecard continuous monitoring readiness controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_continuous_monitoring_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_CONTINUOUS_MONITORING_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_continuous_monitoring_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_continuous_monitoring_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
