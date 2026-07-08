# cavra registry migrate

## Name

`cavra registry migrate` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra registry migrate --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry migrate [OPTIONS]                                                                                      
                                                                                                                                            
 Apply SQLite migrations for the registry and other CAVRA metadata tables.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --sqlite            PATH  [default: .cavra/registry.db]                                                                                  │
│ --migrations        PATH  [default: migrations/sqlite]                                                                                   │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra registry agent-register`](cavra_registry_agent_register.md)
- [`cavra registry agent-list`](cavra_registry_agent_list.md)
- [`cavra registry profiles`](cavra_registry_profiles.md)
- [`cavra registry mcp-register`](cavra_registry_mcp_register.md)
- [`cavra registry mcp-list`](cavra_registry_mcp_list.md)
- [`cavra registry mcp-check`](cavra_registry_mcp_check.md)
- [`cavra registry mcp-classifications`](cavra_registry_mcp_classifications.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
