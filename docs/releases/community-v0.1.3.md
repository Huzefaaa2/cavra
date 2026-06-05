# CAVRA Community v0.1.3 Release Notes

CAVRA Community v0.1.3 is a public Community Edition maintenance release. It
publishes the package version bump, release notes, maintenance evidence, README
links, wiki navigation, release index, readiness dashboard, and post-release
artifact verification for the Node 24-ready Community workflow path.

## Release Links

- GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.3>
- Maintenance verification:
  `docs/release-verifications/community-v0.1.3-maintenance-verification.md`
- Post-release verification:
  `docs/release-verifications/community-v0.1.3-post-release-verification.md`
- Community v0.1.3 maintenance planning:
  `docs/community-v0.1.3-maintenance-planning.md`
- Maintenance-release checklist:
  `docs/community-maintenance-release-checklist.md`
- Release-note freshness control:
  `docs/community-release-note-freshness.md`
- Release index:
  `docs/community-release-index.md`
- Release readiness dashboard:
  `docs/community-release-readiness-dashboard.md`

## What Changed

- Bumped the public Community Python package metadata and runtime version from
  `0.1.2` to `0.1.3`.
- Prepared the v0.1.3 Community maintenance release after the Node 24-ready
  workflow upgrade landed on `main`.
- Kept `community-ci`, `security-scan`, `release-community`, and
  `verify-community-release` on `actions/checkout@v6`,
  `actions/setup-python@v6`, and `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`.
- Preserved package metadata validation for BUSL-1.1, project URLs,
  license-file metadata, packaged schemas, and setuptools warning rejection.
- Published the `community-v0.1.3` GitHub Release with public Community wheel
  and source distribution artifacts.
- Verified published asset downloads, SHA-256 checksums, and clean wheel
  install smoke using `scripts/verify-community-release-artifacts.py`.
- Prepared public release notes, README navigation, wiki navigation, release
  index coverage, readiness dashboard coverage, and post-release evidence.

## Artifact Checksums

| Artifact | SHA-256 |
| --- | --- |
| `cavra-0.1.3.tar.gz` | `83ddaeb4a36502bfa8a5441a15b7b089ac6d5c1dcc58692e942e3ad601d3c29f` |
| `cavra-0.1.3-py3-none-any.whl` | `843cf0c13914e4e9d95ebacd8f0a74aaf4c66969e213e8337d1c0d1c8843cb2e` |

## Verification Summary

- Local package metadata validation: pass.
- Local package build: pass.
- `twine check`: pass.
- GitHub Release publication: pass.
- Published asset download: pass.
- Published asset checksum match: pass.
- Clean wheel install smoke: pass.
- CLI version output: `cavra 0.1.3`.
- Public boundary validation: pass.
- Release-note freshness validation: pass.
- Maintenance-release evidence validation: pass.
- Post-release artifact verification: pass.

## Boundary Notice

This release covers the public Community Edition release path only. Enterprise
source code, paid policy packs, SaaS backend implementation, license-service
internals, private keys, private registry credentials, and customer records are
not part of this public release.

## Next Recommendation

Start Community v1.0.0 stabilization planning from the completed Node 24 readiness baseline with release signing,
reproducible provenance, GA announcement readiness, and final operator
evidence.
