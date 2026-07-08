# cavra agent attest

## Name

`cavra agent attest` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra agent attest --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent attest [OPTIONS] SESSION_ID                                                                               
                                                                                                                                            
 Generate PR attestation from audit session.                                                                                                
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    session_id      TEXT  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --audit-dir        PATH  [default: .cavra]                                                                                               │
│ --format           TEXT  [default: markdown]                                                                                             │
│ --help                   Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent start`](cavra_agent_start.md)
- [`cavra agent exec`](cavra_agent_exec.md)
- [`cavra agent enforcement-readiness`](cavra_agent_enforcement_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
