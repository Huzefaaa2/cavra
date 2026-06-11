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
  evidence freshness SLO panels, replay-to-policy draft/test fixture previews,
  review workflow readiness checks, review packet export actions, PR attachment
  guidance, replay-to-policy CI gate setup paths, readiness summary, rollout checklist export, audit packet export, and readiness export actions, and copy/download JSON export actions;
- CAVRA-branded enterprise security visual design with accessible focus states,
  reduced scrolling, and a fixed Classic light theme for high-contrast reading.

The `#ai-posture` route renders the public-safe AISPM contract with sample data
by default and reads `/aispm/posture` when `window.CAVRA_API_BASE` is
configured. It includes posture overview, agent coverage, risk findings,
control coverage, near-miss queue, policy context gaps, pre-action risk
forecasts, intent-to-action drift, evidence confidence drilldown, evidence
freshness SLO panel, replay-to-policy draft and copy/download test fixture
previews, review workflow readiness checks, review packet export actions, PR
attachment guidance, replay-to-policy CI gate setup paths, readiness summary, rollout checklist export, audit packet export, and readiness export actions, execution timeline,
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
