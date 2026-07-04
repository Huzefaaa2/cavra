from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_closeout_handoff import (
    build_customer_closeout_handoff_packet,
    validate_customer_closeout_handoff_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_OPERATING_REVIEW_SCHEMA = "cavra.customer-operating-review.packet.v1"
CUSTOMER_OPERATING_REVIEW_RESULT_SCHEMA = "cavra.customer-operating-review.result.v1"

REQUIRED_REVIEW_OWNER_REFS = {
    "customer_success_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
    "executive_sponsor_ref",
}

REQUIRED_REVIEW_SECTIONS = {
    "success_metrics",
    "evidence_freshness",
    "support_sla_health",
    "aispm_posture",
    "open_exclusions",
    "renewal_checkpoint",
}

REQUIRED_REVIEW_CONTROLS = {
    "closeout_handoff_ready",
    "success_metrics_current",
    "evidence_freshness_current",
    "support_sla_healthy",
    "aispm_posture_acceptable",
    "open_exclusions_reviewed",
    "renewal_checkpoint_current",
    "next_review_scheduled",
}

HEALTHY_REVIEW_STATUSES = {"healthy", "none_open", "current", "acceptable", "scheduled"}


def build_customer_operating_review_packet(
    closeout_handoff_packet: dict[str, Any] | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    closeout_handoff = closeout_handoff_packet or build_customer_closeout_handoff_packet(evidence_mode=evidence_mode)
    closeout_handoff_result = validate_customer_closeout_handoff_packet(
        closeout_handoff,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_OPERATING_REVIEW_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "review_id": f"cavra-{evidence_mode}-customer-operating-review",
        "customer_profile_ref": closeout_handoff.get("customer_profile_ref", f"{prefix}://customer/redacted"),
        "closeout_handoff_ref": f"{prefix}://customer-closeout-handoff/packet",
        "closeout_handoff_result": closeout_handoff_result,
        "review_owner_refs": {
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
            "executive_sponsor_ref": f"{prefix}://owner/executive-sponsor",
        },
        "review_sections": [
            _review_section(
                "success_metrics",
                "healthy",
                [
                    f"{prefix}://metrics/adoption",
                    f"{prefix}://metrics/decision-coverage",
                    f"{prefix}://metrics/time-to-approval",
                ],
            ),
            _review_section(
                "evidence_freshness",
                "current",
                [
                    f"{prefix}://evidence-room/freshness-report",
                    f"{prefix}://audit/evidence-custody",
                ],
            ),
            _review_section(
                "support_sla_health",
                "healthy",
                [
                    f"{prefix}://support/sla-dashboard",
                    "ticket://support/escalation-review",
                ],
            ),
            _review_section(
                "aispm_posture",
                "acceptable",
                [
                    f"{prefix}://aispm/posture-score",
                    f"{prefix}://aispm/drift-review",
                    f"{prefix}://aispm/remediation-summary",
                ],
            ),
            _review_section(
                "open_exclusions",
                "none_open",
                [
                    f"{prefix}://exclusion/register",
                    f"{prefix}://risk-acceptance/review",
                ],
            ),
            _review_section(
                "renewal_checkpoint",
                "scheduled",
                [
                    f"{prefix}://commercial/renewal-checkpoint",
                    f"{prefix}://operating-review/next",
                ],
            ),
        ],
        "review_controls": {
            "closeout_handoff_ready": closeout_handoff_result["blocker_count"] == 0,
            "success_metrics_current": True,
            "evidence_freshness_current": True,
            "support_sla_healthy": True,
            "aispm_posture_acceptable": True,
            "open_exclusions_reviewed": True,
            "renewal_checkpoint_current": True,
            "next_review_scheduled": True,
        },
    }


def validate_customer_operating_review_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_OPERATING_REVIEW_SCHEMA else "blocker",
        "Customer operating review schema is valid."
        if packet.get("schema_version") == CUSTOMER_OPERATING_REVIEW_SCHEMA
        else f"Packet must use {CUSTOMER_OPERATING_REVIEW_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_profile_ref"), checks, "customer_profile_ref")
    _check_safe_ref(packet.get("closeout_handoff_ref"), checks, "closeout_handoff_ref")
    _check_closeout_handoff_result(packet.get("closeout_handoff_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("review_owner_refs", {}), REQUIRED_REVIEW_OWNER_REFS, checks, "review_owner_refs")
    _check_review_sections(packet.get("review_sections", []), checks)
    _check_review_controls(packet.get("review_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Operating review contains sanitized refs and control metadata only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_OPERATING_REVIEW_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_operating_review": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_operating_review_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_operating_review_packet(evidence_mode="sample")
    live = build_customer_operating_review_packet(evidence_mode="live")
    sample_result = validate_customer_operating_review_packet(sample)
    live_result = validate_customer_operating_review_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-operating-review.sample.json",
        "live_sanitized_example": output_dir / "customer-operating-review.live.sanitized.example.json",
        "sample_result": output_dir / "customer-operating-review.sample.result.json",
        "live_result": output_dir / "customer-operating-review.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-operating-review.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_operating_review": live_result["ready_for_customer_operating_review"],
    }


def _review_section(section_id: str, status: str, refs: list[Any]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "status": status,
        "evidence_refs": [str(ref) for ref in refs if ref],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized customer operating review supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample operating review validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Operating review requires evidence_mode=live and sanitized=true.")


def _check_closeout_handoff_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "closeout_handoff_result", "blocker", "closeout_handoff_result must be an object.")
        return
    ready = result.get("ready_for_customer_closeout_handoff") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "closeout_handoff_result", "pass", "Source closeout handoff is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "closeout_handoff_result", "warn", "Source closeout handoff validates shape but is not live.")
    else:
        _add_check(checks, "closeout_handoff_result", "blocker", "Source closeout handoff is not ready.")


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


def _check_review_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "review_sections", "blocker", "review_sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing = sorted(REQUIRED_REVIEW_SECTIONS - set(section_by_id))
    bad_statuses: list[str] = []
    bad_refs: list[str] = []
    empty_sections: list[str] = []
    for section_id, section in section_by_id.items():
        status = str(section.get("status", ""))
        if status not in HEALTHY_REVIEW_STATUSES:
            bad_statuses.append(section_id)
        refs = section.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            empty_sections.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing and not bad_statuses and not bad_refs and not empty_sections:
        _add_check(checks, "review_sections", "pass", "Operating review sections are complete and healthy.")
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
        _add_check(checks, "review_sections", "blocker", f"Operating review sections are invalid: {'; '.join(problems)}.")


def _check_review_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "review_controls", "blocker", "review_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_REVIEW_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "review_controls",
        "pass" if not missing else "blocker",
        "Operating review controls are explicit."
        if not missing
        else f"Operating review controls missing or false: {', '.join(missing)}.",
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
