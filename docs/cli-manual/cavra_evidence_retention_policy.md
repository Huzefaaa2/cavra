# cavra evidence retention-policy

## Name

`cavra evidence retention-policy` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra evidence retention-policy --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence retention-policy [OPTIONS] BUNDLE_DIR                                                                  
                                                                                                                                            
 Export evidence retention controls for an existing bundle.                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                               PATH     [default: .cavra/evidence/retention]                                                     │
│ --retention-days                       INTEGER  [default: 2555]                                                                          │
│ --classification                       TEXT     [default: regulated-sdlc]                                                                │
│ --legal-hold        --no-legal-hold             [default: no-legal-hold]                                                                 │
│ --help                                          Show this message and exit.                                                              │
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
- [`cavra evidence export-siem`](cavra_evidence_export_siem.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
