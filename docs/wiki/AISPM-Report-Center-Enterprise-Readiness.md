# AISPM Report Center Enterprise Readiness

This page maps the public AISPM CSO Report Center contracts to the private
`cavra-enterprise` implementation work needed before Enterprise Trial and GA
reporting workflows are ready for external evaluators. It is public-safe: it
documents services, APIs, workers, stores, controls, and validation evidence
without exposing Enterprise source code, tenant data, provider credentials, or
report payloads.

## Readiness Goal

Enterprise Report Center is ready when a tenant can configure report delivery,
render report packages from live AISPM metadata, enforce RBAC and recipient
governance, require approval before sensitive sends, deliver via portal/email/
GRC paths, retain immutable evidence, and validate the complete flow in the
Enterprise Trial package.

## Private Module Map

Recommended private package layout:

```text
src/cavra_enterprise/aispm_reports/
  api.py
  catalog.py
  renderer.py
  setup.py
  delivery.py
  delivery_providers/
  scheduler.py
  audit.py
  retention.py
  retrieval.py
  export_packages.py
  recipients.py
  approvals.py
  exceptions.py
  evidence_rooms.py
  incidents.py
  kpi_metrics.py
  alerts.py
  remediation.py
  distribution.py
  trial_validation.py
```

## Contract-To-Implementation Map

| Contract area | Private implementation | Required evidence |
| --- | --- | --- |
| Report delivery | Catalog, render, send, deliveries, and schedules APIs | Render, send, block, retry, and delivery-audit evidence |
| Setup wizard | Tenant report settings, provider references, branding, retention | Settings saved without raw credential values in evidence |
| Delivery audit | Immutable report action event writer | Every render/send/schedule/test action has digest and evidence refs |
| Operations dashboard | Delivery health projection worker | Failed delivery, retry, schedule, and provider health projections |
| Retention lifecycle | Retention, archive, hold, and deletion worker | Archive, hold, expiry, and deletion-readiness evidence |
| Search/retrieval | Report metadata index and retrieval APIs | RBAC and retention-aware search with audit events |
| Export manifest | Signed package manifest builder | Artifact digests, evidence refs, retention class, and manifest refs |
| Schedule policy | Scheduler and blackout-window evaluator | Scheduled, skipped, blocked, and retry run evidence |
| Recipient policy | Domain allowlist and channel eligibility evaluator | External recipients blocked until policy and approval pass |
| Approval decisions | Approval request and decision workflow | Immutable approval evidence for sends, schedules, and domains |
| Exceptions | Exception expiry, renewal, revocation, and closure workflow | Evidence-backed exception lifecycle events |
| Evidence rooms | Scoped auditor access package worker | Expiring, watermarked, revocable access with access logs |
| Evidence room access events | Immutable room event writer | View, download, revoke, expiry, and failed-policy events |
| Incident packets | Incident packet builder | Exceptions, approvals, access events, and evidence refs |
| Incident closure | Closure workflow and follow-up task store | Closure blocked until remediation and follow-up evidence exist |
| KPI metrics | Aggregate KPI projection worker | Delivery health, approval latency, SLO, and audit readiness metrics |
| Alert escalation | Alert evaluator, router, and acknowledgement workflow | Routed alert with due time, acknowledgement, and incident linkage |
| Alert operations | Alert dashboard projection worker | Active alerts, suppressions, routing health, and overdue acknowledgement |
| Alert drilldown | Single-alert timeline API | Alert timeline, routed roles, incident refs, and evidence chain |
| Alert remediation plan | Owner-scoped task and control update workflow | Task, approval, due-date, and closure-criteria evidence |
| Alert remediation closure | Final closure workflow | Completed tasks, final approval, residual risk, and closure evidence |
| Closure operations dashboard | Closure throughput and SLO projection worker | Closure rate, bottlenecks, residual-risk aging, and dashboard evidence |
| Executive digest | Board-pack renderer | Public-safe talking points, audit readiness, and digest evidence |
| Digest distribution | Distribution worker | Approval-before-send, delivery readiness, signed manifest, and immutable send evidence |

## Minimum Private APIs

- `GET /enterprise/aispm/reports/catalog`
- `POST /enterprise/aispm/reports/render`
- `POST /enterprise/aispm/reports/send`
- `GET /enterprise/aispm/reports/deliveries`
- `POST /enterprise/aispm/reports/schedules`
- `POST /enterprise/aispm/reports/search`
- `POST /enterprise/aispm/reports/evidence-rooms`
- `POST /enterprise/aispm/reports/alerts/{alert_ref}/acknowledge`
- `POST /enterprise/aispm/reports/remediation/{plan_ref}/close`
- `POST /enterprise/aispm/reports/distributions/{distribution_ref}/approve`

## Enterprise Trial Validation Paths

| Trial path | Expected proof |
| --- | --- |
| Setup wizard | Tenant settings saved with provider references only. |
| Render report | Report artifact metadata includes digest and retention class. |
| Policy-blocked send | Missing approval or invalid recipient blocks delivery. |
| Approved send | Delivery creates immutable send evidence and audit event. |
| Schedule run | Schedule honors blackout and retry policy. |
| Evidence room | Scoped room logs view/download, revoke, and expiry events. |
| Alert escalation | SLO breach routes an alert and requires acknowledgement. |
| Remediation closure | Closure requires completed tasks, approval, and closure evidence. |
| Executive digest distribution | Email waits for approval; portal/GRC packages are ready. |
| Revocation and retention | Revoked or expired artifacts cannot be retrieved. |

The public-safe trial validation packet is packaged at
`src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json`,
with a redacted example at
`examples/aispm/enterprise-report-center-trial-validation-packet-public.example.json`.

The trial operator dashboard readiness contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json`,
with a redacted example at
`examples/aispm/enterprise-report-center-trial-operator-dashboard-readiness-public.example.json`.
The trial operator dashboard API/view-model contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json`,
with a redacted example at
`examples/aispm/enterprise-report-center-trial-operator-api-view-model-public.example.json`.
The trial evaluator handoff packet contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json`,
with a redacted example at
`examples/aispm/enterprise-report-center-trial-evaluator-handoff-packet-public.example.json`.
The trial revocation and expiry evidence contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json`,
with a redacted example at
`examples/aispm/enterprise-report-center-trial-revocation-expiry-evidence-public.example.json`.
The trial lab notebook outline contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json`,
with a redacted example at
`examples/aispm/enterprise-report-center-trial-lab-notebook-outline-public.example.json`.
The trial lab notebook publication readiness contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json`,
with a redacted example at
`examples/aispm/enterprise-report-center-trial-lab-notebook-publication-readiness-public.example.json`.

## Release Acceptance

- Private Enterprise output fixtures validate against every public schema.
- Trial lab notebook publication readiness verifies Wiki navigation, link
  health, redacted assets, checkpoint evidence, and required reviews before
  public Wiki publication.
- Trial evidence excludes raw prompts, model reasoning, raw tool output,
  customer records, recipient addresses, IP addresses, provider responses,
  private remediation details, tenant drilldown records, and credential values.
- Every render, send, retry, approval, exception, access, alert, remediation,
  closure, and distribution event has an evidence ref.
- Operator dashboards show delivery health, retry health, evidence-room
  activity, alert status, remediation closure, and distribution readiness.
- Operator dashboard readiness summarizes validation status, blockers,
  evidence links, operator actions, and evaluator handoff without exposing
  private trial details.
- Operator dashboard API/view-model output maps readiness packets to
  authenticated private portal routes, UI sections, approval actions, state
  transitions, and immutable audit events.
- Evaluator handoff packets expose setup steps, package access status, trial
  license status, support state, expiry, and revocation posture without
  exposing package URLs, license keys, identities, secrets, or source code.
- Revocation and expiry evidence proves license validation, package access,
  trial portal access, report rendering, and support handoff are blocked after
  revocation or expiry.
- Lab notebook outlines define public-safe chapters, role paths, labs,
  screenshots, diagrams, flow charts, and verification checkpoints for the
  future Wiki trial textbook.
- Trial evaluators can complete setup, render, approval, send, evidence-room,
  alert, closure, digest, and distribution workflows without operator shell
  access.

## Public Boundary

The Community repository keeps public schemas, redacted examples, public docs,
trial usage instructions, and readiness checklists. Private Enterprise owns
renderers, delivery providers, schedulers, tenant stores, audit stores,
approval workflows, evidence-room workers, alert evaluators, remediation
workers, distribution workers, license enforcement, and SaaS persistence.
