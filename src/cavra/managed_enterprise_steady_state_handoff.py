from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANAGED_ENTERPRISE_STEADY_STATE_HANDOFF_SCHEMA = "cavra.managed-enterprise-steady-state-handoff.v1"
MANAGED_ENTERPRISE_STEADY_STATE_HANDOFF_RESULT_SCHEMA = "cavra.managed-enterprise-steady-state-handoff.result.v1"

REQUIRED_PROFILE_FIELDS = {
    "stabilization_report_ref",
    "environment_ref",
    "operating_model_ref",
    "evidence_room_ref",
    "customer_success_plan_ref",
    "support_model_ref",
}

REQUIRED_HANDOFF_AREAS = {
    "service_ownership": "Named operating owner, backup owner, and escalation path are documented.",
    "slo_monitoring": "SLOs, dashboards, alerts, and review cadence are active.",
    "security_operations": "Security review, incident path, break-glass review, and audit cadence are active.",
    "connector_operations": "Connector ownership, retry handling, and delivery monitoring are active.",
    "runtime_operations": "Runtime workflow control review and agent/tool exception handling are active.",
    "aispm_operations": "AISPM posture, reporting, findings, and blocker review cadence are active.",
    "support_operations": "Support triage, escalation, customer communication, and SLA routing are active.",
    "customer_success": "Operating review, renewal path, enablement, and adoption checkpoints are active.",
    "evidence_custody": "Evidence archive, retention, immutable audit, and verifier access are active.",
}

REQUIRED_AREA_FIELDS = {
    "area_id",
    "title",
    "objective",
    "owner_ref",
    "cadence_ref",
    "evidence_ref",
    "handoff_status_ref",
}

REQUIRED_OUTCOME_FIELDS = {
    "steady_state_decision_ref",
    "open_risks_ref",
    "next_operating_review_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
}

REQUIRED_REDACTION_CONTROLS = {
    "contains_no_credentials",
    "contains_no_customer_pii",
    "contains_no_raw_alert_payloads",
    "contains_no_raw_contracts",
    "contains_no_raw_logs",
    "contains_no_raw_model_data",
    "contains_no_raw_prompts",
    "contains_no_secrets",
    "contains_no_tenant_names",
}

FORBIDDEN_FIELDS = {
    "api_key",
    "connection_string",
    "contract_value",
    "customer_name",
    "email",
    "legal_terms",
    "password",
    "private_key",
    "raw_alert",
    "raw_alerts",
    "raw_contract",
    "raw_contracts",
    "raw_log",
    "raw_logs",
    "raw_model",
    "raw_prompt",
    "raw_prompts",
    "secret",
    "smtp_password",
    "smtp_username",
    "tenant_name",
    "token",
    "training_data",
}

ALLOWED_REF_PREFIXES = (
    "audit://",
    "evidence://",
    "git://",
    "runbook://",
    "share://",
    "ticket://",
    "vault://",
    "workflow://",
    "sample://",
)


def build_managed_enterprise_steady_state_handoff(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": MANAGED_ENTERPRISE_STEADY_STATE_HANDOFF_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "handoff_profile": {
            "stabilization_report_ref": f"{prefix}://managed-enterprise-stabilization/report",
            "environment_ref": f"{prefix}://environment/managed-enterprise-production",
            "operating_model_ref": f"{prefix}://runbook/managed-enterprise-operating-model",
            "evidence_room_ref": f"{prefix}://evidence-room/managed-enterprise-steady-state",
            "customer_success_plan_ref": f"{prefix}://customer-success/operating-plan",
            "support_model_ref": f"{prefix}://support/managed-enterprise-model",
        },
        "handoff_areas": [
            {
                "area_id": area_id,
                "title": area_id.replace("_", " ").title(),
                "objective": objective,
                "owner_ref": f"{prefix}://owner/{area_id}",
                "cadence_ref": f"{prefix}://cadence/{area_id}",
                "evidence_ref": f"{prefix}://steady-state/{area_id}/evidence",
                "handoff_status_ref": f"{prefix}://steady-state/{area_id}/status",
            }
            for area_id, objective in REQUIRED_HANDOFF_AREAS.items()
        ],
        "steady_state_outcome": {
            "steady_state_decision_ref": f"{prefix}://decision/steady-state-ready",
            "open_risks_ref": f"{prefix}://risks/none-or-accepted",
            "next_operating_review_ref": f"{prefix}://review/next-managed-enterprise-operating-review",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security",
        },
        "redaction_controls": {
            control: True
            for control in sorted(REQUIRED_REDACTION_CONTROLS)
        },
    }


def validate_managed_enterprise_steady_state_handoff(
    handoff: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if handoff.get("schema_version") == MANAGED_ENTERPRISE_STEADY_STATE_HANDOFF_SCHEMA else "blocker",
        "Steady-state handoff schema is valid."
        if handoff.get("schema_version") == MANAGED_ENTERPRISE_STEADY_STATE_HANDOFF_SCHEMA
        else f"Handoff must use {MANAGED_ENTERPRISE_STEADY_STATE_HANDOFF_SCHEMA}.",
    )
    _check_evidence_mode(handoff, checks, require_live=require_live)
    _check_ref_object(
        handoff.get("handoff_profile", {}),
        checks,
        name="handoff_profile",
        required_fields=REQUIRED_PROFILE_FIELDS,
    )
    _check_handoff_areas(handoff.get("handoff_areas", []), checks)
    _check_ref_object(
        handoff.get("steady_state_outcome", {}),
        checks,
        name="steady_state_outcome",
        required_fields=REQUIRED_OUTCOME_FIELDS,
    )
    _check_redaction_controls(handoff.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_steady_state_fields(handoff))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Handoff contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and handoff.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_STEADY_STATE_HANDOFF_RESULT_SCHEMA,
        "product": handoff.get("product", "CAVRA"),
        "evidence_mode": handoff.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_steady_state": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "area_count": len(handoff.get("handoff_areas", [])) if isinstance(handoff.get("handoff_areas"), list) else 0,
        "required_area_count": len(REQUIRED_HANDOFF_AREAS),
        "checks": checks,
    }


def write_managed_enterprise_steady_state_handoff_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_steady_state_handoff(evidence_mode="sample")
    live = build_managed_enterprise_steady_state_handoff(evidence_mode="live")
    sample_result = validate_managed_enterprise_steady_state_handoff(sample)
    live_result = validate_managed_enterprise_steady_state_handoff(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-steady-state-handoff.sample.json",
        "live_sanitized_example": output_dir / "managed-enterprise-steady-state-handoff.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-steady-state-handoff.sample.result.json",
        "live_result": output_dir / "managed-enterprise-steady-state-handoff.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.managed-enterprise-steady-state-handoff.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_steady_state": live_result["ready_for_managed_enterprise_steady_state"],
    }


def find_forbidden_steady_state_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_steady_state_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_steady_state_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(handoff: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = handoff.get("evidence_mode")
    sanitized = handoff.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized steady-state handoff supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample steady-state handoff validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Steady-state handoff requires evidence_mode=live and sanitized=true.")


def _check_ref_object(
    value: Any,
    checks: list[dict[str, str]],
    *,
    name: str,
    required_fields: set[str],
) -> None:
    if not isinstance(value, dict):
        _add_check(checks, name, "blocker", f"{name} must be an object.")
        return
    missing = sorted(required_fields - set(value))
    invalid_refs = sorted(
        key
        for key, item in value.items()
        if key in required_fields and not _is_ref(item)
    )
    if missing or invalid_refs:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid_refs:
            details.append(f"invalid refs: {', '.join(invalid_refs)}")
        _add_check(checks, name, "blocker", "; ".join(details))
    else:
        _add_check(checks, name, "pass", f"{name} references are complete.")


def _check_handoff_areas(areas: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(areas, list):
        _add_check(checks, "handoff_areas", "blocker", "handoff_areas must be a list.")
        return
    by_id = {area.get("area_id"): area for area in areas if isinstance(area, dict)}
    missing_area_ids = sorted(set(REQUIRED_HANDOFF_AREAS) - set(by_id))
    extra_area_ids = sorted(set(by_id) - set(REQUIRED_HANDOFF_AREAS))
    failures: list[str] = []
    for area_id in REQUIRED_HANDOFF_AREAS:
        area = by_id.get(area_id)
        if not isinstance(area, dict):
            continue
        missing_fields = sorted(REQUIRED_AREA_FIELDS - set(area))
        if missing_fields:
            failures.append(f"{area_id} missing fields: {', '.join(missing_fields)}")
        for field in ("owner_ref", "cadence_ref", "evidence_ref", "handoff_status_ref"):
            if field in area and not _is_ref(area[field]):
                failures.append(f"{area_id}.{field} must be a sanitized reference")
    if missing_area_ids or extra_area_ids or failures:
        details = []
        if missing_area_ids:
            details.append(f"missing areas: {', '.join(missing_area_ids)}")
        if extra_area_ids:
            details.append(f"unexpected areas: {', '.join(extra_area_ids)}")
        details.extend(failures)
        _add_check(checks, "handoff_areas", "blocker", "; ".join(details))
    else:
        _add_check(checks, "handoff_areas", "pass", "All required steady-state handoff areas are present.")


def _check_redaction_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "redaction_controls", "blocker", "redaction_controls must be an object.")
        return
    missing = sorted(REQUIRED_REDACTION_CONTROLS - set(controls))
    false_controls = sorted(key for key in REQUIRED_REDACTION_CONTROLS if controls.get(key) is not True)
    if missing or false_controls:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if false_controls:
            details.append(f"must be true: {', '.join(false_controls)}")
        _add_check(checks, "redaction_controls", "blocker", "; ".join(details))
    else:
        _add_check(checks, "redaction_controls", "pass", "Redaction controls are asserted.")


def _is_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(ALLOWED_REF_PREFIXES)


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
