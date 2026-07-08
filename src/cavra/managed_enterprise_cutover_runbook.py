from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANAGED_ENTERPRISE_CUTOVER_RUNBOOK_SCHEMA = "cavra.managed-enterprise-cutover-runbook.v1"
MANAGED_ENTERPRISE_CUTOVER_RUNBOOK_RESULT_SCHEMA = "cavra.managed-enterprise-cutover-runbook.result.v1"

REQUIRED_CUTOVER_PROFILE_FIELDS = {
    "runbook_ref",
    "live_validation_plan_ref",
    "environment_ref",
    "change_window_ref",
    "evidence_room_ref",
    "rollback_plan_ref",
}

REQUIRED_CUTOVER_STEPS = {
    "preflight_freeze": "Confirm change freeze, release candidate, operator staffing, and evidence room are ready.",
    "identity_access": "Validate Enterprise identity, SSO/RBAC, and break-glass controls.",
    "tenant_isolation": "Validate tenant isolation and persistence boundaries.",
    "connectors_runtime": "Validate live connectors, scanners, runtime workflows, and MCP/tool controls.",
    "smtp_reporting": "Validate production SMTP/report delivery and recipient policy.",
    "aispm_gate": "Validate AISPM production readiness with no blockers.",
    "go_no_go": "Record executive go/no-go decision and approval references.",
    "activation": "Activate Managed or Enterprise control plane under operator supervision.",
    "rollback_rehearsal": "Confirm rollback trigger, owner, and rehearsal evidence references.",
    "customer_closeout": "Attach customer evidence-room, operating-review, and closeout references.",
    "public_status_sync": "Publish only customer-safe status and documentation references.",
}

REQUIRED_STEP_FIELDS = {
    "step_id",
    "title",
    "objective",
    "required_evidence_ref",
    "owner_ref",
    "approver_ref",
    "status_ref",
    "validator_command",
}

REQUIRED_CONTROL_FIELDS = {
    "change_freeze_ref",
    "go_no_go_ref",
    "rollback_trigger_ref",
    "incident_channel_ref",
    "customer_notification_ref",
    "evidence_archive_ref",
}

REQUIRED_REDACTION_CONTROLS = {
    "contains_no_customer_pii",
    "contains_no_credentials",
    "contains_no_raw_logs",
    "contains_no_raw_prompts",
    "contains_no_raw_model_data",
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


def build_managed_enterprise_cutover_runbook(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": MANAGED_ENTERPRISE_CUTOVER_RUNBOOK_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "cutover_profile": {
            "runbook_ref": f"{prefix}://runbook/managed-enterprise-cutover",
            "live_validation_plan_ref": f"{prefix}://managed-enterprise-live-validation/plan",
            "environment_ref": f"{prefix}://environment/managed-enterprise-production",
            "change_window_ref": f"{prefix}://change-window/managed-enterprise-cutover",
            "evidence_room_ref": f"{prefix}://evidence-room/managed-enterprise-cutover",
            "rollback_plan_ref": f"{prefix}://runbook/managed-enterprise-rollback",
        },
        "cutover_steps": [
            {
                "step_id": step_id,
                "title": step_id.replace("_", " ").title(),
                "objective": objective,
                "required_evidence_ref": f"{prefix}://managed-enterprise-cutover/{step_id}/evidence",
                "owner_ref": f"{prefix}://owner/{step_id}",
                "approver_ref": f"{prefix}://approval/{step_id}",
                "status_ref": f"{prefix}://status/{step_id}",
                "validator_command": _validator_command_for_step(step_id),
            }
            for step_id, objective in REQUIRED_CUTOVER_STEPS.items()
        ],
        "cutover_controls": {
            "change_freeze_ref": f"{prefix}://control/change-freeze",
            "go_no_go_ref": f"{prefix}://control/go-no-go",
            "rollback_trigger_ref": f"{prefix}://control/rollback-trigger",
            "incident_channel_ref": f"{prefix}://control/incident-channel",
            "customer_notification_ref": f"{prefix}://control/customer-notification",
            "evidence_archive_ref": f"{prefix}://control/evidence-archive",
        },
        "redaction_controls": {
            control: True
            for control in sorted(REQUIRED_REDACTION_CONTROLS)
        },
    }


def validate_managed_enterprise_cutover_runbook(
    runbook: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if runbook.get("schema_version") == MANAGED_ENTERPRISE_CUTOVER_RUNBOOK_SCHEMA else "blocker",
        "Cutover runbook schema is valid."
        if runbook.get("schema_version") == MANAGED_ENTERPRISE_CUTOVER_RUNBOOK_SCHEMA
        else f"Runbook must use {MANAGED_ENTERPRISE_CUTOVER_RUNBOOK_SCHEMA}.",
    )
    _check_evidence_mode(runbook, checks, require_live=require_live)
    _check_ref_object(
        runbook.get("cutover_profile", {}),
        checks,
        name="cutover_profile",
        required_fields=REQUIRED_CUTOVER_PROFILE_FIELDS,
    )
    _check_cutover_steps(runbook.get("cutover_steps", []), checks)
    _check_ref_object(
        runbook.get("cutover_controls", {}),
        checks,
        name="cutover_controls",
        required_fields=REQUIRED_CONTROL_FIELDS,
    )
    _check_redaction_controls(runbook.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_cutover_fields(runbook))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Runbook contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and runbook.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_CUTOVER_RUNBOOK_RESULT_SCHEMA,
        "product": runbook.get("product", "CAVRA"),
        "evidence_mode": runbook.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_cutover": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "step_count": len(runbook.get("cutover_steps", [])) if isinstance(runbook.get("cutover_steps"), list) else 0,
        "required_step_count": len(REQUIRED_CUTOVER_STEPS),
        "checks": checks,
    }


def write_managed_enterprise_cutover_runbook_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_cutover_runbook(evidence_mode="sample")
    live = build_managed_enterprise_cutover_runbook(evidence_mode="live")
    sample_result = validate_managed_enterprise_cutover_runbook(sample)
    live_result = validate_managed_enterprise_cutover_runbook(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-cutover-runbook.sample.json",
        "live_sanitized_example": output_dir / "managed-enterprise-cutover-runbook.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-cutover-runbook.sample.result.json",
        "live_result": output_dir / "managed-enterprise-cutover-runbook.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.managed-enterprise-cutover-runbook.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_cutover": live_result["ready_for_managed_enterprise_cutover"],
    }


def find_forbidden_cutover_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_cutover_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_cutover_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _validator_command_for_step(step_id: str) -> str:
    commands = {
        "identity_access": "python3 scripts/validate_enterprise_live_identity_packet.py --require-live",
        "tenant_isolation": "python3 scripts/validate_postgres_tenant_rls_smoke.py --require-live",
        "connectors_runtime": "python3 scripts/validate_priority_connectors.py --require-live",
        "smtp_reporting": "python3 scripts/validate_aispm_report_delivery_production.py",
        "aispm_gate": "python3 scripts/validate_aispm_production_readiness.py",
        "customer_closeout": "python3 scripts/validate_customer_operating_review.py --require-live",
    }
    return commands.get(step_id, "operator evidence-room reference required")


def _check_evidence_mode(runbook: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = runbook.get("evidence_mode")
    sanitized = runbook.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized cutover runbook supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample runbook validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Cutover requires evidence_mode=live and sanitized=true.")


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


def _check_cutover_steps(steps: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(steps, list):
        _add_check(checks, "cutover_steps", "blocker", "cutover_steps must be a list.")
        return
    by_id = {step.get("step_id"): step for step in steps if isinstance(step, dict)}
    missing_step_ids = sorted(set(REQUIRED_CUTOVER_STEPS) - set(by_id))
    extra_step_ids = sorted(set(by_id) - set(REQUIRED_CUTOVER_STEPS))
    step_failures: list[str] = []
    for step_id in REQUIRED_CUTOVER_STEPS:
        step = by_id.get(step_id)
        if not isinstance(step, dict):
            continue
        missing_fields = sorted(REQUIRED_STEP_FIELDS - set(step))
        if missing_fields:
            step_failures.append(f"{step_id} missing fields: {', '.join(missing_fields)}")
        for field in ("required_evidence_ref", "owner_ref", "approver_ref", "status_ref"):
            if field in step and not _is_ref(step[field]):
                step_failures.append(f"{step_id}.{field} must be a sanitized reference")
        if not isinstance(step.get("validator_command"), str) or not step.get("validator_command"):
            step_failures.append(f"{step_id}.validator_command must be non-empty")
    if missing_step_ids or extra_step_ids or step_failures:
        details = []
        if missing_step_ids:
            details.append(f"missing steps: {', '.join(missing_step_ids)}")
        if extra_step_ids:
            details.append(f"unexpected steps: {', '.join(extra_step_ids)}")
        details.extend(step_failures)
        _add_check(checks, "cutover_steps", "blocker", "; ".join(details))
    else:
        _add_check(checks, "cutover_steps", "pass", "All required cutover steps are present.")


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
