# MCP Governance

CAVRA governs MCP servers with policy allowlists, blocklists, trust tiers, capability classification, unknown server blocking, and high-risk tool approval. Use `cavra-mcp-server --list-tools` to inspect local tools.

The MCP Trust Registry stores server ID, trust tier, capabilities, owner, approval state, approved tools, last seen, and evidence references:

```bash
cavra registry mcp-register github-mcp --trust-tier approved --approval-state approved --capability repository --tool create_pull_request --owner "Developer Platform"
cavra registry mcp-list --trust-tier approved
cavra registry mcp-check github-mcp create_pull_request --capability repository
```

When `CAVRA_REGISTRY_STORE` is configured for the API, `POST /decisions` uses the registry for `mcp_tool_call` decisions. Registered approved servers can be allowed, unregistered servers remain blocked by default, and out-of-scope tools or capabilities require AI Governance approval.
