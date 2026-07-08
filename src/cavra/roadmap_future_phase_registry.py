from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.roadmap_future_phase_opening_gate import (
    build_roadmap_future_phase_opening_gate,
    validate_roadmap_future_phase_opening_gate,
)


ROADMAP_FUTURE_PHASE_REGISTRY_SCHEMA = "cavra.roadmap-future-phase-registry.v1"
ROADMAP_FUTURE_PHASE_REGISTRY_RESULT_SCHEMA = "cavra.roadmap-future-phase-registry.result.v1"

REQUIRED_REGISTRY_PROFILE_FIELDS = {
    "registry_owner_ref",
    "registry_ref",
    "review_cadence_ref",
    "roadmap_boundary_ref",
}

REQUIRED_PHASE_ENTRY_FIELDS = {
    "architecture_owner_ref",
    "exit_criteria_ref",
    "initial_backlog_ref",
    "phase_id_ref",
    "phase_owner_ref",
    "phase_status",
    "phase_title_ref",
    "product_owner_ref",
    "public_contract_boundary_ref",
    "release_gate_ref",
    "source_opening_gate_ref",
    "status_report_ref",
}

REQUIRED_DECISION_FIELDS = {
    "decision_ref",
    "next_action_ref",
    "registry_decision",
    "target_registry_ref",
}

ALLOWED_PHASE_STATUSES = {
    "registered_pending_execution",
    "rejected_to_opening_gate",
}

ALLOWED_REGISTRY_DECISIONS = {
    "ready_to_register_future_phase",
    "rejected_to_opening_gate",
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
    "registry://",
    "roadmap://",
    "sample://",
    "security://",
    "test://",
    "workflow://",
)


def build_roadmap_future_phase_registry(
    *,
    evidence_mode: str = "sample",
    requested_change_type: str = "new_product_capability",
) -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    opening_gate = build_roadmap_future_phase_opening_gate(
        evidence_mode=evidence_mode,
        requested_change_type=requested_change_type,
    )
    opening_result = validate_roadmap_future_phase_opening_gate(
        opening_gate,
        require_live=evidence_mode == "live",
    )
    source_ready = (
        opening_result.get("blocker_count") == 0
        and opening_result.get("decision") == "ready_to_open_future_product_phase"
    )
    phase_status = "registered_pending_execution" if source_ready else "rejected_to_opening_gate"
    registry_decision = (
        "ready_to_register_future_phase" if source_ready else "rejected_to_opening_gate"
    )
    return {
        "schema_version": ROADMAP_FUTURE_PHASE_REGISTRY_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "source_opening_gate_result": opening_result,
        "registry_profile": {
            "registry_ref": f"{prefix}://registry/future-phase",
            "registry_owner_ref": f"{prefix}://owner/product-operations",
            "review_cadence_ref": f"{prefix}://workflow/future-phase-registry-review",
            "roadmap_boundary_ref": f"{prefix}://roadmap/phase-7-closeout-r7-61",
        },
        "future_phase_entries": [
            {
                "phase_id_ref": f"{prefix}://phase/{requested_change_type}",
                "source_opening_gate_ref": f"{prefix}://phase-opening-gate/{requested_change_type}",
                "phase_title_ref": f"{prefix}://phase/title/{requested_change_type}",
                "phase_owner_ref": f"{prefix}://owner/future-phase",
                "product_owner_ref": f"{prefix}://owner/product",
                "architecture_owner_ref": f"{prefix}://owner/architecture",
                "phase_status": phase_status,
                "initial_backlog_ref": f"{prefix}://github/backlog/{requested_change_type}",
                "release_gate_ref": f"{prefix}://workflow/release-gate/{requested_change_type}",
                "status_report_ref": f"{prefix}://docs/status/{requested_change_type}",
                "public_contract_boundary_ref": f"{prefix}://product/public-contract/{requested_change_type}",
                "exit_criteria_ref": f"{prefix}://phase/exit-criteria/{requested_change_type}",
            }
        ],
        "registry_decision": {
            "registry_decision": registry_decision,
            "decision_ref": f"{prefix}://decision/{registry_decision}",
            "next_action_ref": f"{prefix}://next-action/{registry_decision}",
            "target_registry_ref": f"{prefix}://registry/future-phase",
        },
        "redaction_controls": {control: True for control in sorted(REQUIRED_REDACTION_CONTROLS)},
    }


def validate_roadmap_future_phase_registry(
    registry: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if registry.get("schema_version") == ROADMAP_FUTURE_PHASE_REGISTRY_SCHEMA else "blocker",
        "Roadmap future phase registry schema is valid."
        if registry.get("schema_version") == ROADMAP_FUTURE_PHASE_REGISTRY_SCHEMA
        else f"Registry must use {ROADMAP_FUTURE_PHASE_REGISTRY_SCHEMA}.",
    )
    _check_evidence_mode(registry, checks, require_live=require_live)
    _check_source_opening_gate(
        registry.get("source_opening_gate_result", {}),
        checks,
        require_live=require_live,
    )
    _check_ref_object(
        registry.get("registry_profile", {}),
        checks,
        "registry_profile",
        REQUIRED_REGISTRY_PROFILE_FIELDS,
    )
    _check_phase_entries(registry.get("future_phase_entries", []), checks)
    _check_registry_decision(registry.get("registry_decision", {}), checks)
    _check_redaction_controls(registry.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_roadmap_future_phase_registry_fields(registry))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Roadmap future phase registry contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and registry.get("evidence_mode") == "live"
    entries = registry.get("future_phase_entries", [])
    return {
        "schema_version": ROADMAP_FUTURE_PHASE_REGISTRY_RESULT_SCHEMA,
        "product": registry.get("product", "CAVRA"),
        "evidence_mode": registry.get("evidence_mode", "unknown"),
        "ready_for_roadmap_future_phase_registry": ready,
        "decision": registry.get("registry_decision", {}).get("registry_decision", "unknown"),
        "future_phase_entry_count": len(entries) if isinstance(entries, list) else 0,
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "checks": checks,
    }


def write_roadmap_future_phase_registry_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_roadmap_future_phase_registry(evidence_mode="sample")
    live = build_roadmap_future_phase_registry(evidence_mode="live")
    rejected = build_roadmap_future_phase_registry(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )
    sample_result = validate_roadmap_future_phase_registry(sample)
    live_result = validate_roadmap_future_phase_registry(live, require_live=True)
    rejected_result = validate_roadmap_future_phase_registry(rejected, require_live=True)
    written = {
        "sample": output_dir / "roadmap-future-phase-registry.sample.json",
        "live_candidate": output_dir / "roadmap-future-phase-registry.live.sanitized.example.json",
        "rejected_operating": output_dir
        / "roadmap-future-phase-registry.rejected-operating.live.sanitized.example.json",
        "sample_result": output_dir / "roadmap-future-phase-registry.sample.result.json",
        "live_candidate_result": output_dir / "roadmap-future-phase-registry.live.sanitized.result.json",
        "rejected_operating_result": output_dir
        / "roadmap-future-phase-registry.rejected-operating.live.sanitized.result.json",
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
        "schema_version": "cavra.roadmap-future-phase-registry.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_roadmap_future_phase_registry": live_result["ready_for_roadmap_future_phase_registry"],
    }


def find_forbidden_roadmap_future_phase_registry_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_roadmap_future_phase_registry_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_roadmap_future_phase_registry_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(registry: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = registry.get("evidence_mode")
    sanitized = registry.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized future phase registry supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample future phase registry validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Future phase registry requires evidence_mode=live and sanitized=true.",
        )


def _check_source_opening_gate(opening_gate: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(opening_gate, dict):
        _add_check(checks, "source_opening_gate_result", "blocker", "source_opening_gate_result must be an object.")
        return
    if opening_gate.get("blocker_count") != 0:
        _add_check(checks, "source_opening_gate_result", "blocker", "Source future phase opening gate has blockers.")
        return
    if require_live and opening_gate.get("ready_for_roadmap_future_phase_opening") is not True:
        _add_check(
            checks,
            "source_opening_gate_result",
            "blocker",
            "Source future phase opening gate must be live and ready.",
        )
        return
    if opening_gate.get("decision") != "ready_to_open_future_product_phase":
        _add_check(
            checks,
            "source_opening_gate_result",
            "blocker",
            "Future phase registry requires ready_to_open_future_product_phase.",
        )
        return
    if not require_live and opening_gate.get("ready_for_roadmap_future_phase_opening") is not True:
        _add_check(
            checks,
            "source_opening_gate_result",
            "warn",
            "Sample source opening gate validates shape only.",
        )
        return
    _add_check(checks, "source_opening_gate_result", "pass", "Source future phase opening gate is ready.")


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


def _check_phase_entries(entries: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(entries, list) or not entries:
        _add_check(checks, "future_phase_entries", "blocker", "future_phase_entries must be a non-empty list.")
        return
    failures: list[str] = []
    phase_ids: list[str] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            failures.append(f"entry {index} must be an object")
            continue
        missing = sorted(REQUIRED_PHASE_ENTRY_FIELDS - set(entry))
        if missing:
            failures.append(f"entry {index} missing: {', '.join(missing)}")
        phase_status = entry.get("phase_status")
        if phase_status not in ALLOWED_PHASE_STATUSES:
            failures.append(f"entry {index}.phase_status must be one of: {', '.join(sorted(ALLOWED_PHASE_STATUSES))}")
        if phase_status != "registered_pending_execution":
            failures.append(f"entry {index}.phase_status must be registered_pending_execution")
        phase_id = entry.get("phase_id_ref")
        if isinstance(phase_id, str):
            phase_ids.append(phase_id)
        for field in REQUIRED_PHASE_ENTRY_FIELDS - {"phase_status"}:
            if field in entry and not _is_ref(entry[field]):
                failures.append(f"entry {index}.{field} must be a sanitized ref")
    duplicates = sorted({phase_id for phase_id in phase_ids if phase_ids.count(phase_id) > 1})
    if duplicates:
        failures.append(f"duplicate phase_id_ref values: {', '.join(duplicates)}")
    if failures:
        _add_check(checks, "future_phase_entries", "blocker", "; ".join(failures))
    else:
        _add_check(checks, "future_phase_entries", "pass", "Future phase registry entries are complete.")


def _check_registry_decision(decision: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(decision, dict):
        _add_check(checks, "registry_decision", "blocker", "registry_decision must be an object.")
        return
    missing = sorted(REQUIRED_DECISION_FIELDS - set(decision))
    ref_fields = REQUIRED_DECISION_FIELDS - {"registry_decision"}
    invalid = sorted(key for key in ref_fields if key in decision and not _is_ref(decision[key]))
    registry_decision = decision.get("registry_decision")
    failures: list[str] = []
    if registry_decision not in ALLOWED_REGISTRY_DECISIONS:
        failures.append(f"registry_decision must be one of: {', '.join(sorted(ALLOWED_REGISTRY_DECISIONS))}")
    if registry_decision != "ready_to_register_future_phase":
        failures.append("future phase registries must be ready_to_register_future_phase")
    if missing or invalid or failures:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid:
            details.append(f"invalid refs: {', '.join(invalid)}")
        details.extend(failures)
        _add_check(checks, "registry_decision", "blocker", "; ".join(details))
    else:
        _add_check(checks, "registry_decision", "pass", "Future phase registry decision is ready.")


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
