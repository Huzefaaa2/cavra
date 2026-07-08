# cavra agent exec

## Name

`cavra agent exec` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra agent exec --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent exec [OPTIONS] COMMAND                                                                                    
                                                                                                                                            
 Execute a command under governance policy.                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    command      TEXT  [required]                                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --tool               TEXT  [default: claude-code]                                                                                        │
│ --repo               PATH  [default: .]                                                                                                  │
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --output             PATH  [default: .cavra]                                                                                             │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent start`](cavra_agent_start.md)
- [`cavra agent attest`](cavra_agent_attest.md)
- [`cavra agent enforcement-readiness`](cavra_agent_enforcement_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
