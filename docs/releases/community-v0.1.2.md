# CAVRA Community v0.1.2 Release Notes

CAVRA Community v0.1.2 is a public Community Edition maintenance release. It
converts the earlier v0.1.2 dry-run record into an official GitHub Release with
published wheel and source distribution artifacts, SHA-256 checksums,
clean-install smoke evidence, README links, wiki navigation, release index
coverage, and readiness dashboard coverage.

## Release Links

- GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.2>
- Maintenance verification:
  `docs/release-verifications/community-v0.1.2-maintenance-verification.md`
- Post-release verification:
  `docs/release-verifications/community-v0.1.2-post-release-verification.md`
- Community v0.1.2 readiness:
  `docs/community-v0.1.2-readiness.md`
- Maintenance-release checklist:
  `docs/community-maintenance-release-checklist.md`
- Release-note freshness control:
  `docs/community-release-note-freshness.md`
- Release index:
  `docs/community-release-index.md`
- Release readiness dashboard:
  `docs/community-release-readiness-dashboard.md`

## What Changed

- Bumped the Community Python package metadata and runtime version from
  `0.1.1` to `0.1.2`.
- Kept `pyproject.toml` as the package metadata source of truth and
  `setup.py` as the legacy setuptools shim.
- Preserved package metadata validation for BUSL-1.1, project URLs,
  license-file metadata, packaged schemas, and setuptools warning rejection.
- Published public Community wheel and source distribution artifacts:
  `cavra-0.1.2-py3-none-any.whl` and `cavra-0.1.2.tar.gz`.
- Verified published GitHub Release asset SHA-256 checksums.
- Verified a clean virtual environment wheel install and `cavra version`
  output of `cavra 0.1.2`.

## Artifact Checksums

| Artifact | SHA-256 |
| --- | --- |
| `cavra-0.1.2.tar.gz` | `f7a477cfef65d77bd4c36520a83d256c1086e7b81ffcd9411ee9c68d017ab1d0` |
| `cavra-0.1.2-py3-none-any.whl` | `bbdb2f593ce3c14742446c1682c23bef7933925a02382a874e59b8ef7e389163` |

## Verification Summary

- Local package build: pass.
- `twine check`: pass.
- Published asset download: pass.
- Published asset checksum match: pass.
- Clean wheel install smoke: pass.
- CLI version output: `cavra 0.1.2`.
- Public boundary validation: pass.
- Release-note freshness validation: pass.
- Maintenance-release evidence validation: pass.

## Boundary Notice

This release covers the public Community Edition release path only. Enterprise
source code, paid policy packs, SaaS backend implementation, license-service
internals, private keys, private registry credentials, and customer records are
not part of this public release.

## Next Recommendation

Prepare Community v0.1.3 maintenance planning and GitHub Actions Node 24
readiness.
