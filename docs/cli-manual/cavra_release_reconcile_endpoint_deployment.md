# cavra release reconcile-endpoint-deployment

## Name

`cavra release reconcile-endpoint-deployment` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release reconcile-endpoint-deployment --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release reconcile-endpoint-deployment                                                                           
            [OPTIONS] PACKAGE_DIR OBSERVED_INVENTORY                                                                                        
                                                                                                                                            
 Compare desired signed endpoint deployment state with observed endpoint inventory.                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir             PATH  [required]                                                                                            │
│ *    observed_inventory      PATH  [required]                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                                         PATH     [default: .cavra/release/endpoint-reconciliation]              │
│ --stale-after-hours                                              INTEGER  [default: 24]                                                  │
│ --metadata-json                                                  PATH                                                                    │
│ --sqlite                                                         PATH                                                                    │
│ --require-package-verification    --skip-package-verification             Verify the Go release package before reconciling observed      │
│                                                                           endpoints.                                                     │
│                                                                           [default: require-package-verification]                        │
│ --json                                                                    Print machine-readable reconciliation output.                  │
│ --help                                                                    Show this message and exit.                                    │
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
