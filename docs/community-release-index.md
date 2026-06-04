# Community Release Index

This index summarizes public CAVRA Community release records, release notes,
verification packets, publication state, and next action. It is the public
starting point for users and maintainers who need to verify which Community
artifacts are published and which release evidence is ready for publication.

## Release Summary

| Release | State | GitHub Release | Release Notes | Verification Packet | Next Action |
| --- | --- | --- | --- | --- | --- |
| Community GA v0.1.0 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0> | `docs/releases/community-v0.1.0.md` | `docs/release-verifications/community-v0.1.0-post-release-verification.md` | Use as the current public Community GA baseline. |
| Community v0.1.1 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1> | `docs/releases/community-v0.1.1.md` | `docs/release-verifications/community-v0.1.1-maintenance-verification.md` | Archive post-publication verifier output and begin the next maintenance-release readiness slice. |

## Current Public Baseline

Community GA v0.1.0 is the current published public Community release. It has a
GitHub Release, attached source distribution and wheel artifacts, recorded
SHA-256 checksums, and a clean install smoke result.

## Current Maintenance Release

Community v0.1.1 is the current maintenance-release record. It records the
package version bump, public artifact names, SHA-256 checksums, install-smoke
result, release documentation, evidence packet, public boundary, and freshness
checks for the official maintenance release.

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

Archive the post-publication Community v0.1.1 verifier output and begin the
next maintenance-release readiness slice.
