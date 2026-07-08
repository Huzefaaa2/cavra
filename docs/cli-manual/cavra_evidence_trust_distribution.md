# cavra evidence trust-distribution

## Name

`cavra evidence trust-distribution` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence trust-distribution --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence trust-distribution [OPTIONS]                                                                           
                                                        TRUST_ROOTS...                                                                      
                                                                                                                                            
 Create an offline distribution package for CAVRA evidence trust roots.                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    trust_roots      TRUST_ROOTS...  [required]                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                 PATH  [default: .cavra/keys/trust-root-distribution]                                                            │
│ --environment            TEXT  [default: production]                                                                                     │
│ --distribution-id        TEXT                                                                                                            │
│ --channel                TEXT                                                                                                            │
│ --help                         Show this message and exit.                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra evidence bundle`](cavra_evidence_bundle.md)
- [`cavra evidence generate-keypair`](cavra_evidence_generate_keypair.md)
- [`cavra evidence trust-root`](cavra_evidence_trust_root.md)
- [`cavra evidence trust-bundle`](cavra_evidence_trust_bundle.md)
- [`cavra evidence verify`](cavra_evidence_verify.md)
- [`cavra evidence siem-event`](cavra_evidence_siem_event.md)
- [`cavra evidence retention-policy`](cavra_evidence_retention_policy.md)
- [`cavra evidence export-siem`](cavra_evidence_export_siem.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
