# cavra evidence search

## Name

`cavra evidence search` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence search --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence search [OPTIONS]                                                                                       
                                                                                                                                            
 Search SQLite-backed evidence metadata with filters and pagination.                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --sqlite                                              PATH     [default: .cavra/evidence/metadata.db]                                    │
│ --session-id                                          TEXT                                                                               │
│ --signer                                              TEXT                                                                               │
│ --min-blocked                                         INTEGER                                                                            │
│ --has-approvals                 --no-has-approvals                                                                                       │
│ --metadata-kind                                       TEXT                                                                               │
│ --rollout-status                                      TEXT                                                                               │
│ --environment                                         TEXT                                                                               │
│ --deployment-target                                   TEXT                                                                               │
│ --target-ring                                         TEXT                                                                               │
│ --approval-state                                      TEXT                                                                               │
│ --promotion-execution-status                          TEXT                                                                               │
│ --rollback-execution-status                           TEXT                                                                               │
│ --limit                                               INTEGER  [default: 50]                                                             │
│ --offset                                              INTEGER  [default: 0]                                                              │
│ --help                                                         Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra evidence bundle`](cavra_evidence_bundle.md)
- [`cavra evidence generate-keypair`](cavra_evidence_generate_keypair.md)
- [`cavra evidence trust-root`](cavra_evidence_trust_root.md)
- [`cavra evidence trust-bundle`](cavra_evidence_trust_bundle.md)
- [`cavra evidence trust-distribution`](cavra_evidence_trust_distribution.md)
- [`cavra evidence verify`](cavra_evidence_verify.md)
- [`cavra evidence siem-event`](cavra_evidence_siem_event.md)
- [`cavra evidence retention-policy`](cavra_evidence_retention_policy.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
