# Go Release Packaging

CAVRA includes a GitHub Actions workflow for packaging the Go enforcement-plane runtime with checksums, SPDX-style SBOM metadata, detached Ed25519 signatures, and release evidence.

## Workflow

Workflow file: `.github/workflows/go-release.yml`

The workflow:

- Runs on manual dispatch for dry-run packaging and on published GitHub releases.
- Builds `cavra-runtime` for Linux, macOS, and Windows on `amd64` and `arm64`.
- Uses `go build -trimpath -ldflags="-s -w"` for reproducible, stripped binaries.
- Exports Go module metadata with `go list -m -json all`.
- Generates `cavra-runtime.sbom.spdx.json`.
- Generates `checksums.txt`.
- Generates `release-evidence.json` and `release-evidence.md`.
- Signs release artifacts with detached Ed25519 signature JSON files when `CAVRA_GO_RELEASE_SIGNING_KEY` is configured.
- Requires signing material for real release events or non-dry-run manual dispatches.
- Uploads the full package as `cavra-go-runtime-release-package`.

## How To Use

Dry run:

```bash
gh workflow run go-release.yml --repo Huzefaaa2/cavra \
  -f version=dry-run \
  -f dry_run=true
```

Production release:

1. Configure repository secret `CAVRA_GO_RELEASE_SIGNING_KEY` with an Ed25519 private key PEM.
2. Publish a GitHub release.
3. Download the `cavra-go-runtime-release-package` artifact.
4. Verify `checksums.txt`, signature JSON files, SBOM, and `release-evidence.json`.

Generate an Ed25519 keypair with CAVRA:

```bash
cavra evidence generate-keypair \
  --private-key .cavra/keys/go-release-private.pem \
  --public-key .cavra/keys/go-release-public.pem
```

Do not commit private keys. Store production signing keys in GitHub Actions secrets or an enterprise secret manager.

## User Stories

- As a release manager, I can publish Go runtime binaries with checksums, SBOM, signatures, and evidence.
- As a security engineer, I can verify that binaries map to a specific commit, ref, and dependency set.
- As an enterprise architect, I can review a path toward air-gapped runtime distribution.

## Enterprise Challenge Solved

Enterprise buyers require release integrity before allowing local enforcement binaries onto developer laptops, CI runners, or air-gapped environments. The Go release package turns runtime binaries into auditable artifacts with checksums, SBOM metadata, detached signatures, and CAVRA release evidence.

## Next Work

1. Attach signed Go release packages directly to GitHub Releases.
2. Add verifier CLI support for Go release signatures.
3. Add SLSA provenance after the release process stabilizes.
