# cavra

## Name

`cavra` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli [OPTIONS] COMMAND [ARGS]...                                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ version                                                                                                                                  │
│ evaluate     Evaluate one action before an AI agent performs it.                                                                         │
│ agent        AI agent runtime commands.                                                                                                  │
│ policy       Policy registry commands.                                                                                                   │
│ demo         Runnable CAVRA demos.                                                                                                       │
│ init         Initialize CAVRA integrations.                                                                                              │
│ integration  Enterprise connector delivery commands.                                                                                     │
│ evidence     Evidence bundle commands.                                                                                                   │
│ approval     Human approval router commands.                                                                                             │
│ registry     Agent and MCP trust registry commands.                                                                                      │
│ ops          Persistent API operations commands.                                                                                         │
│ release      Release package verification commands.                                                                                      │
│ runtime      Runtime backend pilot commands.                                                                                             │
│ saas         Public-safe SaaS Control Plane contract commands.                                                                           │
│ aispm        AI Security Posture Management commands.                                                                                    │
│ monitor      Continuous monitoring event commands.                                                                                       │
│ benchmark    Benchmark and SLO regression commands.                                                                                      │
│ adapter      Generic agent adapter and action taxonomy commands.                                                                         │
│ ai-red-team  Native AI red-team, guardrail, and supply-chain commands.                                                                   │
│ deployment   Reference deployment and zero-trust packaging commands.                                                                     │
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
