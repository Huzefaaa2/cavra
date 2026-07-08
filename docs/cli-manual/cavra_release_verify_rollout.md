# cavra release verify-rollout

## Name

`cavra release verify-rollout` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release verify-rollout --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli release verify-rollout [OPTIONS] ROLLOUT_DIR                                                                    
                                                                                                                                            
 Verify managed endpoint rollout evidence and optionally index its metadata.                                                                
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    rollout_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --package-dir                                                    PATH                                                                    │
│ --require-package-verification    --skip-package-verification          Verify the referenced release package while verifying rollout     │
│                                                                        evidence.                                                         │
│                                                                        [default: require-package-verification]                           │
│ --require-signatures              --allow-unsigned                     Require detached Ed25519 signatures for referenced release        │
│                                                                        artifacts.                                                        │
│                                                                        [default: require-signatures]                                     │
│ --require-provenance              --allow-missing-provenance           Require SLSA provenance for referenced release artifacts.         │
│                                                                        [default: require-provenance]                                     │
│ --metadata-json                                                  PATH                                                                    │
│ --sqlite                                                         PATH                                                                    │
│ --json                                                                 Print machine-readable verification output.                       │
│ --help                                                                 Show this message and exit.                                       │
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
