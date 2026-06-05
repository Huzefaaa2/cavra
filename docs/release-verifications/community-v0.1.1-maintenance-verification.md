# Community v0.1.1 Maintenance Release Verification

Release: CAVRA Community v0.1.1
Release State: `ready_for_publication`
Prepared By: `release-agent`
Prepared At: 2026-06-04T00:00:00Z

## Scope

- Edition: Community
- Release tag: `community-v0.1.1`
- GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1>
- Release notes: `docs/releases/community-v0.1.1.md`
- Verification workflow:
  `https://github.com/Huzefaaa2/cavra/actions/workflows/verify-community-release.yml`
- Wiki sync commit: pending until this release-conversion packet is merged and synced.

## Required Gate Results

| Gate | Status | Evidence Reference | Owner | Notes |
| --- | --- | --- | --- | --- |
| Release notes | pass | `docs/releases/community-v0.1.1.md` | release-agent | Official maintenance-release notes are present and linked. |
| Changelog | pass | `CHANGELOG.md` | release-agent | Changelog records the v0.1.1 maintenance-release conversion. |
| README link | pass | `README.md` | docs-agent | README links the v0.1.1 release notes and verification packet. |
| Wiki link | pass | `docs/wiki/Home.md` | docs-agent | Wiki-ready navigation links v0.1.1 release notes and verification pages. |
| Verification workflow | pass | `.github/workflows/verify-community-release.yml` | release-agent | Workflow defaults now target `community-v0.1.1` with recorded checksums. |
| Artifact checksums | pass | `dist/cavra-0.1.1*` | release-agent | Wheel SHA-256 `32ab7a220eb5f25ea5ab42ccbc62a43b7260de12b9a0d3f3d7bdafa1501a5d6a`; source distribution SHA-256 `b123c6d2aadd72b055ba916caa68953af94122d34f1215756804d74e91174950`. |
| Install smoke | pass | `cavra version` | test-agent | Clean virtual environment install returned `cavra 0.1.1`. |
| Public boundary | pass | `bash scripts/validate-boundaries.sh .` | security-agent | Public boundary validation covers this release packet. |
| CI evidence | pass | GitHub required checks | release-agent | Required checks validate the release evidence structure and links. |

## Validation Commands

```bash
rm -rf dist build src/cavra.egg-info
python3 -m build
shasum -a 256 dist/cavra-0.1.1.tar.gz dist/cavra-0.1.1-py3-none-any.whl
python3 scripts/validate-maintenance-release-evidence.py
python3 scripts/validate-community-release-note-freshness.py
python3 scripts/validate-release-packets.py
python3 scripts/validate-community-release-index.py
python3 scripts/validate-community-release-readiness-dashboard.py
bash scripts/validate-boundaries.sh .
python3 -m pytest -q
```

Clean install smoke:

```bash
python3 -m venv /tmp/cavra-v011-verify/venv
/tmp/cavra-v011-verify/venv/bin/python -m pip install --upgrade pip
/tmp/cavra-v011-verify/venv/bin/python -m pip install \
  dist/cavra-0.1.1-py3-none-any.whl
/tmp/cavra-v011-verify/venv/bin/cavra version
```

Expected output:

```text
cavra 0.1.1
```

After the GitHub Release is published, run the reusable public verifier:

```bash
python scripts/verify-community-release-artifacts.py
```

## Accepted Risks

None.

## Public Boundary Review

- Enterprise source included: no
- Paid policy packs included: no
- Customer records included: no
- Private keys included: no
- Private registry credentials included: no
- Boundary validation result: pass

## Decision

Decision: approve publication.

Rationale: the Community v0.1.1 release notes, package metadata, artifact
checksums, install-smoke evidence, README links, wiki-ready pages, release
index, release dashboard, and public boundary checks are aligned for official
publication.

## Next Recommendation

Start Community v1.0.0 stabilization planning from the completed Node 24 readiness baseline with release signing, reproducible provenance, GA announcement readiness, and final operator evidence.
