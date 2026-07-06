from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_refresh_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_OPERATING_LOOP_INDEX_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-operating-loop-index.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_OPERATING_LOOP_INDEX_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-operating-loop-index.result.v1"
)

REQUIRED_OPERATING_LOOP_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
}

REQUIRED_OPERATING_LOOP_CONTRACT_FIELDS = {
    "operating_loop_index_ref",
    "source_refresh_closeout_ref",
    "publication_closeout_ref",
    "refresh_checkpoint_ref",
    "refresh_closeout_ref",
    "cadence_ref",
    "loop_health_ref",
    "next_cycle_trigger_ref",
    "governance_review_ref",
    "redaction_status",
}

REQUIRED_LOOP_DEPENDENCY_REFS = {
    "public_operating_scorecard_ref",
    "publication_closeout_ref",
    "refresh_checkpoint_ref",
    "refresh_closeout_ref",
    "next_cycle_readiness_ref",
}

REQUIRED_LOOP_CADENCE_REFS = {
    "active_loop_cadence_ref",
    "last_loop_completion_ref",
    "next_loop_due_ref",
    "exception_handling_ref",
}

REQUIRED_LOOP_HEALTH_REFS = {
    "loop_health_summary_ref",
    "publication_freshness_ref",
    "owner_response_slo_ref",
    "stale_resolution_slo_ref",
}

REQUIRED_LOOP_ARCHIVE_REFS = {
    "operating_loop_manifest_ref",
    "publication_archive_ref",
    "refresh_archive_ref",
    "closeout_archive_ref",
}

REQUIRED_NEXT_CYCLE_TRIGGER_REFS = {
    "next_public_scorecard_cycle_ref",
    "next_refresh_checkpoint_trigger_ref",
    "next_closeout_trigger_ref",
    "owner_review_trigger_ref",
}

REQUIRED_GOVERNANCE_REFS = {
    "executive_review_ref",
    "communications_review_ref",
    "security_review_ref",
    "product_review_ref",
}

REQUIRED_CI_GATES = {
    "source_refresh_closeout_validation",
    "dependency_index_validation",
    "cadence_validation",
    "loop_health_validation",
    "archive_validation",
    "next_cycle_trigger_validation",
    "governance_validation",
    "redaction_validation",
}

REQUIRED_OPERATING_LOOP_CONTROLS = {
    "refresh_closeout_ready",
    "dependency_refs_defined",
    "cadence_refs_defined",
    "loop_health_refs_defined",
    "archive_refs_defined",
    "next_cycle_trigger_refs_defined",
    "governance_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_OPERATING_LOOP_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_health_score",
    "customer_name",
    "customer_score",
    "customer_status",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_archive",
    "raw_audit",
    "raw_contract",
    "raw_dashboard",
    "raw_dependency",
    "raw_evidence",
    "raw_governance",
    "raw_health",
    "raw_loop",
    "raw_notification",
    "raw_publication",
    "raw_refresh",
    "raw_resolution",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "raw_trigger",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
    refresh_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    refresh_closeout = (
        refresh_closeout_packet
        or build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    refresh_closeout_result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
        refresh_closeout,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_OPERATING_LOOP_INDEX_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "operating_loop_index_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-operating-loop-index",
        "refresh_closeout_ref": f"{prefix}://customer-lifecycle-phase8-public-scorecard-refresh-closeout/r7",
        "refresh_closeout_result": refresh_closeout_result,
        "operating_loop_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "operating_loop_contract": {
            "operating_loop_index_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/index",
            "source_refresh_closeout_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/source-refresh-closeout",
            "publication_closeout_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/publication-closeout",
            "refresh_checkpoint_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/refresh-checkpoint",
            "refresh_closeout_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/refresh-closeout",
            "cadence_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/cadence",
            "loop_health_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/loop-health",
            "next_cycle_trigger_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/next-cycle-trigger",
            "governance_review_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/governance-review",
            "redaction_status": "sanitized",
        },
        "loop_dependency_refs": {
            "public_operating_scorecard_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/dependency/public-operating-scorecard",
            "publication_closeout_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/dependency/publication-closeout",
            "refresh_checkpoint_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/dependency/refresh-checkpoint",
            "refresh_closeout_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/dependency/refresh-closeout",
            "next_cycle_readiness_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/dependency/next-cycle-readiness",
        },
        "loop_cadence_refs": {
            "active_loop_cadence_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/cadence/active",
            "last_loop_completion_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/cadence/last-completion",
            "next_loop_due_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/cadence/next-due",
            "exception_handling_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/cadence/exceptions",
        },
        "loop_health_refs": {
            "loop_health_summary_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/health/summary",
            "publication_freshness_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/health/publication-freshness",
            "owner_response_slo_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/health/owner-response-slo",
            "stale_resolution_slo_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/health/stale-resolution-slo",
        },
        "loop_archive_refs": {
            "operating_loop_manifest_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/archive/manifest",
            "publication_archive_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/archive/publication",
            "refresh_archive_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/archive/refresh",
            "closeout_archive_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/archive/closeout",
        },
        "next_cycle_trigger_refs": {
            "next_public_scorecard_cycle_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/next-cycle/public-scorecard",
            "next_refresh_checkpoint_trigger_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/next-cycle/refresh-checkpoint",
            "next_closeout_trigger_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/next-cycle/closeout",
            "owner_review_trigger_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/next-cycle/owner-review",
        },
        "governance_review_refs": {
            "executive_review_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/governance/executive",
            "communications_review_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/governance/communications",
            "security_review_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/governance/security",
            "product_review_ref": f"{prefix}://phase8/public-scorecard-operating-loop-index/governance/product",
        },
        "ci_gate_coverage": {
            "source_refresh_closeout_validation": f"{prefix}://ci/phase8/public-scorecard-operating-loop-index/source-refresh-closeout-validation",
            "dependency_index_validation": f"{prefix}://ci/phase8/public-scorecard-operating-loop-index/dependency-index-validation",
            "cadence_validation": f"{prefix}://ci/phase8/public-scorecard-operating-loop-index/cadence-validation",
            "loop_health_validation": f"{prefix}://ci/phase8/public-scorecard-operating-loop-index/loop-health-validation",
            "archive_validation": f"{prefix}://ci/phase8/public-scorecard-operating-loop-index/archive-validation",
            "next_cycle_trigger_validation": f"{prefix}://ci/phase8/public-scorecard-operating-loop-index/next-cycle-trigger-validation",
            "governance_validation": f"{prefix}://ci/phase8/public-scorecard-operating-loop-index/governance-validation",
            "redaction_validation": f"{prefix}://ci/phase8/public-scorecard-operating-loop-index/redaction-validation",
        },
        "operating_loop_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-operating-loop-index/source-refresh-closeout",
            f"{prefix}://phase8/public-scorecard-operating-loop-index/dependency-index",
            f"{prefix}://phase8/public-scorecard-operating-loop-index/cadence",
            f"{prefix}://phase8/public-scorecard-operating-loop-index/loop-health",
            f"{prefix}://phase8/public-scorecard-operating-loop-index/archive",
            f"{prefix}://phase8/public-scorecard-operating-loop-index/next-cycle-triggers",
            f"{prefix}://phase8/public-scorecard-operating-loop-index/governance",
        ],
        "operating_loop_controls": {
            "refresh_closeout_ready": refresh_closeout_result["blocker_count"] == 0,
            "dependency_refs_defined": True,
            "cadence_refs_defined": True,
            "loop_health_refs_defined": True,
            "archive_refs_defined": True,
            "next_cycle_trigger_refs_defined": True,
            "governance_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass"
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_OPERATING_LOOP_INDEX_SCHEMA
        else "blocker",
        "Customer lifecycle Phase 8 public scorecard operating loop index schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_OPERATING_LOOP_INDEX_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_OPERATING_LOOP_INDEX_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("refresh_closeout_ref"), checks, "refresh_closeout_ref")
    _check_refresh_closeout_result(packet.get("refresh_closeout_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("operating_loop_owner_refs", {}),
        REQUIRED_OPERATING_LOOP_OWNER_REFS,
        checks,
        "operating_loop_owner_refs",
    )
    _check_operating_loop_contract(packet.get("operating_loop_contract", {}), checks)
    _check_required_refs(
        packet.get("loop_dependency_refs", {}),
        REQUIRED_LOOP_DEPENDENCY_REFS,
        checks,
        "loop_dependency_refs",
    )
    _check_required_refs(packet.get("loop_cadence_refs", {}), REQUIRED_LOOP_CADENCE_REFS, checks, "loop_cadence_refs")
    _check_required_refs(packet.get("loop_health_refs", {}), REQUIRED_LOOP_HEALTH_REFS, checks, "loop_health_refs")
    _check_required_refs(packet.get("loop_archive_refs", {}), REQUIRED_LOOP_ARCHIVE_REFS, checks, "loop_archive_refs")
    _check_required_refs(
        packet.get("next_cycle_trigger_refs", {}),
        REQUIRED_NEXT_CYCLE_TRIGGER_REFS,
        checks,
        "next_cycle_trigger_refs",
    )
    _check_required_refs(
        packet.get("governance_review_refs", {}),
        REQUIRED_GOVERNANCE_REFS,
        checks,
        "governance_review_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("operating_loop_evidence_refs", []), checks, "operating_loop_evidence_refs", min_count=7)
    _check_controls(packet.get("operating_loop_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_operating_loop_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard operating loop index contains sanitized refs and public-safe loop refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_OPERATING_LOOP_INDEX_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_operating_loop_index_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-operating-loop-index.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-operating-loop-index.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-scorecard-operating-loop-index.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-operating-loop-index.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-operating-loop-index.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 public scorecard operating loop index supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 public scorecard operating loop index validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Public scorecard operating loop index requires evidence_mode=live and sanitized=true.",
        )


def _check_refresh_closeout_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "refresh_closeout_result", "blocker", "refresh_closeout_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "refresh_closeout_result", "pass", "Source public scorecard refresh closeout is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "refresh_closeout_result",
            "warn",
            "Source public scorecard refresh closeout validates shape but is not live.",
        )
    else:
        _add_check(checks, "refresh_closeout_result", "blocker", "Source public scorecard refresh closeout is not ready.")


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


def _check_operating_loop_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "operating_loop_contract", "blocker", "operating_loop_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_OPERATING_LOOP_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_OPERATING_LOOP_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "operating_loop_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard operating loop index contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard operating loop index contract invalid: "
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
        _add_check(checks, "operating_loop_controls", "blocker", "operating_loop_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_OPERATING_LOOP_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "operating_loop_controls",
        "pass" if not missing else "blocker",
        "Public scorecard operating loop index controls are explicit."
        if not missing
        else f"Public scorecard operating loop index controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_operating_loop_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_OPERATING_LOOP_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_operating_loop_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_operating_loop_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
