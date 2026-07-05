from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_backlog import (
    build_customer_lifecycle_phase8_backlog_packet,
    validate_customer_lifecycle_phase8_backlog_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_KICKOFF_SCHEMA = "cavra.customer-lifecycle-phase8-kickoff.packet.v1"
CUSTOMER_LIFECYCLE_PHASE8_KICKOFF_RESULT_SCHEMA = "cavra.customer-lifecycle-phase8-kickoff.result.v1"

REQUIRED_KICKOFF_OWNER_REFS = {
    "program_owner_ref",
    "product_owner_ref",
    "engineering_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
}

REQUIRED_KICKOFF_SECTIONS = {
    "kickoff_agenda",
    "first_sprint_plan",
    "readiness_gates",
    "communication_plan",
}

REQUIRED_FIRST_SPRINT_ITEMS = {
    "phase8-telemetry-depth",
    "phase8-support-automation",
    "phase8-analytics",
}

REQUIRED_KICKOFF_CONTROLS = {
    "backlog_ready",
    "kickoff_owners_assigned",
    "first_sprint_defined",
    "readiness_gates_defined",
    "communication_plan_defined",
    "evidence_boundary_confirmed",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

FORBIDDEN_PHASE8_KICKOFF_FIELDS = {
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


def build_customer_lifecycle_phase8_kickoff_packet(
    backlog_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    backlog = backlog_packet or build_customer_lifecycle_phase8_backlog_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    backlog_result = validate_customer_lifecycle_phase8_backlog_packet(
        backlog,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_KICKOFF_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "kickoff_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-kickoff",
        "backlog_ref": f"{prefix}://customer-lifecycle-phase8-backlog/r7",
        "backlog_result": backlog_result,
        "kickoff_owner_refs": {
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "engineering_owner_ref": f"{prefix}://owner/engineering-delivery",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
        },
        "kickoff_sections": {
            "kickoff_agenda": [
                "Review R7 closeout evidence and R7.14 backlog priorities.",
                "Confirm Phase 8 scope, owners, readiness gates, and evidence boundary.",
                "Approve first sprint execution plan for telemetry, support, and analytics workstreams.",
            ],
            "first_sprint_plan": [
                _sprint_item(
                    "phase8-telemetry-depth",
                    f"{prefix}://owner/security-platform",
                    f"{prefix}://roadmap/phase8-telemetry-depth",
                    [
                        "Draft telemetry packet schema.",
                        "Add live sanitized validation fixture.",
                        "Prepare CI gate for telemetry packet examples.",
                    ],
                ),
                _sprint_item(
                    "phase8-support-automation",
                    f"{prefix}://owner/support",
                    f"{prefix}://roadmap/phase8-support-automation",
                    [
                        "Define support checkpoint packet shape.",
                        "Map escalation and owner references.",
                        "Prepare automation readiness validator.",
                    ],
                ),
                _sprint_item(
                    "phase8-analytics",
                    f"{prefix}://owner/product-management",
                    f"{prefix}://roadmap/phase8-analytics",
                    [
                        "Define lifecycle analytics input contract.",
                        "Add dashboard-safe output examples.",
                        "Prepare tests for posture, adoption, and cadence summaries.",
                    ],
                ),
            ],
            "readiness_gates": [
                "Backlog packet validates live sanitized with no blockers.",
                "Every first sprint item has owner, tracking ref, and acceptance tasks.",
                "No customer identities, raw evidence, private notes, pricing, legal, or commercial terms are embedded.",
            ],
            "communication_plan": [
                "Publish internal Phase 8 kickoff note using sanitized references only.",
                "Keep customer-specific delivery context in deployment-private systems.",
                "Update public roadmap only after validated gate completion.",
            ],
        },
        "kickoff_controls": {
            "backlog_ready": backlog_result["blocker_count"] == 0,
            "kickoff_owners_assigned": True,
            "first_sprint_defined": True,
            "readiness_gates_defined": True,
            "communication_plan_defined": True,
            "evidence_boundary_confirmed": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_kickoff_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_KICKOFF_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 kickoff schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_KICKOFF_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_KICKOFF_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("backlog_ref"), checks, "backlog_ref")
    _check_backlog_result(packet.get("backlog_result", {}), checks, require_live=require_live)
    _check_required_refs(packet.get("kickoff_owner_refs", {}), REQUIRED_KICKOFF_OWNER_REFS, checks, "kickoff_owner_refs")
    _check_kickoff_sections(packet.get("kickoff_sections", {}), checks)
    _check_controls(packet.get("kickoff_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_kickoff_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 kickoff contains sanitized refs and customer-safe planning text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_KICKOFF_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_kickoff": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_kickoff_artifacts(output_dir: Path, repo_root: Path | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_kickoff_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_kickoff_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_kickoff_packet(sample)
    live_result = validate_customer_lifecycle_phase8_kickoff_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-kickoff.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-phase8-kickoff.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-kickoff.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-kickoff.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-kickoff.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_kickoff": live_result["ready_for_customer_lifecycle_phase8_kickoff"],
    }


def _sprint_item(item_id: str, owner_ref: str, tracking_ref: str, acceptance_tasks: list[str]) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "owner_ref": owner_ref,
        "tracking_ref": tracking_ref,
        "acceptance_tasks": acceptance_tasks,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 kickoff supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 kickoff validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Phase 8 kickoff requires evidence_mode=live and sanitized=true.")


def _check_backlog_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "backlog_result", "blocker", "backlog_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_backlog") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "backlog_result", "pass", "Source Phase 8 backlog packet is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "backlog_result", "warn", "Source Phase 8 backlog validates shape but is not live.")
    else:
        _add_check(checks, "backlog_result", "blocker", "Source Phase 8 backlog packet is not ready.")


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


def _check_kickoff_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, dict):
        _add_check(checks, "kickoff_sections", "blocker", "kickoff_sections must be an object.")
        return
    missing = sorted(section for section in REQUIRED_KICKOFF_SECTIONS if section not in sections)
    bad: list[str] = []
    for section in REQUIRED_KICKOFF_SECTIONS - {"first_sprint_plan"}:
        values = sections.get(section, [])
        if not isinstance(values, list) or len(values) < 2:
            bad.append(section)
        elif any(len(str(value).strip()) < 25 for value in values):
            bad.append(section)
    _check_first_sprint_plan(sections.get("first_sprint_plan", []), bad)
    if not missing and not bad:
        _add_check(checks, "kickoff_sections", "pass", "Phase 8 kickoff sections are complete.")
    else:
        problems = []
        if missing:
            problems.append(f"missing sections: {', '.join(missing)}")
        if bad:
            problems.append(f"invalid sections: {', '.join(sorted(bad))}")
        _add_check(checks, "kickoff_sections", "blocker", f"Phase 8 kickoff sections invalid: {'; '.join(problems)}.")


def _check_first_sprint_plan(values: Any, bad: list[str]) -> None:
    if not isinstance(values, list):
        bad.append("first_sprint_plan")
        return
    by_id = {str(item.get("item_id")): item for item in values if isinstance(item, dict)}
    if REQUIRED_FIRST_SPRINT_ITEMS - set(by_id):
        bad.append("first_sprint_plan:item_ids")
    for item_id, item in by_id.items():
        if not _is_safe_ref(item.get("owner_ref")):
            bad.append(f"first_sprint_plan:{item_id}:owner_ref")
        if not _is_safe_ref(item.get("tracking_ref")):
            bad.append(f"first_sprint_plan:{item_id}:tracking_ref")
        tasks = item.get("acceptance_tasks", [])
        if not isinstance(tasks, list) or len(tasks) < 2:
            bad.append(f"first_sprint_plan:{item_id}:acceptance_tasks")
        elif any(len(str(task).strip()) < 20 for task in tasks):
            bad.append(f"first_sprint_plan:{item_id}:acceptance_tasks")


def _check_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "kickoff_controls", "blocker", "kickoff_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_KICKOFF_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "kickoff_controls",
        "pass" if not missing else "blocker",
        "Phase 8 kickoff controls are explicit."
        if not missing
        else f"Phase 8 kickoff controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_kickoff_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_KICKOFF_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_kickoff_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_kickoff_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
