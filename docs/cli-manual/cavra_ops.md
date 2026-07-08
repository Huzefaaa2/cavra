# cavra ops

## Name

`cavra ops` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra ops --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops [OPTIONS] COMMAND [ARGS]...                                                                                 
                                                                                                                                            
 Persistent API operations commands.                                                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ stores          List configured persistent API stores and whether each path exists.                                                      │
│ backup          Back up configured JSON and SQLite persistent API stores.                                                                │
│ restore         Restore a persistent API backup after checksum validation.                                                               │
│ retention-plan  Export backup, restore-test, and retention controls for persistent API stores.                                           │
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
- [`cavra registry`](cavra_registry.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
