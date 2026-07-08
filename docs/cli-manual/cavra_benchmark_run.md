# cavra benchmark run

## Name

`cavra benchmark run` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra benchmark run --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli benchmark run [OPTIONS]                                                                                         
                                                                                                                                            
 Run or emit the benchmark/SLO report and fail when the gate has blockers.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --measured      --no-measured             [default: no-measured]                                                                         │
│ --iterations                     INTEGER  [default: 25]                                                                                  │
│ --help                                    Show this message and exit.                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra benchmark export`](cavra_benchmark_export.md)
- [`cavra benchmark readiness`](cavra_benchmark_readiness.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
