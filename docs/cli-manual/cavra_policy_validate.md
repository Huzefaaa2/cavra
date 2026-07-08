# cavra policy validate

## Name

`cavra policy validate` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra policy validate --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy validate [OPTIONS] PATH                                                                                  
                                                                                                                                            
 Validate a policy pack against the CAVRA JSON Schema.                                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra policy list`](cavra_policy_list.md)
- [`cavra policy test`](cavra_policy_test.md)
- [`cavra policy explain`](cavra_policy_explain.md)
- [`cavra policy compile`](cavra_policy_compile.md)
- [`cavra policy rego-export`](cavra_policy_rego_export.md)
- [`cavra policy rego-test`](cavra_policy_rego_test.md)
- [`cavra policy rego-readiness`](cavra_policy_rego_readiness.md)
- [`cavra policy lifecycle-plan`](cavra_policy_lifecycle_plan.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
