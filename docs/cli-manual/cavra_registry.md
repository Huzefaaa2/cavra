# cavra registry

## Name

`cavra registry` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra registry --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry [OPTIONS] COMMAND [ARGS]...                                                                            
                                                                                                                                            
 Agent and MCP trust registry commands.                                                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ agent-register       Register or update a governed AI-agent identity.                                                                    │
│ agent-list           List governed AI-agent identities.                                                                                  │
│ profiles             List predefined AI-agent capability profiles.                                                                       │
│ mcp-register         Register or update an MCP server trust record.                                                                      │
│ mcp-list             List MCP server trust records.                                                                                      │
│ mcp-check            Evaluate an MCP tool call against the trust registry.                                                               │
│ mcp-classifications  List MCP tool capability classifications.                                                                           │
│ migrate              Apply SQLite migrations for the registry and other CAVRA metadata tables.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent`](cavra_agent.md)
- [`cavra policy`](cavra_policy.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra evidence`](cavra_evidence.md)
- [`cavra approval`](cavra_approval.md)
- [`cavra ops`](cavra_ops.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
