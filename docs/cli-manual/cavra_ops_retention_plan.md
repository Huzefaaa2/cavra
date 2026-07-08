# cavra ops retention-plan

## Name

`cavra ops retention-plan` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra ops retention-plan --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops retention-plan [OPTIONS]                                                                                    
                                                                                                                                            
 Export backup, restore-test, and retention controls for persistent API stores.                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                               PATH     [default: .cavra/operations/retention]                                                   │
│ --retention-days                       INTEGER  [default: 2555]                                                                          │
│ --classification                       TEXT     [default: regulated-sdlc]                                                                │
│ --legal-hold        --no-legal-hold             [default: no-legal-hold]                                                                 │
│ --help                                          Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra ops stores`](cavra_ops_stores.md)
- [`cavra ops backup`](cavra_ops_backup.md)
- [`cavra ops restore`](cavra_ops_restore.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
