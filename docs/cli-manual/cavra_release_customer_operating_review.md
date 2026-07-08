# cavra release customer-operating-review

## Name

`cavra release customer-operating-review` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release customer-operating-review --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-operating-review                                                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the recurring customer operating review packet.                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                   PATH                                                                                          │
│ --closeout-handoff                         PATH                                                                                          │
│ --export-dir                               PATH                                                                                          │
│ --require-live        --no-require-live          [default: no-require-live]                                                              │
│ --help                                           Show this message and exit.                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra release phase6-rollup`](cavra_release_phase6_rollup.md)
- [`cavra release phase4-closeout`](cavra_release_phase4_closeout.md)
- [`cavra release phase5-closeout`](cavra_release_phase5_closeout.md)
- [`cavra release customer-live-evidence`](cavra_release_customer_live_evidence.md)
- [`cavra release customer-evidence-room`](cavra_release_customer_evidence_room.md)
- [`cavra release customer-closeout-handoff`](cavra_release_customer_closeout_handoff.md)
- [`cavra release customer-renewal-expansion`](cavra_release_customer_renewal_expansion.md)
- [`cavra release customer-renewal-outcome`](cavra_release_customer_renewal_outcome.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
