# CAVRA Sandbox GUI Redesign Plan

Goal: turn the sandbox from a public product/demo website into a real, actionable, stateful software application interface for security and platform operators.

This plan intentionally does not implement code. It defines the app model, screen structure, data sources, and backlog for review.

## 1. Information Architecture

### Proposed Persistent Navigation

Use a persistent left sidebar on desktop and a compact top/mobile drawer on mobile.

Primary app sections:

1. **Dashboard**
2. **Setup**
3. **Policies**
4. **Agents & MCP Trust**
5. **Approvals**
6. **Evidence**
7. **AISPM Posture**
8. **Reports**
9. **Integrations**
10. **Settings**
11. **Help**

### Existing Route Mapping

| Current Route | New Section | Treatment |
| --- | --- | --- |
| `dashboard` | Dashboard | Replace marketing hero with live stateful widgets. Keep a short product identity line only in the header. |
| `first-run-setup` | Setup | Promote to real setup wizard and status center. |
| `policy-engine` | Policies | Convert static examples into policy pack inventory, rule viewer/editor, validation, and simulator. |
| `integrations` | Integrations | Convert static connector list into connector health/config cards. |
| `evidence` | Evidence | Convert static evidence story into searchable evidence hub. |
| `ai-posture` | AISPM Posture + Reports | Split into live posture dashboard and separate report center. |
| `architecture` | Help or Settings > Environment | Remove from main operator path; convert useful pieces into deployment topology/status panels. |
| `use-cases` | Help / scenario templates | Remove marketing copy; keep runnable scenario templates if useful. |
| `operator-experience` | Help / role paths | Move to docs/help drawer. |
| `enterprise-trial` | Product/trial site | Remove from operator app unless current tenant is a trial and needs entitlement status. |
| `compliance` | AISPM Posture / Reports | Convert into control coverage and compliance exports backed by posture/evidence data. |
| `roadmap` | GitHub/docs | Remove from operator app. |
| `documentation` | Help | Keep as help links, not a first-class app workflow. |

### Content To Remove From The App Shell

Move or keep only outside the app:

- "Before the agent acts, CAVRA decides" hero blocks.
- Business outcome and product-path sections.
- Trial access funnel.
- Public roadmap.
- Product use cases.
- Long-form architecture explainers.
- Edition comparison and marketing CTAs.
- "Request Trial", "View GitHub", and public website CTAs as primary app controls.

Keep inside the app only when rewritten as operational empty states, help hints, or links.

## 2. Empty-State Vs Configured-State Dashboard

### Empty-State Dashboard

Show this when `/setup/status` returns `configured: false` or `setup_complete: false`.

```text
+---------------------------------------------------------------+
| CAVRA Local Console                         API: Connected    |
+-------------------+-------------------------------------------+
| Sidebar           | Setup required                            |
| Dashboard         |                                           |
| Setup             | [1] Connect local API        OK/Fail      |
| Policies          | [2] Create defaults         Not started  |
| Agents & MCP      | [3] Generate demo workspace Not started  |
| Approvals         | [4] Validate decisions       Not started |
| Evidence          | [5] Complete setup           Disabled    |
| AISPM Posture     |                                           |
| Reports           | Primary CTA: Start Setup Wizard           |
+-------------------+-------------------------------------------+
```

Widgets:

| Widget | Purpose | Data Source |
| --- | --- | --- |
| API Reachability | Shows backend status/version. | `GET /health`, `GET /version`, `GET /console/config` |
| Setup State | Shows configured/setup-complete state. | `GET /setup/status` |
| Default Policy Pack | Shows active/default pack availability. | `GET /setup/status`, `GET /policy-action-catalog` |
| Demo Workspace | Shows whether sample risky fixtures exist. | `GET /setup/status` |
| SMTP/Reports | Shows report delivery placeholder or configured state. | `GET /setup/status`, future report config endpoint |
| Next Step | Single primary CTA based on setup state. | Derived client-side from setup state |

### Configured-State Dashboard

Show this when `/setup/status` returns `configured: true` and `setup_complete: true`.

```text
+---------------------------------------------------------------+
| Dashboard                                      Last refresh 5s |
+-------------------+-------------------------------------------+
| Sidebar           | [Policy Health] [Recent Decisions]        |
| Dashboard         | [Open Approvals] [Evidence Bundles]       |
| Setup             | [AISPM Score] [Agent/MCP Trust]           |
| Policies          |                                           |
| Agents & MCP      | Recent Activity Stream                    |
| Approvals         | - blocked terraform apply                 |
| Evidence          | - approval routed IAM role change         |
| AISPM Posture     | - evidence bundle generated               |
| Reports           |                                           |
+-------------------+-------------------------------------------+
```

Widgets:

| Widget | Contents | Data Source |
| --- | --- | --- |
| Policy Health | Loaded packs, validation status, last update. | `GET /policy-action-catalog`, future `GET /policies` |
| Policy Evaluations 24h | allow/block/approval/warn counts. | `GET /activity` or AISPM posture source |
| Open Approvals | pending count, oldest pending, severity. | `GET /approvals?state=pending` |
| Evidence Bundles This Week | count, newest bundle, verification status. | `GET /evidence` |
| AISPM Posture Score | risk level, findings, coverage score. | `GET /aispm/posture`, `/aispm/findings`, `/aispm/control-coverage` |
| Agent/MCP Trust Status | agents, unknown tools, unapproved MCP servers. | `GET /agents`, `GET /mcp/servers`, `GET /mcp/trust` |
| Connector Health | connected/error/disconnected counts. | `GET /console/config`, future `GET /integrations` |
| Recent Decisions | timestamp, actor, action, target, decision, severity. | `GET /activity` or evidence/activity endpoint |

Refresh cadence:

- Health/config: 30 seconds.
- Decision stream: 5-10 seconds or manual refresh in Community.
- AISPM posture: 30-60 seconds.
- Evidence and reports: manual refresh plus after export actions.

## 3. Setup Wizard

The Setup wizard should be a stateful stepper, not a static explanation page.

### Step 1: Connect Local API

Controls:

- API base URL input.
- "Test connection" button.
- Show `/health`, `/version`, and `/console/config`.

Validation:

- Green: API reachable and product is CAVRA.
- Yellow: API reachable but version/config incomplete.
- Red: API unreachable or CORS blocked.

### Step 2: Create Default Environment

Action:

- `POST /setup/bootstrap`

Visible results:

- Workspace name.
- Mode/edition.
- Artifact root.
- Default policy pack.
- Setup state path.

### Step 3: Load Or Select Policy Pack

Data:

- `GET /policy-action-catalog`

Controls:

- Default pack selector.
- Rule catalog grouped by Files, Commands, Git, MCP, Cloud, Evidence.
- Read-only preview for Community first pass.
- Future edit/add/delete actions.

Validation:

- Policy pack exists.
- At least one block rule and one approval rule.
- No schema validation errors.

### Step 4: Register First Agent

Data:

- `GET /agents/profiles`
- `GET /agents`
- `POST /agents`

Controls:

- Agent profile: Codex, Claude Code, Copilot, Cursor, Gemini CLI.
- Repository scope.
- Allowed tools.
- Owner.
- Risk tier.

Validation:

- Required owner and repo scope.
- Tool capabilities classified.
- Unknown MCP tools blocked by default.

### Step 5: Generate Demo Workspace

Action:

- `POST /setup/demo-workspace`

Visible results:

- File tree.
- Known risky actions.
- Expected decisions.

### Step 6: Run First Evaluation

Actions:

- `POST /policy-action-catalog/test`
- `POST /setup/validate`

Visible results:

- Decision result.
- Rule ID.
- Severity.
- Evidence reference.
- AISPM posture delta.

### Step 7: Configure Notifications/Reports

Actions:

- `POST /setup/smtp/test`
- Future report delivery config endpoint.

Controls:

- SMTP host/port/from/recipient.
- Password reference only, not stored raw in UI.
- Send test report.

### Step 8: Complete Setup

Action:

- `POST /setup/complete`

Exit state:

- Redirect to configured dashboard.
- Show "Run a scenario" and "Connect an agent" as next actions.

## 4. Configuration Screens

### Policies

Tabs:

- Policy Packs
- Rules
- Simulator
- Validation
- Rollout

Fields:

- Rule ID: required, unique.
- Action type: select.
- Target pattern: string/glob with inline preview.
- Decision: allow/block/require-approval/warn/attest.
- Severity: info/low/medium/high/critical.
- Approver group: required when decision is approval.
- Evidence requirement: checkbox/select.

Validation:

- JSON/YAML schema validation.
- Conflicting rule detection.
- Test cases before save.
- "Preview decisions" before publish.

### Agents

Tabs:

- Agents
- Profiles
- Repository Scopes
- Risk Tiers

Fields:

- Agent ID, vendor, type, version.
- Capabilities.
- Allowed repositories.
- Allowed tools.
- Owner.
- Status.

Validation:

- Agent ID uniqueness.
- Owner required.
- Capability must map to known classifications.

### MCP Trust

Tabs:

- MCP Servers
- Tool Classifications
- Trust Evaluation

States:

- Approved
- Pending
- Blocked
- Unknown
- Error

Actions:

- Register server.
- Approve trust.
- Revoke trust.
- Test tool call.

### Approvals

Tabs:

- Queue
- Routing Rules
- Provider Delivery
- Break Glass
- Audit

Fields:

- Approver group.
- Actor/claims.
- Reason.
- Expiry.
- External reference.

Validation:

- Reason required for approve/deny/break glass.
- Expiry required for break glass.
- RBAC/OIDC checks surfaced inline.

### Notifications

Tabs:

- SMTP
- Slack/Teams
- Jira/ServiceNow
- Webhooks
- Recipient Governance

Validation:

- Secret references only.
- Test delivery.
- Recipient allowlist.
- Delivery evidence capture.

## 5. Integrations Hub

### Layout

```text
Integrations
  Filters: All | Connected | Disconnected | Error | Planned

  [GitHub]          Connected      Last check 2m ago   [Configure] [Test]
  [MCP Servers]     Error          Unknown tool seen    [Review] [Reconnect]
  [Slack]           Disconnected   Webhook missing      [Connect]
  [ServiceNow]      Planned        Enterprise only      [Learn]
```

### Card Fields

- Provider name and icon.
- State: Connected, Disconnected, Error, Planned, Enterprise-only.
- Scope: CI/CD, MCP, SIEM, ITSM, ChatOps, Cloud, Reports.
- Last checked timestamp.
- Evidence reference.
- Actions by state:
  - Connected: Configure, Test, View Evidence.
  - Disconnected: Connect, View Setup Guide.
  - Error: Reconnect, View Error Detail, Export Diagnostic.
  - Planned/Enterprise-only: View capability boundary.

### Data Sources

- Existing: `GET /console/config`
- Registry: `GET /agents`, `GET /mcp/servers`
- Future: `GET /integrations`, `POST /integrations/{id}/test`, `GET /integrations/{id}/deliveries`

## 6. Monitoring Dashboard

### Metrics

| Metric | Visualization | Status Semantics |
| --- | --- | --- |
| Decisions over time | Stacked area or bar chart | Green: mostly allowed/attested; yellow: approvals rising; red: critical blocks rising |
| Blocked actions | Severity table + sparkline | Red for critical/high |
| Approval queue depth | Number + aging table | Yellow over SLO; red oldest pending over SLO |
| AISPM posture | Score/risk badge + trend | Green/yellow/red from AISPM risk level |
| Evidence freshness | SLO gauge | Green fresh, yellow stale soon, red stale/missing |
| Agent trust | Donut/status list | Red unknown active agents/MCP tools |
| Connector health | Status grid | Red provider error or credentials missing |

### Refresh Cadence

- Default: manual refresh plus 30-second polling.
- Decision stream: 5-10 seconds in local mode.
- Enterprise future: websocket/server-sent events optional.

### Severity Mapping

| CAVRA Severity | UI Status |
| --- | --- |
| `info`, `low` | Green/neutral |
| `medium` | Yellow |
| `high` | Orange |
| `critical` | Red |

## 7. Report Center

### Layout

```text
Reports
  [Date range] [Scope] [Format] [Generate]

  Report Catalog
  - Executive Risk Brief      Markdown/PDF future
  - Board KPI Pack            JSON
  - SOC 2 Audit Summary       Markdown
  - Control Coverage Export   CSV
  - Evidence Freshness Export CSV
  - Agent Risk Register       CSV

  History
  Date | Report | Scope | Status | Download | Evidence
```

### Filters

- Date range.
- Repository.
- Agent.
- Policy pack.
- Severity.
- Decision.
- Report type.
- Evidence status.

### Export UI

- Format selector: Markdown, JSON, CSV in Community.
- Enterprise placeholders: PDF, XLSX, DOCX, signed JSON, scheduled email.
- Generate button.
- Download action.
- Copy CLI command action.

### Data Sources

- `GET /aispm/posture`
- `GET /aispm/findings`
- `GET /aispm/control-coverage`
- `GET /aispm/evidence-freshness`
- Browser-generated report exports today.
- Future report history endpoint for generated artifacts.

## 8. Component And Design-System Notes

The current stack is static HTML/CSS/vanilla JS. A framework rewrite is not required for the next product step. The recommended approach is a lightweight application shell using small vanilla JS modules.

### Recommended Frontend Structure

```text
apps/sandbox-ui/
  index.html
  styles.css
  sandbox.js
  app/
    api-client.js
    state-store.js
    router.js
    components/
      status-badge.js
      metric-card.js
      data-table.js
      stepper.js
      connector-card.js
      empty-state.js
      command-bar.js
    views/
      dashboard-view.js
      setup-view.js
      policies-view.js
      agents-view.js
      approvals-view.js
      evidence-view.js
      aispm-view.js
      reports-view.js
      integrations-view.js
      settings-view.js
```

### Design Tokens

Add/normalize tokens:

- `--status-ok`
- `--status-warn`
- `--status-danger`
- `--status-muted`
- `--surface-panel`
- `--surface-raised`
- `--border-subtle`
- `--text-primary`
- `--text-secondary`
- `--focus-ring`

### Component Rules

- Every metric card must show source, last refresh, and empty/error state.
- Every table must support empty state and error state.
- Every API-backed view must show connection status.
- Every destructive action must require confirmation and evidence reason.
- Every disabled Enterprise-only action must explain the boundary without looking broken.

### Framework Tradeoff

Stay vanilla for the next pass because:

- The app is already static-hostable.
- The current surface can be modularized without build tooling.
- It keeps Community easy to deploy through GitHub Pages, Azure Static Web Apps, Replit static hosting, and local Docker.

Consider a framework only after the operator console needs complex route-level state, authenticated tenant sessions, table virtualization, form schema rendering, or real-time collaboration.

## Prioritized Backlog

### P0: Blocks Calling This An Application

| Item | Outcome | Status |
| --- | --- | --- |
| Replace dashboard hero with stateful dashboard | Dashboard shows unconfigured/configured/degraded states from live API data. | Complete |
| Add shared API client and app state store | All live views use one consistent fetch/error/loading pattern. | Complete |
| Auto-load `/setup/status` on app start | App knows whether to show setup wizard or configured dashboard. | Complete |
| Build setup stepper | First-run setup becomes a guided workflow with status checks. | Complete |
| Add live dashboard widgets | Policy health, recent decisions, open approvals, evidence count, AISPM score, connector health. | Complete |
| Remove marketing routes from main app nav | Roadmap, trial funnel, use cases, long architecture explainer move to docs/product site/help. | Complete: primary navigation now stays operator-focused; Help contains application workflow cards plus secondary reference cards for architecture, use cases, role paths, trial, compliance, and roadmap deep links. |

### P1: Major Workflow Gaps

| Item | Outcome | Status |
| --- | --- | --- |
| Policies screen | Policy pack inventory, rule viewer, simulator, validation output. | Complete for catalog filters and simulator; rule editing/publish controls remain future API work. |
| Agents & MCP Trust screen | Agent registry, MCP server trust, capability classifications, unknown tool checks. | Complete for filters, selected detail, sample registry seeding, profile/classification references, MCP trust checks, and audit output; deeper connector actions remain future API work. |
| Approvals queue | Pending/approved/denied/expired queue with approve/deny/break-glass actions. | Complete for queue filters, detail view, approve/deny/expire/break-glass/deliver controls, sample seed action, and audit output. |
| Evidence hub | Search, filters, artifact listing, verification status, downloads. | Complete for search/filter, selected detail, verification status, AISPM evidence-reference correlation, copy/download JSON, and audit output; artifact bundle retrieval remains dependent on configured artifact root. |
| AISPM posture dashboard | Live posture, findings, control coverage, near misses, timeline, freshness. | Complete for live overview, findings, blockers, agent risk, timeline, and freshness; deeper control coverage and near-miss drilldowns remain future API work. |
| Report center | Date range, scope, export type, generated report history. | Complete for report type/range/scope/format controls, live source inventory, metric cards, JSON/Markdown/CSV previews, copy, and browser downloads; persisted report history and provider delivery remain future API work. |
| Integrations hub | Connector states, configure/test actions, error details. | Complete for live integration inventory, filters, sample seeding, selected detail, connector delivery dashboard, provider-boundary status, and safe delivery test output. |
| Settings and environment status | API connection, setup state, provider boundaries, storage modes, local UI controls, and diagnostics export. | Complete for API/version/setup/config state, provider and storage tables, theme/sidebar controls, local UI reset, and copy/download diagnostics. |

### P2: Polish

| Item | Outcome | Status |
| --- | --- | --- |
| Command palette becomes app command bar | Search routes plus run setup actions, refresh views, export reports. | Complete: `Ctrl+K` now searches pages/references and runs operator actions for refresh, setup validation/catalog tests, sample seeding, report preview/download, diagnostics export, sidebar state, and setup prompt. |
| Mobile operator view | Top nav/drawer optimized for dashboard, approvals, evidence, and posture. | Complete: phone layout now has a six-action bottom bar for Dashboard, Setup, Search, Approvals, Evidence, and AISPM plus a drawer-level operator action grid for refresh, setup validation, approval seeding, report generation, and diagnostics export. |
| Inline docs drawers | Keep helpful documentation without taking over primary workflow. | Complete: major operator routes now expose contextual Page Guide triggers that open an inline drawer with route-specific operator path, next actions, and related screen links. |
| Empty/error/loading states | Every live widget explains what to do next. | Complete for rebuilt live workstations: dashboard, setup, policies, AISPM, approvals, evidence, agents/MCP, integrations, reports, and settings render explicit loading, offline, empty, provider-boundary, or next-action states. |
| Accessibility pass | Keyboard focus, aria labels, table semantics, reduced-motion behavior. | Complete for closeout scope: route smoke verified named visible buttons, guide availability, command-palette keyboard focus, Escape close behavior, and no console errors across rebuilt primary routes. |
| Visual density pass | Reduce landing-page whitespace; increase table/widget density for workstation use. | Complete for operator console scope: rebuilt workstations use compact panels, filters, tables, summaries, mobile bottom actions, and validated no horizontal overflow across priority mobile routes. |

## Closeout QA

| Check | Result |
| --- | --- |
| Static JavaScript syntax | Passed with `node --check apps/sandbox-ui/sandbox.js`. |
| Visual regression smoke | Passed with `npm run validate:sandbox:visual`. |
| Desktop route activation | Passed across Dashboard, Setup, Policies, Agents/MCP, Approvals, Evidence, AISPM, Reports, Integrations, Settings, Help, and secondary references. |
| Contextual help | Passed: each rebuilt primary operator route has one `Page Guide` trigger. |
| Keyboard command bar | Passed: `Cmd/Ctrl+K` opens the command bar, focuses search, and renders command results. |
| Mobile priority workflow | Passed for Dashboard, Setup, Approvals, Evidence, AISPM, and Reports at `390x844`; no horizontal overflow observed. |
| Console errors | None observed during closeout smoke. |
