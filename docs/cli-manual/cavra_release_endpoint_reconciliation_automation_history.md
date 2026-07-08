# cavra release endpoint-reconciliation-automation-history

## Name

`cavra release endpoint-reconciliation-automation-history` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release endpoint-reconciliation-automation-history --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-reconciliation-automation-history                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint reconciliation automation history.                                                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json         PATH                                                                                                             │
│ --sqlite                PATH     [default: .cavra/evidence/metadata.db]                                                                  │
│ --drift-status          TEXT                                                                                                             │
│ --alert-level           TEXT                                                                                                             │
│ --approval-state        TEXT                                                                                                             │
│ --provider              TEXT                                                                                                             │
│ --limit                 INTEGER  [default: 50]                                                                                           │
│ --offset                INTEGER  [default: 0]                                                                                            │
│ --help                           Show this message and exit.                                                                             │
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
