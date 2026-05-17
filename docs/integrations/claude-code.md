# CAVRA for Claude Code

CAVRA gives Claude Code a runtime authority layer. It evaluates sensitive agent actions before they reach files, shell commands, Git operations, MCP tools, Terraform, Kubernetes, or cloud control planes.

One-line install path:

```bash
claude mcp add cavra -- cavra-mcp-server
```

Repository setup:

```bash
cavra init claude-code
```

This creates `.mcp.json`, `.cavra/policy.yaml`, and `.cavra/session/`.
