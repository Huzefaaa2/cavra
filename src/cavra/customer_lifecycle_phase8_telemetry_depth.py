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


CUSTOMER_LIFECYCLE_PHASE8_TELEMETRY_DEPTH_SCHEMA = "cavra.customer-lifecycle-phase8-telemetry-depth.packet.v1"
CUSTOMER_LIFECYCLE_PHASE8_TELEMETRY_DEPTH_RESULT_SCHEMA = "cavra.customer-lifecycle-phase8-telemetry-depth.result.v1"

REQUIRED_TELEMETRY_OWNER_REFS = {
    "program_owner_ref",
    "security_owner_ref",
    "engineering_owner_ref",
    "analytics_owner_ref",
}

REQUIRED_TELEMETRY_SCHEMA_FIELDS = {
    "runtime_event_ref",
    "decision_ref",
    "policy_ref",
    "agent_ref",
    "tool_ref",
    "risk_score",
    "posture_signal",
    "evidence_ref",
}

REQUIRED_FIXTURE_FIELDS = {
    "fixture_ref",
    "source_event_ref",
    "decision_ref",
    "policy_ref",
    "posture_signal",
    "redaction_status",
}

REQUIRED_CI_GATES = {
    "schema_validation",
    "fixture_validation",
    "redaction_validation",
}

REQUIRED_TELEMETRY_CONTROLS = {
    "sprint1_checkpoint_ready",
    "schema_fields_defined",
    "live_fixture_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_TELEMETRY_FIELDS = {
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


def build_customer_lifecycle_phase8_telemetry_depth_packet(
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
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_TELEMETRY_DEPTH_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "telemetry_depth_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-telemetry-depth",
        "sprint1_checkpoint_ref": f"{prefix}://customer-lifecycle-phase8-sprint1-checkpoint/r7",
        "sprint1_checkpoint_result": sprint1_result,
        "telemetry_owner_refs": {
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "engineering_owner_ref": f"{prefix}://owner/engineering-delivery",
            "analytics_owner_ref": f"{prefix}://owner/product-analytics",
        },
        "telemetry_schema": {
            "schema_ref": f"{prefix}://phase8/telemetry-depth/schema",
            "schema_fields": sorted(REQUIRED_TELEMETRY_SCHEMA_FIELDS),
            "version_ref": f"{prefix}://phase8/telemetry-depth/schema/v1",
            "redaction_model_ref": f"{prefix}://phase8/telemetry-depth/redaction-model",
        },
        "live_sanitized_fixture": {
            "fixture_ref": f"{prefix}://phase8/telemetry-depth/live-sanitized-fixture",
            "source_event_ref": f"{prefix}://runtime/event/sanitized-agent-action",
            "decision_ref": f"{prefix}://runtime/decision/approval-required",
            "policy_ref": f"{prefix}://policy/runtime-authority/default",
            "posture_signal": "agent-action-risk-reviewed",
            "redaction_status": "sanitized",
        },
        "ci_gate_coverage": {
            "schema_validation": f"{prefix}://ci/phase8/telemetry-schema-validation",
            "fixture_validation": f"{prefix}://ci/phase8/telemetry-fixture-validation",
            "redaction_validation": f"{prefix}://ci/phase8/telemetry-redaction-validation",
        },
        "telemetry_evidence_refs": [
            f"{prefix}://phase8/sprint1/telemetry-progress",
            f"{prefix}://phase8/telemetry-depth/schema",
            f"{prefix}://phase8/telemetry-depth/live-sanitized-fixture",
        ],
        "telemetry_controls": {
            "sprint1_checkpoint_ready": sprint1_result["blocker_count"] == 0,
            "schema_fields_defined": True,
            "live_fixture_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_telemetry_depth_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_TELEMETRY_DEPTH_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 telemetry depth schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_TELEMETRY_DEPTH_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_TELEMETRY_DEPTH_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("sprint1_checkpoint_ref"), checks, "sprint1_checkpoint_ref")
    _check_sprint1_result(packet.get("sprint1_checkpoint_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("telemetry_owner_refs", {}), REQUIRED_TELEMETRY_OWNER_REFS, checks)
    _check_telemetry_schema(packet.get("telemetry_schema", {}), checks)
    _check_live_fixture(packet.get("live_sanitized_fixture", {}), checks)
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_evidence_refs(packet.get("telemetry_evidence_refs", []), checks)
    _check_controls(packet.get("telemetry_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_telemetry_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 telemetry depth contains sanitized refs and customer-safe telemetry contract text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_TELEMETRY_DEPTH_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_telemetry_depth": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_telemetry_depth_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_telemetry_depth_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_telemetry_depth_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_telemetry_depth_packet(sample)
    live_result = validate_customer_lifecycle_phase8_telemetry_depth_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-telemetry-depth.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-phase8-telemetry-depth.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-telemetry-depth.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-telemetry-depth.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-telemetry-depth.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_telemetry_depth": live_result[
            "ready_for_customer_lifecycle_phase8_telemetry_depth"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 telemetry depth supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 telemetry depth validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Telemetry depth requires evidence_mode=live and sanitized=true.")


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


def _check_required_refs(
    payload: Any,
    required: set[str],
    checks: list[dict[str, str]],
) -> None:
    if not isinstance(payload, dict):
        _add_check(checks, "telemetry_owner_refs", "blocker", "telemetry_owner_refs must be an object.")
        return
    missing = sorted(field for field in required if not payload.get(field))
    unsafe = sorted(field for field, value in payload.items() if value and not _is_safe_ref(value))
    if not missing and not unsafe:
        _add_check(checks, "telemetry_owner_refs", "pass", "telemetry_owner_refs are present and sanitized.")
    else:
        problems = []
        if missing:
            problems.append(f"missing refs: {', '.join(missing)}")
        if unsafe:
            problems.append(f"unsafe refs: {', '.join(unsafe)}")
        _add_check(checks, "telemetry_owner_refs", "blocker", f"telemetry_owner_refs are invalid: {'; '.join(problems)}.")


def _check_telemetry_schema(schema: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(schema, dict):
        _add_check(checks, "telemetry_schema", "blocker", "telemetry_schema must be an object.")
        return
    fields = set(schema.get("schema_fields", [])) if isinstance(schema.get("schema_fields"), list) else set()
    missing = sorted(REQUIRED_TELEMETRY_SCHEMA_FIELDS - fields)
    safe_refs = all(
        _is_safe_ref(schema.get(field))
        for field in ("schema_ref", "version_ref", "redaction_model_ref")
    )
    _add_check(
        checks,
        "telemetry_schema",
        "pass" if not missing and safe_refs else "blocker",
        "Telemetry schema fields and refs are complete."
        if not missing and safe_refs
        else f"Telemetry schema invalid: missing fields {', '.join(missing) or 'none'}; refs safe={safe_refs}.",
    )


def _check_live_fixture(fixture: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(fixture, dict):
        _add_check(checks, "live_sanitized_fixture", "blocker", "live_sanitized_fixture must be an object.")
        return
    missing = sorted(field for field in REQUIRED_FIXTURE_FIELDS if not fixture.get(field))
    unsafe = sorted(
        field
        for field in ("fixture_ref", "source_event_ref", "decision_ref", "policy_ref")
        if fixture.get(field) and not _is_safe_ref(fixture.get(field))
    )
    redacted = fixture.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "live_sanitized_fixture",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Live sanitized telemetry fixture is complete."
        if not missing and not unsafe and redacted
        else f"Live sanitized telemetry fixture invalid: missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}.",
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


def _check_evidence_refs(refs: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(refs, list) or len(refs) < 3:
        _add_check(checks, "telemetry_evidence_refs", "blocker", "telemetry_evidence_refs must contain at least 3 refs.")
        return
    unsafe = [str(ref) for ref in refs if not _is_safe_ref(ref)]
    _add_check(
        checks,
        "telemetry_evidence_refs",
        "pass" if not unsafe else "blocker",
        "Telemetry evidence refs are sanitized."
        if not unsafe
        else f"Telemetry evidence refs are unsafe: {', '.join(unsafe)}.",
    )


def _check_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "telemetry_controls", "blocker", "telemetry_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_TELEMETRY_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "telemetry_controls",
        "pass" if not missing else "blocker",
        "Telemetry depth controls are explicit."
        if not missing
        else f"Telemetry depth controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_telemetry_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_TELEMETRY_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_telemetry_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_telemetry_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
