# Agent Registry and MCP Trust Registry

Phase 5 starts the governed identity layer for AI agents and MCP servers.

## Current Implementation

- JSON-backed registry store for self-hosted pilots.
- Governed agent identities with agent ID, type, vendor, version, capabilities, scopes, allowed repositories, allowed tools, risk tier, owner, status, last seen, and evidence references.
- MCP server trust records with server ID, trust tier, capabilities, owner, approval state, approved tools, last seen, and evidence references.
- API endpoints for agents, MCP servers, and MCP trust evaluation.
- CLI commands for registering, listing, and checking registry records.
- Runtime MCP decisions can use registry trust state.
- Unknown MCP servers are blocked by default.

## CLI

```bash
cavra registry agent-register codex-agent --vendor OpenAI --capability code_edit --repository payments/api --owner "Platform AI"
cavra registry agent-list --owner "Platform AI"
cavra registry mcp-register github-mcp --trust-tier approved --approval-state approved --capability repository --tool create_pull_request --owner "Developer Platform"
cavra registry mcp-list --trust-tier approved
cavra registry mcp-check github-mcp create_pull_request --capability repository
```

## API

- `GET /agents`
- `POST /agents`
- `GET /agents/{agent_id}`
- `GET /mcp/servers`
- `POST /mcp/servers`
- `GET /mcp/servers/{server_id}`
- `GET /mcp/trust`

Set `CAVRA_REGISTRY_STORE` to choose the registry JSON path.

## User Stories

- As an AI governance lead, I can see which agents are active and what they are allowed to do.
- As a platform engineer, I can approve trusted MCP servers once and reuse that trust across repositories.
- As a security engineer, I can keep unknown MCP servers blocked by default.
- As an auditor, I can review owner, capability, approval state, and evidence metadata for agent and MCP trust decisions.

## Enterprise Challenge Solved

The registry removes identity ambiguity and MCP tool sprawl. Agents and tools become governed records with owners, scopes, approval state, and runtime decision impact.

## Next

- SQLite registry persistence and migrations.
- Console registry views.
- Predefined agent capability profiles for Claude Code, Codex, Copilot, Cursor, Gemini CLI, and AWS Q Developer.
- MCP tool classification for filesystem, shell, network, database, SaaS, and cloud.
