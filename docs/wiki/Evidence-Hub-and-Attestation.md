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
- Provider-specific SIEM payloads for Splunk, Sentinel, Datadog, and webhooks.
- Immutable storage reference plans for S3 Object Lock and Azure immutable blob.

## Commands

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
cavra evidence verify .cavra/evidence/latest
cavra evidence siem-event .cavra/evidence/latest
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
```

## Enterprise Value

Evidence bundles turn pre-action runtime decisions into artifacts that reviewers, auditors, and SOC teams can inspect. The manifest includes checksums and signature metadata so tampering can be detected. SIEM exports let teams route CAVRA decisions into existing SOC pipelines without giving the CLI live SIEM credentials.

## Export Files

- `splunk-hec-events.json`
- `sentinel-log-analytics.json`
- `datadog-events.json`
- `webhook-payload.json`
- `immutable-storage-plan.json`
- `immutable-storage-plan.md`

## Next Work

- Public/private key evidence signatures.
- Evidence retention controls.
- Evidence metadata persistence in the API.
