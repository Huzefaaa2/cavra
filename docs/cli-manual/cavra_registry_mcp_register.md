# cavra registry mcp-register

## Name

`cavra registry mcp-register` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra registry mcp-register --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry mcp-register [OPTIONS] SERVER_ID                                                                       
                                                                                                                                            
 Register or update an MCP server trust record.                                                                                             
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    server_id      TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH  [default: .cavra/registry.json]                                                                            │
│ --sqlite                PATH                                                                                                             │
│ --name                  TEXT                                                                                                             │
│ --trust-tier            TEXT  [default: unknown]                                                                                         │
│ --capability            TEXT                                                                                                             │
│ --owner                 TEXT  [default: unassigned]                                                                                      │
│ --approval-state        TEXT  [default: pending]                                                                                         │
│ --tool                  TEXT                                                                                                             │
│ --help                        Show this message and exit.                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra registry agent-register`](cavra_registry_agent_register.md)
- [`cavra registry agent-list`](cavra_registry_agent_list.md)
- [`cavra registry profiles`](cavra_registry_profiles.md)
- [`cavra registry mcp-list`](cavra_registry_mcp_list.md)
- [`cavra registry mcp-check`](cavra_registry_mcp_check.md)
- [`cavra registry mcp-classifications`](cavra_registry_mcp_classifications.md)
- [`cavra registry migrate`](cavra_registry_migrate.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
