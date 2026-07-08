# cavra agent start

## Name

`cavra agent start` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra agent start --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent start [OPTIONS] TOOL                                                                                      
                                                                                                                                            
 Start an AI agent governance session.                                                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    tool      TEXT  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo               PATH  [default: .]                                                                                                  │
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --output             PATH  [default: .cavra]                                                                                             │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent exec`](cavra_agent_exec.md)
- [`cavra agent attest`](cavra_agent_attest.md)
- [`cavra agent enforcement-readiness`](cavra_agent_enforcement_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
