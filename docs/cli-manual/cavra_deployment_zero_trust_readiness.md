# cavra deployment zero-trust-readiness

## Name

`cavra deployment zero-trust-readiness` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra deployment zero-trust-readiness --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli deployment zero-trust-readiness                                                                                 
            [OPTIONS] PACKET                                                                                                                
                                                                                                                                            
 Validate a zero-trust reference deployment readiness packet.                                                                               
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo-root                            PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra deployment zero-trust-catalog`](cavra_deployment_zero_trust_catalog.md)
- [`cavra deployment zero-trust-export`](cavra_deployment_zero_trust_export.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
