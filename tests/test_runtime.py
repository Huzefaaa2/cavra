from pathlib import Path

from cavra.policy_registry import PolicyRegistry
from cavra.runtime import RuntimeGuard


def test_runtime_guard_blocks_sensitive_read() -> None:
    registry = PolicyRegistry(root=Path(__file__).resolve().parents[1] / "policies")
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
