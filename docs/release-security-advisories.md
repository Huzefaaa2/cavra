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
- release-candidate upgrade validation with `cavra release validate-upgrade`;
- SBOM, installer metadata, checksum, detached signature, GitHub keyless attestation, and SLSA provenance references.

## Go Runtime Release Gate

Before publishing a Go runtime package:

1. Build release binaries through `.github/workflows/go-release.yml`.
2. Require `CAVRA_GO_RELEASE_SIGNING_KEY` for production releases.
3. Confirm the package contains:
   - `checksums.txt`;
   - `cavra-runtime.installers.json`;
   - `cavra-runtime.sbom.spdx.json`;
   - `cavra-runtime.provenance.intoto.json`;
   - detached `*.sig.json` files;
   - `github-keyless-attestation.json`;
   - `offline-trust-root-bootstrap.json`;
   - `release-evidence.json`;
   - `release-evidence.md`.
4. Verify locally:

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-<version>
```

5. Verify the air-gapped zip:

```bash
cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-<version>.zip
```

6. Verify the GitHub keyless attestation:

```bash
gh attestation verify go/cavra-runtime/dist/cavra-go-runtime-<version>.zip \
  --repo Huzefaaa2/cavra
```

7. Validate the candidate against the previously approved package:

```bash
cavra release validate-upgrade \
  go/cavra-runtime/dist/go-runtime-<previous-version> \
  go/cavra-runtime/dist/go-runtime-<candidate-version>
```

8. Attach `cavra-go-runtime-<version>.zip` and `github-keyless-attestation.json` to the GitHub Release.
9. Link the release asset, keyless attestation, installer metadata, offline bootstrap manifest, upgrade validation result, and provenance statement from the advisory.

## User Stories

- As a security engineer, I can connect an advisory to a signed release asset, keyless GitHub attestation, and provenance statement.
- As a platform owner, I can block runtime rollout until verification succeeds.
- As an enterprise architect, I can verify an air-gapped runtime bundle before restricted-network transfer.
- As a release manager, I can reject rollback versions or missing runtime targets before promoting a release candidate.
- As an endpoint engineering owner, I can approve signed install paths and platform targets before managed rollout.
- As an auditor, I can prove that security releases follow the same evidence path as normal releases.

## Enterprise Challenge Solved

Enterprises need vulnerability response and release integrity in the same operating model. CAVRA advisories tie security fixes to signed, keyless-attested, provenance-backed artifacts, signed installer metadata, and release-candidate upgrade checks so regulated teams can approve upgrades with less manual evidence collection.
