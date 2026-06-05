# Community Release Readiness Dashboard Validation

CAVRA validates the public Community release readiness dashboard so release
state, evidence links, verification commands, README navigation, wiki
navigation, and publication state cannot drift from the release index.

## Validation Command

```bash
python3 scripts/validate-community-release-readiness-dashboard.py
```

The validator checks:

- `docs/community-release-readiness-dashboard.md` exists.
- `docs/wiki/Community-Release-Readiness-Dashboard.md` exists.
- README links the dashboard.
- Wiki navigation links the dashboard.
- Every release in `docs/community-release-index.md` appears in the dashboard.
- Dashboard release state, GitHub Release URL, release evidence, verification
  packet, and next action match the release index.
- Dashboard readiness values use supported states.
- Required control evidence appears in the dashboard.
- Required verification commands appear in the dashboard.
- Required CI workflows appear in the dashboard.
- Public boundary language covers Enterprise source, paid policy packs, SaaS
  backend implementation, private keys, and customer records.

## CI Enforcement

The validator runs in:

- `.github/workflows/community-ci.yml`
- `.github/workflows/security-scan.yml`
- `.github/workflows/release-community.yml`
- `.github/workflows/cavra-governance.yml`

## Boundary Notice

This control validates public Community release documentation only. It does not
load Enterprise packages, inspect private release registries, contact license
services, or expose private artifact locations.

## Next Recommendation

Publish Community v0.1.3 maintenance release after GitHub Actions Node 24 readiness and workflow verification are complete.
