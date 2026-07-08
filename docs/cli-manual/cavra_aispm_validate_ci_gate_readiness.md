# cavra aispm validate-ci-gate-readiness

## Name

`cavra aispm validate-ci-gate-readiness` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra aispm validate-ci-gate-readiness --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli aispm validate-ci-gate-readiness                                                                                
            [OPTIONS] PATH                                                                                                                  
                                                                                                                                            
 Validate AISPM replay-to-policy CI gate readiness before production use.                                                                   
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo-root        PATH                                                                                                                  │
│ --json                   Print the validation report JSON.                                                                               │
│ --help                   Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra aispm validate-review-packet`](cavra_aispm_validate_review_packet.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
