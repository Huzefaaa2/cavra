# cavra runtime go-rollback-drill-schedule

## Name

`cavra runtime go-rollback-drill-schedule` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra runtime go-rollback-drill-schedule --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-drill-schedule                                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show recurring rollback drill schedule and stale-drill notification readiness.                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                                TEXT   [default: disabled]                                                                         │
│ --rollback-drill-history-path         TEXT                                                                                               │
│ --rollback-drill-max-age-days         FLOAT  [default: 90.0]                                                                             │
│ --rollback-drill-schedule-path        TEXT                                                                                               │
│ --rollback-drill-due-soon-days        FLOAT  [default: 14.0]                                                                             │
│ --json                                       Print rollback drill schedule JSON.                                                         │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra runtime go-pilot-readiness`](cavra_runtime_go_pilot_readiness.md)
- [`cavra runtime go-deployment-readiness`](cavra_runtime_go_deployment_readiness.md)
- [`cavra runtime go-promotion-readiness`](cavra_runtime_go_promotion_readiness.md)
- [`cavra runtime go-rollback-readiness`](cavra_runtime_go_rollback_readiness.md)
- [`cavra runtime go-rollback-rehearsal`](cavra_runtime_go_rollback_rehearsal.md)
- [`cavra runtime go-rollback-drills`](cavra_runtime_go_rollback_drills.md)
- [`cavra runtime go-rollback-drill-notification-plan`](cavra_runtime_go_rollback_drill_notification_plan.md)
- [`cavra runtime go-rollback-drill-notification-ack`](cavra_runtime_go_rollback_drill_notification_ack.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
