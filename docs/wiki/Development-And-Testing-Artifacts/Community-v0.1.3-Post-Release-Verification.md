# Community v0.1.3 Post-Release Verification

This packet records public post-release verification for the published CAVRA
Community v0.1.3 GitHub Release.

## Release

- Release: CAVRA Community v0.1.3
- Tag: `community-v0.1.3`
- Release target: `5173db90af69410d27b5cd6ef4274c35e26d6a08`
- Release URL:
  <https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.3>
- Maintenance verification:
  `docs/release-verifications/community-v0.1.3-maintenance-verification.md`
- Verification date: 2026-06-05

## Verification Results

| Check | Result | Evidence |
| --- | --- | --- |
| Release page reachable | Pass | GitHub Release metadata returned tag `community-v0.1.3`. |
| Wheel downloadable | Pass | `cavra-0.1.3-py3-none-any.whl` downloaded from the release page. |
| Source distribution downloadable | Pass | `cavra-0.1.3.tar.gz` downloaded from the release page. |
| Wheel checksum | Pass | `843cf0c13914e4e9d95ebacd8f0a74aaf4c66969e213e8337d1c0d1c8843cb2e` |
| Source distribution checksum | Pass | `83ddaeb4a36502bfa8a5441a15b7b089ac6d5c1dcc58692e942e3ad601d3c29f` |
| Clean install smoke | Pass | Installed the wheel into a temporary virtual environment and ran `cavra version`. |
| CLI version output | Pass | `cavra 0.1.3` |
| README release link freshness | Pass | README links the public release, release notes, maintenance verification, and this post-release verification page. |
| Wiki release link freshness | Pass | Wiki home links the release notes, maintenance verification, and this post-release verification page. |

## Commands

Reusable public verification used the following command:

```bash
python3 scripts/verify-community-release-artifacts.py \
  --tag community-v0.1.3 \
  --version 0.1.3 \
  --wheel-sha256 843cf0c13914e4e9d95ebacd8f0a74aaf4c66969e213e8337d1c0d1c8843cb2e \
  --sdist-sha256 83ddaeb4a36502bfa8a5441a15b7b089ac6d5c1dcc58692e942e3ad601d3c29f
```

## Boundary Notice

This verification covers the public Community Edition release artifacts only.
It does not validate Enterprise source code, Enterprise packages, paid policy
packs, license-service internals, SaaS backend implementation, private keys,
customer records, or private deployment evidence.

## Decision

Decision: post-release verification passed.

The public Community v0.1.3 artifacts are downloadable, match the published
SHA-256 checksums, install successfully in a clean environment, and expose the
expected CLI version.

## Next Recommendation

Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
