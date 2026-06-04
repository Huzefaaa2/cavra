# Community v0.1.1 Maintenance Release Dry-Run Verification

Release: CAVRA Community v0.1.1 dry run
Release State: `ready_with_accepted_risk`
Prepared By: `release-agent`
Prepared At: 2026-06-04T00:00:00Z

## Scope

- Edition: Community
- Planned release tag: `community-v0.1.1`
- Planned GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1>
- Release notes: `docs/releases/community-v0.1.1.md`
- Verification workflow:
  `https://github.com/Huzefaaa2/cavra/actions/workflows/verify-community-release.yml`
- Wiki sync commit: pending until this dry-run packet is merged and synced.

## Required Gate Results

| Gate | Status | Evidence Reference | Owner | Notes |
| --- | --- | --- | --- | --- |
| Release notes | pass | `docs/releases/community-v0.1.1.md` | release-agent | Dry-run release notes are present and linked. |
| Changelog | pass | `CHANGELOG.md` | release-agent | Changelog records the dry-run governance update. |
| README link | pass | `README.md` | docs-agent | README links the dry-run release notes and verification packet. |
| Wiki link | pass | `docs/wiki/Home.md` | docs-agent | Wiki-ready navigation links dry-run release notes and verification pages. |
| Verification workflow | warn | `.github/workflows/verify-community-release.yml` | release-agent | Workflow exists; it must be run against real v0.1.1 artifacts after publication. |
| Artifact checksums | warn | `scripts/verify-community-release-artifacts.py` | release-agent | No v0.1.1 artifacts exist yet; checksums must be captured after publication. |
| Install smoke | warn | `cavra version` | test-agent | Clean venv install smoke must run after the real wheel is published. |
| Public boundary | pass | `bash scripts/validate-boundaries.sh .` | security-agent | Public boundary validation covers this dry-run packet. |
| CI evidence | pass | GitHub required checks | release-agent | Required checks validate the dry-run evidence structure and links. |

## Validation Commands

```bash
python3 scripts/validate-maintenance-release-evidence.py
python3 scripts/validate-community-release-note-freshness.py
python3 scripts/validate-release-packets.py
bash scripts/validate-boundaries.sh .
python3 -m pytest -q
```

## Accepted Risks

| Risk | Severity | Owner | Expiry | Compensating Control | Decision |
| --- | --- | --- | --- | --- | --- |
| v0.1.1 artifacts are not published during dry run | low | release-agent | 2026-07-04 | Keep release state as `ready_with_accepted_risk`; rerun verification workflow and replace warnings with passing evidence after real publication. | accepted |

## Public Boundary Review

- Enterprise source included: no
- Paid policy packs included: no
- Customer records included: no
- Private keys included: no
- Private registry credentials included: no
- Boundary validation result: pass

## Decision

Decision: defer real publication.

Rationale: the public Community maintenance-release evidence path is ready for
a future v0.1.1 release, but actual artifact checksum and install-smoke evidence
must wait until a real tag and release artifacts are published.

## Next Recommendation

Complete enterprise integration validation for GitHub App/orchestrator production hardening, GitLab/Azure DevOps parity, SAML identity readiness, and SIEM/ITSM workflow evidence.
