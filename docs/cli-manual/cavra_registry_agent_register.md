# cavra registry agent-register

## Name

`cavra registry agent-register` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra registry agent-register --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry agent-register [OPTIONS] AGENT_ID                                                                      
                                                                                                                                            
 Register or update a governed AI-agent identity.                                                                                           
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    agent_id      TEXT  [required]                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store             PATH  [default: .cavra/registry.json]                                                                                │
│ --sqlite            PATH                                                                                                                 │
│ --agent-type        TEXT  [default: coding-agent]                                                                                        │
│ --vendor            TEXT  [default: unknown]                                                                                             │
│ --version           TEXT  [default: unknown]                                                                                             │
│ --capability        TEXT                                                                                                                 │
│ --scope             TEXT                                                                                                                 │
│ --repository        TEXT                                                                                                                 │
│ --tool              TEXT                                                                                                                 │
│ --risk-tier         TEXT  [default: medium]                                                                                              │
│ --owner             TEXT  [default: unassigned]                                                                                          │
│ --status            TEXT  [default: active]                                                                                              │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra registry agent-list`](cavra_registry_agent_list.md)
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
