# cavra monitor replay

## Name

`cavra monitor replay` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra monitor replay --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli monitor replay [OPTIONS] EVENTS                                                                                 
                                                                                                                                            
 Replay continuous monitoring events and report dedupe, latency, and freshness.                                                             
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    events      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --now                        TEXT     [default: 2026-07-04T10:00:00+00:00]                                                               │
│ --latency-slo-ms             INTEGER  [default: 5000]                                                                                    │
│ --stale-after-minutes        INTEGER  [default: 60]                                                                                      │
│ --help                                Show this message and exit.                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra monitor sample-events`](cavra_monitor_sample_events.md)
- [`cavra monitor export`](cavra_monitor_export.md)
- [`cavra monitor readiness`](cavra_monitor_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
