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


CUSTOMER_LIFECYCLE_PHASE8_LIFECYCLE_ANALYTICS_SCHEMA = (
    "cavra.customer-lifecycle-phase8-lifecycle-analytics.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_LIFECYCLE_ANALYTICS_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-lifecycle-analytics.result.v1"
)

REQUIRED_ANALYTICS_OWNER_REFS = {
    "program_owner_ref",
    "analytics_owner_ref",
    "security_owner_ref",
    "customer_success_owner_ref",
    "product_owner_ref",
}

REQUIRED_ANALYTICS_INPUT_FIELDS = {
    "analytics_event_ref",
    "source_signal_ref",
    "posture_signal",
    "adoption_signal",
    "cadence_signal",
    "evidence_ref",
    "redaction_status",
}

REQUIRED_DASHBOARD_OUTPUT_FIELDS = {
    "posture_summary_ref",
    "adoption_summary_ref",
    "cadence_summary_ref",
    "trend_ref",
    "executive_summary_ref",
    "redaction_status",
}

REQUIRED_SUMMARY_REFS = {
    "posture_summary_ref",
    "adoption_summary_ref",
    "cadence_summary_ref",
}

REQUIRED_CI_GATES = {
    "input_validation",
    "dashboard_output_validation",
    "summary_validation",
    "redaction_validation",
}

REQUIRED_ANALYTICS_CONTROLS = {
    "sprint1_checkpoint_ready",
    "analytics_input_contract_defined",
    "dashboard_outputs_defined",
    "summary_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_ANALYTICS_FIELDS = {
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


def build_customer_lifecycle_phase8_lifecycle_analytics_packet(
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
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_LIFECYCLE_ANALYTICS_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "lifecycle_analytics_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-lifecycle-analytics",
        "sprint1_checkpoint_ref": f"{prefix}://customer-lifecycle-phase8-sprint1-checkpoint/r7",
        "sprint1_checkpoint_result": sprint1_result,
        "analytics_owner_refs": {
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "analytics_owner_ref": f"{prefix}://owner/product-analytics",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "analytics_input_contract": {
            "contract_ref": f"{prefix}://phase8/lifecycle-analytics/input-contract",
            "schema_fields": sorted(REQUIRED_ANALYTICS_INPUT_FIELDS),
            "version_ref": f"{prefix}://phase8/lifecycle-analytics/input-contract/v1",
            "redaction_model_ref": f"{prefix}://phase8/lifecycle-analytics/redaction-model",
        },
        "dashboard_safe_outputs": {
            "posture_summary_ref": f"{prefix}://phase8/lifecycle-analytics/dashboard/posture-summary",
            "adoption_summary_ref": f"{prefix}://phase8/lifecycle-analytics/dashboard/adoption-summary",
            "cadence_summary_ref": f"{prefix}://phase8/lifecycle-analytics/dashboard/cadence-summary",
            "trend_ref": f"{prefix}://phase8/lifecycle-analytics/dashboard/trends",
            "executive_summary_ref": f"{prefix}://phase8/lifecycle-analytics/dashboard/executive-summary",
            "redaction_status": "sanitized",
        },
        "lifecycle_summary_refs": {
            "posture_summary_ref": f"{prefix}://phase8/lifecycle-analytics/summary/posture",
            "adoption_summary_ref": f"{prefix}://phase8/lifecycle-analytics/summary/adoption",
            "cadence_summary_ref": f"{prefix}://phase8/lifecycle-analytics/summary/cadence",
        },
        "ci_gate_coverage": {
            "input_validation": f"{prefix}://ci/phase8/lifecycle-analytics/input-validation",
            "dashboard_output_validation": f"{prefix}://ci/phase8/lifecycle-analytics/dashboard-output-validation",
            "summary_validation": f"{prefix}://ci/phase8/lifecycle-analytics/summary-validation",
            "redaction_validation": f"{prefix}://ci/phase8/lifecycle-analytics/redaction-validation",
        },
        "analytics_evidence_refs": [
            f"{prefix}://phase8/sprint1/analytics-progress",
            f"{prefix}://phase8/lifecycle-analytics/input-contract",
            f"{prefix}://phase8/lifecycle-analytics/dashboard-safe-outputs",
            f"{prefix}://phase8/lifecycle-analytics/summary-refs",
        ],
        "analytics_controls": {
            "sprint1_checkpoint_ready": sprint1_result["blocker_count"] == 0,
            "analytics_input_contract_defined": True,
            "dashboard_outputs_defined": True,
            "summary_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_lifecycle_analytics_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_LIFECYCLE_ANALYTICS_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 lifecycle analytics schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_LIFECYCLE_ANALYTICS_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_LIFECYCLE_ANALYTICS_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("sprint1_checkpoint_ref"), checks, "sprint1_checkpoint_ref")
    _check_sprint1_result(packet.get("sprint1_checkpoint_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("analytics_owner_refs", {}), REQUIRED_ANALYTICS_OWNER_REFS, checks)
    _check_analytics_input_contract(packet.get("analytics_input_contract", {}), checks)
    _check_dashboard_safe_outputs(packet.get("dashboard_safe_outputs", {}), checks)
    _check_summary_refs(packet.get("lifecycle_summary_refs", {}), checks)
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("analytics_evidence_refs", []), checks, "analytics_evidence_refs", min_count=4)
    _check_controls(packet.get("analytics_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_analytics_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 lifecycle analytics contains sanitized refs and customer-safe analytics contract text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_LIFECYCLE_ANALYTICS_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_lifecycle_analytics": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_lifecycle_analytics_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(sample)
    live_result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-lifecycle-analytics.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-phase8-lifecycle-analytics.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-lifecycle-analytics.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-lifecycle-analytics.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-lifecycle-analytics.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_lifecycle_analytics": live_result[
            "ready_for_customer_lifecycle_phase8_lifecycle_analytics"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 lifecycle analytics supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 lifecycle analytics validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Lifecycle analytics requires evidence_mode=live and sanitized=true.")


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
        _add_check(checks, "analytics_owner_refs", "blocker", "analytics_owner_refs must be an object.")
        return
    missing = sorted(field for field in required if not payload.get(field))
    unsafe = sorted(field for field, value in payload.items() if value and not _is_safe_ref(value))
    if not missing and not unsafe:
        _add_check(checks, "analytics_owner_refs", "pass", "analytics_owner_refs are present and sanitized.")
    else:
        problems = []
        if missing:
            problems.append(f"missing refs: {', '.join(missing)}")
        if unsafe:
            problems.append(f"unsafe refs: {', '.join(unsafe)}")
        _add_check(checks, "analytics_owner_refs", "blocker", f"analytics_owner_refs are invalid: {'; '.join(problems)}.")


def _check_analytics_input_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "analytics_input_contract", "blocker", "analytics_input_contract must be an object.")
        return
    fields = set(contract.get("schema_fields", [])) if isinstance(contract.get("schema_fields"), list) else set()
    missing = sorted(REQUIRED_ANALYTICS_INPUT_FIELDS - fields)
    safe_refs = all(
        _is_safe_ref(contract.get(field))
        for field in ("contract_ref", "version_ref", "redaction_model_ref")
    )
    _add_check(
        checks,
        "analytics_input_contract",
        "pass" if not missing and safe_refs else "blocker",
        "Analytics input contract fields and refs are complete."
        if not missing and safe_refs
        else f"Analytics input contract invalid: missing fields {', '.join(missing) or 'none'}; refs safe={safe_refs}.",
    )


def _check_dashboard_safe_outputs(outputs: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(outputs, dict):
        _add_check(checks, "dashboard_safe_outputs", "blocker", "dashboard_safe_outputs must be an object.")
        return
    missing = sorted(field for field in REQUIRED_DASHBOARD_OUTPUT_FIELDS if not outputs.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_DASHBOARD_OUTPUT_FIELDS
        if field.endswith("_ref") and outputs.get(field) and not _is_safe_ref(outputs.get(field))
    )
    redacted = outputs.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "dashboard_safe_outputs",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Dashboard-safe analytics outputs are complete."
        if not missing and not unsafe and redacted
        else f"Dashboard outputs invalid: missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}.",
    )


def _check_summary_refs(summaries: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(summaries, dict):
        _add_check(checks, "lifecycle_summary_refs", "blocker", "lifecycle_summary_refs must be an object.")
        return
    missing = sorted(field for field in REQUIRED_SUMMARY_REFS if not summaries.get(field))
    unsafe = sorted(field for field, value in summaries.items() if value and not _is_safe_ref(value))
    _add_check(
        checks,
        "lifecycle_summary_refs",
        "pass" if not missing and not unsafe else "blocker",
        "Lifecycle posture, adoption, and cadence summary refs are complete."
        if not missing and not unsafe
        else f"Lifecycle summary refs invalid: missing {', '.join(missing) or 'none'}; unsafe {', '.join(unsafe) or 'none'}.",
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
        _add_check(checks, "analytics_controls", "blocker", "analytics_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_ANALYTICS_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "analytics_controls",
        "pass" if not missing else "blocker",
        "Lifecycle analytics controls are explicit."
        if not missing
        else f"Lifecycle analytics controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_analytics_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_ANALYTICS_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_analytics_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_analytics_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
