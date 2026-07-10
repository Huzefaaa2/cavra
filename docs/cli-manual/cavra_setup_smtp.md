# cavra setup smtp

## Name

`cavra setup smtp` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra setup smtp --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup smtp [OPTIONS]                                                                                            
                                                                                                                                            
 Validate or save SMTP/report-delivery setup metadata without storing passwords.                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --host                         TEXT                                                                                                      │
│ --port                         INTEGER  [default: 587]                                                                                   │
│ --from-email                   TEXT                                                                                                      │
│ --recipient                    TEXT                                                                                                      │
│ --username                     TEXT                                                                                                      │
│ --password-ref                 TEXT     [default: CAVRA_REPORT_SMTP_PASSWORD]                                                            │
│ --state                        PATH                                                                                                      │
│ --live            --no-live             [default: no-live]                                                                               │
│ --save            --no-save             [default: no-save]                                                                               │
│ --help                                  Show this message and exit.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra setup status`](cavra_setup_status.md)
- [`cavra setup init`](cavra_setup_init.md)
- [`cavra setup wizard`](cavra_setup_wizard.md)
- [`cavra setup demo-env`](cavra_setup_demo_env.md)
- [`cavra setup validate`](cavra_setup_validate.md)
- [`cavra setup complete`](cavra_setup_complete.md)
- [`cavra setup policy-actions`](cavra_setup_policy_actions.md)
- [`cavra setup policy-action-test`](cavra_setup_policy_action_test.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
