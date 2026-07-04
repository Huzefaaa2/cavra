from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)
from cavra.customer_renewal_expansion import (
    build_customer_renewal_expansion_packet,
    validate_customer_renewal_expansion_packet,
)


CUSTOMER_RENEWAL_OUTCOME_SCHEMA = "cavra.customer-renewal-outcome-closeout.packet.v1"
CUSTOMER_RENEWAL_OUTCOME_RESULT_SCHEMA = "cavra.customer-renewal-outcome-closeout.result.v1"

REQUIRED_OUTCOME_OWNER_REFS = {
    "account_owner_ref",
    "customer_success_owner_ref",
    "commercial_owner_ref",
    "security_owner_ref",
    "executive_sponsor_ref",
    "finance_operations_ref",
}

REQUIRED_OUTCOME_SECTIONS = {
    "renewal_decision",
    "expansion_decisions",
    "risk_closeout",
    "value_confirmation",
    "contract_handoff",
    "lifecycle_archive",
    "next_success_plan",
}

REQUIRED_OUTCOME_CONTROLS = {
    "renewal_readiness_ready",
    "renewal_outcome_recorded",
    "expansion_decisions_recorded",
    "no_unresolved_blocking_risk",
    "commercial_terms_excluded",
    "security_acceptance_recorded",
    "archive_ready",
    "next_lifecycle_checkpoint_scheduled",
}

HEALTHY_OUTCOME_STATUSES = {
    "recorded",
    "accepted",
    "closed",
    "confirmed",
    "ready",
    "scheduled",
}

FORBIDDEN_RENEWAL_OUTCOME_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_name",
    "private_note",
    "pricing",
    "raw_contract",
    "renewal_amount",
}


def build_customer_renewal_outcome_packet(
    renewal_expansion_packet: dict[str, Any] | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    renewal_expansion = renewal_expansion_packet or build_customer_renewal_expansion_packet(
        evidence_mode=evidence_mode,
    )
    renewal_expansion_result = validate_customer_renewal_expansion_packet(
        renewal_expansion,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_RENEWAL_OUTCOME_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "renewal_outcome_id": f"cavra-{evidence_mode}-customer-renewal-outcome-closeout",
        "customer_profile_ref": renewal_expansion.get("customer_profile_ref", f"{prefix}://customer/redacted"),
        "renewal_readiness_ref": f"{prefix}://customer-renewal-expansion/packet",
        "renewal_readiness_result": renewal_expansion_result,
        "outcome_owner_refs": {
            "account_owner_ref": f"{prefix}://owner/account",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "commercial_owner_ref": f"{prefix}://owner/commercial",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "executive_sponsor_ref": f"{prefix}://owner/executive-sponsor",
            "finance_operations_ref": f"{prefix}://owner/finance-operations",
        },
        "outcome_sections": [
            _outcome_section(
                "renewal_decision",
                "recorded",
                [
                    f"{prefix}://renewal/outcome-record",
                    f"{prefix}://renewal/executive-acceptance",
                ],
            ),
            _outcome_section(
                "expansion_decisions",
                "recorded",
                [
                    f"{prefix}://expansion/approved-scope",
                    f"{prefix}://expansion/deferred-scope",
                    f"{prefix}://expansion/next-evaluation",
                ],
            ),
            _outcome_section(
                "risk_closeout",
                "closed",
                [
                    f"{prefix}://risk/renewal-blocker-closeout",
                    f"{prefix}://security/risk-acceptance-summary",
                ],
            ),
            _outcome_section(
                "value_confirmation",
                "confirmed",
                [
                    f"{prefix}://metrics/value-realization-final",
                    f"{prefix}://metrics/adoption-confirmation",
                    f"{prefix}://metrics/aispm-posture-trend",
                ],
            ),
            _outcome_section(
                "contract_handoff",
                "ready",
                [
                    f"{prefix}://commercial/contract-handoff",
                    "ticket://commercial/finance-ops-handoff",
                ],
            ),
            _outcome_section(
                "lifecycle_archive",
                "ready",
                [
                    f"{prefix}://evidence-room/renewal-outcome-archive",
                    f"{prefix}://audit/renewal-outcome-manifest",
                ],
            ),
            _outcome_section(
                "next_success_plan",
                "scheduled",
                [
                    f"{prefix}://success/next-quarter-plan",
                    f"{prefix}://operating-review/next-cycle",
                ],
            ),
        ],
        "expansion_outcomes": [
            {
                "candidate_id": "govern-more-agents",
                "decision_ref": f"{prefix}://expansion/govern-more-agents/decision",
                "owner_ref": f"{prefix}://owner/customer-success",
                "next_step_ref": f"{prefix}://expansion/govern-more-agents/activation-plan",
            },
            {
                "candidate_id": "aispm-deeper-connectors",
                "decision_ref": f"{prefix}://expansion/aispm-connectors/decision",
                "owner_ref": f"{prefix}://owner/security-platform",
                "next_step_ref": f"{prefix}://expansion/aispm-connectors/connector-plan",
            },
        ],
        "outcome_controls": {
            "renewal_readiness_ready": renewal_expansion_result["blocker_count"] == 0,
            "renewal_outcome_recorded": True,
            "expansion_decisions_recorded": True,
            "no_unresolved_blocking_risk": True,
            "commercial_terms_excluded": True,
            "security_acceptance_recorded": True,
            "archive_ready": True,
            "next_lifecycle_checkpoint_scheduled": True,
        },
    }


def validate_customer_renewal_outcome_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_RENEWAL_OUTCOME_SCHEMA else "blocker",
        "Customer renewal outcome closeout schema is valid."
        if packet.get("schema_version") == CUSTOMER_RENEWAL_OUTCOME_SCHEMA
        else f"Packet must use {CUSTOMER_RENEWAL_OUTCOME_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_profile_ref"), checks, "customer_profile_ref")
    _check_safe_ref(packet.get("renewal_readiness_ref"), checks, "renewal_readiness_ref")
    _check_renewal_readiness_result(packet.get("renewal_readiness_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("outcome_owner_refs", {}), REQUIRED_OUTCOME_OWNER_REFS, checks, "outcome_owner_refs")
    _check_outcome_sections(packet.get("outcome_sections", []), checks)
    _check_expansion_outcomes(packet.get("expansion_outcomes", []), checks)
    _check_outcome_controls(packet.get("outcome_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_renewal_outcome_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Renewal outcome packet contains sanitized refs and control metadata only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_RENEWAL_OUTCOME_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_renewal_outcome_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_renewal_outcome_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_renewal_outcome_packet(evidence_mode="sample")
    live = build_customer_renewal_outcome_packet(evidence_mode="live")
    sample_result = validate_customer_renewal_outcome_packet(sample)
    live_result = validate_customer_renewal_outcome_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-renewal-outcome.sample.json",
        "live_sanitized_example": output_dir / "customer-renewal-outcome.live.sanitized.example.json",
        "sample_result": output_dir / "customer-renewal-outcome.sample.result.json",
        "live_result": output_dir / "customer-renewal-outcome.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-renewal-outcome-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_renewal_outcome_closeout": live_result["ready_for_customer_renewal_outcome_closeout"],
    }


def _outcome_section(section_id: str, status: str, refs: list[Any]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "status": status,
        "evidence_refs": [str(ref) for ref in refs if ref],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized customer renewal outcome packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample renewal outcome packet validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Renewal outcome requires evidence_mode=live and sanitized=true.")


def _check_renewal_readiness_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "renewal_readiness_result", "blocker", "renewal_readiness_result must be an object.")
        return
    ready = result.get("ready_for_customer_renewal_expansion") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "renewal_readiness_result", "pass", "Source customer renewal expansion readiness is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "renewal_readiness_result", "warn", "Source renewal readiness validates shape but is not live.")
    else:
        _add_check(checks, "renewal_readiness_result", "blocker", "Source customer renewal expansion readiness is not ready.")


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


def _check_outcome_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "outcome_sections", "blocker", "outcome_sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing = sorted(REQUIRED_OUTCOME_SECTIONS - set(section_by_id))
    bad_statuses: list[str] = []
    bad_refs: list[str] = []
    empty_sections: list[str] = []
    for section_id, section in section_by_id.items():
        if str(section.get("status", "")) not in HEALTHY_OUTCOME_STATUSES:
            bad_statuses.append(section_id)
        refs = section.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            empty_sections.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing and not bad_statuses and not bad_refs and not empty_sections:
        _add_check(checks, "outcome_sections", "pass", "Renewal outcome sections are complete and healthy.")
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
        _add_check(checks, "outcome_sections", "blocker", f"Renewal outcome sections invalid: {'; '.join(problems)}.")


def _check_expansion_outcomes(outcomes: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(outcomes, list) or not outcomes:
        _add_check(checks, "expansion_outcomes", "blocker", "expansion_outcomes must be a non-empty list.")
        return
    unsafe: list[str] = []
    for index, outcome in enumerate(outcomes):
        if not isinstance(outcome, dict):
            unsafe.append(f"{index}:not-object")
            continue
        for field in ("decision_ref", "owner_ref", "next_step_ref"):
            if not _is_safe_ref(outcome.get(field)):
                unsafe.append(f"{index}:{field}")
    _add_check(
        checks,
        "expansion_outcomes",
        "pass" if not unsafe else "blocker",
        "Expansion outcomes are explicit and sanitized."
        if not unsafe
        else f"Expansion outcomes contain missing or unsafe refs: {', '.join(unsafe)}.",
    )


def _check_outcome_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "outcome_controls", "blocker", "outcome_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_OUTCOME_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "outcome_controls",
        "pass" if not missing else "blocker",
        "Renewal outcome controls are explicit."
        if not missing
        else f"Renewal outcome controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_renewal_outcome_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_RENEWAL_OUTCOME_FIELDS:
                found.add(path)
            found.update(_find_forbidden_renewal_outcome_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_renewal_outcome_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
