# CAVRA Sandbox GUI Audit Report

Generated from the automated Playwright audit in `gui-audit/findings.json`.

Target: `http://localhost:5173/`

Screenshots: `gui-audit/screenshots/`

## Executive Finding

The current sandbox GUI is visually polished and useful as a public product/demo portal, but it is not yet structured as a real operator application. The dominant interaction model is a long-form product website embedded in an app shell: hero copy, product-path language, static feature grids, static diagrams, sample packets, external trial CTAs, and explanatory documentation sections.

The most important application gap is state. The audit observed no backend API calls during route load for any of the 13 application screens. The setup route contains interactive controls for local API-backed setup actions, but the normal screen render is still static until the operator manually presses a control. There is no state-aware landing experience that switches between unconfigured, configured, degraded, and live-monitoring states.

## Automated Inspection Summary

| Item | Result |
| --- | --- |
| Routes discovered | 13 `.page-panel` screens |
| Desktop screenshots | 13 |
| Mobile screenshots | 3 representative screens |
| API-backed screens during route load | 0 |
| Static screens during route load | 13 |
| Screens with website/product patterns | 13 |

Screens audited:

- `dashboard`
- `first-run-setup`
- `ai-posture`
- `architecture`
- `policy-engine`
- `evidence`
- `use-cases`
- `operator-experience`
- `enterprise-trial`
- `integrations`
- `compliance`
- `roadmap`
- `documentation`

## Screen-By-Screen Findings

| Screen | Screenshot | Current Role | App Readiness Finding |
| --- | --- | --- | --- |
| Dashboard | `screenshots/dashboard-desktop.png` | Product overview and public demo entry point | Strong marketing-site pattern. It should become the operator home with live status widgets, setup state, policy status, open approvals, recent decisions, and AISPM score. |
| First-Run Setup | `screenshots/first-run-setup-desktop.png` | Setup explanation plus live action controls | Best current application candidate. It has setup controls but does not load setup status automatically on route entry. Needs stepper, status checks, validation, and persisted state summary. |
| AISPM | `screenshots/ai-posture-desktop.png` | Static posture/report center explainer with generated sample packets | Partial. It lists AISPM concepts and export packets, but needs live posture cards, findings table, filters, report generation, export history, and state from `/aispm/*` endpoints. |
| Architecture | `screenshots/architecture-desktop.png` | Static architecture explanation | Belongs mostly in docs or product site. In the app, architecture should become environment/config topology and connector health. |
| Policy Engine | `screenshots/policy-engine-desktop.png` | Static policy examples | Missing true policy management. Needs policy pack list, rule editor/preview, test harness, validation errors, publish/rollback controls, and decision simulation. |
| Evidence | `screenshots/evidence-desktop.png` | Static evidence story and sample payload | Partial. Needs evidence search, filters, artifact downloads, checksum/signature verification, retention status, and live `/evidence` data. |
| Use Cases | `screenshots/use-cases-desktop.png` | Product use-case catalog | Product-site content. Should be removed from operational app or converted into runnable scenario templates. |
| Operator Paths | `screenshots/operator-experience-desktop.png` | Persona guidance | Product/training content. Should move to docs or become role-aware landing presets after login. |
| Trial Access | `screenshots/enterprise-trial-desktop.png` | Trial funnel explanation | Product/trial-site content. Should not be in the operator app except as entitlement status if running a trial tenant. |
| Integrations | `screenshots/integrations-desktop.png` | Static list of ready/planned connectors | Partial. Needs connector cards with Connected/Disconnected/Error states, configuration, test connection, logs, and evidence. |
| Compliance | `screenshots/compliance-desktop.png` | Static control mapping summary | Partial. Needs control coverage linked to decisions, evidence freshness, mapped frameworks, and exportable control packets. |
| Roadmap | `screenshots/roadmap-desktop.png` | Public product roadmap | Does not belong in operational app. Keep roadmap in GitHub/docs. |
| Documentation | `screenshots/documentation-desktop.png` | Documentation directory | Useful but should be a Help/Docs drawer or external links, not a primary operator workflow. |

## Gap Analysis Against Target Application Model

### A. Progressive Disclosure And State-Aware Layout

| Requirement | Score | Evidence | Gap |
| --- | --- | --- | --- |
| Distinct unconfigured / first-run state | Partial | `first-run-setup` route exists and contains setup controls. | The app does not automatically route unconfigured users to setup, nor does the dashboard collapse to one primary setup CTA. |
| Distinct configured dashboard state | Missing | `dashboard` remains a product hero/feature page. | No live widgets for policy health, recent evaluations, open approvals, evidence count, AISPM score, connector health, or agent trust. |
| UI persists and reflects actual state | Partial | Setup controls can call API actions, and the local API supports setup state. | Normal route load did not call backend APIs in the audit. Most cards and numbers are static arrays in `sandbox.js`. |

### B. Core Lifecycle Workflow

| Lifecycle Area | Score | Evidence | Gap |
| --- | --- | --- | --- |
| 1. Installation & Setup | Partial | `first-run-setup` has browser controls and setup copy. | Needs stateful stepper with automatic compatibility checks: API reachable, CLI installed, policy pack loaded, demo workspace present, SMTP configured, AISPM seeded. |
| 2. Configuration | Missing | `policy-engine` is static and example-driven. | No editable Policies, Agents, Approvals, Notifications, SMTP, retention, or connector configuration screens. |
| 3. Integration | Partial | `integrations` lists GitHub, Terraform, Kubernetes, MCP, Azure, GitLab, Azure DevOps. | No live connector state, test connection action, credentials status, error detail, or connector audit evidence. |
| 4. Monitoring | Missing | `dashboard` and `ai-posture` show static/public sample content. | No live decision stream, approval queue depth, blocked action trend, posture refresh, risk severity state, or recent activity feed. |
| 5. Reporting | Partial | `ai-posture` references report packs and packet downloads. | No date range, report scope, export format selector, report history, scheduled delivery, recipient governance, or delivery audit state. |

### C. Website-Pattern Smells

| Smell | Instances |
| --- | --- |
| Hero banners/taglines in app chrome | Dashboard hero: "Before the agent acts, CAVRA decides"; `Runtime Authority for AI coding agents`. |
| Feature-grid marketing cards | Dashboard "Why Enterprises Deploy CAVRA", product paths, proof strip, business outcome cards. |
| Trial/demo/access CTAs inside app | Top nav `Request Trial`, dashboard "Run Public Demo", trial access route. |
| Long scrolling single-page layout | Dashboard and AISPM routes use long page sections rather than compact workstation views. |
| Static diagrams/screenshots as operational substitutes | Architecture, AISPM, evidence, integrations, and compliance screens primarily explain concepts rather than show live system state. |
| Public roadmap in app shell | `roadmap` route is a product/docs artifact, not an operator workflow. |
| Documentation as primary app view | `documentation` route is useful, but should be Help/Docs, not a core application page. |

## Live-Vs-Static Data Verdict

The audit captured no API requests during route load. Therefore:

- The current GUI can render without the FastAPI backend.
- Most screen content is generated from static arrays in `apps/sandbox-ui/sandbox.js`.
- Setup controls are present and appear API-oriented, but the route does not automatically read setup state on entry.
- Operational surfaces such as Evidence, Approvals, Agent Registry, MCP Trust, AISPM, and Reports are not yet live data workstations.

## Notable Existing Strengths

- Consistent visual system and route shell already exist.
- Sidebar/top navigation exists and can be adapted into an operator console.
- First-run setup controls are a solid foundation for an app-grade setup wizard.
- The public API already exposes many domains needed for a real application: setup status, policy action catalog, evidence, approvals, agents, MCP trust, AISPM posture, and console config.
- The static UI has enough domain content to seed empty states, tooltips, and help panels after the app redesign.

## Primary Conclusion

The current GUI should be split conceptually:

1. Keep product education, trial funnel, roadmap, use cases, and high-level diagrams in the public product site and documentation.
2. Rebuild the sandbox GUI into a stateful operator console with Dashboard, Setup, Policies, Agents & MCP Trust, Approvals, Evidence, AISPM Posture, Reports, Integrations, and Settings.

