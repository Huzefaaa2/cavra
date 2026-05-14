from pathlib import Path

from terraguard_agentshield.policy_registry import PolicyRegistry
from terraguard_agentshield.runtime import RuntimeGuard


def test_runtime_guard_blocks_sensitive_read() -> None:
    registry = PolicyRegistry(root=Path(__file__).resolve().parents[1] / "policies")
    guard = RuntimeGuard(policy_pack="ai-agent-baseline")
    decision = guard.evaluate_file_access(Path(".env"), "read")
    assert decision.decision == "block"


def test_runtime_guard_blocks_terraform_apply() -> None:
    guard = RuntimeGuard(policy_pack="ai-agent-baseline")
    decision = guard.evaluate_command("terraform apply -auto-approve")
    assert decision.decision == "block"


def test_runtime_guard_requires_approval_for_unknown_command() -> None:
    guard = RuntimeGuard(policy_pack="ai-agent-baseline")
    decision = guard.evaluate_command("rm -rf /tmp/important")
    assert decision.decision == "require_approval"
