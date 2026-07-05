from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_retrospective import (
    build_customer_lifecycle_retrospective_packet,
    validate_customer_lifecycle_retrospective_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_BACKLOG_SCHEMA = "cavra.customer-lifecycle-phase8-backlog.packet.v1"
CUSTOMER_LIFECYCLE_PHASE8_BACKLOG_RESULT_SCHEMA = "cavra.customer-lifecycle-phase8-backlog.result.v1"

REQUIRED_BACKLOG_OWNER_REFS = {
    "program_owner_ref",
    "product_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
}

REQUIRED_BACKLOG_ITEM_IDS = {
    "phase8-telemetry-depth",
    "phase8-support-automation",
    "phase8-analytics",
}

REQUIRED_BACKLOG_CONTROLS = {
    "retrospective_ready",
    "priorities_assigned",
    "owners_assigned",
    "dependencies_mapped",
    "acceptance_gates_defined",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

VALID_PRIORITIES = {"P0", "P1", "P2"}

FORBIDDEN_PHASE8_BACKLOG_FIELDS = {
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


def build_customer_lifecycle_phase8_backlog_packet(
    retrospective_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    retrospective = retrospective_packet or build_customer_lifecycle_retrospective_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    retrospective_result = validate_customer_lifecycle_retrospective_packet(
        retrospective,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_BACKLOG_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "backlog_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-backlog",
        "retrospective_ref": f"{prefix}://customer-lifecycle-retrospective/r7",
        "retrospective_result": retrospective_result,
        "backlog_owner_refs": {
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
        },
        "backlog_items": [
            _item(
                "phase8-telemetry-depth",
                "P0",
                "Expand customer-safe telemetry depth for lifecycle operations.",
                f"{prefix}://owner/security-platform",
                [f"{prefix}://customer-lifecycle-retrospective/r7"],
                [
                    "Telemetry packet schema is defined.",
                    "Live sanitized example validates with no blockers.",
                    "CI gate covers sample and live sanitized packets.",
                ],
                f"{prefix}://roadmap/phase8-telemetry-depth",
            ),
            _item(
                "phase8-support-automation",
                "P1",
                "Automate support and customer-success checkpoint evidence capture.",
                f"{prefix}://owner/support",
                [f"{prefix}://customer-lifecycle-retrospective/r7", f"{prefix}://support/customer-handoff"],
                [
                    "Support checkpoint packet is defined.",
                    "Owner and escalation refs are sanitized.",
                    "Automation readiness gate validates live sanitized packet.",
                ],
                f"{prefix}://roadmap/phase8-support-automation",
            ),
            _item(
                "phase8-analytics",
                "P1",
                "Add lifecycle analytics for posture, adoption, and operating cadence.",
                f"{prefix}://owner/product-management",
                [f"{prefix}://customer-lifecycle-retrospective/r7", f"{prefix}://roadmap/phase8-telemetry-depth"],
                [
                    "Analytics input contract is defined.",
                    "Dashboard-ready sanitized output examples exist.",
                    "Acceptance tests cover posture, adoption, and cadence summaries.",
                ],
                f"{prefix}://roadmap/phase8-analytics",
            ),
        ],
        "backlog_controls": {
            "retrospective_ready": retrospective_result["blocker_count"] == 0,
            "priorities_assigned": True,
            "owners_assigned": True,
            "dependencies_mapped": True,
            "acceptance_gates_defined": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_backlog_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_BACKLOG_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 backlog schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_BACKLOG_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_BACKLOG_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("retrospective_ref"), checks, "retrospective_ref")
    _check_retrospective_result(packet.get("retrospective_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("backlog_owner_refs", {}), REQUIRED_BACKLOG_OWNER_REFS, checks, "backlog_owner_refs")
    _check_backlog_items(packet.get("backlog_items", []), checks)
    _check_controls(packet.get("backlog_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_backlog_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 backlog contains sanitized refs and customer-safe roadmap text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_BACKLOG_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_backlog": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_backlog_artifacts(output_dir: Path, repo_root: Path | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_backlog_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_backlog_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_backlog_packet(sample)
    live_result = validate_customer_lifecycle_phase8_backlog_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-backlog.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-phase8-backlog.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-backlog.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-backlog.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-backlog.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_backlog": live_result["ready_for_customer_lifecycle_phase8_backlog"],
    }


def _item(
    item_id: str,
    priority: str,
    summary: str,
    owner_ref: str,
    dependency_refs: list[str],
    acceptance_gates: list[str],
    tracking_ref: str,
) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "priority": priority,
        "summary": summary,
        "owner_ref": owner_ref,
        "dependency_refs": dependency_refs,
        "acceptance_gates": acceptance_gates,
        "tracking_ref": tracking_ref,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 backlog supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 backlog validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Phase 8 backlog requires evidence_mode=live and sanitized=true.")


def _check_retrospective_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "retrospective_result", "blocker", "retrospective_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_retrospective") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "retrospective_result", "pass", "Source retrospective packet is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "retrospective_result", "warn", "Source retrospective validates shape but is not live.")
    else:
        _add_check(checks, "retrospective_result", "blocker", "Source retrospective packet is not ready.")


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


def _check_backlog_items(items: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(items, list):
        _add_check(checks, "backlog_items", "blocker", "backlog_items must be a list.")
        return
    by_id = {str(item.get("item_id")): item for item in items if isinstance(item, dict)}
    missing = sorted(REQUIRED_BACKLOG_ITEM_IDS - set(by_id))
    unexpected = sorted(set(by_id) - REQUIRED_BACKLOG_ITEM_IDS)
    bad: list[str] = []
    for item_id, item in by_id.items():
        if item.get("priority") not in VALID_PRIORITIES:
            bad.append(f"{item_id}:priority")
        if len(str(item.get("summary", "")).strip()) < 30:
            bad.append(f"{item_id}:summary")
        if not _is_safe_ref(item.get("owner_ref")):
            bad.append(f"{item_id}:owner_ref")
        if not _is_safe_ref(item.get("tracking_ref")):
            bad.append(f"{item_id}:tracking_ref")
        dependencies = item.get("dependency_refs", [])
        if not isinstance(dependencies, list) or not dependencies:
            bad.append(f"{item_id}:dependency_refs")
        else:
            bad.extend(f"{item_id}:dependency_refs[{index}]" for index, ref in enumerate(dependencies) if not _is_safe_ref(ref))
        gates = item.get("acceptance_gates", [])
        if not isinstance(gates, list) or len(gates) < 2:
            bad.append(f"{item_id}:acceptance_gates")
        else:
            bad.extend(f"{item_id}:acceptance_gates[{index}]" for index, gate in enumerate(gates) if len(str(gate).strip()) < 20)
    if not missing and not unexpected and not bad:
        _add_check(checks, "backlog_items", "pass", "Phase 8 backlog items are prioritized, owned, and gated.")
    else:
        problems = []
        if missing:
            problems.append(f"missing items: {', '.join(missing)}")
        if unexpected:
            problems.append(f"unexpected items: {', '.join(unexpected)}")
        if bad:
            problems.append(f"invalid fields: {', '.join(sorted(bad))}")
        _add_check(checks, "backlog_items", "blocker", f"Phase 8 backlog items invalid: {'; '.join(problems)}.")


def _check_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "backlog_controls", "blocker", "backlog_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_BACKLOG_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "backlog_controls",
        "pass" if not missing else "blocker",
        "Phase 8 backlog controls are explicit."
        if not missing
        else f"Phase 8 backlog controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_backlog_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_BACKLOG_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_backlog_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_backlog_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
