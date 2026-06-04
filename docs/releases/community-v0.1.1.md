# CAVRA Community v0.1.1 Release Notes

CAVRA Community v0.1.1 is the first public Community maintenance release after
Community GA v0.1.0. It converts the earlier maintenance-release dry-run record
into an official public release path with concrete distribution artifacts,
recorded checksums, install-smoke evidence, README links, wiki navigation, and
release-readiness dashboard coverage.

## Release Links

- GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1>
- Maintenance verification:
  `docs/release-verifications/community-v0.1.1-maintenance-verification.md`
- Post-release verification:
  `docs/release-verifications/community-v0.1.1-post-release-verification.md`
- Maintenance-release checklist:
  `docs/community-maintenance-release-checklist.md`
- Release-note freshness control:
  `docs/community-release-note-freshness.md`
- Release index:
  `docs/community-release-index.md`
- Release readiness dashboard:
  `docs/community-release-readiness-dashboard.md`

## What Changed

- Bumped the Community Python package metadata from `0.1.0` to `0.1.1`.
- Added a shared package version constant and updated the CLI and MCP server to
  report `0.1.1` instead of the previous hardcoded `0.1.0`.
- Rebuilt public Community wheel and source distribution artifacts:
  `cavra-0.1.1-py3-none-any.whl` and `cavra-0.1.1.tar.gz`.
- Recorded SHA-256 checksums for both artifacts in the maintenance
  verification packet.
- Verified a clean virtual environment wheel install and `cavra version`
  output of `cavra 0.1.1`.
- Updated the Community release index, readiness dashboard, README links, and
  wiki-ready release navigation.

## Artifact Checksums

| Artifact | SHA-256 |
| --- | --- |
| `cavra-0.1.1.tar.gz` | `b123c6d2aadd72b055ba916caa68953af94122d34f1215756804d74e91174950` |
| `cavra-0.1.1-py3-none-any.whl` | `32ab7a220eb5f25ea5ab42ccbc62a43b7260de12b9a0d3f3d7bdafa1501a5d6a` |

## Verification Summary

- Local package build: pass.
- Clean wheel install smoke: pass.
- CLI version output: `cavra 0.1.1`.
- Public boundary validation: pass.
- Release-note freshness validation: pass.
- Maintenance-release evidence validation: pass.

## Boundary Notice

This release covers the public Community Edition release path only. Enterprise
source code, paid policy packs, SaaS backend implementation, license-service
internals, private keys, private registry credentials, and customer records are
not part of this public release.

## Next Recommendation

Prepare Community v0.1.2 release notes and dry-run verification packet using
the package metadata and release workflow guard evidence.
