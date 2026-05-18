# Release Security Advisories

Security-relevant CAVRA releases must be traceable from source commit to release package, advisory, and verification command.

## Advisory Content

Every security advisory or security-impacting release note should include:

- advisory ID or release tag;
- severity and affected components;
- affected versions and fixed versions;
- customer impact and exploitation prerequisites;
- mitigation before upgrade;
- fixed commit, pull request, and release asset links;
- verification steps, including `cavra release verify-go-package`;
- SBOM, checksum, detached signature, GitHub keyless attestation, and SLSA provenance references.

## Go Runtime Release Gate

Before publishing a Go runtime package:

1. Build release binaries through `.github/workflows/go-release.yml`.
2. Require `CAVRA_GO_RELEASE_SIGNING_KEY` for production releases.
3. Confirm the package contains `checksums.txt`, `cavra-runtime.sbom.spdx.json`, `cavra-runtime.provenance.intoto.json`, detached signatures, `github-keyless-attestation.json`, `offline-trust-root-bootstrap.json`, and release evidence.
4. Verify locally with `cavra release verify-go-package go/cavra-runtime/dist/go-runtime-<version>`.
5. Verify the air-gapped zip with `cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-<version>.zip`.
6. Verify the GitHub keyless attestation with `gh attestation verify go/cavra-runtime/dist/cavra-go-runtime-<version>.zip --repo Huzefaaa2/cavra`.
7. Attach `cavra-go-runtime-<version>.zip` and `github-keyless-attestation.json` to the GitHub Release.
8. Link the release asset, keyless attestation, offline bootstrap manifest, and provenance statement from the advisory.

## User Stories

- As a security engineer, I can connect an advisory to a signed release asset, keyless GitHub attestation, and provenance statement.
- As a platform owner, I can block runtime rollout until verification succeeds.
- As an enterprise architect, I can verify an air-gapped runtime bundle before restricted-network transfer.
- As an auditor, I can prove that security releases follow the same evidence path as normal releases.

## Enterprise Challenge Solved

Enterprises need vulnerability response and release integrity in the same operating model. CAVRA advisories tie security fixes to signed, keyless-attested, provenance-backed artifacts so regulated teams can approve upgrades with less manual evidence collection.
