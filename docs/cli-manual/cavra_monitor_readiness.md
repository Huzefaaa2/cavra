# cavra monitor readiness

## Name

`cavra monitor readiness` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra monitor readiness --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli monitor readiness [OPTIONS] PACKET                                                                              
                                                                                                                                            
 Validate a continuous monitoring readiness packet.                                                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra monitor sample-events`](cavra_monitor_sample_events.md)
- [`cavra monitor replay`](cavra_monitor_replay.md)
- [`cavra monitor export`](cavra_monitor_export.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
