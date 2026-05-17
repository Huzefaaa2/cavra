from pathlib import Path

from cavra.registry import RegistryStore, evaluate_mcp_registry_trust
from cavra.runtime import RuntimeGuard


def test_registry_store_upserts_agent_and_mcp_server(tmp_path: Path) -> None:
    store = RegistryStore(tmp_path / "registry.json")

    agent = store.upsert_agent(
        {
            "agent_id": "codex-agent",
            "vendor": "OpenAI",
            "capabilities": ["code_edit", "test"],
            "allowed_repositories": ["payments/api"],
            "owner": "Platform AI",
        }
    )
    server = store.upsert_mcp_server(
        {
            "server_id": "github-mcp",
            "trust_tier": "approved",
            "approval_state": "approved",
            "capabilities": ["repository"],
            "allowed_tools": ["create_pull_request"],
            "owner": "Developer Platform",
        }
    )

    assert agent["status"] == "active"
    assert store.list_agents(owner="Platform AI")["total"] == 1
    assert server["trust_tier"] == "approved"
    assert store.list_mcp_servers(capability="repository")["total"] == 1


def test_mcp_registry_trust_allows_approved_server_scope(tmp_path: Path) -> None:
    store = RegistryStore(tmp_path / "registry.json")
    store.upsert_mcp_server(
        {
            "server_id": "github-mcp",
            "trust_tier": "approved",
            "approval_state": "approved",
            "capabilities": ["repository"],
            "allowed_tools": ["create_pull_request"],
        }
    )

    decision = store.evaluate_mcp("github-mcp", "create_pull_request", "repository")

    assert decision["decision"] == "allow"
    assert decision["rule_id"] == "mcp.registry.allow"


def test_mcp_registry_trust_requires_approval_for_tool_scope(tmp_path: Path) -> None:
    store = RegistryStore(tmp_path / "registry.json")
    store.upsert_mcp_server(
        {
            "server_id": "github-mcp",
            "trust_tier": "approved",
            "approval_state": "approved",
            "capabilities": ["repository"],
            "allowed_tools": ["create_pull_request"],
        }
    )

    decision = store.evaluate_mcp("github-mcp", "delete_repository", "repository")

    assert decision["decision"] == "require_approval"
    assert decision["approver_group"] == "AI Governance"


def test_mcp_registry_trust_blocks_denied_server() -> None:
    decision = evaluate_mcp_registry_trust(
        "unknown-filesystem",
        "read_file",
        "filesystem",
        {
            "server_id": "unknown-filesystem",
            "trust_tier": "blocked",
            "approval_state": "denied",
        },
    )

    assert decision["decision"] == "block"


def test_runtime_guard_uses_registry_for_mcp_decisions(tmp_path: Path) -> None:
    store = RegistryStore(tmp_path / "registry.json")
    store.upsert_mcp_server(
        {
            "server_id": "github-mcp",
            "trust_tier": "approved",
            "approval_state": "approved",
            "capabilities": ["repository"],
            "allowed_tools": ["create_pull_request"],
        }
    )
    guard = RuntimeGuard(policy_pack="cavra-mcp-enterprise", registry_store=store)

    allowed = guard.evaluate_mcp_tool_call("github-mcp", "create_pull_request", "repository")
    blocked = guard.evaluate_mcp_tool_call("unknown-filesystem", "read_file", "filesystem")

    assert allowed.decision == "allow"
    assert allowed.rule_id == "mcp.registry.allow"
    assert blocked.decision == "block"
    assert blocked.rule_id == "mcp.registry.unknown"
