# Evidence Hub and Attestation

Phase 3 is in progress.

## What Changed

CAVRA now creates verifier-ready evidence bundles:

- `manifest.json`
- `evidence.json`
- `pr-attestation.md`
- `compliance-mapping.md`
- `siem-event.json`
- `sandbox-run-summary.json`
- `retention-policy.json`
- HMAC or Ed25519 manifest signatures.
- Key IDs and trust-root verification.
- Provider-specific SIEM payloads for Splunk, Sentinel, Datadog, and webhooks.
- Immutable storage reference plans for S3 Object Lock and Azure immutable blob.
- Evidence metadata indexing through CLI and API workflows.
- SQLite-backed evidence search with filters and pagination.
- PR attestation verifier reports.

## Commands

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
cavra evidence verify .cavra/evidence/latest
cavra evidence siem-event .cavra/evidence/latest
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

## Enterprise Value

Evidence bundles turn pre-action runtime decisions into artifacts that reviewers, auditors, and SOC teams can inspect. The manifest includes checksums and signature metadata so tampering can be detected. SIEM exports let teams route CAVRA decisions into existing SOC pipelines without giving the CLI live SIEM credentials.

## Export Files

- `splunk-hec-events.json`
- `sentinel-log-analytics.json`
- `datadog-events.json`
- `webhook-payload.json`
- `retention-policy.json`
- `retention-policy.md`
- `immutable-storage-plan.json`
- `immutable-storage-plan.md`
- `pr-attestation-verification.json`
- `pr-attestation-verification.md`

## API Metadata

- `GET /evidence`
- `POST /evidence`
- `GET /evidence/{session_id}`

For security, the API does not read arbitrary server-side bundle paths. Use `cavra evidence index` locally to extract metadata from a bundle, then persist it with `POST /evidence`.

Set `CAVRA_EVIDENCE_METADATA_DB` to use SQLite-backed metadata search with filters and pagination.

## Next Work

- Hosted console views for evidence search and attestation verification.
- Production database migration path for evidence metadata.
- Automated trust-root distribution guidance for enterprise deployments.
