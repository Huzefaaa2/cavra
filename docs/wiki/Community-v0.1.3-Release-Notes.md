# CAVRA Community v0.1.3 Release Notes

CAVRA Community v0.1.3 is a public Community Edition maintenance release
candidate. It prepares the package version, release notes, maintenance
evidence, README links, wiki navigation, release index, and readiness dashboard
for publication after the Node 24-ready Community workflow path is verified on
`main`.

## Release Links

- GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.3>
- Maintenance verification:
  `docs/release-verifications/community-v0.1.3-maintenance-verification.md`
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
- Prepared public release notes, README navigation, wiki navigation, release
  index coverage, and readiness dashboard coverage.

## Artifact Checksums

Final artifact checksums are pending until `community-v0.1.3` is built from
merged `main` and published as a GitHub Release.

| Artifact | SHA-256 |
| --- | --- |
| `cavra-0.1.3.tar.gz` | Pending publication |
| `cavra-0.1.3-py3-none-any.whl` | Pending publication |

## Verification Summary

- Local package metadata validation: pending release-prep PR validation.
- Local package build: pending release-prep PR validation.
- `twine check`: pending release-prep PR validation.
- GitHub Release publication: pending merge to `main`.
- Published asset download: pending publication.
- Published asset checksum match: pending publication.
- Clean wheel install smoke: pending publication.
- CLI version output: expected `cavra 0.1.3`.
- Public boundary validation: pending release-prep PR validation.
- Release-note freshness validation: pending release-prep PR validation.
- Maintenance-release evidence validation: pending release-prep PR validation.

## Boundary Notice

This release covers the public Community Edition release path only. Enterprise
source code, paid policy packs, SaaS backend implementation, license-service
internals, private keys, private registry credentials, and customer records are
not part of this public release.

## Next Recommendation

Publish Community v0.1.3 GitHub Release from merged main after Node 24 readiness and replace pending artifact evidence with post-release verification.
