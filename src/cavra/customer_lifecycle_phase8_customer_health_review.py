from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_lifecycle_analytics import (
    build_customer_lifecycle_phase8_lifecycle_analytics_packet,
    validate_customer_lifecycle_phase8_lifecycle_analytics_packet,
)
from cavra.customer_lifecycle_phase8_support_automation import (
    build_customer_lifecycle_phase8_support_automation_packet,
    validate_customer_lifecycle_phase8_support_automation_packet,
)
from cavra.customer_lifecycle_phase8_telemetry_depth import (
    build_customer_lifecycle_phase8_telemetry_depth_packet,
    validate_customer_lifecycle_phase8_telemetry_depth_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_CUSTOMER_HEALTH_REVIEW_SCHEMA = (
    "cavra.customer-lifecycle-phase8-customer-health-review.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_CUSTOMER_HEALTH_REVIEW_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-customer-health-review.result.v1"
)

REQUIRED_HEALTH_OWNER_REFS = {
    "program_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "analytics_owner_ref",
    "security_owner_ref",
}

REQUIRED_INPUT_REFS = {
    "telemetry_depth_ref",
    "support_automation_ref",
    "lifecycle_analytics_ref",
}

REQUIRED_REVIEW_FIELDS = {
    "review_ref",
    "telemetry_summary_ref",
    "support_summary_ref",
    "lifecycle_summary_ref",
    "risk_review_ref",
    "next_action_ref",
    "redaction_status",
}

REQUIRED_CI_GATES = {
    "input_gate_validation",
    "review_contract_validation",
    "dashboard_validation",
    "redaction_validation",
}

REQUIRED_HEALTH_CONTROLS = {
    "telemetry_depth_ready",
    "support_automation_ready",
    "lifecycle_analytics_ready",
    "review_contract_defined",
    "dashboard_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_HEALTH_FIELDS = {
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


def build_customer_lifecycle_phase8_customer_health_review_packet(
    telemetry_packet: dict[str, Any] | None = None,
    support_packet: dict[str, Any] | None = None,
    analytics_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    telemetry = telemetry_packet or build_customer_lifecycle_phase8_telemetry_depth_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    support = support_packet or build_customer_lifecycle_phase8_support_automation_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    analytics = analytics_packet or build_customer_lifecycle_phase8_lifecycle_analytics_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    require_live = evidence_mode == "live"
    telemetry_result = validate_customer_lifecycle_phase8_telemetry_depth_packet(telemetry, require_live=require_live)
    support_result = validate_customer_lifecycle_phase8_support_automation_packet(support, require_live=require_live)
    analytics_result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(analytics, require_live=require_live)
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_CUSTOMER_HEALTH_REVIEW_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "customer_health_review_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-customer-health-review",
        "phase8_input_refs": {
            "telemetry_depth_ref": f"{prefix}://customer-lifecycle-phase8-telemetry-depth/r7",
            "support_automation_ref": f"{prefix}://customer-lifecycle-phase8-support-automation/r7",
            "lifecycle_analytics_ref": f"{prefix}://customer-lifecycle-phase8-lifecycle-analytics/r7",
        },
        "phase8_input_results": {
            "telemetry_depth_result": telemetry_result,
            "support_automation_result": support_result,
            "lifecycle_analytics_result": analytics_result,
        },
        "health_owner_refs": {
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "analytics_owner_ref": f"{prefix}://owner/product-analytics",
            "security_owner_ref": f"{prefix}://owner/security-platform",
        },
        "health_review_contract": {
            "review_ref": f"{prefix}://phase8/customer-health-review/review",
            "telemetry_summary_ref": f"{prefix}://phase8/customer-health-review/telemetry-summary",
            "support_summary_ref": f"{prefix}://phase8/customer-health-review/support-summary",
            "lifecycle_summary_ref": f"{prefix}://phase8/customer-health-review/lifecycle-summary",
            "risk_review_ref": f"{prefix}://phase8/customer-health-review/risk-review",
            "next_action_ref": f"{prefix}://phase8/customer-health-review/next-actions",
            "redaction_status": "sanitized",
        },
        "health_dashboard_refs": [
            f"{prefix}://phase8/customer-health-review/dashboard/posture",
            f"{prefix}://phase8/customer-health-review/dashboard/support-load",
            f"{prefix}://phase8/customer-health-review/dashboard/adoption",
            f"{prefix}://phase8/customer-health-review/dashboard/cadence",
        ],
        "ci_gate_coverage": {
            "input_gate_validation": f"{prefix}://ci/phase8/customer-health-review/input-gate-validation",
            "review_contract_validation": f"{prefix}://ci/phase8/customer-health-review/review-contract-validation",
            "dashboard_validation": f"{prefix}://ci/phase8/customer-health-review/dashboard-validation",
            "redaction_validation": f"{prefix}://ci/phase8/customer-health-review/redaction-validation",
        },
        "health_evidence_refs": [
            f"{prefix}://phase8/customer-health-review/input-gate-summary",
            f"{prefix}://phase8/customer-health-review/review-contract",
            f"{prefix}://phase8/customer-health-review/dashboard-refs",
            f"{prefix}://phase8/customer-health-review/next-actions",
        ],
        "health_controls": {
            "telemetry_depth_ready": telemetry_result["blocker_count"] == 0,
            "support_automation_ready": support_result["blocker_count"] == 0,
            "lifecycle_analytics_ready": analytics_result["blocker_count"] == 0,
            "review_contract_defined": True,
            "dashboard_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_customer_health_review_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_CUSTOMER_HEALTH_REVIEW_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 customer health review schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_CUSTOMER_HEALTH_REVIEW_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_CUSTOMER_HEALTH_REVIEW_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_required_refs(packet.get("phase8_input_refs", {}), REQUIRED_INPUT_REFS, checks, "phase8_input_refs")
    _check_input_results(packet.get("phase8_input_results", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("health_owner_refs", {}), REQUIRED_HEALTH_OWNER_REFS, checks, "health_owner_refs")
    _check_health_review_contract(packet.get("health_review_contract", {}), checks)
    _check_ref_list(packet.get("health_dashboard_refs", []), checks, "health_dashboard_refs", min_count=4)
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("health_evidence_refs", []), checks, "health_evidence_refs", min_count=4)
    _check_controls(packet.get("health_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_health_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 customer health review contains sanitized refs and customer-safe health review text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_CUSTOMER_HEALTH_REVIEW_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_customer_health_review": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_customer_health_review_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_customer_health_review_packet(sample)
    live_result = validate_customer_lifecycle_phase8_customer_health_review_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-customer-health-review.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-phase8-customer-health-review.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-customer-health-review.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-customer-health-review.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-customer-health-review.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_customer_health_review": live_result[
            "ready_for_customer_lifecycle_phase8_customer_health_review"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 customer health review supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 customer health review validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Customer health review requires evidence_mode=live and sanitized=true.")


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


def _check_input_results(results: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(results, dict):
        _add_check(checks, "phase8_input_results", "blocker", "phase8_input_results must be an object.")
        return
    required = {
        "telemetry_depth_result": "ready_for_customer_lifecycle_phase8_telemetry_depth",
        "support_automation_result": "ready_for_customer_lifecycle_phase8_support_automation",
        "lifecycle_analytics_result": "ready_for_customer_lifecycle_phase8_lifecycle_analytics",
    }
    missing = sorted(name for name in required if not isinstance(results.get(name), dict))
    blockers = sorted(
        name
        for name, readiness_key in required.items()
        if isinstance(results.get(name), dict) and int(results[name].get("blocker_count", 1)) > 0
    )
    not_ready = sorted(
        name
        for name, readiness_key in required.items()
        if require_live and isinstance(results.get(name), dict) and results[name].get(readiness_key) is not True
    )
    warnings = sorted(
        name
        for name in required
        if isinstance(results.get(name), dict) and int(results[name].get("warning_count", 0)) > 0
    )
    if missing or blockers or not_ready:
        _add_check(
            checks,
            "phase8_input_results",
            "blocker",
            "Phase 8 input results are not ready: "
            f"missing {', '.join(missing) or 'none'}; blockers {', '.join(blockers) or 'none'}; "
            f"not ready {', '.join(not_ready) or 'none'}.",
        )
    elif warnings and not require_live:
        _add_check(checks, "phase8_input_results", "warn", "Sample Phase 8 input results validate shape but are not live.")
    else:
        _add_check(checks, "phase8_input_results", "pass", "Phase 8 input results are ready.")


def _check_health_review_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "health_review_contract", "blocker", "health_review_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_REVIEW_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_REVIEW_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "health_review_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Customer health review contract is complete."
        if not missing and not unsafe and redacted
        else f"Customer health review contract invalid: missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}.",
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
        _add_check(checks, "health_controls", "blocker", "health_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_HEALTH_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "health_controls",
        "pass" if not missing else "blocker",
        "Customer health review controls are explicit."
        if not missing
        else f"Customer health review controls missing or false: {', '.join(missing)}.",
    )


def _prefix(evidence_mode: str) -> str:
    return "sample" if evidence_mode == "sample" else "evidence"


def _is_safe_ref(value: Any) -> bool:
    text = str(value)
    return any(text.startswith(prefix) for prefix in ALLOWED_REF_PREFIXES)


def _find_forbidden_phase8_health_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_HEALTH_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_health_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_health_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
