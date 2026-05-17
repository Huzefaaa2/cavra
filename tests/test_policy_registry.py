from pathlib import Path

from cavra.policy_registry import PolicyRegistry


def test_list_policy_packs() -> None:
    root = Path(__file__).resolve().parents[1] / "policies"
    registry = PolicyRegistry(root=root)
    packs = registry.list_policy_packs()
    assert any(pack["id"] == "cavra-ai-agent-baseline" for pack in packs)
    assert any(pack["id"] == "cavra-banking-baseline" for pack in packs)


def test_get_policy_pack() -> None:
    root = Path(__file__).resolve().parents[1] / "policies"
    registry = PolicyRegistry(root=root)
    pack = registry.get_policy_pack("cavra-ai-agent-baseline")
    assert pack["title"] == "CAVRA AI Agent Baseline"
    assert "policy" in pack and "filesystem" in pack["policy"]
