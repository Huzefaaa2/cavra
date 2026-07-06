from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_action_followup_checkpoint import (
    build_customer_lifecycle_phase8_action_followup_checkpoint_packet,
    validate_customer_lifecycle_phase8_action_followup_checkpoint_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_FOLLOWUP_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-executive-followup-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_FOLLOWUP_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-executive-followup-closeout.result.v1"
)

REQUIRED_CLOSEOUT_OWNER_REFS = {
    "executive_owner_ref",
    "program_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
}

REQUIRED_CLOSEOUT_CONTRACT_FIELDS = {
    "closeout_plan_ref",
    "acceptance_evidence_ref",
    "escalation_outcome_ref",
    "residual_risk_ref",
    "next_cycle_handoff_ref",
    "decision_record_ref",
    "redaction_status",
}

REQUIRED_RESOLUTION_REFS = {
    "risk_posture_resolution_ref",
    "support_resolution_ref",
    "adoption_resolution_ref",
    "executive_escalation_resolution_ref",
}

REQUIRED_HANDOFF_REFS = {
    "next_cycle_backlog_ref",
    "owner_transition_ref",
    "cadence_reset_ref",
    "evidence_archive_ref",
}

REQUIRED_CI_GATES = {
    "source_checkpoint_validation",
    "closeout_contract_validation",
    "resolution_ref_validation",
    "handoff_ref_validation",
    "redaction_validation",
}

REQUIRED_CLOSEOUT_CONTROLS = {
    "action_followup_checkpoint_ready",
    "closeout_refs_defined",
    "resolution_refs_defined",
    "acceptance_evidence_defined",
    "escalation_outcomes_defined",
    "next_cycle_handoff_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_CLOSEOUT_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_name",
    "customer_status",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_acceptance",
    "raw_blocker",
    "raw_contract",
    "raw_evidence",
    "raw_resolution",
    "raw_status",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_executive_followup_closeout_packet(
    action_followup_checkpoint_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    checkpoint = (
        action_followup_checkpoint_packet
        or build_customer_lifecycle_phase8_action_followup_checkpoint_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    checkpoint_result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(
        checkpoint,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_FOLLOWUP_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "executive_followup_closeout_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-executive-followup-closeout",
        "action_followup_checkpoint_ref": f"{prefix}://customer-lifecycle-phase8-action-followup-checkpoint/r7",
        "action_followup_checkpoint_result": checkpoint_result,
        "closeout_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "executive_followup_closeout_contract": {
            "closeout_plan_ref": f"{prefix}://phase8/executive-followup-closeout/plan",
            "acceptance_evidence_ref": f"{prefix}://phase8/executive-followup-closeout/acceptance-evidence",
            "escalation_outcome_ref": f"{prefix}://phase8/executive-followup-closeout/escalation-outcomes",
            "residual_risk_ref": f"{prefix}://phase8/executive-followup-closeout/residual-risk",
            "next_cycle_handoff_ref": f"{prefix}://phase8/executive-followup-closeout/next-cycle-handoff",
            "decision_record_ref": f"{prefix}://phase8/executive-followup-closeout/decision-record",
            "redaction_status": "sanitized",
        },
        "closeout_resolution_refs": {
            "risk_posture_resolution_ref": f"{prefix}://phase8/executive-followup-closeout/resolution/risk-posture",
            "support_resolution_ref": f"{prefix}://phase8/executive-followup-closeout/resolution/support",
            "adoption_resolution_ref": f"{prefix}://phase8/executive-followup-closeout/resolution/adoption",
            "executive_escalation_resolution_ref": (
                f"{prefix}://phase8/executive-followup-closeout/resolution/executive-escalation"
            ),
        },
        "next_cycle_handoff_refs": {
            "next_cycle_backlog_ref": f"{prefix}://phase8/executive-followup-closeout/handoff/backlog",
            "owner_transition_ref": f"{prefix}://phase8/executive-followup-closeout/handoff/owner-transition",
            "cadence_reset_ref": f"{prefix}://phase8/executive-followup-closeout/handoff/cadence-reset",
            "evidence_archive_ref": f"{prefix}://phase8/executive-followup-closeout/handoff/evidence-archive",
        },
        "ci_gate_coverage": {
            "source_checkpoint_validation": (
                f"{prefix}://ci/phase8/executive-followup-closeout/source-checkpoint-validation"
            ),
            "closeout_contract_validation": (
                f"{prefix}://ci/phase8/executive-followup-closeout/closeout-contract-validation"
            ),
            "resolution_ref_validation": (
                f"{prefix}://ci/phase8/executive-followup-closeout/resolution-ref-validation"
            ),
            "handoff_ref_validation": f"{prefix}://ci/phase8/executive-followup-closeout/handoff-ref-validation",
            "redaction_validation": f"{prefix}://ci/phase8/executive-followup-closeout/redaction-validation",
        },
        "closeout_evidence_refs": [
            f"{prefix}://phase8/executive-followup-closeout/source-checkpoint",
            f"{prefix}://phase8/executive-followup-closeout/acceptance-evidence",
            f"{prefix}://phase8/executive-followup-closeout/escalation-outcomes",
            f"{prefix}://phase8/executive-followup-closeout/next-cycle-handoff",
        ],
        "closeout_controls": {
            "action_followup_checkpoint_ready": checkpoint_result["blocker_count"] == 0,
            "closeout_refs_defined": True,
            "resolution_refs_defined": True,
            "acceptance_evidence_defined": True,
            "escalation_outcomes_defined": True,
            "next_cycle_handoff_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_executive_followup_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass"
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_FOLLOWUP_CLOSEOUT_SCHEMA
        else "blocker",
        "Customer lifecycle Phase 8 executive follow-up closeout schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_FOLLOWUP_CLOSEOUT_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_FOLLOWUP_CLOSEOUT_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("action_followup_checkpoint_ref"), checks, "action_followup_checkpoint_ref")
    _check_checkpoint_result(packet.get("action_followup_checkpoint_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("closeout_owner_refs", {}), REQUIRED_CLOSEOUT_OWNER_REFS, checks, "closeout_owner_refs")
    _check_closeout_contract(packet.get("executive_followup_closeout_contract", {}), checks)
    _check_required_refs(
        packet.get("closeout_resolution_refs", {}),
        REQUIRED_RESOLUTION_REFS,
        checks,
        "closeout_resolution_refs",
    )
    _check_required_refs(
        packet.get("next_cycle_handoff_refs", {}),
        REQUIRED_HANDOFF_REFS,
        checks,
        "next_cycle_handoff_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("closeout_evidence_refs", []), checks, "closeout_evidence_refs", min_count=4)
    _check_controls(packet.get("closeout_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_closeout_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 executive follow-up closeout contains sanitized refs and customer-safe closeout text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_FOLLOWUP_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_executive_followup_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_executive_followup_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_executive_followup_closeout_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_executive_followup_closeout_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_executive_followup_closeout_packet(sample)
    live_result = validate_customer_lifecycle_phase8_executive_followup_closeout_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-executive-followup-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-executive-followup-closeout.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-executive-followup-closeout.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-executive-followup-closeout.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-executive-followup-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_executive_followup_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_executive_followup_closeout"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 executive follow-up closeout supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 executive follow-up closeout validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Executive follow-up closeout requires evidence_mode=live and sanitized=true.",
        )


def _check_checkpoint_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "action_followup_checkpoint_result",
            "blocker",
            "action_followup_checkpoint_result must be an object.",
        )
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_action_followup_checkpoint") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "action_followup_checkpoint_result", "pass", "Source action follow-up checkpoint is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "action_followup_checkpoint_result",
            "warn",
            "Source action follow-up checkpoint validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "action_followup_checkpoint_result",
            "blocker",
            "Source action follow-up checkpoint is not ready.",
        )


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


def _check_closeout_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(
            checks,
            "executive_followup_closeout_contract",
            "blocker",
            "executive_followup_closeout_contract must be an object.",
        )
        return
    missing = sorted(field for field in REQUIRED_CLOSEOUT_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_CLOSEOUT_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "executive_followup_closeout_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Executive follow-up closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Executive follow-up closeout contract invalid: "
            f"missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}."
        ),
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
        _add_check(checks, "closeout_controls", "blocker", "closeout_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_CLOSEOUT_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "closeout_controls",
        "pass" if not missing else "blocker",
        "Executive follow-up closeout controls are explicit."
        if not missing
        else f"Executive follow-up closeout controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_closeout_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_CLOSEOUT_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_closeout_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_closeout_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
