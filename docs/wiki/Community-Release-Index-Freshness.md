# Community Release Index Freshness

CAVRA validates the public Community release index so users and maintainers can
trust that each indexed Community release points to matching release notes,
verification evidence, README links, wiki navigation, and a valid publication
state.

## Validation Command

```bash
python3 scripts/validate-community-release-index.py
```

The validator checks release index rows, supported publication states, public
Community GitHub Release URLs, release notes paths, verification packet paths,
README links, wiki navigation, release-note backlinks, and explicit dry-run
marking for dry-run release records.

## CI Enforcement

The validator runs in Community CI, security scan, release-community, and the
`cavra-required-check` governance workflow.

## Boundary Notice

This control validates public Community release documentation only. It does not
load Enterprise packages, inspect private release registries, contact license
services, or expose private artifact locations.

## Next Recommendation

Complete enterprise integration validation for GitHub App/orchestrator production hardening, GitLab/Azure DevOps parity, SAML identity readiness, and SIEM/ITSM workflow evidence.
