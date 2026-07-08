# cavra evidence storage-plan

## Name

`cavra evidence storage-plan` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence storage-plan --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence storage-plan [OPTIONS] BUNDLE_DIR                                                                      
                                                                                                                                            
 Create S3 Object Lock and Azure immutable blob reference plans.                                                                            
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                 PATH     [default: .cavra/evidence/storage]                                                                     │
│ --retention-days         INTEGER  [default: 2555]                                                                                        │
│ --s3-bucket              TEXT     [default: cavra-evidence]                                                                              │
│ --s3-prefix              TEXT     [default: evidence/]                                                                                   │
│ --azure-account          TEXT     [default: cavraevidence]                                                                               │
│ --azure-container        TEXT     [default: evidence]                                                                                    │
│ --help                            Show this message and exit.                                                                            │
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
