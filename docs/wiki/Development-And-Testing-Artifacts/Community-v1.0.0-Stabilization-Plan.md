# Community v1.0.0 Stabilization Plan

This plan starts the public-safe Community v1.0.0 stabilization path from the
completed Node 24 readiness baseline and the published Community v0.1.3
maintenance release.

## Objective

Community v1.0.0 should be stable enough for public announcement only when a
user can verify the release artifacts, understand the operator path, inspect
the Evidence Console, and confirm that Enterprise-only implementation remains
outside the public Community repository.

## Scope

| Workstream | Required Evidence | Exit Condition |
| --- | --- | --- |
| Release signing | Release signing operations metadata, detached signatures, and keyless attestation guidance | Public release artifacts can be verified without exposing private signing keys. |
| Reproducible provenance | SLSA provenance, checksum manifest, SBOM metadata, and rebuild instructions | Maintainers can reproduce or verify artifacts from tagged source and recorded build inputs. |
| GA announcement readiness | README, release notes, wiki navigation, release dashboard, and announcement checklist | Public users can install, verify, and evaluate Community Edition without private context. |
| Final operator evidence | Operator runbook, Evidence Console path, release verifier output, and boundary validation | Auditors, platform teams, and CISOs can follow a single evidence chain. |
| Open-core boundary | Boundary validator output, Enterprise documentation, and private implementation warning | Community artifacts contain no Enterprise source, secrets, private policy packs, or customer material. |

## Required Public Artifacts

- `docs/community-v1.0.0-stabilization-plan.md`
- `docs/release-verifications/community-v1.0.0-stabilization-plan.json`
- `docs/releases/community-v1.0.0.md` before final publication
- `docs/release-verifications/community-v1.0.0-maintenance-verification.md`
- `docs/release-verifications/community-v1.0.0-post-release-verification.md`
- `docs/community-release-index.md`
- `docs/community-release-readiness-dashboard.md`
- `.github/workflows/verify-community-release.yml`
- `scripts/verify-community-release-artifacts.py`
- `scripts/validate-community-v100-stabilization.py`

## Release Gates

| Gate | Status | Owner | Evidence |
| --- | --- | --- | --- |
| Node 24 readiness baseline | Ready | release-agent | Community v0.1.3 workflows use Node 24-ready actions and verifier defaults. |
| Release signing plan | Planned | release-agent | `docs/release-signing-operations.md` and Go release signing metadata patterns. |
| Provenance plan | Planned | release-agent | SLSA provenance and SBOM patterns from Go release packaging. |
| Announcement checklist | Planned | docs-agent | README, wiki, release notes, release dashboard, and public sandbox path. |
| Operator evidence path | Planned | architect-agent | Evidence Console, operator runbook, release verifier, and public boundary validation. |
| Public boundary | Ready | security-agent | `scripts/validate-boundaries.sh .` and open-core boundary documentation. |

## Announcement Checklist

- [ ] `community-v1.0.0` release notes exist and link matching verification packets.
- [ ] Release index and readiness dashboard mark v1.0.0 as the current Community baseline.
- [ ] Release artifacts have SHA-256 checksums.
- [ ] Release artifacts are signed or have documented keyless attestation evidence.
- [ ] SLSA provenance and SBOM metadata are available or explicitly scoped for the Community artifact type.
- [ ] Clean install smoke returns `cavra 1.0.0`.
- [ ] README quickstart, docs navigation, and wiki navigation point to the v1.0.0 release.
- [ ] Evidence Console and operator docs show the user-verifiable GA path.
- [ ] Public boundary validation passes.
- [ ] No Enterprise source, paid policy pack, private key, license-service secret, private registry token, or customer material is included.

## User Stories

- As a developer, I can install Community v1.0.0 and verify that `cavra version`
  matches the release notes.
- As a platform engineer, I can validate checksums, signatures, and provenance
  before adding CAVRA to an internal golden image or CI runner.
- As a CISO, I can review a single public evidence path before approving a
  broader AI-agent governance pilot.
- As an auditor, I can confirm that the release was built from a tagged public
  source state and that Enterprise-only code was not included.

## Enterprise Challenge Solved

The v1.0.0 stabilization plan turns CAVRA from an evolving Community release
track into a publicly verifiable baseline. That matters for enterprise
adoption because buyers need artifact integrity, repeatable evidence,
operator-ready documentation, and a clear open-core boundary before they will
allow AI-agent governance controls into developer workstations, CI runners, or
regulated repositories.

## Boundary Notice

This plan covers public Community release stabilization only. It does not
include Enterprise source code, private policy packs, private trial packages,
license-service internals, SaaS backend implementation, private signing keys,
private registry credentials, or customer records.

## Next Recommendation

Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
