from __future__ import annotations

import json
from pathlib import Path

from cavra.policy_lifecycle import (
    REQUIRED_DRY_RUN_CASES,
    build_policy_approval_workflow,
    build_policy_dry_run_report,
    build_policy_lifecycle_plan,
    build_policy_rollback_plan,
    build_policy_shadow_mode_plan,
    build_policy_version_manifest,
    lint_policy_lifecycle,
    validate_policy_lifecycle_packet,
    write_policy_lifecycle_artifacts,
)
from cavra.policy_registry import PolicyRegistry

SAMPLE_PACKET = Path("examples/policy-lifecycle/enterprise-policy-lifecycle.sample.json")
LIVE_PACKET = Path("examples/policy-lifecycle/enterprise-policy-lifecycle.live.sanitized.example.json")


def _baseline_policy() -> dict:
    return PolicyRegistry().load_policy("cavra-ai-agent-baseline")


def test_policy_lifecycle_lint_accepts_baseline_policy() -> None:
    report = lint_policy_lifecycle(_baseline_policy())

    assert report["valid"] is True
    assert report["blocker_count"] == 0
    assert report["summary"]["policy_id"] == "cavra-ai-agent-baseline"


def test_policy_lifecycle_lint_blocks_invalid_draft() -> None:
    report = lint_policy_lifecycle({"metadata": {"id": "bad"}})

    assert report["valid"] is False
    assert report["blocker_count"] >= 1
    assert any(issue["code"] == "policy.controls.missing" for issue in report["issues"])


def test_policy_version_manifest_is_digest_backed_and_git_versioned() -> None:
    policy = _baseline_policy()
    manifest = build_policy_version_manifest(policy, source_ref="git://example/policies")

    assert manifest["policy_digest"].startswith("sha256:")
    assert manifest["policy_version"] == "0.1.0"
    assert manifest["source_ref"] == "git://example/policies"
    assert manifest["git_versioned"] is True


def test_policy_dry_run_report_covers_required_runtime_decisions() -> None:
    report = build_policy_dry_run_report(_baseline_policy(), policy_pack="cavra-ai-agent-baseline")

    assert report["failed_count"] == 0
    assert report["required_cases_present"] is True
    assert REQUIRED_DRY_RUN_CASES <= {item["case_id"] for item in report["results"]}


def test_policy_shadow_mode_plan_is_non_enforcing_and_promotion_gated() -> None:
    plan = build_policy_shadow_mode_plan(_baseline_policy(), policy_pack="cavra-ai-agent-baseline")

    assert plan["mode"] == "shadow"
    assert plan["non_enforcing"] is True
    assert plan["promotion_criteria"]["approval_required"] is True


def test_policy_rollback_plan_requires_approval() -> None:
    policy = _baseline_policy()
    plan = build_policy_rollback_plan(
        current_policy=policy,
        previous_policy=policy,
        reason="rollback drill",
        requested_by="security@example.com",
    )

    assert plan["approval_required"] is True
    assert plan["rollback_ref"].startswith("policy-rollback://")
    assert len(plan["steps"]) >= 4


def test_policy_approval_workflow_contains_publish_decision() -> None:
    workflow = build_policy_approval_workflow(_baseline_policy(), requested_by="platform@example.com")

    assert workflow["approval_required"] is True
    assert workflow["publish_decision"]["decision"] == "require_approval"
    assert "dry_run_report" in workflow["required_evidence"]


def test_policy_lifecycle_plan_export_writes_expected_artifacts(tmp_path: Path) -> None:
    plan = build_policy_lifecycle_plan(_baseline_policy(), policy_pack="cavra-ai-agent-baseline")
    result = write_policy_lifecycle_artifacts(plan, tmp_path)

    assert Path(result["artifacts"]["policy_lifecycle_plan"]).exists()
    assert Path(result["artifacts"]["lint_report"]).exists()
    assert Path(result["artifacts"]["version_manifest"]).exists()
    assert Path(result["artifacts"]["dry_run_report"]).exists()
    assert Path(result["artifacts"]["approval_workflow"]).exists()


def test_sample_policy_lifecycle_packet_validates_with_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_policy_lifecycle_packet(packet)

    assert result["ready_for_policy_lifecycle_contract"] is True
    assert result["ready_for_live_policy_lifecycle"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1


def test_live_policy_lifecycle_packet_passes_live_gate() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))

    result = validate_policy_lifecycle_packet(packet, require_live=True)

    assert result["ready_for_live_policy_lifecycle"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0


def test_policy_lifecycle_packet_blocks_missing_controls() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))
    packet["lifecycle_capabilities"] = []
    packet["dry_run_report"]["failed_count"] = 1
    packet["operating_evidence"]["ci_run_ref"] = ""

    result = validate_policy_lifecycle_packet(packet, require_live=True)
    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}

    assert {"lifecycle_capabilities", "dry_run_report", "operating_evidence"} <= blocker_names
    assert result["ready_for_live_policy_lifecycle"] is False
