from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANAGED_ENTERPRISE_STABILIZATION_REPORT_SCHEMA = "cavra.managed-enterprise-stabilization-report.v1"
MANAGED_ENTERPRISE_STABILIZATION_REPORT_RESULT_SCHEMA = "cavra.managed-enterprise-stabilization-report.result.v1"

REQUIRED_PROFILE_FIELDS = {
    "cutover_runbook_ref",
    "environment_ref",
    "stabilization_window_ref",
    "evidence_room_ref",
    "operator_channel_ref",
    "customer_status_ref",
}

REQUIRED_HEALTH_SIGNALS = {
    "api_health": "API health and uptime are within the agreed stabilization window.",
    "identity_health": "SSO, RBAC, break-glass, and operator access are stable.",
    "tenant_isolation_health": "Tenant isolation checks remain clean after activation.",
    "connector_health": "Connectors and scanners are delivering expected evidence references.",
    "runtime_control_health": "Runtime agent/tool controls are evaluating expected workflows.",
    "smtp_report_health": "SMTP/report delivery has no unresolved blocker.",
    "aispm_health": "AISPM posture generation has no production-readiness blocker.",
    "audit_evidence_health": "Audit, evidence custody, and archive refs are complete.",
    "support_alert_health": "Alerts, incidents, and customer-visible support items are triaged.",
}

REQUIRED_SIGNAL_FIELDS = {
    "signal_id",
    "title",
    "objective",
    "status_ref",
    "evidence_ref",
    "owner_ref",
    "reviewed_by_ref",
}

REQUIRED_OUTCOME_FIELDS = {
    "stabilization_decision_ref",
    "rollback_required_ref",
    "open_blockers_ref",
    "customer_acceptance_ref",
    "next_review_ref",
}

REQUIRED_REDACTION_CONTROLS = {
    "contains_no_credentials",
    "contains_no_customer_pii",
    "contains_no_raw_alert_payloads",
    "contains_no_raw_logs",
    "contains_no_raw_model_data",
    "contains_no_raw_prompts",
    "contains_no_secrets",
    "contains_no_tenant_names",
}

FORBIDDEN_FIELDS = {
    "api_key",
    "connection_string",
    "customer_name",
    "email",
    "password",
    "private_key",
    "raw_alert",
    "raw_alerts",
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


def build_managed_enterprise_stabilization_report(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": MANAGED_ENTERPRISE_STABILIZATION_REPORT_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "stabilization_profile": {
            "cutover_runbook_ref": f"{prefix}://managed-enterprise-cutover/runbook",
            "environment_ref": f"{prefix}://environment/managed-enterprise-production",
            "stabilization_window_ref": f"{prefix}://window/post-cutover-stabilization",
            "evidence_room_ref": f"{prefix}://evidence-room/managed-enterprise-stabilization",
            "operator_channel_ref": f"{prefix}://channel/operator-war-room",
            "customer_status_ref": f"{prefix}://status/customer-safe-stabilization",
        },
        "health_signals": [
            {
                "signal_id": signal_id,
                "title": signal_id.replace("_", " ").title(),
                "objective": objective,
                "status_ref": f"{prefix}://stabilization/{signal_id}/status",
                "evidence_ref": f"{prefix}://stabilization/{signal_id}/evidence",
                "owner_ref": f"{prefix}://owner/{signal_id}",
                "reviewed_by_ref": f"{prefix}://review/{signal_id}",
            }
            for signal_id, objective in REQUIRED_HEALTH_SIGNALS.items()
        ],
        "stabilization_outcome": {
            "stabilization_decision_ref": f"{prefix}://decision/stabilization-ready",
            "rollback_required_ref": f"{prefix}://rollback/not-required-or-documented",
            "open_blockers_ref": f"{prefix}://blockers/none-or-triaged",
            "customer_acceptance_ref": f"{prefix}://acceptance/customer-safe",
            "next_review_ref": f"{prefix}://review/next-operating-review",
        },
        "redaction_controls": {
            control: True
            for control in sorted(REQUIRED_REDACTION_CONTROLS)
        },
    }


def validate_managed_enterprise_stabilization_report(
    report: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if report.get("schema_version") == MANAGED_ENTERPRISE_STABILIZATION_REPORT_SCHEMA else "blocker",
        "Stabilization report schema is valid."
        if report.get("schema_version") == MANAGED_ENTERPRISE_STABILIZATION_REPORT_SCHEMA
        else f"Report must use {MANAGED_ENTERPRISE_STABILIZATION_REPORT_SCHEMA}.",
    )
    _check_evidence_mode(report, checks, require_live=require_live)
    _check_ref_object(
        report.get("stabilization_profile", {}),
        checks,
        name="stabilization_profile",
        required_fields=REQUIRED_PROFILE_FIELDS,
    )
    _check_health_signals(report.get("health_signals", []), checks)
    _check_ref_object(
        report.get("stabilization_outcome", {}),
        checks,
        name="stabilization_outcome",
        required_fields=REQUIRED_OUTCOME_FIELDS,
    )
    _check_redaction_controls(report.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_stabilization_fields(report))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Report contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and report.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_STABILIZATION_REPORT_RESULT_SCHEMA,
        "product": report.get("product", "CAVRA"),
        "evidence_mode": report.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_stabilization_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "signal_count": len(report.get("health_signals", [])) if isinstance(report.get("health_signals"), list) else 0,
        "required_signal_count": len(REQUIRED_HEALTH_SIGNALS),
        "checks": checks,
    }


def write_managed_enterprise_stabilization_report_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_stabilization_report(evidence_mode="sample")
    live = build_managed_enterprise_stabilization_report(evidence_mode="live")
    sample_result = validate_managed_enterprise_stabilization_report(sample)
    live_result = validate_managed_enterprise_stabilization_report(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-stabilization-report.sample.json",
        "live_sanitized_example": output_dir / "managed-enterprise-stabilization-report.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-stabilization-report.sample.result.json",
        "live_result": output_dir / "managed-enterprise-stabilization-report.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.managed-enterprise-stabilization-report.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_stabilization_closeout": live_result[
            "ready_for_managed_enterprise_stabilization_closeout"
        ],
    }


def find_forbidden_stabilization_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_stabilization_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_stabilization_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(report: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = report.get("evidence_mode")
    sanitized = report.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized stabilization report supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample stabilization report validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Stabilization requires evidence_mode=live and sanitized=true.")


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


def _check_health_signals(signals: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(signals, list):
        _add_check(checks, "health_signals", "blocker", "health_signals must be a list.")
        return
    by_id = {signal.get("signal_id"): signal for signal in signals if isinstance(signal, dict)}
    missing_signal_ids = sorted(set(REQUIRED_HEALTH_SIGNALS) - set(by_id))
    extra_signal_ids = sorted(set(by_id) - set(REQUIRED_HEALTH_SIGNALS))
    failures: list[str] = []
    for signal_id in REQUIRED_HEALTH_SIGNALS:
        signal = by_id.get(signal_id)
        if not isinstance(signal, dict):
            continue
        missing_fields = sorted(REQUIRED_SIGNAL_FIELDS - set(signal))
        if missing_fields:
            failures.append(f"{signal_id} missing fields: {', '.join(missing_fields)}")
        for field in ("status_ref", "evidence_ref", "owner_ref", "reviewed_by_ref"):
            if field in signal and not _is_ref(signal[field]):
                failures.append(f"{signal_id}.{field} must be a sanitized reference")
    if missing_signal_ids or extra_signal_ids or failures:
        details = []
        if missing_signal_ids:
            details.append(f"missing signals: {', '.join(missing_signal_ids)}")
        if extra_signal_ids:
            details.append(f"unexpected signals: {', '.join(extra_signal_ids)}")
        details.extend(failures)
        _add_check(checks, "health_signals", "blocker", "; ".join(details))
    else:
        _add_check(checks, "health_signals", "pass", "All required stabilization health signals are present.")


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
