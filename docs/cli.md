# CLI

Primary commands: `cavra version`, `cavra evaluate`, `cavra agent start`, `cavra agent exec`, `cavra agent attest`, `cavra policy list`, `cavra policy validate`, `cavra policy test`, `cavra policy explain`, `cavra policy sign`, `cavra policy verify`, `cavra approval create`, `cavra approval list`, `cavra approval approve`, `cavra approval deny`, `cavra approval expire`, `cavra approval break-glass`, `cavra approval route`, `cavra approval migrate`, `cavra approval export-notifications`, `cavra approval provider-requests`, `cavra evidence generate-keypair`, `cavra evidence trust-root`, `cavra evidence trust-bundle`, `cavra evidence bundle`, `cavra evidence verify`, `cavra evidence siem-event`, `cavra evidence export-siem`, `cavra evidence retention-policy`, `cavra evidence storage-plan`, `cavra evidence verify-attestation`, `cavra evidence migrate`, `cavra evidence index`, `cavra evidence search`, `cavra init claude-code`, and `cavra demo before-the-agent-acts`.

Approval examples:

```bash
cavra evaluate write_file iam/admin-role.tf --json > /tmp/cavra-decision.json
cavra approval migrate --sqlite .cavra/approvals.db
cavra approval create /tmp/cavra-decision.json --requested-by developer
cavra approval create /tmp/cavra-decision.json --sqlite .cavra/approvals.db --routing-file .cavra/approval-routing.json --requested-by developer
cavra approval route /tmp/cavra-decision.json
cavra approval route /tmp/cavra-decision.json --routing-file .cavra/approval-routing.json
cavra approval list --state pending
cavra approval approve apr_123 --actor platform-security --reason "Scoped IAM change reviewed" --external-ref CHG-123
cavra approval approve apr_123 --actor iam@example.com --actor-claims /tmp/oidc-claims.json --reason "Scoped IAM change reviewed"
cavra approval deny apr_123 --actor platform-security --reason "Missing rollback plan"
cavra approval expire apr_123
cavra approval break-glass /tmp/cavra-decision.json --actor incident-commander --reason "Production recovery" --external-ref INC-777
cavra approval export-notifications apr_123 --output .cavra/approvals/notifications
cavra approval provider-requests apr_123 --provider jira --output .cavra/approvals/provider-requests
```

Evidence integration examples:

```bash
cavra evidence bundle --output .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
cavra evidence generate-keypair --private-key .cavra/keys/evidence-private.pem --public-key .cavra/keys/evidence-public.pem
cavra evidence trust-root .cavra/keys/evidence-public.pem --output .cavra/keys/evidence-trust-root.json --key-id prod-evidence
cavra evidence trust-bundle .cavra/keys/evidence-trust-root.json --output .cavra/keys/evidence-trust-roots.json
cavra evidence verify .cavra/evidence/latest --trust-root .cavra/keys/evidence-trust-roots.json --key-id prod-evidence --minimum-retention-days 2555
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence retention-policy .cavra/evidence/latest --output .cavra/evidence/retention --retention-days 2555
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
cavra evidence verify-attestation .cavra/evidence/latest --output .cavra/evidence/attestation
cavra evidence migrate --sqlite .cavra/evidence/metadata.db
cavra evidence index .cavra/evidence/latest --sqlite .cavra/evidence/metadata.db
cavra evidence search --sqlite .cavra/evidence/metadata.db --min-blocked 1 --limit 25
```
