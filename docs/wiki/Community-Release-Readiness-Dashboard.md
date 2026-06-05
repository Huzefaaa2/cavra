# Community Release Readiness Dashboard

This dashboard gives maintainers one public place to inspect CAVRA Community
release readiness. It rolls up the release index, freshness validators,
verification commands, CI evidence, publication state, and the next action for
each public Community release record.

## Release Readiness

| Release | State | Public Release | Release Evidence | Verification | Readiness | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| Community GA v0.1.0 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0> | `docs/releases/community-v0.1.0.md` | `docs/release-verifications/community-v0.1.0-post-release-verification.md` | Ready | Use as the current public Community GA baseline. |
| Community v0.1.1 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1> | `docs/releases/community-v0.1.1.md` | `docs/release-verifications/community-v0.1.1-post-release-verification.md` | Ready | Use as the previous public Community maintenance baseline. |
| Community v0.1.2 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.2> | `docs/releases/community-v0.1.2.md` | `docs/release-verifications/community-v0.1.2-post-release-verification.md` | Ready | Use as the previous published Community maintenance baseline. |
| Community v0.1.3 | Published | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.3> | `docs/releases/community-v0.1.3.md` | `docs/release-verifications/community-v0.1.3-post-release-verification.md` | Ready | Use as the current published Community maintenance baseline while v1.0.0 stabilization planning begins. |
| Community v1.0.0 RC1 | Dry run | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1> | `docs/releases/community-v1.0.0-rc.1.md` | `docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md` | Pending real artifacts | Publish Community v1.0.0 release-candidate artifacts from the completed Node 24 readiness baseline and record signed artifact checksums, provenance, GitHub Release links, and post-publication verification evidence. |

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
| Public boundary | `scripts/validate-boundaries.sh` | Checks that public Community release paths do not include Enterprise code, secrets, private keys, or customer data. |

## Verification Commands

Run these commands before publishing or updating public Community release
records:

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

## Maintainer Workflow

1. Start with `docs/community-release-index.md` to identify the current release
   state.
2. Open this dashboard to inspect readiness, validation commands, and CI
   evidence.
3. For a maintenance release, verify artifact checksums, release notes,
   README links, wiki navigation, and install-smoke evidence before publishing.
4. Run all verification commands before opening or merging release
   documentation changes.
5. Sync `docs/wiki` pages to the GitHub wiki after every release documentation
   PR that updates public release records.

## Boundary Notice

This dashboard covers public CAVRA Community release readiness only. It does not
include Enterprise source code, paid policy packs, SaaS backend implementation,
license-service internals, private registry details, private keys, or customer
records.

## Next Recommendation

Publish Community v1.0.0 release-candidate artifacts from the completed Node 24 readiness baseline and record signed artifact checksums, provenance, GitHub Release links, and post-publication verification evidence.
