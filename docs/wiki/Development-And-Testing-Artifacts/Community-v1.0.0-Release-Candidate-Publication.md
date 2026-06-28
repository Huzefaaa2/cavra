# Community v1.0.0 Release-Candidate Publication Preparation

This packet prepares the public Community v1.0.0 release-candidate publication
from the completed Node 24 readiness baseline, the stabilization plan, and the
release-candidate hardening packet.

## Objective

Community v1.0.0 RC1 can be published only after the maintainer can produce a
tagged public source state, release notes, signed artifact verification,
provenance evidence, and announcement-ready documentation without exposing
Enterprise source code, private signing keys, private policy packs, private
registry credentials, or customer material.

## Publication Target

| Field | Value |
| --- | --- |
| Candidate | CAVRA Community v1.0.0 RC1 |
| Tag | `community-v1.0.0-rc.1` |
| Package version | `1.0.0rc1` |
| Release state | `dry-run-publication-ready` |
| Planned GitHub Release | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1> |
| Release notes draft | `docs/releases/community-v1.0.0-rc.1.md` |
| Publication readiness verification | `docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md` |
| Publication packet | `docs/release-verifications/community-v1.0.0-release-candidate-publication.json` |
| Validator | `scripts/validate-community-v100-rc-publication.py` |

## Publication Gates

| Gate | Status | Evidence |
| --- | --- | --- |
| Node 24 readiness baseline | Ready | Community CI, release, security, governance, and verification workflows use Node 24-ready action versions. |
| Release notes | Ready | `docs/releases/community-v1.0.0-rc.1.md` describes the RC scope, dry-run state, and verification path. |
| Signed artifact verification | Pending real artifacts | Final SHA-256 checksums, detached signatures, and keyless attestation links must be recorded after artifacts exist. |
| Provenance evidence | Pending real artifacts | Final SBOM and SLSA provenance references must be recorded after the release workflow produces artifacts. |
| Announcement readiness | Ready | README, wiki navigation, release index, release dashboard, and release notes point to the RC1 dry-run record. |
| Public boundary | Ready | `bash scripts/validate-boundaries.sh .` remains mandatory before publishing the RC. |

## Operator Runbook

1. Create the `community-v1.0.0-rc.1` tag from merged `main`.
2. Run the Community release workflow and attach only public Community artifacts.
3. Record SHA-256 checksums for every attached artifact.
4. Attach detached signatures or keyless attestation evidence for every artifact.
5. Attach SBOM and SLSA provenance evidence when produced by the workflow.
6. Run `scripts/verify-community-release-artifacts.py --tag community-v1.0.0-rc.1`.
7. Replace the dry-run readiness packet with post-publication verification.
8. Confirm `README.md`, `docs/community-release-index.md`, `docs/community-release-readiness-dashboard.md`, and `docs/wiki/Home.md` all point to the published RC.
9. Run `scripts/validate-community-v100-rc-publication.py`.
10. Run `scripts/validate-boundaries.sh .`.

## Announcement Checklist

- [x] RC1 release notes draft exists.
- [x] RC1 publication readiness verification exists.
- [x] README links RC1 release notes, readiness verification, and publication packet.
- [x] Wiki navigation links RC1 release notes, verification, and publication preparation.
- [x] Release index and readiness dashboard include RC1 as a dry-run record.
- [x] Publication validator runs in Community CI, security scan, release, and governance workflows.
- [ ] GitHub Release exists for `community-v1.0.0-rc.1`.
- [ ] Published artifacts include SHA-256 checksums.
- [ ] Published artifacts include detached signatures or keyless attestation evidence.
- [ ] Published artifacts include SBOM and SLSA provenance references when generated.
- [ ] Clean install smoke records `cavra 1.0.0rc1`.

## User Stories

- As a developer, I can inspect the RC1 release notes before the release is
  published and understand which verification steps will become mandatory.
- As a platform engineer, I can see exactly where checksums, signatures, and
  provenance must be recorded before testing RC1 internally.
- As a CISO, I can confirm the RC announcement path is gated on public boundary
  validation and does not depend on private Enterprise implementation.
- As an auditor, I can trace the RC1 dry-run record to the future tagged
  release, verification packet, README links, and wiki navigation.

## Current Decision

Decision: approve RC1 publication preparation as a dry-run release record.

The actual Community v1.0.0 RC1 release must still be published from merged
`main`, and final artifact checksums, signature verification, provenance
evidence, release links, and post-publication verification must be recorded
after artifacts exist.

## Boundary Notice

This publication preparation covers public Community release-candidate
documentation only. It does not include Enterprise source code, private policy
packs, SaaS backend implementation, license-service internals, private signing
keys, private registry credentials, customer templates, or customer records.

## Next Recommendation

Publish Community v1.0.0 release-candidate artifacts from the completed Node 24 readiness baseline and record signed artifact checksums, provenance, GitHub Release links, and post-publication verification evidence.
