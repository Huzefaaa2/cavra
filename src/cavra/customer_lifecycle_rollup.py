from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_closeout_handoff import (
    build_customer_closeout_handoff_packet,
    validate_customer_closeout_handoff_packet,
)
from cavra.customer_evidence_room import (
    build_customer_evidence_room_index,
    validate_customer_evidence_room_index,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    build_customer_live_evidence_template,
    find_forbidden_live_evidence_fields,
    validate_customer_live_evidence_packet,
)
from cavra.customer_operating_review import (
    build_customer_operating_review_packet,
    validate_customer_operating_review_packet,
)
from cavra.customer_renewal_expansion import (
    build_customer_renewal_expansion_packet,
    validate_customer_renewal_expansion_packet,
)
from cavra.customer_renewal_outcome import (
    build_customer_renewal_outcome_packet,
    validate_customer_renewal_outcome_packet,
)


CUSTOMER_LIFECYCLE_ROLLUP_SCHEMA = "cavra.customer-lifecycle-executive-rollup.packet.v1"
CUSTOMER_LIFECYCLE_ROLLUP_RESULT_SCHEMA = "cavra.customer-lifecycle-executive-rollup.result.v1"

REQUIRED_LIFECYCLE_GATES: dict[str, dict[str, Any]] = {
    "R7.1": {
        "title": "Customer live evidence intake",
        "packet_ref": "customer-live-evidence",
        "ready_key": "ready_for_customer_live_evidence_intake",
    },
    "R7.2": {
        "title": "Customer evidence room closeout",
        "packet_ref": "customer-evidence-room",
        "ready_key": "ready_for_customer_evidence_room_closeout",
    },
    "R7.3": {
        "title": "Customer closeout handoff",
        "packet_ref": "customer-closeout-handoff",
        "ready_key": "ready_for_customer_closeout_handoff",
    },
    "R7.4": {
        "title": "Customer operating review",
        "packet_ref": "customer-operating-review",
        "ready_key": "ready_for_customer_operating_review",
    },
    "R7.5": {
        "title": "Customer renewal and expansion readiness",
        "packet_ref": "customer-renewal-expansion",
        "ready_key": "ready_for_customer_renewal_expansion",
    },
    "R7.6": {
        "title": "Customer renewal outcome closeout",
        "packet_ref": "customer-renewal-outcome",
        "ready_key": "ready_for_customer_renewal_outcome_closeout",
    },
}

REQUIRED_EXECUTIVE_SUMMARY_SECTIONS = {
    "implementation_closeout",
    "operating_health",
    "value_realization",
    "risk_and_security",
    "renewal_outcome",
    "expansion_plan",
    "next_lifecycle_checkpoint",
}

REQUIRED_ROLLUP_CONTROLS = {
    "all_lifecycle_gates_ready",
    "executive_summary_complete",
    "customer_identifiers_excluded",
    "commercial_terms_excluded",
    "private_notes_excluded",
    "archive_refs_present",
    "next_checkpoint_scheduled",
}

HEALTHY_ROLLUP_STATUSES = {"ready", "complete", "confirmed", "scheduled"}

FORBIDDEN_LIFECYCLE_ROLLUP_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_name",
    "private_note",
    "pricing",
    "raw_contract",
    "renewal_amount",
}


def build_customer_lifecycle_rollup_packet(
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    chain = _build_lifecycle_chain(evidence_mode=evidence_mode)
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_ROLLUP_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "rollup_id": f"cavra-{evidence_mode}-customer-lifecycle-executive-rollup",
        "customer_profile_ref": chain["customer_live_evidence"].get(
            "customer_profile_ref",
            f"{prefix}://customer/redacted",
        ),
        "executive_owner_refs": {
            "executive_sponsor_ref": f"{prefix}://owner/executive-sponsor",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "commercial_owner_ref": f"{prefix}://owner/commercial",
            "operations_owner_ref": f"{prefix}://owner/platform-operations",
        },
        "lifecycle_gates": [
            _lifecycle_gate(
                gate_id,
                title=str(config["title"]),
                packet_ref=f"{prefix}://{config['packet_ref']}/packet",
                readiness_result=chain["results"][gate_id],
                ready_key=str(config["ready_key"]),
            )
            for gate_id, config in REQUIRED_LIFECYCLE_GATES.items()
        ],
        "executive_summary_sections": [
            _summary_section(
                "implementation_closeout",
                "complete",
                [f"{prefix}://customer-closeout-handoff/packet", f"{prefix}://evidence-room/closeout-index"],
            ),
            _summary_section(
                "operating_health",
                "confirmed",
                [f"{prefix}://customer-operating-review/packet", f"{prefix}://metrics/support-sla-health"],
            ),
            _summary_section(
                "value_realization",
                "confirmed",
                [f"{prefix}://metrics/value-realization", f"{prefix}://metrics/aispm-posture-trend"],
            ),
            _summary_section(
                "risk_and_security",
                "ready",
                [f"{prefix}://security/risk-closeout", f"{prefix}://audit/security-acceptance"],
            ),
            _summary_section(
                "renewal_outcome",
                "complete",
                [f"{prefix}://customer-renewal-outcome/packet", f"{prefix}://renewal/executive-acceptance"],
            ),
            _summary_section(
                "expansion_plan",
                "ready",
                [f"{prefix}://expansion/approved-scope", f"{prefix}://expansion/activation-plan"],
            ),
            _summary_section(
                "next_lifecycle_checkpoint",
                "scheduled",
                [f"{prefix}://success/next-quarter-plan", f"{prefix}://operating-review/next-cycle"],
            ),
        ],
        "rollup_controls": {
            "all_lifecycle_gates_ready": all(
                chain["results"][gate_id].get(str(config["ready_key"])) is True
                and chain["results"][gate_id].get("blocker_count") == 0
                for gate_id, config in REQUIRED_LIFECYCLE_GATES.items()
            ),
            "executive_summary_complete": True,
            "customer_identifiers_excluded": True,
            "commercial_terms_excluded": True,
            "private_notes_excluded": True,
            "archive_refs_present": True,
            "next_checkpoint_scheduled": True,
        },
    }


def validate_customer_lifecycle_rollup_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_ROLLUP_SCHEMA else "blocker",
        "Customer lifecycle executive rollup schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_ROLLUP_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_ROLLUP_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_profile_ref"), checks, "customer_profile_ref")
    _check_owner_refs(packet.get("executive_owner_refs", {}), checks)
    _check_lifecycle_gates(packet.get("lifecycle_gates", []), checks, require_live=require_live)
    _check_summary_sections(packet.get("executive_summary_sections", []), checks)
    _check_rollup_controls(packet.get("rollup_controls", {}), checks, require_live=require_live)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_lifecycle_rollup_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Lifecycle rollup contains sanitized refs and executive-safe control metadata only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_ROLLUP_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_executive_rollup": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_rollup_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_lifecycle_rollup_packet(evidence_mode="sample")
    live = build_customer_lifecycle_rollup_packet(evidence_mode="live")
    sample_result = validate_customer_lifecycle_rollup_packet(sample)
    live_result = validate_customer_lifecycle_rollup_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-rollup.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-rollup.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-rollup.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-rollup.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-executive-rollup.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_executive_rollup": live_result[
            "ready_for_customer_lifecycle_executive_rollup"
        ],
    }


def _build_lifecycle_chain(*, evidence_mode: str) -> dict[str, Any]:
    live_evidence = build_customer_live_evidence_template(evidence_mode=evidence_mode)
    evidence_room = build_customer_evidence_room_index(live_evidence, evidence_mode=evidence_mode)
    handoff = build_customer_closeout_handoff_packet(evidence_room, evidence_mode=evidence_mode)
    review = build_customer_operating_review_packet(handoff, evidence_mode=evidence_mode)
    renewal = build_customer_renewal_expansion_packet(review, evidence_mode=evidence_mode)
    outcome = build_customer_renewal_outcome_packet(renewal, evidence_mode=evidence_mode)
    require_live = evidence_mode == "live"
    results = {
        "R7.1": validate_customer_live_evidence_packet(live_evidence, require_live=require_live),
        "R7.2": validate_customer_evidence_room_index(evidence_room, require_live=require_live),
        "R7.3": validate_customer_closeout_handoff_packet(handoff, require_live=require_live),
        "R7.4": validate_customer_operating_review_packet(review, require_live=require_live),
        "R7.5": validate_customer_renewal_expansion_packet(renewal, require_live=require_live),
        "R7.6": validate_customer_renewal_outcome_packet(outcome, require_live=require_live),
    }
    return {
        "customer_live_evidence": live_evidence,
        "customer_evidence_room": evidence_room,
        "customer_closeout_handoff": handoff,
        "customer_operating_review": review,
        "customer_renewal_expansion": renewal,
        "customer_renewal_outcome": outcome,
        "results": results,
    }


def _lifecycle_gate(
    gate_id: str,
    *,
    title: str,
    packet_ref: str,
    readiness_result: dict[str, Any],
    ready_key: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "title": title,
        "packet_ref": packet_ref,
        "ready_key": ready_key,
        "ready": readiness_result.get(ready_key) is True and readiness_result.get("blocker_count") == 0,
        "readiness_result": readiness_result,
    }


def _summary_section(section_id: str, status: str, refs: list[str]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "status": status,
        "evidence_refs": refs,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized lifecycle rollup packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample lifecycle rollup validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Lifecycle rollup requires evidence_mode=live and sanitized=true.")


def _check_owner_refs(payload: Any, checks: list[dict[str, str]]) -> None:
    required = {
        "executive_sponsor_ref",
        "customer_success_owner_ref",
        "security_owner_ref",
        "commercial_owner_ref",
        "operations_owner_ref",
    }
    if not isinstance(payload, dict):
        _add_check(checks, "executive_owner_refs", "blocker", "executive_owner_refs must be an object.")
        return
    missing = sorted(field for field in required if not payload.get(field))
    unsafe = sorted(field for field, value in payload.items() if value and not _is_safe_ref(value))
    if not missing and not unsafe:
        _add_check(checks, "executive_owner_refs", "pass", "Executive owner refs are present and sanitized.")
    else:
        problems = []
        if missing:
            problems.append(f"missing refs: {', '.join(missing)}")
        if unsafe:
            problems.append(f"unsafe refs: {', '.join(unsafe)}")
        _add_check(checks, "executive_owner_refs", "blocker", f"Executive owner refs invalid: {'; '.join(problems)}.")


def _check_lifecycle_gates(gates: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(gates, list):
        _add_check(checks, "lifecycle_gates", "blocker", "lifecycle_gates must be a list.")
        return
    gate_by_id = {str(gate.get("gate_id")): gate for gate in gates if isinstance(gate, dict)}
    missing = sorted(set(REQUIRED_LIFECYCLE_GATES) - set(gate_by_id))
    blockers: list[str] = []
    warnings: list[str] = []
    unsafe_refs: list[str] = []
    for gate_id, config in REQUIRED_LIFECYCLE_GATES.items():
        gate = gate_by_id.get(gate_id)
        if not gate:
            continue
        if not _is_safe_ref(gate.get("packet_ref")):
            unsafe_refs.append(gate_id)
        result = gate.get("readiness_result", {})
        ready_key = str(config["ready_key"])
        if not isinstance(result, dict) or result.get("blocker_count") != 0:
            blockers.append(gate_id)
        elif result.get(ready_key) is not True and not require_live:
            warnings.append(gate_id)
        elif result.get(ready_key) is not True:
            blockers.append(gate_id)
        elif require_live and result.get("warning_count") != 0:
            warnings.append(gate_id)
    if not missing and not blockers and not warnings and not unsafe_refs:
        _add_check(checks, "lifecycle_gates", "pass", "All customer lifecycle gates are ready.")
    elif not missing and not blockers and warnings and not unsafe_refs and not require_live:
        _add_check(
            checks,
            "lifecycle_gates",
            "warn",
            f"Customer lifecycle gates validate shape but are not live: {', '.join(warnings)}.",
        )
    else:
        problems = []
        if missing:
            problems.append(f"missing gates: {', '.join(missing)}")
        if blockers:
            problems.append(f"blocked gates: {', '.join(blockers)}")
        if warnings:
            problems.append(f"warning gates: {', '.join(warnings)}")
        if unsafe_refs:
            problems.append(f"unsafe packet refs: {', '.join(unsafe_refs)}")
        _add_check(checks, "lifecycle_gates", "blocker", f"Customer lifecycle gates invalid: {'; '.join(problems)}.")


def _check_summary_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "executive_summary_sections", "blocker", "executive_summary_sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing = sorted(REQUIRED_EXECUTIVE_SUMMARY_SECTIONS - set(section_by_id))
    bad_statuses: list[str] = []
    bad_refs: list[str] = []
    empty_sections: list[str] = []
    for section_id, section in section_by_id.items():
        if str(section.get("status", "")) not in HEALTHY_ROLLUP_STATUSES:
            bad_statuses.append(section_id)
        refs = section.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            empty_sections.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing and not bad_statuses and not bad_refs and not empty_sections:
        _add_check(checks, "executive_summary_sections", "pass", "Executive summary sections are complete.")
    else:
        problems = []
        if missing:
            problems.append(f"missing sections: {', '.join(missing)}")
        if bad_statuses:
            problems.append(f"bad statuses: {', '.join(sorted(bad_statuses))}")
        if empty_sections:
            problems.append(f"empty sections: {', '.join(sorted(empty_sections))}")
        if bad_refs:
            problems.append(f"unsafe refs: {', '.join(sorted(bad_refs))}")
        _add_check(checks, "executive_summary_sections", "blocker", f"Executive summary invalid: {'; '.join(problems)}.")


def _check_rollup_controls(controls: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "rollup_controls", "blocker", "rollup_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_ROLLUP_CONTROLS if controls.get(control) is not True)
    if missing == ["all_lifecycle_gates_ready"] and not require_live:
        _add_check(
            checks,
            "rollup_controls",
            "warn",
            "Lifecycle rollup controls validate shape but lifecycle gates are not live.",
        )
        return
    _add_check(
        checks,
        "rollup_controls",
        "pass" if not missing else "blocker",
        "Lifecycle rollup controls are explicit."
        if not missing
        else f"Lifecycle rollup controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_lifecycle_rollup_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_LIFECYCLE_ROLLUP_FIELDS:
                found.add(path)
            found.update(_find_forbidden_lifecycle_rollup_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_lifecycle_rollup_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
