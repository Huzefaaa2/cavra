from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_executive_summary_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_READINESS_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-distribution-readiness.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_READINESS_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-distribution-readiness.result.v1"
)

REQUIRED_DISTRIBUTION_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
    "web_owner_ref",
}

REQUIRED_DISTRIBUTION_CONTRACT_FIELDS = {
    "distribution_readiness_ref",
    "source_executive_summary_closeout_ref",
    "channel_plan_ref",
    "audience_subscription_ref",
    "release_notification_ref",
    "website_linkage_ref",
    "archive_ref",
    "redaction_ref",
    "redaction_status",
}

REQUIRED_CHANNEL_REFS = {
    "website_channel_ref",
    "github_readme_channel_ref",
    "github_wiki_channel_ref",
    "status_page_channel_ref",
    "email_update_channel_ref",
}

REQUIRED_AUDIENCE_REFS = {
    "executive_subscriber_ref",
    "security_subscriber_ref",
    "customer_success_subscriber_ref",
    "public_reader_ref",
}

REQUIRED_NOTIFICATION_REFS = {
    "release_notification_ref",
    "customer_success_notification_ref",
    "security_notification_ref",
    "public_status_notification_ref",
}

REQUIRED_LINKAGE_REFS = {
    "product_website_link_ref",
    "readme_link_ref",
    "wiki_link_ref",
    "trial_field_guide_link_ref",
    "sandbox_link_ref",
}

REQUIRED_ARCHIVE_REFS = {
    "distribution_manifest_ref",
    "published_channel_snapshot_ref",
    "notification_archive_ref",
    "linkage_archive_ref",
}

REQUIRED_REDACTION_REFS = {
    "distribution_redaction_manifest_ref",
    "private_material_scan_ref",
    "customer_identity_scan_ref",
    "commercial_terms_scan_ref",
}

REQUIRED_CI_GATES = {
    "source_executive_summary_closeout_validation",
    "channel_ref_validation",
    "audience_ref_validation",
    "notification_ref_validation",
    "linkage_ref_validation",
    "archive_ref_validation",
    "redaction_validation",
}

REQUIRED_DISTRIBUTION_CONTROLS = {
    "executive_summary_closeout_ready",
    "channel_refs_defined",
    "audience_refs_defined",
    "notification_refs_defined",
    "linkage_refs_defined",
    "archive_refs_defined",
    "redaction_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_DISTRIBUTION_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_health_score",
    "customer_name",
    "customer_score",
    "customer_status",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_archive",
    "raw_audience",
    "raw_channel",
    "raw_contract",
    "raw_distribution",
    "raw_evidence",
    "raw_linkage",
    "raw_notification",
    "raw_publication",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "raw_subscriber",
    "raw_summary",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
    executive_summary_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    executive_summary_closeout = (
        executive_summary_closeout_packet
        or build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    executive_summary_closeout_result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        executive_summary_closeout,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_READINESS_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "distribution_readiness_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-distribution-readiness"
        ),
        "executive_summary_closeout_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-executive-summary-closeout/r7"
        ),
        "executive_summary_closeout_result": executive_summary_closeout_result,
        "distribution_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "web_owner_ref": f"{prefix}://owner/web-platform",
        },
        "distribution_contract": {
            "distribution_readiness_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/readiness",
            "source_executive_summary_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-readiness/source-executive-summary-closeout"
            ),
            "channel_plan_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/channel-plan",
            "audience_subscription_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/audience-subscription",
            "release_notification_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/release-notification",
            "website_linkage_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/website-linkage",
            "archive_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/archive",
            "redaction_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/redaction",
            "redaction_status": "sanitized",
        },
        "channel_refs": {
            "website_channel_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/channel/website",
            "github_readme_channel_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/channel/github-readme",
            "github_wiki_channel_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/channel/github-wiki",
            "status_page_channel_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/channel/status-page",
            "email_update_channel_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/channel/email-update",
        },
        "audience_refs": {
            "executive_subscriber_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/audience/executive",
            "security_subscriber_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/audience/security",
            "customer_success_subscriber_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/audience/customer-success",
            "public_reader_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/audience/public-reader",
        },
        "notification_refs": {
            "release_notification_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/notification/release",
            "customer_success_notification_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-readiness/notification/customer-success"
            ),
            "security_notification_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/notification/security",
            "public_status_notification_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-readiness/notification/public-status"
            ),
        },
        "linkage_refs": {
            "product_website_link_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/link/product-website",
            "readme_link_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/link/readme",
            "wiki_link_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/link/wiki",
            "trial_field_guide_link_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/link/trial-field-guide",
            "sandbox_link_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/link/sandbox",
        },
        "archive_refs": {
            "distribution_manifest_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/archive/manifest",
            "published_channel_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-readiness/archive/published-channel-snapshot"
            ),
            "notification_archive_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/archive/notifications",
            "linkage_archive_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/archive/linkage",
        },
        "redaction_refs": {
            "distribution_redaction_manifest_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-readiness/redaction/manifest"
            ),
            "private_material_scan_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/redaction/private-material-scan",
            "customer_identity_scan_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/redaction/customer-identity-scan",
            "commercial_terms_scan_ref": f"{prefix}://phase8/public-scorecard-distribution-readiness/redaction/commercial-terms-scan",
        },
        "ci_gate_coverage": {
            "source_executive_summary_closeout_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-readiness/source-executive-summary-closeout-validation"
            ),
            "channel_ref_validation": f"{prefix}://ci/phase8/public-scorecard-distribution-readiness/channel-ref-validation",
            "audience_ref_validation": f"{prefix}://ci/phase8/public-scorecard-distribution-readiness/audience-ref-validation",
            "notification_ref_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-readiness/notification-ref-validation"
            ),
            "linkage_ref_validation": f"{prefix}://ci/phase8/public-scorecard-distribution-readiness/linkage-ref-validation",
            "archive_ref_validation": f"{prefix}://ci/phase8/public-scorecard-distribution-readiness/archive-ref-validation",
            "redaction_validation": f"{prefix}://ci/phase8/public-scorecard-distribution-readiness/redaction-validation",
        },
        "distribution_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-distribution-readiness/source-executive-summary-closeout",
            f"{prefix}://phase8/public-scorecard-distribution-readiness/channels",
            f"{prefix}://phase8/public-scorecard-distribution-readiness/audiences",
            f"{prefix}://phase8/public-scorecard-distribution-readiness/notifications",
            f"{prefix}://phase8/public-scorecard-distribution-readiness/linkage",
            f"{prefix}://phase8/public-scorecard-distribution-readiness/archive",
            f"{prefix}://phase8/public-scorecard-distribution-readiness/redaction",
        ],
        "distribution_controls": {
            "executive_summary_closeout_ready": executive_summary_closeout_result["blocker_count"] == 0,
            "channel_refs_defined": True,
            "audience_refs_defined": True,
            "notification_refs_defined": True,
            "linkage_refs_defined": True,
            "archive_refs_defined": True,
            "redaction_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_READINESS_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 public scorecard distribution readiness schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_READINESS_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_READINESS_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("executive_summary_closeout_ref"), checks, "executive_summary_closeout_ref")
    _check_executive_summary_closeout_result(
        packet.get("executive_summary_closeout_result", {}),
        checks,
        require_live=require_live,
    )
    _check_required_refs(packet.get("distribution_owner_refs", {}), REQUIRED_DISTRIBUTION_OWNER_REFS, checks, "distribution_owner_refs")
    _check_distribution_contract(packet.get("distribution_contract", {}), checks)
    _check_required_refs(packet.get("channel_refs", {}), REQUIRED_CHANNEL_REFS, checks, "channel_refs")
    _check_required_refs(packet.get("audience_refs", {}), REQUIRED_AUDIENCE_REFS, checks, "audience_refs")
    _check_required_refs(packet.get("notification_refs", {}), REQUIRED_NOTIFICATION_REFS, checks, "notification_refs")
    _check_required_refs(packet.get("linkage_refs", {}), REQUIRED_LINKAGE_REFS, checks, "linkage_refs")
    _check_required_refs(packet.get("archive_refs", {}), REQUIRED_ARCHIVE_REFS, checks, "archive_refs")
    _check_required_refs(packet.get("redaction_refs", {}), REQUIRED_REDACTION_REFS, checks, "redaction_refs")
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("distribution_evidence_refs", []), checks, "distribution_evidence_refs", min_count=7)
    _check_controls(packet.get("distribution_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_distribution_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard distribution readiness contains sanitized refs and public-safe distribution refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_READINESS_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_distribution_readiness_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-distribution-readiness.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-distribution-readiness.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-scorecard-distribution-readiness.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-distribution-readiness.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-distribution-readiness.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 public scorecard distribution readiness supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 public scorecard distribution readiness validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Distribution readiness requires evidence_mode=live and sanitized=true.")


def _check_executive_summary_closeout_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "executive_summary_closeout_result", "blocker", "executive_summary_closeout_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "executive_summary_closeout_result", "pass", "Source public scorecard executive summary closeout is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "executive_summary_closeout_result",
            "warn",
            "Source public scorecard executive summary closeout validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "executive_summary_closeout_result",
            "blocker",
            "Source public scorecard executive summary closeout is not ready.",
        )


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


def _check_distribution_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "distribution_contract", "blocker", "distribution_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_DISTRIBUTION_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_DISTRIBUTION_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "distribution_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard distribution readiness contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard distribution readiness contract invalid: "
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
        _add_check(checks, "distribution_controls", "blocker", "distribution_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_DISTRIBUTION_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "distribution_controls",
        "pass" if not missing else "blocker",
        "Public scorecard distribution readiness controls are explicit."
        if not missing
        else f"Public scorecard distribution readiness controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_distribution_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_DISTRIBUTION_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_distribution_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_distribution_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
