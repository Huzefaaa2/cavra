# Community v0.1.2 Maintenance Release Verification

Release: CAVRA Community v0.1.2
Release State: `ready_for_publication`
Prepared By: `release-agent`
Prepared At: 2026-06-04T13:41:44Z

## Scope

- Edition: Community
- Release tag: `community-v0.1.2`
- GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.2>
- Release notes: `docs/releases/community-v0.1.2.md`
- Post-release verification:
  `docs/release-verifications/community-v0.1.2-post-release-verification.md`
- Verification workflow:
  `https://github.com/Huzefaaa2/cavra/actions/workflows/verify-community-release.yml`

## Required Gate Results

| Gate | Status | Evidence Reference | Owner | Notes |
| --- | --- | --- | --- | --- |
| Release notes | pass | `docs/releases/community-v0.1.2.md` | release-agent | Official maintenance release notes are present and linked. |
| Changelog | pass | `CHANGELOG.md` | release-agent | Changelog records the v0.1.2 package version bump, release publication, checksums, and verification evidence. |
| README link | pass | `README.md` | docs-agent | README links the v0.1.2 release notes, maintenance verification, and post-release verification packet. |
| Wiki link | pass | `docs/wiki/Home.md` | docs-agent | Wiki-ready navigation links v0.1.2 release notes, maintenance verification, and post-release verification pages. |
| Verification workflow | pass | `.github/workflows/verify-community-release.yml` | release-agent | Manual verification workflow remains available for published v0.1.2 artifacts. |
| Artifact checksums | pass | `cavra-0.1.2-py3-none-any.whl` and `cavra-0.1.2.tar.gz` | release-agent | Published GitHub Release asset checksums match the expected SHA-256 values. |
| Install smoke | pass | `cavra version` | test-agent | Published wheel installed in a clean temporary virtual environment and returned `cavra 0.1.2`. |
| Public boundary | pass | `bash scripts/validate-boundaries.sh .` | security-agent | Public boundary validation covers this release packet. |
| CI evidence | pass | Community CI, Test, CodeQL, Release Community, Release Security Readiness, and tag Test workflows | release-agent | Required checks validate package metadata, release workflow guards, public boundary, and tag-triggered release readiness. |

## Artifact Checksums

| Artifact | SHA-256 |
| --- | --- |
| `cavra-0.1.2.tar.gz` | `f7a477cfef65d77bd4c36520a83d256c1086e7b81ffcd9411ee9c68d017ab1d0` |
| `cavra-0.1.2-py3-none-any.whl` | `bbdb2f593ce3c14742446c1682c23bef7933925a02382a874e59b8ef7e389163` |

## Validation Commands

```bash
python3 scripts/validate-python-package-metadata.py
python3 -m pytest tests/test_package_metadata.py tests/test_ci_templates.py -q
python3 -m pytest -q
python3 -m build
python3 -m twine check dist/*
python3 scripts/verify-community-release-artifacts.py \
  --tag community-v0.1.2 \
  --version 0.1.2 \
  --wheel-sha256 bbdb2f593ce3c14742446c1682c23bef7933925a02382a874e59b8ef7e389163 \
  --sdist-sha256 f7a477cfef65d77bd4c36520a83d256c1086e7b81ffcd9411ee9c68d017ab1d0
python3 scripts/validate-maintenance-release-evidence.py
python3 scripts/validate-community-release-note-freshness.py
python3 scripts/validate-community-release-index.py
python3 scripts/validate-community-release-readiness-dashboard.py
bash scripts/validate-boundaries.sh .
```

## Accepted Risks

None.

## Public Boundary Review

- Enterprise source code included: no
- Enterprise source included: no
- Paid policy packs included: no
- Customer records included: no
- Private keys included: no
- Private registry credentials included: no
- Boundary validation result: pass

## Decision

Decision: approve official publication.

Rationale: the Community v0.1.2 release notes, package metadata, artifact
checksums, clean-install smoke evidence, README links, wiki-ready pages,
release index, release dashboard, and public boundary checks are aligned for
official publication.

## Next Recommendation

Publish Community v0.1.3 maintenance release after GitHub Actions Node 24
readiness and workflow verification are complete.
