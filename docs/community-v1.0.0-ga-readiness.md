# Community v1.0.0 GA Readiness

This packet advances CAVRA Community v1.0.0 from the published RC1 evidence
baseline into GA release readiness. It validates upgrade notes, installer
paths, announcement copy, and final GA evidence gates before the final
`community-v1.0.0` artifacts are built or announced.

## Scope

| Item | Status | Evidence |
| --- | --- | --- |
| RC1 feedback baseline | Ready | `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md` |
| Node 24 readiness baseline | Ready | Community CI, release, security, governance, and verification workflows use Node 24-ready action versions. |
| Upgrade notes | Ready for GA publication package | Community v0.1.3 and v1.0.0 RC1 users can upgrade to v1.0.0 using the public package and Docker paths below. |
| Installer paths | Ready for GA publication package | Python wheel, source distribution, Community Docker image, GitHub Actions verifier, and source install paths are documented. |
| Announcement copy | Ready for approval | Public announcement copy is drafted below and remains public-safe. |
| Final GA evidence gates | Ready for publication package | Final artifacts, checksums, provenance, signatures or attestations, release notes, README, wiki, and dashboard must be updated together. |
| Public boundary | Ready | Enterprise source code, paid policy packs, private signing keys, license-service secrets, private registry credentials, and customer records remain outside the public Community repository. |

## Upgrade Notes

Community v1.0.0 GA should be treated as the first stable public baseline after
the v1.0.0 RC1 candidate. Users should upgrade from either Community v0.1.3 or
Community v1.0.0 RC1 by installing the final `1.0.0` package from the
published GitHub Release artifact or the approved package index path once the
GA artifacts exist.

Expected user-facing upgrade notes for the final GA package:

- From `0.1.3`: reinstall CAVRA Community from the final `community-v1.0.0`
  wheel or source distribution, then run `cavra version` and verify it returns
  `cavra 1.0.0`.
- From `1.0.0rc1`: replace the release-candidate package with the final
  `1.0.0` package, rerun policy validation, and verify evidence bundle
  generation still works.
- Existing Community policies remain public Community policies; Enterprise
  features still require private packages and must not be expected in the
  public Community artifact.
- Final GA release notes must link the matching post-release verification
  packet, checksum manifest, provenance evidence, README entry, wiki entry, and
  release readiness dashboard row.

## Installer Paths

The final GA publication package must validate these installation paths before
announcement:

| Path | Command or Evidence | GA Gate |
| --- | --- | --- |
| Python wheel | `python3 -m pip install cavra-1.0.0-py3-none-any.whl` | Clean install smoke returns `cavra 1.0.0`. |
| Source distribution | `python3 -m pip install cavra-1.0.0.tar.gz` | Source distribution installs without private dependencies. |
| GitHub Release download | `https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0` | Release assets are downloadable and match SHA-256 checksums. |
| Community Docker image | `docker build -f docker/Dockerfile.community .` | Image builds only Community source and runs without a license key. |
| GitHub Actions verifier | `.github/workflows/verify-community-release.yml` | Defaults must point to `community-v1.0.0` after final artifacts exist. |
| Source checkout | `python3 -m pip install -e ".[dev]"` | Public source install runs tests and validators without Enterprise packages. |

## Announcement Copy

Draft public announcement copy for maintainer approval:

> CAVRA Community v1.0.0 is the first stable public Community baseline for
> Controlled Agentic Verification and Runtime Authority. It gives developers,
> platform teams, and security leaders a public, verifiable way to run local
> policy evaluation, collect evidence, validate release integrity, and inspect
> the AI-agent governance path without exposing Enterprise source code or
> private commercial modules.

Announcement approval requires the final GA release notes, release verification
packet, README links, wiki navigation, release index, release dashboard, and
public boundary validator to pass after the final `community-v1.0.0` artifacts
are attached.

## Final GA Evidence Gates

| Gate | Required Result | Evidence Owner |
| --- | --- | --- |
| Final tag | `community-v1.0.0` points at the approved `main` commit | release-agent |
| Package version | Python metadata and runtime report `1.0.0` | release-agent |
| Artifact checksums | Wheel and source distribution SHA-256 checksums are recorded | release-agent |
| Provenance metadata | Public provenance file is attached or explicitly scoped | release-agent |
| Signatures or attestations | Detached signatures or keyless attestation evidence is attached, or any gap is documented as a release blocker | security-agent |
| Clean install smoke | `cavra version` returns `cavra 1.0.0` from a clean environment | test-agent |
| Release notes freshness | `docs/releases/community-v1.0.0.md` links the matching verification packet, README, and wiki entry | docs-agent |
| Dashboard freshness | Release index and readiness dashboard mark v1.0.0 as the current published Community baseline | docs-agent |
| Public boundary | Boundary validation passes with no Enterprise source, paid policy packs, private keys, license-service secrets, private registry credentials, or customer records | security-agent |
| Announcement approval | Maintainer-approved announcement copy references only public Community and Enterprise documentation, not private implementation | release-agent |

## User Stories

- As a developer, I can upgrade from RC1 to GA and verify `cavra 1.0.0` from a
  clean install.
- As a platform engineer, I can choose a supported installer path and verify
  the final artifact checksums before internal rollout.
- As a CISO, I can read the announcement and evidence gates without needing
  access to private Enterprise source.
- As an auditor, I can trace the final GA evidence from release notes to the
  verification packet, release dashboard, README, wiki, and GitHub Release.

## Enterprise Challenge Solved

This readiness packet reduces release risk before a public launch. It makes
the final GA release auditable by requiring install verification, artifact
integrity, announcement approval, documentation freshness, and a strict
open-core boundary before CAVRA is announced as stable.

## Boundary Notice

This packet covers public Community GA readiness only. It does not include
Enterprise source code, paid policy packs, private trial packages,
license-service internals, SaaS backend implementation, private signing keys,
private registry credentials, customer records, or private deployment evidence.

## Validation

```bash
python3 scripts/validate-community-v100-ga-readiness.py
```

## Decision

Decision: approve GA publication package preparation.

Community v1.0.0 is not yet GA-published. The next step is to prepare the
final publication package with release notes, artifact build plan, verifier
inputs, and announcement approval evidence.

## Next Recommendation

Prepare Community v1.0.0 GA publication package from validated RC1 feedback and the completed Node 24 readiness baseline by drafting final release notes, v1.0.0 artifact build plan, verifier inputs, and announcement approval evidence.
