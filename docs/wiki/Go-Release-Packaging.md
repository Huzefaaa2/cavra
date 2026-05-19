# Go Release Packaging

CAVRA now includes a release packaging workflow for the Go enforcement-plane runtime.

## Delivered

- `.github/workflows/go-release.yml`
- Linux, macOS, and Windows builds for `amd64` and `arm64`.
- `checksums.txt`.
- SPDX-style SBOM: `cavra-runtime.sbom.spdx.json`.
- SLSA provenance: `cavra-runtime.provenance.intoto.json`.
- Managed endpoint deployment manifest: `cavra-runtime.endpoint-deployment.json`.
- Managed endpoint rollout evidence: `managed-endpoint-rollout-evidence.json`, `managed-endpoint-rollout-evidence.md`, and `checksums.txt`.
- Governed rollout artifact retrieval through the `/evidence/{session_id}/artifacts` and `/evidence/{session_id}/artifact-bundle` APIs.
- Rollout artifact integrity status and promotion readiness indicators in the evidence API and console artifact panel.
- Release evidence: `release-evidence.json` and `release-evidence.md`.
- Detached Ed25519 signature JSON files when `CAVRA_GO_RELEASE_SIGNING_KEY` is configured.
- Required signing for real release events and non-dry-run manual packaging.
- Dry-run mode for validation before production releases.
- GitHub Release asset attachment for signed production packages.
- CLI verification with `cavra release verify-go-package`.

## How To Use

```bash
gh workflow run go-release.yml --repo Huzefaaa2/cavra \
  -f version=dry-run \
  -f dry_run=true
```

For production releases, configure `CAVRA_GO_RELEASE_SIGNING_KEY` with an Ed25519 private key PEM and publish a GitHub release. The workflow attaches `cavra-go-runtime-<version>.zip` to the release.

Verify a signed package:

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-v0.1.0
```

Inspect managed endpoint deployment guidance:

```bash
jq '.deployment_targets[] | {id, surface, platform, installer_target}' \
  go/cavra-runtime/dist/go-runtime-v0.1.0/cavra-runtime.endpoint-deployment.json
```

The endpoint deployment manifest maps signed runtime binaries to approved CI runner and developer workstation channels. Package verification requires the manifest and validates its binary references, rollout controls, and installer smoke-test guidance before approval.

Capture rollout evidence:

```bash
cavra release capture-rollout \
  go/cavra-runtime/dist/go-runtime-v0.1.0 \
  --deployment-id github-actions-linux-amd64-runner \
  --change-record CHG-123
```

The rollout command verifies the signed package, selects approved deployment targets, and writes change-record evidence for endpoint rollout.

Verify and index rollout evidence:

```bash
cavra release verify-rollout \
  .cavra/release/rollout \
  --metadata-json .cavra/evidence/metadata.json \
  --sqlite .cavra/evidence/metadata.db
```

The verification command checks rollout checksums, source package checksums, package verification status, selected targets, and rollout controls before indexing metadata by rollout ID.

Search rollout evidence:

```bash
cavra evidence search \
  --sqlite .cavra/evidence/metadata.db \
  --metadata-kind managed-endpoint-rollout \
  --rollout-status staged \
  --deployment-target github-actions-linux-amd64-runner
```

The CLI, `/evidence` API, and console Evidence Search view support rollout filters for kind, status, environment, and deployment target.

Download rollout artifacts after configuring `CAVRA_EVIDENCE_ARTIFACT_ROOT` to contain the indexed rollout directory:

```bash
curl http://127.0.0.1:8000/evidence/chg-123-v0.1.0/artifacts
curl -OJ http://127.0.0.1:8000/evidence/chg-123-v0.1.0/artifacts/managed-endpoint-rollout-evidence.json
curl -OJ http://127.0.0.1:8000/evidence/chg-123-v0.1.0/artifact-bundle
```

The artifact listing reports checksum integrity and promotion readiness so release owners can distinguish verified, incomplete, blocked, and ready rollout records.

Verify an unsigned dry-run package:

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-dry-run --allow-unsigned
```

## User Stories

- As a release manager, I can publish Go binaries with release evidence, provenance, and GitHub keyless attestations.
- As a security engineer, I can validate checksums, SBOM metadata, SLSA provenance, detached signatures, and `gh attestation verify` results.
- As an enterprise architect, I can verify an air-gapped runtime zip before restricted-network transfer.
- As an endpoint engineering owner, I can approve deployment channels for CI runners and developer workstations before rollout.
- As an endpoint engineering owner, I can capture rollout status and change-record evidence for approved endpoint channels.
- As an endpoint engineering owner, I can verify rollout evidence and index it for audit retrieval.
- As an endpoint engineering owner, I can find rollout evidence by environment, status, and target from the CLI, API, or console.
- As an endpoint engineering owner, I can download the verified rollout evidence files and checksum manifest from a governed artifact root.
- As a release manager, I can see whether rollout evidence is ready for the next deployment ring.
- As an auditor, I can run a local verifier before approving runtime distribution.

## Enterprise Challenge Solved

Signed Go release packaging gives regulated teams an auditable path from source commit to binary artifact before CAVRA is distributed to local developer machines, CI runners, or restricted environments. Release attachment, SLSA provenance, signed installer metadata, managed endpoint deployment manifests, rollout evidence capture, rollout evidence verification and indexing, rollout evidence search filters, governed rollout artifact retrieval, rollout artifact integrity status, promotion readiness indicators, console/API views, installer smoke validation, GitHub OIDC-backed keyless attestations, offline trust bootstrap metadata, air-gapped zip verification, release-candidate upgrade validation, and CLI verification reduce manual release-review steps.

## Next

Add signed promotion approval requests for endpoint rollout readiness.
