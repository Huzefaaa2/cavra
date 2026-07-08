from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANAGED_ENTERPRISE_OPERATING_ANNOUNCEMENT_SCHEMA = "cavra.managed-enterprise-operating-announcement.v1"
MANAGED_ENTERPRISE_OPERATING_ANNOUNCEMENT_RESULT_SCHEMA = "cavra.managed-enterprise-operating-announcement.result.v1"

REQUIRED_PROFILE_FIELDS = {
    "operating_release_index_ref",
    "announcement_owner_ref",
    "approval_record_ref",
    "target_audience_ref",
    "publication_window_ref",
    "evidence_room_ref",
}

REQUIRED_ANNOUNCEMENT_SECTIONS = {
    "release_summary": "Public-safe summary of the Managed or Enterprise operating release.",
    "customer_value": "Customer-safe value statement without customer names or private commercial terms.",
    "operating_assurance": "Statement of live validation, cutover, stabilization, and steady-state assurance.",
    "security_and_trust": "Trust posture, evidence custody, support path, and AISPM operating assurance.",
    "next_steps": "Customer-safe next action, contact path, and operating review cadence.",
}

REQUIRED_SECTION_FIELDS = {
    "section_id",
    "title",
    "objective",
    "content_ref",
    "evidence_ref",
    "approved_by_ref",
}

REQUIRED_CHANNEL_FIELDS = {
    "channel_id",
    "audience_ref",
    "message_ref",
    "owner_ref",
    "approval_ref",
    "publication_status_ref",
}

REQUIRED_CHANNELS = {
    "website": "Product website or commercial front-door update.",
    "github_readme": "Public README note or documentation pointer.",
    "github_wiki": "Wiki textbook or operator documentation pointer.",
    "customer_success": "Customer-success communication for active customers or evaluators.",
    "sales_enablement": "Sales or partner enablement summary.",
}

REQUIRED_OUTCOME_FIELDS = {
    "announcement_decision_ref",
    "publication_blockers_ref",
    "public_safe_claims_ref",
    "next_review_ref",
    "support_contact_ref",
}

REQUIRED_REDACTION_CONTROLS = {
    "contains_no_credentials",
    "contains_no_customer_pii",
    "contains_no_private_release_notes",
    "contains_no_raw_alert_payloads",
    "contains_no_raw_contracts",
    "contains_no_raw_logs",
    "contains_no_raw_model_data",
    "contains_no_raw_prompts",
    "contains_no_secrets",
    "contains_no_tenant_names",
}

FORBIDDEN_FIELDS = {
    "api_key",
    "connection_string",
    "contract_value",
    "customer_name",
    "email",
    "legal_terms",
    "password",
    "private_key",
    "private_release_notes",
    "raw_alert",
    "raw_alerts",
    "raw_contract",
    "raw_contracts",
    "raw_log",
    "raw_logs",
    "raw_model",
    "raw_prompt",
    "raw_prompts",
    "secret",
    "smtp_password",
    "smtp_username",
    "tenant_name",
    "token",
    "training_data",
}

ALLOWED_REF_PREFIXES = (
    "audit://",
    "content://",
    "evidence://",
    "git://",
    "release://",
    "runbook://",
    "share://",
    "ticket://",
    "vault://",
    "workflow://",
    "sample://",
)


def build_managed_enterprise_operating_announcement(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": MANAGED_ENTERPRISE_OPERATING_ANNOUNCEMENT_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "announcement_profile": {
            "operating_release_index_ref": f"{prefix}://managed-enterprise-operating-release/index",
            "announcement_owner_ref": f"{prefix}://owner/managed-enterprise-announcement",
            "approval_record_ref": f"{prefix}://approval/managed-enterprise-announcement",
            "target_audience_ref": f"{prefix}://audience/customer-safe-managed-enterprise",
            "publication_window_ref": f"{prefix}://window/managed-enterprise-announcement",
            "evidence_room_ref": f"{prefix}://evidence-room/managed-enterprise-announcement",
        },
        "announcement_sections": [
            {
                "section_id": section_id,
                "title": section_id.replace("_", " ").title(),
                "objective": objective,
                "content_ref": f"{prefix}://announcement/{section_id}/content",
                "evidence_ref": f"{prefix}://announcement/{section_id}/evidence",
                "approved_by_ref": f"{prefix}://approval/{section_id}",
            }
            for section_id, objective in REQUIRED_ANNOUNCEMENT_SECTIONS.items()
        ],
        "publication_channels": [
            {
                "channel_id": channel_id,
                "audience_ref": f"{prefix}://audience/{channel_id}",
                "message_ref": f"{prefix}://announcement/{channel_id}/message",
                "owner_ref": f"{prefix}://owner/{channel_id}",
                "approval_ref": f"{prefix}://approval/{channel_id}",
                "publication_status_ref": f"{prefix}://publication/{channel_id}/status",
            }
            for channel_id in REQUIRED_CHANNELS
        ],
        "announcement_outcome": {
            "announcement_decision_ref": f"{prefix}://decision/managed-enterprise-announcement-ready",
            "publication_blockers_ref": f"{prefix}://blockers/none-or-accepted",
            "public_safe_claims_ref": f"{prefix}://claims/public-safe-managed-enterprise",
            "next_review_ref": f"{prefix}://review/next-announcement-review",
            "support_contact_ref": f"{prefix}://support/customer-safe-contact-path",
        },
        "redaction_controls": {
            control: True
            for control in sorted(REQUIRED_REDACTION_CONTROLS)
        },
    }


def validate_managed_enterprise_operating_announcement(
    announcement: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if announcement.get("schema_version") == MANAGED_ENTERPRISE_OPERATING_ANNOUNCEMENT_SCHEMA else "blocker",
        "Operating announcement schema is valid."
        if announcement.get("schema_version") == MANAGED_ENTERPRISE_OPERATING_ANNOUNCEMENT_SCHEMA
        else f"Announcement must use {MANAGED_ENTERPRISE_OPERATING_ANNOUNCEMENT_SCHEMA}.",
    )
    _check_evidence_mode(announcement, checks, require_live=require_live)
    _check_ref_object(
        announcement.get("announcement_profile", {}),
        checks,
        name="announcement_profile",
        required_fields=REQUIRED_PROFILE_FIELDS,
    )
    _check_sections(announcement.get("announcement_sections", []), checks)
    _check_channels(announcement.get("publication_channels", []), checks)
    _check_ref_object(
        announcement.get("announcement_outcome", {}),
        checks,
        name="announcement_outcome",
        required_fields=REQUIRED_OUTCOME_FIELDS,
    )
    _check_redaction_controls(announcement.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_operating_announcement_fields(announcement))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Announcement contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and announcement.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_OPERATING_ANNOUNCEMENT_RESULT_SCHEMA,
        "product": announcement.get("product", "CAVRA"),
        "evidence_mode": announcement.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_operating_announcement": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "section_count": (
            len(announcement.get("announcement_sections", []))
            if isinstance(announcement.get("announcement_sections"), list)
            else 0
        ),
        "required_section_count": len(REQUIRED_ANNOUNCEMENT_SECTIONS),
        "channel_count": (
            len(announcement.get("publication_channels", []))
            if isinstance(announcement.get("publication_channels"), list)
            else 0
        ),
        "required_channel_count": len(REQUIRED_CHANNELS),
        "checks": checks,
    }


def write_managed_enterprise_operating_announcement_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_operating_announcement(evidence_mode="sample")
    live = build_managed_enterprise_operating_announcement(evidence_mode="live")
    sample_result = validate_managed_enterprise_operating_announcement(sample)
    live_result = validate_managed_enterprise_operating_announcement(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-operating-announcement.sample.json",
        "live_sanitized_example": output_dir / "managed-enterprise-operating-announcement.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-operating-announcement.sample.result.json",
        "live_result": output_dir / "managed-enterprise-operating-announcement.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.managed-enterprise-operating-announcement.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_operating_announcement": live_result[
            "ready_for_managed_enterprise_operating_announcement"
        ],
    }


def find_forbidden_operating_announcement_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_operating_announcement_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_operating_announcement_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(announcement: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = announcement.get("evidence_mode")
    sanitized = announcement.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized operating announcement supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample operating announcement validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Operating announcement requires evidence_mode=live and sanitized=true.")


def _check_ref_object(
    value: Any,
    checks: list[dict[str, str]],
    *,
    name: str,
    required_fields: set[str],
) -> None:
    if not isinstance(value, dict):
        _add_check(checks, name, "blocker", f"{name} must be an object.")
        return
    missing = sorted(required_fields - set(value))
    invalid_refs = sorted(
        key
        for key, item in value.items()
        if key in required_fields and not _is_ref(item)
    )
    if missing or invalid_refs:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid_refs:
            details.append(f"invalid refs: {', '.join(invalid_refs)}")
        _add_check(checks, name, "blocker", "; ".join(details))
    else:
        _add_check(checks, name, "pass", f"{name} references are complete.")


def _check_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, list):
        _add_check(checks, "announcement_sections", "blocker", "announcement_sections must be a list.")
        return
    by_id = {section.get("section_id"): section for section in sections if isinstance(section, dict)}
    missing_section_ids = sorted(set(REQUIRED_ANNOUNCEMENT_SECTIONS) - set(by_id))
    extra_section_ids = sorted(set(by_id) - set(REQUIRED_ANNOUNCEMENT_SECTIONS))
    failures: list[str] = []
    for section_id in REQUIRED_ANNOUNCEMENT_SECTIONS:
        section = by_id.get(section_id)
        if not isinstance(section, dict):
            continue
        missing_fields = sorted(REQUIRED_SECTION_FIELDS - set(section))
        if missing_fields:
            failures.append(f"{section_id} missing fields: {', '.join(missing_fields)}")
        for field in ("content_ref", "evidence_ref", "approved_by_ref"):
            if field in section and not _is_ref(section[field]):
                failures.append(f"{section_id}.{field} must be a sanitized reference")
    if missing_section_ids or extra_section_ids or failures:
        details = []
        if missing_section_ids:
            details.append(f"missing sections: {', '.join(missing_section_ids)}")
        if extra_section_ids:
            details.append(f"unexpected sections: {', '.join(extra_section_ids)}")
        details.extend(failures)
        _add_check(checks, "announcement_sections", "blocker", "; ".join(details))
    else:
        _add_check(checks, "announcement_sections", "pass", "All required announcement sections are present.")


def _check_channels(channels: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(channels, list):
        _add_check(checks, "publication_channels", "blocker", "publication_channels must be a list.")
        return
    by_id = {channel.get("channel_id"): channel for channel in channels if isinstance(channel, dict)}
    missing_channel_ids = sorted(set(REQUIRED_CHANNELS) - set(by_id))
    extra_channel_ids = sorted(set(by_id) - set(REQUIRED_CHANNELS))
    failures: list[str] = []
    for channel_id in REQUIRED_CHANNELS:
        channel = by_id.get(channel_id)
        if not isinstance(channel, dict):
            continue
        missing_fields = sorted(REQUIRED_CHANNEL_FIELDS - set(channel))
        if missing_fields:
            failures.append(f"{channel_id} missing fields: {', '.join(missing_fields)}")
        for field in ("audience_ref", "message_ref", "owner_ref", "approval_ref", "publication_status_ref"):
            if field in channel and not _is_ref(channel[field]):
                failures.append(f"{channel_id}.{field} must be a sanitized reference")
    if missing_channel_ids or extra_channel_ids or failures:
        details = []
        if missing_channel_ids:
            details.append(f"missing channels: {', '.join(missing_channel_ids)}")
        if extra_channel_ids:
            details.append(f"unexpected channels: {', '.join(extra_channel_ids)}")
        details.extend(failures)
        _add_check(checks, "publication_channels", "blocker", "; ".join(details))
    else:
        _add_check(checks, "publication_channels", "pass", "All required publication channels are present.")


def _check_redaction_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "redaction_controls", "blocker", "redaction_controls must be an object.")
        return
    missing = sorted(REQUIRED_REDACTION_CONTROLS - set(controls))
    false_controls = sorted(key for key in REQUIRED_REDACTION_CONTROLS if controls.get(key) is not True)
    if missing or false_controls:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if false_controls:
            details.append(f"must be true: {', '.join(false_controls)}")
        _add_check(checks, "redaction_controls", "blocker", "; ".join(details))
    else:
        _add_check(checks, "redaction_controls", "pass", "Redaction controls are asserted.")


def _is_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(ALLOWED_REF_PREFIXES)


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
