# cavra approval migrate

## Name

`cavra approval migrate` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra approval migrate --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval migrate [OPTIONS]                                                                                      
                                                                                                                                            
 Apply SQLite migrations for approval persistence.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --sqlite                PATH  [default: .cavra/approvals.db]                                                                             │
│ --migrations-dir        PATH  [default: migrations/sqlite]                                                                               │
│ --help                        Show this message and exit.                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra approval create`](cavra_approval_create.md)
- [`cavra approval list`](cavra_approval_list.md)
- [`cavra approval approve`](cavra_approval_approve.md)
- [`cavra approval deny`](cavra_approval_deny.md)
- [`cavra approval expire`](cavra_approval_expire.md)
- [`cavra approval break-glass`](cavra_approval_break_glass.md)
- [`cavra approval route`](cavra_approval_route.md)
- [`cavra approval export-notifications`](cavra_approval_export_notifications.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
