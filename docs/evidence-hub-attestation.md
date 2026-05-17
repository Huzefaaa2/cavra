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

## Bundle Files

- `manifest.json`: schema version, file list, checksums, signer, created timestamp, and signature metadata.
- `evidence.json`: complete decision records.
- `pr-attestation.md`: reviewer-oriented summary.
- `compliance-mapping.md`: control-objective mapping.
- `siem-event.json`: machine-readable event for SOC workflows.
- `sandbox-run-summary.json`: compact demo/session summary.

## Enterprise Value

Evidence bundles help enterprises prove what happened before an AI-agent action reached code, shell, Git, MCP, cloud, or infrastructure. Reviewers get PR attestation, auditors get compliance mapping, and SOC teams get SIEM-ready events.

## User Stories

- As an auditor, I can verify evidence bundle checksums.
- As a reviewer, I can attach CAVRA PR attestation to AI-assisted changes.
- As a SOC analyst, I can ingest CAVRA decisions into SIEM workflows.
- As a platform engineer, I can produce evidence without granting CAVRA access to external systems.

## Next Work

- Add public/private key evidence signatures.
- Add immutable evidence store exporters for S3 Object Lock and Azure immutable blob.
- Add Splunk, Sentinel, Datadog, and generic webhook exporter commands.
- Persist evidence metadata in the API.
