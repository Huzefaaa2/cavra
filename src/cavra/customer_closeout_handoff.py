from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_evidence_room import (
    build_customer_evidence_room_index,
    validate_customer_evidence_room_index,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_CLOSEOUT_HANDOFF_SCHEMA = "cavra.customer-closeout-handoff.packet.v1"
CUSTOMER_CLOSEOUT_HANDOFF_RESULT_SCHEMA = "cavra.customer-closeout-handoff.result.v1"

REQUIRED_HANDOFF_OWNER_REFS = {
    "release_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "approver_ref",
}

REQUIRED_COMMUNICATION_REFS = {
    "announcement_ref",
    "evidence_room_ref",
    "handoff_ticket_ref",
    "support_path_ref",
}

REQUIRED_OPERATING_REVIEW_REFS = {
    "next_review_ref",
    "cadence_ref",
    "success_metrics_ref",
    "renewal_checkpoint_ref",
}

REQUIRED_HANDOFF_CONTROLS = {
    "evidence_room_ready",
    "release_owner_assigned",
    "customer_success_owner_assigned",
    "security_owner_assigned",
    "support_path_defined",
    "customer_ack_required",
    "operating_review_scheduled",
    "rollback_contact_defined",
}


def build_customer_closeout_handoff_packet(
    evidence_room_index: dict[str, Any] | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    evidence_room = evidence_room_index or build_customer_evidence_room_index(evidence_mode=evidence_mode)
    evidence_room_result = validate_customer_evidence_room_index(
        evidence_room,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_CLOSEOUT_HANDOFF_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "closeout_id": f"cavra-{evidence_mode}-customer-closeout-handoff",
        "customer_profile_ref": evidence_room.get("customer_profile_ref", f"{prefix}://customer/redacted"),
        "evidence_room_index_ref": f"{prefix}://customer-evidence-room/index",
        "evidence_room_result": evidence_room_result,
        "handoff_owner_refs": {
            "release_owner_ref": f"{prefix}://owner/release-authority",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "approver_ref": f"{prefix}://approver/cavra-release-authority",
        },
        "communication_refs": {
            "announcement_ref": f"{prefix}://announcement/customer-closeout",
            "evidence_room_ref": evidence_room.get("source_intake_packet_ref", f"{prefix}://evidence-room/cavra-closeout"),
            "handoff_ticket_ref": "ticket://customer-closeout/handoff",
            "support_path_ref": "runbook://support/managed-enterprise-escalation",
        },
        "operating_review": {
            "next_review_ref": f"{prefix}://operating-review/next",
            "cadence_ref": "runbook://operating-review/monthly-cadence",
            "success_metrics_ref": f"{prefix}://metrics/customer-success-slo",
            "renewal_checkpoint_ref": f"{prefix}://commercial/renewal-checkpoint",
        },
        "known_exclusions": [
            {
                "exclusion_id": "none-open",
                "reason_ref": f"{prefix}://exclusion/none-open",
                "owner_ref": f"{prefix}://owner/release-authority",
                "risk_acceptance_ref": f"{prefix}://risk-acceptance/not-required",
            }
        ],
        "handoff_controls": {
            "evidence_room_ready": evidence_room_result["blocker_count"] == 0,
            "release_owner_assigned": True,
            "customer_success_owner_assigned": True,
            "security_owner_assigned": True,
            "support_path_defined": True,
            "customer_ack_required": True,
            "operating_review_scheduled": True,
            "rollback_contact_defined": True,
        },
    }


def validate_customer_closeout_handoff_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_CLOSEOUT_HANDOFF_SCHEMA else "blocker",
        "Customer closeout handoff schema is valid."
        if packet.get("schema_version") == CUSTOMER_CLOSEOUT_HANDOFF_SCHEMA
        else f"Packet must use {CUSTOMER_CLOSEOUT_HANDOFF_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_profile_ref"), checks, "customer_profile_ref")
    _check_safe_ref(packet.get("evidence_room_index_ref"), checks, "evidence_room_index_ref")
    _check_evidence_room_result(packet.get("evidence_room_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("handoff_owner_refs", {}), REQUIRED_HANDOFF_OWNER_REFS, checks, "handoff_owner_refs")
    _check_required_refs(packet.get("communication_refs", {}), REQUIRED_COMMUNICATION_REFS, checks, "communication_refs")
    _check_required_refs(packet.get("operating_review", {}), REQUIRED_OPERATING_REVIEW_REFS, checks, "operating_review")
    _check_known_exclusions(packet.get("known_exclusions", []), checks)
    _check_handoff_controls(packet.get("handoff_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Closeout handoff contains sanitized refs and control metadata only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_CLOSEOUT_HANDOFF_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_closeout_handoff": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_closeout_handoff_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_closeout_handoff_packet(evidence_mode="sample")
    live = build_customer_closeout_handoff_packet(evidence_mode="live")
    sample_result = validate_customer_closeout_handoff_packet(sample)
    live_result = validate_customer_closeout_handoff_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-closeout-handoff.sample.json",
        "live_sanitized_example": output_dir / "customer-closeout-handoff.live.sanitized.example.json",
        "sample_result": output_dir / "customer-closeout-handoff.sample.result.json",
        "live_result": output_dir / "customer-closeout-handoff.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-closeout-handoff.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_closeout_handoff": live_result["ready_for_customer_closeout_handoff"],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized customer closeout handoff supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample closeout handoff validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Closeout handoff requires evidence_mode=live and sanitized=true.")


def _check_evidence_room_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "evidence_room_result", "blocker", "evidence_room_result must be an object.")
        return
    ready = result.get("ready_for_customer_evidence_room_closeout") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "evidence_room_result", "pass", "Source evidence-room closeout is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "evidence_room_result", "warn", "Source evidence-room validates shape but is not live.")
    else:
        _add_check(checks, "evidence_room_result", "blocker", "Source evidence-room closeout is not ready.")


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


def _check_known_exclusions(exclusions: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(exclusions, list) or not exclusions:
        _add_check(checks, "known_exclusions", "blocker", "known_exclusions must be a non-empty list.")
        return
    unsafe: list[str] = []
    for index, exclusion in enumerate(exclusions):
        if not isinstance(exclusion, dict):
            unsafe.append(f"{index}:not-object")
            continue
        for field in ("reason_ref", "owner_ref", "risk_acceptance_ref"):
            if not _is_safe_ref(exclusion.get(field)):
                unsafe.append(f"{index}:{field}")
    _add_check(
        checks,
        "known_exclusions",
        "pass" if not unsafe else "blocker",
        "Known exclusions are explicit and sanitized."
        if not unsafe
        else f"Known exclusions contain missing or unsafe refs: {', '.join(unsafe)}.",
    )


def _check_handoff_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "handoff_controls", "blocker", "handoff_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_HANDOFF_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "handoff_controls",
        "pass" if not missing else "blocker",
        "Closeout handoff controls are explicit."
        if not missing
        else f"Handoff controls missing or false: {', '.join(missing)}.",
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
