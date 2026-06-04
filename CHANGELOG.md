# Changelog

## Unreleased

- Bumped the Community package metadata and runtime version to `0.1.2` so
  the `community-v0.1.2` release artifacts can be built and published from
  main before final checksum and install-smoke evidence is recorded.
- Added Community v0.1.2 dry-run release notes and maintenance verification
  evidence using package metadata and release workflow guard validation, while
  deferring official publication until real artifacts exist.
- Closed Community v0.1.2 package metadata warnings by making
  `pyproject.toml` the source of package metadata, adding package metadata
  validation to Community CI and release workflows, and documenting release
  workflow guard evidence.
- Added Community GA v0.1.0 post-release verification evidence, reusable
  artifact verifier, manual GitHub Actions verification workflow, verification
  runbook, and public release notes.
- Added the Community maintenance-release checklist, evidence template, JSON
  schema, validator, example packet, CI enforcement, and wiki-ready
  documentation for future public Community tags.
- Added Community release-note freshness validation to keep release notes,
  verification packets, README links, and wiki navigation in sync.
- Converted the Community v0.1.1 maintenance-release packet from dry-run
  evidence into official release notes, artifact checksums, install-smoke
  evidence, and publication-ready verification.
- Added the Community release index for public Community release states, notes,
  verification packets, and next actions.
- Added Community release index freshness validation to keep indexed Community
  release states, release notes, verification packets, README links, and wiki
  navigation in sync.
- Added the Community release readiness dashboard to roll up release state,
  freshness controls, verification commands, CI evidence, and maintainer next
  actions.
- Redesigned the GitHub Pages sandbox into a Backstage-style CAVRA developer
  portal with persistent navigation, command palette search, mobile navigation,
  interactive architecture, policy, evidence, integration, compliance,
  documentation, and roadmap pages.
- Added Community release readiness dashboard validation to keep dashboard
  rows, release links, freshness controls, verification commands, README
  navigation, wiki navigation, and publication state aligned with the release
  index.
- Added CAVRA developer portal smoke validation to keep public GitHub Pages
  routes, command palette content, mobile navigation, architecture nodes,
  compliance filters, workflow smoke strings, brand assets, README links, and
  wiki navigation aligned.
- Added the console closeout operator experience with persona-specific
  prospect, auditor, platform team, and CISO journeys plus CI-enforced
  validation.
- Added the user-verifiable Community GA path tying policy, evidence, console,
  Go runtime readiness, release verification, README, wiki navigation, and
  workflow validation into one public operator runbook.
- Added production deployment guide validation for install, configuration,
  storage, backup, restore, CORS/API, GitHub Pages portal checks, release
  validators, CI wiring, README navigation, and wiki navigation.
- Added Go enforcement production hardening validation for Unix-socket
  transport, gRPC boundary planning, air-gapped packaging, reproducibility,
  upgrade validation, performance smoke evidence, operational readiness, CI
  wiring, README navigation, and wiki navigation.
- Added Enterprise integration validation for GitHub App/orchestrator
  governance, GitLab and Azure DevOps parity, SAML identity readiness,
  SIEM/ITSM workflow evidence, CI wiring, README navigation, and wiki
  navigation.
- Added production readiness procurement closeout validation for performance,
  concurrency, backup/restore, upgrade/migration, SOC 2 readiness, security
  advisory drills, final release integrity evidence, CI wiring, README
  navigation, and wiki navigation.
- Archived Community v0.1.1 post-release verification evidence with published
  GitHub Release asset download checks, SHA-256 matches, clean install smoke,
  README/wiki freshness, release index, and readiness dashboard links.

## Community v0.1.1 - 2026-06-04

- Bumped the Community Python package metadata, CLI version output, and MCP
  server version advertisement to `0.1.1`.
- Built public Community wheel and source distribution artifacts for
  `community-v0.1.1`.
- Recorded SHA-256 checksums for `cavra-0.1.1.tar.gz` and
  `cavra-0.1.1-py3-none-any.whl`.
- Verified a clean wheel install smoke with `cavra version` returning
  `cavra 0.1.1`.
- Updated README, release index, readiness dashboard, release notes,
  verification packet, and wiki-ready pages for the official maintenance
  release.
- Archived post-release verification for the published `community-v0.1.1`
  GitHub Release assets.

## Community GA v0.1.0 - 2026-06-04

- Published CAVRA Community GA v0.1.0 as a public GitHub Release with source
  distribution and wheel artifacts.
- Recorded the official release packet, publication evidence, artifact
  checksums, post-release install smoke result, and Community-only boundary
  statement.

- Added open-core edition boundary plan for Community, Enterprise, Trial, and
  SaaS Control Plane packaging.
- Added public-safe edition, licensing, feature, and plugin extension
  interfaces.
- Added public boundary validation script for risky commercial/private terms.
