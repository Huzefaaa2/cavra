from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROADMAP_INTAKE_GATE_SCHEMA = "cavra.roadmap-intake-gate.v1"
ROADMAP_INTAKE_GATE_RESULT_SCHEMA = "cavra.roadmap-intake-gate.result.v1"

PRODUCT_ROADMAP_CHANGE_TYPES = {
    "new_api_or_cli",
    "new_aispm_posture_capability",
    "new_connector",
    "new_deployment_target",
    "new_edition_or_packaging_model",
    "new_evidence_schema",
    "new_product_capability",
    "new_trust_artifact",
    "new_validator_family",
    "new_buyer_facing_surface",
}

OPERATING_EVIDENCE_CHANGE_TYPES = {
    "customer_monitoring_cycle",
    "customer_operating_review",
    "drift_remediation",
    "evidence_room_maintenance",
    "private_customer_closeout",
    "private_live_validation",
    "public_scorecard_refresh",
    "renewal_review",
    "support_case",
}

ALLOWED_DECISIONS = {
    "live_operations_evidence",
    "new_product_roadmap_candidate",
    "needs_architect_review",
}

REQUIRED_PROFILE_FIELDS = {
    "request_id_ref",
    "requester_ref",
    "request_summary_ref",
    "classification_owner_ref",
    "roadmap_boundary_ref",
}

REQUIRED_CLASSIFICATION_FIELDS = {
    "requested_change_type",
    "requested_scope_ref",
    "candidate_new_capability",
    "product_surface_refs",
}

REQUIRED_OPERATING_EVIDENCE_FIELDS = {
    "repeated_customer_cycle",
    "evidence_room_ref",
    "customer_safe_record_ref",
    "private_operations_record_ref",
}

REQUIRED_DECISION_FIELDS = {
    "decision",
    "decision_ref",
    "rationale_ref",
    "owner_ref",
    "next_action_ref",
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
    "audit://",
    "classification://",
    "decision://",
    "docs://",
    "evidence://",
    "github://",
    "intake://",
    "operations://",
    "product://",
    "roadmap://",
    "sample://",
    "ticket://",
    "workflow://",
)


def build_roadmap_intake_gate_packet(
    *,
    evidence_mode: str = "sample",
    requested_change_type: str = "customer_monitoring_cycle",
) -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    is_product_candidate = requested_change_type in PRODUCT_ROADMAP_CHANGE_TYPES
    is_operating_cycle = requested_change_type in OPERATING_EVIDENCE_CHANGE_TYPES
    decision = (
        "new_product_roadmap_candidate"
        if is_product_candidate
        else "live_operations_evidence"
        if is_operating_cycle
        else "needs_architect_review"
    )
    return {
        "schema_version": ROADMAP_INTAKE_GATE_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "intake_profile": {
            "request_id_ref": f"{prefix}://roadmap-intake/request",
            "requester_ref": f"{prefix}://roadmap-intake/requester",
            "request_summary_ref": f"{prefix}://roadmap-intake/summary",
            "classification_owner_ref": f"{prefix}://owner/roadmap-boundary",
            "roadmap_boundary_ref": f"{prefix}://roadmap/phase-7-closeout-r7-61",
        },
        "request_classification": {
            "requested_change_type": requested_change_type,
            "requested_scope_ref": f"{prefix}://roadmap-intake/scope/{requested_change_type}",
            "candidate_new_capability": is_product_candidate,
            "product_surface_refs": [
                f"{prefix}://product-surface/{requested_change_type}"
            ]
            if is_product_candidate
            else [],
        },
        "operating_evidence": {
            "repeated_customer_cycle": is_operating_cycle,
            "evidence_room_ref": f"{prefix}://evidence-room/operating-cycle",
            "customer_safe_record_ref": f"{prefix}://customer-safe/operating-cycle",
            "private_operations_record_ref": f"{prefix}://operations/private-cycle-record",
        },
        "boundary_decision": {
            "decision": decision,
            "decision_ref": f"{prefix}://decision/{decision}",
            "rationale_ref": f"{prefix}://rationale/{requested_change_type}",
            "owner_ref": f"{prefix}://owner/roadmap-intake",
            "next_action_ref": f"{prefix}://next-action/{decision}",
        },
        "redaction_controls": {control: True for control in sorted(REQUIRED_REDACTION_CONTROLS)},
    }


def validate_roadmap_intake_gate_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == ROADMAP_INTAKE_GATE_SCHEMA else "blocker",
        "Roadmap intake gate schema is valid."
        if packet.get("schema_version") == ROADMAP_INTAKE_GATE_SCHEMA
        else f"Packet must use {ROADMAP_INTAKE_GATE_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_ref_object(packet.get("intake_profile", {}), checks, "intake_profile", REQUIRED_PROFILE_FIELDS)
    _check_request_classification(packet.get("request_classification", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    _check_boundary_decision(
        packet.get("request_classification", {}),
        packet.get("operating_evidence", {}),
        packet.get("boundary_decision", {}),
        checks,
    )
    _check_redaction_controls(packet.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_roadmap_intake_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Roadmap intake gate contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and packet.get("evidence_mode") == "live"
    decision = packet.get("boundary_decision", {}).get("decision")
    return {
        "schema_version": ROADMAP_INTAKE_GATE_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_roadmap_intake_decision": ready,
        "decision": decision if decision in ALLOWED_DECISIONS else "invalid",
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "checks": checks,
    }


def write_roadmap_intake_gate_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_operating = build_roadmap_intake_gate_packet(
        evidence_mode="sample",
        requested_change_type="customer_monitoring_cycle",
    )
    live_operating = build_roadmap_intake_gate_packet(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )
    live_candidate = build_roadmap_intake_gate_packet(
        evidence_mode="live",
        requested_change_type="new_product_capability",
    )
    sample_result = validate_roadmap_intake_gate_packet(sample_operating)
    live_operating_result = validate_roadmap_intake_gate_packet(live_operating, require_live=True)
    live_candidate_result = validate_roadmap_intake_gate_packet(live_candidate, require_live=True)
    written = {
        "sample_operating": output_dir / "roadmap-intake-gate.operating.sample.json",
        "live_operating": output_dir / "roadmap-intake-gate.operating.live.sanitized.example.json",
        "live_candidate": output_dir / "roadmap-intake-gate.product-candidate.live.sanitized.example.json",
        "sample_result": output_dir / "roadmap-intake-gate.operating.sample.result.json",
        "live_operating_result": output_dir / "roadmap-intake-gate.operating.live.sanitized.result.json",
        "live_candidate_result": output_dir / "roadmap-intake-gate.product-candidate.live.sanitized.result.json",
    }
    payloads = {
        "sample_operating": sample_operating,
        "live_operating": live_operating,
        "live_candidate": live_candidate,
        "sample_result": sample_result,
        "live_operating_result": live_operating_result,
        "live_candidate_result": live_candidate_result,
    }
    for name, payload in payloads.items():
        written[name].write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.roadmap-intake-gate.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_roadmap_intake_decision": (
            live_operating_result["ready_for_roadmap_intake_decision"]
            and live_candidate_result["ready_for_roadmap_intake_decision"]
        ),
    }


def find_forbidden_roadmap_intake_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_roadmap_intake_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_roadmap_intake_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized roadmap intake packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample roadmap intake packet validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Roadmap intake gate requires evidence_mode=live and sanitized=true.",
        )


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


def _check_request_classification(classification: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(classification, dict):
        _add_check(checks, "request_classification", "blocker", "request_classification must be an object.")
        return
    missing = sorted(REQUIRED_CLASSIFICATION_FIELDS - set(classification))
    change_type = classification.get("requested_change_type")
    blockers: list[str] = []
    if missing:
        blockers.append(f"missing: {', '.join(missing)}")
    if change_type not in PRODUCT_ROADMAP_CHANGE_TYPES | OPERATING_EVIDENCE_CHANGE_TYPES:
        blockers.append(f"unknown requested_change_type: {change_type}")
    if not _is_ref(classification.get("requested_scope_ref")):
        blockers.append("requested_scope_ref must be a sanitized reference")
    surface_refs = classification.get("product_surface_refs")
    if not isinstance(surface_refs, list) or any(not _is_ref(ref) for ref in surface_refs):
        blockers.append("product_surface_refs must be a list of sanitized references")
    if change_type in PRODUCT_ROADMAP_CHANGE_TYPES:
        if classification.get("candidate_new_capability") is not True:
            blockers.append("product roadmap candidates require candidate_new_capability=true")
        if not surface_refs:
            blockers.append("product roadmap candidates require at least one product_surface_ref")
    if change_type in OPERATING_EVIDENCE_CHANGE_TYPES and classification.get("candidate_new_capability") is not False:
        blockers.append("operating evidence requests require candidate_new_capability=false")
    if blockers:
        _add_check(checks, "request_classification", "blocker", "; ".join(blockers))
    else:
        _add_check(checks, "request_classification", "pass", "Request classification is consistent.")


def _check_operating_evidence(evidence: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(evidence, dict):
        _add_check(checks, "operating_evidence", "blocker", "operating_evidence must be an object.")
        return
    missing = sorted(REQUIRED_OPERATING_EVIDENCE_FIELDS - set(evidence))
    ref_fields = REQUIRED_OPERATING_EVIDENCE_FIELDS - {"repeated_customer_cycle"}
    invalid = sorted(key for key in ref_fields if key in evidence and not _is_ref(evidence[key]))
    if missing or invalid:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        _add_check(checks, "operating_evidence", "blocker", "; ".join(details))
    else:
        _add_check(checks, "operating_evidence", "pass", "operating_evidence references are complete.")
    if not isinstance(evidence.get("repeated_customer_cycle"), bool):
        _add_check(
            checks,
            "operating_evidence_repeated_cycle",
            "blocker",
            "repeated_customer_cycle must be a boolean.",
        )


def _check_boundary_decision(
    classification: Any,
    evidence: Any,
    decision: Any,
    checks: list[dict[str, str]],
) -> None:
    if not isinstance(decision, dict):
        _add_check(checks, "boundary_decision", "blocker", "boundary_decision must be an object.")
        return
    missing = sorted(REQUIRED_DECISION_FIELDS - set(decision))
    ref_fields = REQUIRED_DECISION_FIELDS - {"decision"}
    invalid = sorted(key for key in ref_fields if key in decision and not _is_ref(decision[key]))
    if missing or invalid:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        _add_check(checks, "boundary_decision", "blocker", "; ".join(details))
    else:
        _add_check(checks, "boundary_decision", "pass", "boundary_decision references are complete.")
    if not isinstance(classification, dict) or not isinstance(evidence, dict):
        return
    change_type = classification.get("requested_change_type")
    boundary_decision = decision.get("decision")
    blockers: list[str] = []
    if boundary_decision not in ALLOWED_DECISIONS:
        blockers.append(f"decision must be one of: {', '.join(sorted(ALLOWED_DECISIONS))}")
    if change_type in PRODUCT_ROADMAP_CHANGE_TYPES and boundary_decision != "new_product_roadmap_candidate":
        blockers.append("new product capability requests must become roadmap candidates")
    if change_type in OPERATING_EVIDENCE_CHANGE_TYPES:
        if boundary_decision != "live_operations_evidence":
            blockers.append("routine operating requests must remain live operations evidence")
        if evidence.get("repeated_customer_cycle") is not True:
            blockers.append("routine operating requests require repeated_customer_cycle=true")
    if blockers:
        _add_check(checks, "roadmap_boundary_decision", "blocker", "; ".join(blockers))
    else:
        _add_check(checks, "roadmap_boundary_decision", "pass", "Boundary decision matches request type.")


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
