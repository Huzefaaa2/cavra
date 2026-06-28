# Community Release Keyless Attestation

CAVRA Community releases use GitHub artifact attestations for public release
asset provenance hardening. The `Attest Community Release` workflow downloads
published release assets, verifies their SHA-256 checksums, generates a
Sigstore-backed keyless attestation using GitHub Actions OIDC, verifies the
attestation with GitHub CLI, and uploads verifier evidence for the release.

## Workflow

| Field | Value |
| --- | --- |
| Workflow | `.github/workflows/attest-community-release.yml` |
| Default tag | `community-v1.0.0` |
| Default version | `1.0.0` |
| Attestation action | `actions/attest@v4` |
| Required permissions | `id-token: write`, `attestations: write`, `artifact-metadata: write`, `contents: read` |
| Verification command | `gh attestation verify` |
| Signer workflow | `Huzefaaa2/cavra/.github/workflows/attest-community-release.yml` |

GitHub's official artifact attestation action creates signed in-toto
attestations with short-lived Sigstore certificates and requires OIDC and
attestation permissions. GitHub CLI verifies the artifact, repository identity,
signer workflow, and SLSA provenance predicate.

## Covered Assets

The default v1.0.0 attestation covers:

| Artifact | SHA-256 |
| --- | --- |
| `cavra-1.0.0-py3-none-any.whl` | `464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914` |
| `cavra-1.0.0.tar.gz` | `851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331` |
| `cavra-1.0.0-SHA256SUMS.txt` | `c9049c68d23e089f2129ab3f1f130f7a8e07aecc4bb1e8b4b5360b22a5c617fd` |
| `cavra-1.0.0.provenance.json` | `38b6e2127695050e697d33dde22f111eaee5cccbcf598cb82fc60c6a795c99aa` |

## v1.0.0 Attestation Evidence

| Field | Value |
| --- | --- |
| Workflow run | <https://github.com/Huzefaaa2/cavra/actions/runs/27003626701> |
| Attestation ID | `29988580` |
| Attestation URL | <https://github.com/Huzefaaa2/cavra/attestations/29988580> |
| Workflow commit | `a06d996927117e59ad012b7b575b386ef9b9d663` |
| Signer identity | `https://github.com/Huzefaaa2/cavra/.github/workflows/attest-community-release.yml@refs/heads/main` |
| Predicate type | `https://slsa.dev/provenance/v1` |
| Rekor timestamp | `2026-06-05T08:13:01Z` |
| Evidence artifact | `community-release-keyless-attestation-1.0.0` |
| Status | Pass |

## Maintainer Runbook

1. Publish the Community GitHub Release assets.
2. Run `Verify Community Release` with the final SHA-256 values.
3. Run `Attest Community Release` with the matching tag, version, and SHA-256
   values.
4. Confirm the workflow verifies every generated attestation with:

```bash
gh attestation verify <asset> \
  --repo Huzefaaa2/cavra \
  --signer-workflow Huzefaaa2/cavra/.github/workflows/attest-community-release.yml \
  --deny-self-hosted-runners
```

5. Record the workflow run, verifier evidence artifact, README link, release
   note update, and wiki navigation entry.

The workflow uploads `community-release-keyless-attestation-evidence.json`
alongside per-asset `*.attestation-verification.json` files.

## Boundary Notice

The attestation workflow covers public Community release assets only. It does
not use private signing keys, Enterprise source code, paid policy packs,
private registry credentials, license-service secrets, or customer records.

## Validation

```bash
python3 scripts/validate-community-release-keyless-attestation.py
```
