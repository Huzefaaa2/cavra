# CAVRA Developer Portal Smoke Validation

The sandbox portal smoke validator protects the public GitHub Pages experience
as a user-facing product surface. It verifies that the static portal still
contains the required routes, command palette, mobile navigation, architecture
workbench, compliance filters, brand assets, and deployment workflow checks.

## Validation Command

Run the validator from the repository root:

```bash
python scripts/validate-sandbox-portal.py
```

Expected success output:

```text
CAVRA sandbox portal smoke validation passed.
```

## What It Checks

- Required portal files and brand assets exist.
- Required routes are present: dashboard, AI Posture, architecture, policy
  engine, evidence, integrations, compliance, use cases, documentation, and
  roadmap.
- The command palette includes page, policy, integration, control, and use-case
  search content, plus AI Posture entries for agent observability, kill switch,
  evidence confidence, trace replay, approval lineage, behavior
  fingerprinting, policy context gaps, pre-action risk forecasts, intent-to-action drift, tool-chain risk graphing, agent blast-radius mapping, control coverage heatmap views, replay-to-policy draft and copy/download test fixture previews, replay-to-policy review workflow checks, replay-to-policy review packet export actions, replay-to-policy PR attachment guidance, and replay-to-policy CI gate setup paths, readiness summary, rollout checklist export, audit packet export, and readiness export actions.
- Theme selectors remain available on desktop and mobile for Sentinel, Classic,
  Retro, and Executive dashboard themes.
- Mobile drawer and bottom navigation anchors remain available.
- Architecture nodes remain visible for GitHub, GitLab, IaC, Kubernetes,
  CAVRA, Policy Engine, Evidence Engine, Audit Trail, and cloud providers.
- AI Posture DOM anchors remain available for provenance, overview cards,
  agent coverage, findings, control coverage, near misses, timeline, trace
  replay drill-down, approval lineage, behavior fingerprinting, pre-action
  risk forecasts, intent-to-action drift, tool-chain risk graph, agent blast-radius map, control coverage heatmap, replay-to-policy draft, replay-to-policy review workflow, replay-to-policy review packet export, replay-to-policy PR attachment guidance, replay-to-policy CI gate setup, readiness summary, rollout checklist export, audit packet export, and readiness export, replay-to-policy test fixture copy/download actions, payload,
  `/aispm/posture`, `/aispm/trace-replay`, `/aispm/replay-to-policy-draft`, `/aispm/replay-to-policy-tests`, `/aispm/approval-lineage`, and
  `/aispm/behavior-fingerprints` plus `/aispm/policy-context-gaps` and
  `/aispm/pre-action-risk-forecasts`, `/aispm/intent-action-drift`, `/aispm/tool-chain-graph`, and
  `/aispm/agent-blast-radius`, and `/aispm/control-coverage-heatmap` fallback loading.
- Compliance filters still include NIST, SOC2, ISO27001, CIS, PCI DSS, and
  OWASP.
- The GitHub Pages workflow still smoke-tests the page, JavaScript, stylesheet,
  brand assets, C4 diagram, evidence JSON, Enterprise Trial portal link, and
  AISPM trial lab notebook readiness summary link.
- The Enterprise Trial page links to the AISPM trial lab notebook publication
  readiness Markdown, readiness JSON, and GitHub Wiki lab notebook.
- The Enterprise Trial page exposes a stable page-local TOC anchor for AISPM
  trial lab notebook readiness.
- The AI Posture page exposes an AISPM Enterprise Trial readiness checklist for
  lab notebook, access portal, operator approval, revocation/expiry, release
  evidence, and Enterprise automation boundary review.
- The readiness checklist can copy a Markdown summary and download
  `cavra-aispm-enterprise-trial-readiness-packet.json`.
- The AI Posture page shows the Enterprise Trial evaluator handoff covering
  trial portal, package reference, license boundary, lab notebook, support
  path, and revocation/expiry closeout.
- The AI Posture page shows the Enterprise Trial evaluation journey from
  request submission through operator approval, package pull, license
  validation, scenario execution, evidence review, and closeout verification.
- The AI Posture page shows AISPM Trial Closeout Evidence for license expiry,
  revocation, package access removal, blocked runtime validation, archived
  evidence, and evaluator feedback.
- The AI Posture page shows AISPM Trial Feedback Intake categories for setup
  friction, policy clarity, dashboard usefulness, report usefulness,
  integration gaps, procurement concerns, and go/no-go decision.
- The AI Posture page shows AISPM Trial Outcome Summary for readiness,
  evaluator handoff, journey coverage, closeout evidence, feedback coverage,
  and CSO/CISO go/no-go review.
- The AI Posture page can copy or download
  `cavra-aispm-trial-review-packet.json` as a public-safe trial review bundle.
- The AI Posture page shows AISPM Trial Review Packet Integrity for schema,
  generated timestamp, expected filename, public-safety boundary, excluded
  private fields, and Enterprise-only boundary signals.
- The AI Posture page shows AISPM Trial Procurement Readiness for legal,
  security, deployment, support, licensing, data handling, and pilot-scope
  buyer review.
- The AI Posture page shows AISPM Trial Pilot Scope Builder for target
  repositories, AI agents, required checks, policies, evidence owners, success
  criteria, and go/no-go date.
- The AI Posture page can copy or download
  `cavra-aispm-trial-pilot-scope-packet.json` as a public-safe pilot approval
  attachment.
- The AI Posture page shows AISPM Pilot Approval Checklist for owner
  assignment, repository selection, agent registration, required checks, policy
  selection, evidence owners, support path, and go/no-go acceptance.
- The AI Posture page can copy or download
  `cavra-aispm-pilot-approval-packet.json` as a public-safe production-pilot
  approval attachment.
- The AI Posture page shows AISPM Pilot Launch Readiness Summary for scope
  definition, approval readiness, report availability, evidence review,
  support confirmation, and CSO/CISO go/no-go readiness.
- The AI Posture page can copy or download
  `cavra-aispm-pilot-launch-decision-packet.json` as a public-safe launch
  decision record attachment.
- The AI Posture page shows Production Pilot Evidence Room for CSO/CISO,
  security, platform, procurement, auditor, and operator review catalogs.
- The AI Posture page can copy or download
  `cavra-aispm-pilot-evidence-room-packet.json` as a public-safe evidence room
  reviewer handoff artifact.
- The AI Posture page shows Evidence Room Reviewer Checklist for CSO/CISO,
  security, platform, procurement, auditor, and operator pre-pilot acceptance
  criteria.
- The AI Posture page can copy or download
  `cavra-aispm-evidence-reviewer-checklist-packet.json` as a public-safe launch
  reviewer checklist artifact.
- The AI Posture page shows Pilot Exception Register for unresolved risks,
  accepted exceptions, owners, status, expiry expectations, and Enterprise
  workflow boundaries.
- The AI Posture page can copy or download
  `cavra-aispm-pilot-exception-register-packet.json` as a public-safe exception
  register launch approval artifact.
- The AI Posture page shows Pilot Risk Acceptance Summary for open exceptions,
  accepted risks, monitored risks, accountable owners, launch-blocking items,
  and Enterprise-only signed risk acceptance.
- The AI Posture page can copy or download
  `cavra-aispm-pilot-risk-acceptance-packet.json` as a public-safe CSO/CISO
  risk acceptance launch approval artifact.
- The AI Posture page shows Pilot Launch Board Pack for launch decision,
  evidence room, risk acceptance, exception register, reviewer checklist, and
  executive report artifacts.
- The AI Posture page can copy or download
  `cavra-aispm-pilot-launch-board-pack-packet.json` as a public-safe board/CISO
  artifact index with freshness and integrity metadata.
- The AISPM launch artifact index is maintained at
  `docs/release-verifications/aispm-launch-board-pack-artifact-index.json` and
  validated by `scripts/validate-aispm-launch-artifacts.py`.
- Playwright visual smoke validation is available through
  `npm run validate:sandbox:visual`, implemented by
  `scripts/validate-sandbox-visual.mjs`. It captures public-safe desktop and
  mobile screenshots under `.cavra/visual-smoke/` and checks the dashboard,
  AISPM board-pack panel, report center panel, command palette, and theme
  readability.
- The visual smoke validation record is maintained at
  `docs/release-verifications/aispm-visual-smoke-validation.md` and
  `docs/release-verifications/aispm-visual-smoke-validation.json`.
- Visual freshness is enforced by
  `scripts/validate-aispm-visual-freshness.py`, which keeps the visual smoke
  record, board-pack artifact index, wiki navigation, package script, and
  GitHub workflow references synchronized.
- The AISPM launch readiness rollup is maintained at
  `docs/release-verifications/aispm-launch-readiness-rollup.md` and
  `docs/release-verifications/aispm-launch-readiness-rollup.json`, and is
  validated by `scripts/validate-aispm-launch-readiness.py`.
- Hosted GitHub Pages browser smoke is recorded at
  `docs/release-verifications/hosted-sandbox-pages-smoke-validation.md` and
  `docs/release-verifications/hosted-sandbox-pages-smoke-validation.json`, and
  is validated after deploy by `scripts/validate-hosted-sandbox-pages.mjs`.
- Hosted GitHub Pages deployment freshness is recorded at
  `docs/release-verifications/hosted-sandbox-deployment-freshness.md` and
  `docs/release-verifications/hosted-sandbox-deployment-freshness.json`, and
  is validated by `scripts/validate-hosted-sandbox-deployment-freshness.py`
  using the build sentinel `community-v1.0.0-aispm-release-evidence-index`.
- Hosted release operator status is recorded at
  `docs/release-verifications/hosted-sandbox-operator-release-status.md` and
  `docs/release-verifications/hosted-sandbox-operator-release-status.json`,
  validated by `scripts/validate-hosted-sandbox-operator-status.py`, and
  exported from the portal as `cavra-hosted-sandbox-operator-status-packet.json`.
- Hosted GitHub Pages post-deploy evidence is defined at
  `docs/release-verifications/hosted-sandbox-post-deploy-evidence.md` and
  `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json`,
  generated by `scripts/generate-hosted-sandbox-deploy-evidence.py`, validated
  by `scripts/validate-hosted-sandbox-deploy-evidence.py`, and uploaded as
  `cavra-hosted-sandbox-post-deploy-evidence`.
- The AISPM Release Evidence Index is defined at
  `docs/release-verifications/aispm-release-evidence-index.md` and
  `docs/release-verifications/aispm-release-evidence-index.json`, validated by
  `scripts/validate-aispm-release-evidence-index.py`, and exported from the
  portal as `cavra-aispm-release-evidence-index-packet.json`.
- AISPM report catalog readiness is defined at
  `docs/release-verifications/aispm-report-catalog-readiness.md` and
  `docs/release-verifications/aispm-report-catalog-readiness.json`, validated
  by `scripts/validate-aispm-report-catalog-readiness.py`, and exported from
  the portal as `cavra-aispm-report-catalog-packet.json`.
- AISPM report delivery setup readiness is defined at
  `docs/release-verifications/aispm-report-delivery-setup-readiness.md` and
  `docs/release-verifications/aispm-report-delivery-setup-readiness.json`,
  validated by `scripts/validate-aispm-report-delivery-setup-readiness.py`,
  and exported from the portal as
  `cavra-aispm-report-delivery-setup-packet.json`.
- AISPM report operations readiness is defined at
  `docs/release-verifications/aispm-report-operations-readiness.md` and
  `docs/release-verifications/aispm-report-operations-readiness.json`,
  validated by `scripts/validate-aispm-report-operations-readiness.py`, and
  exported from the portal as
  `cavra-aispm-report-operations-readiness-packet.json`.
- AISPM report governance readiness is defined at
  `docs/release-verifications/aispm-report-governance-readiness.md` and
  `docs/release-verifications/aispm-report-governance-readiness.json`,
  validated by `scripts/validate-aispm-report-governance-readiness.py`, and
  exported from the portal as
  `cavra-aispm-report-governance-readiness-packet.json`.
- AISPM report assurance readiness is defined at
  `docs/release-verifications/aispm-report-assurance-readiness.md` and
  `docs/release-verifications/aispm-report-assurance-readiness.json`,
  validated by `scripts/validate-aispm-report-assurance-readiness.py`, and
  exported from the portal as
  `cavra-aispm-report-assurance-readiness-packet.json`.
- AISPM report response readiness is defined at
  `docs/release-verifications/aispm-report-response-readiness.md` and
  `docs/release-verifications/aispm-report-response-readiness.json`,
  validated by `scripts/validate-aispm-report-response-readiness.py`, and
  exported from the portal as
  `cavra-aispm-report-response-readiness-packet.json`.
- AISPM report trial operations readiness is defined at
  `docs/release-verifications/aispm-report-trial-operations-readiness.md` and
  `docs/release-verifications/aispm-report-trial-operations-readiness.json`,
  validated by `scripts/validate-aispm-report-trial-operations-readiness.py`,
  and exported from the portal as
  `cavra-aispm-report-trial-operations-readiness-packet.json`.
- AISPM pilot control readiness is defined at
  `docs/release-verifications/aispm-pilot-control-readiness.md` and
  `docs/release-verifications/aispm-pilot-control-readiness.json`, validated by
  `scripts/validate-aispm-pilot-control-readiness.py`, and exported from the
  portal as `cavra-aispm-pilot-control-readiness-packet.json`.
- AISPM v1.0 public release readiness is defined at
  `docs/release-verifications/aispm-v1.0-public-release-readiness.md` and
  `docs/release-verifications/aispm-v1.0-public-release-readiness.json`,
  validated by `scripts/validate-aispm-v100-public-release.py`, and supported
  by `docs/releases/community-v1.0.0-aispm.md` and
  `docs/aispm-v1.0-public-walkthrough.md`.
- The board pack freshness gate covers
  `cavra-aispm-pilot-launch-decision-packet.json`,
  `cavra-aispm-pilot-evidence-room-packet.json`,
  `cavra-aispm-pilot-risk-acceptance-packet.json`,
  `cavra-aispm-pilot-exception-register-packet.json`,
  `cavra-aispm-evidence-reviewer-checklist-packet.json`,
  `cavra-aispm-executive-risk-brief.md`,
  `cavra-aispm-board-kpi-pack.json`, and
  `cavra-aispm-soc2-audit-summary.md`.
- The command palette can find the AISPM trial lab notebook readiness summary,
  readiness JSON, and GitHub Wiki lab notebook from `Ctrl+K`.
- README and wiki navigation link to the portal documentation.

## CI Enforcement

The validator is enforced by:

- `.github/workflows/community-ci.yml`
- `.github/workflows/security-scan.yml`
- `.github/workflows/release-community.yml`
- `.github/workflows/cavra-governance.yml`
- `.github/workflows/deploy-sandbox.yml`

## Public Boundary

This validator only checks public Community Edition portal contracts. It does
not require Enterprise source code, private policy packs, SaaS backend logic,
license-service internals, customer data, provider credentials, or private
registry paths.

## User Stories

- As a CISO, I can trust that the public portal still explains CAVRA's control
  model clearly before a release.
- As an auditor, I can inspect a stable compliance and evidence navigation
  surface without needing private systems.
- As a platform engineer, I can catch broken route, asset, and workflow
  regressions before GitHub Pages deployment.
- As a buyer evaluating CAVRA, I can see a coherent public product experience
  with architecture, policies, integrations, compliance, and documentation in
  one place.

## Enterprise Challenge Solved

Enterprise AI governance tools are often evaluated through public demos before
security teams grant deeper access. This validator keeps the public portal
credible by ensuring the most important buyer, auditor, and operator surfaces do
not silently regress.

## Next Recommendation

Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
