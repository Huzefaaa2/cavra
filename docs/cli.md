# CLI

Primary commands: `cavra version`, `cavra evaluate`, `cavra agent start`, `cavra agent exec`, `cavra agent attest`, `cavra policy list`, `cavra policy validate`, `cavra policy test`, `cavra policy explain`, `cavra policy sign`, `cavra policy verify`, `cavra evidence bundle`, `cavra evidence verify`, `cavra evidence siem-event`, `cavra evidence export-siem`, `cavra evidence storage-plan`, `cavra init claude-code`, and `cavra demo before-the-agent-acts`.

Evidence integration examples:

```bash
cavra evidence bundle --output .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
```
