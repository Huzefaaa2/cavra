from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_distribution_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_AUDIT_INDEX_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-distribution-audit-index.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_AUDIT_INDEX_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-distribution-audit-index.result.v1"
)

REQUIRED_AUDIT_INDEX_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
    "web_owner_ref",
    "compliance_owner_ref",
    "audit_owner_ref",
}

REQUIRED_AUDIT_INDEX_CONTRACT_FIELDS = {
    "distribution_audit_index_ref",
    "source_distribution_readiness_ref",
    "source_distribution_closeout_ref",
    "publication_snapshot_index_ref",
    "delivery_proof_index_ref",
    "link_check_index_ref",
    "redaction_scan_index_ref",
    "archive_handoff_index_ref",
    "next_review_ref",
    "redaction_status",
}

REQUIRED_DEPENDENCY_REFS = {
    "distribution_readiness_ref",
    "distribution_closeout_ref",
    "executive_summary_closeout_ref",
    "public_scorecard_operating_loop_ref",
}

REQUIRED_PUBLICATION_SNAPSHOT_REFS = {
    "product_website_snapshot_ref",
    "github_readme_snapshot_ref",
    "github_wiki_snapshot_ref",
    "status_page_snapshot_ref",
    "email_update_snapshot_ref",
}

REQUIRED_DELIVERY_PROOF_REFS = {
    "release_notification_proof_ref",
    "customer_success_notification_proof_ref",
    "security_notification_proof_ref",
    "public_status_notification_proof_ref",
}

REQUIRED_LINK_AUDIT_REFS = {
    "product_website_link_audit_ref",
    "readme_link_audit_ref",
    "wiki_link_audit_ref",
    "trial_field_guide_link_audit_ref",
    "sandbox_link_audit_ref",
}

REQUIRED_REDACTION_SCAN_REFS = {
    "private_material_scan_ref",
    "customer_identity_scan_ref",
    "commercial_terms_scan_ref",
    "public_boundary_scan_ref",
}

REQUIRED_ARCHIVE_HANDOFF_REFS = {
    "distribution_archive_manifest_ref",
    "audit_index_archive_ref",
    "evidence_room_handoff_ref",
    "immutable_snapshot_ref",
}

REQUIRED_NEXT_REVIEW_REFS = {
    "next_refresh_trigger_ref",
    "next_audit_review_ref",
    "owner_ack_ref",
    "roadmap_followup_ref",
}

REQUIRED_CI_GATES = {
    "source_distribution_readiness_validation",
    "source_distribution_closeout_validation",
    "publication_snapshot_index_validation",
    "delivery_proof_index_validation",
    "link_audit_validation",
    "redaction_scan_index_validation",
    "archive_handoff_validation",
    "next_review_validation",
}

REQUIRED_AUDIT_INDEX_CONTROLS = {
    "distribution_readiness_ready",
    "distribution_closeout_ready",
    "publication_snapshots_indexed",
    "delivery_proofs_indexed",
    "link_checks_indexed",
    "redaction_scans_indexed",
    "archive_handoff_indexed",
    "next_review_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_DISTRIBUTION_AUDIT_INDEX_FIELDS = {
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
    "raw_index",
    "raw_link_check",
    "raw_notification",
    "raw_proof",
    "raw_publication",
    "raw_score",
    "raw_scorecard",
    "raw_scan",
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


def build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
    distribution_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    distribution_closeout = (
        distribution_closeout_packet
        or build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    distribution_closeout_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        distribution_closeout,
        require_live=evidence_mode == "live",
    )
    distribution_readiness_result = distribution_closeout.get("distribution_readiness_result", {})
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_AUDIT_INDEX_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "distribution_audit_index_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-distribution-audit-index"
        ),
        "distribution_closeout_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-distribution-closeout/r7"
        ),
        "distribution_readiness_result": distribution_readiness_result,
        "distribution_closeout_result": distribution_closeout_result,
        "audit_index_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "web_owner_ref": f"{prefix}://owner/web-platform",
            "compliance_owner_ref": f"{prefix}://owner/compliance",
            "audit_owner_ref": f"{prefix}://owner/audit",
        },
        "audit_index_contract": {
            "distribution_audit_index_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/index",
            "source_distribution_readiness_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/source-distribution-readiness"
            ),
            "source_distribution_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/source-distribution-closeout"
            ),
            "publication_snapshot_index_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/publication-snapshot-index"
            ),
            "delivery_proof_index_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/delivery-proof-index"
            ),
            "link_check_index_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/link-check-index",
            "redaction_scan_index_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/redaction-scan-index"
            ),
            "archive_handoff_index_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/archive-handoff-index"
            ),
            "next_review_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/next-review",
            "redaction_status": "sanitized",
        },
        "dependency_refs": {
            "distribution_readiness_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/dependency/distribution-readiness"
            ),
            "distribution_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/dependency/distribution-closeout"
            ),
            "executive_summary_closeout_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/dependency/executive-summary-closeout"
            ),
            "public_scorecard_operating_loop_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/dependency/operating-loop-index"
            ),
        },
        "publication_snapshot_refs": {
            "product_website_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/snapshot/product-website"
            ),
            "github_readme_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/snapshot/github-readme"
            ),
            "github_wiki_snapshot_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/snapshot/github-wiki",
            "status_page_snapshot_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/snapshot/status-page",
            "email_update_snapshot_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/snapshot/email-update",
        },
        "delivery_proof_refs": {
            "release_notification_proof_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/delivery-proof/release"
            ),
            "customer_success_notification_proof_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/delivery-proof/customer-success"
            ),
            "security_notification_proof_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/delivery-proof/security"
            ),
            "public_status_notification_proof_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/delivery-proof/public-status"
            ),
        },
        "link_audit_refs": {
            "product_website_link_audit_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/link-audit/product-website"
            ),
            "readme_link_audit_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/link-audit/readme",
            "wiki_link_audit_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/link-audit/wiki",
            "trial_field_guide_link_audit_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/link-audit/trial-field-guide"
            ),
            "sandbox_link_audit_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/link-audit/sandbox",
        },
        "redaction_scan_refs": {
            "private_material_scan_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/redaction/private-material-scan"
            ),
            "customer_identity_scan_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/redaction/customer-identity-scan"
            ),
            "commercial_terms_scan_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/redaction/commercial-terms-scan"
            ),
            "public_boundary_scan_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/redaction/public-boundary-scan"
            ),
        },
        "archive_handoff_refs": {
            "distribution_archive_manifest_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/archive/distribution-manifest"
            ),
            "audit_index_archive_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/archive/audit-index"
            ),
            "evidence_room_handoff_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/archive/evidence-room-handoff"
            ),
            "immutable_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/archive/immutable-snapshot"
            ),
        },
        "next_review_refs": {
            "next_refresh_trigger_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/next-review/refresh-trigger"
            ),
            "next_audit_review_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/next-review/audit-review"
            ),
            "owner_ack_ref": f"{prefix}://phase8/public-scorecard-distribution-audit-index/next-review/owner-ack",
            "roadmap_followup_ref": (
                f"{prefix}://phase8/public-scorecard-distribution-audit-index/next-review/roadmap-followup"
            ),
        },
        "ci_gate_coverage": {
            "source_distribution_readiness_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-audit-index/source-distribution-readiness-validation"
            ),
            "source_distribution_closeout_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-audit-index/source-distribution-closeout-validation"
            ),
            "publication_snapshot_index_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-audit-index/publication-snapshot-index-validation"
            ),
            "delivery_proof_index_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-audit-index/delivery-proof-index-validation"
            ),
            "link_audit_validation": f"{prefix}://ci/phase8/public-scorecard-distribution-audit-index/link-audit-validation",
            "redaction_scan_index_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-audit-index/redaction-scan-index-validation"
            ),
            "archive_handoff_validation": (
                f"{prefix}://ci/phase8/public-scorecard-distribution-audit-index/archive-handoff-validation"
            ),
            "next_review_validation": f"{prefix}://ci/phase8/public-scorecard-distribution-audit-index/next-review-validation",
        },
        "audit_index_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-distribution-audit-index/source-distribution-readiness",
            f"{prefix}://phase8/public-scorecard-distribution-audit-index/source-distribution-closeout",
            f"{prefix}://phase8/public-scorecard-distribution-audit-index/publication-snapshots",
            f"{prefix}://phase8/public-scorecard-distribution-audit-index/delivery-proofs",
            f"{prefix}://phase8/public-scorecard-distribution-audit-index/link-audits",
            f"{prefix}://phase8/public-scorecard-distribution-audit-index/redaction-scans",
            f"{prefix}://phase8/public-scorecard-distribution-audit-index/archive-handoff",
            f"{prefix}://phase8/public-scorecard-distribution-audit-index/next-review",
        ],
        "audit_index_controls": {
            "distribution_readiness_ready": _source_blocker_free(distribution_readiness_result),
            "distribution_closeout_ready": distribution_closeout_result["blocker_count"] == 0,
            "publication_snapshots_indexed": True,
            "delivery_proofs_indexed": True,
            "link_checks_indexed": True,
            "redaction_scans_indexed": True,
            "archive_handoff_indexed": True,
            "next_review_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_AUDIT_INDEX_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard distribution audit index schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("distribution_closeout_ref"), checks, "distribution_closeout_ref")
    _check_distribution_readiness_result(packet.get("distribution_readiness_result", {}), checks, require_live=require_live)
    _check_distribution_closeout_result(packet.get("distribution_closeout_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("audit_index_owner_refs", {}),
        REQUIRED_AUDIT_INDEX_OWNER_REFS,
        checks,
        "audit_index_owner_refs",
    )
    _check_audit_index_contract(packet.get("audit_index_contract", {}), checks)
    _check_required_refs(packet.get("dependency_refs", {}), REQUIRED_DEPENDENCY_REFS, checks, "dependency_refs")
    _check_required_refs(
        packet.get("publication_snapshot_refs", {}),
        REQUIRED_PUBLICATION_SNAPSHOT_REFS,
        checks,
        "publication_snapshot_refs",
    )
    _check_required_refs(packet.get("delivery_proof_refs", {}), REQUIRED_DELIVERY_PROOF_REFS, checks, "delivery_proof_refs")
    _check_required_refs(packet.get("link_audit_refs", {}), REQUIRED_LINK_AUDIT_REFS, checks, "link_audit_refs")
    _check_required_refs(packet.get("redaction_scan_refs", {}), REQUIRED_REDACTION_SCAN_REFS, checks, "redaction_scan_refs")
    _check_required_refs(
        packet.get("archive_handoff_refs", {}),
        REQUIRED_ARCHIVE_HANDOFF_REFS,
        checks,
        "archive_handoff_refs",
    )
    _check_required_refs(packet.get("next_review_refs", {}), REQUIRED_NEXT_REVIEW_REFS, checks, "next_review_refs")
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("audit_index_evidence_refs", []), checks, "audit_index_evidence_refs", min_count=8)
    _check_controls(packet.get("audit_index_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_distribution_audit_index_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard distribution audit index contains sanitized refs and public-safe audit refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_DISTRIBUTION_AUDIT_INDEX_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-distribution-audit-index.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-distribution-audit-index.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-scorecard-distribution-audit-index.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-distribution-audit-index.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-distribution-audit-index.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 public scorecard distribution audit index supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 public scorecard distribution audit index validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Distribution audit index requires evidence_mode=live and sanitized=true.")


def _check_distribution_readiness_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    _check_source_result(
        result,
        checks,
        check_name="distribution_readiness_result",
        ready_key="ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness",
        pass_message="Source public scorecard distribution readiness is ready.",
        warn_message="Source public scorecard distribution readiness validates shape but is not live.",
        block_message="Source public scorecard distribution readiness is not ready.",
        require_live=require_live,
    )


def _check_distribution_closeout_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    _check_source_result(
        result,
        checks,
        check_name="distribution_closeout_result",
        ready_key="ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout",
        pass_message="Source public scorecard distribution closeout is ready.",
        warn_message="Source public scorecard distribution closeout validates shape but is not live.",
        block_message="Source public scorecard distribution closeout is not ready.",
        require_live=require_live,
    )


def _check_source_result(
    result: Any,
    checks: list[dict[str, str]],
    *,
    check_name: str,
    ready_key: str,
    pass_message: str,
    warn_message: str,
    block_message: str,
    require_live: bool,
) -> None:
    if not isinstance(result, dict):
        _add_check(checks, check_name, "blocker", f"{check_name} must be an object.")
        return
    ready = result.get(ready_key) is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, check_name, "pass", pass_message)
    elif not require_live and blockers == 0:
        _add_check(checks, check_name, "warn", warn_message)
    else:
        _add_check(checks, check_name, "blocker", block_message)


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


def _check_audit_index_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "audit_index_contract", "blocker", "audit_index_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_AUDIT_INDEX_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_AUDIT_INDEX_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "audit_index_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard distribution audit index contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard distribution audit index contract invalid: "
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
        _add_check(checks, "audit_index_controls", "blocker", "audit_index_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_AUDIT_INDEX_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "audit_index_controls",
        "pass" if not missing else "blocker",
        "Public scorecard distribution audit index controls are explicit."
        if not missing
        else f"Public scorecard distribution audit index controls missing or false: {', '.join(missing)}.",
    )


def _check_safe_ref(value: Any, checks: list[dict[str, str]], name: str) -> None:
    _add_check(
        checks,
        name,
        "pass" if _is_safe_ref(value) else "blocker",
        f"{name} is a sanitized reference." if _is_safe_ref(value) else f"{name} must be a sanitized reference.",
    )


def _source_blocker_free(result: Any) -> bool:
    return isinstance(result, dict) and int(result.get("blocker_count", 1)) == 0


def _prefix(evidence_mode: str) -> str:
    return "sample" if evidence_mode == "sample" else "evidence"


def _is_safe_ref(value: Any) -> bool:
    text = str(value)
    return any(text.startswith(prefix) for prefix in ALLOWED_REF_PREFIXES)


def _find_forbidden_phase8_distribution_audit_index_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_DISTRIBUTION_AUDIT_INDEX_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_distribution_audit_index_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_distribution_audit_index_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
