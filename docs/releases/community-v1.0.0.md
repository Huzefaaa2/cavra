# CAVRA Community v1.0.0 Release Notes

CAVRA Community v1.0.0 is prepared as the final GA publication package after
the published Community v1.0.0 RC1 baseline. The package metadata is now bumped
to final `1.0.0`; the final `community-v1.0.0` artifacts are not published yet.
This release note remains a dry-run GA record until the merged `main` branch is
tagged and the GitHub Release assets are uploaded.

## Release Links

- Planned GitHub Release:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0>
- GA publication package:
  `docs/community-v1.0.0-ga-publication-package.md`
- Publication readiness verification:
  `docs/release-verifications/community-v1.0.0-publication-readiness.md`
- Publication package packet:
  `docs/release-verifications/community-v1.0.0-ga-publication-package.json`
- GA readiness:
  `docs/community-v1.0.0-ga-readiness.md`
- RC1 post-publication verification:
  `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md`
- Release index:
  `docs/community-release-index.md`
- Release readiness dashboard:
  `docs/community-release-readiness-dashboard.md`

## What Changed

- Prepared the final public Community v1.0.0 GA publication package from
  validated RC1 feedback and the completed Node 24 readiness baseline.
- Drafted final release notes and announcement copy for maintainer approval.
- Defined the artifact build plan for the wheel, source distribution, checksum
  manifest, provenance metadata, and Community Docker image path.
- Defined verifier inputs for the reusable Community release verifier.
- Bumped the public package metadata and runtime version from `1.0.0rc1` to
  final `1.0.0`.
- Verified a pre-publication local wheel build and clean virtualenv install
  smoke with `cavra version` returning `cavra 1.0.0`.
- Kept final SHA-256 checksums, signature or keyless attestation evidence,
  final tagged-artifact clean install smoke, and post-publication verification
  as required publication blockers until final artifacts exist.
- Confirmed the package remains public Community documentation only and does
  not include Enterprise source code or private release material.

## Upgrade Notes

- From Community v0.1.3: install the final `1.0.0` wheel or source
  distribution after publication, then run `cavra version` and verify
  `cavra 1.0.0`.
- From Community v1.0.0 RC1: replace the release-candidate package with the
  final `1.0.0` package, rerun policy validation, and verify evidence bundle
  generation.
- Enterprise features remain outside the public Community artifact and require
  private packages or commercial access.

## Artifact Verification

Final GA artifacts are not published yet. The final publication record must
replace this dry-run section with:

- `cavra-1.0.0-py3-none-any.whl` SHA-256 checksum;
- `cavra-1.0.0.tar.gz` SHA-256 checksum;
- checksum manifest;
- provenance metadata;
- detached signature or keyless attestation evidence;
- clean install smoke output for `cavra 1.0.0`.

Pre-publication local build smoke for this metadata-bump branch returned
`cavra 1.0.0`. Final checksums are intentionally not recorded here until the
`community-v1.0.0` tag exists on `main`.

## Verification Summary

- GA publication package: pass.
- Publication readiness verification: pass.
- Evidence validator:
  `scripts/validate-community-v100-ga-publication-package.py`.
- README release link freshness: pass.
- Wiki release link freshness: pass.
- Release index dry-run row: pass.
- Release readiness dashboard dry-run row: pass.
- Package metadata bump: pass.
- Pre-publication local wheel install smoke: pass.
- Artifact checksums: pending final artifacts.
- Provenance evidence: pending final artifacts.
- Signature or keyless attestation evidence: pending final artifacts.
- Clean install smoke: pending final artifacts.
- Public boundary validation: required before final publication.

## Boundary Notice

This dry-run GA release note covers public Community Edition release
documentation only. Enterprise source code, paid policy packs, SaaS backend
implementation, license-service internals, private signing keys, private
registry credentials, and customer records are not part of this public release
record.

## Next Recommendation

Merge the Community v1.0.0 metadata bump, create the community-v1.0.0 tag from main, build and upload final GitHub Release assets, then record final checksums, provenance, verifier defaults, and post-publication verification.
