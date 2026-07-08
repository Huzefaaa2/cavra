# cavra release phase4-closeout

## Name

`cavra release phase4-closeout` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release phase4-closeout --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release phase4-closeout [OPTIONS]                                                                               
                                                                                                                                            
 Validate or export the Phase 4 connector and scanner closeout.                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                                 PATH                                                                            │
│ --repo-root                                              PATH  [default: .]                                                              │
│ --export-dir                                             PATH                                                                            │
│ --require-customer-live    --no-require-customer-live          [default: no-require-customer-live]                                       │
│ --help                                                         Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra release phase6-rollup`](cavra_release_phase6_rollup.md)
- [`cavra release phase5-closeout`](cavra_release_phase5_closeout.md)
- [`cavra release customer-live-evidence`](cavra_release_customer_live_evidence.md)
- [`cavra release customer-evidence-room`](cavra_release_customer_evidence_room.md)
- [`cavra release customer-closeout-handoff`](cavra_release_customer_closeout_handoff.md)
- [`cavra release customer-operating-review`](cavra_release_customer_operating_review.md)
- [`cavra release customer-renewal-expansion`](cavra_release_customer_renewal_expansion.md)
- [`cavra release customer-renewal-outcome`](cavra_release_customer_renewal_outcome.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
