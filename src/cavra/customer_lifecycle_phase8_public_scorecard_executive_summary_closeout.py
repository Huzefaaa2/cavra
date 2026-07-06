from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_operating_loop_index import (
    build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet,
    validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_EXECUTIVE_SUMMARY_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-executive-summary-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_EXECUTIVE_SUMMARY_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-executive-summary-closeout.result.v1"
)

REQUIRED_EXECUTIVE_SUMMARY_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
    "legal_review_owner_ref",
}

REQUIRED_EXECUTIVE_SUMMARY_CONTRACT_FIELDS = {
    "executive_summary_closeout_ref",
    "source_operating_loop_index_ref",
    "summary_publication_ref",
    "audience_alignment_ref",
    "approval_ref",
    "archive_ref",
    "redaction_ref",
    "redaction_status",
}

REQUIRED_SUMMARY_REFS = {
    "public_executive_summary_ref",
    "decision_summary_ref",
    "operating_loop_summary_ref",
    "next_cycle_summary_ref",
}

REQUIRED_AUDIENCE_REFS = {
    "executive_audience_ref",
    "security_audience_ref",
    "customer_success_audience_ref",
    "public_reader_audience_ref",
}

REQUIRED_APPROVAL_REFS = {
    "executive_approval_ref",
    "communications_approval_ref",
    "security_approval_ref",
    "product_approval_ref",
    "legal_redaction_approval_ref",
}

REQUIRED_PUBLICATION_REFS = {
    "published_summary_ref",
    "readme_link_ref",
    "wiki_link_ref",
    "status_page_link_ref",
}

REQUIRED_ARCHIVE_REFS = {
    "summary_archive_manifest_ref",
    "published_summary_snapshot_ref",
    "approval_archive_ref",
    "redaction_archive_ref",
}

REQUIRED_REDACTION_REFS = {
    "redaction_manifest_ref",
    "private_material_scan_ref",
    "customer_identity_scan_ref",
    "commercial_terms_scan_ref",
}

REQUIRED_CI_GATES = {
    "source_operating_loop_index_validation",
    "summary_ref_validation",
    "audience_ref_validation",
    "approval_ref_validation",
    "publication_ref_validation",
    "archive_ref_validation",
    "redaction_validation",
}

REQUIRED_EXECUTIVE_SUMMARY_CONTROLS = {
    "operating_loop_index_ready",
    "summary_refs_defined",
    "audience_refs_defined",
    "approval_refs_defined",
    "publication_refs_defined",
    "archive_refs_defined",
    "redaction_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_EXECUTIVE_SUMMARY_FIELDS = {
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
    "raw_approval",
    "raw_archive",
    "raw_audience",
    "raw_contract",
    "raw_dashboard",
    "raw_decision",
    "raw_evidence",
    "raw_loop",
    "raw_publication",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "raw_summary",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
    operating_loop_index_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    operating_loop_index = (
        operating_loop_index_packet
        or build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    operating_loop_index_result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        operating_loop_index,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_EXECUTIVE_SUMMARY_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "executive_summary_closeout_id": (
            f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-executive-summary-closeout"
        ),
        "operating_loop_index_ref": f"{prefix}://customer-lifecycle-phase8-public-scorecard-operating-loop-index/r7",
        "operating_loop_index_result": operating_loop_index_result,
        "executive_summary_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "legal_review_owner_ref": f"{prefix}://owner/legal-review",
        },
        "executive_summary_contract": {
            "executive_summary_closeout_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/closeout",
            "source_operating_loop_index_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/source-operating-loop-index",
            "summary_publication_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/summary-publication",
            "audience_alignment_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/audience-alignment",
            "approval_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/approval",
            "archive_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/archive",
            "redaction_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/redaction",
            "redaction_status": "sanitized",
        },
        "summary_refs": {
            "public_executive_summary_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/summary/public",
            "decision_summary_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/summary/decision",
            "operating_loop_summary_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/summary/operating-loop",
            "next_cycle_summary_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/summary/next-cycle",
        },
        "audience_refs": {
            "executive_audience_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/audience/executive",
            "security_audience_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/audience/security",
            "customer_success_audience_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/audience/customer-success",
            "public_reader_audience_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/audience/public-reader",
        },
        "approval_refs": {
            "executive_approval_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/approval/executive",
            "communications_approval_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/approval/communications",
            "security_approval_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/approval/security",
            "product_approval_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/approval/product",
            "legal_redaction_approval_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/approval/legal-redaction",
        },
        "publication_refs": {
            "published_summary_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/publication/summary",
            "readme_link_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/publication/readme-link",
            "wiki_link_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/publication/wiki-link",
            "status_page_link_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/publication/status-page-link",
        },
        "archive_refs": {
            "summary_archive_manifest_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/archive/manifest",
            "published_summary_snapshot_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/archive/published-summary",
            "approval_archive_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/archive/approvals",
            "redaction_archive_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/archive/redaction",
        },
        "redaction_refs": {
            "redaction_manifest_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/redaction/manifest",
            "private_material_scan_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/redaction/private-material-scan",
            "customer_identity_scan_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/redaction/customer-identity-scan",
            "commercial_terms_scan_ref": f"{prefix}://phase8/public-scorecard-executive-summary-closeout/redaction/commercial-terms-scan",
        },
        "ci_gate_coverage": {
            "source_operating_loop_index_validation": (
                f"{prefix}://ci/phase8/public-scorecard-executive-summary-closeout/source-operating-loop-index-validation"
            ),
            "summary_ref_validation": f"{prefix}://ci/phase8/public-scorecard-executive-summary-closeout/summary-ref-validation",
            "audience_ref_validation": f"{prefix}://ci/phase8/public-scorecard-executive-summary-closeout/audience-ref-validation",
            "approval_ref_validation": f"{prefix}://ci/phase8/public-scorecard-executive-summary-closeout/approval-ref-validation",
            "publication_ref_validation": (
                f"{prefix}://ci/phase8/public-scorecard-executive-summary-closeout/publication-ref-validation"
            ),
            "archive_ref_validation": f"{prefix}://ci/phase8/public-scorecard-executive-summary-closeout/archive-ref-validation",
            "redaction_validation": f"{prefix}://ci/phase8/public-scorecard-executive-summary-closeout/redaction-validation",
        },
        "executive_summary_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-executive-summary-closeout/source-operating-loop-index",
            f"{prefix}://phase8/public-scorecard-executive-summary-closeout/summary",
            f"{prefix}://phase8/public-scorecard-executive-summary-closeout/audience",
            f"{prefix}://phase8/public-scorecard-executive-summary-closeout/approvals",
            f"{prefix}://phase8/public-scorecard-executive-summary-closeout/publication",
            f"{prefix}://phase8/public-scorecard-executive-summary-closeout/archive",
            f"{prefix}://phase8/public-scorecard-executive-summary-closeout/redaction",
        ],
        "executive_summary_controls": {
            "operating_loop_index_ready": operating_loop_index_result["blocker_count"] == 0,
            "summary_refs_defined": True,
            "audience_refs_defined": True,
            "approval_refs_defined": True,
            "publication_refs_defined": True,
            "archive_refs_defined": True,
            "redaction_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass"
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_EXECUTIVE_SUMMARY_CLOSEOUT_SCHEMA
        else "blocker",
        "Customer lifecycle Phase 8 public scorecard executive summary closeout schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_EXECUTIVE_SUMMARY_CLOSEOUT_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_EXECUTIVE_SUMMARY_CLOSEOUT_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("operating_loop_index_ref"), checks, "operating_loop_index_ref")
    _check_operating_loop_index_result(packet.get("operating_loop_index_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("executive_summary_owner_refs", {}),
        REQUIRED_EXECUTIVE_SUMMARY_OWNER_REFS,
        checks,
        "executive_summary_owner_refs",
    )
    _check_executive_summary_contract(packet.get("executive_summary_contract", {}), checks)
    _check_required_refs(packet.get("summary_refs", {}), REQUIRED_SUMMARY_REFS, checks, "summary_refs")
    _check_required_refs(packet.get("audience_refs", {}), REQUIRED_AUDIENCE_REFS, checks, "audience_refs")
    _check_required_refs(packet.get("approval_refs", {}), REQUIRED_APPROVAL_REFS, checks, "approval_refs")
    _check_required_refs(packet.get("publication_refs", {}), REQUIRED_PUBLICATION_REFS, checks, "publication_refs")
    _check_required_refs(packet.get("archive_refs", {}), REQUIRED_ARCHIVE_REFS, checks, "archive_refs")
    _check_required_refs(packet.get("redaction_refs", {}), REQUIRED_REDACTION_REFS, checks, "redaction_refs")
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(
        packet.get("executive_summary_evidence_refs", []),
        checks,
        "executive_summary_evidence_refs",
        min_count=7,
    )
    _check_controls(packet.get("executive_summary_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_executive_summary_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard executive summary closeout contains sanitized refs and public-safe summary refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_EXECUTIVE_SUMMARY_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        live,
        require_live=True,
    )
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-executive-summary-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-executive-summary-closeout.live.sanitized.example.json",
        "sample_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-executive-summary-closeout.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-executive-summary-closeout.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-executive-summary-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(
            checks,
            "evidence_mode",
            "pass",
            "Live sanitized Phase 8 public scorecard executive summary closeout supplied.",
        )
    elif mode == "sample" and not require_live:
        _add_check(
            checks,
            "evidence_mode",
            "warn",
            "Sample Phase 8 public scorecard executive summary closeout validates shape only.",
        )
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Public scorecard executive summary closeout requires evidence_mode=live and sanitized=true.",
        )


def _check_operating_loop_index_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "operating_loop_index_result", "blocker", "operating_loop_index_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "operating_loop_index_result", "pass", "Source public scorecard operating loop index is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "operating_loop_index_result",
            "warn",
            "Source public scorecard operating loop index validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "operating_loop_index_result",
            "blocker",
            "Source public scorecard operating loop index is not ready.",
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


def _check_executive_summary_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "executive_summary_contract", "blocker", "executive_summary_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_EXECUTIVE_SUMMARY_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_EXECUTIVE_SUMMARY_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "executive_summary_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard executive summary closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard executive summary closeout contract invalid: "
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
        _add_check(checks, "executive_summary_controls", "blocker", "executive_summary_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_EXECUTIVE_SUMMARY_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "executive_summary_controls",
        "pass" if not missing else "blocker",
        "Public scorecard executive summary closeout controls are explicit."
        if not missing
        else f"Public scorecard executive summary closeout controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_executive_summary_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_EXECUTIVE_SUMMARY_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_executive_summary_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_executive_summary_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
