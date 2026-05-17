# Evidence Hub and Attestation

Phase 3 begins the production Evidence Hub. CAVRA now creates verifier-ready evidence bundles for runtime decisions.

## Delivered Capabilities

- Evidence bundle directory with `manifest.json`.
- SHA-256 checksums for bundle files.
- Optional HMAC manifest signature.
- Ed25519 public/private key manifest signatures.
- `evidence.json` with full CAVRA decisions.
- `pr-attestation.md` for pull request review.
- `compliance-mapping.md` for audit and control review.
- `siem-event.json` for SIEM ingestion.
- Bundle verification with checksum and optional signature validation.
- Splunk HEC, Microsoft Sentinel, Datadog, and generic webhook SIEM export payloads.
- Retention policy artifacts with minimum-retention verification.
- S3 Object Lock and Azure immutable blob reference storage plans.
- Evidence metadata indexing for CLI and API workflows.

## CLI Usage

Create a bundle:

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
```

Create and sign with a local HMAC key:

```bash
cavra evidence bundle --output .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
```

Create and sign with an Ed25519 key:

```bash
cavra evidence generate-keypair --private-key .cavra/keys/evidence-private.pem --public-key .cavra/keys/evidence-public.pem
cavra evidence bundle --output .cavra/evidence/latest --private-key .cavra/keys/evidence-private.pem
```

Verify:

```bash
cavra evidence verify .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
cavra evidence verify .cavra/evidence/latest --public-key .cavra/keys/evidence-public.pem --minimum-retention-days 2555
```

Print the SIEM event:

```bash
cavra evidence siem-event .cavra/evidence/latest
```

Export provider-specific SIEM payloads:

```bash
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence export-siem .cavra/evidence/latest --provider splunk --splunk-index cavra_prod
cavra evidence export-siem .cavra/evidence/latest --provider datadog --datadog-service cavra-runtime
```

Create immutable storage reference plans:

```bash
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
```

Export retention and metadata:

```bash
cavra evidence retention-policy .cavra/evidence/latest --output .cavra/evidence/retention --retention-days 2555
cavra evidence index .cavra/evidence/latest --store .cavra/evidence/metadata.json
```

## Bundle Files

- `manifest.json`: schema version, file list, checksums, signer, created timestamp, and signature metadata.
- `evidence.json`: complete decision records.
- `pr-attestation.md`: reviewer-oriented summary.
- `compliance-mapping.md`: control-objective mapping.
- `siem-event.json`: machine-readable event for SOC workflows.
- `sandbox-run-summary.json`: compact demo/session summary.
- `retention-policy.json`: classification, retain-until timestamp, delete protection, and legal-hold state.

## SIEM Export Files

`cavra evidence export-siem` writes provider-specific payloads without requiring live credentials:

- `splunk-hec-events.json`: Splunk HTTP Event Collector event envelope.
- `sentinel-log-analytics.json`: Microsoft Sentinel and Log Analytics record envelope.
- `datadog-events.json`: Datadog event payload with service, status, tags, and attributes.
- `webhook-payload.json`: generic webhook payload for internal pipelines, GRC tooling, or custom collectors.

## Immutable Storage Reference Files

`cavra evidence storage-plan` writes:

- `immutable-storage-plan.json`: machine-readable reference plan for S3 Object Lock and Azure immutable blob storage.
- `immutable-storage-plan.md`: reviewer-friendly storage plan summary.

These files intentionally describe storage requirements and object targets. They do not upload evidence or require cloud credentials.

## API Metadata Persistence

The API now supports evidence metadata persistence through:

- `GET /evidence`
- `POST /evidence`
- `GET /evidence/{session_id}`

By default, metadata is stored in `.cavra/api/evidence-metadata.json`. Operators can set `CAVRA_EVIDENCE_METADATA_STORE` to move the metadata file.

For security, the API does not read arbitrary server-side bundle paths. Use `cavra evidence index` locally to extract metadata from a bundle, then persist the resulting metadata through `POST /evidence`.

## Enterprise Value

Evidence bundles help enterprises prove what happened before an AI-agent action reached code, shell, Git, MCP, cloud, or infrastructure. Reviewers get PR attestation, auditors get compliance mapping, and SOC teams get SIEM-ready events.

## User Stories

- As an auditor, I can verify evidence bundle checksums.
- As an auditor, I can verify Ed25519-signed evidence bundles with a public key.
- As a reviewer, I can attach CAVRA PR attestation to AI-assisted changes.
- As a SOC analyst, I can ingest CAVRA decisions into Splunk, Sentinel, Datadog, or webhook workflows.
- As a platform engineer, I can create immutable storage plans without granting CAVRA cloud credentials.
- As a platform engineer, I can persist evidence metadata for API search and review workflows.

## Next Work

- Harden key trust roots, key IDs, and rotation guidance.
- Add database-backed evidence metadata persistence with pagination and filters.
- Add PR attestation verifier output.
