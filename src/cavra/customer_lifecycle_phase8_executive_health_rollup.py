from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_customer_health_review import (
    build_customer_lifecycle_phase8_customer_health_review_packet,
    validate_customer_lifecycle_phase8_customer_health_review_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_HEALTH_ROLLUP_SCHEMA = (
    "cavra.customer-lifecycle-phase8-executive-health-rollup.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_HEALTH_ROLLUP_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-executive-health-rollup.result.v1"
)

REQUIRED_EXECUTIVE_OWNER_REFS = {
    "executive_owner_ref",
    "program_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
}

REQUIRED_ROLLUP_FIELDS = {
    "decision_ref",
    "trend_ref",
    "risk_posture_ref",
    "support_status_ref",
    "adoption_status_ref",
    "next_action_readiness_ref",
    "redaction_status",
}

REQUIRED_CI_GATES = {
    "source_health_validation",
    "rollup_contract_validation",
    "executive_brief_validation",
    "redaction_validation",
}

REQUIRED_ROLLUP_CONTROLS = {
    "customer_health_review_ready",
    "decision_refs_defined",
    "trend_refs_defined",
    "risk_posture_defined",
    "support_status_defined",
    "adoption_status_defined",
    "next_action_readiness_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_EXECUTIVE_FIELDS = {
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


def build_customer_lifecycle_phase8_executive_health_rollup_packet(
    health_review_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    health_review = health_review_packet or build_customer_lifecycle_phase8_customer_health_review_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    health_review_result = validate_customer_lifecycle_phase8_customer_health_review_packet(
        health_review,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_HEALTH_ROLLUP_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "executive_health_rollup_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-executive-health-rollup",
        "customer_health_review_ref": f"{prefix}://customer-lifecycle-phase8-customer-health-review/r7",
        "customer_health_review_result": health_review_result,
        "executive_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
        },
        "executive_rollup_contract": {
            "decision_ref": f"{prefix}://phase8/executive-health-rollup/decision",
            "trend_ref": f"{prefix}://phase8/executive-health-rollup/trends",
            "risk_posture_ref": f"{prefix}://phase8/executive-health-rollup/risk-posture",
            "support_status_ref": f"{prefix}://phase8/executive-health-rollup/support-status",
            "adoption_status_ref": f"{prefix}://phase8/executive-health-rollup/adoption-status",
            "next_action_readiness_ref": f"{prefix}://phase8/executive-health-rollup/next-action-readiness",
            "redaction_status": "sanitized",
        },
        "executive_brief_refs": [
            f"{prefix}://phase8/executive-health-rollup/brief/summary",
            f"{prefix}://phase8/executive-health-rollup/brief/risk",
            f"{prefix}://phase8/executive-health-rollup/brief/support",
            f"{prefix}://phase8/executive-health-rollup/brief/adoption",
        ],
        "ci_gate_coverage": {
            "source_health_validation": f"{prefix}://ci/phase8/executive-health-rollup/source-health-validation",
            "rollup_contract_validation": f"{prefix}://ci/phase8/executive-health-rollup/rollup-contract-validation",
            "executive_brief_validation": f"{prefix}://ci/phase8/executive-health-rollup/executive-brief-validation",
            "redaction_validation": f"{prefix}://ci/phase8/executive-health-rollup/redaction-validation",
        },
        "rollup_evidence_refs": [
            f"{prefix}://phase8/executive-health-rollup/customer-health-review-source",
            f"{prefix}://phase8/executive-health-rollup/rollup-contract",
            f"{prefix}://phase8/executive-health-rollup/executive-brief",
            f"{prefix}://phase8/executive-health-rollup/next-actions",
        ],
        "rollup_controls": {
            "customer_health_review_ready": health_review_result["blocker_count"] == 0,
            "decision_refs_defined": True,
            "trend_refs_defined": True,
            "risk_posture_defined": True,
            "support_status_defined": True,
            "adoption_status_defined": True,
            "next_action_readiness_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_executive_health_rollup_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_HEALTH_ROLLUP_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 executive health rollup schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_HEALTH_ROLLUP_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_HEALTH_ROLLUP_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_health_review_ref"), checks, "customer_health_review_ref")
    _check_health_review_result(packet.get("customer_health_review_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("executive_owner_refs", {}), REQUIRED_EXECUTIVE_OWNER_REFS, checks)
    _check_rollup_contract(packet.get("executive_rollup_contract", {}), checks)
    _check_ref_list(packet.get("executive_brief_refs", []), checks, "executive_brief_refs", min_count=4)
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("rollup_evidence_refs", []), checks, "rollup_evidence_refs", min_count=4)
    _check_controls(packet.get("rollup_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_executive_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 executive health rollup contains sanitized refs and customer-safe executive text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_EXECUTIVE_HEALTH_ROLLUP_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_executive_health_rollup": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_executive_health_rollup_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(sample)
    live_result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-executive-health-rollup.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-phase8-executive-health-rollup.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-executive-health-rollup.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-executive-health-rollup.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-executive-health-rollup.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_executive_health_rollup": live_result[
            "ready_for_customer_lifecycle_phase8_executive_health_rollup"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 executive health rollup supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 executive health rollup validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Executive health rollup requires evidence_mode=live and sanitized=true.")


def _check_health_review_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "customer_health_review_result", "blocker", "customer_health_review_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_customer_health_review") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "customer_health_review_result", "pass", "Source customer health review is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "customer_health_review_result", "warn", "Source customer health review validates shape but is not live.")
    else:
        _add_check(checks, "customer_health_review_result", "blocker", "Source customer health review is not ready.")


def _check_required_refs(payload: Any, required: set[str], checks: list[dict[str, str]]) -> None:
    if not isinstance(payload, dict):
        _add_check(checks, "executive_owner_refs", "blocker", "executive_owner_refs must be an object.")
        return
    missing = sorted(field for field in required if not payload.get(field))
    unsafe = sorted(field for field, value in payload.items() if value and not _is_safe_ref(value))
    if not missing and not unsafe:
        _add_check(checks, "executive_owner_refs", "pass", "executive_owner_refs are present and sanitized.")
    else:
        problems = []
        if missing:
            problems.append(f"missing refs: {', '.join(missing)}")
        if unsafe:
            problems.append(f"unsafe refs: {', '.join(unsafe)}")
        _add_check(checks, "executive_owner_refs", "blocker", f"executive_owner_refs are invalid: {'; '.join(problems)}.")


def _check_rollup_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "executive_rollup_contract", "blocker", "executive_rollup_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_ROLLUP_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_ROLLUP_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "executive_rollup_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Executive health rollup contract is complete."
        if not missing and not unsafe and redacted
        else f"Executive health rollup contract invalid: missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}.",
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
        _add_check(checks, "rollup_controls", "blocker", "rollup_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_ROLLUP_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "rollup_controls",
        "pass" if not missing else "blocker",
        "Executive health rollup controls are explicit."
        if not missing
        else f"Executive health rollup controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_executive_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_EXECUTIVE_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_executive_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_executive_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
