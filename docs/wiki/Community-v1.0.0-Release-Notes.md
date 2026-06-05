# CAVRA Community v1.0.0 Release Notes

CAVRA Community v1.0.0 is prepared as the final GA publication package after
the published Community v1.0.0 RC1 baseline. The package metadata is now bumped
to final `1.0.0`; final artifacts are not published yet, so this remains the
dry-run GA release record.

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
  clean install smoke, and post-publication verification as required
  publication blockers until final artifacts exist.

## Artifact Verification

Final GA artifacts are not published yet. The final publication record must
replace this dry-run section with artifact checksums, provenance evidence,
signature or keyless attestation evidence, and clean install smoke output for
`cavra 1.0.0`.

## Boundary Notice

This dry-run GA release note covers public Community Edition release
documentation only. Enterprise source code, paid policy packs, SaaS backend
implementation, license-service internals, private signing keys, private
registry credentials, and customer records are not part of this public release
record.

## Next Recommendation

Merge the Community v1.0.0 metadata bump, create the community-v1.0.0 tag from main, build and upload final GitHub Release assets, then record final checksums, provenance, verifier defaults, and post-publication verification.
