# CLI

Primary commands: `cavra version`, `cavra evaluate`, `cavra agent start`, `cavra agent exec`, `cavra agent attest`, `cavra policy list`, `cavra policy validate`, `cavra policy test`, `cavra policy explain`, `cavra policy sign`, `cavra policy verify`, `cavra evidence generate-keypair`, `cavra evidence trust-root`, `cavra evidence bundle`, `cavra evidence verify`, `cavra evidence siem-event`, `cavra evidence export-siem`, `cavra evidence retention-policy`, `cavra evidence storage-plan`, `cavra evidence verify-attestation`, `cavra evidence index`, `cavra evidence search`, `cavra init claude-code`, and `cavra demo before-the-agent-acts`.

Evidence integration examples:

```bash
cavra evidence bundle --output .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
cavra evidence generate-keypair --private-key .cavra/keys/evidence-private.pem --public-key .cavra/keys/evidence-public.pem
cavra evidence trust-root .cavra/keys/evidence-public.pem --output .cavra/keys/evidence-trust-root.json --key-id prod-evidence
cavra evidence verify .cavra/evidence/latest --trust-root .cavra/keys/evidence-trust-root.json --key-id prod-evidence --minimum-retention-days 2555
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence retention-policy .cavra/evidence/latest --output .cavra/evidence/retention --retention-days 2555
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
cavra evidence verify-attestation .cavra/evidence/latest --output .cavra/evidence/attestation
cavra evidence index .cavra/evidence/latest --sqlite .cavra/evidence/metadata.db
cavra evidence search --sqlite .cavra/evidence/metadata.db --min-blocked 1 --limit 25
```
