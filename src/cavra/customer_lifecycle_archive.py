from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_rollup import (
    build_customer_lifecycle_rollup_packet,
    validate_customer_lifecycle_rollup_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_ARCHIVE_SCHEMA = "cavra.customer-lifecycle-archive-manifest.packet.v1"
CUSTOMER_LIFECYCLE_ARCHIVE_RESULT_SCHEMA = "cavra.customer-lifecycle-archive-manifest.result.v1"

REQUIRED_ARCHIVE_OWNER_REFS = {
    "archive_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "compliance_owner_ref",
    "operations_owner_ref",
}

REQUIRED_ARCHIVE_SECTIONS = {
    "executive_rollup",
    "evidence_room",
    "audit_manifest",
    "retention_policy",
    "verifier_bundle",
    "handoff_record",
}

REQUIRED_RETENTION_CONTROLS = {
    "retention_policy_ref",
    "legal_hold_policy_ref",
    "immutability_policy_ref",
    "deletion_review_policy_ref",
}

REQUIRED_ARCHIVE_CONTROLS = {
    "lifecycle_rollup_ready",
    "archive_sections_complete",
    "retention_controls_present",
    "verifier_refs_present",
    "audit_handoff_ready",
    "customer_identifiers_excluded",
    "commercial_terms_excluded",
    "private_notes_excluded",
}

HEALTHY_ARCHIVE_STATUSES = {"archived", "ready", "retained", "verified", "handed_off"}

FORBIDDEN_LIFECYCLE_ARCHIVE_FIELDS = {
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


def build_customer_lifecycle_archive_manifest(
    lifecycle_rollup_packet: dict[str, Any] | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    rollup = lifecycle_rollup_packet or build_customer_lifecycle_rollup_packet(evidence_mode=evidence_mode)
    rollup_result = validate_customer_lifecycle_rollup_packet(
        rollup,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_ARCHIVE_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "archive_manifest_id": f"cavra-{evidence_mode}-customer-lifecycle-archive-manifest",
        "customer_profile_ref": rollup.get("customer_profile_ref", f"{prefix}://customer/redacted"),
        "lifecycle_rollup_ref": f"{prefix}://customer-lifecycle-rollup/packet",
        "lifecycle_rollup_result": rollup_result,
        "archive_owner_refs": {
            "archive_owner_ref": f"{prefix}://owner/archive",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "compliance_owner_ref": f"{prefix}://owner/compliance",
            "operations_owner_ref": f"{prefix}://owner/platform-operations",
        },
        "archive_sections": [
            _archive_section(
                "executive_rollup",
                "archived",
                [f"{prefix}://archive/executive-rollup", f"{prefix}://customer-lifecycle-rollup/result"],
            ),
            _archive_section(
                "evidence_room",
                "archived",
                [f"{prefix}://archive/evidence-room-index", f"{prefix}://evidence-room/manifest"],
            ),
            _archive_section(
                "audit_manifest",
                "ready",
                [f"{prefix}://audit/lifecycle-archive-manifest", f"{prefix}://audit/hash-chain-check"],
            ),
            _archive_section(
                "retention_policy",
                "retained",
                [f"{prefix}://retention/customer-lifecycle-policy", f"{prefix}://retention/legal-hold-policy"],
            ),
            _archive_section(
                "verifier_bundle",
                "verified",
                [f"{prefix}://verifier/customer-lifecycle-bundle", f"{prefix}://verifier/trust-root"],
            ),
            _archive_section(
                "handoff_record",
                "handed_off",
                [f"{prefix}://operations/archive-handoff", "ticket://operations/archive-closeout"],
            ),
        ],
        "retention_controls": {
            "retention_policy_ref": f"{prefix}://retention/customer-lifecycle-policy",
            "legal_hold_policy_ref": f"{prefix}://retention/legal-hold-policy",
            "immutability_policy_ref": f"{prefix}://storage/immutable-archive-policy",
            "deletion_review_policy_ref": f"{prefix}://retention/deletion-review-policy",
        },
        "verifier_refs": [
            f"{prefix}://verifier/customer-lifecycle-bundle",
            f"{prefix}://verifier/trust-root",
            f"{prefix}://audit/hash-chain-check",
        ],
        "archive_controls": {
            "lifecycle_rollup_ready": rollup_result["blocker_count"] == 0,
            "archive_sections_complete": True,
            "retention_controls_present": True,
            "verifier_refs_present": True,
            "audit_handoff_ready": True,
            "customer_identifiers_excluded": True,
            "commercial_terms_excluded": True,
            "private_notes_excluded": True,
        },
    }


def validate_customer_lifecycle_archive_manifest(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_ARCHIVE_SCHEMA else "blocker",
        "Customer lifecycle archive manifest schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_ARCHIVE_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_ARCHIVE_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_profile_ref"), checks, "customer_profile_ref")
    _check_safe_ref(packet.get("lifecycle_rollup_ref"), checks, "lifecycle_rollup_ref")
    _check_rollup_result(packet.get("lifecycle_rollup_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("archive_owner_refs", {}), REQUIRED_ARCHIVE_OWNER_REFS, checks, "archive_owner_refs")
    _check_archive_sections(packet.get("archive_sections", []), checks)
    _check_retention_controls(packet.get("retention_controls", {}), checks)
    _check_verifier_refs(packet.get("verifier_refs", []), checks)
    _check_archive_controls(packet.get("archive_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_lifecycle_archive_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Lifecycle archive manifest contains sanitized refs and archive control metadata only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_ARCHIVE_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_archive_manifest": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_archive_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_lifecycle_archive_manifest(evidence_mode="sample")
    live = build_customer_lifecycle_archive_manifest(evidence_mode="live")
    sample_result = validate_customer_lifecycle_archive_manifest(sample)
    live_result = validate_customer_lifecycle_archive_manifest(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-archive.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-archive.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-archive.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-archive.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-archive-manifest.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_archive_manifest": live_result[
            "ready_for_customer_lifecycle_archive_manifest"
        ],
    }


def _archive_section(section_id: str, status: str, refs: list[str]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "status": status,
        "archive_refs": refs,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized lifecycle archive manifest supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample lifecycle archive manifest validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Lifecycle archive requires evidence_mode=live and sanitized=true.")


def _check_rollup_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "lifecycle_rollup_result", "blocker", "lifecycle_rollup_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_executive_rollup") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "lifecycle_rollup_result", "pass", "Source lifecycle executive rollup is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "lifecycle_rollup_result", "warn", "Source lifecycle rollup validates shape but is not live.")
    else:
        _add_check(checks, "lifecycle_rollup_result", "blocker", "Source lifecycle executive rollup is not ready.")


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


def _check_archive_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "archive_sections", "blocker", "archive_sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing = sorted(REQUIRED_ARCHIVE_SECTIONS - set(section_by_id))
    bad_statuses: list[str] = []
    bad_refs: list[str] = []
    empty_sections: list[str] = []
    for section_id, section in section_by_id.items():
        if str(section.get("status", "")) not in HEALTHY_ARCHIVE_STATUSES:
            bad_statuses.append(section_id)
        refs = section.get("archive_refs", [])
        if not isinstance(refs, list) or not refs:
            empty_sections.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing and not bad_statuses and not bad_refs and not empty_sections:
        _add_check(checks, "archive_sections", "pass", "Lifecycle archive sections are complete.")
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
        _add_check(checks, "archive_sections", "blocker", f"Lifecycle archive sections invalid: {'; '.join(problems)}.")


def _check_retention_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "retention_controls", "blocker", "retention_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_RETENTION_CONTROLS if not controls.get(control))
    unsafe = sorted(field for field, value in controls.items() if value and not _is_safe_ref(value))
    if not missing and not unsafe:
        _add_check(checks, "retention_controls", "pass", "Retention controls are present and sanitized.")
    else:
        problems = []
        if missing:
            problems.append(f"missing controls: {', '.join(missing)}")
        if unsafe:
            problems.append(f"unsafe refs: {', '.join(unsafe)}")
        _add_check(checks, "retention_controls", "blocker", f"Retention controls invalid: {'; '.join(problems)}.")


def _check_verifier_refs(refs: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(refs, list) or not refs:
        _add_check(checks, "verifier_refs", "blocker", "verifier_refs must be a non-empty list.")
        return
    unsafe = [str(index) for index, ref in enumerate(refs) if not _is_safe_ref(ref)]
    _add_check(
        checks,
        "verifier_refs",
        "pass" if not unsafe else "blocker",
        "Verifier refs are present and sanitized." if not unsafe else f"Unsafe verifier refs: {', '.join(unsafe)}.",
    )


def _check_archive_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "archive_controls", "blocker", "archive_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_ARCHIVE_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "archive_controls",
        "pass" if not missing else "blocker",
        "Lifecycle archive controls are explicit."
        if not missing
        else f"Lifecycle archive controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_lifecycle_archive_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_LIFECYCLE_ARCHIVE_FIELDS:
                found.add(path)
            found.update(_find_forbidden_lifecycle_archive_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_lifecycle_archive_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
