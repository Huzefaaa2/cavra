# cavra setup wizard

## Name

`cavra setup wizard` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra setup wizard --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup wizard [OPTIONS]                                                                                          
                                                                                                                                            
 Run the non-interactive default setup wizard for local Community validation.                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --state                               PATH                                                                                               │
│ --workspace-name                      TEXT  [default: local-community]                                                                   │
│ --overwrite         --no-overwrite          [default: no-overwrite]                                                                      │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra setup status`](cavra_setup_status.md)
- [`cavra setup init`](cavra_setup_init.md)
- [`cavra setup demo-env`](cavra_setup_demo_env.md)
- [`cavra setup validate`](cavra_setup_validate.md)
- [`cavra setup complete`](cavra_setup_complete.md)
- [`cavra setup smtp`](cavra_setup_smtp.md)
- [`cavra setup policy-actions`](cavra_setup_policy_actions.md)
- [`cavra setup policy-action-test`](cavra_setup_policy_action_test.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
