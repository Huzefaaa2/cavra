# AISPM Report Center Enterprise Readiness Checklist

This checklist turns the public AISPM CSO Report Center contracts into an
implementation plan for the private `cavra-enterprise` repository. It is
public-safe by design: it names required services, APIs, workers, stores, and
validation evidence without shipping Enterprise source code, tenant data,
provider credentials, customer records, or report payloads.

## Readiness Goal

Enterprise Report Center is ready for trial evaluators when a tenant can:

1. Configure organization report settings and delivery providers through
   tenant-scoped setup.
2. Render report packages from live AISPM posture, alert, evidence, and
   remediation metadata.
3. Apply recipient governance, RBAC, approval gates, retention policy, and
   exception lifecycle rules before delivery.
4. Deliver report packages through portal, email, and GRC upload paths with
   immutable delivery and retry evidence.
5. Search, retrieve, expire, archive, revoke, and audit every report artifact
   through tenant-scoped controls.
6. Validate the flow in Enterprise Trial without exposing private
   implementation details in the public Community repository.

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

## Contract-To-Implementation Matrix

| Public contract | Private API or worker | Private store | Governance gate | Trial validation evidence |
| --- | --- | --- | --- | --- |
| `aispm-report-delivery-contract.schema.json` | `GET /enterprise/aispm/reports/catalog`, `POST /enterprise/aispm/reports/render`, `POST /enterprise/aispm/reports/send` | Report catalog, render job, delivery job | Tenant RBAC, license entitlement, recipient policy | Catalog loads, render succeeds, send blocked until policy passes |
| `aispm-report-setup-wizard-contract.schema.json` | `GET/PUT /enterprise/aispm/reports/setup` | Tenant report settings, provider references | Admin role, setting validation, secret-manager references only | Fresh tenant can save settings without raw credentials in evidence |
| `aispm-report-delivery-audit-event.schema.json` | Delivery event writer | Immutable report audit event store | Every render/send/schedule/test event must emit evidence | Delivery event chain has action, status, digest, and immutable ref |
| `aispm-report-operations-dashboard.schema.json` | Operations dashboard projection worker | Delivery health projection store | RBAC-scoped dashboard access | Failed delivery, retry, schedule, and provider health projections render |
| `aispm-report-retention-lifecycle.schema.json` | Retention lifecycle worker | Retention policy, archive, legal hold, deletion queue | Retention policy, legal hold approval | Archive, hold, expiry, and deletion readiness produce evidence |
| `aispm-report-search-retrieval.schema.json` | `POST /enterprise/aispm/reports/search`, `GET /enterprise/aispm/reports/{id}` | Report index, artifact reference store | RBAC, retention, evidence-room scope | Search excludes expired/revoked artifacts and records audit events |
| `aispm-report-export-package-manifest.schema.json` | Export package builder | Artifact manifest and digest store | Signed manifest required before download or upload | Package manifest includes digests, evidence refs, and retention class |
| `aispm-report-schedule-policy.schema.json` | Scheduler and schedule evaluator | Schedule policy store, run history | Blackout windows, approval gates, recipient policy | Scheduled run respects blackout and retry policy |
| `aispm-report-recipient-policy.schema.json` | Recipient policy evaluator | Recipient policy and domain allowlist store | Domain allowlist, RBAC, channel eligibility | External recipient blocked until policy and approval gates pass |
| `aispm-report-approval-decision.schema.json` | Approval workflow worker | Approval request and decision store | Approver role, due time, immutable decision | Send, schedule change, and domain change approvals produce evidence |
| `aispm-report-exception-lifecycle.schema.json` | Exception lifecycle worker | Exception request, renewal, revocation, closure store | Expiry, renewal approval, revocation control | Exception expires, renews, revokes, and closes with evidence |
| `aispm-report-evidence-room.schema.json` | Evidence room API | Evidence room, scoped artifact access, watermark state | Expiring access, RBAC, watermark policy | Auditor access is scoped, expiring, watermarked, and revocable |
| `aispm-report-evidence-room-access-event.schema.json` | Evidence room access event writer | Immutable room access log | Access, download, revoke, expiry, failed policy events | Every room action has digest-chain refs and no private identities |
| `aispm-report-incident-packet.schema.json` | Incident packet builder | Incident packet and chain-of-custody store | Incident review state and artifact scope | Incident packet links exceptions, approvals, events, and evidence refs |
| `aispm-report-incident-closure.schema.json` | Incident closure workflow | Incident closure, lessons, follow-up task store | Closure approval, follow-up evidence | Incident cannot close until remediation and follow-up evidence are present |
| `aispm-report-kpi-metrics.schema.json` | KPI aggregation worker | Aggregate KPI projection store | Tenant aggregation only, no tenant drilldown in public evidence | KPI metrics render for delivery health, approval latency, SLOs, and audit readiness |
| `aispm-report-alert-escalation.schema.json` | Alert evaluator and router | Alert event, route, acknowledgement store | Severity, escalation ladder, duplicate suppression | Failed delivery spike routes alert and waits for acknowledgement |
| `aispm-report-alert-operations-dashboard.schema.json` | Alert dashboard projection worker | Alert operations projection store | RBAC-scoped operations access | Active alerts, overdue acknowledgement, suppression, and routing health render |
| `aispm-report-alert-drilldown.schema.json` | Alert drilldown API | Alert timeline and evidence-chain store | Single-alert RBAC and redaction policy | Alert timeline shows routed owner roles without private identities |
| `aispm-report-alert-remediation-plan.schema.json` | Alert remediation workflow | Remediation plan, task, control update store | Owner-scoped tasks, approval gates, due dates | Tasks, control updates, and closure criteria are evidence-backed |
| `aispm-report-alert-remediation-closure.schema.json` | Alert remediation closure workflow | Closure event and residual-risk store | Final approval, residual-risk acceptance, post-incident review | Closure requires completed tasks, final approval, and immutable evidence |
| `aispm-report-remediation-closure-operations-dashboard.schema.json` | Closure operations dashboard worker | Closure operations projection store | SLO policy, RBAC, retention-aware dashboard | Closure throughput, residual-risk aging, bottlenecks, and SLOs render |
| `aispm-report-remediation-closure-executive-digest.schema.json` | Executive digest renderer | Digest package and board-pack metadata store | Executive approval and recipient policy | Board-ready digest renders with public-safe talking points and evidence refs |
| `aispm-report-remediation-closure-digest-distribution.schema.json` | Digest distribution worker | Distribution job, send evidence, provider delivery state | Approval-before-send, recipient policy, signed manifest | Email remains blocked before approval; portal/GRC packages are ready with immutable send evidence |

## Private API Readiness

Minimum private API surface:

| API | Purpose | Required controls |
| --- | --- | --- |
| `GET /enterprise/aispm/reports/catalog` | List available Community and Enterprise report definitions. | Tenant entitlement, role-based visibility. |
| `POST /enterprise/aispm/reports/render` | Start a report render job for supported formats. | Tenant scope, report authorization, retention class. |
| `POST /enterprise/aispm/reports/send` | Deliver an approved report package. | Approval-before-send, recipient policy, delivery audit. |
| `GET /enterprise/aispm/reports/deliveries` | Query delivery history and retries. | RBAC, immutable audit refs. |
| `POST /enterprise/aispm/reports/schedules` | Create governed recurring report schedules. | Schedule policy, blackout windows, recipient policy. |
| `POST /enterprise/aispm/reports/search` | Search retained report metadata and evidence refs. | RBAC, retention, evidence-room scope. |
| `POST /enterprise/aispm/reports/evidence-rooms` | Create scoped auditor access packages. | Expiry, watermarking, revocation, access audit. |
| `POST /enterprise/aispm/reports/alerts/{alert_ref}/acknowledge` | Acknowledge report-center alerts. | Owner role, acknowledgement SLO, immutable event. |
| `POST /enterprise/aispm/reports/remediation/{plan_ref}/close` | Close remediation plans. | Completed tasks, final approval, residual-risk state. |
| `POST /enterprise/aispm/reports/distributions/{distribution_ref}/approve` | Approve executive digest distribution. | CISO/CSO role, due time, immutable approval evidence. |

## Worker Readiness

Required private workers:

| Worker | Input | Output evidence |
| --- | --- | --- |
| Report renderer | Report request, tenant posture metadata, format request | Render job evidence, artifact digest, retention class |
| Delivery worker | Approved delivery job, provider reference, recipient policy | Delivery event, provider status summary, retry state |
| Schedule runner | Schedule policy, blackout calendar, recipient policy | Scheduled run evidence, skipped/blocked run evidence |
| Retention worker | Retention policy, artifact metadata, legal hold state | Archive, expiry, deletion-readiness, and hold evidence |
| Search indexer | Report metadata, artifact refs, evidence refs | Search index update evidence |
| Export package builder | Report artifacts, manifest requirements | Signed manifest, artifact digest list, package evidence |
| Evidence room worker | Scoped artifact list, auditor access policy | Room package, watermark evidence, access expiry |
| KPI aggregator | Delivery, approval, incident, exception, and access events | Aggregate KPI packet with no tenant drilldown records |
| Alert evaluator | KPI and operations dashboard signals | Alert event, route, acknowledgement due time |
| Remediation worker | Alert drilldown, tasks, approval gates | Plan evidence, closure evidence, residual-risk evidence |
| Digest distribution worker | Executive digest, recipient policy, approval state | Approval-before-send evidence, delivery readiness, immutable send evidence |

## Storage Readiness

Private Enterprise should provide tenant-scoped stores for:

- report catalog definitions and report availability;
- render jobs, artifact references, artifact digests, and retention classes;
- setup profile, delivery provider references, domain allowlists, and branding;
- delivery jobs, delivery events, retry state, and provider status summaries;
- schedules, blackout windows, run history, and skipped-run reasons;
- recipient policies, approval requests, immutable approval decisions, and
  exception lifecycle state;
- evidence rooms, scoped access grants, watermark events, and access logs;
- incident packets, incident closures, follow-up tasks, and closure evidence;
- KPI projections, alert events, alert timelines, acknowledgement events, and
  remediation closure operations projections;
- executive digests, board-pack package refs, distribution jobs, signed
  manifest refs, and immutable send evidence.

## Approval And Delivery Gates

Before any Enterprise report leaves the tenant boundary, private Enterprise
must verify:

- the tenant license enables the requested Enterprise report capability;
- the requesting user has a role allowed for the report audience;
- recipients match domain allowlists and channel eligibility;
- external recipients have required approval decisions;
- scheduled sends respect blackout windows and retry policy;
- executive digest sends have approval-before-send evidence;
- report packages have artifact digests and signed manifests where required;
- delivery events are written before final success is shown to the operator;
- revocation, expiry, and retention states are honored during retrieval.

## Enterprise Trial Validation Evidence

The Enterprise Trial package should produce public-safe verification packets
for these evaluator paths:

| Trial path | Required evidence |
| --- | --- |
| Setup wizard | Settings saved with provider references and no raw credentials in evidence. |
| Render report | PDF, DOCX, HTML, signed JSON, CSV, and JSONL render metadata with artifact digests. |
| Send blocked by policy | External recipient or missing approval blocks delivery and writes evidence. |
| Send after approval | Approved delivery writes immutable send evidence and delivery audit event. |
| Schedule run | Schedule creates run history and respects blackout or retry controls. |
| Evidence room | Scoped room grants access, logs view/download, supports revoke and expiry. |
| Alert escalation | Delivery or approval SLO breach raises alert, routes it, and requires acknowledgement. |
| Remediation closure | Alert remediation plan closes only after tasks, final approval, and closure evidence. |
| Executive digest distribution | Email waits for approval; portal/GRC package readiness is visible; send evidence is immutable. |
| Revocation and retention | Revoked or expired artifacts cannot be retrieved and produce audit evidence. |

The public-safe trial validation packet is packaged at
`src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json`.
The redacted example packet is available at
`examples/aispm/enterprise-report-center-trial-validation-packet-public.example.json`.

The trial operator dashboard readiness contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json`.
The redacted example is available at
`examples/aispm/enterprise-report-center-trial-operator-dashboard-readiness-public.example.json`.
The trial operator dashboard API/view-model contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json`.
The redacted example is available at
`examples/aispm/enterprise-report-center-trial-operator-api-view-model-public.example.json`.
The trial evaluator handoff packet contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json`.
The redacted example is available at
`examples/aispm/enterprise-report-center-trial-evaluator-handoff-packet-public.example.json`.
The trial revocation and expiry evidence contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json`.
The redacted example is available at
`examples/aispm/enterprise-report-center-trial-revocation-expiry-evidence-public.example.json`.
The trial lab notebook outline contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json`.
The redacted example is available at
`examples/aispm/enterprise-report-center-trial-lab-notebook-outline-public.example.json`.
The trial lab notebook publication readiness contract is packaged at
`src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json`.
The redacted example is available at
`examples/aispm/enterprise-report-center-trial-lab-notebook-publication-readiness-public.example.json`.

## Release Acceptance Checklist

- All public schemas validate against private Enterprise output fixtures.
- Trial package includes sample tenant data only and never emits raw prompts,
  model reasoning, raw tool output, customer records, recipient addresses, IP
  addresses, provider responses, private remediation details, tenant drilldown
  records, or credential values in public-safe evidence.
- Every render, send, retry, approval, exception, access, alert,
  remediation, closure, and distribution event has an evidence ref.
- Public Community docs link to trial usage instructions but not to private
  implementation internals.
- GitHub, GitLab, Azure DevOps, SIEM, ITSM, GRC, SMTP/provider, and portal
  delivery paths have trial smoke-test evidence where enabled.
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
- Lab notebook publication readiness verifies Wiki navigation, link health,
  redacted screenshots, diagrams, flow charts, checkpoint evidence, and
  required reviews before public Wiki publication.
- Trial evaluators can complete setup, render, approval, send, evidence-room,
  alert, closure, digest, and distribution workflows without operator shell
  access.

## Public Repository Boundary

This Community repository should only contain:

- public schemas;
- redacted examples;
- public architecture and setup docs;
- trial usage instructions;
- public-safe roadmap and readiness checklists.

Private Enterprise owns implementations for renderers, delivery providers,
schedulers, tenant stores, audit stores, approval workflows, evidence-room
workers, alert evaluators, remediation workers, distribution workers, license
enforcement, and SaaS control-plane persistence.
