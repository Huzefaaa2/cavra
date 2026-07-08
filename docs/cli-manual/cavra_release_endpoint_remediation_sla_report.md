# cavra release endpoint-remediation-sla-report

## Name

`cavra release endpoint-remediation-sla-report` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release endpoint-remediation-sla-report --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-report                                                                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Generate endpoint remediation SLA, escalation, and executive reporting.                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                     PATH     [default: .cavra/release/endpoint-remediation-sla]                                                 │
│ --metadata-json              PATH                                                                                                        │
│ --sqlite                     PATH     [default: .cavra/evidence/metadata.db]                                                             │
│ --warning-hours              INTEGER  [default: 24]                                                                                      │
│ --critical-hours             INTEGER  [default: 48]                                                                                      │
│ --generated-by               TEXT     [default: release-manager]                                                                         │
│ --index-metadata-json        PATH                                                                                                        │
│ --index-sqlite               PATH                                                                                                        │
│ --json                                Print machine-readable SLA report output.                                                          │
│ --help                                Show this message and exit.                                                                        │
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
