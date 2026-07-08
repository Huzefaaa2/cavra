from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANAGED_ENTERPRISE_LIVE_VALIDATION_PLAN_SCHEMA = "cavra.managed-enterprise-live-validation-plan.v1"
MANAGED_ENTERPRISE_LIVE_VALIDATION_PLAN_RESULT_SCHEMA = "cavra.managed-enterprise-live-validation-plan.result.v1"

REQUIRED_DEPLOYMENT_PROFILE_FIELDS = {
    "deployment_ref",
    "environment_ref",
    "owner_group_ref",
    "evidence_room_ref",
    "change_window_ref",
}

REQUIRED_VALIDATION_STAGES = {
    "identity_and_access": {
        "ready_flag": "ready_for_enterprise_live_identity",
        "command": "python3 scripts/validate_enterprise_live_identity_packet.py --require-live",
    },
    "tenant_isolation": {
        "ready_flag": "ready_for_postgres_tenant_rls_smoke",
        "command": "python3 scripts/validate_postgres_tenant_rls_smoke.py --require-live",
    },
    "ha_dr": {
        "ready_flag": "ready_for_enterprise_live_ha",
        "command": "python3 scripts/validate_enterprise_ha_readiness.py --require-live",
    },
    "evidence_custody": {
        "ready_flag": "ready_for_enterprise_evidence_custody",
        "command": "python3 scripts/validate_enterprise_evidence_custody.py --require-live",
    },
    "immutable_audit": {
        "ready_flag": "ready_for_enterprise_audit_log",
        "command": "python3 scripts/validate_enterprise_audit_log.py --require-live",
    },
    "connectors_and_scanners": {
        "ready_flag": "ready_for_enterprise_connectors_and_scanners",
        "command": "python3 scripts/validate_priority_connectors.py --require-live",
    },
    "policy_and_monitoring": {
        "ready_flag": "ready_for_continuous_monitoring",
        "command": "python3 scripts/validate_continuous_monitoring.py --require-live",
    },
    "runtime_workflows": {
        "ready_flag": "ready_for_runtime_workflow_validation",
        "command": "cavra evaluate ...",
    },
    "aispm_production_gate": {
        "ready_flag": "ready_for_aispm_production",
        "command": "python3 scripts/validate_aispm_production_readiness.py",
    },
    "smtp_report_delivery": {
        "ready_flag": "ready_for_report_delivery",
        "command": "python3 scripts/validate_aispm_report_delivery_production.py",
    },
    "customer_evidence_room": {
        "ready_flag": "ready_for_customer_evidence_room_closeout",
        "command": "python3 scripts/validate_customer_evidence_room.py --require-live",
    },
    "customer_operating_closeout": {
        "ready_flag": "ready_for_customer_operating_review",
        "command": "python3 scripts/validate_customer_operating_review.py --require-live",
    },
}

REQUIRED_STAGE_FIELDS = {
    "stage_id",
    "title",
    "ready_flag",
    "validator_command",
    "packet_ref",
    "result_ref",
    "evidence_ref",
    "owner_ref",
    "run_id_ref",
}

REQUIRED_ATTESTATION_FIELDS = {
    "prepared_by_ref",
    "reviewed_by_ref",
    "approval_ref",
}

REQUIRED_REDACTION_CONTROLS = {
    "contains_no_secrets",
    "contains_no_customer_pii",
    "contains_no_raw_logs",
    "contains_no_raw_prompts",
    "contains_no_raw_model_data",
    "contains_no_credentials",
}

FORBIDDEN_LIVE_VALIDATION_FIELDS = {
    "secret",
    "password",
    "token",
    "api_key",
    "private_key",
    "connection_string",
    "smtp_password",
    "smtp_username",
    "raw_log",
    "raw_logs",
    "raw_prompt",
    "raw_prompts",
    "raw_model",
    "model_weights",
    "training_data",
    "tenant_name",
    "customer_name",
    "email",
}

ALLOWED_REF_PREFIXES = (
    "evidence://",
    "ticket://",
    "audit://",
    "runbook://",
    "git://",
    "workflow://",
    "vault://",
    "share://",
    "sample://",
)


def build_managed_enterprise_live_validation_plan(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": MANAGED_ENTERPRISE_LIVE_VALIDATION_PLAN_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "deployment_profile": {
            "deployment_ref": f"{prefix}://deployment/managed-enterprise",
            "environment_ref": f"{prefix}://environment/production",
            "owner_group_ref": f"{prefix}://owner/platform-security",
            "evidence_room_ref": f"{prefix}://evidence-room/managed-enterprise-live-validation",
            "change_window_ref": f"{prefix}://change-window/live-validation",
        },
        "validation_stages": [
            {
                "stage_id": stage_id,
                "title": stage_id.replace("_", " ").title(),
                "ready_flag": contract["ready_flag"],
                "validator_command": contract["command"],
                "packet_ref": f"{prefix}://managed-enterprise-live-validation/{stage_id}/packet",
                "result_ref": f"{prefix}://managed-enterprise-live-validation/{stage_id}/result",
                "evidence_ref": f"{prefix}://managed-enterprise-live-validation/{stage_id}/evidence",
                "owner_ref": f"{prefix}://owner/{stage_id}",
                "run_id_ref": f"{prefix}://run/{stage_id}",
            }
            for stage_id, contract in REQUIRED_VALIDATION_STAGES.items()
        ],
        "redaction_controls": {
            control: True
            for control in sorted(REQUIRED_REDACTION_CONTROLS)
        },
        "attestation": {
            "prepared_by_ref": f"{prefix}://operator/platform-security",
            "reviewed_by_ref": f"{prefix}://approver/security-leadership",
            "approval_ref": f"{prefix}://approval/managed-enterprise-live-validation",
        },
    }


def validate_managed_enterprise_live_validation_plan(
    plan: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if plan.get("schema_version") == MANAGED_ENTERPRISE_LIVE_VALIDATION_PLAN_SCHEMA else "blocker",
        "Live validation plan schema is valid."
        if plan.get("schema_version") == MANAGED_ENTERPRISE_LIVE_VALIDATION_PLAN_SCHEMA
        else f"Plan must use {MANAGED_ENTERPRISE_LIVE_VALIDATION_PLAN_SCHEMA}.",
    )
    _check_evidence_mode(plan, checks, require_live=require_live)
    _check_profile(plan.get("deployment_profile", {}), checks)
    _check_validation_stages(plan.get("validation_stages", []), checks)
    _check_redaction_controls(plan.get("redaction_controls", {}), checks)
    _check_attestation(plan.get("attestation", {}), checks)
    forbidden = sorted(find_forbidden_live_validation_fields(plan))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Plan contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    live_ready = blocker_count == 0 and warning_count == 0 and plan.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_LIVE_VALIDATION_PLAN_RESULT_SCHEMA,
        "product": plan.get("product", "CAVRA"),
        "evidence_mode": plan.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_live_validation": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "stage_count": len(plan.get("validation_stages", [])) if isinstance(plan.get("validation_stages"), list) else 0,
        "required_stage_count": len(REQUIRED_VALIDATION_STAGES),
        "checks": checks,
    }


def write_managed_enterprise_live_validation_plan_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_live_validation_plan(evidence_mode="sample")
    live = build_managed_enterprise_live_validation_plan(evidence_mode="live")
    sample_result = validate_managed_enterprise_live_validation_plan(sample)
    live_result = validate_managed_enterprise_live_validation_plan(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-live-validation-plan.sample.json",
        "live_sanitized_example": output_dir / "managed-enterprise-live-validation-plan.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-live-validation-plan.sample.result.json",
        "live_result": output_dir / "managed-enterprise-live-validation-plan.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.managed-enterprise-live-validation-plan.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_live_validation": live_result["ready_for_managed_enterprise_live_validation"],
    }


def find_forbidden_live_validation_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            normalized = str(key).lower()
            if normalized in FORBIDDEN_LIVE_VALIDATION_FIELDS:
                found.add(path)
            found.update(find_forbidden_live_validation_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_live_validation_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(plan: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = plan.get("evidence_mode")
    sanitized = plan.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized validation plan supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample plan validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live validation requires evidence_mode=live and sanitized=true.")


def _check_profile(profile: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(profile, dict):
        _add_check(checks, "deployment_profile", "blocker", "deployment_profile must be an object.")
        return
    missing = sorted(REQUIRED_DEPLOYMENT_PROFILE_FIELDS - set(profile))
    invalid_refs = sorted(
        key
        for key, value in profile.items()
        if key in REQUIRED_DEPLOYMENT_PROFILE_FIELDS and not _is_ref(value)
    )
    if missing or invalid_refs:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid_refs:
            details.append(f"invalid refs: {', '.join(invalid_refs)}")
        _add_check(checks, "deployment_profile", "blocker", "; ".join(details))
    else:
        _add_check(checks, "deployment_profile", "pass", "Deployment profile references are complete.")


def _check_validation_stages(stages: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(stages, list):
        _add_check(checks, "validation_stages", "blocker", "validation_stages must be a list.")
        return
    by_id = {stage.get("stage_id"): stage for stage in stages if isinstance(stage, dict)}
    missing_stage_ids = sorted(set(REQUIRED_VALIDATION_STAGES) - set(by_id))
    extra_stage_ids = sorted(set(by_id) - set(REQUIRED_VALIDATION_STAGES))
    stage_failures: list[str] = []
    for stage_id, contract in REQUIRED_VALIDATION_STAGES.items():
        stage = by_id.get(stage_id)
        if not isinstance(stage, dict):
            continue
        missing_fields = sorted(REQUIRED_STAGE_FIELDS - set(stage))
        if missing_fields:
            stage_failures.append(f"{stage_id} missing fields: {', '.join(missing_fields)}")
        if stage.get("ready_flag") != contract["ready_flag"]:
            stage_failures.append(f"{stage_id} ready_flag must be {contract['ready_flag']}")
        command = stage.get("validator_command")
        if not isinstance(command, str) or not command:
            stage_failures.append(f"{stage_id} validator_command must be non-empty")
        elif contract["command"].split()[0] not in command:
            stage_failures.append(f"{stage_id} validator_command must reference {contract['command']}")
        for field in ("packet_ref", "result_ref", "evidence_ref", "owner_ref", "run_id_ref"):
            if field in stage and not _is_ref(stage[field]):
                stage_failures.append(f"{stage_id}.{field} must be a sanitized reference")
    if missing_stage_ids or extra_stage_ids or stage_failures:
        details = []
        if missing_stage_ids:
            details.append(f"missing stages: {', '.join(missing_stage_ids)}")
        if extra_stage_ids:
            details.append(f"unexpected stages: {', '.join(extra_stage_ids)}")
        details.extend(stage_failures)
        _add_check(checks, "validation_stages", "blocker", "; ".join(details))
    else:
        _add_check(checks, "validation_stages", "pass", "All required validation stages are present.")


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


def _check_attestation(attestation: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(attestation, dict):
        _add_check(checks, "attestation", "blocker", "attestation must be an object.")
        return
    missing = sorted(REQUIRED_ATTESTATION_FIELDS - set(attestation))
    invalid_refs = sorted(
        key
        for key, value in attestation.items()
        if key in REQUIRED_ATTESTATION_FIELDS and not _is_ref(value)
    )
    if missing or invalid_refs:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid_refs:
            details.append(f"invalid refs: {', '.join(invalid_refs)}")
        _add_check(checks, "attestation", "blocker", "; ".join(details))
    else:
        _add_check(checks, "attestation", "pass", "Attestation references are complete.")


def _is_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(ALLOWED_REF_PREFIXES)


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
