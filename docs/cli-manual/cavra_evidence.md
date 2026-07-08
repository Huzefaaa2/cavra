# cavra evidence

## Name

`cavra evidence` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence [OPTIONS] COMMAND [ARGS]...                                                                            
                                                                                                                                            
 Evidence bundle commands.                                                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ bundle              Generate a CAVRA evidence bundle from the flagship decision sequence.                                                │
│ generate-keypair    Generate an Ed25519 keypair for evidence manifest signatures.                                                        │
│ trust-root          Create a CAVRA evidence signing trust-root document.                                                                 │
│ trust-bundle        Create a distributable bundle of CAVRA evidence trust roots.                                                         │
│ trust-distribution  Create an offline distribution package for CAVRA evidence trust roots.                                               │
│ verify              Verify evidence bundle manifest, checksums, and optional signature.                                                  │
│ siem-event          Print the SIEM event from an evidence bundle.                                                                        │
│ retention-policy    Export evidence retention controls for an existing bundle.                                                           │
│ export-siem         Export provider-specific SIEM payloads from an evidence bundle.                                                      │
│ storage-plan        Create S3 Object Lock and Azure immutable blob reference plans.                                                      │
│ verify-attestation  Verify PR attestation content against bundle evidence.                                                               │
│ index               Persist searchable evidence metadata from a bundle.                                                                  │
│ search              Search SQLite-backed evidence metadata with filters and pagination.                                                  │
│ migrate             Apply SQLite migrations for evidence metadata search.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent`](cavra_agent.md)
- [`cavra policy`](cavra_policy.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra approval`](cavra_approval.md)
- [`cavra registry`](cavra_registry.md)
- [`cavra ops`](cavra_ops.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
