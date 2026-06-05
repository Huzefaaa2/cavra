# CAVRA Community v1.0.0 RC1 Release Notes

CAVRA Community v1.0.0 RC1 is the published release-candidate record for the
public Community Edition. It records the GitHub Release, downloadable Python
artifacts, SHA-256 checksums, provenance metadata, clean install smoke,
README links, wiki navigation, release index, and release dashboard after the
`community-v1.0.0-rc.1` artifacts were published.

## Release Links

- GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1>
- Release target:
  `e04ba0025f00b13bf05ab468669bcb3fb494eb89`
- Published at:
  `2026-06-05T05:49:28Z`
- Publication preparation:
  `docs/community-v1.0.0-release-candidate-publication.md`
- Publication readiness verification:
  `docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md`
- Post-publication verification:
  `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md`
- Post-publication packet:
  `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.json`

The post-publication verification packet is the authoritative public evidence
record for the published RC1 artifacts.
- Release-candidate hardening:
  `docs/community-v1.0.0-release-candidate-hardening.md`
- Stabilization plan:
  `docs/community-v1.0.0-stabilization-plan.md`
- Release index:
  `docs/community-release-index.md`
- Release readiness dashboard:
  `docs/community-release-readiness-dashboard.md`

## What Changed

- Published the public Community v1.0.0 RC1 GitHub Release from the completed
  Node 24 readiness baseline.
- Attached the wheel, source distribution, checksum file, and provenance JSON
  artifact evidence for the RC1 artifact publication step.
- Recorded SHA-256 checksums, release workflow links, and clean install smoke
  output for `cavra 1.0.0rc1`.
- Kept detached signatures and keyless attestation links as explicit GA
  hardening gates before final v1.0.0 announcement.
- Kept Public boundary validation mandatory before the RC can be announced.
- Confirmed the RC1 record is public Community documentation only and does not
  include Enterprise source code or private release material.

## Artifact Verification

RC1 artifacts are published on the GitHub Release.

| Artifact | SHA-256 | Size |
| --- | --- | ---: |
| `cavra-1.0.0rc1-py3-none-any.whl` | `6d06bd04965d3b1340ecacf007bc39111c8a8d5d0a73ee32f44aeb06ebb1be01` | 324003 |
| `cavra-1.0.0rc1.tar.gz` | `f4312e51a4d4180387982eafa86f301c584be5af147ba09098d733d187662e0c` | 1030541 |
| `cavra-1.0.0rc1-SHA256SUMS.txt` | `73a4f20e42ea4823a8087bfb9d703bf224cd8e9128ed5590a9eaad047a8ea166` | 283 |
| `cavra-1.0.0rc1.provenance.json` | `fdb69a24e6f76a737e225b2d259c8842a08172cd929fdf3f5e41020ad5d32217` | 1140 |

Reusable verification:

```bash
python3 scripts/verify-community-release-artifacts.py \
  --tag community-v1.0.0-rc.1 \
  --version 1.0.0rc1 \
  --wheel-sha256 6d06bd04965d3b1340ecacf007bc39111c8a8d5d0a73ee32f44aeb06ebb1be01 \
  --sdist-sha256 f4312e51a4d4180387982eafa86f301c584be5af147ba09098d733d187662e0c
```

The RC1 release records checksum and provenance evidence for the Python
artifacts. Detached signature and keyless attestation evidence are not attached
for this RC1 Python artifact path; they remain a GA hardening gate before the
final v1.0.0 announcement.

## Verification Summary

- Release notes: pass.
- Publication readiness verification: pass.
- Evidence validator: `scripts/validate-community-v100-rc-publication.py`.
- Post-publication validator:
  `scripts/validate-community-v100-rc-post-publication.py`.
- README release link freshness: pass.
- Wiki release link freshness: pass.
- Release index published row: pass.
- Release readiness dashboard published row: pass.
- SHA-256 artifact verification: pass.
- Provenance evidence: pass.
- Clean install smoke: `cavra 1.0.0rc1`.
- Public boundary validation: pass.

## Boundary Notice

This RC1 release note covers public Community Edition release artifacts and
documentation only. Enterprise source code, paid policy packs, SaaS backend
implementation, license-service internals, private signing keys, private registry credentials,
and customer records are not part of this public release
candidate record.

## Next Recommendation

Advance Community v1.0.0 RC1 feedback from the completed Node 24 readiness baseline into GA release readiness by validating upgrade notes, installer paths, announcement copy, and final GA evidence gates.
