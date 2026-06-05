# Community v0.1.1 Post-Release Verification

This packet records public post-release verification for the published CAVRA
Community v0.1.1 GitHub Release.

## Release

- Release: CAVRA Community v0.1.1
- Tag: `community-v0.1.1`
- Release URL:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1>
- Maintenance verification:
  `docs/release-verifications/community-v0.1.1-maintenance-verification.md`
- Verification date: 2026-06-04

## Verification Results

| Check | Result | Evidence |
| --- | --- | --- |
| Release page reachable | Pass | GitHub Release metadata returned tag `community-v0.1.1`. |
| Wheel downloadable | Pass | `cavra-0.1.1-py3-none-any.whl` downloaded from the release page. |
| Source distribution downloadable | Pass | `cavra-0.1.1.tar.gz` downloaded from the release page. |
| Wheel checksum | Pass | `32ab7a220eb5f25ea5ab42ccbc62a43b7260de12b9a0d3f3d7bdafa1501a5d6a` |
| Source distribution checksum | Pass | `b123c6d2aadd72b055ba916caa68953af94122d34f1215756804d74e91174950` |
| Clean install smoke | Pass | Installed the wheel into a temporary virtual environment and ran `cavra version`. |
| CLI version output | Pass | `cavra 0.1.1` |
| README release link freshness | Pass | README links the public release, release notes, maintenance verification, and this post-release verification page. |
| Wiki release link freshness | Pass | Wiki home links the release notes, maintenance verification, and this post-release verification page. |

## Commands

Reusable public verification used the following command:

```bash
python scripts/verify-community-release-artifacts.py \
  --output-dir /tmp/cavra-community-v011-release-verify
```

Equivalent explicit verification:

```bash
python scripts/verify-community-release-artifacts.py \
  --tag community-v0.1.1 \
  --version 0.1.1 \
  --wheel-sha256 32ab7a220eb5f25ea5ab42ccbc62a43b7260de12b9a0d3f3d7bdafa1501a5d6a \
  --sdist-sha256 b123c6d2aadd72b055ba916caa68953af94122d34f1215756804d74e91174950
```

## Boundary Notice

This verification covers the public Community Edition release artifacts only.
It does not validate Enterprise packages, paid policy packs, license-service
internals, SaaS backend implementation, private keys, customer records, or
private deployment evidence.

## Decision

Decision: post-release verification passed.

The public Community v0.1.1 artifacts are downloadable, match the published
SHA-256 checksums, install successfully in a clean environment, and expose the
expected CLI version.

## Next Recommendation

Publish Community v0.1.3 GitHub Release from merged main after Node 24 readiness and replace pending artifact evidence with post-release verification.
