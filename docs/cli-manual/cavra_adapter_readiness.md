# cavra adapter readiness

## Name

`cavra adapter readiness` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra adapter readiness --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter readiness [OPTIONS] PACKET                                                                              
                                                                                                                                            
 Validate a generic adapter readiness packet.                                                                                               
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra adapter taxonomy`](cavra_adapter_taxonomy.md)
- [`cavra adapter manifest-validate`](cavra_adapter_manifest_validate.md)
- [`cavra adapter evaluate`](cavra_adapter_evaluate.md)
- [`cavra adapter export`](cavra_adapter_export.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
