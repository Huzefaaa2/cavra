# cavra adapter evaluate

## Name

`cavra adapter evaluate` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra adapter evaluate --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter evaluate [OPTIONS] ACTIONS                                                                              
                                                                                                                                            
 Evaluate generic non-coding agent actions through the CAVRA taxonomy.                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    actions      PATH  [required]                                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra adapter taxonomy`](cavra_adapter_taxonomy.md)
- [`cavra adapter manifest-validate`](cavra_adapter_manifest_validate.md)
- [`cavra adapter export`](cavra_adapter_export.md)
- [`cavra adapter readiness`](cavra_adapter_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
