# cavra adapter export

## Name

`cavra adapter export` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra adapter export --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter export [OPTIONS]                                                                                        
                                                                                                                                            
 Export reference generic adapter taxonomy, manifest, scenario, evaluation, and packet artifacts.                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir        PATH  [default: dist/generic-agent-adapter]                                                                          │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra adapter taxonomy`](cavra_adapter_taxonomy.md)
- [`cavra adapter manifest-validate`](cavra_adapter_manifest_validate.md)
- [`cavra adapter evaluate`](cavra_adapter_evaluate.md)
- [`cavra adapter readiness`](cavra_adapter_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
