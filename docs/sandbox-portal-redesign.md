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
- AISPM final announcement readiness through
  `docs/release-verifications/aispm-final-announcement-readiness.md`,
  `docs/release-verifications/aispm-final-announcement-readiness.json`,
  `scripts/validate-aispm-final-announcement-readiness.py`, and
  `cavra-aispm-final-announcement-readiness-packet.json`;
- command palette with `Ctrl+K` search for pages, policies, controls,
  integrations, documentation, and examples;
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
  for repository/target/tool/policy reach, control coverage heatmap views,
  evidence confidence drilldowns, evidence freshness SLO panels, executive
  risk narratives, AISPM Enterprise Trial readiness checklist with copy/download
  packet export, Enterprise Trial evaluator handoff, Enterprise Trial evaluation
  journey timeline, AISPM Trial Closeout Evidence panel, AISPM Trial Feedback
  Intake model, AISPM Trial Outcome Summary, AISPM Trial Review Packet export,
  AISPM Trial Review Packet Integrity panel,
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
  replay-to-policy draft/test fixture previews, workflow readiness checks,
  review packet export actions, PR attachment
  guidance, replay-to-policy CI gate setup paths, readiness summary, rollout checklist export, audit packet export, and readiness export actions, and copy/download JSON export actions by agent, repository, and
  control surface;
- Enterprise Trial reviewer links for the AISPM trial lab notebook publication
  readiness summary, readiness JSON, and GitHub Wiki lab notebook, with a
  stable page-local TOC anchor for release reviewers;
- command palette entries for the AISPM trial lab notebook readiness summary,
  readiness JSON, and GitHub Wiki lab notebook;
- CAVRA-branded enterprise security visual design with accessible focus states,
  reduced scrolling, and a fixed Classic light theme for high-contrast reading.

## Pages

| Route | Purpose |
| --- | --- |
| `#dashboard` | Hero, mission, feature cards, risk score, governance metrics, Community GA controls, and production pilot readiness. |
| `#ai-posture` | Public-safe AISPM view with sample/local activity provenance, posture score, agent coverage, risk findings, control coverage, near-miss queue, policy context gaps, pre-action risk forecasts, intent-to-action drift, tool-chain risk graph, agent blast-radius map, control coverage heatmap, evidence confidence drilldown, evidence freshness and retention SLO panel, executive risk narrative, AISPM Enterprise Trial readiness checklist and export packet, Enterprise Trial evaluator handoff, Enterprise Trial evaluation journey timeline, AISPM Trial Closeout Evidence panel, AISPM Trial Feedback Intake model, AISPM Trial Outcome Summary, AISPM Trial Review Packet export, AISPM Trial Review Packet Integrity panel, AISPM Trial Procurement Readiness panel, AISPM Trial Pilot Scope Builder, AISPM Trial Pilot Scope Packet export, AISPM Pilot Approval Checklist, AISPM Pilot Approval Packet export, AISPM Pilot Launch Readiness Summary, AISPM Pilot Launch Decision Packet export as `cavra-aispm-pilot-launch-decision-packet.json`, Production Pilot Evidence Room, Production Pilot Evidence Room Packet export as `cavra-aispm-pilot-evidence-room-packet.json`, Evidence Room Reviewer Checklist, Evidence Room Reviewer Checklist Packet export as `cavra-aispm-evidence-reviewer-checklist-packet.json`, Pilot Exception Register, Pilot Exception Register Packet export as `cavra-aispm-pilot-exception-register-packet.json`, Pilot Risk Acceptance Summary, Pilot Risk Acceptance Packet export as `cavra-aispm-pilot-risk-acceptance-packet.json`, Pilot Launch Board Pack, Pilot Launch Board Pack Packet export as `cavra-aispm-pilot-launch-board-pack-packet.json`, artifact freshness validation through `scripts/validate-aispm-launch-artifacts.py`, AISPM launch readiness rollup through `docs/release-verifications/aispm-launch-readiness-rollup.md`, `docs/release-verifications/aispm-launch-readiness-rollup.json`, and `scripts/validate-aispm-launch-readiness.py`, hosted Pages smoke validation through `docs/release-verifications/hosted-sandbox-pages-smoke-validation.md`, `docs/release-verifications/hosted-sandbox-pages-smoke-validation.json`, and `scripts/validate-hosted-sandbox-pages.mjs`, hosted deployment freshness through `docs/release-verifications/hosted-sandbox-deployment-freshness.md`, `docs/release-verifications/hosted-sandbox-deployment-freshness.json`, `scripts/validate-hosted-sandbox-deployment-freshness.py`, and `community-v1.0.0-aispm-release-evidence-index`, hosted release operator status through `docs/release-verifications/hosted-sandbox-operator-release-status.md`, `docs/release-verifications/hosted-sandbox-operator-release-status.json`, `scripts/validate-hosted-sandbox-operator-status.py`, and `cavra-hosted-sandbox-operator-status-packet.json`, hosted post-deploy evidence through `docs/release-verifications/hosted-sandbox-post-deploy-evidence.md`, `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json`, `scripts/generate-hosted-sandbox-deploy-evidence.py`, `scripts/validate-hosted-sandbox-deploy-evidence.py`, and `cavra-hosted-sandbox-post-deploy-evidence`, AISPM Release Evidence Index through `docs/release-verifications/aispm-release-evidence-index.md`, `docs/release-verifications/aispm-release-evidence-index.json`, `scripts/validate-aispm-release-evidence-index.py`, and `cavra-aispm-release-evidence-index-packet.json`, CSO report center downloads including `cavra-aispm-executive-risk-brief.md`, `cavra-aispm-board-kpi-pack.json`, and `cavra-aispm-soc2-audit-summary.md`, replay-to-policy draft and copy/download test fixture previews, review workflow readiness checks, review packet export actions, PR attachment guidance, replay-to-policy CI gate setup paths, readiness summary, rollout checklist export, audit packet export, CI gate rollout auditor view, and readiness export actions, timeline, approval lineage, behavior fingerprinting, trace replay packet drill-down, and Enterprise locked controls. |
| `#architecture` | Interactive node explorer for source platforms, IaC/cloud, CAVRA, Policy Engine, Evidence Engine, and audit trail. |
| `#policy-engine` | Policy packs, risk levels, violation examples, and remediation guidance. |
| `#evidence` | Evidence workflow, attestations, chain of custody, and sample evidence payload. |
| `#integrations` | Cards for GitHub, GitLab, Azure DevOps, Terraform, OpenTofu, Kubernetes, AWS, Azure, GCP, and MCP servers. |
| `#compliance` | Searchable compliance matrix for NIST, SOC2, ISO27001, CIS, PCI DSS, and OWASP. |
| `#use-cases` | Terraform governance, infrastructure drift, Kubernetes security, AI-agent governance, MCP governance, software supply chain, and audit automation. |
| `#documentation` | GitBook-style documentation surface with nested links and copyable code snippets. |
| `#enterprise-trial` | Enterprise Trial portal link, package/license boundary status, and AISPM trial lab notebook readiness links with page-local navigation for release reviewers. |
| `#roadmap` | Interactive roadmap columns for Community, Enterprise, SaaS, and ecosystem work. |

## Target Next.js Architecture

The static portal can later move to a Next.js app without changing the
information architecture:

```text
apps/portal/
  app/
    layout.tsx
    page.tsx
    architecture/page.tsx
    policy-engine/page.tsx
    evidence/page.tsx
    integrations/page.tsx
    compliance/page.tsx
    use-cases/page.tsx
    documentation/page.tsx
    roadmap/page.tsx
  components/
    portal/AppShell.tsx
    portal/TopHeader.tsx
    portal/SidebarNav.tsx
    portal/MobileNavigation.tsx
    portal/RightToc.tsx
    search/CommandPalette.tsx
    architecture/ArchitectureExplorer.tsx
    policy/PolicyExplorer.tsx
    compliance/ComplianceMatrix.tsx
    docs/DocsReader.tsx
  content/
    navigation.ts
    policies.ts
    integrations.ts
    compliance.ts
    roadmap.ts
  lib/
    search-index.ts
    github-pages-base-path.ts
```

Recommended stack for the future app:

- Next.js with static export for GitHub Pages;
- TypeScript for content contracts and route models;
- Tailwind CSS for the portal design system;
- shadcn/ui for command palette, drawer, tabs, cards, table, and dialog
  primitives;
- Framer Motion for route transitions, drawer animation, command palette
  animation, and architecture node hover/selection;
- Lucide Icons for sidebar, top header, command palette, and mobile bottom bar.

## Accessibility And Performance

The static implementation avoids external runtime dependencies, keeps all page
switching client-side, supports keyboard navigation, exposes ARIA labels for
major navigation regions, uses visible focus states, and hides the right table
of contents on mobile to prevent horizontal scrolling.

## Boundary Notice

The portal is public Community Edition documentation and demo UX only. It does
not include Enterprise source code, private policy packs, SaaS backend
implementation, license-service internals, customer data, private keys, or
private registry details.

## Next Recommendation

Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
