# cavra evaluate

## Name

`cavra evaluate` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evaluate --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evaluate [OPTIONS] ACTION_TYPE TARGET                                                                           
                                                                                                                                            
 Evaluate one action before an AI agent performs it.                                                                                        
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    action_type      TEXT  [required]                                                                                                   │
│ *    target           TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack               TEXT  [default: cavra-ai-agent-baseline]                                                                     │
│ --policy-mode               TEXT  [default: enforce]                                                                                     │
│ --break-glass-reason        TEXT                                                                                                         │
│ --break-glass-actor         TEXT                                                                                                         │
│ --json                            Print the full decision JSON.                                                                          │
│ --help                            Show this message and exit.                                                                            │
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
