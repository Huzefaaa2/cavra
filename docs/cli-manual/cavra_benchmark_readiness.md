# cavra benchmark readiness

## Name

`cavra benchmark readiness` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra benchmark readiness --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli benchmark readiness [OPTIONS] PACKET                                                                            
                                                                                                                                            
 Validate a benchmark/SLO readiness packet.                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra benchmark export`](cavra_benchmark_export.md)
- [`cavra benchmark run`](cavra_benchmark_run.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
