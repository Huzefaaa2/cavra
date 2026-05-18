from pathlib import Path

from cavra.policy_registry import PolicyRegistry
from cavra.policy_engine import (
    diff_policies,
    load_policy_file,
    validate_policy,
    verify_policy_signature,
    write_policy_signature,
)


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


def test_all_repository_policy_packs_validate() -> None:
    root = Path(__file__).resolve().parents[1] / "policies"
    registry = PolicyRegistry(root=root)
    for pack in registry.list_policy_packs():
        errors = validate_policy(pack["policy"])
        assert errors == []


def test_policy_inheritance_merges_parent_rules(tmp_path: Path) -> None:
    parent = tmp_path / "cavra-parent"
    child = tmp_path / "cavra-child"
    parent.mkdir()
    child.mkdir()
    parent.joinpath("policy.yaml").write_text(
        """
metadata:
  id: cavra-parent
  title: Parent
  description: Parent policy
  version: 1
filesystem:
  block_read:
    - ".env"
commands:
  allow:
    - "terraform plan*"
""",
        encoding="utf-8",
    )
    child.joinpath("policy.yaml").write_text(
        """
metadata:
  id: cavra-child
  title: Child
  description: Child policy
  version: 1
  inherits: cavra-parent
filesystem:
  block_read:
    - "**/secrets.*"
commands:
  block:
    - "terraform apply*"
""",
        encoding="utf-8",
    )
    policy = PolicyRegistry(root=tmp_path).load_policy("cavra-child")
    assert policy["filesystem"]["block_read"] == ["**/secrets.*", ".env"]
    assert policy["commands"]["allow"] == ["terraform plan*"]
    assert policy["commands"]["block"] == ["terraform apply*"]


def test_policy_diff_reports_changed_paths() -> None:
    root = Path(__file__).resolve().parents[1] / "policies"
    left = load_policy_file(root / "cavra-ai-agent-baseline")
    right = load_policy_file(root / "cavra-banking-baseline")
    diff = diff_policies(left, right)
    assert "metadata.id" in diff.changed
    assert "git.require_pull_request" in diff.added


def test_policy_signature_round_trip(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(
        """
metadata:
  id: cavra-test-policy
  title: Test Policy
  description: Test policy
  version: 1
commands:
  allow:
    - "terraform plan*"
""",
        encoding="utf-8",
    )
    signature_path = write_policy_signature(policy_path, signer="pytest", key="secret")
    ok, message = verify_policy_signature(policy_path, signature_path=signature_path, key="secret")
    assert ok, message
    policy_path.write_text(policy_path.read_text(encoding="utf-8") + "\nfilesystem: {}\n", encoding="utf-8")
    ok, message = verify_policy_signature(policy_path, signature_path=signature_path, key="secret")
    assert not ok
    assert "mismatch" in message
