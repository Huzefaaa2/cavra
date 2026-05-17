# Evidence Hub and Attestation

Phase 3 begins the production Evidence Hub. CAVRA now creates verifier-ready evidence bundles for runtime decisions.

## Delivered Capabilities

- Evidence bundle directory with `manifest.json`.
- SHA-256 checksums for bundle files.
- Optional HMAC manifest signature.
- `evidence.json` with full CAVRA decisions.
- `pr-attestation.md` for pull request review.
- `compliance-mapping.md` for audit and control review.
- `siem-event.json` for SIEM ingestion.
- Bundle verification with checksum and optional signature validation.
- Splunk HEC, Microsoft Sentinel, Datadog, and generic webhook SIEM export payloads.
- S3 Object Lock and Azure immutable blob reference storage plans.

## CLI Usage

Create a bundle:

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
```

Create and sign with a local HMAC key:

```bash
cavra evidence bundle --output .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
```

Verify:

```bash
cavra evidence verify .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
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

## Bundle Files

- `manifest.json`: schema version, file list, checksums, signer, created timestamp, and signature metadata.
- `evidence.json`: complete decision records.
- `pr-attestation.md`: reviewer-oriented summary.
- `compliance-mapping.md`: control-objective mapping.
- `siem-event.json`: machine-readable event for SOC workflows.
- `sandbox-run-summary.json`: compact demo/session summary.

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

## Enterprise Value

Evidence bundles help enterprises prove what happened before an AI-agent action reached code, shell, Git, MCP, cloud, or infrastructure. Reviewers get PR attestation, auditors get compliance mapping, and SOC teams get SIEM-ready events.

## User Stories

- As an auditor, I can verify evidence bundle checksums.
- As a reviewer, I can attach CAVRA PR attestation to AI-assisted changes.
- As a SOC analyst, I can ingest CAVRA decisions into Splunk, Sentinel, Datadog, or webhook workflows.
- As a platform engineer, I can create immutable storage plans without granting CAVRA cloud credentials.

## Next Work

- Add public/private key evidence signatures.
- Add evidence retention policy controls.
- Persist evidence metadata in the API.
