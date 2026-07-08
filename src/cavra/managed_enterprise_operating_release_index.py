from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANAGED_ENTERPRISE_OPERATING_RELEASE_INDEX_SCHEMA = "cavra.managed-enterprise-operating-release-index.v1"
MANAGED_ENTERPRISE_OPERATING_RELEASE_INDEX_RESULT_SCHEMA = "cavra.managed-enterprise-operating-release-index.result.v1"

REQUIRED_PROFILE_FIELDS = {
    "environment_ref",
    "evidence_room_ref",
    "release_owner_ref",
    "operating_model_ref",
    "customer_status_ref",
    "public_status_ref",
}

REQUIRED_OPERATING_GATES = {
    "live_validation": "Real tenants, connectors, SMTP/report delivery, runtime workflows, AISPM, and closeout evidence refs are attached.",
    "cutover": "Activation, go/no-go, rollback, customer closeout, and status synchronization are complete.",
    "stabilization": "The first post-cutover health window is closed with no unresolved blocker.",
    "steady_state_handoff": "Named operating owners, cadence, support, AISPM operations, and evidence custody are active.",
    "evidence_archive": "Final operating evidence archive, retention, and verifier access are recorded.",
    "public_safe_status_sync": "Public-safe README, wiki, status, and release notes are aligned without customer-private material.",
}

REQUIRED_GATE_FIELDS = {
    "gate_id",
    "title",
    "objective",
    "result_ref",
    "evidence_ref",
    "owner_ref",
    "status_ref",
}

REQUIRED_OUTCOME_FIELDS = {
    "operating_release_decision_ref",
    "open_blockers_ref",
    "accepted_risks_ref",
    "next_operating_review_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
}

REQUIRED_REDACTION_CONTROLS = {
    "contains_no_credentials",
    "contains_no_customer_pii",
    "contains_no_private_release_notes",
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
    "private_release_notes",
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
    "release://",
    "runbook://",
    "share://",
    "ticket://",
    "vault://",
    "workflow://",
    "sample://",
)


def build_managed_enterprise_operating_release_index(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": MANAGED_ENTERPRISE_OPERATING_RELEASE_INDEX_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "release_profile": {
            "environment_ref": f"{prefix}://environment/managed-enterprise-production",
            "evidence_room_ref": f"{prefix}://evidence-room/managed-enterprise-operating-release",
            "release_owner_ref": f"{prefix}://owner/managed-enterprise-operating-release",
            "operating_model_ref": f"{prefix}://runbook/managed-enterprise-operating-model",
            "customer_status_ref": f"{prefix}://status/customer-safe-operating-release",
            "public_status_ref": f"{prefix}://status/public-safe-operating-release",
        },
        "operating_gates": [
            {
                "gate_id": gate_id,
                "title": gate_id.replace("_", " ").title(),
                "objective": objective,
                "result_ref": f"{prefix}://operating-release/{gate_id}/result",
                "evidence_ref": f"{prefix}://operating-release/{gate_id}/evidence",
                "owner_ref": f"{prefix}://owner/{gate_id}",
                "status_ref": f"{prefix}://operating-release/{gate_id}/status",
            }
            for gate_id, objective in REQUIRED_OPERATING_GATES.items()
        ],
        "operating_release_outcome": {
            "operating_release_decision_ref": f"{prefix}://decision/managed-enterprise-operating-release-ready",
            "open_blockers_ref": f"{prefix}://blockers/none-or-accepted",
            "accepted_risks_ref": f"{prefix}://risks/accepted-operating-risks",
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


def validate_managed_enterprise_operating_release_index(
    index: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if index.get("schema_version") == MANAGED_ENTERPRISE_OPERATING_RELEASE_INDEX_SCHEMA else "blocker",
        "Operating release index schema is valid."
        if index.get("schema_version") == MANAGED_ENTERPRISE_OPERATING_RELEASE_INDEX_SCHEMA
        else f"Index must use {MANAGED_ENTERPRISE_OPERATING_RELEASE_INDEX_SCHEMA}.",
    )
    _check_evidence_mode(index, checks, require_live=require_live)
    _check_ref_object(
        index.get("release_profile", {}),
        checks,
        name="release_profile",
        required_fields=REQUIRED_PROFILE_FIELDS,
    )
    _check_operating_gates(index.get("operating_gates", []), checks)
    _check_ref_object(
        index.get("operating_release_outcome", {}),
        checks,
        name="operating_release_outcome",
        required_fields=REQUIRED_OUTCOME_FIELDS,
    )
    _check_redaction_controls(index.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_operating_release_fields(index))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Index contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and index.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_OPERATING_RELEASE_INDEX_RESULT_SCHEMA,
        "product": index.get("product", "CAVRA"),
        "evidence_mode": index.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_operating_release": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "gate_count": len(index.get("operating_gates", [])) if isinstance(index.get("operating_gates"), list) else 0,
        "required_gate_count": len(REQUIRED_OPERATING_GATES),
        "checks": checks,
    }


def write_managed_enterprise_operating_release_index_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_operating_release_index(evidence_mode="sample")
    live = build_managed_enterprise_operating_release_index(evidence_mode="live")
    sample_result = validate_managed_enterprise_operating_release_index(sample)
    live_result = validate_managed_enterprise_operating_release_index(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-operating-release-index.sample.json",
        "live_sanitized_example": output_dir / "managed-enterprise-operating-release-index.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-operating-release-index.sample.result.json",
        "live_result": output_dir / "managed-enterprise-operating-release-index.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.managed-enterprise-operating-release-index.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_operating_release": live_result["ready_for_managed_enterprise_operating_release"],
    }


def find_forbidden_operating_release_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_operating_release_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_operating_release_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(index: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = index.get("evidence_mode")
    sanitized = index.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized operating release index supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample operating release index validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Operating release requires evidence_mode=live and sanitized=true.")


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


def _check_operating_gates(gates: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(gates, list):
        _add_check(checks, "operating_gates", "blocker", "operating_gates must be a list.")
        return
    by_id = {gate.get("gate_id"): gate for gate in gates if isinstance(gate, dict)}
    missing_gate_ids = sorted(set(REQUIRED_OPERATING_GATES) - set(by_id))
    extra_gate_ids = sorted(set(by_id) - set(REQUIRED_OPERATING_GATES))
    failures: list[str] = []
    for gate_id in REQUIRED_OPERATING_GATES:
        gate = by_id.get(gate_id)
        if not isinstance(gate, dict):
            continue
        missing_fields = sorted(REQUIRED_GATE_FIELDS - set(gate))
        if missing_fields:
            failures.append(f"{gate_id} missing fields: {', '.join(missing_fields)}")
        for field in ("result_ref", "evidence_ref", "owner_ref", "status_ref"):
            if field in gate and not _is_ref(gate[field]):
                failures.append(f"{gate_id}.{field} must be a sanitized reference")
    if missing_gate_ids or extra_gate_ids or failures:
        details = []
        if missing_gate_ids:
            details.append(f"missing gates: {', '.join(missing_gate_ids)}")
        if extra_gate_ids:
            details.append(f"unexpected gates: {', '.join(extra_gate_ids)}")
        details.extend(failures)
        _add_check(checks, "operating_gates", "blocker", "; ".join(details))
    else:
        _add_check(checks, "operating_gates", "pass", "All required operating release gates are present.")


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
