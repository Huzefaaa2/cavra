from pathlib import Path

from cavra.runtime import RuntimeGuard, summarize_policy_mode


def test_runtime_guard_blocks_sensitive_read() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    decision = guard.evaluate_file_access(Path(".env"), "read")
    assert decision.decision == "block"
    assert decision.policy_pack == "cavra-ai-agent-baseline"


def test_runtime_guard_blocks_terraform_apply() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    decision = guard.evaluate_command("terraform apply -auto-approve")
    assert decision.decision == "block"


def test_runtime_guard_allows_terraform_plan() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    decision = guard.evaluate_command("terraform plan")
    assert decision.decision == "allow"


def test_runtime_guard_requires_approval_for_unknown_command() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    decision = guard.evaluate_command("rm -rf /tmp/important")
    assert decision.decision == "require_approval"


def test_runtime_guard_requires_approval_for_iam_write() -> None:
    guard = RuntimeGuard(policy_pack="cavra-banking-baseline")
    decision = guard.evaluate_file_access(Path("iam/admin-role.tf"), "write")
    assert decision.decision == "require_approval"


def test_runtime_guard_blocks_unknown_mcp_server() -> None:
    guard = RuntimeGuard(policy_pack="cavra-mcp-enterprise")
    decision = guard.evaluate_mcp_tool_call("unknown-filesystem", "read_file", "filesystem")
    assert decision.decision == "block"


def test_runtime_guard_blocks_push_to_main() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    decision = guard.evaluate_git_action("push", "origin/main")
    assert decision.decision == "block"


def test_policy_mode_summary_audit_only_records_without_enforcing() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    decision = guard.evaluate_command("terraform apply -auto-approve")
    summary = summarize_policy_mode(decision, "audit_only")
    assert summary["base_decision"]["decision"] == "block"
    assert summary["effective_decision"] == "audit_only"
    assert summary["evidence_required"] is True


def test_policy_mode_summary_break_glass_requires_actor_and_reason() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    decision = guard.evaluate_command("terraform apply -auto-approve")

    blocked = summarize_policy_mode(decision, "break_glass")
    allowed = summarize_policy_mode(
        decision,
        "break_glass",
        break_glass_actor="incident-commander",
        break_glass_reason="Production recovery",
    )

    assert blocked["effective_decision"] == "block"
    assert allowed["effective_decision"] == "allow_with_attestation"
