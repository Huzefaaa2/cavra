from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_public_scorecard_publication_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CHECKPOINT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CHECKPOINT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.result.v1"
)

REQUIRED_REFRESH_OWNER_REFS = {
    "executive_owner_ref",
    "communications_owner_ref",
    "customer_success_owner_ref",
    "support_owner_ref",
    "security_owner_ref",
    "product_owner_ref",
}

REQUIRED_REFRESH_CONTRACT_FIELDS = {
    "refresh_checkpoint_ref",
    "source_publication_ref",
    "refresh_cadence_ref",
    "staleness_detection_ref",
    "owner_followup_ref",
    "update_publication_ref",
    "refresh_audit_ref",
    "redaction_status",
}

REQUIRED_CADENCE_REFS = {
    "active_cadence_ref",
    "last_refresh_ref",
    "next_refresh_ref",
    "cadence_exception_ref",
}

REQUIRED_STALE_REFS = {
    "stale_scorecard_detection_ref",
    "staleness_threshold_ref",
    "stale_owner_escalation_ref",
    "stale_public_notice_ref",
}

REQUIRED_OWNER_FOLLOWUP_REFS = {
    "executive_followup_ref",
    "customer_success_followup_ref",
    "support_followup_ref",
    "security_followup_ref",
    "product_followup_ref",
}

REQUIRED_UPDATE_PUBLICATION_REFS = {
    "updated_scorecard_ref",
    "update_release_notes_ref",
    "public_status_update_ref",
    "stakeholder_update_ref",
}

REQUIRED_AUDIT_REFS = {
    "refresh_manifest_ref",
    "redaction_audit_ref",
    "archive_snapshot_ref",
    "refresh_evidence_ref",
}

REQUIRED_CI_GATES = {
    "source_publication_closeout_validation",
    "refresh_contract_validation",
    "cadence_ref_validation",
    "staleness_ref_validation",
    "owner_followup_validation",
    "update_publication_validation",
    "refresh_audit_redaction_validation",
}

REQUIRED_REFRESH_CONTROLS = {
    "publication_closeout_ready",
    "refresh_cadence_defined",
    "staleness_detection_defined",
    "owner_followup_refs_defined",
    "update_publication_refs_defined",
    "refresh_audit_refs_defined",
    "ci_gates_defined",
    "evidence_refs_sanitized",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_REFRESH_FIELDS = {
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
    "raw_evidence",
    "raw_followup",
    "raw_publication",
    "raw_refresh",
    "raw_score",
    "raw_scorecard",
    "raw_status",
    "raw_trend",
    "renewal_amount",
    "secret",
    "status_detail",
    "token",
}


def build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
    publication_closeout_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    publication_closeout = (
        publication_closeout_packet
        or build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
            repo_root=root,
            evidence_mode=evidence_mode,
        )
    )
    publication_closeout_result = validate_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
        publication_closeout,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CHECKPOINT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "refresh_checkpoint_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-public-scorecard-refresh-checkpoint",
        "publication_closeout_ref": f"{prefix}://customer-lifecycle-phase8-public-scorecard-publication-closeout/r7",
        "publication_closeout_result": publication_closeout_result,
        "refresh_owner_refs": {
            "executive_owner_ref": f"{prefix}://owner/executive-sponsor",
            "communications_owner_ref": f"{prefix}://owner/communications",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "support_owner_ref": f"{prefix}://owner/support",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "product_owner_ref": f"{prefix}://owner/product-management",
        },
        "refresh_checkpoint_contract": {
            "refresh_checkpoint_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/checkpoint",
            "source_publication_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/source-publication",
            "refresh_cadence_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/refresh-cadence",
            "staleness_detection_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/staleness-detection",
            "owner_followup_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/owner-followup",
            "update_publication_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/update-publication",
            "refresh_audit_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/refresh-audit",
            "redaction_status": "sanitized",
        },
        "refresh_cadence_refs": {
            "active_cadence_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/cadence/active",
            "last_refresh_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/cadence/last-refresh",
            "next_refresh_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/cadence/next-refresh",
            "cadence_exception_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/cadence/exception",
        },
        "stale_scorecard_refs": {
            "stale_scorecard_detection_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/stale/detection",
            "staleness_threshold_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/stale/threshold",
            "stale_owner_escalation_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/stale/owner-escalation",
            "stale_public_notice_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/stale/public-notice",
        },
        "owner_followup_refs": {
            "executive_followup_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/followup/executive",
            "customer_success_followup_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/followup/customer-success",
            "support_followup_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/followup/support",
            "security_followup_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/followup/security",
            "product_followup_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/followup/product",
        },
        "update_publication_refs": {
            "updated_scorecard_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/update/scorecard",
            "update_release_notes_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/update/release-notes",
            "public_status_update_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/update/public-status",
            "stakeholder_update_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/update/stakeholder",
        },
        "refresh_audit_refs": {
            "refresh_manifest_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/audit/refresh-manifest",
            "redaction_audit_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/audit/redaction",
            "archive_snapshot_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/audit/archive-snapshot",
            "refresh_evidence_ref": f"{prefix}://phase8/public-scorecard-refresh-checkpoint/audit/refresh-evidence",
        },
        "ci_gate_coverage": {
            "source_publication_closeout_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-checkpoint/source-publication-closeout-validation",
            "refresh_contract_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-checkpoint/refresh-contract-validation",
            "cadence_ref_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-checkpoint/cadence-ref-validation",
            "staleness_ref_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-checkpoint/staleness-ref-validation",
            "owner_followup_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-checkpoint/owner-followup-validation",
            "update_publication_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-checkpoint/update-publication-validation",
            "refresh_audit_redaction_validation": f"{prefix}://ci/phase8/public-scorecard-refresh-checkpoint/refresh-audit-redaction-validation",
        },
        "refresh_checkpoint_evidence_refs": [
            f"{prefix}://phase8/public-scorecard-refresh-checkpoint/source-publication-closeout",
            f"{prefix}://phase8/public-scorecard-refresh-checkpoint/cadence-refs",
            f"{prefix}://phase8/public-scorecard-refresh-checkpoint/staleness-refs",
            f"{prefix}://phase8/public-scorecard-refresh-checkpoint/followup-refs",
            f"{prefix}://phase8/public-scorecard-refresh-checkpoint/update-publication-refs",
            f"{prefix}://phase8/public-scorecard-refresh-checkpoint/audit-refs",
        ],
        "refresh_checkpoint_controls": {
            "publication_closeout_ready": publication_closeout_result["blocker_count"] == 0,
            "refresh_cadence_defined": True,
            "staleness_detection_defined": True,
            "owner_followup_refs_defined": True,
            "update_publication_refs_defined": True,
            "refresh_audit_refs_defined": True,
            "ci_gates_defined": True,
            "evidence_refs_sanitized": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass"
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CHECKPOINT_SCHEMA
        else "blocker",
        "Customer lifecycle Phase 8 public scorecard refresh checkpoint schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CHECKPOINT_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CHECKPOINT_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("publication_closeout_ref"), checks, "publication_closeout_ref")
    _check_publication_closeout_result(packet.get("publication_closeout_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("refresh_owner_refs", {}), REQUIRED_REFRESH_OWNER_REFS, checks, "refresh_owner_refs")
    _check_refresh_contract(packet.get("refresh_checkpoint_contract", {}), checks)
    _check_required_refs(packet.get("refresh_cadence_refs", {}), REQUIRED_CADENCE_REFS, checks, "refresh_cadence_refs")
    _check_required_refs(packet.get("stale_scorecard_refs", {}), REQUIRED_STALE_REFS, checks, "stale_scorecard_refs")
    _check_required_refs(packet.get("owner_followup_refs", {}), REQUIRED_OWNER_FOLLOWUP_REFS, checks, "owner_followup_refs")
    _check_required_refs(
        packet.get("update_publication_refs", {}),
        REQUIRED_UPDATE_PUBLICATION_REFS,
        checks,
        "update_publication_refs",
    )
    _check_required_refs(packet.get("refresh_audit_refs", {}), REQUIRED_AUDIT_REFS, checks, "refresh_audit_refs")
    _check_ci_gate_coverage(packet.get("ci_gate_coverage", {}), checks)
    _check_ref_list(
        packet.get("refresh_checkpoint_evidence_refs", []),
        checks,
        "refresh_checkpoint_evidence_refs",
        min_count=6,
    )
    _check_controls(packet.get("refresh_checkpoint_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_refresh_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 public scorecard refresh checkpoint contains sanitized refs and public-safe refresh refs only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_PUBLIC_SCORECARD_REFRESH_CHECKPOINT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
        repo_root=root,
        evidence_mode="sample",
    )
    live = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
        repo_root=root,
        evidence_mode="live",
    )
    sample_result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(sample)
    live_result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.sample.result.json",
        "live_result": output_dir
        / "customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint": live_result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"
        ],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 public scorecard refresh checkpoint supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 public scorecard refresh checkpoint validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Public scorecard refresh checkpoint requires evidence_mode=live and sanitized=true.",
        )


def _check_publication_closeout_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(
            checks,
            "publication_closeout_result",
            "blocker",
            "publication_closeout_result must be an object.",
        )
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_public_scorecard_publication_closeout") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(
            checks,
            "publication_closeout_result",
            "pass",
            "Source public scorecard publication closeout is ready.",
        )
    elif not require_live and blockers == 0:
        _add_check(
            checks,
            "publication_closeout_result",
            "warn",
            "Source public scorecard publication closeout validates shape but is not live.",
        )
    else:
        _add_check(
            checks,
            "publication_closeout_result",
            "blocker",
            "Source public scorecard publication closeout is not ready.",
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


def _check_refresh_contract(contract: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict):
        _add_check(
            checks,
            "refresh_checkpoint_contract",
            "blocker",
            "refresh_checkpoint_contract must be an object.",
        )
        return
    missing = sorted(field for field in REQUIRED_REFRESH_CONTRACT_FIELDS if not contract.get(field))
    unsafe = sorted(
        field
        for field in REQUIRED_REFRESH_CONTRACT_FIELDS
        if field.endswith("_ref") and contract.get(field) and not _is_safe_ref(contract.get(field))
    )
    redacted = contract.get("redaction_status") == "sanitized"
    _add_check(
        checks,
        "refresh_checkpoint_contract",
        "pass" if not missing and not unsafe and redacted else "blocker",
        "Public scorecard refresh checkpoint contract is complete."
        if not missing and not unsafe and redacted
        else (
            "Public scorecard refresh checkpoint contract invalid: "
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
            "refresh_checkpoint_controls",
            "blocker",
            "refresh_checkpoint_controls must be an object.",
        )
        return
    missing = sorted(control for control in REQUIRED_REFRESH_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "refresh_checkpoint_controls",
        "pass" if not missing else "blocker",
        "Public scorecard refresh checkpoint controls are explicit."
        if not missing
        else f"Public scorecard refresh checkpoint controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_refresh_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_REFRESH_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_refresh_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_refresh_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
