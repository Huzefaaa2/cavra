# cavra agent

## Name

`cavra agent` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra agent --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent [OPTIONS] COMMAND [ARGS]...                                                                               
                                                                                                                                            
 AI agent runtime commands.                                                                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ start                  Start an AI agent governance session.                                                                             │
│ exec                   Execute a command under governance policy.                                                                        │
│ attest                 Generate PR attestation from audit session.                                                                       │
│ enforcement-readiness  Report whether a repository can enforce CAVRA for AI coding agents.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra policy`](cavra_policy.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra evidence`](cavra_evidence.md)
- [`cavra approval`](cavra_approval.md)
- [`cavra registry`](cavra_registry.md)
- [`cavra ops`](cavra_ops.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
