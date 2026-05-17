from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AGENT_STATUSES = {"active", "disabled", "retired"}
MCP_TRUST_TIERS = {"trusted", "approved", "experimental", "blocked", "unknown"}
APPROVAL_STATES = {"approved", "pending", "denied", "not_required"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_agent_record(payload: dict[str, Any]) -> dict[str, Any]:
    agent_id = payload.get("agent_id") or payload.get("id")
    if not agent_id:
        raise ValueError("agent record must include agent_id")
    status = str(payload.get("status", "active"))
    if status not in AGENT_STATUSES:
        raise ValueError(f"agent status must be one of: {', '.join(sorted(AGENT_STATUSES))}")
    now = utc_now()
    return {
        "schema_version": "cavra.agent.v1",
        "agent_id": str(agent_id),
        "type": str(payload.get("type", "coding-agent")),
        "vendor": payload.get("vendor", "unknown"),
        "version": payload.get("version", "unknown"),
        "capabilities": _string_list(payload.get("capabilities", [])),
        "scopes": _string_list(payload.get("scopes", [])),
        "allowed_repositories": _string_list(payload.get("allowed_repositories", [])),
        "allowed_tools": _string_list(payload.get("allowed_tools", [])),
        "risk_tier": payload.get("risk_tier", "medium"),
        "owner": payload.get("owner", "unassigned"),
        "status": status,
        "last_seen": payload.get("last_seen") or now,
        "created_at": payload.get("created_at") or now,
        "updated_at": now,
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
    }


def normalize_mcp_server_record(payload: dict[str, Any]) -> dict[str, Any]:
    server_id = payload.get("server_id") or payload.get("id") or payload.get("name")
    if not server_id:
        raise ValueError("MCP server record must include server_id")
    trust_tier = str(payload.get("trust_tier", "unknown"))
    approval_state = str(payload.get("approval_state", "pending" if trust_tier in {"unknown", "experimental"} else "approved"))
    if trust_tier not in MCP_TRUST_TIERS:
        raise ValueError(f"MCP trust_tier must be one of: {', '.join(sorted(MCP_TRUST_TIERS))}")
    if approval_state not in APPROVAL_STATES:
        raise ValueError(f"MCP approval_state must be one of: {', '.join(sorted(APPROVAL_STATES))}")
    now = utc_now()
    return {
        "schema_version": "cavra.mcp_server.v1",
        "server_id": str(server_id),
        "name": str(payload.get("name", server_id)),
        "trust_tier": trust_tier,
        "capabilities": _string_list(payload.get("capabilities", [])),
        "owner": payload.get("owner", "unassigned"),
        "approval_state": approval_state,
        "allowed_tools": _string_list(payload.get("allowed_tools", [])),
        "last_seen": payload.get("last_seen") or now,
        "created_at": payload.get("created_at") or now,
        "updated_at": now,
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
    }


def evaluate_mcp_registry_trust(
    server: str,
    tool: str,
    capability: str | None,
    record: dict[str, Any] | None,
    *,
    block_unknown: bool = True,
) -> dict[str, Any]:
    if record is None:
        decision = "block" if block_unknown else "require_approval"
        return {
            "decision": decision,
            "reason": "MCP server is not registered.",
            "rule_id": "mcp.registry.unknown",
            "severity": "high",
            "approver_group": "AI Governance" if decision == "require_approval" else None,
        }
    if record.get("trust_tier") == "blocked" or record.get("approval_state") == "denied":
        return {
            "decision": "block",
            "reason": "MCP server is blocked or denied in the trust registry.",
            "rule_id": "mcp.registry.blocked",
            "severity": "high",
            "approver_group": None,
        }
    if record.get("approval_state") == "pending" or record.get("trust_tier") in {"unknown", "experimental"}:
        return {
            "decision": "require_approval",
            "reason": "MCP server requires trust approval before use.",
            "rule_id": "mcp.registry.requires_approval",
            "severity": "medium",
            "approver_group": "AI Governance",
        }
    allowed_tools = set(record.get("allowed_tools", []))
    if allowed_tools and tool not in allowed_tools:
        return {
            "decision": "require_approval",
            "reason": "MCP tool is outside the server's approved tool scope.",
            "rule_id": "mcp.registry.tool_scope",
            "severity": "medium",
            "approver_group": "AI Governance",
        }
    capabilities = set(record.get("capabilities", []))
    if capability and capabilities and capability not in capabilities:
        return {
            "decision": "require_approval",
            "reason": "MCP capability is outside the server's approved capability scope.",
            "rule_id": "mcp.registry.capability_scope",
            "severity": "medium",
            "approver_group": "AI Governance",
        }
    return {
        "decision": "allow",
        "reason": "MCP server is approved in the trust registry.",
        "rule_id": "mcp.registry.allow",
        "severity": "low",
        "approver_group": None,
    }


class RegistryStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list_agents(self, *, status: str | None = None, owner: str | None = None) -> dict[str, Any]:
        agents = self._load()["agents"]
        if status:
            agents = [item for item in agents if item.get("status") == status]
        if owner:
            agents = [item for item in agents if item.get("owner") == owner]
        return {"items": sorted(agents, key=lambda item: item.get("agent_id", "")), "total": len(agents)}

    def upsert_agent(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_agent_record(payload)
        data = self._load()
        data["agents"] = [item for item in data["agents"] if item.get("agent_id") != record["agent_id"]]
        data["agents"].append(record)
        self._save(data)
        return record

    def get_agent(self, agent_id: str) -> dict[str, Any] | None:
        return next((item for item in self._load()["agents"] if item.get("agent_id") == agent_id), None)

    def list_mcp_servers(
        self,
        *,
        trust_tier: str | None = None,
        approval_state: str | None = None,
        capability: str | None = None,
    ) -> dict[str, Any]:
        servers = self._load()["mcp_servers"]
        if trust_tier:
            servers = [item for item in servers if item.get("trust_tier") == trust_tier]
        if approval_state:
            servers = [item for item in servers if item.get("approval_state") == approval_state]
        if capability:
            servers = [item for item in servers if capability in item.get("capabilities", [])]
        return {"items": sorted(servers, key=lambda item: item.get("server_id", "")), "total": len(servers)}

    def upsert_mcp_server(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_mcp_server_record(payload)
        data = self._load()
        data["mcp_servers"] = [item for item in data["mcp_servers"] if item.get("server_id") != record["server_id"]]
        data["mcp_servers"].append(record)
        self._save(data)
        return record

    def get_mcp_server(self, server_id: str) -> dict[str, Any] | None:
        return next(
            (
                item
                for item in self._load()["mcp_servers"]
                if item.get("server_id") == server_id or item.get("name") == server_id
            ),
            None,
        )

    def evaluate_mcp(self, server: str, tool: str, capability: str | None = None) -> dict[str, Any]:
        return evaluate_mcp_registry_trust(server, tool, capability, self.get_mcp_server(server))

    def _load(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists():
            return {"agents": [], "mcp_servers": []}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return {
            "agents": list(payload.get("agents", [])),
            "mcp_servers": list(payload.get("mcp_servers", [])),
        }

    def _save(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    raise ValueError("expected a string or list of strings")
