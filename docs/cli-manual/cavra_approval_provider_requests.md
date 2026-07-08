# cavra approval provider-requests

## Name

`cavra approval provider-requests` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra approval provider-requests --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval provider-requests [OPTIONS] APPROVAL_ID                                                                
                                                                                                                                            
 Export credential-free HTTP request specs for approval providers.                                                                          
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    approval_id      TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store           PATH  [default: .cavra/approvals.json]                                                                                 │
│ --sqlite          PATH                                                                                                                   │
│ --output          PATH  [default: .cavra/approvals/provider-requests]                                                                    │
│ --provider        TEXT  [default: all]                                                                                                   │
│ --help                  Show this message and exit.                                                                                      │
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
