# cavra monitor export

## Name

`cavra monitor export` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra monitor export --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli monitor export [OPTIONS]                                                                                        
                                                                                                                                            
 Export sample continuous monitoring artifacts.                                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir           PATH  [default: dist/continuous-monitoring]                                                                       │
│ --evidence-mode        TEXT  [default: sample]                                                                                           │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra monitor sample-events`](cavra_monitor_sample_events.md)
- [`cavra monitor replay`](cavra_monitor_replay.md)
- [`cavra monitor readiness`](cavra_monitor_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
