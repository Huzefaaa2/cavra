# cavra aispm validate-review-packet

## Name

`cavra aispm validate-review-packet` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra aispm validate-review-packet --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli aispm validate-review-packet [OPTIONS] PATH                                                                     
                                                                                                                                            
 Validate an AISPM replay-to-policy review packet before PR attachment.                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --json          Print the validation report JSON.                                                                                        │
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra aispm validate-ci-gate-readiness`](cavra_aispm_validate_ci_gate_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
