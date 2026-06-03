from __future__ import annotations

import json
from pathlib import Path

from cavra.runtime import RuntimeGuard, summarize_policy_mode


FIXTURE = Path(__file__).parent / "fixtures" / "golden_decisions" / "community_ga_control_hardening.json"
STABLE_FIELDS = (
    "action_type",
    "target",
    "requested_operation",
    "policy_pack",
    "policy_id",
    "rule_id",
    "decision",
    "severity",
    "approver_group",
)


def test_community_ga_control_hardening_golden_decisions() -> None:
    baseline = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    mcp = RuntimeGuard(policy_pack="cavra-mcp-enterprise")
    actual = [
        _stable("sensitive_env_read", baseline.evaluate_file_access(Path(".env"), "read").to_dict()),
        _stable("allowed_terraform_plan", baseline.evaluate_command("terraform plan").to_dict()),
        _stable("unknown_command_requires_review", baseline.evaluate_command("rm -rf /tmp/important").to_dict()),
        _stable("main_branch_push_blocked", baseline.evaluate_git_action("push", "origin/main").to_dict()),
        _stable("unknown_mcp_server_blocked", mcp.evaluate_mcp_tool_call("unknown-filesystem", "read_file", "filesystem").to_dict()),
    ]

    expected = json.loads(FIXTURE.read_text(encoding="utf-8"))

    assert actual == expected


def test_strict_mode_golden_effective_decision() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    summary = summarize_policy_mode(guard.evaluate_command("terraform plan"), "strict")

    assert summary["base_decision"]["decision"] == "allow"
    assert summary["effective_decision"] == "require_approval"
    assert summary["evidence_required"] is True


def _stable(name: str, decision: dict[str, object]) -> dict[str, object]:
    return {"name": name, **{field: decision[field] for field in STABLE_FIELDS}}
