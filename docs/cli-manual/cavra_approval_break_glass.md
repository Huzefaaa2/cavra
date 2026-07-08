# cavra approval break-glass

## Name

`cavra approval break-glass` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra approval break-glass --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval break-glass [OPTIONS] DECISION_FILE                                                                    
                                                                                                                                            
 Record a break-glass override with mandatory evidence.                                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    decision_file      PATH  [required]                                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH     [default: .cavra/approvals.json]                                                                        │
│ --sqlite                PATH                                                                                                             │
│ --actor                 TEXT                                                                                                             │
│ --reason                TEXT                                                                                                             │
│ --approver-group        TEXT     [default: Change Advisory Board]                                                                        │
│ --external-ref          TEXT                                                                                                             │
│ --ttl-hours             INTEGER  [default: 4]                                                                                            │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra approval create`](cavra_approval_create.md)
- [`cavra approval list`](cavra_approval_list.md)
- [`cavra approval approve`](cavra_approval_approve.md)
- [`cavra approval deny`](cavra_approval_deny.md)
- [`cavra approval expire`](cavra_approval_expire.md)
- [`cavra approval route`](cavra_approval_route.md)
- [`cavra approval export-notifications`](cavra_approval_export_notifications.md)
- [`cavra approval provider-requests`](cavra_approval_provider_requests.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
