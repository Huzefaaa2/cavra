from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_sprint1_checkpoint import (
    build_customer_lifecycle_phase8_sprint1_checkpoint_packet,
    validate_customer_lifecycle_phase8_sprint1_checkpoint_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_SUPPORT_AUTOMATION_SCHEMA = (
    "cavra.customer-lifecycle-phase8-support-automation.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_SUPPORT_AUTOMATION_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-support-automation.result.v1"
)

REQUIRED_SUPPORT_OWNER_REFS = {
    "program_owner_ref",
    "support_owner_ref",
    "engineering_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
}

REQUIRED_SUPPORT_SCHEMA_FIELDS = {
    "checkpoint_ref",
    "support_case_ref",
    "escalation_ref",
    "owner_ref",
    "automation_trigger_ref",
    "status",
    "evidence_ref",
    "next_action_ref",
}

REQUIRED_TRIGGER_FIELDS = {
    "trigger_ref",
    "event_source_ref",
    "handler_ref",
    "delivery_channel_ref",
    "redaction_status",
}

REQUIRED_CI_GATES = {
    "schema_validation",
    "trigger_validation",
    "redaction_validation",
}

REQUIRED_SUPPORT_CONTROLS = {
    "sprint1_checkpoint_ready",
    "support_schema_defined",
    "automation_trigger_defined",
    "escalation_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_SUPPORT_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_name",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_contract",
    "raw_evidence",
    "renewal_amount",
    "secret",
    "token",
}


def build_customer_lifecycle_phase8_support_automation_packet(
    sprint1_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    sprint1 = sprint1_packet or build_customer_lifecycle_phase8_sprint1_checkpoint_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    sprint1_result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(
        sprint1,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_SUPPORT_AUTOMATION_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "support_automation_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-support-automation",
        "sprint1_checkpoint_ref": f"{prefix}://customer-lifecycle-phase8-sprint1-checkpoint/r7",
        "sprint1_checkpoint_result": sprint1_result,
        "support_owner_refs": {
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "support_owner_ref": f"{prefix}://owner/support",
            "engineering_owner_ref": f"{prefix}://owner/engineering-delivery",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
        },
        "support_checkpoint_schema": {
            "schema_ref": f"{prefix}://phase8/support-automation/checkpoint-schema",
            "schema_fields": sorted(REQUIRED_SUPPORT_SCHEMA_FIELDS),
            "version_ref": f"{prefix}://phase8/support-automation/checkpoint-schema/v1",
            "redaction_model_ref": f"{prefix}://phase8/support-automation/redaction-model",
        },
        "automation_trigger_contract": {
            "trigger_ref": f"{prefix}://phase8/support-automation/trigger",
            "event_source_ref": f"{prefix}://phase8/support-automation/sanitized-event-source",
            "handler_ref": f"{prefix}://phase8/support-automation/checkpoint-handler",
            "delivery_channel_ref": f"{prefix}://phase8/support-automation/support-delivery-channel",
            "redaction_status": "sanitized",
        },
        "escalation_matrix_refs": [
            f"{prefix}://phase8/support-automation/escalation/support",
            f"{prefix}://phase8/support-automation/escalation/security",
            f"{prefix}://phase8/support-automation/escalation/engineering",
        ],
        "ci_gate_coverage": {
            "schema_validation": f"{prefix}://ci/phase8/support-schema-validation",
            "trigger_validation": f"{prefix}://ci/phase8/support-trigger-validation",
            "redaction_validation": f"{prefix}://ci/phase8/support-redaction-validation",
        },
        "support_evidence_refs": [
            f"{prefix}://phase8/sprint1/support-progress",
            f"{prefix}://phase8/support-automation/checkpoint-schema",
            f"{prefix}://phase8/support-automation/trigger",
        ],
        "support_controls": {
            "sprint1_checkpoint_ready": sprint1_result["blocker_count"] == 0,
            "support_schema_defined": True,
            "automation_trigger_defined": True,
            "escalation_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_support_automation_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_SUPPORT_AUTOMATION_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 support automation schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_SUPPORT_AUTOMATION_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_SUPPORT_AUTOMATION_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("sprint1_checkpoint_ref"), checks, "sprint1_checkpoint_ref")
    _check_sprint1_result(packet.get("sprint1_checkpoint_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("support_owner_refs", {}), REQUIRED_SUPPORT_OWNER_REFS, checks)
    _check_support_schema(packet.get("support_checkpoint_schema", {}), checks)
    _check_trigger_contract(packet.get("automation_trigger_contract", {}), checks)
    _check_ref_list(packet.get("escalation_matrix_refs", []), checks, "escalation_matrix_refs", min_count=3)
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("support_evidence_refs", []), checks, "support_evidence_refs", min_count=3)
    _check_controls(packet.get("support_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_support_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 support automation contains sanitized refs and customer-safe support contract text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_SUPPORT_AUTOMATION_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_support_automation": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_support_automation_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_support_automation_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_support_automation_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_support_automation_packet(sample)
    live_result = validate_customer_lifecycle_phase8_support_automation_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-support-automation.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-phase8-support-automation.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-support-automation.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-support-automation.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-support-automation.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_support_automation": live_result[
            "ready_for_customer_lifecycle_phase8_support_automation"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 support automation supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 support automation validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Support automation requires evidence_mode=live and sanitized=true.")


def _check_sprint1_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "sprint1_checkpoint_result", "blocker", "sprint1_checkpoint_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_sprint1_checkpoint") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "sprint1_checkpoint_result", "pass", "Source Phase 8 Sprint 1 checkpoint is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "sprint1_checkpoint_result", "warn", "Source Sprint 1 checkpoint validates shape but is not live.")
    else:
        _add_check(checks, "sprint1_checkpoint_result", "blocker", "Source Sprint 1 checkpoint is not ready.")


def _check_required_refs(payload: Any, required: set[str], checks: list[dict[str, str]]) -> None:
    if not isinstance(payload, dict):
        _add_check(checks, "support_owner_refs", "blocker", "support_owner_refs must be an object.")
        return
    missing = sorted(field for field in required if not payload.get(field))
    unsafe = sorted(field for field, value in payload.items() if value and not _is_safe_ref(value))
    if not missing and not unsafe:
        _add_check(checks, "support_owner_refs", "pass", "support_owner_refs are present and sanitized.")
    else:
        problems = []
        if missing:
            problems.append(f"missing refs: {', '.join(missing)}")
        if unsafe:
            problems.append(f"unsafe refs: {', '.join(unsafe)}")
        _add_check(checks, "support_owner_refs", "blocker", f"support_owner_refs are invalid: {'; '.join(problems)}.")


def _check_support_schema(schema: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(schema, dict):
        _add_check(checks, "support_checkpoint_schema", "blocker", "support_checkpoint_schema must be an object.")
        return
    fields = set(schema.get("schema_fields", [])) if isinstance(schema.get("schema_fields"), list) else set()
    missing = sorted(REQUIRED_SUPPORT_SCHEMA_FIELDS - fields)
    safe_refs = all(
        _is_safe_ref(schema.get(field))
        for field in ("schema_ref", "version_ref", "redaction_model_ref")
    )
    _add_check(
        checks,
        "support_checkpoint_schema",
        "pass" if not missing and safe_refs else "blocker",
        "Support checkpoint schema fields and refs are complete."
        if not missing and safe_refs
        else f"Support checkpoint schema invalid: missing fields {', '.join(missing) or 'none'}; refs safe={safe_refs}.",
    )


def _check_trigger_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "automation_trigger_contract", "blocker", "automation_trigger_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_TRIGGER_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in ("trigger_ref", "event_source_ref", "handler_ref", "delivery_channel_ref")
        if contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "automation_trigger_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Automation trigger contract is complete."
        if not missing and not unsafe and redacted
        else f"Automation trigger contract invalid: missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}.",
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
        _add_check(checks, "support_controls", "blocker", "support_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_SUPPORT_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "support_controls",
        "pass" if not missing else "blocker",
        "Support automation controls are explicit."
        if not missing
        else f"Support automation controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_support_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_SUPPORT_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_support_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_support_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
