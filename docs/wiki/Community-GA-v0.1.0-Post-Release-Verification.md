# Community GA v0.1.0 Post-Release Verification

This packet records public post-release verification for the published CAVRA
Community GA v0.1.0 GitHub Release.

## Release

- Release: CAVRA Community GA v0.1.0
- Tag: `community-v0.1.0`
- Release URL:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0>
- Publication record: `docs/community-ga-v0.1.0-release-publication.md`
- Verification date: 2026-06-04

## Verification Results

| Check | Result | Evidence |
| --- | --- | --- |
| Release page reachable | Pass | GitHub Release metadata returned tag `community-v0.1.0`. |
| Wheel downloadable | Pass | `cavra-0.1.0-py3-none-any.whl` downloaded from the release page. |
| Source distribution downloadable | Pass | `cavra-0.1.0.tar.gz` downloaded from the release page. |
| Wheel checksum | Pass | `1a586ce0fe91af6c24c14b0f8b833d722f9de9e24cfcb1fd81dafc0f016306d8` |
| Source distribution checksum | Pass | `35370dea724612c8619100db812635c048b91ede65fd905e8d8c189b7c07c26e` |
| Clean install smoke | Pass | Installed the wheel into a temporary virtual environment and ran `cavra version`. |
| CLI version output | Pass | `cavra 0.1.0` |
| README release link freshness | Pass | README links the public release and publication record. |
| Wiki release link freshness | Pass | Wiki home links the release packet, publication record, and this verification page. |

## Reusable Verification

```bash
python scripts/verify-community-release-artifacts.py
```

## Decision

Decision: post-release verification passed.

The public Community GA v0.1.0 artifacts are downloadable, match the published
SHA-256 checksums, install successfully in a clean environment, and expose the
expected CLI version.

## Next Recommendation

Use the manual `Verify Community Release` GitHub Actions workflow for every
future Community release tag and publish its result in the release notes before
moving to the next public Community maintenance release.
