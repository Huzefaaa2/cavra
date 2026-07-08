# cavra release automate-endpoint-reconciliation

## Name

`cavra release automate-endpoint-reconciliation` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release automate-endpoint-reconciliation --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release automate-endpoint-reconciliation                                                                        
            [OPTIONS] PACKAGE_DIR INVENTORY_INGESTION                                                                                       
                                                                                                                                            
 Reconcile a fresh inventory ingestion and open remediation when drift is detected.                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir              PATH  [required]                                                                                           │
│ *    inventory_ingestion      PATH  [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                                         PATH     [default: .cavra/release/endpoint-reconciliation-automation]   │
│ --stale-after-hours                                              INTEGER  [default: 24]                                                  │
│ --remediation-strategy                                           TEXT     [default: mixed]                                               │
│ --requested-by                                                   TEXT     [default: release-agent]                                       │
│ --approver-group                                                 TEXT     [default: Endpoint Change Advisory Board]                      │
│ --ttl-hours                                                      INTEGER  [default: 24]                                                  │
│ --approval-store                                                 PATH                                                                    │
│ --approval-sqlite                                                PATH                                                                    │
│ --metadata-json                                                  PATH                                                                    │
│ --sqlite                                                         PATH                                                                    │
│ --require-package-verification    --skip-package-verification             Verify the Go release package before reconciling observed      │
│                                                                           endpoints.                                                     │
│                                                                           [default: skip-package-verification]                           │
│ --json                                                                    Print machine-readable automation output.                      │
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
