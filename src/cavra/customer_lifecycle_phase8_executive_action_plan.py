from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_executive_health_rollup import (
    build_customer_lifecycle_phase8_executive_health_rollup_packet,
    validate_customer_lifecycle_phase8_executive_health_rollup_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_ACTION_PLAN_SCHEMA = (
    "cavra.customer-lifecycle-phase8-executive-action-plan.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_ACTION_PLAN_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-executive-action-plan.result.v1"
)

REQUIRED_ACTION_OWNER_REFS = {
    "executive_owner_ref",
    "program_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
}

REQUIRED_ACTION_PLAN_FIELDS = {
    "action_plan_ref",
    "owner_matrix_ref",
    "due_window_ref",
    "acceptance_criteria_ref",
    "dependency_ref",
    "decision_log_ref",
    "redaction_status",
}

REQUIRED_ACTION_STREAMS = {
    "risk_posture_action_ref",
    "support_action_ref",
    "adoption_action_ref",
    "next_checkpoint_action_ref",
}

REQUIRED_CI_GATES = {
    "source_rollup_validation",
    "action_plan_validation",
    "commitment_ref_validation",
    "redaction_validation",
}

REQUIRED_ACTION_CONTROLS = {
    "executive_health_rollup_ready",
    "action_plan_defined",
    "owner_refs_defined",
    "due_windows_defined",
    "acceptance_refs_defined",
    "commitment_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_ACTION_PLAN_FIELDS = {
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


def build_customer_lifecycle_phase8_executive_action_plan_packet(
    executive_rollup_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    rollup = executive_rollup_packet or build_customer_lifecycle_phase8_executive_health_rollup_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    rollup_result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(
        rollup,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_ACTION_PLAN_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "executive_action_plan_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-executive-action-plan",
        "executive_health_rollup_ref": f"{prefix}://customer-lifecycle-phase8-executive-health-rollup/r7",
        "executive_health_rollup_result": rollup_result,
        "action_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "executive_action_plan_contract": {
            "action_plan_ref": f"{prefix}://phase8/executive-action-plan/plan",
            "owner_matrix_ref": f"{prefix}://phase8/executive-action-plan/owner-matrix",
            "due_window_ref": f"{prefix}://phase8/executive-action-plan/due-windows",
            "acceptance_criteria_ref": f"{prefix}://phase8/executive-action-plan/acceptance-criteria",
            "dependency_ref": f"{prefix}://phase8/executive-action-plan/dependencies",
            "decision_log_ref": f"{prefix}://phase8/executive-action-plan/decision-log",
            "redaction_status": "sanitized",
        },
        "action_commitment_refs": {
            "risk_posture_action_ref": f"{prefix}://phase8/executive-action-plan/action/risk-posture",
            "support_action_ref": f"{prefix}://phase8/executive-action-plan/action/support",
            "adoption_action_ref": f"{prefix}://phase8/executive-action-plan/action/adoption",
            "next_checkpoint_action_ref": f"{prefix}://phase8/executive-action-plan/action/next-checkpoint",
        },
        "ci_gate_coverage": {
            "source_rollup_validation": f"{prefix}://ci/phase8/executive-action-plan/source-rollup-validation",
            "action_plan_validation": f"{prefix}://ci/phase8/executive-action-plan/action-plan-validation",
            "commitment_ref_validation": f"{prefix}://ci/phase8/executive-action-plan/commitment-ref-validation",
            "redaction_validation": f"{prefix}://ci/phase8/executive-action-plan/redaction-validation",
        },
        "action_plan_evidence_refs": [
            f"{prefix}://phase8/executive-action-plan/source-rollup",
            f"{prefix}://phase8/executive-action-plan/plan-contract",
            f"{prefix}://phase8/executive-action-plan/commitments",
            f"{prefix}://phase8/executive-action-plan/acceptance",
        ],
        "action_plan_controls": {
            "executive_health_rollup_ready": rollup_result["blocker_count"] == 0,
            "action_plan_defined": True,
            "owner_refs_defined": True,
            "due_windows_defined": True,
            "acceptance_refs_defined": True,
            "commitment_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_executive_action_plan_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_ACTION_PLAN_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 executive action plan schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_ACTION_PLAN_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_ACTION_PLAN_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("executive_health_rollup_ref"), checks, "executive_health_rollup_ref")
    _check_rollup_result(packet.get("executive_health_rollup_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("action_owner_refs", {}), REQUIRED_ACTION_OWNER_REFS, checks, "action_owner_refs")
    _check_action_plan_contract(packet.get("executive_action_plan_contract", {}), checks)
    _check_required_refs(
        packet.get("action_commitment_refs", {}),
        REQUIRED_ACTION_STREAMS,
        checks,
        "action_commitment_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("action_plan_evidence_refs", []), checks, "action_plan_evidence_refs", min_count=4)
    _check_controls(packet.get("action_plan_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_action_plan_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 executive action plan contains sanitized refs and customer-safe action text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_ACTION_PLAN_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_executive_action_plan": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_executive_action_plan_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_executive_action_plan_packet(sample)
    live_result = validate_customer_lifecycle_phase8_executive_action_plan_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-executive-action-plan.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-phase8-executive-action-plan.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-executive-action-plan.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-executive-action-plan.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-executive-action-plan.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_executive_action_plan": live_result[
            "ready_for_customer_lifecycle_phase8_executive_action_plan"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 executive action plan supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 executive action plan validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Executive action plan requires evidence_mode=live and sanitized=true.")


def _check_rollup_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "executive_health_rollup_result", "blocker", "executive_health_rollup_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_executive_health_rollup") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "executive_health_rollup_result", "pass", "Source executive health rollup is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "executive_health_rollup_result", "warn", "Source executive health rollup validates shape but is not live.")
    else:
        _add_check(checks, "executive_health_rollup_result", "blocker", "Source executive health rollup is not ready.")


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


def _check_action_plan_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "executive_action_plan_contract", "blocker", "executive_action_plan_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_ACTION_PLAN_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_ACTION_PLAN_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "executive_action_plan_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Executive action plan contract is complete."
        if not missing and not unsafe and redacted
        else f"Executive action plan contract invalid: missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}.",
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
        _add_check(checks, "action_plan_controls", "blocker", "action_plan_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_ACTION_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "action_plan_controls",
        "pass" if not missing else "blocker",
        "Executive action plan controls are explicit."
        if not missing
        else f"Executive action plan controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_action_plan_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_ACTION_PLAN_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_action_plan_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_action_plan_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
