# cavra adapter

## Name

`cavra adapter` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra adapter --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter [OPTIONS] COMMAND [ARGS]...                                                                             
                                                                                                                                            
 Generic agent adapter and action taxonomy commands.                                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ taxonomy           Emit the public generic action taxonomy.                                                                              │
│ manifest-validate  Validate a generic adapter manifest.                                                                                  │
│ evaluate           Evaluate generic non-coding agent actions through the CAVRA taxonomy.                                                 │
│ export             Export reference generic adapter taxonomy, manifest, scenario, evaluation, and packet artifacts.                      │
│ readiness          Validate a generic adapter readiness packet.                                                                          │
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
