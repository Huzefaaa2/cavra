# Changelog

## Unreleased

- Added CLI and API validation for AISPM CI gate readiness packets so teams
  can verify required check names and installed CI templates before marking a
  replay-to-policy gate production-ready.

- Added a public-safe AISPM CI gate readiness export with copy/download
  actions for GitHub Actions, GitLab CI, and Azure Pipelines branch-protection
  setup.

- Added a compact Replay-to-Policy CI Gate panel in the AISPM dashboard with
  GitHub Actions, GitLab CI, and Azure Pipelines setup paths and required
  check names.

- Added GitLab CI and Azure Pipelines AISPM review packet validation templates
  so replay-to-policy packet gates can be enforced outside GitHub.

- Added a reusable GitHub Actions AISPM review packet validation template that
  runs `cavra aispm validate-review-packet`, uploads validation reports, and
  fails closed when replay-derived policy or fixture changes lack a packet.

- Added CLI and API validation for AISPM replay-to-policy review packets so
  exported PR and auditor attachments can be checked against the packaged
  schema and semantic consistency rules before use.

- Added a packaged AISPM replay-to-policy review packet schema and
  deterministic Community sample for PR and auditor attachment validation.

- Added compact AISPM replay-to-policy PR attachment guidance with exact
  review packet, policy draft, test fixture attachment paths, and copyable
  reviewer approval language.

- Added AISPM replay-to-policy review packet export actions that combine the
  candidate policy draft, test fixture, and review checklist into one
  public-safe JSON packet for PR attachment or auditor review.

- Added an AISPM replay-to-policy review workflow panel that summarizes
  candidate-control, fixture, evidence, validation-command, approval-gate, and
  Enterprise-boundary readiness before generated outputs are used in CI.

- Added copy and download actions for AISPM replay-to-policy test fixture
  previews in the public GitHub Pages dashboard so reviewers can export
  review-only JSON fixtures without browser developer tools.

- Added public-safe AISPM replay-to-policy test fixture exports for Community,
  including `/aispm/replay-to-policy-tests`, packaged schema/sample data,
  dashboard fixture JSON previews, docs/wiki updates, and Enterprise-locked
  prompt/reasoning/tool-payload test generation, tenant-history simulation,
  private ticket/asset enrichment, CI write-back, and organization-wide
  regression campaign boundaries.
- Added public-safe AISPM replay-to-policy draft authoring for Community,
  including `/aispm/replay-to-policy-draft`, packaged schema/sample data,
  dashboard candidate-control cards, read-only policy-pack previews,
  docs/wiki updates, and Enterprise-locked prompt, reasoning, tool-payload,
  ticket, asset, approval-policy, simulation, and write-back automation
  boundaries.
- Added deterministic public-safe AISPM executive risk narratives for Community,
  including `/aispm/executive-risk-narrative`, packaged schema/sample data,
  dashboard CSO/CISO narrative cards, docs/wiki updates, and Enterprise-locked
  AI-assisted board summaries, private trend history, tenant benchmarking,
  business criticality, customer-impact, scheduled brief, and GRC/incident
  export boundaries.
- Added public-safe AISPM evidence freshness and retention SLO reporting for
  Community, including `/aispm/evidence-freshness`, packaged schema/sample
  data, dashboard stale-evidence and retention-gap rows, docs/wiki updates, and
  Enterprise-locked immutable archive, object-lock, KMS, lifecycle, external
  archive, and auditor export boundaries.
- Added public-safe AISPM evidence confidence drilldown for Community,
  including `/aispm/evidence-confidence`, packaged schema/sample data,
  dashboard confidence rows for signed/activity/sample/metadata-only evidence,
  docs/wiki updates, and Enterprise-locked immutable evidence store,
  signature trust-chain, external ticket, customer-data, and tenant evidence
  boundaries.
- Added public-safe AISPM control coverage heatmap for Community, including
  `/aispm/control-coverage-heatmap`, packaged schema/sample data, dashboard
  matrix cards by agent/repository/control surface, docs/wiki updates, and
  Enterprise-locked repository owner graph, identity claims, permission matrix,
  environment criticality, CMDB mapping, and live organization baseline
  boundaries.
- Added public-safe AISPM agent blast-radius mapping for Community, including
  `/aispm/agent-blast-radius`, packaged schema/sample data, dashboard summary
  cards, per-agent repository/target/tool/policy reach cards, ActivityStore
  session metadata rollups, docs/wiki updates, and Enterprise-locked private
  asset graph, identity permission graph, cloud account inventory, dependency
  graph, secret name, and customer topology boundaries.
- Added public-safe AISPM tool-chain risk graphing for Community, including
  `/aispm/tool-chain-graph`, packaged schema/sample data, dashboard graph
  summary cards, hotspot and edge views, ActivityStore preservation for safe
  tool metadata, docs/wiki updates, and Enterprise-locked raw tool payload,
  tool result, connector span, cross-system call graph, and private network
  target boundaries.
- Added public-safe AISPM intent-to-action drift detection for Community,
  including `/aispm/intent-action-drift`, packaged schema/sample data,
  dashboard summary cards, drift score rows, ActivityStore preservation for
  declared intent/context metadata, docs/wiki updates, and Enterprise-locked
  raw prompt, reasoning, ticket, full tool payload, and semantic intent
  boundaries.
- Added public-safe AISPM pre-action risk forecasts for Community, including
  `/aispm/pre-action-risk-forecasts`, packaged schema/sample data, dashboard
  summary cards, projected blast-radius cards, docs/wiki updates, and
  Enterprise-locked private asset, dependency, identity, runtime, and
  prompt-intent enrichment.
- Added public-safe AISPM policy context gap detection for Community, including
  `/aispm/policy-context-gaps`, packaged schema/sample data, dashboard summary
  cards, docs/wiki updates, and Enterprise-locked private CMDB, data catalog,
  identity, cloud inventory, ticketing, and change-calendar enrichment.
- Added public-safe AISPM behavior fingerprinting for Community, including
  `/aispm/behavior-fingerprints`, packaged schema/sample data, dashboard
  summary cards, risk-signal chips, docs/wiki updates, and Enterprise-locked
  private behavior baseline boundaries.
- Added public-safe AISPM approval lineage for Community, including the
  `/aispm/approval-lineage` API endpoint, packaged schema/sample, dashboard
  panel, docs/wiki updates, and role-labelled actor redaction for local
  approval records.
- Added a public-safe AISPM trace replay drill-down to the GitHub Pages
  dashboard, including a session selector, replay summary cards, normalized
  decision steps, redaction boundary status, API-backed
  `/aispm/trace-replay/{session_id}` loading, and static sample fallback.
- Added the Community release keyless attestation workflow and runbook for
  `community-v1.0.0` release assets. The workflow downloads published GitHub
  Release assets, validates final SHA-256 checksums, generates a GitHub
  Actions OIDC/Sigstore attestation with `actions/attest@v4`, verifies assets
  with `gh attestation verify`, and uploads verifier evidence.
- Verified Community v1.0.0 keyless attestation in workflow run `27003626701`
  and recorded attestation `29988580` for all four public release assets.
- Published Community v1.0.0 as the stable public Community baseline and
  recorded Community v1.0.0 post-publication verification at
  `docs/release-verifications/community-v1.0.0-post-publication-verification.md`
  for final artifact SHA-256 checksums, checksum manifest, provenance metadata,
  clean install smoke, Community Docker build evidence, verifier workflow
  defaults, release index state, readiness dashboard state, README links, wiki
  navigation, and public boundary validation.
  Next recommendation: Use Community v1.0.0 as the stable public baseline and begin the v1.0.1 maintenance planning path for post-GA fixes, release integrity hardening, detached signing or keyless attestation, and adoption feedback.
- Bumped the Community package metadata, runtime version, and release verifier
  tag/version defaults to final `1.0.0`, while keeping final checksum defaults
  as explicit placeholders until the `community-v1.0.0` GitHub Release assets
  are uploaded from merged `main`. The GA publication package now records the
  metadata bump and pre-publication clean wheel install smoke for `cavra 1.0.0`.
  Next recommendation: Merge the Community v1.0.0 metadata bump, create the community-v1.0.0 tag from main, build and upload final GitHub Release assets, then record final checksums, provenance, verifier defaults, and post-publication verification.
- Added Community v1.0.0 GA publication package preparation with draft final
  release notes, publication readiness verification, artifact build plan,
  verifier inputs, announcement approval evidence, release index/dashboard
  dry-run rows, README/wiki links, and the validator at
  `scripts/validate-community-v100-ga-publication-package.py`. The publication
  package is stored at `docs/community-v1.0.0-ga-publication-package.md` with
  structured evidence at
  `docs/release-verifications/community-v1.0.0-ga-publication-package.json`.
  Next recommendation: Merge the Community v1.0.0 metadata bump, create the community-v1.0.0 tag from main, build and upload final GitHub Release assets, then record final checksums, provenance, verifier defaults, and post-publication verification.
- Added Community v1.0.0 GA readiness evidence with upgrade notes, installer
  paths, draft announcement copy, final GA evidence gates, README/wiki links,
  roadmap coverage, and the validator at
  `scripts/validate-community-v100-ga-readiness.py`. The readiness packet is
  stored at `docs/community-v1.0.0-ga-readiness.md` with structured evidence at
  `docs/release-verifications/community-v1.0.0-ga-readiness.json`.
  Next recommendation: Merge the Community v1.0.0 metadata bump, create the community-v1.0.0 tag from main, build and upload final GitHub Release assets, then record final checksums, provenance, verifier defaults, and post-publication verification.
- Added Community v1.0.0 RC1 post-publication verification for the published
  `community-v1.0.0-rc.1` GitHub Release, including artifact SHA-256
  checksums, provenance metadata, workflow evidence, clean install smoke,
  README links, release index status, release dashboard status, wiki navigation,
  the verification packet at
  `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md`,
  and the validator at `scripts/validate-community-v100-rc-post-publication.py`.
  Next recommendation: Merge the Community v1.0.0 metadata bump, create the community-v1.0.0 tag from main, build and upload final GitHub Release assets, then record final checksums, provenance, verifier defaults, and post-publication verification.
- Bumped the Community package metadata and runtime version to `1.0.0rc1`
  for the `community-v1.0.0-rc.1` release-candidate artifact publication.
- Added Community v1.0.0 RC1 publication preparation with dry-run release
  notes, publication readiness verification, a publication packet, release
  index and dashboard coverage, README/wiki navigation, and CI validation
  through `docs/community-v1.0.0-release-candidate-publication.md`.
  Next recommendation: Publish Community v1.0.0 release-candidate artifacts from the completed Node 24 readiness baseline and record signed artifact checksums, provenance, GitHub Release links, and post-publication verification evidence.
- Added Community v1.0.0 release-candidate hardening with public-safe signed
  artifact, provenance, announcement checklist, final operator evidence,
  boundary validation, CI validation, README/wiki navigation, and roadmap
  handoff through `docs/community-v1.0.0-release-candidate-hardening.md`.
  Next recommendation: Prepare Community v1.0.0 release-candidate publication from the completed Node 24 readiness baseline with signed artifact verification, provenance evidence, release notes, and announcement readiness.
- Added Community v1.0.0 stabilization planning, a public-safe stabilization
  packet, CI validation, README/wiki navigation, and roadmap handoff for
  release signing, reproducible provenance, GA announcement readiness, final
  operator evidence, and open-core boundary validation through
  `docs/community-v1.0.0-stabilization-plan.md`.
  Next recommendation: Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
- Added Community v0.1.3 maintenance planning and upgraded public Community
  release workflows to Node 24-ready action versions.
- Bumped the Community package metadata and runtime version to `0.1.3`, and
  prepared v0.1.3 release notes plus maintenance verification evidence for
  publication from merged `main`.
- Published Community v0.1.3 GitHub Release artifacts, recorded wheel and
  source distribution SHA-256 checksums, verified clean install smoke, updated
  release verifier defaults, and added post-release verification evidence.
- Bumped the Community package metadata and runtime version to `0.1.2` so
  the `community-v0.1.2` release artifacts can be built and published from
  main before final checksum and install-smoke evidence is recorded.
- Published Community v0.1.2 GitHub Release artifacts, recorded wheel and
  source distribution SHA-256 checksums, verified clean install smoke, and
  added post-release verification evidence.
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
