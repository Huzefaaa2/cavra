from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.roadmap_candidate_charter import (
    build_roadmap_candidate_charter,
    validate_roadmap_candidate_charter,
)


ROADMAP_FUTURE_PHASE_OPENING_GATE_SCHEMA = "cavra.roadmap-future-phase-opening-gate.v1"
ROADMAP_FUTURE_PHASE_OPENING_GATE_RESULT_SCHEMA = "cavra.roadmap-future-phase-opening-gate.result.v1"

REQUIRED_PROFILE_FIELDS = {
    "architecture_owner_ref",
    "phase_candidate_ref",
    "phase_owner_ref",
    "product_owner_ref",
    "roadmap_boundary_ref",
    "source_charter_ref",
}

REQUIRED_PHASE_PLAN_FIELDS = {
    "dependency_refs",
    "exit_criteria_ref",
    "milestone_refs",
    "phase_name_ref",
    "problem_statement_ref",
    "scope_ref",
}

REQUIRED_OPENING_CONTROLS = {
    "backlog_ref",
    "docs_plan_ref",
    "implementation_plan_ref",
    "release_gate_ref",
    "rollback_plan_ref",
    "security_review_ref",
    "test_plan_ref",
}

REQUIRED_DECISION_FIELDS = {
    "decision_ref",
    "next_action_ref",
    "opening_decision",
    "target_phase_ref",
}

ALLOWED_OPENING_DECISIONS = {
    "needs_more_charter_detail",
    "ready_to_open_future_product_phase",
    "rejected_to_operations_evidence",
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
    "customer_email",
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
}

ALLOWED_REF_PREFIXES = (
    "architecture://",
    "charter://",
    "decision://",
    "docs://",
    "evidence://",
    "github://",
    "intake://",
    "phase://",
    "plan://",
    "product://",
    "roadmap://",
    "sample://",
    "security://",
    "test://",
    "workflow://",
)


def build_roadmap_future_phase_opening_gate(
    *,
    evidence_mode: str = "sample",
    requested_change_type: str = "new_product_capability",
) -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    candidate_charter = build_roadmap_candidate_charter(
        evidence_mode=evidence_mode,
        requested_change_type=requested_change_type,
    )
    candidate_result = validate_roadmap_candidate_charter(
        candidate_charter,
        require_live=evidence_mode == "live",
    )
    source_ready = (
        candidate_result.get("blocker_count") == 0
        and candidate_result.get("decision") == "ready_for_product_roadmap_planning"
    )
    opening_decision = (
        "ready_to_open_future_product_phase" if source_ready else "rejected_to_operations_evidence"
    )
    return {
        "schema_version": ROADMAP_FUTURE_PHASE_OPENING_GATE_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "source_candidate_charter_result": candidate_result,
        "phase_opening_profile": {
            "phase_candidate_ref": f"{prefix}://phase-candidate/{requested_change_type}",
            "source_charter_ref": f"{prefix}://charter/{requested_change_type}",
            "phase_owner_ref": f"{prefix}://owner/future-phase",
            "product_owner_ref": f"{prefix}://owner/product",
            "architecture_owner_ref": f"{prefix}://owner/architecture",
            "roadmap_boundary_ref": f"{prefix}://roadmap/phase-7-closeout-r7-61",
        },
        "phase_plan": {
            "phase_name_ref": f"{prefix}://phase/name/{requested_change_type}",
            "problem_statement_ref": f"{prefix}://phase/problem/{requested_change_type}",
            "scope_ref": f"{prefix}://phase/scope/{requested_change_type}",
            "milestone_refs": [
                f"{prefix}://phase/milestone/contract",
                f"{prefix}://phase/milestone/implementation",
                f"{prefix}://phase/milestone/validation",
            ],
            "dependency_refs": [
                f"{prefix}://dependency/roadmap-intake-gate",
                f"{prefix}://dependency/roadmap-candidate-charter",
                f"{prefix}://dependency/release-boundary",
            ],
            "exit_criteria_ref": f"{prefix}://phase/exit-criteria/{requested_change_type}",
        },
        "opening_controls": {
            "backlog_ref": f"{prefix}://github/backlog/{requested_change_type}",
            "implementation_plan_ref": f"{prefix}://plan/implementation/{requested_change_type}",
            "test_plan_ref": f"{prefix}://test/plan/{requested_change_type}",
            "docs_plan_ref": f"{prefix}://docs/plan/{requested_change_type}",
            "release_gate_ref": f"{prefix}://workflow/release-gate/{requested_change_type}",
            "rollback_plan_ref": f"{prefix}://plan/rollback/{requested_change_type}",
            "security_review_ref": f"{prefix}://security/review/{requested_change_type}",
        },
        "opening_decision": {
            "opening_decision": opening_decision,
            "decision_ref": f"{prefix}://decision/{opening_decision}",
            "next_action_ref": f"{prefix}://next-action/{opening_decision}",
            "target_phase_ref": f"{prefix}://roadmap/future-product-phase",
        },
        "redaction_controls": {control: True for control in sorted(REQUIRED_REDACTION_CONTROLS)},
    }


def validate_roadmap_future_phase_opening_gate(
    gate: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if gate.get("schema_version") == ROADMAP_FUTURE_PHASE_OPENING_GATE_SCHEMA else "blocker",
        "Roadmap future phase opening gate schema is valid."
        if gate.get("schema_version") == ROADMAP_FUTURE_PHASE_OPENING_GATE_SCHEMA
        else f"Gate must use {ROADMAP_FUTURE_PHASE_OPENING_GATE_SCHEMA}.",
    )
    _check_evidence_mode(gate, checks, require_live=require_live)
    _check_source_candidate_charter(
        gate.get("source_candidate_charter_result", {}),
        checks,
        require_live=require_live,
    )
    _check_ref_object(gate.get("phase_opening_profile", {}), checks, "phase_opening_profile", REQUIRED_PROFILE_FIELDS)
    _check_phase_plan(gate.get("phase_plan", {}), checks)
    _check_ref_object(gate.get("opening_controls", {}), checks, "opening_controls", REQUIRED_OPENING_CONTROLS)
    _check_opening_decision(gate.get("opening_decision", {}), checks)
    _check_redaction_controls(gate.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_roadmap_future_phase_opening_gate_fields(gate))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Roadmap future phase opening gate contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and gate.get("evidence_mode") == "live"
    phase_plan = gate.get("phase_plan", {})
    return {
        "schema_version": ROADMAP_FUTURE_PHASE_OPENING_GATE_RESULT_SCHEMA,
        "product": gate.get("product", "CAVRA"),
        "evidence_mode": gate.get("evidence_mode", "unknown"),
        "ready_for_roadmap_future_phase_opening": ready,
        "decision": gate.get("opening_decision", {}).get("opening_decision", "unknown"),
        "milestone_count": (
            len(phase_plan.get("milestone_refs", [])) if isinstance(phase_plan, dict) else 0
        ),
        "dependency_count": (
            len(phase_plan.get("dependency_refs", [])) if isinstance(phase_plan, dict) else 0
        ),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "checks": checks,
    }


def write_roadmap_future_phase_opening_gate_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_roadmap_future_phase_opening_gate(evidence_mode="sample")
    live = build_roadmap_future_phase_opening_gate(evidence_mode="live")
    rejected = build_roadmap_future_phase_opening_gate(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )
    sample_result = validate_roadmap_future_phase_opening_gate(sample)
    live_result = validate_roadmap_future_phase_opening_gate(live, require_live=True)
    rejected_result = validate_roadmap_future_phase_opening_gate(rejected, require_live=True)
    written = {
        "sample": output_dir / "roadmap-future-phase-opening-gate.sample.json",
        "live_candidate": output_dir / "roadmap-future-phase-opening-gate.live.sanitized.example.json",
        "rejected_operating": output_dir
        / "roadmap-future-phase-opening-gate.rejected-operating.live.sanitized.example.json",
        "sample_result": output_dir / "roadmap-future-phase-opening-gate.sample.result.json",
        "live_candidate_result": output_dir / "roadmap-future-phase-opening-gate.live.sanitized.result.json",
        "rejected_operating_result": output_dir
        / "roadmap-future-phase-opening-gate.rejected-operating.live.sanitized.result.json",
    }
    payloads = {
        "sample": sample,
        "live_candidate": live,
        "rejected_operating": rejected,
        "sample_result": sample_result,
        "live_candidate_result": live_result,
        "rejected_operating_result": rejected_result,
    }
    for name, payload in payloads.items():
        written[name].write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.roadmap-future-phase-opening-gate.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_roadmap_future_phase_opening": live_result["ready_for_roadmap_future_phase_opening"],
    }


def find_forbidden_roadmap_future_phase_opening_gate_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_roadmap_future_phase_opening_gate_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_roadmap_future_phase_opening_gate_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(gate: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = gate.get("evidence_mode")
    sanitized = gate.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized future phase opening gate supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample future phase opening gate validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Future phase opening gate requires evidence_mode=live and sanitized=true.",
        )


def _check_source_candidate_charter(charter: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(charter, dict):
        _add_check(
            checks,
            "source_candidate_charter_result",
            "blocker",
            "source_candidate_charter_result must be an object.",
        )
        return
    if charter.get("blocker_count") != 0:
        _add_check(checks, "source_candidate_charter_result", "blocker", "Source candidate charter has blockers.")
        return
    if require_live and charter.get("ready_for_roadmap_candidate_charter") is not True:
        _add_check(
            checks,
            "source_candidate_charter_result",
            "blocker",
            "Source candidate charter must be live and ready.",
        )
        return
    if charter.get("decision") != "ready_for_product_roadmap_planning":
        _add_check(
            checks,
            "source_candidate_charter_result",
            "blocker",
            "Future phase opening requires ready_for_product_roadmap_planning.",
        )
        return
    if not require_live and charter.get("ready_for_roadmap_candidate_charter") is not True:
        _add_check(
            checks,
            "source_candidate_charter_result",
            "warn",
            "Sample source candidate charter validates shape only.",
        )
        return
    _add_check(checks, "source_candidate_charter_result", "pass", "Source candidate charter is ready.")


def _check_ref_object(value: Any, checks: list[dict[str, str]], name: str, required_fields: set[str]) -> None:
    if not isinstance(value, dict):
        _add_check(checks, name, "blocker", f"{name} must be an object.")
        return
    missing = sorted(required_fields - set(value))
    invalid = sorted(key for key in required_fields if key in value and not _is_ref(value[key]))
    if missing or invalid:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        _add_check(checks, name, "blocker", "; ".join(details))
    else:
        _add_check(checks, name, "pass", f"{name} references are complete.")


def _check_phase_plan(plan: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(plan, dict):
        _add_check(checks, "phase_plan", "blocker", "phase_plan must be an object.")
        return
    missing = sorted(REQUIRED_PHASE_PLAN_FIELDS - set(plan))
    ref_fields = REQUIRED_PHASE_PLAN_FIELDS - {"dependency_refs", "milestone_refs"}
    invalid = sorted(key for key in ref_fields if key in plan and not _is_ref(plan[key]))
    list_failures = []
    for key in ("dependency_refs", "milestone_refs"):
        values = plan.get(key)
        if not isinstance(values, list) or not values or any(not _is_ref(value) for value in values):
            list_failures.append(f"{key} must be a non-empty list of sanitized refs")
    if missing or invalid or list_failures:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        details.extend(list_failures)
        _add_check(checks, "phase_plan", "blocker", "; ".join(details))
    else:
        _add_check(checks, "phase_plan", "pass", "Future phase plan references are complete.")


def _check_opening_decision(decision: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(decision, dict):
        _add_check(checks, "opening_decision", "blocker", "opening_decision must be an object.")
        return
    missing = sorted(REQUIRED_DECISION_FIELDS - set(decision))
    ref_fields = REQUIRED_DECISION_FIELDS - {"opening_decision"}
    invalid = sorted(key for key in ref_fields if key in decision and not _is_ref(decision[key]))
    opening_decision = decision.get("opening_decision")
    failures: list[str] = []
    if opening_decision not in ALLOWED_OPENING_DECISIONS:
        failures.append(f"opening_decision must be one of: {', '.join(sorted(ALLOWED_OPENING_DECISIONS))}")
    if opening_decision != "ready_to_open_future_product_phase":
        failures.append("future phase opening gates must be ready_to_open_future_product_phase")
    if missing or invalid or failures:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        details.extend(failures)
        _add_check(checks, "opening_decision", "blocker", "; ".join(details))
    else:
        _add_check(checks, "opening_decision", "pass", "Future phase opening decision is ready.")


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
