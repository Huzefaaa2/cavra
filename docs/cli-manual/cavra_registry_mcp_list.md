# cavra registry mcp-list

## Name

`cavra registry mcp-list` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra registry mcp-list --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry mcp-list [OPTIONS]                                                                                     
                                                                                                                                            
 List MCP server trust records.                                                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH  [default: .cavra/registry.json]                                                                            │
│ --sqlite                PATH                                                                                                             │
│ --trust-tier            TEXT                                                                                                             │
│ --approval-state        TEXT                                                                                                             │
│ --capability            TEXT                                                                                                             │
│ --help                        Show this message and exit.                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra registry agent-register`](cavra_registry_agent_register.md)
- [`cavra registry agent-list`](cavra_registry_agent_list.md)
- [`cavra registry profiles`](cavra_registry_profiles.md)
- [`cavra registry mcp-register`](cavra_registry_mcp_register.md)
- [`cavra registry mcp-check`](cavra_registry_mcp_check.md)
- [`cavra registry mcp-classifications`](cavra_registry_mcp_classifications.md)
- [`cavra registry migrate`](cavra_registry_migrate.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
