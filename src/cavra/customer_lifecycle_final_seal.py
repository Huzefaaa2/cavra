from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_status import (
    build_customer_lifecycle_status_packet,
    validate_customer_lifecycle_status_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_FINAL_SEAL_SCHEMA = "cavra.customer-lifecycle-final-release-seal.packet.v1"
CUSTOMER_LIFECYCLE_FINAL_SEAL_RESULT_SCHEMA = "cavra.customer-lifecycle-final-release-seal.result.v1"

REQUIRED_SEAL_OWNER_REFS = {
    "release_owner_ref",
    "customer_success_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
    "communications_owner_ref",
    "archive_owner_ref",
}

REQUIRED_SEAL_COMPONENTS = {
    "lifecycle_public_status",
    "archive_manifest",
    "executive_rollup",
    "renewal_outcome",
    "operating_review",
    "evidence_room",
    "live_evidence_intake",
}

REQUIRED_RELEASE_CONTROLS = {
    "public_status_ready",
    "archive_manifest_ready",
    "release_notes_ready",
    "customer_success_handoff_ready",
    "support_handoff_ready",
    "security_owner_accepted",
    "communications_owner_accepted",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_FINAL_SEAL_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_name",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_contract",
    "raw_evidence",
    "renewal_amount",
}


def build_customer_lifecycle_final_seal_packet(
    status_packet: dict[str, Any] | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    status = status_packet or build_customer_lifecycle_status_packet(evidence_mode=evidence_mode)
    status_result = validate_customer_lifecycle_status_packet(status, require_live=evidence_mode == "live")
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_FINAL_SEAL_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "final_seal_id": f"cavra-{evidence_mode}-customer-lifecycle-final-release-seal",
        "customer_profile_ref": status.get("customer_profile_ref", f"{prefix}://customer/redacted"),
        "public_status_ref": f"{prefix}://customer-lifecycle-status/public-summary",
        "public_status_result": status_result,
        "seal_owner_refs": {
            "release_owner_ref": f"{prefix}://owner/release-management",
            "customer_success_owner_ref": f"{prefix}://owner/customer-success",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
            "communications_owner_ref": f"{prefix}://owner/customer-communications",
            "archive_owner_ref": f"{prefix}://owner/evidence-archive",
        },
        "sealed_components": [
            _sealed_component("lifecycle_public_status", "sealed", f"{prefix}://customer-lifecycle-status/public-summary"),
            _sealed_component("archive_manifest", "sealed", f"{prefix}://customer-lifecycle-archive/manifest"),
            _sealed_component("executive_rollup", "sealed", f"{prefix}://customer-lifecycle-rollup/executive"),
            _sealed_component("renewal_outcome", "sealed", f"{prefix}://customer-renewal-outcome/closeout"),
            _sealed_component("operating_review", "sealed", f"{prefix}://customer-operating-review/current"),
            _sealed_component("evidence_room", "sealed", f"{prefix}://customer-evidence-room/index"),
            _sealed_component("live_evidence_intake", "sealed", f"{prefix}://customer-live-evidence/intake"),
        ],
        "release_publication_refs": [
            f"{prefix}://release-notes/customer-lifecycle-closeout",
            f"{prefix}://public-status/customer-lifecycle",
            f"{prefix}://support/customer-handoff",
            f"{prefix}://success/next-quarter-plan",
        ],
        "final_release_controls": {
            "public_status_ready": status_result["blocker_count"] == 0,
            "archive_manifest_ready": True,
            "release_notes_ready": True,
            "customer_success_handoff_ready": True,
            "support_handoff_ready": True,
            "security_owner_accepted": True,
            "communications_owner_accepted": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
        "completion_statement": (
            "The CAVRA customer lifecycle public status, archive, executive rollup, renewal outcome, "
            "operating review, evidence room, and live evidence intake are sealed for customer-safe release."
        ),
    }


def validate_customer_lifecycle_final_seal_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_FINAL_SEAL_SCHEMA else "blocker",
        "Customer lifecycle final release seal schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_FINAL_SEAL_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_FINAL_SEAL_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("customer_profile_ref"), checks, "customer_profile_ref")
    _check_safe_ref(packet.get("public_status_ref"), checks, "public_status_ref")
    _check_public_status_result(packet.get("public_status_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("seal_owner_refs", {}), REQUIRED_SEAL_OWNER_REFS, checks, "seal_owner_refs")
    _check_sealed_components(packet.get("sealed_components", []), checks)
    _check_ref_list(packet.get("release_publication_refs", []), checks, "release_publication_refs")
    _check_release_controls(packet.get("final_release_controls", {}), checks)
    _check_completion_statement(packet.get("completion_statement"), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_final_seal_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Final release seal contains sanitized refs and customer-safe release text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_FINAL_SEAL_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_final_release_seal": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_final_seal_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_lifecycle_final_seal_packet(evidence_mode="sample")
    live = build_customer_lifecycle_final_seal_packet(evidence_mode="live")
    sample_result = validate_customer_lifecycle_final_seal_packet(sample)
    live_result = validate_customer_lifecycle_final_seal_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-final-seal.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-final-seal.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-final-seal.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-final-seal.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-final-release-seal.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_final_release_seal": live_result[
            "ready_for_customer_lifecycle_final_release_seal"
        ],
    }


def _sealed_component(component_id: str, status: str, ref: str) -> dict[str, str]:
    return {
        "component_id": component_id,
        "status": status,
        "seal_ref": ref,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized customer lifecycle final seal supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample customer lifecycle final seal validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Final release seal requires evidence_mode=live and sanitized=true.")


def _check_public_status_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "public_status_result", "blocker", "public_status_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_public_status") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "public_status_result", "pass", "Source lifecycle public status is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "public_status_result", "warn", "Source lifecycle public status validates shape but is not live.")
    else:
        _add_check(checks, "public_status_result", "blocker", "Source lifecycle public status is not ready.")


def _check_required_refs(
    payload: Any,
    required: set[str],
    checks: list[dict[str, str]],
    name: str,
) -> None:
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


def _check_sealed_components(components: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(components, list):
        _add_check(checks, "sealed_components", "blocker", "sealed_components must be a list.")
        return
    component_by_id = {str(component.get("component_id")): component for component in components if isinstance(component, dict)}
    missing = sorted(REQUIRED_SEAL_COMPONENTS - set(component_by_id))
    bad_statuses = sorted(
        component_id
        for component_id, component in component_by_id.items()
        if str(component.get("status")) != "sealed"
    )
    bad_refs = sorted(
        component_id
        for component_id, component in component_by_id.items()
        if not _is_safe_ref(component.get("seal_ref"))
    )
    if not missing and not bad_statuses and not bad_refs:
        _add_check(checks, "sealed_components", "pass", "Required lifecycle components are sealed.")
    else:
        problems = []
        if missing:
            problems.append(f"missing components: {', '.join(missing)}")
        if bad_statuses:
            problems.append(f"unsealed components: {', '.join(bad_statuses)}")
        if bad_refs:
            problems.append(f"unsafe seal refs: {', '.join(bad_refs)}")
        _add_check(checks, "sealed_components", "blocker", f"Sealed components invalid: {'; '.join(problems)}.")


def _check_ref_list(refs: Any, checks: list[dict[str, str]], name: str) -> None:
    if not isinstance(refs, list) or not refs:
        _add_check(checks, name, "blocker", f"{name} must be a non-empty list.")
        return
    unsafe = [str(index) for index, ref in enumerate(refs) if not _is_safe_ref(ref)]
    _add_check(
        checks,
        name,
        "pass" if not unsafe else "blocker",
        f"{name} are present and sanitized." if not unsafe else f"{name} contain unsafe refs: {', '.join(unsafe)}.",
    )


def _check_release_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "final_release_controls", "blocker", "final_release_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_RELEASE_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "final_release_controls",
        "pass" if not missing else "blocker",
        "Final release controls are explicit."
        if not missing
        else f"Final release controls missing or false: {', '.join(missing)}.",
    )


def _check_completion_statement(value: Any, checks: list[dict[str, str]]) -> None:
    text = str(value or "").strip()
    _add_check(
        checks,
        "completion_statement",
        "pass" if len(text) >= 40 else "blocker",
        "Completion statement is present and customer-safe."
        if len(text) >= 40
        else "completion_statement must be a customer-safe summary of at least 40 characters.",
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


def _find_forbidden_final_seal_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FINAL_SEAL_FIELDS:
                found.add(path)
            found.update(_find_forbidden_final_seal_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_final_seal_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
