# cavra ops restore

## Name

`cavra ops restore` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra ops restore --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops restore [OPTIONS] MANIFEST                                                                                  
                                                                                                                                            
 Restore a persistent API backup after checksum validation.                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    manifest      PATH  [required]                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --target-dir                      PATH                                                                                                   │
│ --overwrite     --no-overwrite          [default: no-overwrite]                                                                          │
│ --help                                  Show this message and exit.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra ops stores`](cavra_ops_stores.md)
- [`cavra ops backup`](cavra_ops_backup.md)
- [`cavra ops retention-plan`](cavra_ops_retention_plan.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
