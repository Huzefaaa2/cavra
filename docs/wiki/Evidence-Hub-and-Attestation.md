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
- Provider-specific SIEM payloads for Splunk, Sentinel, Datadog, and webhooks.
- Immutable storage reference plans for S3 Object Lock and Azure immutable blob.
- Evidence metadata indexing through CLI and API workflows.

## Commands

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
cavra evidence verify .cavra/evidence/latest
cavra evidence siem-event .cavra/evidence/latest
cavra evidence generate-keypair --private-key .cavra/keys/evidence-private.pem --public-key .cavra/keys/evidence-public.pem
cavra evidence verify .cavra/evidence/latest --public-key .cavra/keys/evidence-public.pem --minimum-retention-days 2555
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence retention-policy .cavra/evidence/latest --output .cavra/evidence/retention --retention-days 2555
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
cavra evidence index .cavra/evidence/latest --store .cavra/evidence/metadata.json
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

## API Metadata

- `GET /evidence`
- `POST /evidence`
- `GET /evidence/{session_id}`
- `POST /evidence/index-bundle`

## Next Work

- Key trust roots, key IDs, and rotation guidance.
- Database-backed evidence metadata persistence with pagination and filters.
- PR attestation verifier output.
