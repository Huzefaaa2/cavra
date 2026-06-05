# Community v1.0.0 RC1 Publication Readiness Verification

This packet verifies that CAVRA Community v1.0.0 RC1 is ready to be published
as a dry-run release-candidate record. It does not claim that final artifacts
exist yet.

## Release Metadata

| Field | Value |
| --- | --- |
| Release | CAVRA Community v1.0.0 RC1 |
| State | `dry-run-publication-ready` |
| Repository | `Huzefaaa2/cavra` |
| Tag | `community-v1.0.0-rc.1` |
| Version | `1.0.0` |
| Planned GitHub Release | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1> |
| Release notes | `docs/releases/community-v1.0.0-rc.1.md` |
| Publication preparation | `docs/community-v1.0.0-release-candidate-publication.md` |
| Verification workflow | <https://github.com/Huzefaaa2/cavra/actions/workflows/verify-community-release.yml> |

## Gate Summary

| Gate | Status | Evidence |
| --- | --- | --- |
| Node 24 readiness baseline | Pass | Current Community workflows use Node 24-ready action versions. |
| Release notes | Pass | `docs/releases/community-v1.0.0-rc.1.md` |
| README link | Pass | `README.md` links RC1 release notes, readiness verification, and publication packet. |
| Wiki link | Pass | `docs/wiki/Home.md` links RC1 release notes, verification, and publication preparation. |
| Release index | Pass | `docs/community-release-index.md` includes RC1 as a dry-run release record. |
| Readiness dashboard | Pass | `docs/community-release-readiness-dashboard.md` includes RC1 with pending real artifacts. |
| Signed artifact verification | Warn | Pending real `community-v1.0.0-rc.1` artifacts, SHA-256 checksums, signatures, and attestations. |
| Provenance evidence | Warn | Pending real SBOM and SLSA provenance references from the release workflow. |
| Install smoke | Warn | Pending clean install smoke from the published wheel. |
| Public boundary | Pass | `bash scripts/validate-boundaries.sh .` remains mandatory before publication. |

The dry-run record is announcement-ready for documentation review, but not for
public release announcement until signed artifact verification and provenance
evidence are recorded from real artifacts.

## Accepted Risk

This is a dry-run publication readiness record. Final artifact checksums,
detached signatures, keyless attestation evidence, SBOM metadata, SLSA
provenance, GitHub Release asset links, and clean install smoke cannot be
recorded until the RC1 release is published from merged `main`.

The compensating control is to keep RC1 indexed as `Dry run`, mark readiness as
`Pending real artifacts`, and require post-publication verification before
announcing RC1 as published.

## Validation Commands

```bash
python3 scripts/validate-community-v100-rc-publication.py
python3 scripts/validate-community-v100-rc-hardening.py
python3 scripts/validate-community-release-note-freshness.py
python3 scripts/validate-community-release-index.py
python3 scripts/validate-community-release-readiness-dashboard.py
bash scripts/validate-boundaries.sh .
```

## Boundary Notice

This verification covers public Community release-candidate readiness only.
Enterprise source code, paid policy packs, SaaS backend implementation,
license-service internals, private signing keys, private registry credentials,
and customer records are not included.

## Decision

Decision: approve RC1 dry-run publication readiness.

Final publication still requires real artifacts, signed artifact checksums,
provenance evidence, GitHub Release links, and post-publication verification.

## Next Recommendation

Publish Community v1.0.0 release-candidate artifacts from the completed Node 24 readiness baseline and record signed artifact checksums, provenance, GitHub Release links, and post-publication verification evidence.
