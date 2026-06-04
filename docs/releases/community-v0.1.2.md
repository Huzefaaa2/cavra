# CAVRA Community v0.1.2 Release Notes

CAVRA Community v0.1.2 is a dry-run maintenance release record. It prepares
the public release notes and verification structure for the next Community
maintenance release, but it is not yet an official published GitHub Release.

## Release Links

- Planned GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.2>
- Dry-run maintenance verification:
  `docs/release-verifications/community-v0.1.2-maintenance-verification.md`
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

## What Is Prepared

- Python package metadata now uses `pyproject.toml` as the source of truth.
- `setup.py` remains as a legacy setuptools shim only.
- `scripts/validate-python-package-metadata.py` builds into a temporary
  directory, rejects setuptools metadata warning markers, runs `twine check`,
  and verifies BUSL-1.1, project URL, license-file, and packaged schema
  metadata in the wheel.
- Community CI and Community release builds run the package metadata validator.
- The PyPI publishing workflow runs `twine check` after building distributions.
- PyPI and Go runtime release workflows remain explicitly guarded so they only
  run automatically for their own release tag families or manual dispatch.

## Dry-Run Status

This page is a release-notes dry run only. No `community-v0.1.2` GitHub Release
has been published yet, and no v0.1.2 wheel or source distribution checksums
are claimed in this public record.

## Verification Summary

- Package metadata validation: pass.
- Release workflow guard evidence: pass.
- Public boundary validation: pass.
- Artifact checksums: pending real v0.1.2 artifacts.
- Clean install smoke: pending real v0.1.2 wheel.

## Boundary Notice

This dry-run release record covers the public Community Edition release path
only. Enterprise source code, paid policy packs, SaaS backend implementation,
license-service internals, private keys, private registry credentials, and
customer records are not part of this public release record.

## Next Recommendation

Convert Community v0.1.2 dry-run into an official maintenance release after
maintainer approval and artifact publication.
