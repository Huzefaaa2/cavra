# Community Release Index Freshness

CAVRA validates the public Community release index so users and maintainers can
trust that each indexed Community release points to matching release notes,
verification evidence, README links, wiki navigation, and a valid publication
state.

## Validation Command

```bash
python3 scripts/validate-community-release-index.py
```

The validator checks:

- `docs/community-release-index.md` exists and has at least one Community
  release row.
- Every indexed release uses a supported state: `Published` or `Dry run`.
- Every indexed GitHub Release URL points at the public
  `community-v*` release namespace.
- Every indexed release notes path and verification packet path exists.
- README links the release index, release notes, and verification packet.
- Wiki navigation links the release index, release notes page, and verification
  page.
- Release notes link back to the GitHub Release URL and verification packet.
- Dry-run records are explicitly marked as dry-run evidence.

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
