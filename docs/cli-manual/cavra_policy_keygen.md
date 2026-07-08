# cavra policy keygen

## Name

`cavra policy keygen` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra policy keygen --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy keygen [OPTIONS]                                                                                         
                                                                                                                                            
 Generate a local Ed25519 keypair for public policy signing workflows.                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output        PATH  [default: .cavra/policy-signing]                                                                                   │
│ --key-id        TEXT  [default: local-policy-signing-key]                                                                                │
│ --help                Show this message and exit.                                                                                        │
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
