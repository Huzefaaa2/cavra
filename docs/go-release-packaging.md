# Go Release Packaging

CAVRA includes a GitHub Actions workflow for packaging the Go enforcement-plane runtime with checksums, SPDX-style SBOM metadata, SLSA provenance, detached Ed25519 signatures, and release evidence.

## Workflow

Workflow file: `.github/workflows/go-release.yml`

The workflow:

- Runs on manual dispatch for dry-run packaging and on published GitHub releases.
- Builds `cavra-runtime` for Linux, macOS, and Windows on `amd64` and `arm64`.
- Uses `go build -trimpath -ldflags="-s -w"` for reproducible, stripped binaries.
- Exports Go module metadata with `go list -m -json all`.
- Generates `cavra-runtime.sbom.spdx.json`.
- Generates `cavra-runtime.provenance.intoto.json` using an in-toto Statement and SLSA provenance predicate.
- Generates `checksums.txt`.
- Generates `release-evidence.json` and `release-evidence.md`.
- Signs release artifacts with detached Ed25519 signature JSON files when `CAVRA_GO_RELEASE_SIGNING_KEY` is configured.
- Requires signing material for real release events or non-dry-run manual dispatches.
- Creates a distributable zip named `cavra-go-runtime-<version>.zip`.
- Attaches the signed zip directly to the GitHub Release on published release events.
- Uploads the full package directory as the CI artifact `cavra-go-runtime-release-package`.

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
3. Download `cavra-go-runtime-<version>.zip` from the GitHub Release assets or the `cavra-go-runtime-release-package` workflow artifact.
4. Verify the package with the CAVRA CLI.

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-v0.1.0
```

For unsigned dry-run artifacts only:

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-dry-run --allow-unsigned
```

Generate an Ed25519 keypair with CAVRA:

```bash
cavra evidence generate-keypair \
  --private-key .cavra/keys/go-release-private.pem \
  --public-key .cavra/keys/go-release-public.pem
```

Do not commit private keys. Store production signing keys in GitHub Actions secrets or an enterprise secret manager.

## User Stories

- As a release manager, I can publish Go runtime binaries with checksums, SBOM, SLSA provenance, signatures, and evidence.
- As a security engineer, I can verify that binaries map to a specific commit, ref, and dependency set.
- As an enterprise architect, I can review a path toward air-gapped runtime distribution.
- As an auditor, I can run a single CLI verifier and see checksum, evidence, and signature failures before approval.

## Enterprise Challenge Solved

Enterprise buyers require release integrity before allowing local enforcement binaries onto developer laptops, CI runners, or air-gapped environments. The Go release package turns runtime binaries into auditable artifacts with checksums, SBOM metadata, SLSA provenance, detached signatures, CAVRA release evidence, release-asset attachment, and a local verifier command.

## Next Work

1. Add public telemetry-free demo run counters from persisted backend metadata.
2. Add SLSA keyless attestations with GitHub OIDC after the release process stabilizes.
3. Add air-gapped installer bundle verification.
