from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.opa_rego_policy import build_default_rego_parity_fixtures, evaluate_rego_compatible_policy
from cavra.policy_authoring import (
    build_policy_pack_publish_plan,
    build_policy_publish_decision,
    policy_content_digest,
    summarize_policy,
)
from cavra.policy_engine import diff_policies, validate_policy

POLICY_LIFECYCLE_PLAN_SCHEMA = "cavra.policy-lifecycle.plan.v1"
POLICY_LIFECYCLE_READINESS_SCHEMA = "cavra.policy-lifecycle.readiness.v1"
POLICY_LIFECYCLE_READINESS_RESULT_SCHEMA = "cavra.policy-lifecycle.readiness-result.v1"

REQUIRED_LIFECYCLE_CAPABILITIES = {
    "authoring_ui_contract",
    "lint_report",
    "version_manifest",
    "shadow_mode_plan",
    "dry_run_report",
    "rollback_plan",
    "approval_workflow",
}

REQUIRED_DRY_RUN_CASES = {
    "block_env_read",
    "approval_policy_write",
    "allow_terraform_plan",
    "block_terraform_apply",
    "block_protected_branch_push",
    "block_unknown_mcp_server",
}


def build_policy_lifecycle_plan(
    policy: dict[str, Any],
    *,
    previous_policy: dict[str, Any] | None = None,
    policy_pack: str | None = None,
    sample_actions: list[dict[str, Any]] | None = None,
    requested_by: str = "policy-owner@example.com",
    source_ref: str = "git://policy-catalog/main",
    review_workflow_ref: str = "github://Huzefaaa2/cavra/actions/workflows/policy-lifecycle.yml",
) -> dict[str, Any]:
    """Build a public-safe policy lifecycle plan without publishing policy changes."""
    policy_id = str(policy.get("metadata", {}).get("id", policy_pack or "policy-draft"))
    pack = policy_pack or policy_id
    lint_report = lint_policy_lifecycle(policy)
    version_manifest = build_policy_version_manifest(policy, previous_policy=previous_policy, source_ref=source_ref)
    dry_run_report = build_policy_dry_run_report(policy, actions=sample_actions, policy_pack=pack)
    return {
        "schema_version": POLICY_LIFECYCLE_PLAN_SCHEMA,
        "product": "CAVRA",
        "generated_at": _now(),
        "policy_pack": pack,
        "lifecycle_capabilities": sorted(REQUIRED_LIFECYCLE_CAPABILITIES),
        "authoring_ui_contract": build_authoring_ui_contract(policy_id=policy_id, review_workflow_ref=review_workflow_ref),
        "lint_report": lint_report,
        "version_manifest": version_manifest,
        "shadow_mode_plan": build_policy_shadow_mode_plan(policy, sample_actions=sample_actions, policy_pack=pack),
        "dry_run_report": dry_run_report,
        "rollback_plan": build_policy_rollback_plan(
            current_policy=policy,
            previous_policy=previous_policy,
            reason="Pre-approved rollback path for policy lifecycle rollout.",
            requested_by=requested_by,
        ),
        "approval_workflow": build_policy_approval_workflow(
            policy,
            previous_policy=previous_policy,
            requested_by=requested_by,
            review_workflow_ref=review_workflow_ref,
        ),
        "operator_notes": [
            "Lifecycle plan generation is read-only and does not publish policy changes.",
            "Use shadow mode and dry-run evidence before enforcing a new or changed policy pack.",
            "A live Enterprise rollout must attach UI validation, approval, rollback, and CI evidence.",
        ],
    }


def build_authoring_ui_contract(*, policy_id: str, review_workflow_ref: str) -> dict[str, Any]:
    return {
        "schema_version": "cavra.policy-lifecycle.authoring-ui-contract.v1",
        "policy_id": policy_id,
        "required_surfaces": [
            "draft_editor",
            "schema_lint",
            "semantic_diff",
            "dry_run_simulator",
            "shadow_mode_toggle",
            "approval_workflow_builder",
            "rollback_picker",
        ],
        "api_endpoints": [
            "POST /policy-packs/draft",
            "POST /policy-packs/publish-plan",
            "POST /policy-packs/publish-request",
            "POST /policy-rollouts/change-plan",
            "POST /policy-rollouts/apply-change",
        ],
        "review_workflow_ref": review_workflow_ref,
        "operator_notes": [
            "The public contract defines UI behavior; customer-specific UI screenshots are deployment evidence.",
            "Draft, publish, and rollout API calls are approval-gated and public-safe.",
        ],
    }


def lint_policy_lifecycle(policy: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    schema_errors = validate_policy(policy)
    for error in schema_errors:
        issues.append({"severity": "blocker", "code": "schema_error", "message": error})

    metadata = policy.get("metadata") if isinstance(policy.get("metadata"), dict) else {}
    for field in ("id", "title", "description", "version"):
        if not metadata.get(field):
            issues.append({"severity": "blocker", "code": f"metadata.{field}.missing", "message": f"metadata.{field} is required."})

    sections = {
        "filesystem": policy.get("filesystem"),
        "commands": policy.get("commands"),
        "git": policy.get("git"),
        "mcp": policy.get("mcp"),
        "approvals": policy.get("approvals"),
        "evidence": policy.get("evidence"),
    }
    if not any(isinstance(value, dict) and bool(value) for value in sections.values()):
        issues.append(
            {
                "severity": "blocker",
                "code": "policy.controls.missing",
                "message": "At least one policy control section must be populated.",
            }
        )

    _require_string_list(policy, issues, "filesystem", "block_read")
    _require_string_list(policy, issues, "filesystem", "block_write")
    _require_string_list(policy, issues, "filesystem", "require_approval_write")
    _require_string_list(policy, issues, "commands", "block")
    _require_string_list(policy, issues, "commands", "allow")
    _require_string_list(policy, issues, "mcp", "allowed_servers")
    _require_string_list(policy, issues, "mcp", "blocked_servers")

    commands = policy.get("commands") if isinstance(policy.get("commands"), dict) else {}
    if commands.get("block") and not commands.get("allow"):
        issues.append(
            {
                "severity": "warning",
                "code": "commands.allow.missing",
                "message": "Blocked commands are configured without an allow-list; dry runs may require extra approvals.",
            }
        )

    filesystem = policy.get("filesystem") if isinstance(policy.get("filesystem"), dict) else {}
    if not filesystem.get("block_read"):
        issues.append(
            {
                "severity": "warning",
                "code": "filesystem.block_read.missing",
                "message": "No sensitive read paths are blocked.",
            }
        )

    blocker_count = sum(1 for item in issues if item["severity"] == "blocker")
    warning_count = sum(1 for item in issues if item["severity"] == "warning")
    return {
        "schema_version": "cavra.policy-lifecycle.lint-report.v1",
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "issue_count": len(issues),
        "issues": issues,
        "summary": summarize_policy(policy) if blocker_count == 0 else _safe_policy_summary(policy),
    }


def build_policy_version_manifest(
    policy: dict[str, Any],
    *,
    previous_policy: dict[str, Any] | None = None,
    source_ref: str = "git://policy-catalog/main",
) -> dict[str, Any]:
    policy_id = str(policy.get("metadata", {}).get("id", "policy-draft"))
    version = str(policy.get("metadata", {}).get("version", "unknown"))
    diff = diff_policies(previous_policy, policy).to_dict() if previous_policy else {"added": [], "removed": [], "changed": []}
    return {
        "schema_version": "cavra.policy-lifecycle.version-manifest.v1",
        "policy_id": policy_id,
        "policy_version": version,
        "policy_digest": policy_content_digest(policy),
        "previous_policy_digest": policy_content_digest(previous_policy) if previous_policy else None,
        "source_ref": source_ref,
        "git_versioned": True,
        "generated_at": _now(),
        "diff": diff,
    }


def build_policy_shadow_mode_plan(
    policy: dict[str, Any],
    *,
    sample_actions: list[dict[str, Any]] | None = None,
    policy_pack: str = "policy-draft",
) -> dict[str, Any]:
    actions = sample_actions or build_default_rego_parity_fixtures()
    return {
        "schema_version": "cavra.policy-lifecycle.shadow-mode-plan.v1",
        "policy_pack": policy_pack,
        "mode": "shadow",
        "non_enforcing": True,
        "compare_against": "current_enforced_policy",
        "sample_case_ids": [str(item.get("case_id", f"case_{index + 1}")) for index, item in enumerate(actions)],
        "evidence_refs": [
            f"policy-shadow://{policy_pack}/{policy_content_digest(policy).removeprefix('sha256:')[:12]}",
            f"policy-dry-run://{policy_pack}/{policy_content_digest(policy).removeprefix('sha256:')[:12]}",
        ],
        "promotion_criteria": {
            "dry_run_failed_count": 0,
            "shadow_observation_hours": 24,
            "approval_required": True,
        },
    }


def build_policy_dry_run_report(
    policy: dict[str, Any],
    *,
    actions: list[dict[str, Any]] | None = None,
    policy_pack: str = "policy-draft",
) -> dict[str, Any]:
    fixtures = actions or build_default_rego_parity_fixtures()
    results = []
    for index, fixture in enumerate(fixtures):
        case_id = str(fixture.get("case_id", f"case_{index + 1}"))
        rego_input = fixture.get("input") if isinstance(fixture.get("input"), dict) else fixture
        expected = fixture.get("expected_decision")
        decision = evaluate_rego_compatible_policy(policy, rego_input)
        passed = expected is None or decision["decision"] == expected
        results.append(
            {
                "case_id": case_id,
                "input": rego_input,
                "expected_decision": expected,
                "decision": decision,
                "passed": passed,
            }
        )
    failed = [item for item in results if not item["passed"]]
    return {
        "schema_version": "cavra.policy-lifecycle.dry-run-report.v1",
        "policy_pack": policy_pack,
        "case_count": len(results),
        "passed_count": len(results) - len(failed),
        "failed_count": len(failed),
        "required_cases_present": REQUIRED_DRY_RUN_CASES <= {item["case_id"] for item in results},
        "passed": not failed and REQUIRED_DRY_RUN_CASES <= {item["case_id"] for item in results},
        "results": results,
    }


def build_policy_rollback_plan(
    *,
    current_policy: dict[str, Any],
    previous_policy: dict[str, Any] | None = None,
    reason: str,
    requested_by: str = "policy-owner@example.com",
) -> dict[str, Any]:
    current_id = str(current_policy.get("metadata", {}).get("id", "policy-draft"))
    previous_id = str((previous_policy or current_policy).get("metadata", {}).get("id", current_id))
    return {
        "schema_version": "cavra.policy-lifecycle.rollback-plan.v1",
        "rollback_ref": f"policy-rollback://{previous_id}/{policy_content_digest(previous_policy or current_policy).removeprefix('sha256:')[:12]}",
        "current_policy_id": current_id,
        "current_policy_digest": policy_content_digest(current_policy),
        "previous_policy_id": previous_id,
        "previous_policy_digest": policy_content_digest(previous_policy) if previous_policy else None,
        "approval_required": True,
        "requested_by": requested_by,
        "reason": reason,
        "diff": diff_policies(previous_policy, current_policy).to_dict() if previous_policy else {"added": [], "removed": [], "changed": []},
        "steps": [
            "Freeze new policy promotion.",
            "Restore previous policy YAML and signature from Git.",
            "Run dry-run and shadow comparison against rollback candidate.",
            "Obtain Platform Security approval.",
            "Publish rollback through policy catalog workflow.",
            "Attach rollback evidence bundle to the rollout record.",
        ],
    }


def build_policy_approval_workflow(
    policy: dict[str, Any],
    *,
    previous_policy: dict[str, Any] | None = None,
    requested_by: str = "policy-owner@example.com",
    approver_groups: list[str] | None = None,
    review_workflow_ref: str = "github://Huzefaaa2/cavra/actions/workflows/policy-lifecycle.yml",
) -> dict[str, Any]:
    publish_plan = build_policy_pack_publish_plan(_draft_payload_from_policy(policy), current_policy=previous_policy)
    primary_group = (approver_groups or ["Platform Security", "Repository Owners"])[0]
    decision = build_policy_publish_decision(
        publish_plan,
        requested_by=requested_by,
        approver_group=primary_group,
    )
    return {
        "schema_version": "cavra.policy-lifecycle.approval-workflow.v1",
        "review_workflow_ref": review_workflow_ref,
        "approval_required": True,
        "approver_groups": approver_groups or ["Platform Security", "Repository Owners"],
        "publish_plan": publish_plan,
        "publish_decision": decision,
        "required_evidence": [
            "lint_report",
            "version_manifest",
            "semantic_diff",
            "dry_run_report",
            "shadow_mode_observation",
            "rollback_plan",
        ],
        "review_checklist": [
            "Schema lint is clean.",
            "Diff is understood by policy owner and security reviewer.",
            "Dry-run decisions match expected outcomes.",
            "Shadow mode has no unexplained high-severity divergence.",
            "Rollback reference points to a known-good prior policy.",
        ],
    }


def validate_policy_lifecycle_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    blockers = 0
    warnings = 0

    blockers += _check(
        checks,
        packet.get("schema_version") == POLICY_LIFECYCLE_READINESS_SCHEMA,
        "schema_version",
        "Policy lifecycle evidence packet schema is valid.",
    )
    evidence_mode = str(packet.get("evidence_mode", "sample"))
    if evidence_mode == "live":
        _check(checks, True, "evidence_mode", "Live policy lifecycle evidence packet supplied.")
    elif require_live:
        blockers += _check(checks, False, "evidence_mode", "Live policy lifecycle evidence is required for this gate.")
    else:
        warnings += _warn(checks, "evidence_mode", "Sample policy lifecycle packet validates contract shape only.")

    capabilities = set(packet.get("lifecycle_capabilities", []))
    blockers += _check(
        checks,
        REQUIRED_LIFECYCLE_CAPABILITIES <= capabilities,
        "lifecycle_capabilities",
        "Required policy lifecycle capabilities are present.",
    )

    authoring = packet.get("authoring_ui_contract", {})
    blockers += _check(
        checks,
        bool(authoring.get("review_workflow_ref")) and len(authoring.get("required_surfaces", [])) >= 6,
        "authoring_ui_contract",
        "Authoring UI contract covers editor, lint, simulation, approval, and rollback surfaces.",
    )

    lint = packet.get("lint_report", {})
    blockers += _check(
        checks,
        bool(lint.get("valid")) and int(lint.get("blocker_count", 1)) == 0,
        "lint_report",
        "Policy lint has no blockers.",
    )

    version = packet.get("version_manifest", {})
    blockers += _check(
        checks,
        bool(version.get("policy_digest"))
        and bool(version.get("policy_version"))
        and bool(version.get("source_ref"))
        and bool(version.get("git_versioned")),
        "version_manifest",
        "Policy version manifest is digest-backed and Git-versioned.",
    )

    shadow = packet.get("shadow_mode_plan", {})
    blockers += _check(
        checks,
        shadow.get("mode") == "shadow"
        and bool(shadow.get("non_enforcing"))
        and bool(shadow.get("evidence_refs"))
        and bool(shadow.get("promotion_criteria", {}).get("approval_required")),
        "shadow_mode_plan",
        "Shadow mode plan is non-enforcing and promotion-gated.",
    )

    dry_run = packet.get("dry_run_report", {})
    case_ids = {str(item.get("case_id")) for item in dry_run.get("results", [])} if isinstance(dry_run, dict) else set()
    blockers += _check(
        checks,
        REQUIRED_DRY_RUN_CASES <= case_ids
        and int(dry_run.get("case_count", 0)) >= len(REQUIRED_DRY_RUN_CASES)
        and int(dry_run.get("failed_count", 1)) == 0,
        "dry_run_report",
        "Dry-run report covers required decisions with no failures.",
    )

    rollback = packet.get("rollback_plan", {})
    blockers += _check(
        checks,
        bool(rollback.get("rollback_ref"))
        and bool(rollback.get("approval_required"))
        and len(rollback.get("steps", [])) >= 4,
        "rollback_plan",
        "Rollback plan is approval-gated and executable.",
    )

    approval = packet.get("approval_workflow", {})
    blockers += _check(
        checks,
        bool(approval.get("approval_required"))
        and bool(approval.get("review_workflow_ref"))
        and bool(approval.get("approver_groups"))
        and "dry_run_report" in set(approval.get("required_evidence", [])),
        "approval_workflow",
        "Approval workflow requires reviewers and lifecycle evidence.",
    )

    operating = packet.get("operating_evidence", {})
    blockers += _check(
        checks,
        bool(operating.get("ci_run_ref"))
        and bool(operating.get("policy_review_ref"))
        and bool(operating.get("ui_validation_ref")),
        "operating_evidence",
        "Policy lifecycle operating evidence references are present.",
    )

    ready_contract = blockers == 0
    ready_live = ready_contract and evidence_mode == "live"
    return {
        "schema_version": POLICY_LIFECYCLE_READINESS_RESULT_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "ready_for_policy_lifecycle_contract": ready_contract,
        "ready_for_live_policy_lifecycle": ready_live,
        "status": "blocked" if blockers else ("ready_with_warnings" if warnings else "ready"),
        "blocker_count": blockers,
        "warning_count": warnings,
        "checks": checks,
    }


def write_policy_lifecycle_artifacts(plan: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_map = {
        "policy_lifecycle_plan": ("policy-lifecycle-plan.json", plan),
        "authoring_ui_contract": ("policy-authoring-ui-contract.json", plan["authoring_ui_contract"]),
        "lint_report": ("policy-lint-report.json", plan["lint_report"]),
        "version_manifest": ("policy-version-manifest.json", plan["version_manifest"]),
        "shadow_mode_plan": ("policy-shadow-mode-plan.json", plan["shadow_mode_plan"]),
        "dry_run_report": ("policy-dry-run-report.json", plan["dry_run_report"]),
        "rollback_plan": ("policy-rollback-plan.json", plan["rollback_plan"]),
        "approval_workflow": ("policy-approval-workflow.json", plan["approval_workflow"]),
    }
    artifacts: dict[str, str] = {}
    for key, (name, payload) in artifact_map.items():
        path = output_dir / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        artifacts[key] = str(path)
    return {
        "schema_version": "cavra.policy-lifecycle.export.v1",
        "output_dir": str(output_dir),
        "artifacts": artifacts,
    }


def _draft_payload_from_policy(policy: dict[str, Any]) -> dict[str, Any]:
    metadata = policy.get("metadata") if isinstance(policy.get("metadata"), dict) else {}
    payload: dict[str, Any] = {
        "id": metadata.get("id", "policy-draft"),
        "title": metadata.get("title", "Policy Draft"),
        "description": metadata.get("description", "Policy lifecycle draft."),
        "version": metadata.get("version", "0.0.0"),
    }
    if metadata.get("inherits"):
        payload["inherits"] = metadata["inherits"]
    if metadata.get("mode"):
        payload["mode"] = metadata["mode"]
    for section in ("filesystem", "commands", "git", "mcp", "approvals", "evidence", "compliance"):
        if isinstance(policy.get(section), dict):
            payload[section] = policy[section]
    return payload


def _require_string_list(policy: dict[str, Any], issues: list[dict[str, Any]], section: str, field: str) -> None:
    section_value = policy.get(section)
    if not isinstance(section_value, dict) or field not in section_value:
        return
    value = section_value[field]
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        issues.append(
            {
                "severity": "blocker",
                "code": f"{section}.{field}.invalid",
                "message": f"{section}.{field} must be a list of non-empty strings.",
            }
        )


def _safe_policy_summary(policy: dict[str, Any]) -> dict[str, Any]:
    metadata = policy.get("metadata") if isinstance(policy.get("metadata"), dict) else {}
    return {
        "policy_id": metadata.get("id"),
        "title": metadata.get("title"),
        "version": metadata.get("version"),
        "mode": metadata.get("mode", "enforce"),
    }


def _check(checks: list[dict[str, Any]], ok: bool, name: str, message: str) -> int:
    checks.append({"name": name, "status": "pass" if ok else "blocker", "message": message})
    return 0 if ok else 1


def _warn(checks: list[dict[str, Any]], name: str, message: str) -> int:
    checks.append({"name": name, "status": "warn", "message": message})
    return 1


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
