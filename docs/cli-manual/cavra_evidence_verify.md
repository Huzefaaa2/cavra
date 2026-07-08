# cavra evidence verify

## Name

`cavra evidence verify` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence verify --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence verify [OPTIONS] BUNDLE_DIR                                                                            
                                                                                                                                            
 Verify evidence bundle manifest, checksums, and optional signature.                                                                        
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --key                           TEXT                                                                                                     │
│ --public-key                    PATH                                                                                                     │
│ --trust-root                    PATH                                                                                                     │
│ --key-id                        TEXT                                                                                                     │
│ --minimum-retention-days        INTEGER                                                                                                  │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra evidence bundle`](cavra_evidence_bundle.md)
- [`cavra evidence generate-keypair`](cavra_evidence_generate_keypair.md)
- [`cavra evidence trust-root`](cavra_evidence_trust_root.md)
- [`cavra evidence trust-bundle`](cavra_evidence_trust_bundle.md)
- [`cavra evidence trust-distribution`](cavra_evidence_trust_distribution.md)
- [`cavra evidence siem-event`](cavra_evidence_siem_event.md)
- [`cavra evidence retention-policy`](cavra_evidence_retention_policy.md)
- [`cavra evidence export-siem`](cavra_evidence_export_siem.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
