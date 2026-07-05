from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_verification_index import (
    build_customer_lifecycle_verification_index,
    validate_customer_lifecycle_verification_index,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_ANNOUNCEMENT_SCHEMA = "cavra.customer-lifecycle-announcement.packet.v1"
CUSTOMER_LIFECYCLE_ANNOUNCEMENT_RESULT_SCHEMA = "cavra.customer-lifecycle-announcement.result.v1"

REQUIRED_ANNOUNCEMENT_OWNER_REFS = {
    "release_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
    "communications_owner_ref",
}

REQUIRED_ANNOUNCEMENT_SECTIONS = {
    "headline",
    "customer_safe_summary",
    "what_is_ready",
    "evidence_and_trust",
    "support_and_next_steps",
    "operator_handoff",
}

REQUIRED_ANNOUNCEMENT_CONTROLS = {
    "verification_index_ready",
    "release_notes_approved",
    "customer_safe_language_approved",
    "support_path_verified",
    "operator_handoff_ready",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_ANNOUNCEMENT_FIELDS = {
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


def build_customer_lifecycle_announcement_packet(
    verification_index: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    index = verification_index or build_customer_lifecycle_verification_index(root, evidence_mode=evidence_mode)
    index_result = validate_customer_lifecycle_verification_index(
        index,
        repo_root=root,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_ANNOUNCEMENT_SCHEMA,
        "product": "CAVRA",
        "phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "announcement_id": f"cavra-{evidence_mode}-customer-lifecycle-closeout-announcement",
        "verification_index_ref": f"{prefix}://customer-lifecycle-verification-index/r7",
        "verification_index_result": index_result,
        "announcement_owner_refs": {
            "release_owner_ref": f"{prefix}://owner/release-management",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
            "communications_owner_ref": f"{prefix}://owner/customer-communications",
        },
        "announcement_sections": [
            _section(
                "headline",
                "CAVRA customer lifecycle closeout is ready for customer-safe release.",
                [f"{prefix}://release-notes/customer-lifecycle-closeout"],
            ),
            _section(
                "customer_safe_summary",
                "Runtime authority, evidence, AISPM posture, archive, and support handoff are verified.",
                [f"{prefix}://customer-lifecycle-verification-index/r7"],
            ),
            _section(
                "what_is_ready",
                "All R7 customer lifecycle gates have ready live sanitized examples and validation evidence.",
                [f"{prefix}://customer-lifecycle-final-seal/release"],
            ),
            _section(
                "evidence_and_trust",
                "Customer-safe evidence refs, verification index, and archive refs are ready for operator review.",
                [f"{prefix}://archive/customer-lifecycle", f"{prefix}://verifier/customer-lifecycle"],
            ),
            _section(
                "support_and_next_steps",
                "Support path, next checkpoint, and customer-success handoff references are ready.",
                [f"{prefix}://support/customer-handoff", f"{prefix}://success/next-quarter-plan"],
            ),
            _section(
                "operator_handoff",
                "Operators can use the release notes, verification index, and support refs for final closeout.",
                [f"{prefix}://operator/customer-lifecycle-handoff"],
            ),
        ],
        "release_note_refs": [
            f"{prefix}://release-notes/customer-lifecycle-closeout",
            f"{prefix}://public-status/customer-lifecycle",
        ],
        "operator_handoff_refs": [
            f"{prefix}://operator/customer-lifecycle-handoff",
            f"{prefix}://support/customer-handoff",
            f"{prefix}://success/next-quarter-plan",
        ],
        "announcement_controls": {
            "verification_index_ready": index_result["blocker_count"] == 0,
            "release_notes_approved": True,
            "customer_safe_language_approved": True,
            "support_path_verified": True,
            "operator_handoff_ready": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_announcement_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_ANNOUNCEMENT_SCHEMA else "blocker",
        "Customer lifecycle announcement schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_ANNOUNCEMENT_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_ANNOUNCEMENT_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("verification_index_ref"), checks, "verification_index_ref")
    _check_verification_index_result(packet.get("verification_index_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("announcement_owner_refs", {}),
        REQUIRED_ANNOUNCEMENT_OWNER_REFS,
        checks,
        "announcement_owner_refs",
    )
    _check_announcement_sections(packet.get("announcement_sections", []), checks)
    _check_ref_list(packet.get("release_note_refs", []), checks, "release_note_refs")
    _check_ref_list(packet.get("operator_handoff_refs", []), checks, "operator_handoff_refs")
    _check_announcement_controls(packet.get("announcement_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_announcement_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Announcement packet contains customer-safe copy and sanitized refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_ANNOUNCEMENT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_announcement_packet": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_announcement_artifacts(output_dir: Path, repo_root: Path | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_announcement_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_announcement_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_announcement_packet(sample)
    live_result = validate_customer_lifecycle_announcement_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-announcement.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-announcement.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-announcement.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-announcement.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-announcement.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_announcement_packet": live_result[
            "ready_for_customer_lifecycle_announcement_packet"
        ],
    }


def _section(section_id: str, copy: str, refs: list[str]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "copy": copy,
        "supporting_refs": refs,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized customer lifecycle announcement supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample customer lifecycle announcement validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Announcement requires evidence_mode=live and sanitized=true.")


def _check_verification_index_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "verification_index_result", "blocker", "verification_index_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_verification_index") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "verification_index_result", "pass", "Source lifecycle verification index is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "verification_index_result", "warn", "Source verification index validates shape but is not live.")
    else:
        _add_check(checks, "verification_index_result", "blocker", "Source lifecycle verification index is not ready.")


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


def _check_announcement_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "announcement_sections", "blocker", "announcement_sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing = sorted(REQUIRED_ANNOUNCEMENT_SECTIONS - set(section_by_id))
    bad_copy: list[str] = []
    bad_refs: list[str] = []
    for section_id, section in section_by_id.items():
        copy = str(section.get("copy", "")).strip()
        if len(copy) < 30:
            bad_copy.append(section_id)
        refs = section.get("supporting_refs", [])
        if not isinstance(refs, list) or not refs:
            bad_refs.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing and not bad_copy and not bad_refs:
        _add_check(checks, "announcement_sections", "pass", "Announcement sections are complete and supported.")
    else:
        problems = []
        if missing:
            problems.append(f"missing sections: {', '.join(missing)}")
        if bad_copy:
            problems.append(f"short copy: {', '.join(sorted(bad_copy))}")
        if bad_refs:
            problems.append(f"unsafe or missing refs: {', '.join(sorted(bad_refs))}")
        _add_check(checks, "announcement_sections", "blocker", f"Announcement sections invalid: {'; '.join(problems)}.")


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


def _check_announcement_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "announcement_controls", "blocker", "announcement_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_ANNOUNCEMENT_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "announcement_controls",
        "pass" if not missing else "blocker",
        "Announcement controls are explicit."
        if not missing
        else f"Announcement controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_announcement_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_ANNOUNCEMENT_FIELDS:
                found.add(path)
            found.update(_find_forbidden_announcement_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_announcement_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
