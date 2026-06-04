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
  --tag community-v0.1.1 \
  --version 0.1.1 \
  --wheel-sha256 32ab7a220eb5f25ea5ab42ccbc62a43b7260de12b9a0d3f3d7bdafa1501a5d6a \
  --sdist-sha256 b123c6d2aadd72b055ba916caa68953af94122d34f1215756804d74e91174950
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
