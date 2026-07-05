from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_archive import (
    build_customer_lifecycle_archive_manifest,
    validate_customer_lifecycle_archive_manifest,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_STATUS_SCHEMA = "cavra.customer-lifecycle-public-status.packet.v1"
CUSTOMER_LIFECYCLE_STATUS_RESULT_SCHEMA = "cavra.customer-lifecycle-public-status.result.v1"

REQUIRED_STATUS_OWNER_REFS = {
    "customer_success_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
    "communications_owner_ref",
}

REQUIRED_STATUS_SECTIONS = {
    "deployment_status",
    "security_posture",
    "evidence_status",
    "operating_cadence",
    "renewal_outcome",
    "next_steps",
}

REQUIRED_PUBLICATION_CONTROLS = {
    "archive_manifest_ready",
    "customer_safe_language_approved",
    "no_private_evidence_embedded",
    "no_commercial_terms_embedded",
    "support_handoff_ready",
    "next_checkpoint_visible",
}

HEALTHY_STATUS_VALUES = {"ready", "active", "complete", "published", "scheduled"}

FORBIDDEN_PUBLIC_STATUS_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_name",
    "private_note",
    "pricing",
    "raw_contract",
    "raw_evidence",
    "renewal_amount",
}


def build_customer_lifecycle_status_packet(
    archive_manifest: dict[str, Any] | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    archive = archive_manifest or build_customer_lifecycle_archive_manifest(evidence_mode=evidence_mode)
    archive_result = validate_customer_lifecycle_archive_manifest(
        archive,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_STATUS_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "public_status_id": f"cavra-{evidence_mode}-customer-lifecycle-public-status",
        "customer_profile_ref": archive.get("customer_profile_ref", f"{prefix}://customer/redacted"),
        "archive_manifest_ref": f"{prefix}://customer-lifecycle-archive/manifest",
        "archive_manifest_result": archive_result,
        "status_owner_refs": {
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
            "communications_owner_ref": f"{prefix}://owner/customer-communications",
        },
        "public_status_sections": [
            _status_section(
                "deployment_status",
                "active",
                "CAVRA lifecycle controls are active and the customer lifecycle archive is complete.",
                [f"{prefix}://status/deployment", f"{prefix}://archive/executive-rollup"],
            ),
            _status_section(
                "security_posture",
                "ready",
                "Runtime authority, evidence, and AISPM posture controls are ready for ongoing review.",
                [f"{prefix}://status/security-posture", f"{prefix}://metrics/aispm-posture-trend"],
            ),
            _status_section(
                "evidence_status",
                "complete",
                "Sanitized evidence references are archived and verifier references are available.",
                [f"{prefix}://archive/evidence-room-index", f"{prefix}://verifier/customer-lifecycle-bundle"],
            ),
            _status_section(
                "operating_cadence",
                "scheduled",
                "Customer success and security review cadence is scheduled for the next lifecycle checkpoint.",
                [f"{prefix}://operating-review/next-cycle", f"{prefix}://success/next-quarter-plan"],
            ),
            _status_section(
                "renewal_outcome",
                "complete",
                "Renewal outcome and expansion activation references are closed out in the archive.",
                [f"{prefix}://renewal/executive-acceptance", f"{prefix}://expansion/activation-plan"],
            ),
            _status_section(
                "next_steps",
                "published",
                "Next success plan, support handoff, and archive verification paths are ready for the customer.",
                [f"{prefix}://support/customer-handoff", f"{prefix}://verifier/trust-root"],
            ),
        ],
        "support_refs": [
            f"{prefix}://support/customer-handoff",
            f"{prefix}://support/escalation-path",
            f"{prefix}://success/next-quarter-plan",
        ],
        "publication_controls": {
            "archive_manifest_ready": archive_result["blocker_count"] == 0,
            "customer_safe_language_approved": True,
            "no_private_evidence_embedded": True,
            "no_commercial_terms_embedded": True,
            "support_handoff_ready": True,
            "next_checkpoint_visible": True,
        },
    }


def validate_customer_lifecycle_status_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_STATUS_SCHEMA else "blocker",
        "Customer lifecycle public status schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_STATUS_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_STATUS_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_profile_ref"), checks, "customer_profile_ref")
    _check_safe_ref(packet.get("archive_manifest_ref"), checks, "archive_manifest_ref")
    _check_archive_result(packet.get("archive_manifest_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("status_owner_refs", {}), REQUIRED_STATUS_OWNER_REFS, checks, "status_owner_refs")
    _check_status_sections(packet.get("public_status_sections", []), checks)
    _check_ref_list(packet.get("support_refs", []), checks, "support_refs")
    _check_publication_controls(packet.get("publication_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_public_status_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Public status packet contains sanitized refs and customer-safe status text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_STATUS_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_public_status": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_status_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_lifecycle_status_packet(evidence_mode="sample")
    live = build_customer_lifecycle_status_packet(evidence_mode="live")
    sample_result = validate_customer_lifecycle_status_packet(sample)
    live_result = validate_customer_lifecycle_status_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-status.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-status.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-status.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-status.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-public-status.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_public_status": live_result["ready_for_customer_lifecycle_public_status"],
    }


def _status_section(section_id: str, status: str, summary: str, refs: list[str]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "status": status,
        "summary": summary,
        "evidence_refs": refs,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized lifecycle public status supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample lifecycle public status validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Public status requires evidence_mode=live and sanitized=true.")


def _check_archive_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "archive_manifest_result", "blocker", "archive_manifest_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_archive_manifest") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "archive_manifest_result", "pass", "Source lifecycle archive manifest is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "archive_manifest_result", "warn", "Source lifecycle archive validates shape but is not live.")
    else:
        _add_check(checks, "archive_manifest_result", "blocker", "Source lifecycle archive manifest is not ready.")


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


def _check_status_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "public_status_sections", "blocker", "public_status_sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing = sorted(REQUIRED_STATUS_SECTIONS - set(section_by_id))
    bad_statuses: list[str] = []
    bad_refs: list[str] = []
    bad_summaries: list[str] = []
    for section_id, section in section_by_id.items():
        if str(section.get("status", "")) not in HEALTHY_STATUS_VALUES:
            bad_statuses.append(section_id)
        summary = str(section.get("summary", "")).strip()
        if not summary or len(summary) < 20:
            bad_summaries.append(section_id)
        refs = section.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            bad_refs.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing and not bad_statuses and not bad_refs and not bad_summaries:
        _add_check(checks, "public_status_sections", "pass", "Public status sections are complete.")
    else:
        problems = []
        if missing:
            problems.append(f"missing sections: {', '.join(missing)}")
        if bad_statuses:
            problems.append(f"bad statuses: {', '.join(sorted(bad_statuses))}")
        if bad_summaries:
            problems.append(f"missing summaries: {', '.join(sorted(bad_summaries))}")
        if bad_refs:
            problems.append(f"unsafe or missing refs: {', '.join(sorted(bad_refs))}")
        _add_check(checks, "public_status_sections", "blocker", f"Public status sections invalid: {'; '.join(problems)}.")


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


def _check_publication_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "publication_controls", "blocker", "publication_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_PUBLICATION_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "publication_controls",
        "pass" if not missing else "blocker",
        "Public status publication controls are explicit."
        if not missing
        else f"Publication controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_public_status_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PUBLIC_STATUS_FIELDS:
                found.add(path)
            found.update(_find_forbidden_public_status_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_public_status_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
