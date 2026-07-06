from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_next_cycle_readiness_index import (
    build_customer_lifecycle_phase8_next_cycle_readiness_index_packet,
    validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_OPERATING_SCORECARD_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-operating-scorecard.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_OPERATING_SCORECARD_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-operating-scorecard.result.v1"
)

REQUIRED_PUBLIC_SCORECARD_OWNER_REFS = {
    "executive_owner_ref",
    "program_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
}

REQUIRED_SCORECARD_CONTRACT_FIELDS = {
    "scorecard_ref",
    "public_status_ref",
    "trend_summary_ref",
    "release_decision_ref",
    "evidence_archive_ref",
    "executive_summary_ref",
    "publication_channel_ref",
    "redaction_status",
}

REQUIRED_STATUS_REFS = {
    "operating_readiness_ref",
    "release_gate_status_ref",
    "evidence_archive_status_ref",
    "customer_success_status_ref",
    "support_status_ref",
    "security_status_ref",
}

REQUIRED_TREND_REFS = {
    "posture_trend_ref",
    "adoption_trend_ref",
    "support_trend_ref",
    "lifecycle_trend_ref",
}

REQUIRED_RELEASE_DECISION_REFS = {
    "publish_go_ref",
    "hold_reason_ref",
    "refresh_cadence_ref",
    "evidence_archive_gate_ref",
}

REQUIRED_CI_GATES = {
    "source_readiness_index_validation",
    "scorecard_contract_validation",
    "status_ref_validation",
    "trend_ref_validation",
    "publication_redaction_validation",
}

REQUIRED_SCORECARD_CONTROLS = {
    "next_cycle_readiness_index_ready",
    "public_scorecard_defined",
    "status_refs_defined",
    "trend_refs_defined",
    "release_decision_refs_defined",
    "executive_summary_refs_defined",
    "publication_channel_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_SCORECARD_FIELDS = {
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
    "raw_acceptance",
    "raw_contract",
    "raw_dashboard",
    "raw_evidence",
    "raw_index",
    "raw_readiness",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "raw_trend",
    "renewal_amount",
    "score_detail",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_operating_scorecard_packet(
    next_cycle_readiness_index_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    readiness_index = (
        next_cycle_readiness_index_packet
        or build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    readiness_index_result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
        readiness_index,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_OPERATING_SCORECARD_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "public_operating_scorecard_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-operating-scorecard",
        "next_cycle_readiness_index_ref": f"{prefix}://customer-lifecycle-phase8-next-cycle-readiness-index/r7",
        "next_cycle_readiness_index_result": readiness_index_result,
        "public_scorecard_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "public_operating_scorecard_contract": {
            "scorecard_ref": f"{prefix}://phase8/public-operating-scorecard/scorecard",
            "public_status_ref": f"{prefix}://phase8/public-operating-scorecard/public-status",
            "trend_summary_ref": f"{prefix}://phase8/public-operating-scorecard/trend-summary",
            "release_decision_ref": f"{prefix}://phase8/public-operating-scorecard/release-decision",
            "evidence_archive_ref": f"{prefix}://phase8/public-operating-scorecard/evidence-archive",
            "executive_summary_ref": f"{prefix}://phase8/public-operating-scorecard/executive-summary",
            "publication_channel_ref": f"{prefix}://phase8/public-operating-scorecard/publication-channel",
            "redaction_status": "sanitized",
        },
        "public_status_refs": {
            "operating_readiness_ref": f"{prefix}://phase8/public-operating-scorecard/status/operating-readiness",
            "release_gate_status_ref": f"{prefix}://phase8/public-operating-scorecard/status/release-gate",
            "evidence_archive_status_ref": f"{prefix}://phase8/public-operating-scorecard/status/evidence-archive",
            "customer_success_status_ref": f"{prefix}://phase8/public-operating-scorecard/status/customer-success",
            "support_status_ref": f"{prefix}://phase8/public-operating-scorecard/status/support",
            "security_status_ref": f"{prefix}://phase8/public-operating-scorecard/status/security",
        },
        "public_trend_refs": {
            "posture_trend_ref": f"{prefix}://phase8/public-operating-scorecard/trend/posture",
            "adoption_trend_ref": f"{prefix}://phase8/public-operating-scorecard/trend/adoption",
            "support_trend_ref": f"{prefix}://phase8/public-operating-scorecard/trend/support",
            "lifecycle_trend_ref": f"{prefix}://phase8/public-operating-scorecard/trend/lifecycle",
        },
        "release_decision_refs": {
            "publish_go_ref": f"{prefix}://phase8/public-operating-scorecard/decision/publish-go",
            "hold_reason_ref": f"{prefix}://phase8/public-operating-scorecard/decision/hold-reason",
            "refresh_cadence_ref": f"{prefix}://phase8/public-operating-scorecard/decision/refresh-cadence",
            "evidence_archive_gate_ref": f"{prefix}://phase8/public-operating-scorecard/decision/evidence-archive-gate",
        },
        "executive_summary_refs": [
            f"{prefix}://phase8/public-operating-scorecard/summary/executive",
            f"{prefix}://phase8/public-operating-scorecard/summary/security",
            f"{prefix}://phase8/public-operating-scorecard/summary/customer-success",
        ],
        "ci_gate_coverage": {
            "source_readiness_index_validation": f"{prefix}://ci/phase8/public-operating-scorecard/source-readiness-index-validation",
            "scorecard_contract_validation": f"{prefix}://ci/phase8/public-operating-scorecard/scorecard-contract-validation",
            "status_ref_validation": f"{prefix}://ci/phase8/public-operating-scorecard/status-ref-validation",
            "trend_ref_validation": f"{prefix}://ci/phase8/public-operating-scorecard/trend-ref-validation",
            "publication_redaction_validation": f"{prefix}://ci/phase8/public-operating-scorecard/publication-redaction-validation",
        },
        "publication_evidence_refs": [
            f"{prefix}://phase8/public-operating-scorecard/source-readiness-index",
            f"{prefix}://phase8/public-operating-scorecard/status-refs",
            f"{prefix}://phase8/public-operating-scorecard/trend-refs",
            f"{prefix}://phase8/public-operating-scorecard/release-decision",
            f"{prefix}://phase8/public-operating-scorecard/executive-summary",
        ],
        "scorecard_controls": {
            "next_cycle_readiness_index_ready": readiness_index_result["blocker_count"] == 0,
            "public_scorecard_defined": True,
            "status_refs_defined": True,
            "trend_refs_defined": True,
            "release_decision_refs_defined": True,
            "executive_summary_refs_defined": True,
            "publication_channel_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_operating_scorecard_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass"
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_OPERATING_SCORECARD_SCHEMA
        else "blocker",
        "Customer lifecycle Phase 8 public operating scorecard schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_OPERATING_SCORECARD_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_OPERATING_SCORECARD_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("next_cycle_readiness_index_ref"), checks, "next_cycle_readiness_index_ref")
    _check_readiness_index_result(packet.get("next_cycle_readiness_index_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("public_scorecard_owner_refs", {}),
        REQUIRED_PUBLIC_SCORECARD_OWNER_REFS,
        checks,
        "public_scorecard_owner_refs",
    )
    _check_scorecard_contract(packet.get("public_operating_scorecard_contract", {}), checks)
    _check_required_refs(packet.get("public_status_refs", {}), REQUIRED_STATUS_REFS, checks, "public_status_refs")
    _check_required_refs(packet.get("public_trend_refs", {}), REQUIRED_TREND_REFS, checks, "public_trend_refs")
    _check_required_refs(
        packet.get("release_decision_refs", {}),
        REQUIRED_RELEASE_DECISION_REFS,
        checks,
        "release_decision_refs",
    )
    _check_ref_list(packet.get("executive_summary_refs", []), checks, "executive_summary_refs", min_count=3)
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("publication_evidence_refs", []), checks, "publication_evidence_refs", min_count=5)
    _check_controls(packet.get("scorecard_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_scorecard_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public operating scorecard contains sanitized refs and public-safe summary refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_OPERATING_SCORECARD_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_operating_scorecard": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_operating_scorecard_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_operating_scorecard_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_public_operating_scorecard_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_public_operating_scorecard_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_operating_scorecard_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-operating-scorecard.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-operating-scorecard.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-operating-scorecard.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-public-operating-scorecard.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-operating-scorecard.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_operating_scorecard": live_result[
            "ready_for_customer_lifecycle_phase8_public_operating_scorecard"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 public operating scorecard supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 public operating scorecard validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Public operating scorecard requires evidence_mode=live and sanitized=true.",
        )


def _check_readiness_index_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "next_cycle_readiness_index_result",
            "blocker",
            "next_cycle_readiness_index_result must be an object.",
        )
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_next_cycle_readiness_index") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(
            checks,
            "next_cycle_readiness_index_result",
            "pass",
            "Source next-cycle readiness index is ready.",
        )
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "next_cycle_readiness_index_result",
            "warn",
            "Source next-cycle readiness index validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "next_cycle_readiness_index_result",
            "blocker",
            "Source next-cycle readiness index is not ready.",
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


def _check_scorecard_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(
            checks,
            "public_operating_scorecard_contract",
            "blocker",
            "public_operating_scorecard_contract must be an object.",
        )
        return
    missing = sorted(field for field in REQUIRED_SCORECARD_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_SCORECARD_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "public_operating_scorecard_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public operating scorecard contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public operating scorecard contract invalid: "
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
        _add_check(checks, "scorecard_controls", "blocker", "scorecard_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_SCORECARD_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "scorecard_controls",
        "pass" if not missing else "blocker",
        "Public operating scorecard controls are explicit."
        if not missing
        else f"Public operating scorecard controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_scorecard_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_SCORECARD_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_scorecard_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_scorecard_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
