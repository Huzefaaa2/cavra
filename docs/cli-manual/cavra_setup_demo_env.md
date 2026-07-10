# cavra setup demo-env

## Name

`cavra setup demo-env` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra setup demo-env --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup demo-env [OPTIONS]                                                                                        
                                                                                                                                            
 Create a safe local demo workspace with known policy-triggering scenarios.                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                         PATH  [default: .cavra/demo-workspace]                                                                  │
│ --overwrite    --no-overwrite          [default: no-overwrite]                                                                           │
│ --help                                 Show this message and exit.                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra setup status`](cavra_setup_status.md)
- [`cavra setup init`](cavra_setup_init.md)
- [`cavra setup wizard`](cavra_setup_wizard.md)
- [`cavra setup validate`](cavra_setup_validate.md)
- [`cavra setup complete`](cavra_setup_complete.md)
- [`cavra setup smtp`](cavra_setup_smtp.md)
- [`cavra setup policy-actions`](cavra_setup_policy_actions.md)
- [`cavra setup policy-action-test`](cavra_setup_policy_action_test.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
