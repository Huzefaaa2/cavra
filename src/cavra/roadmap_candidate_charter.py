from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.roadmap_intake_gate import (
    PRODUCT_ROADMAP_CHANGE_TYPES,
    build_roadmap_intake_gate_packet,
    validate_roadmap_intake_gate_packet,
)


ROADMAP_CANDIDATE_CHARTER_SCHEMA = "cavra.roadmap-candidate-charter.v1"
ROADMAP_CANDIDATE_CHARTER_RESULT_SCHEMA = "cavra.roadmap-candidate-charter.result.v1"

REQUIRED_PROFILE_FIELDS = {
    "candidate_id_ref",
    "source_intake_ref",
    "sponsor_ref",
    "product_owner_ref",
    "architecture_owner_ref",
    "roadmap_boundary_ref",
}

REQUIRED_SCOPE_FIELDS = {
    "capability_statement_ref",
    "included_surface_refs",
    "excluded_scope_ref",
    "dependency_refs",
    "customer_value_ref",
}

REQUIRED_ACCEPTANCE_CRITERIA = {
    "api_or_cli_contract_defined",
    "docs_surface_defined",
    "evidence_model_defined",
    "public_contract_boundary_defined",
    "release_gate_defined",
    "security_boundary_defined",
    "test_plan_defined",
}

REQUIRED_ACCEPTANCE_FIELDS = {
    "criterion_id",
    "status",
    "evidence_ref",
    "owner_ref",
}

REQUIRED_RELEASE_FIELDS = {
    "implementation_plan_ref",
    "test_plan_ref",
    "docs_plan_ref",
    "rollback_plan_ref",
    "release_owner_ref",
    "review_cadence_ref",
}

REQUIRED_DECISION_FIELDS = {
    "charter_decision",
    "decision_ref",
    "next_action_ref",
    "target_phase_ref",
}

ALLOWED_CHARTER_DECISIONS = {
    "ready_for_product_roadmap_planning",
    "needs_more_scope",
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
    "plan://",
    "product://",
    "roadmap://",
    "sample://",
    "security://",
    "test://",
    "workflow://",
)


def build_roadmap_candidate_charter(
    *,
    evidence_mode: str = "sample",
    requested_change_type: str = "new_product_capability",
) -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    intake_packet = build_roadmap_intake_gate_packet(
        evidence_mode=evidence_mode,
        requested_change_type=requested_change_type,
    )
    intake_result = validate_roadmap_intake_gate_packet(
        intake_packet,
        require_live=evidence_mode == "live",
    )
    is_product_candidate = requested_change_type in PRODUCT_ROADMAP_CHANGE_TYPES
    charter_decision = (
        "ready_for_product_roadmap_planning"
        if is_product_candidate
        else "rejected_to_operations_evidence"
    )
    return {
        "schema_version": ROADMAP_CANDIDATE_CHARTER_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "source_intake_result": intake_result,
        "charter_profile": {
            "candidate_id_ref": f"{prefix}://roadmap-candidate/{requested_change_type}",
            "source_intake_ref": f"{prefix}://roadmap-intake/{requested_change_type}",
            "sponsor_ref": f"{prefix}://owner/product-sponsor",
            "product_owner_ref": f"{prefix}://owner/product",
            "architecture_owner_ref": f"{prefix}://owner/architecture",
            "roadmap_boundary_ref": f"{prefix}://roadmap/phase-7-closeout-r7-61",
        },
        "candidate_scope": {
            "capability_statement_ref": f"{prefix}://capability/{requested_change_type}",
            "included_surface_refs": [
                f"{prefix}://surface/api-or-cli",
                f"{prefix}://surface/docs",
                f"{prefix}://surface/validation",
            ],
            "excluded_scope_ref": f"{prefix}://scope/exclusions/{requested_change_type}",
            "dependency_refs": [
                f"{prefix}://dependency/roadmap-intake-gate",
                f"{prefix}://dependency/release-boundary",
            ],
            "customer_value_ref": f"{prefix}://value/{requested_change_type}",
        },
        "acceptance_criteria": [
            {
                "criterion_id": criterion_id,
                "status": "defined",
                "evidence_ref": f"{prefix}://acceptance/{criterion_id}",
                "owner_ref": f"{prefix}://owner/{criterion_id}",
            }
            for criterion_id in sorted(REQUIRED_ACCEPTANCE_CRITERIA)
        ],
        "release_controls": {
            "implementation_plan_ref": f"{prefix}://plan/implementation/{requested_change_type}",
            "test_plan_ref": f"{prefix}://test/plan/{requested_change_type}",
            "docs_plan_ref": f"{prefix}://docs/plan/{requested_change_type}",
            "rollback_plan_ref": f"{prefix}://plan/rollback/{requested_change_type}",
            "release_owner_ref": f"{prefix}://owner/release/{requested_change_type}",
            "review_cadence_ref": f"{prefix}://workflow/review-cadence/{requested_change_type}",
        },
        "charter_decision": {
            "charter_decision": charter_decision,
            "decision_ref": f"{prefix}://decision/{charter_decision}",
            "next_action_ref": f"{prefix}://next-action/{charter_decision}",
            "target_phase_ref": f"{prefix}://roadmap/future-product-phase",
        },
        "redaction_controls": {control: True for control in sorted(REQUIRED_REDACTION_CONTROLS)},
    }


def validate_roadmap_candidate_charter(
    charter: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if charter.get("schema_version") == ROADMAP_CANDIDATE_CHARTER_SCHEMA else "blocker",
        "Roadmap candidate charter schema is valid."
        if charter.get("schema_version") == ROADMAP_CANDIDATE_CHARTER_SCHEMA
        else f"Charter must use {ROADMAP_CANDIDATE_CHARTER_SCHEMA}.",
    )
    _check_evidence_mode(charter, checks, require_live=require_live)
    _check_source_intake(charter.get("source_intake_result", {}), checks, require_live=require_live)
    _check_ref_object(charter.get("charter_profile", {}), checks, "charter_profile", REQUIRED_PROFILE_FIELDS)
    _check_scope(charter.get("candidate_scope", {}), checks)
    _check_acceptance_criteria(charter.get("acceptance_criteria", []), checks)
    _check_ref_object(charter.get("release_controls", {}), checks, "release_controls", REQUIRED_RELEASE_FIELDS)
    _check_charter_decision(charter.get("charter_decision", {}), checks)
    _check_redaction_controls(charter.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_roadmap_candidate_charter_fields(charter))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Roadmap candidate charter contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and charter.get("evidence_mode") == "live"
    return {
        "schema_version": ROADMAP_CANDIDATE_CHARTER_RESULT_SCHEMA,
        "product": charter.get("product", "CAVRA"),
        "evidence_mode": charter.get("evidence_mode", "unknown"),
        "ready_for_roadmap_candidate_charter": ready,
        "decision": charter.get("charter_decision", {}).get("charter_decision", "unknown"),
        "acceptance_criteria_count": (
            len(charter.get("acceptance_criteria", []))
            if isinstance(charter.get("acceptance_criteria"), list)
            else 0
        ),
        "required_acceptance_criteria_count": len(REQUIRED_ACCEPTANCE_CRITERIA),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "checks": checks,
    }


def write_roadmap_candidate_charter_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_roadmap_candidate_charter(evidence_mode="sample")
    live = build_roadmap_candidate_charter(evidence_mode="live")
    rejected = build_roadmap_candidate_charter(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )
    sample_result = validate_roadmap_candidate_charter(sample)
    live_result = validate_roadmap_candidate_charter(live, require_live=True)
    rejected_result = validate_roadmap_candidate_charter(rejected, require_live=True)
    written = {
        "sample": output_dir / "roadmap-candidate-charter.sample.json",
        "live_candidate": output_dir / "roadmap-candidate-charter.live.sanitized.example.json",
        "rejected_operating": output_dir / "roadmap-candidate-charter.rejected-operating.live.sanitized.example.json",
        "sample_result": output_dir / "roadmap-candidate-charter.sample.result.json",
        "live_candidate_result": output_dir / "roadmap-candidate-charter.live.sanitized.result.json",
        "rejected_operating_result": output_dir / "roadmap-candidate-charter.rejected-operating.live.sanitized.result.json",
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
        "schema_version": "cavra.roadmap-candidate-charter.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_roadmap_candidate_charter": live_result["ready_for_roadmap_candidate_charter"],
    }


def find_forbidden_roadmap_candidate_charter_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_roadmap_candidate_charter_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_roadmap_candidate_charter_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(charter: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = charter.get("evidence_mode")
    sanitized = charter.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized roadmap candidate charter supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample roadmap candidate charter validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Roadmap candidate charter requires evidence_mode=live and sanitized=true.",
        )


def _check_source_intake(intake: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(intake, dict):
        _add_check(checks, "source_intake_result", "blocker", "source_intake_result must be an object.")
        return
    if intake.get("blocker_count") != 0:
        _add_check(checks, "source_intake_result", "blocker", "Source roadmap intake has blockers.")
        return
    if require_live and intake.get("ready_for_roadmap_intake_decision") is not True:
        _add_check(checks, "source_intake_result", "blocker", "Source roadmap intake must be live and ready.")
        return
    if intake.get("decision") != "new_product_roadmap_candidate":
        _add_check(
            checks,
            "source_intake_result",
            "blocker",
            "Only new_product_roadmap_candidate intake decisions can receive a product charter.",
        )
        return
    _add_check(checks, "source_intake_result", "pass", "Source roadmap intake is a product candidate.")


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


def _check_scope(scope: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(scope, dict):
        _add_check(checks, "candidate_scope", "blocker", "candidate_scope must be an object.")
        return
    missing = sorted(REQUIRED_SCOPE_FIELDS - set(scope))
    ref_fields = REQUIRED_SCOPE_FIELDS - {"included_surface_refs", "dependency_refs"}
    invalid = sorted(key for key in ref_fields if key in scope and not _is_ref(scope[key]))
    list_failures = []
    for key in ("included_surface_refs", "dependency_refs"):
        values = scope.get(key)
        if not isinstance(values, list) or not values or any(not _is_ref(value) for value in values):
            list_failures.append(f"{key} must be a non-empty list of sanitized refs")
    if missing or invalid or list_failures:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        details.extend(list_failures)
        _add_check(checks, "candidate_scope", "blocker", "; ".join(details))
    else:
        _add_check(checks, "candidate_scope", "pass", "Candidate scope is complete.")


def _check_acceptance_criteria(criteria: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(criteria, list):
        _add_check(checks, "acceptance_criteria", "blocker", "acceptance_criteria must be a list.")
        return
    by_id = {criterion.get("criterion_id"): criterion for criterion in criteria if isinstance(criterion, dict)}
    missing = sorted(REQUIRED_ACCEPTANCE_CRITERIA - set(by_id))
    extra = sorted(set(by_id) - REQUIRED_ACCEPTANCE_CRITERIA)
    failures: list[str] = []
    for criterion_id in REQUIRED_ACCEPTANCE_CRITERIA:
        criterion = by_id.get(criterion_id)
        if not isinstance(criterion, dict):
            continue
        missing_fields = sorted(REQUIRED_ACCEPTANCE_FIELDS - set(criterion))
        if missing_fields:
            failures.append(f"{criterion_id} missing fields: {', '.join(missing_fields)}")
        if criterion.get("status") != "defined":
            failures.append(f"{criterion_id}.status must be defined")
        for field in ("evidence_ref", "owner_ref"):
            if field in criterion and not _is_ref(criterion[field]):
                failures.append(f"{criterion_id}.{field} must be a sanitized ref")
    if missing or extra or failures:
        details = []
        if missing:
            details.append(f"missing criteria: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected criteria: {', '.join(extra)}")
        details.extend(failures)
        _add_check(checks, "acceptance_criteria", "blocker", "; ".join(details))
    else:
        _add_check(checks, "acceptance_criteria", "pass", "Acceptance criteria are complete.")


def _check_charter_decision(decision: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(decision, dict):
        _add_check(checks, "charter_decision", "blocker", "charter_decision must be an object.")
        return
    missing = sorted(REQUIRED_DECISION_FIELDS - set(decision))
    ref_fields = REQUIRED_DECISION_FIELDS - {"charter_decision"}
    invalid = sorted(key for key in ref_fields if key in decision and not _is_ref(decision[key]))
    charter_decision = decision.get("charter_decision")
    failures: list[str] = []
    if charter_decision not in ALLOWED_CHARTER_DECISIONS:
        failures.append(f"charter_decision must be one of: {', '.join(sorted(ALLOWED_CHARTER_DECISIONS))}")
    if charter_decision != "ready_for_product_roadmap_planning":
        failures.append("product charters must be ready_for_product_roadmap_planning")
    if missing or invalid or failures:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        details.extend(failures)
        _add_check(checks, "charter_decision", "blocker", "; ".join(details))
    else:
        _add_check(checks, "charter_decision", "pass", "Charter decision is ready for product planning.")


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
