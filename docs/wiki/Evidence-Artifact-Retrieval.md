# Evidence Artifact Retrieval

CAVRA exposes read-only evidence artifacts for indexed sessions and managed endpoint rollout records when `CAVRA_EVIDENCE_ARTIFACT_ROOT` is configured.

## Endpoints

- `GET /evidence/{session_id}/artifacts`
- `GET /evidence/{session_id}/artifacts/{artifact_name}`
- `GET /evidence/{session_id}/artifact-bundle`

## How It Works

The artifact root contains one directory per evidence session or verified rollout record. The session or rollout must exist in metadata before files are served. The API only serves known evidence bundle filenames such as `manifest.json`, `evidence.json`, `pr-attestation.md`, `compliance-mapping.md`, `siem-event.json`, `sandbox-run-summary.json`, and `retention-policy.json`.

For `metadata_kind=managed-endpoint-rollout`, the API serves only `managed-endpoint-rollout-evidence.json`, `managed-endpoint-rollout-evidence.md`, and `checksums.txt`. The rollout `bundle_dir` must resolve inside the configured artifact root.

Downloads include `x-cavra-artifact-sha256` for audit logging and client-side verification.

Rollout artifact listings include checksum integrity and promotion readiness. The console shows whether rollout evidence is verified, incomplete, blocked, or ready before a release owner promotes to the next deployment ring.

## Security Boundary

- No arbitrary server-side paths.
- Disabled unless `CAVRA_EVIDENCE_ARTIFACT_ROOT` is set.
- Metadata record required.
- Allowlisted artifact names only.
- Path traversal rejected.
- Rollout bundle directories outside the configured artifact root are rejected.

## User Stories

- As an auditor, I can download a full CAVRA evidence bundle for a session.
- As a reviewer, I can retrieve the PR attestation directly from the console.
- As an endpoint engineering owner, I can download verified rollout evidence and checksums for a managed endpoint deployment record.
- As a release manager, I can see rollout artifact integrity and promotion readiness before approving the next ring.
- As a platform engineer, I can expose evidence from a controlled root without granting broad filesystem access.

## Enterprise Value

Artifact retrieval connects metadata search to audit-ready evidence. Teams can find a session, inspect risk, download the attestation or bundle, and attach it to change records, incident reviews, or compliance requests.
