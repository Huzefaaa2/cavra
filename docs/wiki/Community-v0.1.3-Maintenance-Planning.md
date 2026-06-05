# Community v0.1.3 Maintenance Planning

This planning note defines the public-safe scope for the Community v0.1.3
maintenance release. The release is intended to keep the public Community
delivery path healthy before the v1.0.0 launch track.

## Scope

Community v0.1.3 is a maintenance release candidate focused on GitHub Actions
Node 24 readiness and release-verification freshness. It does not add
Enterprise source code, private SaaS logic, paid policy packs, license signing
keys, customer records, or private trial package internals.

The GitHub Actions Node 24 readiness scope covers Community CI, security scan,
release build, and release verification workflows.

## Public Boundary

This planning artifact is public Community release evidence only. Enterprise
source code, commercial policy pack implementation, private SaaS backend code,
license-service internals, private registry details, customer records, provider
credentials, and signing keys must remain outside the public repository.

## Node 24 Readiness Matrix

| Workflow | Readiness Control | Status |
| --- | --- | --- |
| `.github/workflows/community-ci.yml` | Uses `actions/checkout@v6`, `actions/setup-python@v6`, and sets `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`. | Ready |
| `.github/workflows/security-scan.yml` | Uses `actions/checkout@v6`, `actions/setup-python@v6`, and sets `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`. | Ready |
| `.github/workflows/release-community.yml` | Uses `actions/checkout@v6`, `actions/setup-python@v6`, and sets `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`. | Ready |
| `.github/workflows/verify-community-release.yml` | Uses `actions/checkout@v6`, `actions/setup-python@v6`, sets `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`, and defaults to the current v0.1.3 release artifacts. | Ready |

## Release Candidate Checklist

- Keep `community-ci`, `security-scan`, `release-community`, and
  `verify-community-release` on Node 24-ready JavaScript action versions.
- Verify the manual Community release workflow defaults point at the current
  published Community release.
- Run release-note freshness, release-index freshness, readiness dashboard,
  portal, console, production deployment, Go hardening, Enterprise integration,
  procurement closeout, boundary, Python, and Go test gates.
- Publish Community v0.1.3 only after all local and GitHub checks are green.
- Sync README and wiki release records after publication.

## User Stories

- As a maintainer, I can run Community release workflows without deprecated
  JavaScript action runtime warnings.
- As a release manager, I can verify the current published release from a
  workflow dispatch screen with correct default artifact checksums.
- As a buyer or auditor, I can see that the public release path remains
  actively maintained before the v1.0.0 launch.

## Enterprise Challenge Solved

Enterprises expect governance products to keep their own CI/CD controls current.
This maintenance plan reduces release-chain drift and keeps CAVRA's public
Community release path credible for pilots, procurement review, and v1.0.0
launch preparation.

## Next Recommendation

Start Community v1.0.0 stabilization planning from the completed Node 24 readiness baseline with release signing, reproducible provenance, GA announcement readiness, and final operator evidence.
