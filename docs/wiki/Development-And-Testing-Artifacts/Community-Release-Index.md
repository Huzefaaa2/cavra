# Community Release Index

This index summarizes public CAVRA Community release records, release notes,
verification packets, publication state, and next action. It is the public
starting point for users and maintainers who need to verify which Community
artifacts are published and which release evidence is ready for publication.

## Release Summary

| Release | State | GitHub Release | Release Notes | Verification Packet | Next Action |
| --- | --- | --- | --- | --- | --- |
| Community GA v0.1.0 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0> | `docs/releases/community-v0.1.0.md` | `docs/release-verifications/community-v0.1.0-post-release-verification.md` | Use as the current public Community GA baseline. |
| Community v0.1.1 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1> | `docs/releases/community-v0.1.1.md` | `docs/release-verifications/community-v0.1.1-post-release-verification.md` | Use as the previous public Community maintenance baseline. |
| Community v0.1.2 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.2> | `docs/releases/community-v0.1.2.md` | `docs/release-verifications/community-v0.1.2-post-release-verification.md` | Use as the previous published Community maintenance baseline. |
| Community v0.1.3 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.3> | `docs/releases/community-v0.1.3.md` | `docs/release-verifications/community-v0.1.3-post-release-verification.md` | Use as the current published Community maintenance baseline while v1.0.0 stabilization planning begins. |
| Community v1.0.0 RC1 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1> | `docs/releases/community-v1.0.0-rc.1.md` | `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md` | Use as the previous release-candidate baseline for v1.0.0 provenance comparison. |
| Community v1.0.0 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0> | `docs/releases/community-v1.0.0.md` | `docs/release-verifications/community-v1.0.0-post-publication-verification.md` | Use as the stable public Community baseline and begin the v1.0.1 maintenance planning path. |

## Current Public Baseline

Community v1.0.0 is the current stable public Community release. It has a
GitHub Release, attached source distribution and wheel artifacts, a checksum
manifest, provenance metadata, recorded SHA-256 checksums, a clean install
smoke result, and Community Docker build evidence. Community v1.0.0 RC1 remains
the previous release-candidate baseline for provenance comparison.

## Current Maintenance Release

Community v0.1.3 is the current published maintenance-release record. It
records the package version bump, Node 24-ready workflow path, release
documentation, maintenance verification packet, public boundary, published
artifact checksums, clean install smoke, and post-release verification.
Community v0.1.2 remains the previous published maintenance baseline.

## Current Release Candidate

Community v1.0.0 RC1 is the previous published release-candidate record. It has
release notes, publication readiness verification, post-publication
verification, README links, wiki navigation, release index coverage, release
dashboard coverage, artifact checksums, provenance metadata, GitHub Release
links, workflow evidence, and clean install smoke evidence.

Community v1.0.0 is the published GA record. It has final release notes,
post-publication verification, artifact checksums, checksum manifest,
provenance metadata, README links, wiki navigation, release index coverage,
release dashboard coverage, clean install smoke, and Community Docker build
evidence. Detached signature and keyless attestation assets remain follow-up
release integrity hardening gates for the v1.0.1 maintenance path.

## Verification Controls

Public Community releases are checked by:

- `scripts/validate-release-packets.py`
- `scripts/validate-maintenance-release-evidence.py`
- `scripts/validate-community-release-note-freshness.py`
- `scripts/validate-community-release-index.py`
- `scripts/validate-boundaries.sh`
- `.github/workflows/verify-community-release.yml`

Node 24 readiness remains the completed GitHub Actions baseline for current
Community release workflows.

## Boundary Notice

This index covers public Community Edition release evidence only. Enterprise
source code, paid policy packs, SaaS backend implementation, license-service
internals, private keys, private registry credentials, and customer records are
not part of this public release index.

## Next Recommendation

Use Community v1.0.0 as the stable public baseline and begin the v1.0.1 maintenance planning path for post-GA fixes, release integrity hardening, detached signing or keyless attestation, and adoption feedback.
