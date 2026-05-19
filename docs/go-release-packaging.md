# Go Release Packaging

CAVRA includes a GitHub Actions workflow for packaging the Go enforcement-plane runtime with checksums, SPDX-style SBOM metadata, signed installer metadata, installer smoke validation, SLSA provenance, detached Ed25519 signatures, GitHub keyless OIDC attestations, offline trust bootstrap metadata, air-gapped zip verification, release-candidate upgrade validation, and release evidence.

## Workflow

Workflow file: `.github/workflows/go-release.yml`

The workflow:

- Runs on manual dispatch for dry-run packaging and on published GitHub releases.
- Builds `cavra-runtime` for Linux, macOS, and Windows on `amd64` and `arm64`.
- Uses `go build -trimpath -ldflags="-s -w"` for reproducible, stripped binaries.
- Exports Go module metadata with `go list -m -json all`.
- Generates `cavra-runtime.sbom.spdx.json`.
- Generates `cavra-runtime.installers.json` with per-platform install metadata, binary checksums, install paths, and verification commands.
- Generates `cavra-runtime.provenance.intoto.json` using an in-toto Statement and SLSA provenance predicate.
- Generates `offline-trust-root-bootstrap.json` with offline operator notes and verification commands.
- Generates `checksums.txt`.
- Generates `release-evidence.json` and `release-evidence.md`.
- Signs release artifacts with detached Ed25519 signature JSON files when `CAVRA_GO_RELEASE_SIGNING_KEY` is configured.
- Requires signing material for real release events or non-dry-run manual dispatches.
- Creates a distributable zip named `cavra-go-runtime-<version>.zip`.
- Generates a GitHub keyless attestation for `cavra-go-runtime-<version>.zip` using the workflow's OIDC identity through `actions/attest@v4`.
- Records `github-keyless-attestation.json` with the attestation ID, URL, issuer, and verification command.
- Attaches the signed zip and keyless attestation metadata directly to the GitHub Release on published release events.
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

Verify the air-gapped zip before transferring it into a restricted environment:

```bash
cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-v0.1.0.zip
```

Verify the GitHub keyless attestation for the release zip:

```bash
gh attestation verify go/cavra-runtime/dist/cavra-go-runtime-v0.1.0.zip \
  --repo Huzefaaa2/cavra
```

Validate a release-candidate upgrade before promotion:

```bash
cavra release validate-upgrade \
  go/cavra-runtime/dist/go-runtime-v0.1.0 \
  go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1
```

The upgrade validator verifies both packages, rejects rollback versions, detects removed release controls, and flags missing Go runtime binary targets across Linux, macOS, and Windows packages.

Inspect signed installer metadata before deploying to developer workstations, CI runners, or restricted networks:

```bash
jq '.targets[] | {target, binary, install_path, binary_sha256}' \
  go/cavra-runtime/dist/go-runtime-v0.1.0/cavra-runtime.installers.json
```

`cavra release verify-go-package` requires `cavra-runtime.installers.json`, checks every referenced binary digest, confirms checksum guidance, and verifies the metadata through checksums, SLSA provenance, and detached signatures.

Smoke-test installer metadata and execute the native packaged runtime when the current OS and architecture are present:

```bash
cavra release smoke-installers go/cavra-runtime/dist/go-runtime-v0.1.0
```

For cross-compiled packages on a nonmatching host, run static installer validation without execution:

```bash
cavra release smoke-installers go/cavra-runtime/dist/go-runtime-v0.1.0 --skip-execution
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

- As a release manager, I can publish Go runtime binaries with checksums, SBOM, SLSA provenance, signatures, keyless attestations, and evidence.
- As a security engineer, I can verify that binaries map to a specific commit, ref, workflow identity, and dependency set.
- As an enterprise architect, I can verify an air-gapped runtime zip before restricted-network transfer.
- As a platform engineer, I can compare the current approved package with a release candidate before promoting it to developers or CI runners.
- As an endpoint engineering owner, I can approve signed installer metadata before placing CAVRA binaries on managed developer workstations.
- As a release engineer, I can smoke-test installer metadata and the native packaged runtime before publishing a release asset.
- As an auditor, I can run a single CLI verifier and see checksum, evidence, and signature failures before approval.

## Enterprise Challenge Solved

Enterprise buyers require release integrity before allowing local enforcement binaries onto developer laptops, CI runners, or air-gapped environments. The Go release package turns runtime binaries into auditable artifacts with checksums, SBOM metadata, signed installer metadata, installer smoke validation, SLSA provenance, detached signatures, GitHub OIDC-backed keyless attestations, offline bootstrap metadata, CAVRA release evidence, release-candidate upgrade validation, release-asset attachment, and local plus GitHub verifier commands.

## Next Work

1. Add managed endpoint deployment manifests for CI runners and developer workstations.
