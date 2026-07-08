# cavra release endpoint-remediation-sla-escalation-recurrence-automation

## Name

`cavra release endpoint-remediation-sla-escalation-recurrence-automation` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release endpoint-remediation-sla-escalation-recurrence-automation --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-automation                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Run one scheduled recurrence automation pass for retry, digest, and trend follow-up.                                                       
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --retry-policy                              PATH                                                                                         │
│ --config                                    PATH                                                                                         │
│ --output                                    PATH     [default: .cavra/release/endpoint-remediation-sla-escalation-recurrence-automation] │
│ --provider                                  TEXT     [default: all]                                                                      │
│ --retries                                   INTEGER  [default: 2]                                                                        │
│ --timeout-seconds                           FLOAT    [default: 10.0]                                                                     │
│ --schedule-interval-minutes                 INTEGER  [default: 60]                                                                       │
│ --max-digest-plans                          INTEGER  [default: 5]                                                                        │
│ --dry-run                      --execute             Plan by default; use --execute to deliver owner digests through configured          │
│                                                      connectors.                                                                         │
│                                                      [default: dry-run]                                                                  │
│ --generated-by                              TEXT     [default: release-manager]                                                          │
│ --metadata-json                             PATH                                                                                         │
│ --sqlite                                    PATH     [default: .cavra/evidence/metadata.db]                                              │
│ --json                                               Print machine-readable automation output.                                           │
│ --help                                               Show this message and exit.                                                         │
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
