# cavra evidence siem-event

## Name

`cavra evidence siem-event` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence siem-event --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence siem-event [OPTIONS] BUNDLE_DIR                                                                        
                                                                                                                                            
 Print the SIEM event from an evidence bundle.                                                                                              
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra evidence bundle`](cavra_evidence_bundle.md)
- [`cavra evidence generate-keypair`](cavra_evidence_generate_keypair.md)
- [`cavra evidence trust-root`](cavra_evidence_trust_root.md)
- [`cavra evidence trust-bundle`](cavra_evidence_trust_bundle.md)
- [`cavra evidence trust-distribution`](cavra_evidence_trust_distribution.md)
- [`cavra evidence verify`](cavra_evidence_verify.md)
- [`cavra evidence retention-policy`](cavra_evidence_retention_policy.md)
- [`cavra evidence export-siem`](cavra_evidence_export_siem.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
