# Go Reproducible Air-Gapped Builds

CAVRA Community Edition now records reproducibility metadata for the Go enforcement-plane runtime. The goal is to let security teams verify a release package online, transfer it through an approved air-gapped process, and rebuild or re-check the single runtime binary without exposing enterprise source code or private release keys.

## What Is Produced

The Go release workflow and `scripts/package_go_release.py` produce `cavra-runtime.reproducibility.json` inside every Go runtime package. The manifest records:

- package version, commit, ref, repository, and workflow reference
- Go module directory
- declared target matrix
- `CGO_ENABLED=0`
- `GOFLAGS="-trimpath -mod=readonly -buildvcs=false"`
- `ldflags="-s -w -buildid="`
- per-target binary paths, sizes, SHA-256 digests, and rebuild commands
- operator controls for restricted-network rebuild evidence

The manifest is included in `checksums.txt`, SLSA provenance subjects, release evidence, detached signatures, and the offline trust bootstrap required-file list.

## Verification Flow

1. Download `cavra-go-runtime-<version>.zip` from the GitHub Release or release workflow artifact.
2. Verify the zip before transfer:

```bash
cavra release verify-airgap-bundle cavra-go-runtime-<version>.zip
```

3. Transfer only the verified zip plus approved public trust material through the enterprise removable-media or offline package process.
4. Inside the restricted environment, verify the extracted package again:

```bash
cavra release verify-go-package go-runtime-<version>
```

5. Rebuild any target binary when required by local policy using the `rebuild_command` from `cavra-runtime.reproducibility.json`.
6. Compare rebuilt binary hashes with `binary_sha256` before installing on CI runners, developer workstations, or restricted servers.

## User Stories

- As a public-sector platform team, I can verify and rebuild a single CAVRA runtime binary before placing it in an air-gapped runner image.
- As a security auditor, I can inspect deterministic build flags and binary digests without needing access to private enterprise source code.
- As a release manager, I can attach reproducibility evidence to the same release change record as checksums, signatures, SBOM, and provenance.

## Enterprise Challenge Solved

Restricted environments often reject opaque binaries unless the package includes verifiable provenance, checksums, rebuild instructions, and repeatable build controls. CAVRA now packages those controls with the community Go runtime so enterprises can evaluate air-gapped deployment using public-safe artifacts.

## Public Boundary

This feature documents and verifies Community Edition Go runtime packaging only. Enterprise modules, commercial policy packs, SaaS license validation, customer-specific deployment scripts, and private signing keys remain outside the public repository.

## Next Work

The next recommended implementation phase is contract-level Go parity for additional high-risk release-governance metadata and production release-signing operations documentation.
