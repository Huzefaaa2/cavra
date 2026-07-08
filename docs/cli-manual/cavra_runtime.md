# cavra runtime

## Name

`cavra runtime` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra runtime --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime [OPTIONS] COMMAND [ARGS]...                                                                             
                                                                                                                                            
 Runtime backend pilot commands.                                                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ go-pilot-readiness                   Show opt-in Go backend pilot readiness.                                                             │
│ go-deployment-readiness              Show Go backend CI runner and workstation deployment readiness.                                     │
│ go-promotion-readiness               Show Go backend promotion readiness for optional backend use.                                       │
│ go-rollback-readiness                Show Go backend rollback readiness for promoted pilots.                                             │
│ go-rollback-rehearsal                Show automated rollback rehearsal evidence status for promoted Go pilots.                           │
│ go-rollback-drills                   Show operational rollback drill history status for promoted Go pilots.                              │
│ go-rollback-drill-schedule           Show recurring rollback drill schedule and stale-drill notification readiness.                      │
│ go-rollback-drill-notification-plan  Build a public-safe stale rollback drill notification plan.                                         │
│ go-rollback-drill-notification-ack   Build public-safe rollback drill notification acknowledgement metadata.                             │
│ go-rollback-drill-escalation-plan    Build an empty public-safe rollback drill notification escalation plan template.                    │
│ go-pilot-evaluate                    Evaluate through the opt-in Go backend pilot with Python fallback.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent`](cavra_agent.md)
- [`cavra policy`](cavra_policy.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra evidence`](cavra_evidence.md)
- [`cavra approval`](cavra_approval.md)
- [`cavra registry`](cavra_registry.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
