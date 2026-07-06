from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_executive_followup_closeout import (
    build_customer_lifecycle_phase8_executive_followup_closeout_packet,
    validate_customer_lifecycle_phase8_executive_followup_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_NEXT_CYCLE_READINESS_INDEX_SCHEMA = (
    "cavra.customer-lifecycle-phase8-next-cycle-readiness-index.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_NEXT_CYCLE_READINESS_INDEX_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-next-cycle-readiness-index.result.v1"
)

REQUIRED_NEXT_CYCLE_OWNER_REFS = {
    "executive_owner_ref",
    "program_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
}

REQUIRED_INDEX_CONTRACT_FIELDS = {
    "readiness_index_ref",
    "backlog_ref",
    "owner_readiness_ref",
    "cadence_ref",
    "evidence_archive_ref",
    "release_decision_gate_ref",
    "redaction_status",
}

REQUIRED_READINESS_REFS = {
    "backlog_readiness_ref",
    "owner_readiness_ref",
    "cadence_readiness_ref",
    "evidence_archive_readiness_ref",
    "release_gate_readiness_ref",
}

REQUIRED_DECISION_GATE_REFS = {
    "next_cycle_go_ref",
    "risk_acceptance_ref",
    "evidence_archive_gate_ref",
    "readiness_review_gate_ref",
}

REQUIRED_CI_GATES = {
    "source_closeout_validation",
    "readiness_index_validation",
    "readiness_ref_validation",
    "decision_gate_validation",
    "redaction_validation",
}

REQUIRED_INDEX_CONTROLS = {
    "executive_followup_closeout_ready",
    "readiness_index_defined",
    "backlog_refs_defined",
    "owner_readiness_refs_defined",
    "cadence_refs_defined",
    "evidence_archive_refs_defined",
    "release_decision_gates_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_INDEX_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_health_score",
    "customer_name",
    "customer_status",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_acceptance",
    "raw_contract",
    "raw_evidence",
    "raw_index",
    "raw_readiness",
    "raw_score",
    "renewal_amount",
    "score_detail",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
    executive_followup_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    closeout = (
        executive_followup_closeout_packet
        or build_customer_lifecycle_phase8_executive_followup_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    closeout_result = validate_customer_lifecycle_phase8_executive_followup_closeout_packet(
        closeout,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_NEXT_CYCLE_READINESS_INDEX_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "next_cycle_readiness_index_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-next-cycle-readiness-index",
        "executive_followup_closeout_ref": f"{prefix}://customer-lifecycle-phase8-executive-followup-closeout/r7",
        "executive_followup_closeout_result": closeout_result,
        "next_cycle_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "next_cycle_readiness_index_contract": {
            "readiness_index_ref": f"{prefix}://phase8/next-cycle-readiness-index/index",
            "backlog_ref": f"{prefix}://phase8/next-cycle-readiness-index/backlog",
            "owner_readiness_ref": f"{prefix}://phase8/next-cycle-readiness-index/owner-readiness",
            "cadence_ref": f"{prefix}://phase8/next-cycle-readiness-index/cadence",
            "evidence_archive_ref": f"{prefix}://phase8/next-cycle-readiness-index/evidence-archive",
            "release_decision_gate_ref": f"{prefix}://phase8/next-cycle-readiness-index/release-decision-gate",
            "redaction_status": "sanitized",
        },
        "next_cycle_readiness_refs": {
            "backlog_readiness_ref": f"{prefix}://phase8/next-cycle-readiness-index/readiness/backlog",
            "owner_readiness_ref": f"{prefix}://phase8/next-cycle-readiness-index/readiness/owners",
            "cadence_readiness_ref": f"{prefix}://phase8/next-cycle-readiness-index/readiness/cadence",
            "evidence_archive_readiness_ref": f"{prefix}://phase8/next-cycle-readiness-index/readiness/evidence-archive",
            "release_gate_readiness_ref": f"{prefix}://phase8/next-cycle-readiness-index/readiness/release-gate",
        },
        "release_decision_gate_refs": {
            "next_cycle_go_ref": f"{prefix}://phase8/next-cycle-readiness-index/gate/next-cycle-go",
            "risk_acceptance_ref": f"{prefix}://phase8/next-cycle-readiness-index/gate/risk-acceptance",
            "evidence_archive_gate_ref": f"{prefix}://phase8/next-cycle-readiness-index/gate/evidence-archive",
            "readiness_review_gate_ref": f"{prefix}://phase8/next-cycle-readiness-index/gate/readiness-review",
        },
        "ci_gate_coverage": {
            "source_closeout_validation": f"{prefix}://ci/phase8/next-cycle-readiness-index/source-closeout-validation",
            "readiness_index_validation": f"{prefix}://ci/phase8/next-cycle-readiness-index/readiness-index-validation",
            "readiness_ref_validation": f"{prefix}://ci/phase8/next-cycle-readiness-index/readiness-ref-validation",
            "decision_gate_validation": f"{prefix}://ci/phase8/next-cycle-readiness-index/decision-gate-validation",
            "redaction_validation": f"{prefix}://ci/phase8/next-cycle-readiness-index/redaction-validation",
        },
        "readiness_evidence_refs": [
            f"{prefix}://phase8/next-cycle-readiness-index/source-closeout",
            f"{prefix}://phase8/next-cycle-readiness-index/readiness-index",
            f"{prefix}://phase8/next-cycle-readiness-index/decision-gates",
            f"{prefix}://phase8/next-cycle-readiness-index/evidence-archive",
        ],
        "readiness_controls": {
            "executive_followup_closeout_ready": closeout_result["blocker_count"] == 0,
            "readiness_index_defined": True,
            "backlog_refs_defined": True,
            "owner_readiness_refs_defined": True,
            "cadence_refs_defined": True,
            "evidence_archive_refs_defined": True,
            "release_decision_gates_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass"
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_NEXT_CYCLE_READINESS_INDEX_SCHEMA
        else "blocker",
        "Customer lifecycle Phase 8 next-cycle readiness index schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_NEXT_CYCLE_READINESS_INDEX_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_NEXT_CYCLE_READINESS_INDEX_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("executive_followup_closeout_ref"), checks, "executive_followup_closeout_ref")
    _check_closeout_result(packet.get("executive_followup_closeout_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("next_cycle_owner_refs", {}), REQUIRED_NEXT_CYCLE_OWNER_REFS, checks, "next_cycle_owner_refs")
    _check_index_contract(packet.get("next_cycle_readiness_index_contract", {}), checks)
    _check_required_refs(
        packet.get("next_cycle_readiness_refs", {}),
        REQUIRED_READINESS_REFS,
        checks,
        "next_cycle_readiness_refs",
    )
    _check_required_refs(
        packet.get("release_decision_gate_refs", {}),
        REQUIRED_DECISION_GATE_REFS,
        checks,
        "release_decision_gate_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("readiness_evidence_refs", []), checks, "readiness_evidence_refs", min_count=4)
    _check_controls(packet.get("readiness_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_index_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 next-cycle readiness index contains sanitized refs and customer-safe readiness text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_NEXT_CYCLE_READINESS_INDEX_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_next_cycle_readiness_index": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_next_cycle_readiness_index_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(sample)
    live_result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-next-cycle-readiness-index.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-next-cycle-readiness-index.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-next-cycle-readiness-index.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-next-cycle-readiness-index.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-next-cycle-readiness-index.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_next_cycle_readiness_index": live_result[
            "ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 next-cycle readiness index supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 next-cycle readiness index validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Next-cycle readiness index requires evidence_mode=live and sanitized=true.",
        )


def _check_closeout_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "executive_followup_closeout_result",
            "blocker",
            "executive_followup_closeout_result must be an object.",
        )
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_executive_followup_closeout") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "executive_followup_closeout_result", "pass", "Source executive follow-up closeout is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "executive_followup_closeout_result",
            "warn",
            "Source executive follow-up closeout validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "executive_followup_closeout_result",
            "blocker",
            "Source executive follow-up closeout is not ready.",
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


def _check_index_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(
            checks,
            "next_cycle_readiness_index_contract",
            "blocker",
            "next_cycle_readiness_index_contract must be an object.",
        )
        return
    missing = sorted(field for field in REQUIRED_INDEX_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_INDEX_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "next_cycle_readiness_index_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Next-cycle readiness index contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Next-cycle readiness index contract invalid: "
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
        _add_check(checks, "readiness_controls", "blocker", "readiness_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_INDEX_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "readiness_controls",
        "pass" if not missing else "blocker",
        "Next-cycle readiness index controls are explicit."
        if not missing
        else f"Next-cycle readiness index controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_index_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_INDEX_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_index_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_index_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
