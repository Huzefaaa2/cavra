# Community v1.0.0 GA Publication Package

This wiki page mirrors the public GA publication package for CAVRA Community
v1.0.0. It prepares final release notes, artifact build planning, verifier
inputs, and announcement approval evidence before final artifacts are
published.

## Publication Target

| Field | Value |
| --- | --- |
| Release | CAVRA Community v1.0.0 |
| Target tag | `community-v1.0.0` |
| Target package version | `1.0.0` |
| Planned GitHub Release | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0> |
| Baseline release candidate | `community-v1.0.0-rc.1` |
| GA readiness packet | `docs/community-v1.0.0-ga-readiness.md` |
| Draft release notes | `docs/releases/community-v1.0.0.md` |
| Publication readiness verification | `docs/release-verifications/community-v1.0.0-publication-readiness.md` |

## Artifact Build Plan

| Artifact | Planned Name | Required Verification |
| --- | --- | --- |
| Python wheel | `cavra-1.0.0-py3-none-any.whl` | SHA-256 checksum, clean install smoke, `cavra version` returns `cavra 1.0.0`. |
| Source distribution | `cavra-1.0.0.tar.gz` | SHA-256 checksum, install from sdist, no private dependencies. |
| Checksum manifest | `cavra-1.0.0-SHA256SUMS.txt` | Contains wheel, sdist, and provenance checksums. |
| Provenance metadata | `cavra-1.0.0.provenance.json` | Records tag, commit, build command, Python version, and public artifact hashes. |
| Community Docker image | `docker/Dockerfile.community` | Builds only Community source and runs without a license key. |

## Verifier Inputs

```yaml
tag: community-v1.0.0
version: "1.0.0"
wheel_sha256: "<final wheel SHA-256>"
sdist_sha256: "<final source distribution SHA-256>"
```

## Announcement Approval Evidence

Draft announcement:

> CAVRA Community v1.0.0 is the stable public Community baseline for
> Controlled Agentic Verification and Runtime Authority. It provides a
> verifiable public path for local policy evaluation, evidence generation,
> release integrity checks, and AI-agent governance adoption while preserving a
> strict open-core boundary around Enterprise source code and commercial
> modules.

## Publication Checklist

- [x] Draft final release notes exist at `docs/releases/community-v1.0.0.md`.
- [x] Publication readiness verification exists at
  `docs/release-verifications/community-v1.0.0-publication-readiness.md`.
- [x] Release index and dashboard include a dry-run GA publication row.
- [x] README and wiki navigation link the GA publication package.
- [ ] Package metadata is bumped from `1.0.0rc1` to `1.0.0`.
- [ ] Final artifacts are built and attached to the GitHub Release.
- [ ] Final artifact SHA-256 checksums are recorded.
- [ ] Clean install smoke returns `cavra 1.0.0`.

## Boundary Notice

This package covers public Community GA publication preparation only. It does
not include Enterprise source code, paid policy packs, private trial packages,
license-service internals, SaaS backend implementation, private signing keys,
private registry credentials, customer records, or private deployment evidence.

## Validation

```bash
python3 scripts/validate-community-v100-ga-publication-package.py
```

## Decision

Decision: approve final GA artifact publication preparation.

## Next Recommendation

Publish Community v1.0.0 GA artifacts from the approved publication package and completed Node 24 readiness baseline by bumping package metadata to 1.0.0, building final artifacts, attaching GitHub Release assets, recording checksums and provenance, and completing post-publication verification.
