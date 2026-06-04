# Community Release Readiness Dashboard

This dashboard gives maintainers one public place to inspect CAVRA Community
release readiness. It rolls up the release index, freshness validators,
verification commands, CI evidence, publication state, and the next action for
each public Community release record.

## Release Readiness

| Release | State | Public Release | Release Evidence | Verification | Readiness | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| Community GA v0.1.0 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0> | `docs/releases/community-v0.1.0.md` | `docs/release-verifications/community-v0.1.0-post-release-verification.md` | Ready | Use as the current public Community GA baseline. |
| Community v0.1.1 | Dry run | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1> | `docs/releases/community-v0.1.1.md` | `docs/release-verifications/community-v0.1.1-maintenance-verification.md` | Pending real artifacts | Publish only after real v0.1.1 artifacts exist and verification warnings are replaced with passing evidence. |

## Control Rollup

| Control | Evidence | Purpose |
| --- | --- | --- |
| Release index | `docs/community-release-index.md` | Lists public Community release records, states, notes, verification packets, and next action. |
| Release-note freshness | `docs/community-release-note-freshness.md` | Verifies Community release notes link GitHub Releases, verification packets, README, and wiki pages. |
| Release-index freshness | `docs/community-release-index-freshness.md` | Verifies indexed release rows have valid state, release notes, verification packets, README links, and wiki links. |
| Maintenance-release evidence | `docs/community-maintenance-release-checklist.md` | Defines the post-GA Community maintenance release gate set. |
| Release packet validation | `docs/community-ga-release-packet-validation.md` | Validates Community GA release packet structure and required gates. |
| Readiness dashboard validation | `scripts/validate-community-release-readiness-dashboard.py` | Verifies dashboard rows, release links, freshness controls, verification commands, README navigation, wiki navigation, and publication state. |
| User-verifiable GA path | `docs/community-ga-user-verifiable-path.md` | Connects policy, evidence, console, Go runtime readiness, release verification, README, wiki navigation, and workflow validation into one public operator path. |
| Public boundary | `scripts/validate-boundaries.sh` | Checks public Community release paths for private-code and secret boundary drift. |

## Verification Commands

```bash
python3 scripts/validate-release-packets.py
python3 scripts/validate-maintenance-release-evidence.py
python3 scripts/validate-community-release-note-freshness.py
python3 scripts/validate-community-release-index.py
python3 scripts/validate-community-release-readiness-dashboard.py
python3 scripts/validate-community-ga-path.py
bash scripts/validate-boundaries.sh .
python3 -m pytest tests/test_release_documentation.py -q
```

## CI Evidence

Public Community release readiness is enforced by:

- `.github/workflows/community-ci.yml`
- `.github/workflows/security-scan.yml`
- `.github/workflows/release-community.yml`
- `.github/workflows/cavra-governance.yml`
- `.github/workflows/verify-community-release.yml`

## Boundary Notice

This dashboard covers public CAVRA Community release readiness only. It does not
include Enterprise source code, paid policy packs, SaaS backend implementation,
license-service internals, private registry details, private keys, or customer
records.

## Next Recommendation

Prepare the next official Community maintenance release by converting the
v0.1.1 dry-run packet into real release artifacts, verification evidence,
release notes, README links, and wiki navigation.
