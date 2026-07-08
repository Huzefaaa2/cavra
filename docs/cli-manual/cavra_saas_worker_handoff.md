# cavra saas worker-handoff

## Name

`cavra saas worker-handoff` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra saas worker-handoff --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli saas worker-handoff [OPTIONS] TENANT_ID                                                                         
                                                                                                                                            
 Print a public-safe SaaS operating automation worker handoff request and response.                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    tenant_id      TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --requested-by                  TEXT  [default: community]                                                                               │
│ --deployment-environment        TEXT  [default: production]                                                                              │
│ --worker-mode                   TEXT  [default: dry_run]                                                                                 │
│ --required-check                TEXT                                                                                                     │
│ --worker-target                 TEXT                                                                                                     │
│ --handoff-status                TEXT  [default: requires_private_service]                                                                │
│ --scheduler-ref                 TEXT  [default: scheduler-pending]                                                                       │
│ --evidence-sink-ref             TEXT  [default: evidence-sink-pending]                                                                   │
│ --retry-policy-ref              TEXT  [default: retry-policy-pending]                                                                    │
│ --worker-owner                  TEXT  [default: operations-owner]                                                                        │
│ --blocker                       TEXT                                                                                                     │
│ --help                                Show this message and exit.                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra saas contract`](cavra_saas_contract.md)
- [`cavra saas operating-automation`](cavra_saas_operating_automation.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
