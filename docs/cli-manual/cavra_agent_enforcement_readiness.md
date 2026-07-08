# cavra agent enforcement-readiness

## Name

`cavra agent enforcement-readiness` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra agent enforcement-readiness --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent enforcement-readiness [OPTIONS]                                                                           
                                                                                                                                            
 Report whether a repository can enforce CAVRA for AI coding agents.                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo-root        PATH  [default: .]                                                                                                    │
│ --settings         PATH                                                                                                                  │
│ --json                   Print the full readiness report JSON.                                                                           │
│ --help                   Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent start`](cavra_agent_start.md)
- [`cavra agent exec`](cavra_agent_exec.md)
- [`cavra agent attest`](cavra_agent_attest.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
