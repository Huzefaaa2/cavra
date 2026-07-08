# cavra runtime go-rollback-rehearsal

## Name

`cavra runtime go-rollback-rehearsal` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra runtime go-rollback-rehearsal --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-rehearsal [OPTIONS]                                                                         
                                                                                                                                            
 Show automated rollback rehearsal evidence status for promoted Go pilots.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                               TEXT   [default: disabled]                                                                          │
│ --rollback-plan-path                 TEXT                                                                                                │
│ --rollback-rehearsal-path            TEXT                                                                                                │
│ --rollback-drill-history-path        TEXT                                                                                                │
│ --rollback-drill-max-age-days        FLOAT  [default: 90.0]                                                                              │
│ --json                                      Print rollback rehearsal JSON.                                                               │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra runtime go-pilot-readiness`](cavra_runtime_go_pilot_readiness.md)
- [`cavra runtime go-deployment-readiness`](cavra_runtime_go_deployment_readiness.md)
- [`cavra runtime go-promotion-readiness`](cavra_runtime_go_promotion_readiness.md)
- [`cavra runtime go-rollback-readiness`](cavra_runtime_go_rollback_readiness.md)
- [`cavra runtime go-rollback-drills`](cavra_runtime_go_rollback_drills.md)
- [`cavra runtime go-rollback-drill-schedule`](cavra_runtime_go_rollback_drill_schedule.md)
- [`cavra runtime go-rollback-drill-notification-plan`](cavra_runtime_go_rollback_drill_notification_plan.md)
- [`cavra runtime go-rollback-drill-notification-ack`](cavra_runtime_go_rollback_drill_notification_ack.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
