# Community v1.0.0 GA Readiness

This wiki page mirrors the public GA readiness packet for CAVRA Community
v1.0.0. It advances the published RC1 evidence baseline into final GA
publication preparation.

## Scope

| Item | Status | Evidence |
| --- | --- | --- |
| RC1 feedback baseline | Ready | `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md` |
| Node 24 readiness baseline | Ready | Community workflows use Node 24-ready action versions. |
| Upgrade notes | Ready for GA publication package | Community v0.1.3 and v1.0.0 RC1 upgrade guidance is documented. |
| Installer paths | Ready for GA publication package | Python wheel, source distribution, Community Docker image, GitHub Actions verifier, and source install paths are documented. |
| Announcement copy | Ready for approval | Public announcement copy is drafted and public-safe. |
| Final GA evidence gates | Ready for publication package | Final artifacts, checksums, provenance, signatures or attestations, release notes, README, wiki, and dashboard must be updated together. |
| Public boundary | Ready | Enterprise source code, paid policy packs, private signing keys, license-service secrets, private registry credentials, and customer records remain outside the public Community repository. |

## Upgrade Notes

- From `0.1.3`: reinstall CAVRA Community from the final `community-v1.0.0`
  wheel or source distribution, then run `cavra version` and verify it returns
  `cavra 1.0.0`.
- From `1.0.0rc1`: replace the release-candidate package with the final
  `1.0.0` package, rerun policy validation, and verify evidence bundle
  generation still works.
- Existing Community policies remain public Community policies; Enterprise
  features still require private packages and must not be expected in the
  public Community artifact.

## Installer Paths

| Path | Command or Evidence | GA Gate |
| --- | --- | --- |
| Python wheel | `python3 -m pip install cavra-1.0.0-py3-none-any.whl` | Clean install smoke returns `cavra 1.0.0`. |
| Source distribution | `python3 -m pip install cavra-1.0.0.tar.gz` | Source distribution installs without private dependencies. |
| GitHub Release download | `https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0` | Release assets are downloadable and match SHA-256 checksums. |
| Community Docker image | `docker build -f docker/Dockerfile.community .` | Image builds only Community source and runs without a license key. |
| GitHub Actions verifier | `.github/workflows/verify-community-release.yml` | Defaults must point to `community-v1.0.0` after final artifacts exist. |
| Source checkout | `python3 -m pip install -e ".[dev]"` | Public source install runs tests and validators without Enterprise packages. |

## Announcement Copy

> CAVRA Community v1.0.0 is the first stable public Community baseline for
> Controlled Agentic Verification and Runtime Authority. It gives developers,
> platform teams, and security leaders a public, verifiable way to run local
> policy evaluation, collect evidence, validate release integrity, and inspect
> the AI-agent governance path without exposing Enterprise source code or
> private commercial modules.

## Final GA Evidence Gates

| Gate | Required Result |
| --- | --- |
| Final tag | `community-v1.0.0` points at the approved `main` commit. |
| Package version | Python metadata and runtime report `1.0.0`. |
| Artifact checksums | Wheel and source distribution SHA-256 checksums are recorded. |
| Provenance metadata | Public provenance file is attached or explicitly scoped. |
| Signatures or attestations | Detached signatures or keyless attestation evidence is attached, or any gap is documented as a release blocker. |
| Clean install smoke | `cavra version` returns `cavra 1.0.0`. |
| Release notes freshness | `docs/releases/community-v1.0.0.md` links matching verification evidence. |
| Public boundary | Boundary validation passes with no Enterprise source, paid policy packs, private keys, license-service secrets, private registry credentials, or customer records. |

## Boundary Notice

This packet covers public Community GA readiness only. It does not include
Enterprise source code, paid policy packs, private trial packages,
license-service internals, SaaS backend implementation, private signing keys,
private registry credentials, customer records, or private deployment evidence.

## Decision

Decision: approve GA publication package preparation.

## Validation

```bash
python3 scripts/validate-community-v100-ga-readiness.py
```

## Next Recommendation

Prepare Community v1.0.0 GA publication package from validated RC1 feedback and the completed Node 24 readiness baseline by drafting final release notes, v1.0.0 artifact build plan, verifier inputs, and announcement approval evidence.
