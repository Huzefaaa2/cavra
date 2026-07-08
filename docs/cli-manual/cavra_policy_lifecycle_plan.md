# cavra policy lifecycle-plan

## Name

`cavra policy lifecycle-plan` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra policy lifecycle-plan --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy lifecycle-plan [OPTIONS]                                                                                 
                                                                                                                                            
 Export policy lifecycle lint, version, shadow, dry-run, rollback, and approval artifacts.                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack                 TEXT  [default: cavra-ai-agent-baseline]                                                                   │
│ --previous-policy-pack        TEXT                                                                                                       │
│ --output-dir                  PATH  [default: dist/policy-lifecycle]                                                                     │
│ --requested-by                TEXT  [default: policy-owner@example.com]                                                                  │
│ --source-ref                  TEXT  [default: git://Huzefaaa2/cavra/main/policies]                                                       │
│ --help                              Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra policy list`](cavra_policy_list.md)
- [`cavra policy validate`](cavra_policy_validate.md)
- [`cavra policy test`](cavra_policy_test.md)
- [`cavra policy explain`](cavra_policy_explain.md)
- [`cavra policy compile`](cavra_policy_compile.md)
- [`cavra policy rego-export`](cavra_policy_rego_export.md)
- [`cavra policy rego-test`](cavra_policy_rego_test.md)
- [`cavra policy rego-readiness`](cavra_policy_rego_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
