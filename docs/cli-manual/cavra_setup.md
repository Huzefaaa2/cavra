# cavra setup

## Name

`cavra setup` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra setup --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup [OPTIONS] COMMAND [ARGS]...                                                                               
                                                                                                                                            
 First-run setup, defaults, demo workspace, SMTP, and validation commands.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ status              Show first-run setup status.                                                                                         │
│ init                Create default first-run CAVRA setup state.                                                                          │
│ wizard              Run the non-interactive default setup wizard for local Community validation.                                         │
│ demo-env            Create a safe local demo workspace with known policy-triggering scenarios.                                           │
│ validate            Validate default setup, policy pack discovery, demo scenarios, and AISPM readiness inputs.                           │
│ complete            Mark setup as complete after validation.                                                                             │
│ smtp                Validate or save SMTP/report-delivery setup metadata without storing passwords.                                      │
│ policy-actions      List editable allow, block, approval, and MCP action catalog entries from a policy pack.                             │
│ policy-action-test  Test one action against the selected policy pack.                                                                    │
│ policy-action-plan  Create a policy draft plan for an allow/block/approval catalog change.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent`](cavra_agent.md)
- [`cavra policy`](cavra_policy.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra evidence`](cavra_evidence.md)
- [`cavra approval`](cavra_approval.md)
- [`cavra registry`](cavra_registry.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
