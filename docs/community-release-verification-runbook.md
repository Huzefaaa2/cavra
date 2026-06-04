# Community Release Verification Runbook

Use this runbook after publishing any public CAVRA Community release.

## When To Run

Run verification after the release workflow publishes artifacts and before
announcing the release as ready for adoption.

## Manual Workflow

1. Open GitHub Actions.
2. Run `Verify Community Release`.
3. Enter the Community release tag, version, wheel SHA-256, and source
   distribution SHA-256 from the release publication record.
4. Confirm the workflow completes successfully.
5. Record the result in a release verification packet under
   `docs/release-verifications/`.
6. Update README, wiki, roadmap status, release notes, and changelog links.

## Local Command

```bash
python scripts/verify-community-release-artifacts.py \
  --tag community-v0.1.0 \
  --version 0.1.0 \
  --wheel-sha256 1a586ce0fe91af6c24c14b0f8b833d722f9de9e24cfcb1fd81dafc0f016306d8 \
  --sdist-sha256 35370dea724612c8619100db812635c048b91ede65fd905e8d8c189b7c07c26e
```

## Required Evidence

- release page URL;
- release workflow URL;
- wheel and source distribution names;
- expected and actual SHA-256 checksums;
- clean virtual environment install result;
- `cavra version` output;
- README and wiki release-link freshness;
- public boundary statement confirming Community-only artifacts.

## Failure Handling

If a checksum, download, or install smoke check fails, do not announce the
release. Open a release blocker, remove or replace the affected artifact, rerun
the release workflow, and publish a corrected verification packet after all
checks pass.

## Boundary Rules

Do not use this public workflow to download, validate, or disclose Enterprise
packages, paid policy packs, SaaS backend artifacts, license-service internals,
customer records, private keys, or private deployment evidence.
