# cavra release execute-rollout-rollback

## Name

`cavra release execute-rollout-rollback` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release execute-rollout-rollback --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release execute-rollout-rollback                                                                                
            [OPTIONS] PROMOTION_EXECUTION                                                                                                   
                                                                                                                                            
 Record an approved endpoint rollout rollback execution.                                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    promotion_execution      PATH  [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                       PATH  [default: .cavra/release/rollout-rollback-execution]                                                │
│ --approval-json                PATH                                                                                                      │
│ --approval-store               PATH                                                                                                      │
│ --approval-sqlite              PATH                                                                                                      │
│ --approval-id                  TEXT                                                                                                      │
│ --executed-by                  TEXT  [default: release-manager]                                                                          │
│ --rollback-reason              TEXT  [default: Rollback approved from promotion execution audit.]                                        │
│ --execution-environment        TEXT                                                                                                      │
│ --notes                        TEXT                                                                                                      │
│ --metadata-json                PATH                                                                                                      │
│ --sqlite                       PATH                                                                                                      │
│ --json                               Print machine-readable rollback execution output.                                                   │
│ --help                               Show this message and exit.                                                                         │
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
