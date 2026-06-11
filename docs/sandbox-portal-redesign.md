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
  risk narratives, replay-to-policy draft/test fixture previews, review
  workflow readiness checks, and copy/download JSON export actions by agent,
  repository, and control surface;
- CAVRA-branded enterprise security visual design with accessible focus states,
  reduced scrolling, and a fixed Classic light theme for high-contrast reading.

## Pages

| Route | Purpose |
| --- | --- |
| `#dashboard` | Hero, mission, feature cards, risk score, governance metrics, Community GA controls, and production pilot readiness. |
| `#ai-posture` | Public-safe AISPM view with sample/local activity provenance, posture score, agent coverage, risk findings, control coverage, near-miss queue, policy context gaps, pre-action risk forecasts, intent-to-action drift, tool-chain risk graph, agent blast-radius map, control coverage heatmap, evidence confidence drilldown, evidence freshness and retention SLO panel, executive risk narrative, replay-to-policy draft and copy/download test fixture previews, review workflow readiness checks, timeline, approval lineage, behavior fingerprinting, trace replay packet drill-down, and Enterprise locked controls. |
| `#architecture` | Interactive node explorer for source platforms, IaC/cloud, CAVRA, Policy Engine, Evidence Engine, and audit trail. |
| `#policy-engine` | Policy packs, risk levels, violation examples, and remediation guidance. |
| `#evidence` | Evidence workflow, attestations, chain of custody, and sample evidence payload. |
| `#integrations` | Cards for GitHub, GitLab, Azure DevOps, Terraform, OpenTofu, Kubernetes, AWS, Azure, GCP, and MCP servers. |
| `#compliance` | Searchable compliance matrix for NIST, SOC2, ISO27001, CIS, PCI DSS, and OWASP. |
| `#use-cases` | Terraform governance, infrastructure drift, Kubernetes security, AI-agent governance, MCP governance, software supply chain, and audit automation. |
| `#documentation` | GitBook-style documentation surface with nested links and copyable code snippets. |
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
