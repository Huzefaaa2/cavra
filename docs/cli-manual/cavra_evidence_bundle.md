# cavra evidence bundle

## Name

`cavra evidence bundle` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence bundle --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence bundle [OPTIONS]                                                                                       
                                                                                                                                            
 Generate a CAVRA evidence bundle from the flagship decision sequence.                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                               PATH     [default: .cavra/evidence/latest]                                                        │
│ --policy-pack                          TEXT     [default: cavra-ai-agent-baseline]                                                       │
│ --signer                               TEXT     [default: local]                                                                         │
│ --key                                  TEXT                                                                                              │
│ --private-key                          PATH                                                                                              │
│ --key-id                               TEXT                                                                                              │
│ --retention-days                       INTEGER  [default: 2555]                                                                          │
│ --classification                       TEXT     [default: regulated-sdlc]                                                                │
│ --legal-hold        --no-legal-hold             [default: no-legal-hold]                                                                 │
│ --help                                          Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra evidence generate-keypair`](cavra_evidence_generate_keypair.md)
- [`cavra evidence trust-root`](cavra_evidence_trust_root.md)
- [`cavra evidence trust-bundle`](cavra_evidence_trust_bundle.md)
- [`cavra evidence trust-distribution`](cavra_evidence_trust_distribution.md)
- [`cavra evidence verify`](cavra_evidence_verify.md)
- [`cavra evidence siem-event`](cavra_evidence_siem_event.md)
- [`cavra evidence retention-policy`](cavra_evidence_retention_policy.md)
- [`cavra evidence export-siem`](cavra_evidence_export_siem.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
