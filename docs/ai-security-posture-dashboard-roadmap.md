# CAVRA AI Security Posture Dashboard Roadmap

This roadmap defines the product direction for a CAVRA AI Security Posture
Management dashboard. The goal is to move beyond a basic evidence console into
a CSO/CISO-ready operating surface for live agent risk, runtime control,
governance, and audit evidence.

## Current Position

CAVRA Community Edition currently provides the public Evidence Console,
activity persistence for sessions and decisions, policy decision records,
evidence search, release readiness views, public-safe behavior fingerprints,
policy context gap detection, pre-action risk forecasts, intent-to-action
drift detection, tool-chain risk graphing, agent blast-radius mapping, control
coverage heatmap views, evidence confidence drilldowns, evidence freshness SLO
panels, deterministic executive risk narratives, replay-to-policy draft
previews, replay-to-policy test fixture previews, and a public-safe sandbox
portal. The Community dashboard also includes replay-to-policy review packets,
cross-platform CI gate readiness exports, production rollout checklists, rollout
audit packets, a human-readable CI gate rollout auditor view for public-safe
branch-protection governance, and a CSO Report Center with Community
downloadable executive, audit, control, evidence, and agent-risk reports.
That is enough to demonstrate the control model, but it is not yet a
production-grade real-time AI Security Posture Management dashboard.

CAVRA Enterprise is the right edition for live, authenticated, multi-tenant
dashboard capability. Enterprise should own production posture visibility,
centralized activity streams, runtime overrides, organization dashboards, and
customer-specific compliance workflows. Community should keep a public-safe
demo/local version using sample or local activity only.

## Recommendation Comparison

The proposed full AISPM dashboard adds important scope beyond the earlier
CAVRA dashboard recommendation.

| Capability area | Earlier CAVRA dashboard recommendation | Added AISPM recommendation | Roadmap decision |
| --- | --- | --- | --- |
| Agent activity | Live activity feed, agent inventory, session timeline | Prompts, reasoning, actions, Claude tool calls, execution traces | Include as first-class observability objects |
| Tool chain | Tool-call graph as Enterprise capability | Agent, tool, target, policy, edge, hotspot graph | Include public-safe local graph and private raw payload graph |
| Security posture | Policy decision stream, risk queue, violations | Risk classification, drift detection | Include risk scoring, posture drift, and violation triage |
| Governance | Approval latency and blocked-action tiles | Approval workflows, RBAC, guardrails | Include approval queue, RBAC scope, guardrail coverage |
| Audit and compliance | Drill-down evidence for every decision | Full trace replay, SOC 2-style logs, who approved what | Include immutable replay packets and approval lineage |
| Control plane | Enterprise live dashboard | Kill switch, policy toggle, runtime overrides | Include emergency controls with evidence and RBAC |

## Enterprise Dashboard Capabilities

### Agent Observability

- Live agent activity feed by repository, user, agent identity, tool, model,
  policy pack, and environment.
- Prompt, response, tool-call, file-action, shell-command, Git-operation, MCP,
  CI runner, and cloud/IaC action traces.
- Claude Code, Codex, GitHub Copilot coding agent, Cursor, Gemini CLI, MCP,
  and CI/CD adapter views as connector-specific trace sources.
- Execution timeline per session with ordered prompts, proposed actions,
  CAVRA decisions, approvals, tool results, and evidence references.
- Tool-call graph that shows which tool called which system, with latency,
  outcome, permission tier, and data sensitivity.
- Agent inventory with owner, repository scope, approved capabilities,
  last-seen time, drift status, current policy version, and coverage status.

### Security Posture

- Policy violation queue grouped by severity, repository, agent, control
  family, data class, and policy pack.
- Risk classification for proposed and completed actions, including blast
  radius, production impact, data exposure, credential exposure, and
  infrastructure-change risk.
- Pre-action risk forecasting for projected blast radius, likely impact,
  required controls, and private asset/dependency/identity enrichment.
- Drift detection for agent behavior, policy coverage, MCP tool inventory,
  repository guardrails, and approved capability profiles.
- Threat pattern detection for prompt injection, suspicious tool chaining,
  unpinned remote execution, unexpected data access, risky credential use, and
  policy-invisible context gaps.
- Risk posture score with trend, top contributors, unresolved findings,
  blocked actions, and approval latency.
- Executive risk narrative for CSO/CISO users that summarizes posture, top
  risks, evidence gaps, and recommended actions. Community provides a
  deterministic local/sample narrative; Enterprise should add AI-assisted
  board summaries, private trend history, tenant benchmarks, service
  criticality, and customer-impact context.

### Governance Layer

- Approval workflow dashboard showing pending, approved, denied, expired,
  escalated, and break-glass requests.
- RBAC-aware views for CSO/CISO, platform engineering, security engineering,
  auditor, repository owner, and developer personas.
- Guardrail coverage map for repositories, policy packs, CI gates, MCP servers,
  runtime modes, and enforcement backends.
- Organization policy toggles for audit-only, warn, enforce, strict regulated,
  and break-glass modes.
- Runtime override controls for emergency allow, emergency block, quarantine
  agent, quarantine tool, and rollback to safer policy version.

### Audit And Compliance

- Full trace replay for a governed agent session, including normalized
  decision requests, decisions, approver identity, evidence references, and
  final outcome.
- SOC 2-style immutable audit logs for policy decisions, approval actions,
  policy changes, override use, evidence access, and admin activity.
- "Who approved what" lineage linking actor, role, request, policy version,
  decision, timestamp, and evidence bundle.
- Compliance views for SOC 2, ISO 27001, NIST SSDF, EU AI Act, PCI DSS, SOX,
  HIPAA, and internal AI governance controls.
- Exportable incident packet for a single violation, session, agent, repository,
  or release window.

### Reporting And Delivery

- CSO/CISO report center for executive risk briefs, board KPI packs, SOC
  2-style audit summaries, ISO/NIST/EU AI Act evidence summaries, agent risk
  registers, control coverage workbooks, exception reports, evidence freshness
  exports, and incident packets.
- Community provides browser-generated Markdown, JSON, and CSV reports from
  public-safe sample or local metadata.
- Enterprise should add PDF, XLSX, DOCX, HTML, signed JSON, SIEM-ready JSONL,
  and GRC upload packages with tenant branding, charts, signatures, and
  immutable evidence references.
- Enterprise should support scheduled and on-demand email delivery through
  SMTP, Microsoft 365, Google Workspace, AWS SES, SendGrid, or private webhook
  providers.
- Enterprise delivery must support recipient allowlists, domain restrictions,
  RBAC, approval gates, DKIM/SPF/DMARC alignment, encryption options, delivery
  retries, bounce tracking, and delivery audit evidence.

### Control Plane

- CSO kill switch to disable an agent identity, tool, MCP server, repository
  scope, policy pack, or runtime connector.
- Policy toggle and rollout control with approval requirements, blast-radius
  preview, rollback plan, and evidence generation.
- Runtime overrides with expiration, owner, reason, evidence, and mandatory
  post-event review.
- Live policy distribution status for connected runtimes and CI enforcement
  points.
- Control-plane health for ingestion lag, event drops, connector errors,
  storage health, license state, and tenant isolation.

## Differentiated Observability Features

These features should help position CAVRA as more than another log dashboard:

- **Pre-action risk forecast**: before execution, show what CAVRA predicts the
  action could change, expose, or break.
- **Intent-to-action drift**: compare the user's stated request with each
  proposed action and flag behavior that no longer matches the original intent.
- **Tool-chain risk graph**: map agent, tool, target, policy, and edge hotspots so operators can see risky chained behavior before it becomes a blind spot.
- **Policy-invisible risk detector**: identify decisions that require missing
  business context, such as data owner, environment tier, customer region,
  change window, or system criticality.
- **Agent blast-radius map**: visualize which repositories, secrets, tools,
  cloud accounts, environments, and approval routes an agent could affect.
- **Evidence confidence score**: report whether each dashboard tile is backed
  by signed evidence, sampled evidence, connector metadata, or demo data.
- **Evidence confidence drilldown**: rank decision and session evidence as
  signed, activity-reference, sample, metadata-only, or missing before audit
  reliance.
- **Evidence freshness and retention SLO**: show stale evidence, missing
  timestamps, retention gaps, and archive-readiness boundaries.
- **Control coverage heatmap**: show where CAVRA is enforcing, warning,
  auditing only, or absent across repositories and agent tools.
- **Near-miss queue**: surface risky actions that were allowed with warnings,
  required approval, or narrowly avoided a block.
- **Behavior fingerprinting**: build baseline patterns per agent, repository,
  and workflow, then flag unusual cadence, tool sequences, access paths, or
  model/tool combinations.
- **Replay-to-policy authoring**: let operators convert a trace segment into a
  draft policy rule or policy test fixture. Community provides read-only
  metadata-derived draft previews; Enterprise should add private prompt,
  reasoning, ticket, asset, simulation, and approval-bound write-back context.
- **Executive risk narrative**: generate public-safe weekly posture summaries
  that explain material AI-agent risks, mitigations, unresolved actions, and
  audit evidence links.
- **CSO report center**: give executives and auditors one place to download or
  schedule decision-ready reports instead of searching through raw evidence,
  logs, and dashboards.

## Implementation Phases

### Phase A: Public-Safe Dashboard Contract

- Define dashboard schemas for agent events, trace steps, posture findings,
  risk scores, control coverage, approval lineage, and replay packets.
- Add Community sample data and documentation without exposing Enterprise
  logic, customer data, private policy packs, or license-service details.
- Document public/private edition boundaries.

### Phase B: Community Demo And Local Activity View

- Add a static-hostable dashboard route in the public portal using sample and
  local activity metadata.
- Show clear data provenance labels: sample, local, API-backed, or Enterprise.
- Add Community-safe control coverage and near-miss queues derived from local
  decisions so CSO/CISO users can see where enforcement, approval gates,
  warnings, and evidence exist without live Enterprise ingestion.
- Add public-safe trace replay packets derived from local decisions so
  operators can inspect sequence, risk, evidence references, and redaction
  status while raw prompts, reasoning, and tool output remain Enterprise.
- Add public-safe approval lineage derived from local approval records so
  operators can inspect state, approver group, decision linkage, timestamps,
  and evidence references while private IdP/RBAC context remains Enterprise.
- Add public-safe behavior fingerprints, policy context gaps, pre-action risk
  forecasts, intent-to-action drift, tool-chain risk graphing, agent blast-radius mapping, control coverage heatmap views, evidence confidence drilldowns, and evidence freshness SLO panels derived from
  normalized local decision metadata while private prompt-derived intent,
  workflow correlation, raw tool payloads, cross-system traces, private asset graphs,
  and semantic models remain Enterprise.
- Add public-safe replay-to-policy draft and test fixture previews derived
  from normalized block, require-approval, warning, high, and critical
  decisions while private prompt/reasoning/tool-payload authoring,
  ticket/asset enrichment, policy simulation, tenant-history regression, CI
  write-back, and automated policy write-back remain Enterprise.
- Add public-safe CI gate readiness, rollout checklist, rollout audit packet,
  and CI gate rollout auditor view so reviewers can confirm required checks,
  evidence attachments, platform coverage, and public/private automation
  boundaries before production branch-protection rollout.
- Keep live multi-tenant streaming, centralized retention, and organization
  controls locked to Enterprise.

### Phase C: Enterprise Live Ingestion

- Add private Enterprise ingestion for agent events, tool calls, prompts,
  decisions, approvals, evidence, MCP activity, CI runner events, and
  cloud/IaC actions.
- Support near-real-time updates through SSE or WebSocket transport.
- Persist normalized events with tenant isolation, retention, and audit
  integrity controls.
- Public-safe Phase C design and envelope contract are documented in
  `docs/architecture/aispm-enterprise-live-ingestion.md`. The public schema is
  `src/cavra/schemas/aispm-enterprise-live-ingestion-envelope.schema.json`, and
  the redacted example is
  `examples/aispm/enterprise-live-ingestion-envelope-public-contract.example.json`.

### Phase D: Enterprise CSO Console

- Build the authenticated CSO/CISO dashboard with posture score, live activity,
  violation queue, trace replay, approval lineage, control coverage, and
  control-plane health.
- Add RBAC-scoped views for security, platform, audit, and repository-owner
  roles.
- Add incident packet export and compliance evidence summaries.

### Phase E: Runtime Control Plane

- Add kill switch, quarantine, policy toggle, runtime override, and rollback
  controls with approval gates and immutable evidence.
- Add policy distribution status and runtime connector health.
- Validate controls through private Enterprise trial and paid-pilot evidence.

### Phase F: CSO Report Center And Delivery

- Add Community report downloads for executive risk briefs, board KPI packs,
  SOC 2-style audit summaries, control coverage CSV, evidence freshness CSV,
  and agent risk registers from public-safe sample or local metadata.
- Add Enterprise report service for PDF, XLSX, DOCX, HTML, signed JSON, JSONL,
  and GRC upload packages with tenant branding and immutable evidence links.
- Add Enterprise email delivery with SMTP or provider integration, recipient
  allowlists, RBAC, approval gates, delivery retry evidence, and delivery audit
  trails.
- Maintain the public-safe report delivery contract in
  `src/cavra/aispm_reports.py`,
  `src/cavra/schemas/aispm-report-delivery-contract.schema.json`, and
  `examples/aispm/enterprise-report-delivery-contract-public.example.json`.
- Maintain the public-safe report setup wizard contract in
  `src/cavra/schemas/aispm-report-setup-wizard-contract.schema.json` and
  `examples/aispm/enterprise-report-setup-wizard-contract-public.example.json`.
- Maintain the public-safe report delivery audit event contract in
  `src/cavra/schemas/aispm-report-delivery-audit-event.schema.json` and
  `examples/aispm/enterprise-report-delivery-audit-event-public.example.json`.
- Maintain the public-safe report operations dashboard contract in
  `src/cavra/schemas/aispm-report-operations-dashboard.schema.json` and
  `examples/aispm/enterprise-report-operations-dashboard-public.example.json`.
- Maintain the public-safe report retention lifecycle contract in
  `src/cavra/schemas/aispm-report-retention-lifecycle.schema.json` and
  `examples/aispm/enterprise-report-retention-lifecycle-public.example.json`.
- Maintain the public-safe report search and evidence retrieval contract in
  `src/cavra/schemas/aispm-report-search-retrieval.schema.json` and
  `examples/aispm/enterprise-report-search-retrieval-public.example.json`.
- Maintain the public-safe report export package manifest contract in
  `src/cavra/schemas/aispm-report-export-package-manifest.schema.json` and
  `examples/aispm/enterprise-report-export-package-manifest-public.example.json`.
- Maintain the public-safe report scheduling policy contract in
  `src/cavra/schemas/aispm-report-schedule-policy.schema.json` and
  `examples/aispm/enterprise-report-schedule-policy-public.example.json`.
- Maintain the public-safe report recipient policy contract in
  `src/cavra/schemas/aispm-report-recipient-policy.schema.json` and
  `examples/aispm/enterprise-report-recipient-policy-public.example.json`.
- Maintain the public-safe report approval decision contract in
  `src/cavra/schemas/aispm-report-approval-decision.schema.json` and
  `examples/aispm/enterprise-report-approval-decision-public.example.json`.
- Maintain the public-safe report exception lifecycle contract in
  `src/cavra/schemas/aispm-report-exception-lifecycle.schema.json` and
  `examples/aispm/enterprise-report-exception-lifecycle-public.example.json`.
- Maintain the public-safe report evidence room contract in
  `src/cavra/schemas/aispm-report-evidence-room.schema.json` and
  `examples/aispm/enterprise-report-evidence-room-public.example.json`.
- Maintain the public-safe report evidence room access event contract in
  `src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json` and
  `examples/aispm/enterprise-report-evidence-room-access-event-public.example.json`.
- Maintain the public-safe report incident packet contract in
  `src/cavra/schemas/aispm-report-incident-packet.schema.json` and
  `examples/aispm/enterprise-report-incident-packet-public.example.json`.
- Maintain the public-safe report incident closure contract in
  `src/cavra/schemas/aispm-report-incident-closure.schema.json` and
  `examples/aispm/enterprise-report-incident-closure-public.example.json`.
- Maintain the public-safe report KPI metrics contract in
  `src/cavra/schemas/aispm-report-kpi-metrics.schema.json` and
  `examples/aispm/enterprise-report-kpi-metrics-public.example.json`.
- Maintain the public-safe report alert escalation contract in
  `src/cavra/schemas/aispm-report-alert-escalation.schema.json` and
  `examples/aispm/enterprise-report-alert-escalation-public.example.json`.
- Maintain the public-safe report alert operations dashboard contract in
  `src/cavra/schemas/aispm-report-alert-operations-dashboard.schema.json` and
  `examples/aispm/enterprise-report-alert-operations-dashboard-public.example.json`.
- Maintain the public-safe report alert drilldown contract in
  `src/cavra/schemas/aispm-report-alert-drilldown.schema.json` and
  `examples/aispm/enterprise-report-alert-drilldown-public.example.json`.
- Maintain the public-safe report alert remediation plan contract in
  `src/cavra/schemas/aispm-report-alert-remediation-plan.schema.json` and
  `examples/aispm/enterprise-report-alert-remediation-plan-public.example.json`.
- Maintain the public-safe report alert remediation closure contract in
  `src/cavra/schemas/aispm-report-alert-remediation-closure.schema.json` and
  `examples/aispm/enterprise-report-alert-remediation-closure-public.example.json`.
- Maintain the public-safe remediation closure operations dashboard contract in
  `src/cavra/schemas/aispm-report-remediation-closure-operations-dashboard.schema.json` and
  `examples/aispm/enterprise-report-remediation-closure-operations-dashboard-public.example.json`.
- Maintain the public-safe remediation closure executive digest contract in
  `src/cavra/schemas/aispm-report-remediation-closure-executive-digest.schema.json` and
  `examples/aispm/enterprise-report-remediation-closure-executive-digest-public.example.json`.
- Maintain the public-safe remediation closure digest distribution contract in
  `src/cavra/schemas/aispm-report-remediation-closure-digest-distribution.schema.json` and
  `examples/aispm/enterprise-report-remediation-closure-digest-distribution-public.example.json`.
- Maintain the private implementation readiness checklist in
  `docs/architecture/aispm-report-center-enterprise-readiness.md` and
  `docs/wiki/AISPM-Report-Center-Enterprise-Readiness.md`.
- Maintain the public-safe Report Center Enterprise Trial validation packet in
  `src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json` and
  `examples/aispm/enterprise-report-center-trial-validation-packet-public.example.json`.
- Maintain the public-safe Report Center trial operator dashboard readiness
  contract in
  `src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json` and
  `examples/aispm/enterprise-report-center-trial-operator-dashboard-readiness-public.example.json`.
- Maintain the public-safe Report Center trial operator dashboard API/view-model
  contract in
  `src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json` and
  `examples/aispm/enterprise-report-center-trial-operator-api-view-model-public.example.json`.
- Maintain the public-safe Report Center trial evaluator handoff packet in
  `src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json` and
  `examples/aispm/enterprise-report-center-trial-evaluator-handoff-packet-public.example.json`.
- Maintain the public-safe Report Center trial revocation and expiry evidence
  contract in
  `src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json` and
  `examples/aispm/enterprise-report-center-trial-revocation-expiry-evidence-public.example.json`.
- Maintain the public-safe Report Center trial lab notebook outline contract in
  `src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json` and
  `examples/aispm/enterprise-report-center-trial-lab-notebook-outline-public.example.json`.
- Maintain the public-safe Report Center trial lab notebook publication
  readiness contract in
  `src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json` and
  `examples/aispm/enterprise-report-center-trial-lab-notebook-publication-readiness-public.example.json`.
- Surface an AISPM Enterprise Trial readiness checklist inside the CSO
  dashboard so reviewers can verify lab notebook, trial access portal,
  operator approval, revocation/expiry, release evidence, and Enterprise
  automation boundaries from one public-safe view.
- Add Community copy/download actions for a public-safe AISPM Enterprise Trial
  readiness summary and JSON packet that can be attached to evaluator,
  procurement, or security review tickets.
- Show the Enterprise Trial evaluator handoff in the AISPM dashboard: trial
  portal, package reference, license validation boundary, lab notebook,
  support path, and revocation/expiry closeout.
- Add an Enterprise Trial evaluation journey timeline for request submission,
  operator approval, package pull, license validation, scenario execution,
  evidence review, and revocation closeout.
- Add an AISPM Trial Closeout Evidence panel for license expiry, revocation
  check, package access removal, blocked runtime validation, archived evidence
  packet, and evaluator feedback collection.
- Add an AISPM Trial Feedback Intake model for setup friction, policy clarity,
  dashboard usefulness, report usefulness, integration gaps, procurement
  concerns, and go/no-go decision capture.
- Add an AISPM Trial Outcome Summary roll-up for readiness, evaluator handoff,
  evaluation journey, closeout evidence, feedback coverage, and CSO/CISO
  go/no-go review.
- Add a public-safe AISPM Trial Review Packet export that bundles readiness,
  evaluator handoff, evaluation journey, closeout evidence, feedback intake,
  and outcome summary into one JSON artifact for CSO/CISO or procurement
  review.
- Add an AISPM Trial Review Packet Integrity panel for schema version,
  generated timestamp, expected filename, public-safety boundary, excluded
  private fields, and Enterprise-only boundary signals.
- Add an AISPM Trial Procurement Readiness panel that translates trial outcome
  evidence into buyer review areas: legal, security, deployment, support,
  licensing, data handling, and production pilot scope.
- Add an AISPM Trial Pilot Scope Builder panel for target repositories, AI
  agents, required checks, policies, evidence owners, success criteria, and
  go/no-go date.
- Add a public-safe AISPM Trial Pilot Scope Packet export for attaching the
  pilot definition to internal pilot approval tickets.
- Add an AISPM Pilot Approval Checklist for owner assignment, repository
  selection, agent registration, required checks, policy selection, evidence
  owner assignment, support path confirmation, and go/no-go acceptance before a
  production pilot starts.
- Add a public-safe AISPM Pilot Approval Packet export that bundles the pilot
  scope packet reference and final approval gates into
  `cavra-aispm-pilot-approval-packet.json` for production-pilot approval
  records.
- Add an AISPM Pilot Launch Readiness Summary that rolls pilot scope,
  approval packet, CSO reports, trial review evidence, support confirmation,
  and CSO/CISO go/no-go readiness into one launch-candidate view.
- Add a public-safe AISPM Pilot Launch Decision Packet export that packages the
  launch readiness summary, source artifact references, public-safety boundary,
  and Enterprise-only signed approval/write-back boundaries into
  `cavra-aispm-pilot-launch-decision-packet.json`.
- Add a Production Pilot Evidence Room view that groups pilot artifacts for
  CSO/CISO, security, platform, procurement, auditor, and operator review while
  keeping authenticated access, retention, and signed activity logs as
  Enterprise-only capabilities.
- Add a public-safe Production Pilot Evidence Room Packet export that packages
  the role-based reviewer catalog, source artifacts, public-safety boundary,
  and Enterprise-only evidence room capabilities into
  `cavra-aispm-pilot-evidence-room-packet.json`.
- Add an Evidence Room Reviewer Checklist with pre-pilot acceptance criteria
  for CSO/CISO, security, platform, procurement, auditor, and operator review
  while keeping signed acceptance as an Enterprise-only workflow.
- Add a public-safe Evidence Room Reviewer Checklist Packet export that
  packages role-based acceptance criteria, source artifact references,
  public-safety boundary, and Enterprise-only signed acceptance boundaries into
  `cavra-aispm-evidence-reviewer-checklist-packet.json`.
- Add a Pilot Exception Register that shows unresolved risks and accepted
  exceptions with owner, status, expiry expectation, and Enterprise-only
  exception workflow boundaries before production pilot launch.
- Add a public-safe Pilot Exception Register Packet export that packages
  unresolved risks, accepted exceptions, source artifact references,
  public-safety boundary, and Enterprise-only exception lifecycle boundaries
  into `cavra-aispm-pilot-exception-register-packet.json`.
- Add a Pilot Risk Acceptance Summary that rolls up open exceptions, accepted
  risks, monitored risks, accountable owners, launch-blocking items, and the
  Enterprise-only signed risk acceptance boundary for CSO/CISO approval.
- Add a public-safe Pilot Risk Acceptance Packet export that packages the
  CSO/CISO risk roll-up, source artifact references, public-safety boundary,
  and Enterprise-only signed risk acceptance boundaries into
  `cavra-aispm-pilot-risk-acceptance-packet.json`.
- Add a Pilot Launch Board Pack view that groups the launch decision, evidence
  room, risk acceptance, exception register, reviewer checklist, and executive
  report artifacts into one board/CISO-ready review surface while keeping
  signed board approval, minutes, PDF generation, and delivery workflow as
  Enterprise-only capabilities.
- Add a public-safe Pilot Launch Board Pack Packet export that packages the
  board/CISO artifact index, freshness gate, integrity summary, source artifact
  references, and Enterprise-only approval/delivery boundaries into
  `cavra-aispm-pilot-launch-board-pack-packet.json`.
- Maintain the board-pack artifact index in
  `docs/release-verifications/aispm-launch-board-pack-artifact-index.json` and
  gate freshness with `scripts/validate-aispm-launch-artifacts.py` so launch
  decision, evidence-room, risk-acceptance, exception-register, reviewer
  checklist, and CSO report artifacts cannot drift silently.
- Maintain the AISPM launch readiness rollup in
  `docs/release-verifications/aispm-launch-readiness-rollup.md` and
  `docs/release-verifications/aispm-launch-readiness-rollup.json`, and gate it
  with `scripts/validate-aispm-launch-readiness.py` so Phase B closeout,
  board-pack freshness, Playwright visual smoke, trial lab notebook readiness,
  and GitHub Pages workflow validation stay aligned.
- Validate the deployed GitHub Pages experience with
  `docs/release-verifications/hosted-sandbox-pages-smoke-validation.md`,
  `docs/release-verifications/hosted-sandbox-pages-smoke-validation.json`, and
  `scripts/validate-hosted-sandbox-pages.mjs` so the live `#dashboard` and
  `#ai-posture` routes are browser-rendered after publication.
- Track hosted GitHub Pages deployment freshness with
  `docs/release-verifications/hosted-sandbox-deployment-freshness.md`,
  `docs/release-verifications/hosted-sandbox-deployment-freshness.json`, and
  `scripts/validate-hosted-sandbox-deployment-freshness.py` using the build
  sentinel `community-v1.0.0-aispm-release-evidence-index` so stale hosted
  Pages content is reported separately from local release readiness.
- Publish hosted release operator status in
  `docs/release-verifications/hosted-sandbox-operator-release-status.md` and
  `docs/release-verifications/hosted-sandbox-operator-release-status.json`,
  validate it with `scripts/validate-hosted-sandbox-operator-status.py`, and
  expose the public portal export as
  `cavra-hosted-sandbox-operator-status-packet.json` so release operators have
  a clear go/no-go view before external announcement.
- Generate post-deploy evidence after hosted smoke with
  `scripts/generate-hosted-sandbox-deploy-evidence.py`, validate the contract
  with `scripts/validate-hosted-sandbox-deploy-evidence.py`, document it in
  `docs/release-verifications/hosted-sandbox-post-deploy-evidence.md` and
  `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json`, and
  upload it as `cavra-hosted-sandbox-post-deploy-evidence`.
- Publish a reviewer-facing AISPM Release Evidence Index in
  `docs/release-verifications/aispm-release-evidence-index.md` and
  `docs/release-verifications/aispm-release-evidence-index.json`, validate it
  with `scripts/validate-aispm-release-evidence-index.py`, and expose the
  public portal export as `cavra-aispm-release-evidence-index-packet.json`.
- Track AISPM report catalog readiness in
  `docs/release-verifications/aispm-report-catalog-readiness.md` and
  `docs/release-verifications/aispm-report-catalog-readiness.json`, validate it
  with `scripts/validate-aispm-report-catalog-readiness.py`, and expose the
  public portal export as `cavra-aispm-report-catalog-packet.json` so CSO/CISO,
  audit, procurement, and release reviewers can verify Community downloads and
  Enterprise-only report delivery boundaries.
- Track AISPM report delivery setup readiness in
  `docs/release-verifications/aispm-report-delivery-setup-readiness.md` and
  `docs/release-verifications/aispm-report-delivery-setup-readiness.json`,
  validate it with
  `scripts/validate-aispm-report-delivery-setup-readiness.py`, and expose the
  public portal export as `cavra-aispm-report-delivery-setup-packet.json` so
  Enterprise trial operators and tenant admins can verify sender identity,
  delivery provider, recipient governance, schedules, retention, and audit
  evidence boundaries before enabling report delivery.
- Track AISPM report operations readiness in
  `docs/release-verifications/aispm-report-operations-readiness.md` and
  `docs/release-verifications/aispm-report-operations-readiness.json`,
  validate it with
  `scripts/validate-aispm-report-operations-readiness.py`, and expose the
  public portal export as
  `cavra-aispm-report-operations-readiness-packet.json` so Enterprise delivery
  audit events, operations health, retention lifecycle, RBAC-scoped
  search/retrieval, and signed export package manifest readiness are visible
  without exposing raw report payloads, provider responses, customer records, or
  signed download URLs.
- Track AISPM report governance readiness in
  `docs/release-verifications/aispm-report-governance-readiness.md` and
  `docs/release-verifications/aispm-report-governance-readiness.json`,
  validate it with
  `scripts/validate-aispm-report-governance-readiness.py`, and expose the
  public portal export as
  `cavra-aispm-report-governance-readiness-packet.json` so Enterprise schedule
  policy, recipient policy, approval decisions, exception lifecycle, and
  evidence-room readiness are visible without exposing identities, recipient
  addresses, private justifications, raw report content, or signed download
  URLs.
- Track AISPM report assurance readiness in
  `docs/release-verifications/aispm-report-assurance-readiness.md` and
  `docs/release-verifications/aispm-report-assurance-readiness.json`,
  validate it with
  `scripts/validate-aispm-report-assurance-readiness.py`, and expose the
  public portal export as
  `cavra-aispm-report-assurance-readiness-packet.json` so Enterprise
  evidence-room access events, incident packets, incident closure, KPI metrics,
  and alert escalation readiness are visible without exposing identities, IP
  addresses, raw report content, private remediation details, tenant
  drilldowns, signed URLs, or customer records.
- Track AISPM report response readiness in
  `docs/release-verifications/aispm-report-response-readiness.md` and
  `docs/release-verifications/aispm-report-response-readiness.json`, validate
  it with `scripts/validate-aispm-report-response-readiness.py`, and expose
  the public portal export as
  `cavra-aispm-report-response-readiness-packet.json` so Enterprise alert
  operations dashboards, alert drilldowns, remediation plans, remediation
  closure, and closure operations readiness are visible without exposing
  assignee identities, tenant alert records, raw report payloads, private
  remediation tasks, customer records, signed URLs, or provider responses.
- Track AISPM report trial operations readiness in
  `docs/release-verifications/aispm-report-trial-operations-readiness.md` and
  `docs/release-verifications/aispm-report-trial-operations-readiness.json`,
  validate it with
  `scripts/validate-aispm-report-trial-operations-readiness.py`, and expose the
  public portal export as
  `cavra-aispm-report-trial-operations-readiness-packet.json` so Enterprise
  executive digest, digest distribution, trial validation packet, trial
  operator dashboard, and operator API/view-model readiness are visible without
  exposing evaluator identities, operator identities, package tokens, license
  keys, raw prompts, model reasoning, raw report content, provider responses,
  customer records, or Enterprise source.
- Track AISPM pilot control readiness in
  `docs/release-verifications/aispm-pilot-control-readiness.md` and
  `docs/release-verifications/aispm-pilot-control-readiness.json`, validate it
  with `scripts/validate-aispm-pilot-control-readiness.py`, and expose the
  public portal export as `cavra-aispm-pilot-control-readiness-packet.json` so
  production-pilot exception, risk acceptance, board pack, artifact freshness,
  and launch-rollup controls are visible without exposing signed approvals,
  board minutes, private telemetry, customer records, license keys, private
  package tokens, Enterprise source, or tenant workflow state.
- Track Community AISPM v1.0 public release readiness in
  `docs/release-verifications/aispm-v1.0-public-release-readiness.md` and
  `docs/release-verifications/aispm-v1.0-public-release-readiness.json`,
  validate it with `scripts/validate-aispm-v100-public-release.py`, publish
  AISPM-specific release notes in `docs/releases/community-v1.0.0-aispm.md`,
  and maintain the evaluator walkthrough in
  `docs/aispm-v1.0-public-walkthrough.md`.
- Track final public announcement readiness in
  `docs/release-verifications/aispm-final-announcement-readiness.md` and
  `docs/release-verifications/aispm-final-announcement-readiness.json`,
  validate it with `scripts/validate-aispm-final-announcement-readiness.py`,
  and export the portal packet as
  `cavra-aispm-final-announcement-readiness-packet.json`.
- During CAVRA setup, collect organization-specific report delivery settings:
  report sender address, allowed recipient domains, SMTP/provider mode,
  encrypted credential references, default report schedule, timezone, branding,
  legal footer, and report retention policy.

### Phase G: CAVRA Trial Field Guide

- After all AISPM phases reach production-ready status, create a GitHub Wiki
  handbook named **CAVRA Trial Field Guide** for trial users and enterprise
  evaluators. It should walk through the complete CAVRA product from signup,
  installation, policy evaluation, AI-agent enforcement, AISPM dashboard use,
  evidence review, approval flows, replay-to-policy authoring, and Enterprise
  trial operation.
- Include step-by-step guided labs with screenshots, diagrams, flow charts,
  expected outputs, troubleshooting notes, and role-specific paths for
  developers, platform teams, auditors, security engineers, and CSO/CISO users.
- Keep the Field Guide public-safe: no Enterprise source code, license
  secrets, private keys, customer data, or private policy-pack implementation
  details.
- Generate the Field Guide from the validated public-safe outline contract so
  chapters, screenshots, diagrams, flow charts, role paths, and verification
  checkpoints remain aligned with release evidence.
- Gate Wiki publication through the validated public-safe publication readiness
  contract so navigation, link health, redacted assets, checkpoint evidence,
  and required reviews are complete before external evaluators use the labs.
- Validate the Wiki Field Guide publication gate with
  `scripts/validate-aispm-trial-lab-notebook.py` so referenced lab pages exist,
  appear in `docs/wiki/Home.md`, include public-safety sections, and remain
  aligned with the readiness packet.
- Run the Field Guide publication validator in `.github/workflows/community-ci.yml`
  and `.github/workflows/release-community.yml` so future Community changes and
  release tags cannot publish stale or unsafe trial handbook references.
- Publish reviewer-facing readiness summaries in
  `docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md`
  and
  `docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json`
  with page, navigation, public-safety, visual-asset, acceptance-criteria, and
  blocker rollups.

## Acceptance Criteria

- Community shows a useful public-safe posture dashboard demo without claiming
  production live monitoring.
- Enterprise shows authenticated live activity, policy decisions, violations,
  risk posture, and execution timelines from real agent workflows.
- Every dashboard tile identifies data provenance and evidence confidence.
- Every kill switch, override, approval, and policy toggle emits immutable
  audit evidence.
- Trace replay can reconstruct prompts, tool calls, actions, CAVRA decisions,
  approvals, and outcomes for a session.
- Documentation explains what is Community, Enterprise, SaaS, and private-only.

## Phase B Closeout Packet

The public-safe Community Phase B closeout packet is maintained at
`docs/aispm-phase-b-closeout-verification.md`. It records the verified
dashboard scope, validation commands, browser render checks, public-safety
boundaries, and the remaining Enterprise handoff into Phase C.
