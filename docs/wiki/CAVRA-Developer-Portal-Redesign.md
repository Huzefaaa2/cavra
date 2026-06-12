# CAVRA Developer Portal Redesign

The GitHub Pages sandbox has been redesigned from a single long-scroll page into
a Backstage-style developer portal experience for CAVRA: Continuous AI
Validation, Risk & Audit.

## Delivered Static Portal

The current public site remains static-hostable on GitHub Pages through
`apps/sandbox-ui` and `.github/workflows/deploy-sandbox.yml`.

Delivered UX:

- sticky top header with logo, search, docs, demo, GitHub, download, theme, and
  version controls;
- persistent left navigation with grouped portal sections;
- center content panels that switch without page reloads;
- sticky right table of contents on desktop;
- mobile drawer navigation and bottom navigation;
- professional dashboard themes: Sentinel, Classic, Retro, and Executive;
- command palette with `Ctrl+K` search;
- interactive architecture explorer with clickable nodes and an inspector
  panel;
- AI Posture, policy, evidence, integrations, compliance, use-case,
  documentation, and roadmap pages, including a public-safe trace replay
  drill-down for normalized decision steps, approval lineage for role-labelled
  approval records, and behavior fingerprinting for baseline-vs-unusual agent
  drift signals, policy context gaps for policy-invisible risk, and
  pre-action risk forecasts for projected blast radius, and intent-to-action
  drift for declared intent versus observed action, and tool-chain risk graphing
  for agent/tool/target/policy edge hotspots, and agent blast-radius mapping
  for repository/target/tool/policy reach, control coverage heatmap views
  by agent, repository, and control surface, evidence confidence drilldowns,
  evidence freshness SLO panels, AISPM Enterprise Trial readiness checklist
  with copy/download packet export, Enterprise Trial evaluator handoff,
  Enterprise Trial evaluation journey timeline, AISPM Trial Closeout Evidence
  panel, AISPM Trial Feedback Intake model, AISPM Trial Outcome Summary,
  AISPM Trial Review Packet export, AISPM Trial Review Packet Integrity panel,
  AISPM Trial Procurement Readiness panel,
  AISPM Trial Pilot Scope Builder,
  AISPM Trial Pilot Scope Packet export,
  AISPM Pilot Approval Checklist,
  AISPM Pilot Approval Packet export,
  AISPM Pilot Launch Readiness Summary,
  AISPM Pilot Launch Decision Packet export,
  Production Pilot Evidence Room,
  Production Pilot Evidence Room Packet export,
  Evidence Room Reviewer Checklist,
  Evidence Room Reviewer Checklist Packet export,
  Pilot Exception Register,
  Pilot Exception Register Packet export,
  Pilot Risk Acceptance Summary,
  Pilot Risk Acceptance Packet export,
  Pilot Launch Board Pack,
  Pilot Launch Board Pack Packet export,
  replay-to-policy draft/test fixture previews,
  review workflow readiness checks, review packet export actions, PR attachment
  guidance, replay-to-policy CI gate setup paths, readiness summary, rollout checklist export, audit packet export, and readiness export actions, and copy/download JSON export actions;
- Enterprise Trial reviewer links for the AISPM trial lab notebook publication
  readiness summary, readiness JSON, and GitHub Wiki lab notebook, with a
  stable page-local TOC anchor for release reviewers;
- command palette entries for the AISPM trial lab notebook readiness summary,
  readiness JSON, and GitHub Wiki lab notebook;
- Playwright visual smoke validation for desktop/mobile dashboard and AISPM
  board-pack/report-center surfaces through `npm run validate:sandbox:visual`
  and `scripts/validate-sandbox-visual.mjs`;
- AISPM visual freshness validation through
  `scripts/validate-aispm-visual-freshness.py` with the public-safe record at
  `docs/release-verifications/aispm-visual-smoke-validation.json`;
- AISPM launch readiness rollup through
  `docs/release-verifications/aispm-launch-readiness-rollup.md`,
  `docs/release-verifications/aispm-launch-readiness-rollup.json`, and
  `scripts/validate-aispm-launch-readiness.py`;
- hosted GitHub Pages browser smoke validation through
  `docs/release-verifications/hosted-sandbox-pages-smoke-validation.md`,
  `docs/release-verifications/hosted-sandbox-pages-smoke-validation.json`, and
  `scripts/validate-hosted-sandbox-pages.mjs`;
- hosted GitHub Pages deployment freshness through
  `docs/release-verifications/hosted-sandbox-deployment-freshness.md`,
  `docs/release-verifications/hosted-sandbox-deployment-freshness.json`,
  `scripts/validate-hosted-sandbox-deployment-freshness.py`, and
  `community-v1.0.0-aispm-release-evidence-index`;
- hosted release operator status through
  `docs/release-verifications/hosted-sandbox-operator-release-status.md`,
  `docs/release-verifications/hosted-sandbox-operator-release-status.json`,
  `scripts/validate-hosted-sandbox-operator-status.py`, and
  `cavra-hosted-sandbox-operator-status-packet.json`;
- hosted GitHub Pages post-deploy evidence through
  `docs/release-verifications/hosted-sandbox-post-deploy-evidence.md`,
  `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json`,
  `scripts/generate-hosted-sandbox-deploy-evidence.py`,
  `scripts/validate-hosted-sandbox-deploy-evidence.py`, and
  `cavra-hosted-sandbox-post-deploy-evidence`;
- AISPM Release Evidence Index through
  `docs/release-verifications/aispm-release-evidence-index.md`,
  `docs/release-verifications/aispm-release-evidence-index.json`,
  `scripts/validate-aispm-release-evidence-index.py`, and
  `cavra-aispm-release-evidence-index-packet.json`;
- AISPM report catalog readiness through
  `docs/release-verifications/aispm-report-catalog-readiness.md`,
  `docs/release-verifications/aispm-report-catalog-readiness.json`,
  `scripts/validate-aispm-report-catalog-readiness.py`, and
  `cavra-aispm-report-catalog-packet.json`;
- AISPM report delivery setup readiness through
  `docs/release-verifications/aispm-report-delivery-setup-readiness.md`,
  `docs/release-verifications/aispm-report-delivery-setup-readiness.json`,
  `scripts/validate-aispm-report-delivery-setup-readiness.py`, and
  `cavra-aispm-report-delivery-setup-packet.json`;
- AISPM report operations readiness through
  `docs/release-verifications/aispm-report-operations-readiness.md`,
  `docs/release-verifications/aispm-report-operations-readiness.json`,
  `scripts/validate-aispm-report-operations-readiness.py`, and
  `cavra-aispm-report-operations-readiness-packet.json`;
- AISPM report governance readiness through
  `docs/release-verifications/aispm-report-governance-readiness.md`,
  `docs/release-verifications/aispm-report-governance-readiness.json`,
  `scripts/validate-aispm-report-governance-readiness.py`, and
  `cavra-aispm-report-governance-readiness-packet.json`;
- AISPM report assurance readiness through
  `docs/release-verifications/aispm-report-assurance-readiness.md`,
  `docs/release-verifications/aispm-report-assurance-readiness.json`,
  `scripts/validate-aispm-report-assurance-readiness.py`, and
  `cavra-aispm-report-assurance-readiness-packet.json`;
- AISPM report response readiness through
  `docs/release-verifications/aispm-report-response-readiness.md`,
  `docs/release-verifications/aispm-report-response-readiness.json`,
  `scripts/validate-aispm-report-response-readiness.py`, and
  `cavra-aispm-report-response-readiness-packet.json`;
- AISPM report trial operations readiness through
  `docs/release-verifications/aispm-report-trial-operations-readiness.md`,
  `docs/release-verifications/aispm-report-trial-operations-readiness.json`,
  `scripts/validate-aispm-report-trial-operations-readiness.py`, and
  `cavra-aispm-report-trial-operations-readiness-packet.json`;
- AISPM pilot control readiness through
  `docs/release-verifications/aispm-pilot-control-readiness.md`,
  `docs/release-verifications/aispm-pilot-control-readiness.json`,
  `scripts/validate-aispm-pilot-control-readiness.py`, and
  `cavra-aispm-pilot-control-readiness-packet.json`;
- AISPM v1.0 public release readiness through
  `docs/release-verifications/aispm-v1.0-public-release-readiness.md`,
  `docs/release-verifications/aispm-v1.0-public-release-readiness.json`,
  `scripts/validate-aispm-v100-public-release.py`,
  `docs/releases/community-v1.0.0-aispm.md`, and
  `docs/aispm-v1.0-public-walkthrough.md`;
- CAVRA-branded enterprise security visual design with accessible focus states,
  reduced scrolling, and a fixed Classic light theme for high-contrast reading.

The `#ai-posture` route renders the public-safe AISPM contract with sample data
by default and reads `/aispm/posture` when `window.CAVRA_API_BASE` is
configured. It includes posture overview, agent coverage, risk findings,
control coverage, near-miss queue, policy context gaps, pre-action risk
forecasts, intent-to-action drift, evidence confidence drilldown, evidence
freshness SLO panel, replay-to-policy draft and copy/download test fixture
previews, review workflow readiness checks, review packet export actions, PR
attachment guidance, replay-to-policy CI gate setup paths, readiness summary, rollout checklist export, audit packet export, Pilot Launch Board Pack Packet export as `cavra-aispm-pilot-launch-board-pack-packet.json`, artifact freshness validation through `scripts/validate-aispm-launch-artifacts.py`, AISPM launch readiness rollup through `docs/release-verifications/aispm-launch-readiness-rollup.md`, `docs/release-verifications/aispm-launch-readiness-rollup.json`, and `scripts/validate-aispm-launch-readiness.py`, hosted Pages smoke validation through `docs/release-verifications/hosted-sandbox-pages-smoke-validation.md`, `docs/release-verifications/hosted-sandbox-pages-smoke-validation.json`, and `scripts/validate-hosted-sandbox-pages.mjs`, hosted deployment freshness through `docs/release-verifications/hosted-sandbox-deployment-freshness.md`, `docs/release-verifications/hosted-sandbox-deployment-freshness.json`, `scripts/validate-hosted-sandbox-deployment-freshness.py`, and `community-v1.0.0-aispm-release-evidence-index`, hosted release operator status through `docs/release-verifications/hosted-sandbox-operator-release-status.md`, `docs/release-verifications/hosted-sandbox-operator-release-status.json`, `scripts/validate-hosted-sandbox-operator-status.py`, and `cavra-hosted-sandbox-operator-status-packet.json`, hosted post-deploy evidence through `docs/release-verifications/hosted-sandbox-post-deploy-evidence.md`, `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json`, `scripts/generate-hosted-sandbox-deploy-evidence.py`, `scripts/validate-hosted-sandbox-deploy-evidence.py`, and `cavra-hosted-sandbox-post-deploy-evidence`, AISPM Release Evidence Index through `docs/release-verifications/aispm-release-evidence-index.md`, `docs/release-verifications/aispm-release-evidence-index.json`, `scripts/validate-aispm-release-evidence-index.py`, and `cavra-aispm-release-evidence-index-packet.json`, and readiness export actions, execution timeline,
public-safe trace replay packet inspection, approval lineage, behavior
fingerprinting, and raw
public-safe payload inspection.
Enterprise live ingestion, raw prompt/reasoning replay, private IdP/RBAC
context, kill switch, and runtime overrides remain private Enterprise
capabilities.
- dark-mode-first enterprise security visual design with accessible focus
  states and reduced scrolling.

## Target Next.js Architecture

The static portal can later move to a Next.js app using `app/` routes,
TypeScript content contracts, Tailwind CSS, shadcn/ui primitives, Framer Motion
animations, and Lucide Icons while preserving the same route model and GitHub
Pages static export behavior.

## Boundary Notice

The portal is public Community Edition documentation and demo UX only. It does
not include Enterprise source code, private policy packs, SaaS backend
implementation, license-service internals, customer data, private keys, or
private registry details.

## Next Recommendation

Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
