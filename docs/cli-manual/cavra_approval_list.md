# cavra approval list

## Name

`cavra approval list` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra approval list --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval list [OPTIONS]                                                                                         
                                                                                                                                            
 List approval queue entries.                                                                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH     [default: .cavra/approvals.json]                                                                        │
│ --sqlite                PATH                                                                                                             │
│ --state                 TEXT                                                                                                             │
│ --approver-group        TEXT                                                                                                             │
│ --limit                 INTEGER  [default: 50]                                                                                           │
│ --offset                INTEGER  [default: 0]                                                                                            │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra approval create`](cavra_approval_create.md)
- [`cavra approval approve`](cavra_approval_approve.md)
- [`cavra approval deny`](cavra_approval_deny.md)
- [`cavra approval expire`](cavra_approval_expire.md)
- [`cavra approval break-glass`](cavra_approval_break_glass.md)
- [`cavra approval route`](cavra_approval_route.md)
- [`cavra approval export-notifications`](cavra_approval_export_notifications.md)
- [`cavra approval provider-requests`](cavra_approval_provider_requests.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
