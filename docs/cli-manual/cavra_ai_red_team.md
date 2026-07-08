# cavra ai-red-team

## Name

`cavra ai-red-team` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra ai-red-team --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli ai-red-team [OPTIONS] COMMAND [ARGS]...                                                                         
                                                                                                                                            
 Native AI red-team, guardrail, and supply-chain commands.                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ guardrails       Run native LLM guardrail tests.                                                                                         │
│ supply-chain     Validate AI artifact supply-chain metadata.                                                                             │
│ malicious-model  Run malicious model checks against AI artifact metadata.                                                                │
│ export           Export native AI red-team, supply-chain, malicious-model, and readiness artifacts.                                      │
│ readiness        Validate an AI red-team readiness packet.                                                                               │
│ packet           Emit a generated AI red-team readiness packet.                                                                          │
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
