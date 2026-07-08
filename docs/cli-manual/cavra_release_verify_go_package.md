# cavra release verify-go-package

## Name

`cavra release verify-go-package` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release verify-go-package --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release verify-go-package [OPTIONS] PACKAGE_DIR                                                                 
                                                                                                                                            
 Verify a CAVRA Go runtime release package.                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-signatures    --allow-unsigned                Require detached Ed25519 signatures for release artifacts.                       │
│                                                         [default: require-signatures]                                                    │
│ --require-provenance    --allow-missing-provenance      Require SLSA provenance for release artifacts. [default: require-provenance]     │
│ --json                                                  Print machine-readable verification output.                                      │
│ --help                                                  Show this message and exit.                                                      │
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
