from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_lifecycle_phase8_kickoff import (
    build_customer_lifecycle_phase8_kickoff_packet,
    validate_customer_lifecycle_phase8_kickoff_packet,
)
from cavra.customer_live_evidence import (
    ALLOWED_REF_PREFIXES,
    find_forbidden_live_evidence_fields,
)


CUSTOMER_LIFECYCLE_PHASE8_SPRINT1_CHECKPOINT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-sprint1-checkpoint.packet.v1"
)
CUSTOMER_LIFECYCLE_PHASE8_SPRINT1_CHECKPOINT_RESULT_SCHEMA = (
    "cavra.customer-lifecycle-phase8-sprint1-checkpoint.result.v1"
)

REQUIRED_CHECKPOINT_OWNER_REFS = {
    "program_owner_ref",
    "product_owner_ref",
    "engineering_owner_ref",
    "security_owner_ref",
    "support_owner_ref",
}

REQUIRED_SPRINT_PROGRESS_ITEMS = {
    "phase8-telemetry-depth",
    "phase8-support-automation",
    "phase8-analytics",
}

REQUIRED_CHECKPOINT_SECTIONS = {
    "sprint_progress",
    "blocker_review",
    "evidence_summary",
    "next_checkpoint_plan",
}

REQUIRED_CHECKPOINT_CONTROLS = {
    "kickoff_ready",
    "progress_updates_recorded",
    "blockers_triaged",
    "next_checkpoint_defined",
    "evidence_boundary_confirmed",
    "no_private_material_embedded",
    "no_customer_identity_embedded",
    "no_commercial_terms_embedded",
}

ALLOWED_PROGRESS_STATUSES = {"on_track", "watch", "blocked"}

FORBIDDEN_PHASE8_SPRINT1_FIELDS = {
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


def build_customer_lifecycle_phase8_sprint1_checkpoint_packet(
    kickoff_packet: dict[str, Any] | None = None,
    *,
    repo_root: Path | None = None,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    kickoff = kickoff_packet or build_customer_lifecycle_phase8_kickoff_packet(
        repo_root=root,
        evidence_mode=evidence_mode,
    )
    kickoff_result = validate_customer_lifecycle_phase8_kickoff_packet(
        kickoff,
        require_live=evidence_mode == "live",
    )
    prefix = _prefix(evidence_mode)
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_SPRINT1_CHECKPOINT_SCHEMA,
        "product": "CAVRA",
        "phase": "R8",
        "source_phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "checkpoint_id": f"cavra-{evidence_mode}-customer-lifecycle-phase8-sprint1-checkpoint",
        "kickoff_ref": f"{prefix}://customer-lifecycle-phase8-kickoff/r7",
        "kickoff_result": kickoff_result,
        "checkpoint_owner_refs": {
            "program_owner_ref": f"{prefix}://owner/customer-lifecycle-program",
            "product_owner_ref": f"{prefix}://owner/product-management",
            "engineering_owner_ref": f"{prefix}://owner/engineering-delivery",
            "security_owner_ref": f"{prefix}://owner/security-platform",
            "support_owner_ref": f"{prefix}://owner/support",
        },
        "checkpoint_sections": {
            "sprint_progress": [
                _progress_item(
                    "phase8-telemetry-depth",
                    "on_track",
                    f"{prefix}://owner/security-platform",
                    f"{prefix}://roadmap/phase8-telemetry-depth",
                    f"{prefix}://phase8/sprint1/telemetry-progress",
                    [
                        "Telemetry packet shape drafted for customer-safe runtime signals.",
                        "Live sanitized telemetry fixture scope identified.",
                    ],
                    ["Finalize CI validation gate for telemetry examples."],
                ),
                _progress_item(
                    "phase8-support-automation",
                    "watch",
                    f"{prefix}://owner/support",
                    f"{prefix}://roadmap/phase8-support-automation",
                    f"{prefix}://phase8/sprint1/support-progress",
                    [
                        "Support checkpoint packet responsibilities mapped.",
                        "Escalation and owner refs reviewed for public-safe representation.",
                    ],
                    ["Confirm automation trigger names in deployment-private workspace."],
                ),
                _progress_item(
                    "phase8-analytics",
                    "on_track",
                    f"{prefix}://owner/product-management",
                    f"{prefix}://roadmap/phase8-analytics",
                    f"{prefix}://phase8/sprint1/analytics-progress",
                    [
                        "Lifecycle analytics dimensions drafted for posture and adoption.",
                        "Dashboard-safe output categories reviewed with product owner.",
                    ],
                    ["Define cadence summary acceptance tests."],
                ),
            ],
            "blocker_review": {
                "open_blocker_count": 0,
                "triage_ref": f"{prefix}://phase8/sprint1/blocker-triage",
                "triage_summary": "No open blockers remain after Sprint 1 checkpoint triage.",
            },
            "evidence_summary": [
                "Progress evidence uses sanitized owner, roadmap, and checkpoint refs only.",
                "Deployment-private customer details remain outside the public packet.",
            ],
            "next_checkpoint_plan": [
                "Validate telemetry depth packet with live sanitized examples.",
                "Confirm support automation readiness and lifecycle analytics input contract.",
                "Update roadmap only after the next checkpoint gate passes.",
            ],
        },
        "checkpoint_controls": {
            "kickoff_ready": kickoff_result["blocker_count"] == 0,
            "progress_updates_recorded": True,
            "blockers_triaged": True,
            "next_checkpoint_defined": True,
            "evidence_boundary_confirmed": True,
            "no_private_material_embedded": True,
            "no_customer_identity_embedded": True,
            "no_commercial_terms_embedded": True,
        },
    }


def validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_SPRINT1_CHECKPOINT_SCHEMA else "blocker",
        "Customer lifecycle Phase 8 Sprint 1 checkpoint schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIFECYCLE_PHASE8_SPRINT1_CHECKPOINT_SCHEMA
        else f"Packet must use {CUSTOMER_LIFECYCLE_PHASE8_SPRINT1_CHECKPOINT_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_safe_ref(packet.get("kickoff_ref"), checks, "kickoff_ref")
    _check_kickoff_result(packet.get("kickoff_result", {}), checks, require_live=require_live)
    _check_required_refs(
        packet.get("checkpoint_owner_refs", {}),
        REQUIRED_CHECKPOINT_OWNER_REFS,
        checks,
        "checkpoint_owner_refs",
    )
    _check_checkpoint_sections(packet.get("checkpoint_sections", {}), checks)
    _check_controls(packet.get("checkpoint_controls", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet) | _find_forbidden_phase8_sprint1_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Phase 8 Sprint 1 checkpoint contains sanitized refs and customer-safe progress text only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_PHASE8_SPRINT1_CHECKPOINT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R8"),
        "source_phase": packet.get("source_phase", "R7"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_phase8_sprint1_checkpoint": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_phase8_sprint1_checkpoint_artifacts(
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=root, evidence_mode="sample")
    live = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(sample)
    live_result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-phase8-sprint1-checkpoint.sample.json",
        "live_sanitized_example": output_dir
        / "customer-lifecycle-phase8-sprint1-checkpoint.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-phase8-sprint1-checkpoint.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-phase8-sprint1-checkpoint.live.sanitized.result.json",
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
        "schema_version": "cavra.customer-lifecycle-phase8-sprint1-checkpoint.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_phase8_sprint1_checkpoint": live_result[
            "ready_for_customer_lifecycle_phase8_sprint1_checkpoint"
        ],
    }


def _progress_item(
    item_id: str,
    status: str,
    owner_ref: str,
    tracking_ref: str,
    evidence_ref: str,
    completed_tasks: list[str],
    open_tasks: list[str],
) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "status": status,
        "owner_ref": owner_ref,
        "tracking_ref": tracking_ref,
        "evidence_ref": evidence_ref,
        "completed_tasks": completed_tasks,
        "open_tasks": open_tasks,
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized Phase 8 Sprint 1 checkpoint supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample Phase 8 Sprint 1 checkpoint validates shape only.")
    else:
        _add_check(
            checks,
            "evidence_mode",
            "blocker",
            "Phase 8 Sprint 1 checkpoint requires evidence_mode=live and sanitized=true.",
        )


def _check_kickoff_result(result: Any, checks: list[dict[str, str]], *, require_live: bool) -> None:
    if not isinstance(result, dict):
        _add_check(checks, "kickoff_result", "blocker", "kickoff_result must be an object.")
        return
    ready = result.get("ready_for_customer_lifecycle_phase8_kickoff") is True
    blockers = int(result.get("blocker_count", 1))
    warnings = int(result.get("warning_count", 0))
    if ready and blockers == 0 and (not require_live or warnings == 0):
        _add_check(checks, "kickoff_result", "pass", "Source Phase 8 kickoff packet is ready.")
    elif not require_live and blockers == 0:
        _add_check(checks, "kickoff_result", "warn", "Source Phase 8 kickoff validates shape but is not live.")
    else:
        _add_check(checks, "kickoff_result", "blocker", "Source Phase 8 kickoff packet is not ready.")


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


def _check_checkpoint_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, dict):
        _add_check(checks, "checkpoint_sections", "blocker", "checkpoint_sections must be an object.")
        return
    missing = sorted(section for section in REQUIRED_CHECKPOINT_SECTIONS if section not in sections)
    bad: list[str] = []
    _check_sprint_progress(sections.get("sprint_progress", []), bad)
    _check_blocker_review(sections.get("blocker_review", {}), bad)
    for section in {"evidence_summary", "next_checkpoint_plan"}:
        values = sections.get(section, [])
        if not isinstance(values, list) or len(values) < 2:
            bad.append(section)
        elif any(len(str(value).strip()) < 25 for value in values):
            bad.append(section)
    if not missing and not bad:
        _add_check(checks, "checkpoint_sections", "pass", "Phase 8 Sprint 1 checkpoint sections are complete.")
    else:
        problems = []
        if missing:
            problems.append(f"missing sections: {', '.join(missing)}")
        if bad:
            problems.append(f"invalid sections: {', '.join(sorted(bad))}")
        _add_check(
            checks,
            "checkpoint_sections",
            "blocker",
            f"Phase 8 Sprint 1 checkpoint sections invalid: {'; '.join(problems)}.",
        )


def _check_sprint_progress(values: Any, bad: list[str]) -> None:
    if not isinstance(values, list):
        bad.append("sprint_progress")
        return
    by_id = {str(item.get("item_id")): item for item in values if isinstance(item, dict)}
    if REQUIRED_SPRINT_PROGRESS_ITEMS - set(by_id):
        bad.append("sprint_progress:item_ids")
    for item_id, item in by_id.items():
        if item.get("status") not in ALLOWED_PROGRESS_STATUSES or item.get("status") == "blocked":
            bad.append(f"sprint_progress:{item_id}:status")
        for ref_field in ("owner_ref", "tracking_ref", "evidence_ref"):
            if not _is_safe_ref(item.get(ref_field)):
                bad.append(f"sprint_progress:{item_id}:{ref_field}")
        completed = item.get("completed_tasks", [])
        open_tasks = item.get("open_tasks", [])
        if not isinstance(completed, list) or len(completed) < 2:
            bad.append(f"sprint_progress:{item_id}:completed_tasks")
        elif any(len(str(task).strip()) < 20 for task in completed):
            bad.append(f"sprint_progress:{item_id}:completed_tasks")
        if not isinstance(open_tasks, list) or not open_tasks:
            bad.append(f"sprint_progress:{item_id}:open_tasks")
        elif any(len(str(task).strip()) < 20 for task in open_tasks):
            bad.append(f"sprint_progress:{item_id}:open_tasks")


def _check_blocker_review(value: Any, bad: list[str]) -> None:
    if not isinstance(value, dict):
        bad.append("blocker_review")
        return
    if value.get("open_blocker_count") != 0:
        bad.append("blocker_review:open_blocker_count")
    if not _is_safe_ref(value.get("triage_ref")):
        bad.append("blocker_review:triage_ref")
    if len(str(value.get("triage_summary", "")).strip()) < 30:
        bad.append("blocker_review:triage_summary")


def _check_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "checkpoint_controls", "blocker", "checkpoint_controls must be an object.")
        return
    missing = sorted(control for control in REQUIRED_CHECKPOINT_CONTROLS if controls.get(control) is not True)
    _add_check(
        checks,
        "checkpoint_controls",
        "pass" if not missing else "blocker",
        "Phase 8 Sprint 1 checkpoint controls are explicit."
        if not missing
        else f"Phase 8 Sprint 1 checkpoint controls missing or false: {', '.join(missing)}.",
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


def _find_forbidden_phase8_sprint1_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_PHASE8_SPRINT1_FIELDS:
                found.add(path)
            found.update(_find_forbidden_phase8_sprint1_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_phase8_sprint1_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
