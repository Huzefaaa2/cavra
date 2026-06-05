# CAVRA Community v1.0.0 RC1 Release Notes

CAVRA Community v1.0.0 RC1 is a dry-run publication-ready release-candidate
record. It prepares the public release notes, verification packet, README
links, wiki navigation, release index, and release dashboard before the actual
`community-v1.0.0-rc.1` artifacts are published.

## Release Links

- Planned GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1>
- Publication preparation:
  `docs/community-v1.0.0-release-candidate-publication.md`
- Publication readiness verification:
  `docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md`
- Release-candidate hardening:
  `docs/community-v1.0.0-release-candidate-hardening.md`
- Stabilization plan:
  `docs/community-v1.0.0-stabilization-plan.md`
- Release index:
  `docs/community-release-index.md`
- Release readiness dashboard:
  `docs/community-release-readiness-dashboard.md`

## What Changed

- Prepared the public Community v1.0.0 RC1 publication path from the completed
  Node 24 readiness baseline.
- Added dry-run release notes and publication readiness verification before
  final artifacts exist.
- Prepared the announcement-ready public documentation path for the RC1
  artifact publication step.
- Kept signed artifact verification, SHA-256 checksums, detached signatures,
  keyless attestation links, SBOM metadata, and SLSA provenance as required
  post-publication evidence.
- Kept public boundary validation mandatory before the RC can be announced.
- Confirmed the RC1 record is public Community documentation only and does not
  include Enterprise source code or private release material.

## Artifact Verification

RC1 artifacts are not published yet. The final publication record must replace
this dry-run section with:

- the source distribution artifact name and SHA-256 checksum;
- the wheel artifact name and SHA-256 checksum;
- detached signature or keyless attestation references;
- SBOM metadata reference;
- SLSA provenance reference;
- clean install smoke output for `cavra 1.0.0rc1`.

## Verification Summary

- Release notes draft: pass.
- Publication readiness verification: pass.
- Evidence validator: `scripts/validate-community-v100-rc-publication.py`.
- README release link freshness: pass.
- Wiki release link freshness: pass.
- Release index dry-run row: pass.
- Release readiness dashboard dry-run row: pass.
- Signed artifact verification: pending real artifacts.
- Provenance evidence: pending real artifacts.
- Clean install smoke: pending real artifacts.
- Public boundary validation: required before final publication.

## Boundary Notice

This dry-run RC1 release note covers public Community Edition release
documentation only. Enterprise source code, paid policy packs, SaaS backend
implementation, license-service internals, private signing keys, private
registry credentials, and customer records are not part of this public release
candidate record.

## Next Recommendation

Publish Community v1.0.0 release-candidate artifacts from the completed Node 24 readiness baseline and record signed artifact checksums, provenance, GitHub Release links, and post-publication verification evidence.
