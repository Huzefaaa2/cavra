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
| Community v1.0.0 RC1 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1> | `docs/releases/community-v1.0.0-rc.1.md` | `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md` | Publish Community v1.0.0 GA artifacts from the approved publication package and completed Node 24 readiness baseline by bumping package metadata to 1.0.0, building final artifacts, attaching GitHub Release assets, recording checksums and provenance, and completing post-publication verification. |
| Community v1.0.0 | Dry run | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0> | `docs/releases/community-v1.0.0.md` | `docs/release-verifications/community-v1.0.0-publication-readiness.md` | Publish Community v1.0.0 GA artifacts from the approved publication package and completed Node 24 readiness baseline by bumping package metadata to 1.0.0, building final artifacts, attaching GitHub Release assets, recording checksums and provenance, and completing post-publication verification. |

## Current Public Baseline

Community v1.0.0 RC1 is the current published public Community release
candidate. It has a GitHub Release, attached source distribution and wheel
artifacts, recorded SHA-256 checksums, provenance metadata, and a clean install
smoke result. Community v0.1.3 remains the current published maintenance
baseline, and Community GA v0.1.0 remains the GA baseline record.

## Current Maintenance Release

Community v0.1.3 is the current published maintenance-release record. It
records the package version bump, Node 24-ready workflow path, release
documentation, maintenance verification packet, public boundary, published
artifact checksums, clean install smoke, and post-release verification.
Community v0.1.2 remains the previous published maintenance baseline.

## Current Release Candidate

Community v1.0.0 RC1 is the current published release-candidate record. It has
release notes, publication readiness verification, post-publication
verification, README links, wiki navigation, release index coverage, release
dashboard coverage, artifact checksums, provenance metadata, GitHub Release
links, workflow evidence, and clean install smoke evidence. Detached signature
and keyless attestation evidence remain GA hardening gates before final v1.0.0
announcement.

Community v1.0.0 is prepared as a dry-run GA publication package. It has draft
final release notes, publication readiness verification, artifact build plan,
verifier inputs, announcement approval evidence, README links, wiki navigation,
release index coverage, and release dashboard coverage. Real final artifacts,
checksums, provenance, signature or attestation evidence, clean install smoke,
and post-publication verification remain pending until artifacts are published.

## Verification Controls

Public Community releases are checked by:

- `scripts/validate-release-packets.py`
- `scripts/validate-maintenance-release-evidence.py`
- `scripts/validate-community-release-note-freshness.py`
- `scripts/validate-community-release-index.py`
- `scripts/validate-boundaries.sh`
- `.github/workflows/verify-community-release.yml`

## Boundary Notice

This index covers public Community Edition release evidence only. Enterprise
source code, paid policy packs, SaaS backend implementation, license-service
internals, private keys, private registry credentials, and customer records are
not part of this public release index.

## Next Recommendation

Publish Community v1.0.0 GA artifacts from the approved publication package and completed Node 24 readiness baseline by bumping package metadata to 1.0.0, building final artifacts, attaching GitHub Release assets, recording checksums and provenance, and completing post-publication verification.
