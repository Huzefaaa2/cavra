# Community Release Readiness Dashboard Validation

CAVRA validates the public Community release readiness dashboard so release
state, evidence links, verification commands, README navigation, wiki
navigation, and publication state cannot drift from the release index.

## Validation Command

```bash
python3 scripts/validate-community-release-readiness-dashboard.py
```

The validator checks dashboard presence, README/wiki navigation, release-index
row parity, supported release and readiness states, required freshness controls,
verification commands, CI workflow references, and public boundary language.

## CI Enforcement

The validator runs in Community CI, security scan, release-community, and the
`cavra-required-check` governance workflow.

## Boundary Notice

This control validates public Community release documentation only. It does not
load Enterprise packages, inspect private release registries, contact license
services, or expose private artifact locations.

## Next Recommendation

Start Community v1.0.0 stabilization planning from the completed Node 24 readiness baseline with release signing, reproducible provenance, GA announcement readiness, and final operator evidence.
