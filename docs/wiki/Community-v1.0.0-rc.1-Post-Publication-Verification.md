# Community v1.0.0 RC1 Post-Publication Verification

This wiki page mirrors the public post-publication verification for the
published CAVRA Community v1.0.0 RC1 GitHub Release.

## Release

- Release: CAVRA Community v1.0.0 RC1
- Tag: `community-v1.0.0-rc.1`
- Version: `1.0.0rc1`
- Release target: `e04ba0025f00b13bf05ab468669bcb3fb494eb89`
- Release URL:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1>
- Published at: `2026-06-05T05:49:28Z`
- Release notes: `docs/releases/community-v1.0.0-rc.1.md`
- Verification packet:
  `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md`

## Artifact Evidence

| Artifact | SHA-256 | Size |
| --- | --- | ---: |
| `cavra-1.0.0rc1-py3-none-any.whl` | `6d06bd04965d3b1340ecacf007bc39111c8a8d5d0a73ee32f44aeb06ebb1be01` | 324003 |
| `cavra-1.0.0rc1.tar.gz` | `f4312e51a4d4180387982eafa86f301c584be5af147ba09098d733d187662e0c` | 1030541 |
| `cavra-1.0.0rc1-SHA256SUMS.txt` | `73a4f20e42ea4823a8087bfb9d703bf224cd8e9128ed5590a9eaad047a8ea166` | 283 |
| `cavra-1.0.0rc1.provenance.json` | `fdb69a24e6f76a737e225b2d259c8842a08172cd929fdf3f5e41020ad5d32217` | 1140 |

The RC1 release records checksum and provenance evidence for the Python
artifacts. The detached signature and keyless attestation evidence are not attached
for this RC1 Python artifact path; they remain a GA hardening gate before the
final v1.0.0 announcement.

## Verification Results

| Check | Result | Evidence |
| --- | --- | --- |
| Release page reachable | Pass | GitHub Release metadata returned tag `community-v1.0.0-rc.1`. |
| Wheel downloadable | Pass | `cavra-1.0.0rc1-py3-none-any.whl` downloaded from the release page. |
| Source distribution downloadable | Pass | `cavra-1.0.0rc1.tar.gz` downloaded from the release page. |
| Clean install smoke | Pass | `cavra 1.0.0rc1` |
| Release Community workflow | Pass | <https://github.com/Huzefaaa2/cavra/actions/runs/26997968188> |
| Test workflow | Pass | <https://github.com/Huzefaaa2/cavra/actions/runs/26997968186> |
| Release Security Readiness workflow | Pass | <https://github.com/Huzefaaa2/cavra/actions/runs/26997989076> |
| Node 24 readiness baseline | Pass | Workflows use Node 24-ready action versions. |
| Public boundary | Pass | Release artifacts and evidence contain public Community material only. |

## Verification Command

```bash
python3 scripts/verify-community-release-artifacts.py \
  --tag community-v1.0.0-rc.1 \
  --version 1.0.0rc1 \
  --wheel-sha256 6d06bd04965d3b1340ecacf007bc39111c8a8d5d0a73ee32f44aeb06ebb1be01 \
  --sdist-sha256 f4312e51a4d4180387982eafa86f301c584be5af147ba09098d733d187662e0c
```

## Boundary Notice

This verification covers public Community Edition release artifacts only. It
does not validate or include Enterprise source code, Enterprise packages, paid policy packs,
license-service internals, SaaS backend implementation, private signing keys,
private registry credentials, customer records, or private deployment evidence.

## Decision

Decision: post-publication verification passed.

## Next Recommendation

Advance Community v1.0.0 RC1 feedback from the completed Node 24 readiness baseline into GA release readiness by validating upgrade notes, installer paths, announcement copy, and final GA evidence gates.
