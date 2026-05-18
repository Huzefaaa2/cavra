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
- Live connector execution hooks for SIEM, ITSM, ChatOps, and generic webhook destinations.
- Immutable storage reference plans for S3 Object Lock and Azure immutable blob.
- Evidence metadata indexing through CLI and API workflows.
- SQLite-backed evidence search with filters and pagination.
- PR attestation verifier reports.
- Governed artifact retrieval APIs for indexed sessions.

## Commands

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
cavra evidence verify .cavra/evidence/latest
cavra evidence siem-event .cavra/evidence/latest
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
cavra integration deliver .cavra/evidence/latest/siem-event.json --config .cavra/connectors.json --provider splunk
```

## Enterprise Value

Evidence bundles turn pre-action runtime decisions into artifacts that reviewers, auditors, and SOC teams can inspect. The manifest includes checksums and signature metadata so tampering can be detected. SIEM exports let teams route CAVRA decisions into existing SOC pipelines, and connector execution hooks let controlled deployments deliver those events with credential-redacted evidence.

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
- `GET /evidence/{session_id}/artifacts`
- `GET /evidence/{session_id}/artifacts/{artifact_name}`
- `GET /evidence/{session_id}/artifact-bundle`

For security, the API does not read arbitrary server-side bundle paths. Use `cavra evidence index` locally to extract metadata from a bundle, then persist it with `POST /evidence`.

Set `CAVRA_EVIDENCE_METADATA_DB` to use SQLite-backed metadata search with filters and pagination. JSON metadata mode now supports the same API filter and pagination shape for local deployments.

Set `CAVRA_EVIDENCE_ARTIFACT_ROOT` to enable read-only artifact retrieval from a governed root. The API requires a metadata record, only serves known bundle filenames, rejects traversal, and returns checksum headers on downloads.

## Console Views

The hosted console surface includes evidence metadata search, evidence artifact downloads, PR attestation verification, and operational readiness indicators.

Configure deployed console/API topologies with `CAVRA_PUBLIC_API_BASE_URL`, `CAVRA_CORS_ORIGINS`, and `GET /console/config`.

## Next Work

- Azure DevOps required-check template.
- Immutable evidence store deployment reference.
- OIDC/RBAC deployment reference bundles.
