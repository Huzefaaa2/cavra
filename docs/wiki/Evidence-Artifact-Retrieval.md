# Evidence Artifact Retrieval

CAVRA exposes read-only evidence bundle artifacts for indexed sessions when `CAVRA_EVIDENCE_ARTIFACT_ROOT` is configured.

## Endpoints

- `GET /evidence/{session_id}/artifacts`
- `GET /evidence/{session_id}/artifacts/{artifact_name}`
- `GET /evidence/{session_id}/artifact-bundle`

## How It Works

The artifact root contains one directory per evidence session. The session must exist in metadata before files are served. The API only serves known evidence bundle filenames such as `manifest.json`, `evidence.json`, `pr-attestation.md`, `compliance-mapping.md`, `siem-event.json`, `sandbox-run-summary.json`, and `retention-policy.json`.

Downloads include `x-cavra-artifact-sha256` for audit logging and client-side verification.

## Security Boundary

- No arbitrary server-side paths.
- Disabled unless `CAVRA_EVIDENCE_ARTIFACT_ROOT` is set.
- Metadata record required.
- Allowlisted artifact names only.
- Path traversal rejected.

## User Stories

- As an auditor, I can download a full CAVRA evidence bundle for a session.
- As a reviewer, I can retrieve the PR attestation directly from the console.
- As a platform engineer, I can expose evidence from a controlled root without granting broad filesystem access.

## Enterprise Value

Artifact retrieval connects metadata search to audit-ready evidence. Teams can find a session, inspect risk, download the attestation or bundle, and attach it to change records, incident reviews, or compliance requests.
