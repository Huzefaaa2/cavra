# cavra setup policy-action-test

## Name

`cavra setup policy-action-test` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra setup policy-action-test --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup policy-action-test [OPTIONS]                                                                              
                                                                                                                                            
 Test one action against the selected policy pack.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --action-type        TEXT  [default: execute_command]                                                                                    │
│ --target             TEXT                                                                                                                │
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra setup status`](cavra_setup_status.md)
- [`cavra setup init`](cavra_setup_init.md)
- [`cavra setup wizard`](cavra_setup_wizard.md)
- [`cavra setup demo-env`](cavra_setup_demo_env.md)
- [`cavra setup validate`](cavra_setup_validate.md)
- [`cavra setup complete`](cavra_setup_complete.md)
- [`cavra setup smtp`](cavra_setup_smtp.md)
- [`cavra setup policy-actions`](cavra_setup_policy_actions.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
