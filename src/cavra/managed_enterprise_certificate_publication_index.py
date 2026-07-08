from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANAGED_ENTERPRISE_CERTIFICATE_PUBLICATION_INDEX_SCHEMA = (
    "cavra.managed-enterprise-certificate-publication-index.v1"
)
MANAGED_ENTERPRISE_CERTIFICATE_PUBLICATION_INDEX_RESULT_SCHEMA = (
    "cavra.managed-enterprise-certificate-publication-index.result.v1"
)

REQUIRED_PROFILE_FIELDS = {
    "operating_certificate_ref",
    "publication_owner_ref",
    "approval_record_ref",
    "evidence_room_ref",
    "publication_window_ref",
    "rollback_plan_ref",
}

REQUIRED_PUBLICATION_CHANNELS = {
    "product_website": "Commercial product site certificate reference.",
    "github_readme": "Repository README certificate pointer.",
    "github_wiki": "Wiki textbook and operating docs certificate pointer.",
    "customer_success": "Customer-success communication reference.",
    "sales_enablement": "Sales and partner enablement reference.",
    "support_portal": "Support portal or customer helpdesk reference.",
}

REQUIRED_CHANNEL_FIELDS = {
    "channel_id",
    "objective",
    "target_ref",
    "owner_ref",
    "approval_ref",
    "publication_status_ref",
    "rollback_ref",
}

REQUIRED_CLAIM_FIELDS = {
    "claim_id",
    "claim_ref",
    "source_evidence_ref",
    "approved_by_ref",
}

REQUIRED_PUBLIC_SAFE_CLAIMS = {
    "operating_chain_validated",
    "certificate_approved",
    "evidence_custody_active",
    "support_path_active",
    "aispm_operations_active",
}

REQUIRED_OUTCOME_FIELDS = {
    "publication_decision_ref",
    "publication_blockers_ref",
    "published_certificate_ref",
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


def build_managed_enterprise_certificate_publication_index(
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": MANAGED_ENTERPRISE_CERTIFICATE_PUBLICATION_INDEX_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "publication_profile": {
            "operating_certificate_ref": f"{prefix}://certificate/managed-enterprise-operating",
            "publication_owner_ref": f"{prefix}://owner/certificate-publication",
            "approval_record_ref": f"{prefix}://approval/certificate-publication",
            "evidence_room_ref": f"{prefix}://evidence-room/certificate-publication",
            "publication_window_ref": f"{prefix}://window/certificate-publication",
            "rollback_plan_ref": f"{prefix}://runbook/certificate-publication-rollback",
        },
        "publication_channels": [
            {
                "channel_id": channel_id,
                "objective": objective,
                "target_ref": f"{prefix}://publication/{channel_id}/target",
                "owner_ref": f"{prefix}://owner/{channel_id}",
                "approval_ref": f"{prefix}://approval/{channel_id}",
                "publication_status_ref": f"{prefix}://publication/{channel_id}/status",
                "rollback_ref": f"{prefix}://rollback/{channel_id}",
            }
            for channel_id, objective in REQUIRED_PUBLICATION_CHANNELS.items()
        ],
        "public_safe_claims": [
            {
                "claim_id": claim_id,
                "claim_ref": f"{prefix}://claims/{claim_id}",
                "source_evidence_ref": f"{prefix}://certificate-publication/{claim_id}/evidence",
                "approved_by_ref": f"{prefix}://approval/{claim_id}",
            }
            for claim_id in sorted(REQUIRED_PUBLIC_SAFE_CLAIMS)
        ],
        "publication_outcome": {
            "publication_decision_ref": f"{prefix}://decision/certificate-publication-ready",
            "publication_blockers_ref": f"{prefix}://blockers/none-or-accepted",
            "published_certificate_ref": f"{prefix}://certificate/published-managed-enterprise-operating",
            "next_review_ref": f"{prefix}://review/next-certificate-publication-review",
            "support_contact_ref": f"{prefix}://support/customer-safe-contact-path",
        },
        "redaction_controls": {control: True for control in sorted(REQUIRED_REDACTION_CONTROLS)},
    }


def validate_managed_enterprise_certificate_publication_index(
    index: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if index.get("schema_version") == MANAGED_ENTERPRISE_CERTIFICATE_PUBLICATION_INDEX_SCHEMA else "blocker",
        "Certificate publication index schema is valid."
        if index.get("schema_version") == MANAGED_ENTERPRISE_CERTIFICATE_PUBLICATION_INDEX_SCHEMA
        else f"Index must use {MANAGED_ENTERPRISE_CERTIFICATE_PUBLICATION_INDEX_SCHEMA}.",
    )
    _check_evidence_mode(index, checks, require_live=require_live)
    _check_ref_object(
        index.get("publication_profile", {}),
        checks,
        name="publication_profile",
        required_fields=REQUIRED_PROFILE_FIELDS,
    )
    _check_channels(index.get("publication_channels", []), checks)
    _check_claims(index.get("public_safe_claims", []), checks)
    _check_ref_object(
        index.get("publication_outcome", {}),
        checks,
        name="publication_outcome",
        required_fields=REQUIRED_OUTCOME_FIELDS,
    )
    _check_redaction_controls(index.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_certificate_publication_fields(index))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Publication index contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and warning_count == 0 and index.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_CERTIFICATE_PUBLICATION_INDEX_RESULT_SCHEMA,
        "product": index.get("product", "CAVRA"),
        "evidence_mode": index.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_certificate_publication": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "channel_count": (
            len(index.get("publication_channels", []))
            if isinstance(index.get("publication_channels"), list)
            else 0
        ),
        "required_channel_count": len(REQUIRED_PUBLICATION_CHANNELS),
        "claim_count": (
            len(index.get("public_safe_claims", []))
            if isinstance(index.get("public_safe_claims"), list)
            else 0
        ),
        "required_claim_count": len(REQUIRED_PUBLIC_SAFE_CLAIMS),
        "checks": checks,
    }


def write_managed_enterprise_certificate_publication_index_artifacts(
    output_dir: Path,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_certificate_publication_index(evidence_mode="sample")
    live = build_managed_enterprise_certificate_publication_index(evidence_mode="live")
    sample_result = validate_managed_enterprise_certificate_publication_index(sample)
    live_result = validate_managed_enterprise_certificate_publication_index(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-certificate-publication-index.sample.json",
        "live_sanitized_example": output_dir
        / "managed-enterprise-certificate-publication-index.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-certificate-publication-index.sample.result.json",
        "live_result": output_dir / "managed-enterprise-certificate-publication-index.live.sanitized.result.json",
    }
    written["sample"].write_text(
        json.dumps(sample, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    written["live_sanitized_example"].write_text(
        json.dumps(live, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    written["sample_result"].write_text(
        json.dumps(sample_result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    written["live_result"].write_text(
        json.dumps(live_result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "schema_version": "cavra.managed-enterprise-certificate-publication-index.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_certificate_publication": live_result[
            "ready_for_managed_enterprise_certificate_publication"
        ],
    }


def find_forbidden_certificate_publication_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_certificate_publication_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_certificate_publication_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _check_evidence_mode(index: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = index.get("evidence_mode")
    sanitized = index.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized certificate publication index supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample certificate publication index validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Certificate publication index requires evidence_mode=live and sanitized=true.",
        )


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


def _check_channels(channels: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(channels, list):
        _add_check(checks, "publication_channels", "blocker", "publication_channels must be a list.")
        return
    by_id = {channel.get("channel_id"): channel for channel in channels if isinstance(channel, dict)}
    missing_channel_ids = sorted(set(REQUIRED_PUBLICATION_CHANNELS) - set(by_id))
    extra_channel_ids = sorted(set(by_id) - set(REQUIRED_PUBLICATION_CHANNELS))
    failures: list[str] = []
    for channel_id in REQUIRED_PUBLICATION_CHANNELS:
        channel = by_id.get(channel_id)
        if not isinstance(channel, dict):
            continue
        missing_fields = sorted(REQUIRED_CHANNEL_FIELDS - set(channel))
        if missing_fields:
            failures.append(f"{channel_id} missing fields: {', '.join(missing_fields)}")
        for field in ("target_ref", "owner_ref", "approval_ref", "publication_status_ref", "rollback_ref"):
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
        _add_check(checks, "publication_channels", "pass", "All required certificate publication channels are present.")


def _check_claims(claims: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(claims, list):
        _add_check(checks, "public_safe_claims", "blocker", "public_safe_claims must be a list.")
        return
    by_id = {claim.get("claim_id"): claim for claim in claims if isinstance(claim, dict)}
    missing_claim_ids = sorted(REQUIRED_PUBLIC_SAFE_CLAIMS - set(by_id))
    extra_claim_ids = sorted(set(by_id) - REQUIRED_PUBLIC_SAFE_CLAIMS)
    failures: list[str] = []
    for claim_id in REQUIRED_PUBLIC_SAFE_CLAIMS:
        claim = by_id.get(claim_id)
        if not isinstance(claim, dict):
            continue
        missing_fields = sorted(REQUIRED_CLAIM_FIELDS - set(claim))
        if missing_fields:
            failures.append(f"{claim_id} missing fields: {', '.join(missing_fields)}")
        for field in ("claim_ref", "source_evidence_ref", "approved_by_ref"):
            if field in claim and not _is_ref(claim[field]):
                failures.append(f"{claim_id}.{field} must be a sanitized reference")
    if missing_claim_ids or extra_claim_ids or failures:
        details = []
        if missing_claim_ids:
            details.append(f"missing claims: {', '.join(missing_claim_ids)}")
        if extra_claim_ids:
            details.append(f"unexpected claims: {', '.join(extra_claim_ids)}")
        details.extend(failures)
        _add_check(checks, "public_safe_claims", "blocker", "; ".join(details))
    else:
        _add_check(checks, "public_safe_claims", "pass", "All required public-safe claims are present.")


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
