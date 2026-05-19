# CLI

Primary commands: `cavra version`, `cavra evaluate`, `cavra agent start`, `cavra agent exec`, `cavra agent attest`, `cavra policy list`, `cavra policy validate`, `cavra policy test`, `cavra policy explain`, `cavra policy sign`, `cavra policy verify`, `cavra approval create`, `cavra approval list`, `cavra approval approve`, `cavra approval deny`, `cavra approval expire`, `cavra approval break-glass`, `cavra approval route`, `cavra approval migrate`, `cavra approval export-notifications`, `cavra approval provider-requests`, `cavra approval deliver`, `cavra integration deliver`, `cavra registry agent-register`, `cavra registry agent-list`, `cavra registry profiles`, `cavra registry mcp-register`, `cavra registry mcp-list`, `cavra registry mcp-check`, `cavra registry mcp-classifications`, `cavra registry migrate`, `cavra ops stores`, `cavra ops backup`, `cavra ops restore`, `cavra ops retention-plan`, `cavra evidence generate-keypair`, `cavra evidence trust-root`, `cavra evidence trust-bundle`, `cavra evidence trust-distribution`, `cavra evidence bundle`, `cavra evidence verify`, `cavra evidence siem-event`, `cavra evidence export-siem`, `cavra evidence retention-policy`, `cavra evidence storage-plan`, `cavra evidence verify-attestation`, `cavra evidence migrate`, `cavra evidence index`, `cavra evidence search`, `cavra release verify-go-package`, `cavra release verify-airgap-bundle`, `cavra release validate-upgrade`, `cavra release smoke-installers`, `cavra release capture-rollout`, `cavra release verify-rollout`, `cavra release request-rollout-promotion`, `cavra release execute-rollout-promotion`, `cavra init claude-code`, and `cavra demo before-the-agent-acts`.

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
cavra approval approve apr_123 --actor iam@example.com --actor-token /tmp/oidc.jwt --oidc-config .cavra/approval-oidc.json --rbac-file .cavra/approval-rbac.yaml --reason "Signed identity verified"
cavra approval deny apr_123 --actor platform-security --reason "Missing rollback plan"
cavra approval expire apr_123
cavra approval break-glass /tmp/cavra-decision.json --actor incident-commander --reason "Production recovery" --external-ref INC-777
cavra approval export-notifications apr_123 --output .cavra/approvals/notifications
cavra approval provider-requests apr_123 --provider jira --output .cavra/approvals/provider-requests
cavra approval deliver apr_123 --config .cavra/approval-providers.yaml --provider jira --retries 2 --timeout-seconds 10 --output .cavra/approvals/deliveries
```

Evidence integration examples:

```bash
cavra evidence bundle --output .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
cavra evidence generate-keypair --private-key .cavra/keys/evidence-private.pem --public-key .cavra/keys/evidence-public.pem
cavra evidence trust-root .cavra/keys/evidence-public.pem --output .cavra/keys/evidence-trust-root.json --key-id prod-evidence
cavra evidence trust-bundle .cavra/keys/evidence-trust-root.json --output .cavra/keys/evidence-trust-roots.json
cavra evidence trust-distribution .cavra/keys/evidence-trust-root.json --output .cavra/keys/trust-root-distribution --distribution-id prod-trust-roots-2026-q2 --channel source-control --channel offline-media
cavra evidence verify .cavra/evidence/latest --trust-root .cavra/keys/evidence-trust-roots.json --key-id prod-evidence --minimum-retention-days 2555
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence retention-policy .cavra/evidence/latest --output .cavra/evidence/retention --retention-days 2555
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
cavra evidence verify-attestation .cavra/evidence/latest --output .cavra/evidence/attestation
cavra evidence migrate --sqlite .cavra/evidence/metadata.db
cavra evidence index .cavra/evidence/latest --sqlite .cavra/evidence/metadata.db
cavra evidence search --sqlite .cavra/evidence/metadata.db --min-blocked 1 --limit 25
cavra evidence search --sqlite .cavra/evidence/metadata.db --metadata-kind managed-endpoint-rollout --rollout-status staged --environment production --deployment-target github-actions-linux-amd64-runner
cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-v0.1.0.zip
cavra release validate-upgrade go/cavra-runtime/dist/go-runtime-v0.1.0 go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1
cavra release smoke-installers go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 --json
cavra release capture-rollout go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 --deployment-id github-actions-linux-amd64-runner --change-record CHG-123 --json
cavra release verify-rollout .cavra/release/rollout --metadata-json .cavra/evidence/metadata.json --sqlite .cavra/evidence/metadata.db --json
cavra release request-rollout-promotion .cavra/release/rollout --target-ring production --approval-store .cavra/api/approvals.json --json
cavra release execute-rollout-promotion .cavra/release/rollout-promotion/rollout-promotion-approval-request.json --approval-store .cavra/api/approvals.json --json
```

`cavra evidence verify-attestation` exits with a nonzero status when `pr-attestation.md` is missing or does not match the bundle evidence, so CI/CD systems can use it as a required merge check.

Connector delivery example:

```bash
cavra integration deliver .cavra/evidence/latest/siem-event.json --config .cavra/connectors.json --provider splunk
```

Registry examples:

```bash
cavra registry agent-register codex-agent --vendor OpenAI --capability code_edit --repository payments/api --owner "Platform AI"
cavra registry agent-register claude-code --vendor Anthropic --capability mcp_tool_call --sqlite .cavra/registry.db
cavra registry agent-list --owner "Platform AI"
cavra registry profiles
cavra registry mcp-register github-mcp --trust-tier approved --approval-state approved --capability repository --tool create_pull_request --owner "Developer Platform"
cavra registry mcp-register filesystem-mcp --trust-tier approved --approval-state approved --capability filesystem --tool read_file --sqlite .cavra/registry.db
cavra registry mcp-list --trust-tier approved
cavra registry mcp-check github-mcp create_pull_request --capability repository
cavra registry mcp-classifications --capability cloud
cavra registry migrate --sqlite .cavra/registry.db
```

## Persistent API Operations

```bash
cavra ops stores
cavra ops backup --output .cavra/backups/$(date +%Y%m%d)
cavra ops restore .cavra/backups/20260518/manifest.json --target-dir /tmp/cavra-restore-test
cavra ops retention-plan --output .cavra/operations/retention --retention-days 2555 --legal-hold
```
