# Agent Identity

The Agent Registry tracks governed AI-agent identities with `agent_id`, type, vendor, version, capabilities, scopes, allowed repositories, allowed tools, risk tier, owner, status, last seen, and evidence references.

The first implementation is JSON-backed for local and self-hosted pilots:

```bash
cavra registry agent-register codex-agent --vendor OpenAI --capability code_edit --repository payments/api --owner "Platform AI"
cavra registry agent-list --owner "Platform AI"
```

API deployments expose:

- `GET /agents`
- `POST /agents`
- `GET /agents/{agent_id}`

Set `CAVRA_REGISTRY_STORE` to choose the registry JSON path.
