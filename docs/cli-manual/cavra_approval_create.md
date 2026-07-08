# cavra approval create

## Name

`cavra approval create` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra approval create --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval create [OPTIONS] DECISION_FILE                                                                         
                                                                                                                                            
 Create a pending approval request from a CAVRA decision.                                                                                   
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    decision_file      PATH  [required]                                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH     [default: .cavra/approvals.json]                                                                        │
│ --sqlite                PATH                                                                                                             │
│ --approver-group        TEXT                                                                                                             │
│ --routing-file          PATH                                                                                                             │
│ --requested-by          TEXT     [default: ai-agent]                                                                                     │
│ --ttl-hours             INTEGER  [default: 24]                                                                                           │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra approval list`](cavra_approval_list.md)
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
