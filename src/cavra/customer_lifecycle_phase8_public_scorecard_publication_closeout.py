from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_operating_scorecard import (
    build_customer_lifecycle_phase8_public_operating_scorecard_packet,
    validate_customer_lifecycle_phase8_public_operating_scorecard_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_PUBLICATION_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-publication-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_PUBLICATION_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-publication-closeout.result.v1"
)

REQUIRED_PUBLICATION_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
}

REQUIRED_PUBLICATION_CONTRACT_FIELDS = {
    "publication_ref",
    "scorecard_ref",
    "announcement_ref",
    "evidence_archive_ref",
    "refresh_cadence_ref",
    "rollback_plan_ref",
    "post_publication_audit_ref",
    "redaction_status",
}

REQUIRED_PUBLICATION_REFS = {
    "published_scorecard_ref",
    "public_status_page_ref",
    "release_notes_ref",
    "stakeholder_notification_ref",
}

REQUIRED_ANNOUNCEMENT_REFS = {
    "executive_announcement_ref",
    "customer_success_announcement_ref",
    "support_announcement_ref",
    "security_announcement_ref",
}

REQUIRED_ARCHIVE_REFS = {
    "immutable_archive_ref",
    "scorecard_snapshot_ref",
    "publication_manifest_ref",
    "audit_evidence_ref",
}

REQUIRED_REFRESH_REFS = {
    "refresh_cadence_ref",
    "next_review_ref",
    "owner_followup_ref",
    "staleness_threshold_ref",
}

REQUIRED_HOLD_ROLLBACK_REFS = {
    "publication_hold_ref",
    "rollback_trigger_ref",
    "rollback_owner_ref",
    "correction_notice_ref",
}

REQUIRED_CI_GATES = {
    "source_scorecard_validation",
    "publication_contract_validation",
    "announcement_ref_validation",
    "archive_ref_validation",
    "rollback_ref_validation",
    "audit_redaction_validation",
}

REQUIRED_CLOSEOUT_CONTROLS = {
    "public_operating_scorecard_ready",
    "publication_refs_defined",
    "announcement_refs_defined",
    "archive_refs_defined",
    "refresh_refs_defined",
    "hold_rollback_refs_defined",
    "post_publication_audit_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_PUBLICATION_CLOSEOUT_FIELDS = {
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
    "raw_announcement",
    "raw_archive",
    "raw_audit",
    "raw_contract",
    "raw_dashboard",
    "raw_evidence",
    "raw_publication",
    "raw_readiness",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "raw_trend",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
    public_operating_scorecard_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    scorecard = (
        public_operating_scorecard_packet
        or build_customer_lifecycle_phase8_public_operating_scorecard_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    scorecard_result = validate_customer_lifecycle_phase8_public_operating_scorecard_packet(
        scorecard,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_PUBLICATION_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "publication_closeout_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-publication-closeout",
        "public_operating_scorecard_ref": f"{prefix}://customer-lifecycle-phase8-public-operating-scorecard/r7",
        "public_operating_scorecard_result": scorecard_result,
        "publication_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "publication_closeout_contract": {
            "publication_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/publication",
            "scorecard_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/scorecard",
            "announcement_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/announcement",
            "evidence_archive_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/evidence-archive",
            "refresh_cadence_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/refresh-cadence",
            "rollback_plan_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/rollback-plan",
            "post_publication_audit_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/post-publication-audit",
            "redaction_status": "sanitized",
        },
        "publication_refs": {
            "published_scorecard_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/publication/published-scorecard",
            "public_status_page_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/publication/public-status-page",
            "release_notes_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/publication/release-notes",
            "stakeholder_notification_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/publication/stakeholder-notification",
        },
        "announcement_refs": {
            "executive_announcement_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/announcement/executive",
            "customer_success_announcement_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/announcement/customer-success",
            "support_announcement_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/announcement/support",
            "security_announcement_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/announcement/security",
        },
        "evidence_archive_refs": {
            "immutable_archive_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/archive/immutable",
            "scorecard_snapshot_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/archive/scorecard-snapshot",
            "publication_manifest_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/archive/publication-manifest",
            "audit_evidence_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/archive/audit-evidence",
        },
        "refresh_cadence_refs": {
            "refresh_cadence_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/refresh/cadence",
            "next_review_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/refresh/next-review",
            "owner_followup_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/refresh/owner-followup",
            "staleness_threshold_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/refresh/staleness-threshold",
        },
        "hold_rollback_refs": {
            "publication_hold_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/rollback/publication-hold",
            "rollback_trigger_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/rollback/trigger",
            "rollback_owner_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/rollback/owner",
            "correction_notice_ref": f"{prefix}://phase8/public-scorecard-publication-closeout/rollback/correction-notice",
        },
        "post_publication_audit_refs": [
            f"{prefix}://phase8/public-scorecard-publication-closeout/audit/redaction",
            f"{prefix}://phase8/public-scorecard-publication-closeout/audit/publication",
            f"{prefix}://phase8/public-scorecard-publication-closeout/audit/archive",
            f"{prefix}://phase8/public-scorecard-publication-closeout/audit/rollback-readiness",
        ],
        "ci_gate_coverage": {
            "source_scorecard_validation": f"{prefix}://ci/phase8/public-scorecard-publication-closeout/source-scorecard-validation",
            "publication_contract_validation": f"{prefix}://ci/phase8/public-scorecard-publication-closeout/publication-contract-validation",
            "announcement_ref_validation": f"{prefix}://ci/phase8/public-scorecard-publication-closeout/announcement-ref-validation",
            "archive_ref_validation": f"{prefix}://ci/phase8/public-scorecard-publication-closeout/archive-ref-validation",
            "rollback_ref_validation": f"{prefix}://ci/phase8/public-scorecard-publication-closeout/rollback-ref-validation",
            "audit_redaction_validation": f"{prefix}://ci/phase8/public-scorecard-publication-closeout/audit-redaction-validation",
        },
        "publication_closeout_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-publication-closeout/source-scorecard",
            f"{prefix}://phase8/public-scorecard-publication-closeout/publication-refs",
            f"{prefix}://phase8/public-scorecard-publication-closeout/announcement-refs",
            f"{prefix}://phase8/public-scorecard-publication-closeout/archive-refs",
            f"{prefix}://phase8/public-scorecard-publication-closeout/audit-refs",
        ],
        "publication_closeout_controls": {
            "public_operating_scorecard_ready": scorecard_result["blocker_count"] == 0,
            "publication_refs_defined": True,
            "announcement_refs_defined": True,
            "archive_refs_defined": True,
            "refresh_refs_defined": True,
            "hold_rollback_refs_defined": True,
            "post_publication_audit_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass"
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_PUBLICATION_CLOSEOUT_SCHEMA
        else "blocker",
        "Customer lifecycle Phase 8 public scorecard publication closeout schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_PUBLICATION_CLOSEOUT_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_PUBLICATION_CLOSEOUT_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("public_operating_scorecard_ref"), checks, "public_operating_scorecard_ref")
    _check_scorecard_result(packet.get("public_operating_scorecard_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("publication_owner_refs", {}),
        REQUIRED_PUBLICATION_OWNER_REFS,
        checks,
        "publication_owner_refs",
    )
    _check_publication_contract(packet.get("publication_closeout_contract", {}), checks)
    _check_required_refs(packet.get("publication_refs", {}), REQUIRED_PUBLICATION_REFS, checks, "publication_refs")
    _check_required_refs(packet.get("announcement_refs", {}), REQUIRED_ANNOUNCEMENT_REFS, checks, "announcement_refs")
    _check_required_refs(
        packet.get("evidence_archive_refs", {}),
        REQUIRED_ARCHIVE_REFS,
        checks,
        "evidence_archive_refs",
    )
    _check_required_refs(
        packet.get("refresh_cadence_refs", {}),
        REQUIRED_REFRESH_REFS,
        checks,
        "refresh_cadence_refs",
    )
    _check_required_refs(
        packet.get("hold_rollback_refs", {}),
        REQUIRED_HOLD_ROLLBACK_REFS,
        checks,
        "hold_rollback_refs",
    )
    _check_ref_list(packet.get("post_publication_audit_refs", []), checks, "post_publication_audit_refs", min_count=4)
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(
        packet.get("publication_closeout_evidence_refs", []),
        checks,
        "publication_closeout_evidence_refs",
        min_count=5,
    )
    _check_controls(packet.get("publication_closeout_controls", {}), checks)
    forbidden = sorted(
        find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_publication_closeout_fields(packet)
    )
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard publication closeout contains sanitized refs and public-safe closeout refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_PUBLICATION_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_publication_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_publication_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-publication-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-publication-closeout.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-scorecard-publication-closeout.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-publication-closeout.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-publication-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_publication_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_publication_closeout"
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
            "Live sanitized Phase 8 public scorecard publication closeout supplied.",
        )
    elif mode == "sample" and not require_live:
        _add_check(
            checks,
            "evidence_mode",
            "warn",
            "Sample Phase 8 public scorecard publication closeout validates shape only.",
        )
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Public scorecard publication closeout requires evidence_mode=live and sanitized=true.",
        )


def _check_scorecard_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "public_operating_scorecard_result",
            "blocker",
            "public_operating_scorecard_result must be an object.",
        )
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_operating_scorecard") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(
            checks,
            "public_operating_scorecard_result",
            "pass",
            "Source public operating scorecard is ready.",
        )
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "public_operating_scorecard_result",
            "warn",
            "Source public operating scorecard validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "public_operating_scorecard_result",
            "blocker",
            "Source public operating scorecard is not ready.",
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


def _check_publication_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(
            checks,
            "publication_closeout_contract",
            "blocker",
            "publication_closeout_contract must be an object.",
        )
        return
    missing = sorted(field for field in REQUIRED_PUBLICATION_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_PUBLICATION_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "publication_closeout_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard publication closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard publication closeout contract invalid: "
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
        _add_check(
            checks,
            "publication_closeout_controls",
            "blocker",
            "publication_closeout_controls must be an object.",
        )
        return
    missing = sorted(control for control in REQUIRED_CLOSEOUT_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "publication_closeout_controls",
        "pass" if not missing else "blocker",
        "Public scorecard publication closeout controls are explicit."
        if not missing
        else f"Public scorecard publication closeout controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_publication_closeout_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_PUBLICATION_CLOSEOUT_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_publication_closeout_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_publication_closeout_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
