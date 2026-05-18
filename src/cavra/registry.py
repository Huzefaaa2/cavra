from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AGENT_STATUSES = {"active", "disabled", "retired"}
MCP_TRUST_TIERS = {"trusted", "approved", "experimental", "blocked", "unknown"}
APPROVAL_STATES = {"approved", "pending", "denied", "not_required"}


AGENT_CAPABILITY_PROFILES: list[dict[str, Any]] = [
    {
        "profile_id": "claude-code",
        "display_name": "Claude Code",
        "vendor": "Anthropic",
        "type": "coding-agent",
        "default_capabilities": ["code_edit", "test", "shell", "mcp_tool_call", "pull_request_attestation"],
        "default_scopes": ["repository", "filesystem", "shell", "mcp"],
        "recommended_tools": ["cavra-mcp-server", "git", "pytest", "ruff"],
        "risk_tier": "high",
        "enterprise_controls": ["mcp_trust_registry", "command_policy", "evidence_attestation", "approval_router"],
    },
    {
        "profile_id": "codex",
        "display_name": "OpenAI Codex",
        "vendor": "OpenAI",
        "type": "coding-agent",
        "default_capabilities": ["code_edit", "test", "shell", "git_operation", "pull_request_attestation"],
        "default_scopes": ["repository", "filesystem", "shell", "git"],
        "recommended_tools": ["cavra", "git", "pytest", "node"],
        "risk_tier": "high",
        "enterprise_controls": ["agent_registry", "protected_branch_policy", "evidence_attestation", "approval_router"],
    },
    {
        "profile_id": "github-copilot",
        "display_name": "GitHub Copilot Agent",
        "vendor": "GitHub",
        "type": "coding-agent",
        "default_capabilities": ["code_edit", "test", "pull_request", "workflow_assistance"],
        "default_scopes": ["repository", "git", "ci"],
        "recommended_tools": ["github-actions", "cavra-pr-attestation"],
        "risk_tier": "medium",
        "enterprise_controls": ["protected_branch_policy", "workflow_change_approval", "pr_attestation"],
    },
    {
        "profile_id": "cursor",
        "display_name": "Cursor Agent",
        "vendor": "Cursor",
        "type": "coding-agent",
        "default_capabilities": ["code_edit", "test", "shell", "repository_search"],
        "default_scopes": ["repository", "filesystem", "shell"],
        "recommended_tools": ["cavra", "git", "test_runner"],
        "risk_tier": "medium",
        "enterprise_controls": ["filesystem_policy", "command_policy", "evidence_attestation"],
    },
    {
        "profile_id": "gemini-cli",
        "display_name": "Gemini CLI",
        "vendor": "Google",
        "type": "coding-agent",
        "default_capabilities": ["code_edit", "test", "shell", "cloud_assistance"],
        "default_scopes": ["repository", "filesystem", "shell", "cloud"],
        "recommended_tools": ["cavra", "gcloud", "pytest"],
        "risk_tier": "high",
        "enterprise_controls": ["cloud_iam_policy", "command_policy", "approval_router", "evidence_attestation"],
    },
    {
        "profile_id": "aws-q-developer",
        "display_name": "AWS Q Developer",
        "vendor": "AWS",
        "type": "coding-agent",
        "default_capabilities": ["code_edit", "test", "shell", "cloud_assistance", "iam_review"],
        "default_scopes": ["repository", "filesystem", "shell", "aws"],
        "recommended_tools": ["cavra", "aws", "terraform"],
        "risk_tier": "high",
        "enterprise_controls": ["cloud_iam_policy", "terraform_policy", "approval_router", "evidence_attestation"],
    },
]


MCP_TOOL_CLASSIFICATIONS: list[dict[str, Any]] = [
    {
        "capability": "filesystem",
        "category": "local_resource",
        "risk_tier": "high",
        "default_decision": "block_unknown",
        "approval_required_for": ["write_file", "delete_file", "read_secret"],
        "example_tools": ["read_file", "write_file", "list_directory"],
        "control_objective": "Prevent unapproved file and secret access from tool-expanded agents.",
    },
    {
        "capability": "shell",
        "category": "execution",
        "risk_tier": "critical",
        "default_decision": "require_approval",
        "approval_required_for": ["execute_command", "install_package", "spawn_process"],
        "example_tools": ["run_command", "shell_exec"],
        "control_objective": "Route command execution through policy, evidence, and approval gates.",
    },
    {
        "capability": "network",
        "category": "egress",
        "risk_tier": "medium",
        "default_decision": "require_approval",
        "approval_required_for": ["external_post", "download_binary", "webhook_call"],
        "example_tools": ["fetch_url", "http_request"],
        "control_objective": "Control data egress and supply-chain download paths.",
    },
    {
        "capability": "database",
        "category": "data_access",
        "risk_tier": "high",
        "default_decision": "require_approval",
        "approval_required_for": ["write_query", "schema_change", "export_table"],
        "example_tools": ["query", "execute_sql", "inspect_schema"],
        "control_objective": "Protect regulated data stores from autonomous reads and writes.",
    },
    {
        "capability": "saas",
        "category": "enterprise_workflow",
        "risk_tier": "medium",
        "default_decision": "approved_server_scope",
        "approval_required_for": ["ticket_transition", "user_permission_change", "bulk_export"],
        "example_tools": ["create_issue", "update_ticket", "post_message"],
        "control_objective": "Keep workflow automation scoped to approved tools and owners.",
    },
    {
        "capability": "cloud",
        "category": "infrastructure",
        "risk_tier": "critical",
        "default_decision": "require_approval",
        "approval_required_for": ["iam_change", "production_deploy", "resource_delete"],
        "example_tools": ["apply_terraform", "update_iam_policy", "delete_resource"],
        "control_objective": "Prevent unapproved production, IAM, and cloud control-plane changes.",
    },
    {
        "capability": "repository",
        "category": "source_control",
        "risk_tier": "medium",
        "default_decision": "approved_server_scope",
        "approval_required_for": ["delete_repository", "change_branch_protection", "workflow_write"],
        "example_tools": ["create_pull_request", "create_issue", "list_branches"],
        "control_objective": "Govern source-control automation with protected-branch and workflow controls.",
    },
]


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


def default_agent_profiles() -> dict[str, Any]:
    items = sorted((dict(item) for item in AGENT_CAPABILITY_PROFILES), key=lambda item: item["profile_id"])
    return {"items": items, "total": len(items)}


def default_mcp_tool_classifications() -> dict[str, Any]:
    items = sorted((dict(item) for item in MCP_TOOL_CLASSIFICATIONS), key=lambda item: item["capability"])
    return {"items": items, "total": len(items)}


def classify_mcp_capability(capability: str) -> dict[str, Any] | None:
    normalized = capability.strip().lower()
    return next((dict(item) for item in MCP_TOOL_CLASSIFICATIONS if item["capability"] == normalized), None)


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


class SQLiteRegistryStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS registry_agents (
                  agent_id TEXT PRIMARY KEY,
                  status TEXT NOT NULL,
                  owner TEXT,
                  vendor TEXT,
                  risk_tier TEXT,
                  last_seen TEXT,
                  updated_at TEXT NOT NULL,
                  payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_registry_agents_status ON registry_agents (status)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_registry_agents_owner ON registry_agents (owner)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_registry_agents_updated_at ON registry_agents (updated_at)")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS registry_mcp_servers (
                  server_id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  trust_tier TEXT NOT NULL,
                  approval_state TEXT NOT NULL,
                  owner TEXT,
                  capabilities TEXT NOT NULL,
                  allowed_tools TEXT NOT NULL,
                  last_seen TEXT,
                  updated_at TEXT NOT NULL,
                  payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_registry_mcp_trust_tier ON registry_mcp_servers (trust_tier)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_registry_mcp_approval_state ON registry_mcp_servers (approval_state)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_registry_mcp_owner ON registry_mcp_servers (owner)")

    def list_agents(self, *, status: str | None = None, owner: str | None = None) -> dict[str, Any]:
        clauses: list[str] = []
        params: list[Any] = []
        if status:
            clauses.append("status = ?")
            params.append(status)
        if owner:
            clauses.append("owner = ?")
            params.append(owner)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._connect() as connection:
            rows = connection.execute(
                f"SELECT payload FROM registry_agents {where} ORDER BY agent_id ASC",
                params,
            ).fetchall()
        agents = [json.loads(row["payload"]) for row in rows]
        return {"items": agents, "total": len(agents)}

    def upsert_agent(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_agent_record(payload)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO registry_agents (agent_id, status, owner, vendor, risk_tier, last_seen, updated_at, payload)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(agent_id) DO UPDATE SET
                  status=excluded.status,
                  owner=excluded.owner,
                  vendor=excluded.vendor,
                  risk_tier=excluded.risk_tier,
                  last_seen=excluded.last_seen,
                  updated_at=excluded.updated_at,
                  payload=excluded.payload
                """,
                (
                    record["agent_id"],
                    record["status"],
                    record["owner"],
                    record["vendor"],
                    record["risk_tier"],
                    record["last_seen"],
                    record["updated_at"],
                    json.dumps(record, sort_keys=True),
                ),
            )
        return record

    def get_agent(self, agent_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload FROM registry_agents WHERE agent_id = ?", (agent_id,)).fetchone()
        return json.loads(row["payload"]) if row else None

    def list_mcp_servers(
        self,
        *,
        trust_tier: str | None = None,
        approval_state: str | None = None,
        capability: str | None = None,
    ) -> dict[str, Any]:
        clauses: list[str] = []
        params: list[Any] = []
        if trust_tier:
            clauses.append("trust_tier = ?")
            params.append(trust_tier)
        if approval_state:
            clauses.append("approval_state = ?")
            params.append(approval_state)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._connect() as connection:
            rows = connection.execute(
                f"SELECT payload FROM registry_mcp_servers {where} ORDER BY server_id ASC",
                params,
            ).fetchall()
        servers = [json.loads(row["payload"]) for row in rows]
        if capability:
            servers = [item for item in servers if capability in item.get("capabilities", [])]
        return {"items": servers, "total": len(servers)}

    def upsert_mcp_server(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_mcp_server_record(payload)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO registry_mcp_servers (
                  server_id, name, trust_tier, approval_state, owner, capabilities, allowed_tools, last_seen, updated_at, payload
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(server_id) DO UPDATE SET
                  name=excluded.name,
                  trust_tier=excluded.trust_tier,
                  approval_state=excluded.approval_state,
                  owner=excluded.owner,
                  capabilities=excluded.capabilities,
                  allowed_tools=excluded.allowed_tools,
                  last_seen=excluded.last_seen,
                  updated_at=excluded.updated_at,
                  payload=excluded.payload
                """,
                (
                    record["server_id"],
                    record["name"],
                    record["trust_tier"],
                    record["approval_state"],
                    record["owner"],
                    json.dumps(record["capabilities"], sort_keys=True),
                    json.dumps(record["allowed_tools"], sort_keys=True),
                    record["last_seen"],
                    record["updated_at"],
                    json.dumps(record, sort_keys=True),
                ),
            )
        return record

    def get_mcp_server(self, server_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM registry_mcp_servers WHERE server_id = ? OR name = ?",
                (server_id, server_id),
            ).fetchone()
        return json.loads(row["payload"]) if row else None

    def evaluate_mcp(self, server: str, tool: str, capability: str | None = None) -> dict[str, Any]:
        return evaluate_mcp_registry_trust(server, tool, capability, self.get_mcp_server(server))


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    raise ValueError("expected a string or list of strings")
