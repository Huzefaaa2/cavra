from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)
from cavra.customer_operating_review import (
    build_customer_operating_review_packet,
    validate_customer_operating_review_packet,
)


CUSTOMER_RENEWAL_EXPANSION_SCHEMA = "cavra.customer-renewal-expansion.packet.v1"
CUSTOMER_RENEWAL_EXPANSION_RESULT_SCHEMA = "cavra.customer-renewal-expansion.result.v1"

REQUIRED_RENEWAL_OWNER_REFS = {
    "account_owner_ref",
    "customer_success_owner_ref",
    "commercial_owner_ref",
    "security_owner_ref",
    "executive_sponsor_ref",
}

REQUIRED_RENEWAL_SECTIONS = {
    "value_realization",
    "adoption_depth",
    "posture_continuity",
    "unresolved_risk",
    "expansion_candidates",
    "commercial_handoff",
}

REQUIRED_RENEWAL_CONTROLS = {
    "operating_review_ready",
    "value_realization_current",
    "adoption_threshold_met",
    "aispm_posture_ready",
    "no_unresolved_blocking_risk",
    "expansion_candidates_reviewed",
    "commercial_handoff_ready",
    "next_checkpoint_scheduled",
}

HEALTHY_RENEWAL_STATUSES = {
    "realized",
    "adopted",
    "ready",
    "none_blocking",
    "reviewed",
    "scheduled",
}


def build_customer_renewal_expansion_packet(
    operating_review_packet: dict[str, Any] | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    operating_review = operating_review_packet or build_customer_operating_review_packet(evidence_mode=evidence_mode)
    operating_review_result = validate_customer_operating_review_packet(
        operating_review,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_RENEWAL_EXPANSION_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "renewal_readiness_id": f"cavra-{evidence_mode}-customer-renewal-expansion",
        "customer_profile_ref": operating_review.get("customer_profile_ref", f"{prefix}://customer/redacted"),
        "operating_review_ref": f"{prefix}://customer-operating-review/packet",
        "operating_review_result": operating_review_result,
        "renewal_owner_refs": {
            "account_owner_ref": f"{prefix}://owner/account",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "commercial_owner_ref": f"{prefix}://owner/commercial",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "executive_sponsor_ref": f"{prefix}://owner/executive-sponsor",
        },
        "renewal_sections": [
            _renewal_section(
                "value_realization",
                "realized",
                [
                    f"{prefix}://metrics/value-realization",
                    f"{prefix}://metrics/risk-reduction",
                    f"{prefix}://metrics/evidence-cycle-time",
                ],
            ),
            _renewal_section(
                "adoption_depth",
                "adopted",
                [
                    f"{prefix}://metrics/governed-agents",
                    f"{prefix}://metrics/governed-workflows",
                    f"{prefix}://metrics/policy-coverage",
                ],
            ),
            _renewal_section(
                "posture_continuity",
                "ready",
                [
                    f"{prefix}://aispm/posture-trend",
                    f"{prefix}://aispm/drift-exceptions",
                    f"{prefix}://evidence-room/freshness-report",
                ],
            ),
            _renewal_section(
                "unresolved_risk",
                "none_blocking",
                [
                    f"{prefix}://risk/register",
                    f"{prefix}://risk/blocker-review",
                ],
            ),
            _renewal_section(
                "expansion_candidates",
                "reviewed",
                [
                    f"{prefix}://expansion/cloud-agents",
                    f"{prefix}://expansion/mcp-tools",
                    f"{prefix}://expansion/connector-pack",
                ],
            ),
            _renewal_section(
                "commercial_handoff",
                "scheduled",
                [
                    f"{prefix}://commercial/renewal-pack",
                    "ticket://commercial/renewal-handoff",
                ],
            ),
        ],
        "expansion_candidates": [
            {
                "candidate_id": "govern-more-agents",
                "value_ref": f"{prefix}://expansion/govern-more-agents/value",
                "owner_ref": f"{prefix}://owner/customer-success",
                "readiness_ref": f"{prefix}://expansion/govern-more-agents/readiness",
            },
            {
                "candidate_id": "aispm-deeper-connectors",
                "value_ref": f"{prefix}://expansion/aispm-connectors/value",
                "owner_ref": f"{prefix}://owner/security-platform",
                "readiness_ref": f"{prefix}://expansion/aispm-connectors/readiness",
            },
        ],
        "renewal_controls": {
            "operating_review_ready": operating_review_result["blocker_count"] == 0,
            "value_realization_current": True,
            "adoption_threshold_met": True,
            "aispm_posture_ready": True,
            "no_unresolved_blocking_risk": True,
            "expansion_candidates_reviewed": True,
            "commercial_handoff_ready": True,
            "next_checkpoint_scheduled": True,
        },
    }


def validate_customer_renewal_expansion_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_RENEWAL_EXPANSION_SCHEMA else "blocker",
        "Customer renewal expansion schema is valid."
        if packet.get("schema_version") == CUSTOMER_RENEWAL_EXPANSION_SCHEMA
        else f"Packet must use {CUSTOMER_RENEWAL_EXPANSION_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_profile_ref"), checks, "customer_profile_ref")
    _check_safe_ref(packet.get("operating_review_ref"), checks, "operating_review_ref")
    _check_operating_review_result(packet.get("operating_review_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("renewal_owner_refs", {}), REQUIRED_RENEWAL_OWNER_REFS, checks, "renewal_owner_refs")
    _check_renewal_sections(packet.get("renewal_sections", []), checks)
    _check_expansion_candidates(packet.get("expansion_candidates", []), checks)
    _check_renewal_controls(packet.get("renewal_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Renewal expansion packet contains sanitized refs and control metadata only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_RENEWAL_EXPANSION_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_renewal_expansion": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_renewal_expansion_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_renewal_expansion_packet(evidence_mode="sample")
    live = build_customer_renewal_expansion_packet(evidence_mode="live")
    sample_result = validate_customer_renewal_expansion_packet(sample)
    live_result = validate_customer_renewal_expansion_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-renewal-expansion.sample.json",
        "live_sanitized_example": output_dir / "customer-renewal-expansion.live.sanitized.example.json",
        "sample_result": output_dir / "customer-renewal-expansion.sample.result.json",
        "live_result": output_dir / "customer-renewal-expansion.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-renewal-expansion.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_renewal_expansion": live_result["ready_for_customer_renewal_expansion"],
    }


def _renewal_section(section_id: str, status: str, refs: list[Any]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "status": status,
        "evidence_refs": [str(ref) for ref in refs if ref],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized customer renewal expansion packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample renewal expansion packet validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Renewal expansion requires evidence_mode=live and sanitized=true.")


def _check_operating_review_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "operating_review_result", "blocker", "operating_review_result must be an object.")
        return
    ready = result.get("ready_for_customer_operating_review") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "operating_review_result", "pass", "Source customer operating review is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "operating_review_result", "warn", "Source operating review validates shape but is not live.")
    else:
        _add_check(checks, "operating_review_result", "blocker", "Source customer operating review is not ready.")


def _check_required_refs(
    payload: Any,
    required: set[str],
    checks: list[dict[str, str]],
    name: str,
) -> None:
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


def _check_renewal_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "renewal_sections", "blocker", "renewal_sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing = sorted(REQUIRED_RENEWAL_SECTIONS - set(section_by_id))
    bad_statuses: list[str] = []
    bad_refs: list[str] = []
    empty_sections: list[str] = []
    for section_id, section in section_by_id.items():
        if str(section.get("status", "")) not in HEALTHY_RENEWAL_STATUSES:
            bad_statuses.append(section_id)
        refs = section.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            empty_sections.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing and not bad_statuses and not bad_refs and not empty_sections:
        _add_check(checks, "renewal_sections", "pass", "Renewal expansion sections are complete and healthy.")
    else:
        problems = []
        if missing:
            problems.append(f"missing sections: {', '.join(missing)}")
        if bad_statuses:
            problems.append(f"unhealthy statuses: {', '.join(sorted(bad_statuses))}")
        if empty_sections:
            problems.append(f"empty sections: {', '.join(sorted(empty_sections))}")
        if bad_refs:
            problems.append(f"unsafe refs: {', '.join(sorted(bad_refs))}")
        _add_check(checks, "renewal_sections", "blocker", f"Renewal expansion sections invalid: {'; '.join(problems)}.")


def _check_expansion_candidates(candidates: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(candidates, list) or not candidates:
        _add_check(checks, "expansion_candidates", "blocker", "expansion_candidates must be a non-empty list.")
        return
    unsafe: list[str] = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            unsafe.append(f"{index}:not-object")
            continue
        for field in ("value_ref", "owner_ref", "readiness_ref"):
            if not _is_safe_ref(candidate.get(field)):
                unsafe.append(f"{index}:{field}")
    _add_check(
        checks,
        "expansion_candidates",
        "pass" if not unsafe else "blocker",
        "Expansion candidates are explicit and sanitized."
        if not unsafe
        else f"Expansion candidates contain missing or unsafe refs: {', '.join(unsafe)}.",
    )


def _check_renewal_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "renewal_controls", "blocker", "renewal_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_RENEWAL_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "renewal_controls",
        "pass" if not missing else "blocker",
        "Renewal expansion controls are explicit."
        if not missing
        else f"Renewal controls missing or false: {', '.join(missing)}.",
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


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
