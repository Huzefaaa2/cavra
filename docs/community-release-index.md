# Community Release Index

This index summarizes public CAVRA Community release records, release notes,
verification packets, publication state, and next action. It is the public
starting point for users and maintainers who need to verify which Community
artifacts are published and which release evidence is still a dry run.

## Release Summary

| Release | State | GitHub Release | Release Notes | Verification Packet | Next Action |
| --- | --- | --- | --- | --- | --- |
| Community GA v0.1.0 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0> | `docs/releases/community-v0.1.0.md` | `docs/release-verifications/community-v0.1.0-post-release-verification.md` | Use as the current public Community GA baseline. |
| Community v0.1.1 | Dry run | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1> | `docs/releases/community-v0.1.1.md` | `docs/release-verifications/community-v0.1.1-maintenance-verification.md` | Publish only after real v0.1.1 artifacts exist and verification warnings are replaced with passing evidence. |

## Current Public Baseline

Community GA v0.1.0 is the current published public Community release. It has a
GitHub Release, attached source distribution and wheel artifacts, recorded
SHA-256 checksums, and a clean install smoke result.

## Maintenance Dry Run

Community v0.1.1 is a dry-run maintenance-release record. It validates the
post-GA release documentation, evidence packet, public boundary, and freshness
checks before a real v0.1.1 tag is published. It does not claim that v0.1.1
artifacts are available.

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

Prepare the next official Community maintenance release by converting the
v0.1.1 dry-run packet into real release artifacts, verification evidence,
release notes, README links, and wiki navigation.
