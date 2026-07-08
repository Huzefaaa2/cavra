# cavra runtime go-rollback-drill-notification-plan

## Name

`cavra runtime go-rollback-drill-notification-plan` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra runtime go-rollback-drill-notification-plan --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-drill-notification-plan                                                                     
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Build a public-safe stale rollback drill notification plan.                                                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                                          TEXT  [default: disabled]                                                                │
│ --rollback-drill-history-path                   TEXT                                                                                     │
│ --rollback-drill-schedule-path                  TEXT                                                                                     │
│ --routing-policy                                PATH                                                                                     │
│ --provider                                      TEXT  [default: all]                                                                     │
│ --force                           --no-force          [default: no-force]                                                                │
│ --json                                                Print notification plan JSON.                                                      │
│ --help                                                Show this message and exit.                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra runtime go-pilot-readiness`](cavra_runtime_go_pilot_readiness.md)
- [`cavra runtime go-deployment-readiness`](cavra_runtime_go_deployment_readiness.md)
- [`cavra runtime go-promotion-readiness`](cavra_runtime_go_promotion_readiness.md)
- [`cavra runtime go-rollback-readiness`](cavra_runtime_go_rollback_readiness.md)
- [`cavra runtime go-rollback-rehearsal`](cavra_runtime_go_rollback_rehearsal.md)
- [`cavra runtime go-rollback-drills`](cavra_runtime_go_rollback_drills.md)
- [`cavra runtime go-rollback-drill-schedule`](cavra_runtime_go_rollback_drill_schedule.md)
- [`cavra runtime go-rollback-drill-notification-ack`](cavra_runtime_go_rollback_drill_notification_ack.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
