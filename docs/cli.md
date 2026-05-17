# CLI

Primary commands: `cavra version`, `cavra evaluate`, `cavra agent start`, `cavra agent exec`, `cavra agent attest`, `cavra policy list`, `cavra policy validate`, `cavra policy test`, `cavra policy explain`, `cavra policy sign`, `cavra policy verify`, `cavra evidence generate-keypair`, `cavra evidence bundle`, `cavra evidence verify`, `cavra evidence siem-event`, `cavra evidence export-siem`, `cavra evidence retention-policy`, `cavra evidence storage-plan`, `cavra evidence index`, `cavra init claude-code`, and `cavra demo before-the-agent-acts`.

Evidence integration examples:

```bash
cavra evidence bundle --output .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
cavra evidence generate-keypair --private-key .cavra/keys/evidence-private.pem --public-key .cavra/keys/evidence-public.pem
cavra evidence verify .cavra/evidence/latest --public-key .cavra/keys/evidence-public.pem --minimum-retention-days 2555
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence retention-policy .cavra/evidence/latest --output .cavra/evidence/retention --retention-days 2555
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
cavra evidence index .cavra/evidence/latest --store .cavra/evidence/metadata.json
```
