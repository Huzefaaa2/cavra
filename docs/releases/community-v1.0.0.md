# CAVRA Community v1.0.0 Release Notes

CAVRA Community v1.0.0 is the stable public Community baseline for Controlled
Agentic Verification and Runtime Authority. The `community-v1.0.0` GitHub
Release is published from merged `main` commit
`bb5dd1005e9c2efb6e7e4df40ad153751476a6d2` at
`2026-06-05T07:30:35Z` with public Community wheel, source distribution,
checksum manifest, and provenance metadata assets.

## Release Links

- GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0>
- Post-publication verification:
  `docs/release-verifications/community-v1.0.0-post-publication-verification.md`
- Post-publication packet:
  `docs/release-verifications/community-v1.0.0-post-publication-verification.json`
- Keyless attestation workflow:
  `docs/community-release-keyless-attestation.md`
- GA publication package:
  `docs/community-v1.0.0-ga-publication-package.md`
- Publication readiness verification:
  `docs/release-verifications/community-v1.0.0-publication-readiness.md`
- Publication package packet:
  `docs/release-verifications/community-v1.0.0-ga-publication-package.json`
- GA readiness:
  `docs/community-v1.0.0-ga-readiness.md`
- RC1 post-publication verification:
  `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md`
- Release index:
  `docs/community-release-index.md`
- Release readiness dashboard:
  `docs/community-release-readiness-dashboard.md`

## What Changed

- Published the final public Community v1.0.0 GitHub Release from validated
  RC1 feedback and the completed Node 24 readiness baseline.
- Bumped the public package metadata and runtime version from `1.0.0rc1` to
  final `1.0.0`.
- Attached the final wheel, source distribution, checksum manifest, and
  provenance metadata to the public GitHub Release.
- Verified the GitHub-hosted wheel and source distribution SHA-256 checksums.
- Verified a clean virtualenv install from the published wheel with
  `cavra version` returning `cavra 1.0.0`.
- Verified the Community Docker image builds from the public source tree using
  `docker/Dockerfile.community`.
- Confirmed the package remains public Community material only and does not
  include Enterprise source code or private release material.

## Upgrade Notes

- From Community v0.1.3: install the final `1.0.0` wheel or source
  distribution, then run `cavra version` and verify `cavra 1.0.0`.
- From Community v1.0.0 RC1: replace the release-candidate package with the
  final `1.0.0` package, rerun policy validation, and verify evidence bundle
  generation.
- Enterprise features remain outside the public Community artifact and require
  private packages or commercial access.

## Artifact Verification

| Artifact | SHA-256 | Size |
| --- | --- | --- |
| `cavra-1.0.0-py3-none-any.whl` | `464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914` | 324060 bytes |
| `cavra-1.0.0.tar.gz` | `851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331` | 1043690 bytes |
| `cavra-1.0.0-SHA256SUMS.txt` | `c9049c68d23e089f2129ab3f1f130f7a8e07aecc4bb1e8b4b5360b22a5c617fd` | 274 bytes |
| `cavra-1.0.0.provenance.json` | `38b6e2127695050e697d33dde22f111eaee5cccbcf598cb82fc60c6a795c99aa` | 893 bytes |

Verification command:

```bash
python3 scripts/verify-community-release-artifacts.py \
  --tag community-v1.0.0 \
  --version 1.0.0 \
  --wheel-sha256 464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914 \
  --sdist-sha256 851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331
```

Observed clean install smoke:

```text
cavra 1.0.0
```

The release is ready for GitHub keyless release asset attestation through
`.github/workflows/attest-community-release.yml`. The workflow downloads the
published assets, validates SHA-256 checksums, generates a Sigstore-backed
attestation with `actions/attest@v4`, and verifies each asset with
`gh attestation verify`. detached signature assets remain optional future
hardening because this path uses GitHub keyless attestation instead of a
maintainer-managed private signing key.

## Verification Summary

- GA publication package: pass.
- Publication readiness verification: pass.
- Evidence validator:
  `scripts/validate-community-v100-ga-post-publication.py`.
- README release link freshness: pass.
- Wiki release link freshness: pass.
- Release index published row: pass.
- Release readiness dashboard published row: pass.
- Package metadata bump: pass.
- Published wheel checksum: pass.
- Published source distribution checksum: pass.
- Published checksum manifest: pass.
- Published provenance metadata: pass.
- Clean install smoke: pass.
- Community Docker build: pass.
- Keyless attestation workflow: ready.
- Public boundary validation: pass.

## Boundary Notice

This published GA release note covers public Community Edition release
documentation and artifacts only. Enterprise source code, paid policy packs,
SaaS backend implementation, license-service internals, private signing keys,
private registry credentials, and customer records are not part of this public
release record.

## Next Recommendation

Use Community v1.0.0 as the stable public baseline and begin the v1.0.1 maintenance planning path for post-GA fixes, release integrity hardening, detached signing or keyless attestation, and adoption feedback.
