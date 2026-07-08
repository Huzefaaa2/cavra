# cavra policy rego-export

## Name

`cavra policy rego-export` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra policy rego-export --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy rego-export [OPTIONS]                                                                                    
                                                                                                                                            
 Export a CAVRA policy pack to a public-safe OPA/Rego compatibility bundle.                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --output-dir         PATH  [default: dist/opa-rego]                                                                                      │
│ --overlay            PATH                                                                                                                │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra policy list`](cavra_policy_list.md)
- [`cavra policy validate`](cavra_policy_validate.md)
- [`cavra policy test`](cavra_policy_test.md)
- [`cavra policy explain`](cavra_policy_explain.md)
- [`cavra policy compile`](cavra_policy_compile.md)
- [`cavra policy rego-test`](cavra_policy_rego_test.md)
- [`cavra policy rego-readiness`](cavra_policy_rego_readiness.md)
- [`cavra policy lifecycle-plan`](cavra_policy_lifecycle_plan.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
