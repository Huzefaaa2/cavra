# Agent Identity

The Agent Registry tracks governed AI-agent identities with `agent_id`, type, vendor, version, capabilities, scopes, allowed repositories, allowed tools, risk tier, owner, status, last seen, and evidence references.

The registry supports JSON for local pilots and SQLite for self-hosted API deployments:

```bash
cavra registry agent-register codex-agent --vendor OpenAI --capability code_edit --repository payments/api --owner "Platform AI"
cavra registry agent-register claude-code --vendor Anthropic --capability mcp_tool_call --sqlite .cavra/registry.db
cavra registry agent-list --owner "Platform AI"
cavra registry profiles
cavra registry migrate --sqlite .cavra/registry.db
```

Predefined profiles document recommended capabilities and controls for Claude Code, OpenAI Codex, GitHub Copilot Agent, Cursor Agent, Gemini CLI, and AWS Q Developer.

API deployments expose:

- `GET /agents`
- `GET /agents/profiles`
- `POST /agents`
- `GET /agents/{agent_id}`

Set `CAVRA_REGISTRY_STORE` to choose the registry JSON path. Set `CAVRA_REGISTRY_DB` to use SQLite-backed registry persistence.
