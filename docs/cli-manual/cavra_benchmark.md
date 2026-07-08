# cavra benchmark

## Name

`cavra benchmark` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra benchmark --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli benchmark [OPTIONS] COMMAND [ARGS]...                                                                           
                                                                                                                                            
 Benchmark and SLO regression commands.                                                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ export     Export benchmark, SLO gate, and readiness artifacts.                                                                          │
│ run        Run or emit the benchmark/SLO report and fail when the gate has blockers.                                                     │
│ readiness  Validate a benchmark/SLO readiness packet.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent`](cavra_agent.md)
- [`cavra policy`](cavra_policy.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra evidence`](cavra_evidence.md)
- [`cavra approval`](cavra_approval.md)
- [`cavra registry`](cavra_registry.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
