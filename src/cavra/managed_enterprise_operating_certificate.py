from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANAGED_ENTERPRISE_OPERATING_CERTIFICATE_SCHEMA = "cavra.managed-enterprise-operating-certificate.v1"
MANAGED_ENTERPRISE_OPERATING_CERTIFICATE_RESULT_SCHEMA = "cavra.managed-enterprise-operating-certificate.result.v1"

REQUIRED_PROFILE_FIELDS = {
    "operating_chain_result_ref",
    "certificate_owner_ref",
    "certificate_version_ref",
    "evidence_room_ref",
    "publication_ref",
    "validity_window_ref",
}

REQUIRED_CERTIFICATE_SECTIONS = {
    "scope": "Customer-safe statement of the Managed or Enterprise operating release scope.",
    "readiness_basis": "References the operating chain, live validation, cutover, stabilization, handoff, index, and announcement.",
    "operating_model": "Summarizes named ownership, support path, review cadence, and AISPM operations.",
    "trust_controls": "Summarizes evidence custody, redaction boundary, audit posture, and security signoff.",
    "customer_next_steps": "Customer-safe next actions, support path, and review cadence.",
}

REQUIRED_SECTION_FIELDS = {
    "section_id",
    "title",
    "objective",
    "content_ref",
    "evidence_ref",
}

REQUIRED_SIGNOFFS = {
    "release_owner": "Release owner approves the operating certificate.",
    "security_owner": "Security owner approves the public-safe trust and evidence claims.",
    "support_owner": "Support owner approves the support and escalation path.",
    "customer_success_owner": "Customer-success owner approves customer-safe next steps.",
    "evidence_custodian": "Evidence custodian approves archive and verifier access references.",
}

REQUIRED_SIGNOFF_FIELDS = {
    "signoff_id",
    "objective",
    "owner_ref",
    "approval_ref",
    "evidence_ref",
}

REQUIRED_OUTCOME_FIELDS = {
    "certificate_decision_ref",
    "operating_release_ref",
    "public_safe_claims_ref",
    "open_blockers_ref",
    "next_review_ref",
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
    "certificate://",
    "content://",
    "evidence://",
    "release://",
    "runbook://",
    "share://",
    "ticket://",
    "vault://",
    "workflow://",
    "sample://",
)


def build_managed_enterprise_operating_certificate(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": MANAGED_ENTERPRISE_OPERATING_CERTIFICATE_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "certificate_profile": {
            "operating_chain_result_ref": f"{prefix}://managed-enterprise-operating-chain/result",
            "certificate_owner_ref": f"{prefix}://owner/managed-enterprise-operating-certificate",
            "certificate_version_ref": f"{prefix}://certificate/managed-enterprise-operating/v1",
            "evidence_room_ref": f"{prefix}://evidence-room/managed-enterprise-operating-certificate",
            "publication_ref": f"{prefix}://publication/managed-enterprise-operating-certificate",
            "validity_window_ref": f"{prefix}://window/managed-enterprise-operating-certificate",
        },
        "certificate_sections": [
            {
                "section_id": section_id,
                "title": section_id.replace("_", " ").title(),
                "objective": objective,
                "content_ref": f"{prefix}://certificate/{section_id}/content",
                "evidence_ref": f"{prefix}://certificate/{section_id}/evidence",
            }
            for section_id, objective in REQUIRED_CERTIFICATE_SECTIONS.items()
        ],
        "signoffs": [
            {
                "signoff_id": signoff_id,
                "objective": objective,
                "owner_ref": f"{prefix}://owner/{signoff_id}",
                "approval_ref": f"{prefix}://approval/{signoff_id}",
                "evidence_ref": f"{prefix}://certificate/{signoff_id}/evidence",
            }
            for signoff_id, objective in REQUIRED_SIGNOFFS.items()
        ],
        "certificate_outcome": {
            "certificate_decision_ref": f"{prefix}://decision/managed-enterprise-operating-certificate-ready",
            "operating_release_ref": f"{prefix}://release/managed-enterprise-operating-release",
            "public_safe_claims_ref": f"{prefix}://claims/managed-enterprise-operating-certificate",
            "open_blockers_ref": f"{prefix}://blockers/none-or-accepted",
            "next_review_ref": f"{prefix}://review/next-operating-certificate-review",
        },
        "redaction_controls": {
            control: True
            for control in sorted(REQUIRED_REDACTION_CONTROLS)
        },
    }


def validate_managed_enterprise_operating_certificate(
    certificate: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if certificate.get("schema_version") == MANAGED_ENTERPRISE_OPERATING_CERTIFICATE_SCHEMA else "blocker",
        "Operating certificate schema is valid."
        if certificate.get("schema_version") == MANAGED_ENTERPRISE_OPERATING_CERTIFICATE_SCHEMA
        else f"Certificate must use {MANAGED_ENTERPRISE_OPERATING_CERTIFICATE_SCHEMA}.",
    )
    _check_evidence_mode(certificate, checks, require_live=require_live)
    _check_ref_object(
        certificate.get("certificate_profile", {}),
        checks,
        name="certificate_profile",
        required_fields=REQUIRED_PROFILE_FIELDS,
    )
    _check_sections(certificate.get("certificate_sections", []), checks)
    _check_signoffs(certificate.get("signoffs", []), checks)
    _check_ref_object(
        certificate.get("certificate_outcome", {}),
        checks,
        name="certificate_outcome",
        required_fields=REQUIRED_OUTCOME_FIELDS,
    )
    _check_redaction_controls(certificate.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_operating_certificate_fields(certificate))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Certificate contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and certificate.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_OPERATING_CERTIFICATE_RESULT_SCHEMA,
        "product": certificate.get("product", "CAVRA"),
        "evidence_mode": certificate.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_operating_certificate": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "section_count": (
            len(certificate.get("certificate_sections", []))
            if isinstance(certificate.get("certificate_sections"), list)
            else 0
        ),
        "required_section_count": len(REQUIRED_CERTIFICATE_SECTIONS),
        "signoff_count": len(certificate.get("signoffs", [])) if isinstance(certificate.get("signoffs"), list) else 0,
        "required_signoff_count": len(REQUIRED_SIGNOFFS),
        "checks": checks,
    }


def write_managed_enterprise_operating_certificate_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_operating_certificate(evidence_mode="sample")
    live = build_managed_enterprise_operating_certificate(evidence_mode="live")
    sample_result = validate_managed_enterprise_operating_certificate(sample)
    live_result = validate_managed_enterprise_operating_certificate(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-operating-certificate.sample.json",
        "live_sanitized_example": output_dir / "managed-enterprise-operating-certificate.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-operating-certificate.sample.result.json",
        "live_result": output_dir / "managed-enterprise-operating-certificate.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.managed-enterprise-operating-certificate.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_operating_certificate": live_result[
            "ready_for_managed_enterprise_operating_certificate"
        ],
    }


def find_forbidden_operating_certificate_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_operating_certificate_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_operating_certificate_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(certificate: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = certificate.get("evidence_mode")
    sanitized = certificate.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized operating certificate supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample operating certificate validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Operating certificate requires evidence_mode=live and sanitized=true.")


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
        _add_check(checks, "certificate_sections", "blocker", "certificate_sections must be a list.")
        return
    by_id = {section.get("section_id"): section for section in sections if isinstance(section, dict)}
    missing_section_ids = sorted(set(REQUIRED_CERTIFICATE_SECTIONS) - set(by_id))
    extra_section_ids = sorted(set(by_id) - set(REQUIRED_CERTIFICATE_SECTIONS))
    failures: list[str] = []
    for section_id in REQUIRED_CERTIFICATE_SECTIONS:
        section = by_id.get(section_id)
        if not isinstance(section, dict):
            continue
        missing_fields = sorted(REQUIRED_SECTION_FIELDS - set(section))
        if missing_fields:
            failures.append(f"{section_id} missing fields: {', '.join(missing_fields)}")
        for field in ("content_ref", "evidence_ref"):
            if field in section and not _is_ref(section[field]):
                failures.append(f"{section_id}.{field} must be a sanitized reference")
    if missing_section_ids or extra_section_ids or failures:
        details = []
        if missing_section_ids:
            details.append(f"missing sections: {', '.join(missing_section_ids)}")
        if extra_section_ids:
            details.append(f"unexpected sections: {', '.join(extra_section_ids)}")
        details.extend(failures)
        _add_check(checks, "certificate_sections", "blocker", "; ".join(details))
    else:
        _add_check(checks, "certificate_sections", "pass", "All required certificate sections are present.")


def _check_signoffs(signoffs: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(signoffs, list):
        _add_check(checks, "signoffs", "blocker", "signoffs must be a list.")
        return
    by_id = {signoff.get("signoff_id"): signoff for signoff in signoffs if isinstance(signoff, dict)}
    missing_signoff_ids = sorted(set(REQUIRED_SIGNOFFS) - set(by_id))
    extra_signoff_ids = sorted(set(by_id) - set(REQUIRED_SIGNOFFS))
    failures: list[str] = []
    for signoff_id in REQUIRED_SIGNOFFS:
        signoff = by_id.get(signoff_id)
        if not isinstance(signoff, dict):
            continue
        missing_fields = sorted(REQUIRED_SIGNOFF_FIELDS - set(signoff))
        if missing_fields:
            failures.append(f"{signoff_id} missing fields: {', '.join(missing_fields)}")
        for field in ("owner_ref", "approval_ref", "evidence_ref"):
            if field in signoff and not _is_ref(signoff[field]):
                failures.append(f"{signoff_id}.{field} must be a sanitized reference")
    if missing_signoff_ids or extra_signoff_ids or failures:
        details = []
        if missing_signoff_ids:
            details.append(f"missing signoffs: {', '.join(missing_signoff_ids)}")
        if extra_signoff_ids:
            details.append(f"unexpected signoffs: {', '.join(extra_signoff_ids)}")
        details.extend(failures)
        _add_check(checks, "signoffs", "blocker", "; ".join(details))
    else:
        _add_check(checks, "signoffs", "pass", "All required certificate signoffs are present.")


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
