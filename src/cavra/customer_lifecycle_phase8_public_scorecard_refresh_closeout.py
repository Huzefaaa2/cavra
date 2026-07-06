from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_refresh_checkpoint import (
    build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet,
    validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CLOSEOUT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-refresh-closeout.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CLOSEOUT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-refresh-closeout.result.v1"
)

REQUIRED_REFRESH_CLOSEOUT_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
}

REQUIRED_REFRESH_CLOSEOUT_CONTRACT_FIELDS = {
    "refresh_closeout_ref",
    "source_refresh_checkpoint_ref",
    "updated_scorecard_publication_ref",
    "notification_ref",
    "archive_snapshot_ref",
    "stale_resolution_ref",
    "refresh_audit_closeout_ref",
    "redaction_status",
}

REQUIRED_UPDATED_SCORECARD_REFS = {
    "published_updated_scorecard_ref",
    "scorecard_delta_ref",
    "public_status_update_ref",
    "release_notes_update_ref",
}

REQUIRED_NOTIFICATION_REFS = {
    "executive_notification_ref",
    "customer_success_notification_ref",
    "support_notification_ref",
    "security_notification_ref",
    "stakeholder_notification_ref",
}

REQUIRED_ARCHIVE_SNAPSHOT_REFS = {
    "immutable_refresh_archive_ref",
    "previous_scorecard_snapshot_ref",
    "updated_scorecard_snapshot_ref",
    "refresh_manifest_ref",
}

REQUIRED_STALE_RESOLUTION_REFS = {
    "stale_scorecard_resolution_ref",
    "owner_resolution_ref",
    "public_notice_resolution_ref",
    "next_staleness_review_ref",
}

REQUIRED_REFRESH_AUDIT_CLOSEOUT_REFS = {
    "refresh_audit_report_ref",
    "redaction_closeout_ref",
    "archive_integrity_ref",
    "publication_integrity_ref",
}

REQUIRED_CI_GATES = {
    "source_refresh_checkpoint_validation",
    "updated_scorecard_validation",
    "notification_ref_validation",
    "archive_snapshot_validation",
    "stale_resolution_validation",
    "refresh_audit_closeout_validation",
    "redaction_validation",
}

REQUIRED_REFRESH_CLOSEOUT_CONTROLS = {
    "refresh_checkpoint_ready",
    "updated_scorecard_refs_defined",
    "notification_refs_defined",
    "archive_snapshot_refs_defined",
    "stale_resolution_refs_defined",
    "refresh_audit_closeout_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_REFRESH_CLOSEOUT_FIELDS = {
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
    "raw_audit",
    "raw_contract",
    "raw_dashboard",
    "raw_delta",
    "raw_evidence",
    "raw_notification",
    "raw_publication",
    "raw_refresh",
    "raw_resolution",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "raw_trend",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
    refresh_checkpoint_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    refresh_checkpoint = (
        refresh_checkpoint_packet
        or build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    refresh_checkpoint_result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
        refresh_checkpoint,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "refresh_closeout_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-refresh-closeout",
        "refresh_checkpoint_ref": f"{prefix}://customer-lifecycle-phase8-public-scorecard-refresh-checkpoint/r7",
        "refresh_checkpoint_result": refresh_checkpoint_result,
        "refresh_closeout_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "refresh_closeout_contract": {
            "refresh_closeout_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/closeout",
            "source_refresh_checkpoint_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/source-refresh-checkpoint",
            "updated_scorecard_publication_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/updated-scorecard-publication",
            "notification_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/notification",
            "archive_snapshot_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/archive-snapshot",
            "stale_resolution_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/stale-resolution",
            "refresh_audit_closeout_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/audit-closeout",
            "redaction_status": "sanitized",
        },
        "updated_scorecard_publication_refs": {
            "published_updated_scorecard_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/publication/updated-scorecard",
            "scorecard_delta_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/publication/delta",
            "public_status_update_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/publication/status-update",
            "release_notes_update_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/publication/release-notes-update",
        },
        "notification_refs": {
            "executive_notification_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/notification/executive",
            "customer_success_notification_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/notification/customer-success",
            "support_notification_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/notification/support",
            "security_notification_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/notification/security",
            "stakeholder_notification_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/notification/stakeholder",
        },
        "archive_snapshot_refs": {
            "immutable_refresh_archive_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/archive/immutable-refresh",
            "previous_scorecard_snapshot_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/archive/previous-scorecard",
            "updated_scorecard_snapshot_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/archive/updated-scorecard",
            "refresh_manifest_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/archive/refresh-manifest",
        },
        "stale_resolution_refs": {
            "stale_scorecard_resolution_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/stale/resolution",
            "owner_resolution_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/stale/owner-resolution",
            "public_notice_resolution_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/stale/public-notice-resolution",
            "next_staleness_review_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/stale/next-review",
        },
        "refresh_audit_closeout_refs": {
            "refresh_audit_report_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/audit/report",
            "redaction_closeout_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/audit/redaction-closeout",
            "archive_integrity_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/audit/archive-integrity",
            "publication_integrity_ref": f"{prefix}://phase8/public-scorecard-refresh-closeout/audit/publication-integrity",
        },
        "ci_gate_coverage": {
            "source_refresh_checkpoint_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-closeout/source-refresh-checkpoint-validation",
            "updated_scorecard_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-closeout/updated-scorecard-validation",
            "notification_ref_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-closeout/notification-ref-validation",
            "archive_snapshot_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-closeout/archive-snapshot-validation",
            "stale_resolution_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-closeout/stale-resolution-validation",
            "refresh_audit_closeout_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-closeout/refresh-audit-closeout-validation",
            "redaction_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-closeout/redaction-validation",
        },
        "refresh_closeout_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-refresh-closeout/source-refresh-checkpoint",
            f"{prefix}://phase8/public-scorecard-refresh-closeout/updated-scorecard-publication",
            f"{prefix}://phase8/public-scorecard-refresh-closeout/notifications",
            f"{prefix}://phase8/public-scorecard-refresh-closeout/archive-snapshots",
            f"{prefix}://phase8/public-scorecard-refresh-closeout/stale-resolution",
            f"{prefix}://phase8/public-scorecard-refresh-closeout/audit-closeout",
        ],
        "refresh_closeout_controls": {
            "refresh_checkpoint_ready": refresh_checkpoint_result["blocker_count"] == 0,
            "updated_scorecard_refs_defined": True,
            "notification_refs_defined": True,
            "archive_snapshot_refs_defined": True,
            "stale_resolution_refs_defined": True,
            "refresh_audit_closeout_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass"
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CLOSEOUT_SCHEMA
        else "blocker",
        "Customer lifecycle Phase 8 public scorecard refresh closeout schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CLOSEOUT_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CLOSEOUT_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("refresh_checkpoint_ref"), checks, "refresh_checkpoint_ref")
    _check_refresh_checkpoint_result(packet.get("refresh_checkpoint_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("refresh_closeout_owner_refs", {}),
        REQUIRED_REFRESH_CLOSEOUT_OWNER_REFS,
        checks,
        "refresh_closeout_owner_refs",
    )
    _check_refresh_closeout_contract(packet.get("refresh_closeout_contract", {}), checks)
    _check_required_refs(
        packet.get("updated_scorecard_publication_refs", {}),
        REQUIRED_UPDATED_SCORECARD_REFS,
        checks,
        "updated_scorecard_publication_refs",
    )
    _check_required_refs(packet.get("notification_refs", {}), REQUIRED_NOTIFICATION_REFS, checks, "notification_refs")
    _check_required_refs(
        packet.get("archive_snapshot_refs", {}),
        REQUIRED_ARCHIVE_SNAPSHOT_REFS,
        checks,
        "archive_snapshot_refs",
    )
    _check_required_refs(
        packet.get("stale_resolution_refs", {}),
        REQUIRED_STALE_RESOLUTION_REFS,
        checks,
        "stale_resolution_refs",
    )
    _check_required_refs(
        packet.get("refresh_audit_closeout_refs", {}),
        REQUIRED_REFRESH_AUDIT_CLOSEOUT_REFS,
        checks,
        "refresh_audit_closeout_refs",
    )
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(packet.get("refresh_closeout_evidence_refs", []), checks, "refresh_closeout_evidence_refs", min_count=6)
    _check_controls(packet.get("refresh_closeout_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_refresh_closeout_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard refresh closeout contains sanitized refs and public-safe closeout refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_refresh_closeout_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-refresh-closeout.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-refresh-closeout.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-scorecard-refresh-closeout.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-public-scorecard-refresh-closeout.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-refresh-closeout.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 public scorecard refresh closeout supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 public scorecard refresh closeout validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Public scorecard refresh closeout requires evidence_mode=live and sanitized=true.",
        )


def _check_refresh_checkpoint_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "refresh_checkpoint_result", "blocker", "refresh_checkpoint_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "refresh_checkpoint_result", "pass", "Source public scorecard refresh checkpoint is ready.")
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "refresh_checkpoint_result",
            "warn",
            "Source public scorecard refresh checkpoint validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "refresh_checkpoint_result",
            "blocker",
            "Source public scorecard refresh checkpoint is not ready.",
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


def _check_refresh_closeout_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(checks, "refresh_closeout_contract", "blocker", "refresh_closeout_contract must be an object.")
        return
    missing = sorted(field for field in REQUIRED_REFRESH_CLOSEOUT_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_REFRESH_CLOSEOUT_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "refresh_closeout_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard refresh closeout contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard refresh closeout contract invalid: "
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
        _add_check(checks, "refresh_closeout_controls", "blocker", "refresh_closeout_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_REFRESH_CLOSEOUT_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "refresh_closeout_controls",
        "pass" if not missing else "blocker",
        "Public scorecard refresh closeout controls are explicit."
        if not missing
        else f"Public scorecard refresh closeout controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_refresh_closeout_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_REFRESH_CLOSEOUT_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_refresh_closeout_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_refresh_closeout_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
