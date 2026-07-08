# cavra ops backup

## Name

`cavra ops backup` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra ops backup --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops backup [OPTIONS]                                                                                            
                                                                                                                                            
 Back up configured JSON and SQLite persistent API stores.                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                     PATH  [default: .cavra/backups/latest]                                                      │
│ --include-missing    --no-include-missing          [default: no-include-missing]                                                         │
│ --help                                             Show this message and exit.                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra ops stores`](cavra_ops_stores.md)
- [`cavra ops restore`](cavra_ops_restore.md)
- [`cavra ops retention-plan`](cavra_ops_retention_plan.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
