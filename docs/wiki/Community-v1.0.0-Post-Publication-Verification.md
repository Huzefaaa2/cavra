# Community v1.0.0 Post-Publication Verification

This packet records the published CAVRA Community v1.0.0 GitHub Release,
artifact integrity checks, clean install smoke, Community Docker build smoke,
README links, wiki navigation, release index state, readiness dashboard state,
and public boundary validation.

## Release Metadata

| Field | Value |
| --- | --- |
| Release | CAVRA Community v1.0.0 |
| Tag | `community-v1.0.0` |
| Version | `1.0.0` |
| GitHub Release | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0> |
| Published at | `2026-06-05T07:30:35Z` |
| Release target | `bb5dd1005e9c2efb6e7e4df40ad153751476a6d2` |
| Release notes | `docs/releases/community-v1.0.0.md` |
| Verification packet | `docs/release-verifications/community-v1.0.0-post-publication-verification.json` |

## Artifact Verification

| Artifact | SHA-256 | Size | Status |
| --- | --- | --- | --- |
| `cavra-1.0.0-py3-none-any.whl` | `464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914` | 324060 bytes | Verified |
| `cavra-1.0.0.tar.gz` | `851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331` | 1043690 bytes | Verified |
| `cavra-1.0.0-SHA256SUMS.txt` | `c9049c68d23e089f2129ab3f1f130f7a8e07aecc4bb1e8b4b5360b22a5c617fd` | 274 bytes | Recorded |
| `cavra-1.0.0.provenance.json` | `38b6e2127695050e697d33dde22f111eaee5cccbcf598cb82fc60c6a795c99aa` | 893 bytes | Recorded |

Published artifact verification command:

```bash
python3 scripts/verify-community-release-artifacts.py \
  --tag community-v1.0.0 \
  --version 1.0.0 \
  --wheel-sha256 464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914 \
  --sdist-sha256 851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331
```

Observed output:

```text
cavra 1.0.0
```

## Verification Gates

| Gate | Status | Evidence |
| --- | --- | --- |
| GitHub Release exists | Pass | `community-v1.0.0` is published and not marked draft or prerelease. |
| Wheel checksum | Pass | Published wheel SHA-256 matched expected hash. |
| Source distribution checksum | Pass | Published source distribution SHA-256 matched expected hash. |
| Checksum manifest | Pass | `cavra-1.0.0-SHA256SUMS.txt` is attached. |
| Provenance metadata | Pass | `cavra-1.0.0.provenance.json` is attached. |
| Clean install smoke | Pass | `cavra version` returned `cavra 1.0.0`. |
| Community Docker build | Pass | `docker build -f docker/Dockerfile.community .` completed successfully. |
| Keyless attestation workflow | Ready | `.github/workflows/attest-community-release.yml` attests published assets with `actions/attest@v4` and verifies them with `gh attestation verify`. |
| README link | Pass | README links release notes and this post-publication packet. |
| Wiki navigation | Pass | `docs/wiki/Home.md` links release notes and this verification packet. |
| Release index | Pass | `docs/community-release-index.md` marks Community v1.0.0 as Published. |
| Release readiness dashboard | Pass | `docs/community-release-readiness-dashboard.md` marks Community v1.0.0 as Ready. |
| Detached signature | Follow-up | No detached signature asset is attached to this release. |
| Keyless attestation | Ready | `docs/community-release-keyless-attestation.md` defines the release asset attestation runbook and workflow dispatch defaults. |
| Public boundary | Pass | Enterprise source code, paid policy packs, private signing keys, private registry credentials, and customer records are excluded. |

## Boundary Notice

This post-publication verification covers public Community Edition release
artifacts only. Enterprise source code, paid policy packs, SaaS backend
implementation, license-service internals, private signing keys, private
registry credentials, and customer records are not part of this public release.

## Validation

```bash
python3 scripts/validate-community-v100-ga-post-publication.py
python3 scripts/validate-community-release-keyless-attestation.py
```

## Decision

Decision: approve Community v1.0.0 as the stable public Community baseline.

## Next Recommendation

Use Community v1.0.0 as the stable public baseline and begin the v1.0.1 maintenance planning path for post-GA fixes, release integrity hardening, detached signing or keyless attestation, and adoption feedback.
