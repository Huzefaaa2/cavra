# cavra deployment

## Name

`cavra deployment` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra deployment --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli deployment [OPTIONS] COMMAND [ARGS]...                                                                          
                                                                                                                                            
 Reference deployment and zero-trust packaging commands.                                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ zero-trust-catalog    Emit and validate the zero-trust reference deployment catalog.                                                     │
│ zero-trust-export     Export zero-trust reference deployment catalog and readiness packets.                                              │
│ zero-trust-readiness  Validate a zero-trust reference deployment readiness packet.                                                       │
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
