# Community v1.0.0 GA Publication Package

This package prepares CAVRA Community v1.0.0 for final GA publication from the
validated RC1 feedback baseline and the completed Node 24 readiness baseline.
It drafts final release notes, defines the v1.0.0 artifact build plan, records
verifier inputs, and captures announcement approval evidence before final
`community-v1.0.0` artifacts are published.

## Publication Target

| Field | Value |
| --- | --- |
| Release | CAVRA Community v1.0.0 |
| Target tag | `community-v1.0.0` |
| Target package version | `1.0.0` |
| Planned GitHub Release | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0> |
| Baseline release candidate | `community-v1.0.0-rc.1` |
| Baseline evidence | `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md` |
| GA readiness packet | `docs/community-v1.0.0-ga-readiness.md` |
| Draft release notes | `docs/releases/community-v1.0.0.md` |
| Publication readiness verification | `docs/release-verifications/community-v1.0.0-publication-readiness.md` |
| Publication package packet | `docs/release-verifications/community-v1.0.0-ga-publication-package.json` |

## Artifact Build Plan

The final GA release must be built from the approved `main` commit after the
package version changes from `1.0.0rc1` to `1.0.0`.

| Artifact | Planned Name | Build Source | Required Verification |
| --- | --- | --- | --- |
| Python wheel | `cavra-1.0.0-py3-none-any.whl` | `python3 -m build` from tagged public source | SHA-256 checksum, clean install smoke, `cavra version` returns `cavra 1.0.0`. |
| Source distribution | `cavra-1.0.0.tar.gz` | `python3 -m build` from tagged public source | SHA-256 checksum, install from sdist, no private dependencies. |
| Checksum manifest | `cavra-1.0.0-SHA256SUMS.txt` | Generated from release artifacts | Contains wheel, sdist, and provenance checksums. |
| Provenance metadata | `cavra-1.0.0.provenance.json` | Public build metadata | Records tag, commit, build command, Python version, and public artifact hashes. |
| Community Docker image | Community image from `docker/Dockerfile.community` | Public source tree only | Builds without Enterprise packages and runs without a license key. |

## Verifier Inputs

The reusable Community release verifier must be updated after the final
artifacts exist:

```yaml
tag: community-v1.0.0
version: "1.0.0"
wheel_sha256: "<final wheel SHA-256>"
sdist_sha256: "<final source distribution SHA-256>"
```

The final verification command must be:

```bash
python3 scripts/verify-community-release-artifacts.py \
  --tag community-v1.0.0 \
  --version 1.0.0 \
  --wheel-sha256 <final wheel SHA-256> \
  --sdist-sha256 <final source distribution SHA-256>
```

## Announcement Approval Evidence

Announcement copy is approved for final maintainer review only after these
public-safe checks pass:

| Approval Check | Status | Evidence |
| --- | --- | --- |
| Message scope | Ready for approval | Announcement describes public Community v1.0.0 and links Enterprise documentation without exposing Enterprise implementation. |
| Artifact integrity | Pending final artifacts | Final SHA-256 checksums, provenance metadata, and signature or attestation evidence must be attached before announcement. |
| Install path | Pending final artifacts | Clean wheel and source distribution installs must return `cavra 1.0.0`. |
| Documentation freshness | Ready for publication package | README, release notes, release index, readiness dashboard, and wiki navigation include the GA publication package. |
| Public boundary | Ready | Enterprise source code, paid policy packs, private signing keys, license-service secrets, private registry credentials, and customer records remain outside the public repository. |

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
- [x] Public boundary requirements are documented.
- [ ] Package metadata is bumped from `1.0.0rc1` to `1.0.0`.
- [ ] `community-v1.0.0` tag is created from approved `main`.
- [ ] Final artifacts are built and attached to the GitHub Release.
- [ ] Final artifact SHA-256 checksums are recorded.
- [ ] Signature or keyless attestation evidence is attached or treated as a
  release blocker.
- [ ] Clean install smoke returns `cavra 1.0.0`.
- [ ] Verifier workflow defaults are updated to final artifact hashes.
- [ ] Post-publication verification is recorded before announcement.

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

Community v1.0.0 final artifacts are not published yet. The next step is to
bump package metadata to `1.0.0`, build final artifacts, attach them to the
GitHub Release, record checksums/provenance, and complete post-publication
verification.

## Next Recommendation

Publish Community v1.0.0 GA artifacts from the approved publication package and completed Node 24 readiness baseline by bumping package metadata to 1.0.0, building final artifacts, attaching GitHub Release assets, recording checksums and provenance, and completing post-publication verification.
