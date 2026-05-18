# Evidence Hub and Attestation

Phase 3 begins the production Evidence Hub. CAVRA now creates verifier-ready evidence bundles for runtime decisions.

## Delivered Capabilities

- Evidence bundle directory with `manifest.json`.
- SHA-256 checksums for bundle files.
- Optional HMAC manifest signature.
- Ed25519 public/private key manifest signatures.
- Key IDs and trust-root verification.
- Trust-root bundle generation for enterprise distribution.
- `evidence.json` with full CAVRA decisions.
- `pr-attestation.md` for pull request review.
- `compliance-mapping.md` for audit and control review.
- `siem-event.json` for SIEM ingestion.
- Bundle verification with checksum and optional signature validation.
- Splunk HEC, Microsoft Sentinel, Datadog, and generic webhook SIEM export payloads.
- Retention policy artifacts with minimum-retention verification.
- S3 Object Lock and Azure immutable blob reference storage plans.
- Evidence metadata indexing for CLI and API workflows.
- SQLite-backed evidence search with filters and pagination.
- PR attestation verifier reports.
- Console API wiring for same-origin and cross-origin deployments.
- Idempotent SQLite metadata migrations.
- Hosted evidence artifact retrieval for indexed sessions through a governed artifact root.

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
cavra evidence trust-root .cavra/keys/evidence-public.pem --output .cavra/keys/evidence-trust-root.json --key-id prod-evidence
cavra evidence trust-bundle .cavra/keys/evidence-trust-root.json --output .cavra/keys/evidence-trust-roots.json
cavra evidence bundle --output .cavra/evidence/latest --private-key .cavra/keys/evidence-private.pem
```

Verify:

```bash
cavra evidence verify .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
cavra evidence verify .cavra/evidence/latest --public-key .cavra/keys/evidence-public.pem --minimum-retention-days 2555
cavra evidence verify .cavra/evidence/latest --trust-root .cavra/keys/evidence-trust-roots.json --key-id prod-evidence
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
cavra evidence verify-attestation .cavra/evidence/latest --output .cavra/evidence/attestation
cavra evidence migrate --sqlite .cavra/evidence/metadata.db
cavra evidence index .cavra/evidence/latest --sqlite .cavra/evidence/metadata.db
cavra evidence search --sqlite .cavra/evidence/metadata.db --min-blocked 1 --limit 25
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
- `pr-attestation-verification.json`: machine-readable attestation verification report.
- `pr-attestation-verification.md`: reviewer-friendly attestation verification report.

These files intentionally describe storage requirements and object targets. They do not upload evidence or require cloud credentials. Deployable operator-owned references now live in `examples/immutable-storage/aws-s3-object-lock` and `examples/immutable-storage/azure-blob-immutability`; see [immutable evidence storage](immutable-evidence-storage.md).

## API Metadata Persistence

The API now supports evidence metadata persistence through:

- `GET /evidence`
- `POST /evidence`
- `GET /evidence/{session_id}`
- `GET /evidence/{session_id}/artifacts`
- `GET /evidence/{session_id}/artifacts/{artifact_name}`
- `GET /evidence/{session_id}/artifact-bundle`

By default, metadata is stored in `.cavra/api/evidence-metadata.json`. Operators can set `CAVRA_EVIDENCE_METADATA_STORE` to move the metadata file. JSON mode supports the same response shape and filters as SQLite mode for local deployments.

For searchable metadata with filters and pagination, set `CAVRA_EVIDENCE_METADATA_DB` to a SQLite database path. The API then returns a paginated object from `GET /evidence` with filters such as `session_id`, `signer`, `min_blocked`, `has_approvals`, `limit`, and `offset`.

For security, the API does not read arbitrary server-side bundle paths. Use `cavra evidence index` locally to extract metadata from a bundle, then persist the resulting metadata through `POST /evidence`.

Set `CAVRA_EVIDENCE_ARTIFACT_ROOT` to enable artifact retrieval. The API only serves allowlisted bundle files from `CAVRA_EVIDENCE_ARTIFACT_ROOT/<session_id>/`, requires a matching evidence metadata record, rejects traversal, and returns a checksum header on artifact downloads.

## Console Views

The hosted console surface in `apps/sandbox-ui` now includes:

- Evidence metadata search.
- Evidence artifact listing and downloads.
- PR attestation verification summary.
- Operational readiness indicators for trust roots, SQLite search, attestation verification, and migrations.

The console reads `GET /console/config` when available. Set `CAVRA_PUBLIC_API_BASE_URL` and `CAVRA_CORS_ORIGINS` for cross-origin deployments, or set `window.CAVRA_API_BASE` before `sandbox.js` loads.

## Enterprise Value

Evidence bundles help enterprises prove what happened before an AI-agent action reached code, shell, Git, MCP, cloud, or infrastructure. Reviewers get PR attestation, auditors get compliance mapping, and SOC teams get SIEM-ready events.

## User Stories

- As an auditor, I can verify evidence bundle checksums.
- As an auditor, I can verify Ed25519-signed evidence bundles with a public key.
- As an auditor, I can verify evidence through an approved trust root and key ID.
- As a reviewer, I can attach CAVRA PR attestation to AI-assisted changes.
- As a reviewer, I can generate a PR attestation verification report.
- As a SOC analyst, I can ingest CAVRA decisions into Splunk, Sentinel, Datadog, or webhook workflows.
- As a SOC analyst, I can deliver CAVRA evidence events through configured SIEM, ITSM, and ChatOps connector hooks while retaining redacted delivery evidence.
- As a platform engineer, I can create immutable storage plans without granting CAVRA cloud credentials.
- As a platform engineer, I can persist evidence metadata for API search and review workflows.
- As a platform engineer, I can distribute one approved trust-root bundle to CI, reviewers, API services, and auditors.

## Next Work

- Add OIDC/RBAC deployment reference bundles.
