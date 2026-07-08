# cavra approval

## Name

`cavra approval` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra approval --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval [OPTIONS] COMMAND [ARGS]...                                                                            
                                                                                                                                            
 Human approval router commands.                                                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create                Create a pending approval request from a CAVRA decision.                                                           │
│ list                  List approval queue entries.                                                                                       │
│ approve               Approve a pending request.                                                                                         │
│ deny                  Deny a pending request.                                                                                            │
│ expire                Expire a pending request.                                                                                          │
│ break-glass           Record a break-glass override with mandatory evidence.                                                             │
│ route                 Show the approver group selected by approval routing policy.                                                       │
│ export-notifications  Export reference notification payloads for approval providers.                                                     │
│ provider-requests     Export credential-free HTTP request specs for approval providers.                                                  │
│ deliver               Send live approval provider requests and write redacted delivery evidence.                                         │
│ migrate               Apply SQLite migrations for approval persistence.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent`](cavra_agent.md)
- [`cavra policy`](cavra_policy.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra evidence`](cavra_evidence.md)
- [`cavra registry`](cavra_registry.md)
- [`cavra ops`](cavra_ops.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
