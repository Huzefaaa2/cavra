from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_distribution_audit_index import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_AUDIT_REVIEW_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-audit-review-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_AUDIT_REVIEW_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-audit-review-closeout.result.v1"
)

REQUIRED_AUDIT_REVIEW_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
    "web_owner_ref",
    "compliance_owner_ref",
    "audit_owner_ref",
    "release_manager_ref",
}

REQUIRED_AUDIT_REVIEW_CONTRACT_FIELDS = {
    "audit_review_closeout_ref",
    "source_distribution_audit_index_ref",
    "owner_acknowledgement_ref",
    "residual_findings_ref",
    "remediation_plan_ref",
    "next_refresh_cadence_ref",
    "final_audit_archive_ref",
    "release_notes_ref",
    "redaction_status",
}

REQUIRED_OWNER_ACK_REFS = {
    "executive_ack_ref",
    "communications_ack_ref",
    "security_ack_ref",
    "customer_success_ack_ref",
    "product_ack_ref",
    "audit_ack_ref",
}

REQUIRED_RESIDUAL_FINDING_REFS = {
    "residual_findings_register_ref",
    "accepted_risk_ref",
    "no_critical_findings_ref",
    "followup_owner_ref",
}

REQUIRED_REMEDIATION_REFS = {
    "remediation_plan_ref",
    "remediation_owner_ref",
    "remediation_due_window_ref",
    "remediation_tracking_ref",
}

REQUIRED_REFRESH_CADENCE_REFS = {
    "next_scorecard_refresh_ref",
    "next_distribution_review_ref",
    "next_audit_review_ref",
    "cadence_owner_ref",
}

REQUIRED_FINAL_ARCHIVE_REFS = {
    "audit_review_manifest_ref",
    "distribution_audit_index_archive_ref",
    "owner_ack_archive_ref",
    "remediation_archive_ref",
    "immutable_closeout_snapshot_ref",
}

REQUIRED_RELEASE_NOTE_REFS = {
    "public_release_note_ref",
    "wiki_update_ref",
    "readme_update_ref",
    "roadmap_update_ref",
}

REQUIRED_CI_GATES = {
    "source_distribution_audit_index_validation",
    "owner_acknowledgement_validation",
    "residual_findings_validation",
    "remediation_plan_validation",
    "refresh_cadence_validation",
    "final_archive_validation",
    "release_notes_validation",
}

REQUIRED_AUDIT_REVIEW_CONTROLS = {
    "distribution_audit_index_ready",
    "owner_acknowledgements_complete",
    "residual_findings_reviewed",
    "remediation_refs_defined",
    "next_refresh_cadence_defined",
    "final_archive_complete",
    "release_notes_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_AUDIT_REVIEW_CLOSEOUT_FIELDS = {
    "accepted_risk_detail",
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_health_score",
    "customer_name",
    "customer_score",
    "customer_status",
    "finding_detail",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_ack",
    "raw_archive",
    "raw_audit",
    "raw_contract",
    "raw_distribution",
    "raw_evidence",
    "raw_finding",
    "raw_index",
    "raw_remediation",
    "raw_review",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "recipient_email",
    "remediation_detail",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
    distribution_audit_index_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    distribution_audit_index = (
        distribution_audit_index_packet
        or build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    distribution_audit_index_result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        distribution_audit_index,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_AUDIT_REVIEW_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "audit_review_closeout_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-audit-review-closeout"
        ),
        "distribution_audit_index_ref": (
            f"{prefix}://customer-lifecycle-phase8-public-scorecard-distribution-audit-index/r7"
        ),
        "distribution_audit_index_result": distribution_audit_index_result,
        "audit_review_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "web_owner_ref": f"{prefix}://owner/web-platform",
            "compliance_owner_ref": f"{prefix}://owner/compliance",
            "audit_owner_ref": f"{prefix}://owner/audit",
            "release_manager_ref": f"{prefix}://owner/release-management",
        },
        "audit_review_contract": {
            "audit_review_closeout_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/closeout",
            "source_distribution_audit_index_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/source-distribution-audit-index"
            ),
            "owner_acknowledgement_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/owner-acknowledgement"
            ),
            "residual_findings_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/residual-findings",
            "remediation_plan_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/remediation-plan",
            "next_refresh_cadence_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/next-refresh-cadence"
            ),
            "final_audit_archive_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/final-audit-archive",
            "release_notes_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/release-notes",
            "redaction_status": "sanitized",
        },
        "owner_acknowledgement_refs": {
            "executive_ack_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/ack/executive",
            "communications_ack_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/ack/communications",
            "security_ack_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/ack/security",
            "customer_success_ack_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/ack/customer-success"
            ),
            "product_ack_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/ack/product",
            "audit_ack_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/ack/audit",
        },
        "residual_finding_refs": {
            "residual_findings_register_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/findings/register"
            ),
            "accepted_risk_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/findings/accepted-risk",
            "no_critical_findings_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/findings/no-critical-findings"
            ),
            "followup_owner_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/findings/followup-owner",
        },
        "remediation_refs": {
            "remediation_plan_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/remediation/plan",
            "remediation_owner_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/remediation/owner",
            "remediation_due_window_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/remediation/due-window"
            ),
            "remediation_tracking_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/remediation/tracking",
        },
        "refresh_cadence_refs": {
            "next_scorecard_refresh_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/cadence/next-scorecard-refresh"
            ),
            "next_distribution_review_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/cadence/next-distribution-review"
            ),
            "next_audit_review_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/cadence/next-audit-review",
            "cadence_owner_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/cadence/owner",
        },
        "final_archive_refs": {
            "audit_review_manifest_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/archive/manifest",
            "distribution_audit_index_archive_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/archive/distribution-audit-index"
            ),
            "owner_ack_archive_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/archive/owner-acks",
            "remediation_archive_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/archive/remediation",
            "immutable_closeout_snapshot_ref": (
                f"{prefix}://phase8/public-scorecard-audit-review-closeout/archive/immutable-closeout-snapshot"
            ),
        },
        "release_note_refs": {
            "public_release_note_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/release-note/public",
            "wiki_update_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/release-note/wiki-update",
            "readme_update_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/release-note/readme-update",
            "roadmap_update_ref": f"{prefix}://phase8/public-scorecard-audit-review-closeout/release-note/roadmap-update",
        },
        "ci_gate_coverage": {
            "source_distribution_audit_index_validation": (
                f"{prefix}://ci/phase8/public-scorecard-audit-review-closeout/source-distribution-audit-index-validation"
            ),
            "owner_acknowledgement_validation": (
                f"{prefix}://ci/phase8/public-scorecard-audit-review-closeout/owner-acknowledgement-validation"
            ),
            "residual_findings_validation": (
                f"{prefix}://ci/phase8/public-scorecard-audit-review-closeout/residual-findings-validation"
            ),
            "remediation_plan_validation": (
                f"{prefix}://ci/phase8/public-scorecard-audit-review-closeout/remediation-plan-validation"
            ),
            "refresh_cadence_validation": (
                f"{prefix}://ci/phase8/public-scorecard-audit-review-closeout/refresh-cadence-validation"
            ),
            "final_archive_validation": (
                f"{prefix}://ci/phase8/public-scorecard-audit-review-closeout/final-archive-validation"
            ),
            "release_notes_validation": (
                f"{prefix}://ci/phase8/public-scorecard-audit-review-closeout/release-notes-validation"
            ),
        },
        "audit_review_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-audit-review-closeout/source-distribution-audit-index",
            f"{prefix}://phase8/public-scorecard-audit-review-closeout/owner-acknowledgements",
            f"{prefix}://phase8/public-scorecard-audit-review-closeout/residual-findings",
            f"{prefix}://phase8/public-scorecard-audit-review-closeout/remediation",
            f"{prefix}://phase8/public-scorecard-audit-review-closeout/refresh-cadence",
            f"{prefix}://phase8/public-scorecard-audit-review-closeout/final-archive",
            f"{prefix}://phase8/public-scorecard-audit-review-closeout/release-notes",
        ],
        "audit_review_controls": {
            "distribution_audit_index_ready": distribution_audit_index_result["blocker_count"] == 0,
            "owner_acknowledgements_complete": True,
            "residual_findings_reviewed": True,
            "remediation_refs_defined": True,
            "next_refresh_cadence_defined": True,
            "final_archive_complete": True,
            "release_notes_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    expected_schema = CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_AUDIT_REVIEW_CLOSEOUT_SCHEMA
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == expected_schema else "blocker",
        "Customer lifecycle Phase 8 public scorecard audit review closeout schema is valid."
        if packet.get("schema_version") == expected_schema
        else f"Packet must use {expected_schema}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("distribution_audit_index_ref"), checks, "distribution_audit_index_ref")
    _check_distribution_audit_index_result(
        packet.get("distribution_audit_index_result", {}),
        checks,
        require_live=require_live,
    )
    _check_required_refs(
        packet.get("audit_review_owner_refs", {}),
        REQUIRED_AUDIT_REVIEW_OWNER_REFS,
        checks,
        "audit_review_owner_refs",
    )
    _check_audit_review_contract(packet.get("audit_review_contract", {}), checks)
    _check_required_refs(
        packet.get("owner_acknowledgement_refs", {}),
        REQUIRED_OWNER_ACK_REFS,
        checks,
        "owner_acknowledgement_refs",
    )
    _check_required_refs(
        packet.get("residual_finding_refs", {}),
        REQUIRED_RESIDUAL_FINDING_REFS,
        checks,
        "residual_finding_refs",
    )
    _check_required_refs(packet.get("remediation_refs", {}), REQUIRED_REMEDIATION_REFS, checks, "remediation_refs")
    _check_required_refs(
        packet.get("refresh_cadence_refs", {}),
        REQUIRED_REFRESH_CADENCE_REFS,
        checks,
        "refresh_cadence_refs",
    )
    _check_required_refs(packet.get("final_archive_refs", {}), REQUIRED_FINAL_ARCHIVE_REFS, checks, "final_archive_refs")
    _check_required_refs(packet.get("release_note_refs", {}), REQUIRED_RELEASE_NOTE_REFS, checks, "release_note_refs")
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("audit_review_evidence_refs", []), checks, "audit_review_evidence_refs", min_count=7)
    _check_controls(packet.get("audit_review_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_audit_review_closeout_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard audit review closeout contains sanitized refs and public-safe audit refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_AUDIT_REVIEW_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-audit-review-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-audit-review-closeout.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-scorecard-audit-review-closeout.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-audit-review-closeout.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-audit-review-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 public scorecard audit review closeout supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 public scorecard audit review closeout validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Audit review closeout requires evidence_mode=live and sanitized=true.")


def _check_distribution_audit_index_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "distribution_audit_index_result", "blocker", "distribution_audit_index_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "distribution_audit_index_result", "pass", "Source public scorecard distribution audit index is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "distribution_audit_index_result",
            "warn",
            "Source public scorecard distribution audit index validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "distribution_audit_index_result",
            "blocker",
            "Source public scorecard distribution audit index is not ready.",
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


def _check_audit_review_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "audit_review_contract", "blocker", "audit_review_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_AUDIT_REVIEW_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_AUDIT_REVIEW_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "audit_review_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard audit review closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard audit review closeout contract invalid: "
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
        _add_check(checks, "audit_review_controls", "blocker", "audit_review_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_AUDIT_REVIEW_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "audit_review_controls",
        "pass" if not missing else "blocker",
        "Public scorecard audit review closeout controls are explicit."
        if not missing
        else f"Public scorecard audit review closeout controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_audit_review_closeout_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_AUDIT_REVIEW_CLOSEOUT_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_audit_review_closeout_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_audit_review_closeout_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
