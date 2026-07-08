# cavra registry agent-list

## Name

`cavra registry agent-list` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra registry agent-list --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry agent-list [OPTIONS]                                                                                   
                                                                                                                                            
 List governed AI-agent identities.                                                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store         PATH  [default: .cavra/registry.json]                                                                                    │
│ --sqlite        PATH                                                                                                                     │
│ --status        TEXT                                                                                                                     │
│ --owner         TEXT                                                                                                                     │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra registry agent-register`](cavra_registry_agent_register.md)
- [`cavra registry profiles`](cavra_registry_profiles.md)
- [`cavra registry mcp-register`](cavra_registry_mcp_register.md)
- [`cavra registry mcp-list`](cavra_registry_mcp_list.md)
- [`cavra registry mcp-check`](cavra_registry_mcp_check.md)
- [`cavra registry mcp-classifications`](cavra_registry_mcp_classifications.md)
- [`cavra registry migrate`](cavra_registry_migrate.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
