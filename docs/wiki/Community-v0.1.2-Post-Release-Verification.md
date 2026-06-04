# Community v0.1.2 Post-Release Verification

This packet records public post-release verification for the published CAVRA
Community v0.1.2 GitHub Release.

## Release

- Release: CAVRA Community v0.1.2
- Tag: `community-v0.1.2`
- Release target: `e3cd7a1d6a3435188b4225d3bf49d79a9f6de128`
- Release URL:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.2>
- Maintenance verification:
  `docs/release-verifications/community-v0.1.2-maintenance-verification.md`
- Verification date: 2026-06-04

## Verification Results

| Check | Result | Evidence |
| --- | --- | --- |
| Release page reachable | Pass | GitHub Release metadata returned tag `community-v0.1.2`. |
| Wheel downloadable | Pass | `cavra-0.1.2-py3-none-any.whl` downloaded from the release page. |
| Source distribution downloadable | Pass | `cavra-0.1.2.tar.gz` downloaded from the release page. |
| Wheel checksum | Pass | `bbdb2f593ce3c14742446c1682c23bef7933925a02382a874e59b8ef7e389163` |
| Source distribution checksum | Pass | `f7a477cfef65d77bd4c36520a83d256c1086e7b81ffcd9411ee9c68d017ab1d0` |
| Clean install smoke | Pass | Installed the wheel into a temporary virtual environment and ran `cavra version`. |
| CLI version output | Pass | `cavra 0.1.2` |
| README release link freshness | Pass | README links the public release, release notes, maintenance verification, and this post-release verification page. |
| Wiki release link freshness | Pass | Wiki home links the release notes, maintenance verification, and this post-release verification page. |

## Commands

Reusable public verification used the following command:

```bash
python scripts/verify-community-release-artifacts.py \
  --tag community-v0.1.2 \
  --version 0.1.2 \
  --wheel-sha256 bbdb2f593ce3c14742446c1682c23bef7933925a02382a874e59b8ef7e389163 \
  --sdist-sha256 f7a477cfef65d77bd4c36520a83d256c1086e7b81ffcd9411ee9c68d017ab1d0
```

## Boundary Notice

This verification covers the public Community Edition release artifacts only.
It does not validate Enterprise source code, Enterprise packages, paid policy
packs, license-service internals, SaaS backend implementation, private keys,
customer records, or private deployment evidence.

## Decision

Decision: post-release verification passed.

The public Community v0.1.2 artifacts are downloadable, match the published
SHA-256 checksums, install successfully in a clean environment, and expose the
expected CLI version.

## Next Recommendation

Prepare Community v0.1.3 maintenance planning and GitHub Actions Node 24
readiness.
