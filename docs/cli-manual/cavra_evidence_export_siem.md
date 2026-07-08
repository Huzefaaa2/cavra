# cavra evidence export-siem

## Name

`cavra evidence export-siem` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence export-siem --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence export-siem [OPTIONS] BUNDLE_DIR                                                                       
                                                                                                                                            
 Export provider-specific SIEM payloads from an evidence bundle.                                                                            
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                 PATH  [default: .cavra/evidence/export]                                                                         │
│ --provider               TEXT  [default: all]                                                                                            │
│ --splunk-index           TEXT  [default: cavra]                                                                                          │
│ --datadog-service        TEXT  [default: cavra]                                                                                          │
│ --help                         Show this message and exit.                                                                               │
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
