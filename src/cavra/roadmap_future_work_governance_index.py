from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.roadmap_candidate_charter import (
    build_roadmap_candidate_charter,
    validate_roadmap_candidate_charter,
)
from cavra.roadmap_future_phase_opening_gate import (
    build_roadmap_future_phase_opening_gate,
    validate_roadmap_future_phase_opening_gate,
)
from cavra.roadmap_future_phase_registry import (
    build_roadmap_future_phase_registry,
    validate_roadmap_future_phase_registry,
)
from cavra.roadmap_intake_gate import (
    build_roadmap_intake_gate_packet,
    validate_roadmap_intake_gate_packet,
)


ROADMAP_FUTURE_WORK_GOVERNANCE_INDEX_SCHEMA = "cavra.roadmap-future-work-governance-index.v1"
ROADMAP_FUTURE_WORK_GOVERNANCE_INDEX_RESULT_SCHEMA = "cavra.roadmap-future-work-governance-index.result.v1"

REQUIRED_PROFILE_FIELDS = {
    "governance_index_ref",
    "governance_owner_ref",
    "review_cadence_ref",
    "roadmap_boundary_ref",
    "source_candidate_charter_ref",
    "source_future_phase_opening_gate_ref",
    "source_future_phase_registry_ref",
    "source_intake_gate_ref",
}

REQUIRED_GOVERNANCE_CONTROLS = {
    "docs_sync_ref",
    "evidence_boundary_ref",
    "registration_policy_ref",
    "release_guard_ref",
    "rollback_policy_ref",
    "status_report_ref",
    "wiki_sync_ref",
}

REQUIRED_DECISION_FIELDS = {
    "decision_ref",
    "governance_decision",
    "next_action_ref",
    "target_boundary_ref",
}

ALLOWED_GOVERNANCE_DECISIONS = {
    "ready_to_close_future_work_governance_chain",
    "rejected_to_prior_gate",
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
    "governance://",
    "intake://",
    "phase://",
    "plan://",
    "product://",
    "registry://",
    "roadmap://",
    "sample://",
    "security://",
    "test://",
    "workflow://",
)


def build_roadmap_future_work_governance_index(
    *,
    evidence_mode: str = "sample",
    requested_change_type: str = "new_product_capability",
) -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    intake = build_roadmap_intake_gate_packet(
        evidence_mode=evidence_mode,
        requested_change_type=requested_change_type,
    )
    charter = build_roadmap_candidate_charter(
        evidence_mode=evidence_mode,
        requested_change_type=requested_change_type,
    )
    opening_gate = build_roadmap_future_phase_opening_gate(
        evidence_mode=evidence_mode,
        requested_change_type=requested_change_type,
    )
    registry = build_roadmap_future_phase_registry(
        evidence_mode=evidence_mode,
        requested_change_type=requested_change_type,
    )
    require_live = evidence_mode == "live"
    intake_result = validate_roadmap_intake_gate_packet(intake, require_live=require_live)
    charter_result = validate_roadmap_candidate_charter(charter, require_live=require_live)
    opening_result = validate_roadmap_future_phase_opening_gate(opening_gate, require_live=require_live)
    registry_result = validate_roadmap_future_phase_registry(registry, require_live=require_live)
    source_ready = (
        intake_result.get("blocker_count") == 0
        and intake_result.get("decision") == "new_product_roadmap_candidate"
        and charter_result.get("blocker_count") == 0
        and charter_result.get("decision") == "ready_for_product_roadmap_planning"
        and opening_result.get("blocker_count") == 0
        and opening_result.get("decision") == "ready_to_open_future_product_phase"
        and registry_result.get("blocker_count") == 0
        and registry_result.get("decision") == "ready_to_register_future_phase"
    )
    governance_decision = (
        "ready_to_close_future_work_governance_chain" if source_ready else "rejected_to_prior_gate"
    )
    return {
        "schema_version": ROADMAP_FUTURE_WORK_GOVERNANCE_INDEX_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "source_results": {
            "roadmap_intake_gate": intake_result,
            "roadmap_candidate_charter": charter_result,
            "roadmap_future_phase_opening_gate": opening_result,
            "roadmap_future_phase_registry": registry_result,
        },
        "governance_profile": {
            "governance_index_ref": f"{prefix}://governance/future-work-index/{requested_change_type}",
            "source_intake_gate_ref": f"{prefix}://intake/{requested_change_type}",
            "source_candidate_charter_ref": f"{prefix}://charter/{requested_change_type}",
            "source_future_phase_opening_gate_ref": f"{prefix}://phase-opening-gate/{requested_change_type}",
            "source_future_phase_registry_ref": f"{prefix}://registry/future-phase/{requested_change_type}",
            "governance_owner_ref": f"{prefix}://owner/product-operations",
            "review_cadence_ref": f"{prefix}://workflow/future-work-governance-review",
            "roadmap_boundary_ref": f"{prefix}://roadmap/phase-7-closeout-r7-61",
        },
        "governance_controls": {
            "registration_policy_ref": f"{prefix}://governance/registration-policy",
            "status_report_ref": f"{prefix}://docs/status/future-work-governance",
            "release_guard_ref": f"{prefix}://workflow/roadmap-completion-boundary",
            "docs_sync_ref": f"{prefix}://docs/sync/future-work-governance",
            "wiki_sync_ref": f"{prefix}://docs/wiki-sync/future-work-governance",
            "evidence_boundary_ref": f"{prefix}://security/evidence-boundary",
            "rollback_policy_ref": f"{prefix}://plan/rollback/future-work-registration",
        },
        "governance_decision": {
            "governance_decision": governance_decision,
            "decision_ref": f"{prefix}://decision/{governance_decision}",
            "next_action_ref": f"{prefix}://next-action/{governance_decision}",
            "target_boundary_ref": f"{prefix}://roadmap/phase-7-closeout-r7-61",
        },
        "redaction_controls": {control: True for control in sorted(REQUIRED_REDACTION_CONTROLS)},
    }


def validate_roadmap_future_work_governance_index(
    index: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if index.get("schema_version") == ROADMAP_FUTURE_WORK_GOVERNANCE_INDEX_SCHEMA else "blocker",
        "Roadmap future work governance index schema is valid."
        if index.get("schema_version") == ROADMAP_FUTURE_WORK_GOVERNANCE_INDEX_SCHEMA
        else f"Index must use {ROADMAP_FUTURE_WORK_GOVERNANCE_INDEX_SCHEMA}.",
    )
    _check_evidence_mode(index, checks, require_live=require_live)
    _check_source_results(index.get("source_results", {}), checks, require_live=require_live)
    _check_ref_object(index.get("governance_profile", {}), checks, "governance_profile", REQUIRED_PROFILE_FIELDS)
    _check_ref_object(
        index.get("governance_controls", {}),
        checks,
        "governance_controls",
        REQUIRED_GOVERNANCE_CONTROLS,
    )
    _check_governance_decision(index.get("governance_decision", {}), checks)
    _check_redaction_controls(index.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_roadmap_future_work_governance_index_fields(index))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Roadmap future work governance index contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and index.get("evidence_mode") == "live"
    source_results = index.get("source_results", {})
    return {
        "schema_version": ROADMAP_FUTURE_WORK_GOVERNANCE_INDEX_RESULT_SCHEMA,
        "product": index.get("product", "CAVRA"),
        "evidence_mode": index.get("evidence_mode", "unknown"),
        "ready_for_roadmap_future_work_governance_index": ready,
        "decision": index.get("governance_decision", {}).get("governance_decision", "unknown"),
        "source_gate_count": len(source_results) if isinstance(source_results, dict) else 0,
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "checks": checks,
    }


def write_roadmap_future_work_governance_index_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_roadmap_future_work_governance_index(evidence_mode="sample")
    live = build_roadmap_future_work_governance_index(evidence_mode="live")
    rejected = build_roadmap_future_work_governance_index(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )
    sample_result = validate_roadmap_future_work_governance_index(sample)
    live_result = validate_roadmap_future_work_governance_index(live, require_live=True)
    rejected_result = validate_roadmap_future_work_governance_index(rejected, require_live=True)
    written = {
        "sample": output_dir / "roadmap-future-work-governance-index.sample.json",
        "live_candidate": output_dir / "roadmap-future-work-governance-index.live.sanitized.example.json",
        "rejected_operating": output_dir
        / "roadmap-future-work-governance-index.rejected-operating.live.sanitized.example.json",
        "sample_result": output_dir / "roadmap-future-work-governance-index.sample.result.json",
        "live_candidate_result": output_dir / "roadmap-future-work-governance-index.live.sanitized.result.json",
        "rejected_operating_result": output_dir
        / "roadmap-future-work-governance-index.rejected-operating.live.sanitized.result.json",
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
        "schema_version": "cavra.roadmap-future-work-governance-index.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_roadmap_future_work_governance_index": live_result[
            "ready_for_roadmap_future_work_governance_index"
        ],
    }


def find_forbidden_roadmap_future_work_governance_index_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_roadmap_future_work_governance_index_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_roadmap_future_work_governance_index_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(index: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = index.get("evidence_mode")
    sanitized = index.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized future work governance index supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample future work governance index validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Future work governance index requires evidence_mode=live and sanitized=true.",
        )


def _check_source_results(source_results: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(source_results, dict):
        _add_check(checks, "source_results", "blocker", "source_results must be an object.")
        return
    expected = {
        "roadmap_intake_gate": (
            "ready_for_roadmap_intake_decision",
            "new_product_roadmap_candidate",
        ),
        "roadmap_candidate_charter": (
            "ready_for_roadmap_candidate_charter",
            "ready_for_product_roadmap_planning",
        ),
        "roadmap_future_phase_opening_gate": (
            "ready_for_roadmap_future_phase_opening",
            "ready_to_open_future_product_phase",
        ),
        "roadmap_future_phase_registry": (
            "ready_for_roadmap_future_phase_registry",
            "ready_to_register_future_phase",
        ),
    }
    failures: list[str] = []
    warnings: list[str] = []
    for gate_name, (ready_key, decision) in expected.items():
        result = source_results.get(gate_name)
        if not isinstance(result, dict):
            failures.append(f"{gate_name} result is missing")
            continue
        if result.get("blocker_count") != 0:
            failures.append(f"{gate_name} has blockers")
        if result.get("decision") != decision:
            failures.append(f"{gate_name} decision must be {decision}")
        if require_live and result.get(ready_key) is not True:
            failures.append(f"{gate_name} must be live and ready")
        if not require_live and result.get(ready_key) is not True:
            warnings.append(f"{gate_name} is sample or not ready")
    if failures:
        _add_check(checks, "source_results", "blocker", "; ".join(failures))
    elif warnings:
        _add_check(checks, "source_results", "warn", "; ".join(warnings))
    else:
        _add_check(checks, "source_results", "pass", "All future work governance source gates are ready.")


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


def _check_governance_decision(decision: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(decision, dict):
        _add_check(checks, "governance_decision", "blocker", "governance_decision must be an object.")
        return
    missing = sorted(REQUIRED_DECISION_FIELDS - set(decision))
    ref_fields = REQUIRED_DECISION_FIELDS - {"governance_decision"}
    invalid = sorted(key for key in ref_fields if key in decision and not _is_ref(decision[key]))
    governance_decision = decision.get("governance_decision")
    failures: list[str] = []
    if governance_decision not in ALLOWED_GOVERNANCE_DECISIONS:
        failures.append(
            f"governance_decision must be one of: {', '.join(sorted(ALLOWED_GOVERNANCE_DECISIONS))}"
        )
    if governance_decision != "ready_to_close_future_work_governance_chain":
        failures.append("future work governance indexes must be ready_to_close_future_work_governance_chain")
    if missing or invalid or failures:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        details.extend(failures)
        _add_check(checks, "governance_decision", "blocker", "; ".join(details))
    else:
        _add_check(checks, "governance_decision", "pass", "Future work governance chain is ready.")


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
