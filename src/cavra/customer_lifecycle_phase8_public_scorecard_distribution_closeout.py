from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_distribution_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-distribution-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-distribution-closeout.result.v1"
)

REQUIRED_CLOSEOUT_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
    "web_owner_ref",
    "release_manager_ref",
}

REQUIRED_CLOSEOUT_CONTRACT_FIELDS = {
    "distribution_closeout_ref",
    "source_distribution_readiness_ref",
    "published_channel_closeout_ref",
    "notification_delivery_closeout_ref",
    "link_check_closeout_ref",
    "archive_snapshot_closeout_ref",
    "redaction_closeout_ref",
    "audit_handoff_ref",
    "redaction_status",
}

REQUIRED_PUBLISHED_CHANNEL_REFS = {
    "product_website_published_ref",
    "github_readme_published_ref",
    "github_wiki_published_ref",
    "status_page_published_ref",
    "email_update_published_ref",
}

REQUIRED_NOTIFICATION_DELIVERY_REFS = {
    "release_notification_delivery_ref",
    "customer_success_notification_delivery_ref",
    "security_notification_delivery_ref",
    "public_status_notification_delivery_ref",
}

REQUIRED_LINK_CHECK_REFS = {
    "product_website_link_check_ref",
    "readme_link_check_ref",
    "wiki_link_check_ref",
    "trial_field_guide_link_check_ref",
    "sandbox_link_check_ref",
}

REQUIRED_ARCHIVE_SNAPSHOT_REFS = {
    "distribution_manifest_snapshot_ref",
    "published_channel_snapshot_ref",
    "notification_delivery_archive_ref",
    "link_check_archive_ref",
    "closeout_manifest_ref",
}

REQUIRED_REDACTION_CLOSEOUT_REFS = {
    "distribution_redaction_closeout_ref",
    "private_material_clean_scan_ref",
    "customer_identity_clean_scan_ref",
    "commercial_terms_clean_scan_ref",
}

REQUIRED_AUDIT_HANDOFF_REFS = {
    "public_distribution_audit_ref",
    "evidence_room_handoff_ref",
    "operator_review_ref",
    "next_refresh_trigger_ref",
}

REQUIRED_CI_GATES = {
    "source_distribution_readiness_validation",
    "published_channel_validation",
    "notification_delivery_validation",
    "link_check_validation",
    "archive_snapshot_validation",
    "redaction_closeout_validation",
    "audit_handoff_validation",
}

REQUIRED_CLOSEOUT_CONTROLS = {
    "distribution_readiness_ready",
    "published_channels_confirmed",
    "notifications_delivered",
    "links_checked",
    "archive_snapshots_captured",
    "redaction_closeout_complete",
    "audit_handoff_complete",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_DISTRIBUTION_CLOSEOUT_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_health_score",
    "customer_name",
    "customer_score",
    "customer_status",
    "delivery_detail",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_archive",
    "raw_audit",
    "raw_channel",
    "raw_contract",
    "raw_delivery",
    "raw_distribution",
    "raw_evidence",
    "raw_link_check",
    "raw_notification",
    "raw_publication",
    "raw_score",
    "raw_scorecard",
    "raw_snapshot",
    "raw_status",
    "raw_subscriber",
    "raw_summary",
    "recipient_email",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
    distribution_readiness_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    distribution_readiness = (
        distribution_readiness_packet
        or build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    distribution_readiness_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        distribution_readiness,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "distribution_closeout_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-distribution-closeout"
        ),
        "distribution_readiness_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-distribution-readiness/r7"
        ),
        "distribution_readiness_result": distribution_readiness_result,
        "closeout_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "web_owner_ref": f"{prefix}://owner/web-platform",
            "release_manager_ref": f"{prefix}://owner/release-management",
        },
        "closeout_contract": {
            "distribution_closeout_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/closeout",
            "source_distribution_readiness_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/source-distribution-readiness"
            ),
            "published_channel_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/published-channel-closeout"
            ),
            "notification_delivery_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/notification-delivery-closeout"
            ),
            "link_check_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/link-check-closeout"
            ),
            "archive_snapshot_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/archive-snapshot-closeout"
            ),
            "redaction_closeout_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/redaction-closeout",
            "audit_handoff_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/audit-handoff",
            "redaction_status": "sanitized",
        },
        "published_channel_refs": {
            "product_website_published_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/published/product-website"
            ),
            "github_readme_published_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/published/github-readme"
            ),
            "github_wiki_published_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/published/github-wiki",
            "status_page_published_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/published/status-page",
            "email_update_published_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/published/email-update",
        },
        "notification_delivery_refs": {
            "release_notification_delivery_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/notification/release-delivered"
            ),
            "customer_success_notification_delivery_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/notification/customer-success-delivered"
            ),
            "security_notification_delivery_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/notification/security-delivered"
            ),
            "public_status_notification_delivery_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/notification/public-status-delivered"
            ),
        },
        "link_check_refs": {
            "product_website_link_check_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/link-check/product-website"
            ),
            "readme_link_check_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/link-check/readme",
            "wiki_link_check_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/link-check/wiki",
            "trial_field_guide_link_check_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/link-check/trial-field-guide"
            ),
            "sandbox_link_check_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/link-check/sandbox",
        },
        "archive_snapshot_refs": {
            "distribution_manifest_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/archive/distribution-manifest-snapshot"
            ),
            "published_channel_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/archive/published-channel-snapshot"
            ),
            "notification_delivery_archive_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/archive/notification-delivery"
            ),
            "link_check_archive_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/archive/link-check",
            "closeout_manifest_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/archive/closeout-manifest",
        },
        "redaction_closeout_refs": {
            "distribution_redaction_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/redaction/closeout"
            ),
            "private_material_clean_scan_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/redaction/private-material-clean-scan"
            ),
            "customer_identity_clean_scan_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/redaction/customer-identity-clean-scan"
            ),
            "commercial_terms_clean_scan_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-closeout/redaction/commercial-terms-clean-scan"
            ),
        },
        "audit_handoff_refs": {
            "public_distribution_audit_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/audit/public-distribution",
            "evidence_room_handoff_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/audit/evidence-room-handoff",
            "operator_review_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/audit/operator-review",
            "next_refresh_trigger_ref": f"{prefix}://phase8/public-scorecard-distribution-closeout/audit/next-refresh-trigger",
        },
        "ci_gate_coverage": {
            "source_distribution_readiness_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-closeout/source-distribution-readiness-validation"
            ),
            "published_channel_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-closeout/published-channel-validation"
            ),
            "notification_delivery_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-closeout/notification-delivery-validation"
            ),
            "link_check_validation": f"{prefix}://ci/phase8/public-scorecard-distribution-closeout/link-check-validation",
            "archive_snapshot_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-closeout/archive-snapshot-validation"
            ),
            "redaction_closeout_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-closeout/redaction-closeout-validation"
            ),
            "audit_handoff_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-closeout/audit-handoff-validation"
            ),
        },
        "closeout_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-distribution-closeout/source-distribution-readiness",
            f"{prefix}://phase8/public-scorecard-distribution-closeout/published-channels",
            f"{prefix}://phase8/public-scorecard-distribution-closeout/notification-delivery",
            f"{prefix}://phase8/public-scorecard-distribution-closeout/link-checks",
            f"{prefix}://phase8/public-scorecard-distribution-closeout/archive-snapshots",
            f"{prefix}://phase8/public-scorecard-distribution-closeout/redaction-closeout",
            f"{prefix}://phase8/public-scorecard-distribution-closeout/audit-handoff",
        ],
        "closeout_controls": {
            "distribution_readiness_ready": distribution_readiness_result["blocker_count"] == 0,
            "published_channels_confirmed": True,
            "notifications_delivered": True,
            "links_checked": True,
            "archive_snapshots_captured": True,
            "redaction_closeout_complete": True,
            "audit_handoff_complete": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_CLOSEOUT_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard distribution closeout schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("distribution_readiness_ref"), checks, "distribution_readiness_ref")
    _check_distribution_readiness_result(packet.get("distribution_readiness_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("closeout_owner_refs", {}), REQUIRED_CLOSEOUT_OWNER_REFS, checks, "closeout_owner_refs")
    _check_closeout_contract(packet.get("closeout_contract", {}), checks)
    _check_required_refs(packet.get("published_channel_refs", {}), REQUIRED_PUBLISHED_CHANNEL_REFS, checks, "published_channel_refs")
    _check_required_refs(
        packet.get("notification_delivery_refs", {}),
        REQUIRED_NOTIFICATION_DELIVERY_REFS,
        checks,
        "notification_delivery_refs",
    )
    _check_required_refs(packet.get("link_check_refs", {}), REQUIRED_LINK_CHECK_REFS, checks, "link_check_refs")
    _check_required_refs(
        packet.get("archive_snapshot_refs", {}),
        REQUIRED_ARCHIVE_SNAPSHOT_REFS,
        checks,
        "archive_snapshot_refs",
    )
    _check_required_refs(
        packet.get("redaction_closeout_refs", {}),
        REQUIRED_REDACTION_CLOSEOUT_REFS,
        checks,
        "redaction_closeout_refs",
    )
    _check_required_refs(packet.get("audit_handoff_refs", {}), REQUIRED_AUDIT_HANDOFF_REFS, checks, "audit_handoff_refs")
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("closeout_evidence_refs", []), checks, "closeout_evidence_refs", min_count=7)
    _check_controls(packet.get("closeout_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_distribution_closeout_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard distribution closeout contains sanitized refs and public-safe closeout refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_distribution_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-distribution-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-distribution-closeout.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-scorecard-distribution-closeout.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-distribution-closeout.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-distribution-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 public scorecard distribution closeout supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 public scorecard distribution closeout validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Distribution closeout requires evidence_mode=live and sanitized=true.")


def _check_distribution_readiness_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "distribution_readiness_result", "blocker", "distribution_readiness_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "distribution_readiness_result", "pass", "Source public scorecard distribution readiness is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "distribution_readiness_result",
            "warn",
            "Source public scorecard distribution readiness validates shape but is not live.",
        )
    else:
        _add_check(checks, "distribution_readiness_result", "blocker", "Source public scorecard distribution readiness is not ready.")


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


def _check_closeout_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "closeout_contract", "blocker", "closeout_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_CLOSEOUT_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_CLOSEOUT_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "closeout_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard distribution closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard distribution closeout contract invalid: "
            f"missing {', '.join(missing) or 'none'}; unsafe refs {', '.join(unsafe) or 'none'}."
        ),
    )


def _check_ref_list(refs: Any, checks: list[dict[str, str]], name: str, *, min_count: int) -> None:
    if not isinstance(refs, list) or len(refs) < min_count:
        _add_check(checks, name, "blocker", f"{name} must contain at least {min_count} refs.")
        return
    unsafe = [str(ref) for ref in refs if not _is_safe_ref(ref)]
    _add_check(
        checks,
        name,
        "pass" if not unsafe else "blocker",
        f"{name} are sanitized." if not unsafe else f"{name} are unsafe: {', '.join(unsafe)}.",
    )


def _check_ci_gate_coverage(coverage: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(coverage, dict):
        _add_check(checks, "ci_gate_coverage", "blocker", "ci_gate_coverage must be an object.")
        return
    missing = sorted(gate for gate in REQUIRED_CI_GATES if not coverage.get(gate))
    unsafe = sorted(gate for gate, value in coverage.items() if value and not _is_safe_ref(value))
    _add_check(
        checks,
        "ci_gate_coverage",
        "pass" if not missing and not unsafe else "blocker",
        "CI gate coverage refs are complete."
        if not missing and not unsafe
        else f"CI gate coverage invalid: missing {', '.join(missing) or 'none'}; unsafe {', '.join(unsafe) or 'none'}.",
    )


def _check_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "closeout_controls", "blocker", "closeout_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_CLOSEOUT_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "closeout_controls",
        "pass" if not missing else "blocker",
        "Public scorecard distribution closeout controls are explicit."
        if not missing
        else f"Public scorecard distribution closeout controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_distribution_closeout_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_DISTRIBUTION_CLOSEOUT_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_distribution_closeout_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_distribution_closeout_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
