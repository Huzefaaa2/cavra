from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_announcement import (
    build_customer_lifecycle_announcement_packet,
    validate_customer_lifecycle_announcement_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_RETROSPECTIVE_SCHEMA = "cavra.customer-lifecycle-retrospective.packet.v1"
CUSTOMER_LIFECYCLE_RETROSPECTIVE_RESULT_SCHEMA = "cavra.customer-lifecycle-retrospective.result.v1"

REQUIRED_RETROSPECTIVE_OWNER_REFS = {
    "program_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
    "product_owner_ref",
}

REQUIRED_RETROSPECTIVE_SECTIONS = {
    "what_worked",
    "operational_gaps",
    "customer_enablement",
    "security_posture",
    "support_readiness",
    "phase8_inputs",
}

REQUIRED_RETROSPECTIVE_CONTROLS = {
    "announcement_packet_ready",
    "internal_safe_language_approved",
    "follow_up_owner_refs_present",
    "phase8_inputs_triaged",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_RETROSPECTIVE_FIELDS = {
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
}


def build_customer_lifecycle_retrospective_packet(
    announcement_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    announcement = announcement_packet or build_customer_lifecycle_announcement_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    announcement_result = validate_customer_lifecycle_announcement_packet(
        announcement,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_RETROSPECTIVE_SCHEMA,
        "product": "CAVRA",
        "phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "retrospective_id": f"cavra-{evidence_mode}-customer-lifecycle-retrospective",
        "announcement_packet_ref": f"{prefix}://customer-lifecycle-announcement/r7",
        "announcement_packet_result": announcement_result,
        "retrospective_owner_refs": {
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "retrospective_sections": [
            _section(
                "what_worked",
                "R7 produced a complete customer lifecycle chain with live sanitized gates and evidence refs.",
                [f"{prefix}://customer-lifecycle-verification-index/r7"],
            ),
            _section(
                "operational_gaps",
                "Future cycles should continue improving live customer evidence collection and support handoff timing.",
                [f"{prefix}://operations/gap-register/r7"],
            ),
            _section(
                "customer_enablement",
                "Trial field guide, public status, support handoff, and operator guidance are ready for reuse.",
                [f"{prefix}://enablement/customer-lifecycle"],
            ),
            _section(
                "security_posture",
                "AISPM posture, evidence archive, and runtime control verification are represented in the closeout chain.",
                [f"{prefix}://security/customer-lifecycle-posture"],
            ),
            _section(
                "support_readiness",
                "Support and customer-success paths are linked to the final announcement and verification index.",
                [f"{prefix}://support/customer-handoff"],
            ),
            _section(
                "phase8_inputs",
                "Phase 8 should focus on production telemetry depth, customer-scale automation, and lifecycle analytics.",
                [f"{prefix}://roadmap/phase8-inputs"],
            ),
        ],
        "follow_up_actions": [
            _action(
                "phase8-telemetry-depth",
                "Expand customer-safe telemetry depth for lifecycle operations.",
                f"{prefix}://owner/security-platform",
                f"{prefix}://roadmap/phase8-telemetry-depth",
            ),
            _action(
                "phase8-support-automation",
                "Automate support and customer-success checkpoint evidence capture.",
                f"{prefix}://owner/support",
                f"{prefix}://roadmap/phase8-support-automation",
            ),
            _action(
                "phase8-analytics",
                "Add lifecycle analytics that summarize posture, adoption, and operating cadence.",
                f"{prefix}://owner/product-management",
                f"{prefix}://roadmap/phase8-analytics",
            ),
        ],
        "phase8_input_refs": [
            f"{prefix}://roadmap/phase8-telemetry-depth",
            f"{prefix}://roadmap/phase8-support-automation",
            f"{prefix}://roadmap/phase8-analytics",
        ],
        "retrospective_controls": {
            "announcement_packet_ready": announcement_result["blocker_count"] == 0,
            "internal_safe_language_approved": True,
            "follow_up_owner_refs_present": True,
            "phase8_inputs_triaged": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_retrospective_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_RETROSPECTIVE_SCHEMA else "blocker",
        "Customer lifecycle retrospective schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_RETROSPECTIVE_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_RETROSPECTIVE_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("announcement_packet_ref"), checks, "announcement_packet_ref")
    _check_announcement_result(packet.get("announcement_packet_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("retrospective_owner_refs", {}),
        REQUIRED_RETROSPECTIVE_OWNER_REFS,
        checks,
        "retrospective_owner_refs",
    )
    _check_sections(packet.get("retrospective_sections", []), checks)
    _check_actions(packet.get("follow_up_actions", []), checks)
    _check_ref_list(packet.get("phase8_input_refs", []), checks, "phase8_input_refs")
    _check_controls(packet.get("retrospective_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_retrospective_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Retrospective packet contains sanitized refs and internal-safe lessons only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_RETROSPECTIVE_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_retrospective": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_retrospective_artifacts(output_dir: Path, repo_root: Path | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_retrospective_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_retrospective_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_retrospective_packet(sample)
    live_result = validate_customer_lifecycle_retrospective_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-retrospective.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-retrospective.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-retrospective.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-retrospective.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-retrospective.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_retrospective": live_result["ready_for_customer_lifecycle_retrospective"],
    }


def _section(section_id: str, summary: str, refs: list[str]) -> dict[str, Any]:
    return {"section_id": section_id, "summary": summary, "supporting_refs": refs}


def _action(action_id: str, summary: str, owner_ref: str, tracking_ref: str) -> dict[str, str]:
    return {
        "action_id": action_id,
        "summary": summary,
        "owner_ref": owner_ref,
        "tracking_ref": tracking_ref,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized customer lifecycle retrospective supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample customer lifecycle retrospective validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Retrospective requires evidence_mode=live and sanitized=true.")


def _check_announcement_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "announcement_packet_result", "blocker", "announcement_packet_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_announcement_packet") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "announcement_packet_result", "pass", "Source announcement packet is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "announcement_packet_result", "warn", "Source announcement validates shape but is not live.")
    else:
        _add_check(checks, "announcement_packet_result", "blocker", "Source announcement packet is not ready.")


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


def _check_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "retrospective_sections", "blocker", "retrospective_sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing = sorted(REQUIRED_RETROSPECTIVE_SECTIONS - set(section_by_id))
    bad_summary: list[str] = []
    bad_refs: list[str] = []
    for section_id, section in section_by_id.items():
        if len(str(section.get("summary", "")).strip()) < 40:
            bad_summary.append(section_id)
        refs = section.get("supporting_refs", [])
        if not isinstance(refs, list) or not refs:
            bad_refs.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing and not bad_summary and not bad_refs:
        _add_check(checks, "retrospective_sections", "pass", "Retrospective sections are complete.")
    else:
        problems = []
        if missing:
            problems.append(f"missing sections: {', '.join(missing)}")
        if bad_summary:
            problems.append(f"short summaries: {', '.join(sorted(bad_summary))}")
        if bad_refs:
            problems.append(f"unsafe or missing refs: {', '.join(sorted(bad_refs))}")
        _add_check(checks, "retrospective_sections", "blocker", f"Retrospective sections invalid: {'; '.join(problems)}.")


def _check_actions(actions: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(actions, list) or len(actions) < 3:
        _add_check(checks, "follow_up_actions", "blocker", "At least three follow-up actions are required.")
        return
    bad: list[str] = []
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            bad.append(str(index))
            continue
        if not str(action.get("action_id", "")).strip():
            bad.append(f"{index}:action_id")
        if len(str(action.get("summary", "")).strip()) < 30:
            bad.append(f"{index}:summary")
        if not _is_safe_ref(action.get("owner_ref")):
            bad.append(f"{index}:owner_ref")
        if not _is_safe_ref(action.get("tracking_ref")):
            bad.append(f"{index}:tracking_ref")
    _add_check(
        checks,
        "follow_up_actions",
        "pass" if not bad else "blocker",
        "Follow-up actions are owner-assigned and sanitized."
        if not bad
        else f"Follow-up actions invalid: {', '.join(bad)}.",
    )


def _check_ref_list(refs: Any, checks: list[dict[str, str]], name: str) -> None:
    if not isinstance(refs, list) or not refs:
        _add_check(checks, name, "blocker", f"{name} must be a non-empty list.")
        return
    unsafe = [str(index) for index, ref in enumerate(refs) if not _is_safe_ref(ref)]
    _add_check(
        checks,
        name,
        "pass" if not unsafe else "blocker",
        f"{name} are present and sanitized." if not unsafe else f"{name} contain unsafe refs: {', '.join(unsafe)}.",
    )


def _check_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "retrospective_controls", "blocker", "retrospective_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_RETROSPECTIVE_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "retrospective_controls",
        "pass" if not missing else "blocker",
        "Retrospective controls are explicit."
        if not missing
        else f"Retrospective controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_retrospective_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_RETROSPECTIVE_FIELDS:
                found.add(path)
            found.update(_find_forbidden_retrospective_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_retrospective_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
