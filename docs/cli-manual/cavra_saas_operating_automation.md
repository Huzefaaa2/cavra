# cavra saas operating-automation

## Name

`cavra saas operating-automation` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra saas operating-automation --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli saas operating-automation [OPTIONS] TENANT_ID                                                                   
                                                                                                                                            
 Print a public-safe SaaS operating automation request and placeholder response.                                                            
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    tenant_id      TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --requested-by                          TEXT  [default: community]                                                                       │
│ --automation-scope                      TEXT  [default: trial-to-paid-customer-scale]                                                    │
│ --automation-cadence                    TEXT  [default: daily]                                                                           │
│ --required-check                        TEXT                                                                                             │
│ --automation-status                     TEXT  [default: unknown]                                                                         │
│ --billing-monitoring-status             TEXT  [default: unknown]                                                                         │
│ --license-telemetry-status              TEXT  [default: unknown]                                                                         │
│ --support-followup-status               TEXT  [default: unknown]                                                                         │
│ --customer-success-review-status        TEXT  [default: unknown]                                                                         │
│ --dashboard-refresh-status              TEXT  [default: unknown]                                                                         │
│ --escalation-drill-status               TEXT  [default: unknown]                                                                         │
│ --closeout-retry-status                 TEXT  [default: unknown]                                                                         │
│ --blocker                               TEXT                                                                                             │
│ --help                                        Show this message and exit.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra saas contract`](cavra_saas_contract.md)
- [`cavra saas worker-handoff`](cavra_saas_worker_handoff.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
