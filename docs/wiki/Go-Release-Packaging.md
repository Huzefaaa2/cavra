# Go Release Packaging

CAVRA now includes a release packaging workflow for the Go enforcement-plane runtime.

## Delivered

- `.github/workflows/go-release.yml`
- Linux, macOS, and Windows builds for `amd64` and `arm64`.
- `checksums.txt`.
- SPDX-style SBOM: `cavra-runtime.sbom.spdx.json`.
- Release evidence: `release-evidence.json` and `release-evidence.md`.
- Detached Ed25519 signature JSON files when `CAVRA_GO_RELEASE_SIGNING_KEY` is configured.
- Required signing for real release events and non-dry-run manual packaging.
- Dry-run mode for validation before production releases.

## How To Use

```bash
gh workflow run go-release.yml --repo Huzefaaa2/cavra \
  -f version=dry-run \
  -f dry_run=true
```

For production releases, configure `CAVRA_GO_RELEASE_SIGNING_KEY` with an Ed25519 private key PEM and publish a GitHub release.

## User Stories

- As a release manager, I can publish Go binaries with release evidence.
- As a security engineer, I can validate checksums, SBOM metadata, and detached signatures.
- As an enterprise architect, I can review binary distribution controls before air-gapped rollout.

## Enterprise Challenge Solved

Signed Go release packaging gives regulated teams an auditable path from source commit to binary artifact before CAVRA is distributed to local developer machines, CI runners, or restricted environments.

## Next

Attach the signed package directly to GitHub Releases, add verifier CLI support, and add SLSA provenance.
