# CAVRA Community v0.1.3 Maintenance Verification

This packet prepares Community v0.1.3 for publication after the release-prep
branch lands on `main`. It is public-safe release-prep dry-run evidence: final artifact
checksums and clean-install smoke evidence remain pending until the GitHub
Release is built from merged `main`.

## Release Metadata

| Field | Value |
| --- | --- |
| Release | CAVRA Community v0.1.3 |
| State | `ready_with_accepted_risk` |
| Prepared at | `2026-06-05T03:16:34Z` |
| Repository | `Huzefaaa2/cavra` |
| Tag | `community-v0.1.3` |
| Version | `0.1.3` |
| Release URL | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.3> |
| Release notes | `docs/releases/community-v0.1.3.md` |
| Verification workflow | <https://github.com/Huzefaaa2/cavra/actions/workflows/verify-community-release.yml> |

## Gate Summary

| Gate | Status | Evidence |
| --- | --- | --- |
| Release notes | Pass | `docs/releases/community-v0.1.3.md` |
| Changelog | Pass | `CHANGELOG.md` |
| README link | Pass | `README.md` |
| Wiki link | Pass | `docs/wiki/Home.md` |
| Verification workflow | Pass | `.github/workflows/verify-community-release.yml` |
| Artifact checksums | Warn | Pending final `community-v0.1.3` GitHub Release artifacts |
| Install smoke | Warn | Pending clean install smoke for the published wheel |
| Public boundary | Pass | `bash scripts/validate-boundaries.sh .` |
| CI evidence | Pass | Release-prep PR local validation and GitHub checks |

## Accepted Risk

Final v0.1.3 artifact checksums and clean-install smoke cannot be recorded
until the release-prep PR is merged and artifacts are built from `main`. This
risk expires before public announcement evidence is produced. The compensating
control is to publish the GitHub Release from merged `main`, run
`scripts/verify-community-release-artifacts.py`, and replace pending artifact
evidence with post-release verification.

## Validation Commands

```bash
python3 scripts/validate-python-package-metadata.py
python3 -m build
python3 -m twine check dist/*
python3 scripts/validate-maintenance-release-evidence.py
python3 scripts/validate-community-release-note-freshness.py
bash scripts/validate-boundaries.sh .
python3 -m pytest -q
```

## Boundary Notice

This packet covers public Community release-prep evidence only. Enterprise
source code, paid policy packs, SaaS backend implementation, license-service
internals, private keys, private registry credentials, and customer records are
not included.

## Decision

Decision: defer final publication until artifacts are built from merged `main`
and post-release verification is recorded.

## Next Recommendation

Publish Community v0.1.3 GitHub Release from merged main after Node 24 readiness and replace pending artifact evidence with post-release verification.
