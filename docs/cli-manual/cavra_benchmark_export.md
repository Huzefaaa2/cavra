# cavra benchmark export

## Name

`cavra benchmark export` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra benchmark export --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli benchmark export [OPTIONS]                                                                                      
                                                                                                                                            
 Export benchmark, SLO gate, and readiness artifacts.                                                                                       
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir                        PATH     [default: dist/benchmark-slo]                                                               │
│ --measured         --no-measured             [default: no-measured]                                                                      │
│ --iterations                        INTEGER  [default: 25]                                                                               │
│ --evidence-mode                     TEXT     [default: sample]                                                                           │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra benchmark run`](cavra_benchmark_run.md)
- [`cavra benchmark readiness`](cavra_benchmark_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
