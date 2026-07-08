# cavra release deliver-endpoint-remediation-sla

## Name

`cavra release deliver-endpoint-remediation-sla` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release deliver-endpoint-remediation-sla --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-endpoint-remediation-sla                                                                        
            [OPTIONS] SLA_REPORT                                                                                                            
                                                                                                                                            
 Deliver endpoint remediation SLA notifications through configured release connectors.                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    sla_report      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                                      PATH     Connector config JSON/YAML path. [required]                                    │
│    --output                                      PATH     [default: .cavra/release/endpoint-remediation-sla-deliveries]                  │
│    --provider                                    TEXT     [default: all]                                                                 │
│    --retries                                     INTEGER  [default: 2]                                                                   │
│    --timeout-seconds                             FLOAT    [default: 10.0]                                                                │
│    --generated-by                                TEXT     [default: release-manager]                                                     │
│    --routing-policy                              PATH                                                                                    │
│    --suppression-window-minutes                  INTEGER                                                                                 │
│    --force                         --no-force             [default: no-force]                                                            │
│    --metadata-json                               PATH                                                                                    │
│    --sqlite                                      PATH                                                                                    │
│    --json                                                 Print machine-readable delivery output.                                        │
│    --help                                                 Show this message and exit.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra release phase6-rollup`](cavra_release_phase6_rollup.md)
- [`cavra release phase4-closeout`](cavra_release_phase4_closeout.md)
- [`cavra release phase5-closeout`](cavra_release_phase5_closeout.md)
- [`cavra release customer-live-evidence`](cavra_release_customer_live_evidence.md)
- [`cavra release customer-evidence-room`](cavra_release_customer_evidence_room.md)
- [`cavra release customer-closeout-handoff`](cavra_release_customer_closeout_handoff.md)
- [`cavra release customer-operating-review`](cavra_release_customer_operating_review.md)
- [`cavra release customer-renewal-expansion`](cavra_release_customer_renewal_expansion.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
