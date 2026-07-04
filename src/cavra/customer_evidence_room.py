from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    build_customer_live_evidence_template,
    find_forbidden_live_evidence_fields,
    validate_customer_live_evidence_packet,
)


CUSTOMER_EVIDENCE_ROOM_SCHEMA = "cavra.customer-evidence-room.index.v1"
CUSTOMER_EVIDENCE_ROOM_RESULT_SCHEMA = "cavra.customer-evidence-room.result.v1"

REQUIRED_EVIDENCE_ROOM_SECTIONS = {
    "executive_summary",
    "platform_readiness",
    "evidence_and_audit",
    "connectors_and_scanners",
    "policy_and_monitoring",
    "phase6_ecosystem",
    "aispm_production",
    "approvals_and_closeout",
}

REQUIRED_PUBLICATION_CONTROLS = {
    "sanitized_only",
    "private_links_access_controlled",
    "no_secret_material",
    "no_raw_model_material",
    "no_customer_pii",
    "reviewer_attestation_required",
}


def build_customer_evidence_room_index(
    intake_packet: dict[str, Any] | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    intake = intake_packet or build_customer_live_evidence_template(evidence_mode=evidence_mode)
    sections = intake.get("evidence_sections", {}) if isinstance(intake.get("evidence_sections"), dict) else {}
    profile = intake.get("customer_profile", {}) if isinstance(intake.get("customer_profile"), dict) else {}
    attestation = intake.get("attestation", {}) if isinstance(intake.get("attestation"), dict) else {}
    return {
        "schema_version": CUSTOMER_EVIDENCE_ROOM_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "evidence_room_id": f"cavra-{evidence_mode}-customer-evidence-room",
        "customer_profile_ref": profile.get("customer_ref", f"{_prefix(evidence_mode)}://customer/redacted"),
        "source_intake_packet_ref": f"{_prefix(evidence_mode)}://customer-live-evidence/intake-packet",
        "publication_controls": {
            "sanitized_only": True,
            "private_links_access_controlled": True,
            "no_secret_material": True,
            "no_raw_model_material": True,
            "no_customer_pii": True,
            "reviewer_attestation_required": True,
        },
        "sections": [
            _section(
                "executive_summary",
                "Executive readiness summary",
                [
                    profile.get("evidence_room_ref", f"{_prefix(evidence_mode)}://evidence-room/cavra-live-closeout"),
                    attestation.get("approval_ref", f"{_prefix(evidence_mode)}://approval/customer-live-closeout"),
                ],
            ),
            _section("platform_readiness", "Platform readiness", _section_refs(sections, "platform_readiness")),
            _section("evidence_and_audit", "Evidence and audit", _section_refs(sections, "evidence_audit")),
            _section("connectors_and_scanners", "Connectors and scanners", _section_refs(sections, "connectors_scanners")),
            _section("policy_and_monitoring", "Policy and monitoring", _section_refs(sections, "policy_monitoring")),
            _section("phase6_ecosystem", "Phase 6 ecosystem gates", _section_refs(sections, "phase6_ecosystem")),
            _section("aispm_production", "AISPM production readiness", _section_refs(sections, "aispm_production")),
            _section(
                "approvals_and_closeout",
                "Approvals and closeout",
                [
                    attestation.get("prepared_by_ref", f"{_prefix(evidence_mode)}://operator/customer-success-security"),
                    attestation.get("reviewer_ref", f"{_prefix(evidence_mode)}://approver/cavra-release-authority"),
                    attestation.get("approval_ref", f"{_prefix(evidence_mode)}://approval/customer-live-closeout"),
                ],
            ),
        ],
        "source_intake_validation": validate_customer_live_evidence_packet(
            intake,
            require_live=evidence_mode == "live",
        ),
    }


def validate_customer_evidence_room_index(
    index: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if index.get("schema_version") == CUSTOMER_EVIDENCE_ROOM_SCHEMA else "blocker",
        "Customer evidence-room index schema is valid."
        if index.get("schema_version") == CUSTOMER_EVIDENCE_ROOM_SCHEMA
        else f"Index must use {CUSTOMER_EVIDENCE_ROOM_SCHEMA}.",
    )
    _check_evidence_mode(index, checks, require_live=require_live)
    _check_publication_controls(index.get("publication_controls", {}), checks)
    _check_sections(index.get("sections", []), checks)
    _check_source_intake(index.get("source_intake_validation", {}), checks, require_live=require_live)
    forbidden = sorted(find_forbidden_live_evidence_fields(index))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Evidence-room index contains sanitized refs and control metadata only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and index.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_EVIDENCE_ROOM_RESULT_SCHEMA,
        "product": index.get("product", "CAVRA"),
        "evidence_mode": index.get("evidence_mode", "unknown"),
        "ready_for_customer_evidence_room_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_evidence_room_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_evidence_room_index(evidence_mode="sample")
    live = build_customer_evidence_room_index(evidence_mode="live")
    sample_result = validate_customer_evidence_room_index(sample)
    live_result = validate_customer_evidence_room_index(live, require_live=True)
    written = {
        "sample": output_dir / "customer-evidence-room.sample.json",
        "live_sanitized_example": output_dir / "customer-evidence-room.live.sanitized.example.json",
        "sample_result": output_dir / "customer-evidence-room.sample.result.json",
        "live_result": output_dir / "customer-evidence-room.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-evidence-room.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_evidence_room_closeout": live_result["ready_for_customer_evidence_room_closeout"],
    }


def _check_evidence_mode(index: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = index.get("evidence_mode")
    sanitized = index.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized evidence-room index supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample evidence-room index validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Evidence-room closeout requires evidence_mode=live and sanitized=true.")


def _check_publication_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "publication_controls", "blocker", "publication_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_PUBLICATION_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "publication_controls",
        "pass" if not missing else "blocker",
        "Evidence-room publication controls are explicit."
        if not missing
        else f"Publication controls missing or false: {', '.join(missing)}.",
    )


def _check_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "sections", "blocker", "sections must be a list.")
        return
    section_by_id = {str(section.get("section_id")): section for section in sections if isinstance(section, dict)}
    missing_sections = sorted(REQUIRED_EVIDENCE_ROOM_SECTIONS - set(section_by_id))
    bad_refs: list[str] = []
    empty_sections: list[str] = []
    for section_id, section in section_by_id.items():
        refs = section.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            empty_sections.append(section_id)
            continue
        bad_refs.extend(f"{section_id}[{index}]" for index, ref in enumerate(refs) if not _is_safe_ref(ref))
    if not missing_sections and not empty_sections and not bad_refs:
        _add_check(checks, "sections", "pass", "Evidence-room sections are complete and sanitized.")
    else:
        problems = []
        if missing_sections:
            problems.append(f"missing sections: {', '.join(missing_sections)}")
        if empty_sections:
            problems.append(f"empty sections: {', '.join(sorted(empty_sections))}")
        if bad_refs:
            problems.append(f"unsafe refs: {', '.join(sorted(bad_refs))}")
        _add_check(checks, "sections", "blocker", f"Evidence-room sections are invalid: {'; '.join(problems)}.")


def _check_source_intake(intake_result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(intake_result, dict):
        _add_check(checks, "source_intake_validation", "blocker", "source_intake_validation must be an object.")
        return
    ready = intake_result.get("ready_for_customer_live_evidence_intake") is True
    blockers = int(intake_result.get("blocker_count", 1))
    warnings = int(intake_result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "source_intake_validation", "pass", "Source customer-live evidence intake is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "source_intake_validation", "warn", "Source intake validates shape but is not live.")
    else:
        _add_check(checks, "source_intake_validation", "blocker", "Source customer-live evidence intake is not ready.")


def _section(section_id: str, title: str, refs: list[Any]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "title": title,
        "evidence_refs": [str(ref) for ref in refs if ref],
    }


def _section_refs(sections: dict[str, Any], key: str) -> list[Any]:
    payload = sections.get(key, {})
    if not isinstance(payload, dict):
        return []
    return [payload[field] for field in sorted(payload) if payload.get(field)]


def _prefix(evidence_mode: str) -> str:
    return "sample" if evidence_mode == "sample" else "evidence"


def _is_safe_ref(value: Any) -> bool:
    text = str(value)
    return any(text.startswith(prefix) for prefix in ALLOWED_REF_PREFIXES)


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
