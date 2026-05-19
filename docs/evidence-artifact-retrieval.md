# Evidence Artifact Retrieval

CAVRA can expose read-only evidence artifacts for indexed sessions and managed endpoint rollout records through a governed artifact root. This gives reviewers and auditors direct access to attestations, manifests, evidence JSON, SIEM events, retention policy files, rollout evidence, and downloadable ZIP bundles without allowing arbitrary server-side file reads.

## Configuration

Set the API artifact root:

```bash
export CAVRA_EVIDENCE_ARTIFACT_ROOT=.cavra/evidence/artifacts
uvicorn cavra.api:app --reload
```

Each indexed session maps to one directory:

```text
.cavra/evidence/artifacts/
  api-session/
    manifest.json
    evidence.json
    pr-attestation.md
    compliance-mapping.md
    siem-event.json
    sandbox-run-summary.json
    retention-policy.json
```

Managed endpoint rollout records use the same endpoints, but their metadata can point to a verified rollout evidence directory under the configured root:

```text
.cavra/evidence/artifacts/
  rollout-1/
    managed-endpoint-rollout-evidence.json
    managed-endpoint-rollout-evidence.md
    checksums.txt
```

The session must also exist in evidence metadata through `POST /evidence`, `cavra evidence index`, or the SQLite metadata store.

## API

- `GET /evidence/{session_id}/artifacts`: list available artifacts, media types, sizes, checksums, descriptions, and download URLs.
- `GET /evidence/{session_id}/artifacts/{artifact_name}`: download one allowlisted artifact.
- `GET /evidence/{session_id}/artifact-bundle`: download a ZIP containing all available allowlisted artifacts.

Downloads include `x-cavra-artifact-sha256` so clients can log or verify the returned payload.

For metadata records with `metadata_kind=managed-endpoint-rollout`, CAVRA serves only the rollout allowlist: `managed-endpoint-rollout-evidence.json`, `managed-endpoint-rollout-evidence.md`, and `checksums.txt`.

Rollout artifact listings also include `rollout_artifact_integrity` and `promotion_readiness`. Integrity verifies rollout evidence files against `checksums.txt`, reports missing, unchecked, and mismatched artifacts, and blocks promotion readiness when checksums do not verify.

## Security Boundary

- The API never accepts arbitrary bundle paths.
- Artifact retrieval is disabled unless `CAVRA_EVIDENCE_ARTIFACT_ROOT` is configured.
- A metadata record is required before artifacts are served.
- Only known bundle filenames are downloadable.
- Session IDs, rollout `bundle_dir` values, and artifact paths are resolved under the configured root and traversal is rejected.
- Rollout metadata cannot expose a directory outside `CAVRA_EVIDENCE_ARTIFACT_ROOT`.

## User Stories

- As an auditor, I can download the manifest and evidence bundle for a reviewed AI-agent session.
- As a pull request reviewer, I can retrieve the PR attestation from the same console used for evidence search.
- As an endpoint engineering owner, I can retrieve verified rollout evidence and checksums for a managed endpoint deployment record.
- As a release manager, I can see whether rollout artifacts are checksum-verified and ready for promotion review.
- As a platform engineer, I can expose artifact downloads from a controlled evidence root without granting the API broad filesystem access.

## Enterprise Value

Artifact retrieval closes the loop between searchable metadata and audit-ready evidence. Teams can search for risky sessions, open the artifact panel, download the attestation or full bundle, and attach it to change records, audit requests, or incident reviews.
