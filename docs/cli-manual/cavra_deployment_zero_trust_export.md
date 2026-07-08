# cavra deployment zero-trust-export

## Name

`cavra deployment zero-trust-export` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra deployment zero-trust-export --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli deployment zero-trust-export [OPTIONS]                                                                          
                                                                                                                                            
 Export zero-trust reference deployment catalog and readiness packets.                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir        PATH  [default: dist/zero-trust-reference-deployments]                                                               │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra deployment zero-trust-catalog`](cavra_deployment_zero_trust_catalog.md)
- [`cavra deployment zero-trust-readiness`](cavra_deployment_zero_trust_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
