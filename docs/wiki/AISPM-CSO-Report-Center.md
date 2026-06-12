# AISPM CSO Report Center

The CAVRA AISPM CSO Report Center gives executives, auditors, GRC teams, and
platform owners downloadable or deliverable reports from AI-agent posture data.

The private implementation readiness checklist is maintained in
[AISPM Report Center Enterprise Readiness](AISPM-Report-Center-Enterprise-Readiness).

## Community Edition

Community provides browser-generated public-safe downloads:

- Executive Risk Brief: Markdown
- Board KPI Pack: JSON
- SOC 2-style Audit Summary: Markdown
- Control Coverage Export: CSV
- Evidence Freshness Export: CSV
- Agent Risk Register: CSV

These reports use sample or local activity metadata and exclude raw prompts,
model reasoning, raw tool output, tenant secrets, private connector payloads,
customer records, private policy-pack implementation, and Enterprise source
code.

## Enterprise Edition

Enterprise should add PDF, XLSX, DOCX, HTML, signed JSON, JSONL, GRC upload
packages, incident packets, exception reports, policy-drift reports, live-agent
activity digests, scheduled delivery, and recipient governance.

## Email Delivery

Enterprise email delivery should support SMTP, Microsoft 365, Google Workspace,
AWS SES, SendGrid, or private webhook/GRC connectors. It must enforce RBAC,
recipient domain allowlists, approval gates, delivery retries, bounce tracking,
and delivery audit evidence.

## Setup Inputs

During Enterprise setup, collect report sender address, allowed recipient
domains, SMTP/provider mode, secret-manager references, default timezone,
branding, legal footer, report retention, and delivery approval policy. Do not
store SMTP passwords, provider tokens, private keys, or customer secrets in the
public repository.

## Canonical Document

The canonical design is `docs/architecture/aispm-report-center.md`.

## Release Verification

Report catalog readiness is documented in
`docs/release-verifications/aispm-report-catalog-readiness.md` with the
machine-readable packet
`docs/release-verifications/aispm-report-catalog-readiness.json`. CI enforces
the gate with `scripts/validate-aispm-report-catalog-readiness.py`, and the
AISPM portal exposes the public-safe
`cavra-aispm-report-catalog-packet.json` export.

Report delivery setup readiness is documented in
`docs/release-verifications/aispm-report-delivery-setup-readiness.md` with the
machine-readable packet
`docs/release-verifications/aispm-report-delivery-setup-readiness.json`. CI
enforces the gate with
`scripts/validate-aispm-report-delivery-setup-readiness.py`, and the AISPM
portal exposes the public-safe
`cavra-aispm-report-delivery-setup-packet.json` export.

Report operations readiness is documented in
`docs/release-verifications/aispm-report-operations-readiness.md` with the
machine-readable packet
`docs/release-verifications/aispm-report-operations-readiness.json`. CI
enforces the gate with
`scripts/validate-aispm-report-operations-readiness.py`, and the AISPM portal
exposes the public-safe
`cavra-aispm-report-operations-readiness-packet.json` export.

Report governance readiness is documented in
`docs/release-verifications/aispm-report-governance-readiness.md` with the
machine-readable packet
`docs/release-verifications/aispm-report-governance-readiness.json`. CI
enforces the gate with
`scripts/validate-aispm-report-governance-readiness.py`, and the AISPM portal
exposes the public-safe
`cavra-aispm-report-governance-readiness-packet.json` export.

Report assurance readiness is documented in
`docs/release-verifications/aispm-report-assurance-readiness.md` with the
machine-readable packet
`docs/release-verifications/aispm-report-assurance-readiness.json`. CI
enforces the gate with
`scripts/validate-aispm-report-assurance-readiness.py`, and the AISPM portal
exposes the public-safe
`cavra-aispm-report-assurance-readiness-packet.json` export.

Report response readiness is documented in
`docs/release-verifications/aispm-report-response-readiness.md` with the
machine-readable packet
`docs/release-verifications/aispm-report-response-readiness.json`. CI enforces
the gate with `scripts/validate-aispm-report-response-readiness.py`, and the
AISPM portal exposes the public-safe
`cavra-aispm-report-response-readiness-packet.json` export.

Report trial operations readiness is documented in
`docs/release-verifications/aispm-report-trial-operations-readiness.md` with
the machine-readable packet
`docs/release-verifications/aispm-report-trial-operations-readiness.json`. CI
enforces the gate with
`scripts/validate-aispm-report-trial-operations-readiness.py`, and the AISPM
portal exposes the public-safe
`cavra-aispm-report-trial-operations-readiness-packet.json` export.

## Public Contract Artifacts

The public repository carries only the public-safe contract:

- `src/cavra/aispm_reports.py`
- `src/cavra/schemas/aispm-report-delivery-contract.schema.json`
- `examples/aispm/enterprise-report-delivery-contract-public.example.json`
- `src/cavra/schemas/aispm-report-setup-wizard-contract.schema.json`
- `examples/aispm/enterprise-report-setup-wizard-contract-public.example.json`
- `src/cavra/schemas/aispm-report-delivery-audit-event.schema.json`
- `examples/aispm/enterprise-report-delivery-audit-event-public.example.json`
- `src/cavra/schemas/aispm-report-operations-dashboard.schema.json`
- `examples/aispm/enterprise-report-operations-dashboard-public.example.json`
- `src/cavra/schemas/aispm-report-retention-lifecycle.schema.json`
- `examples/aispm/enterprise-report-retention-lifecycle-public.example.json`
- `src/cavra/schemas/aispm-report-search-retrieval.schema.json`
- `examples/aispm/enterprise-report-search-retrieval-public.example.json`
- `src/cavra/schemas/aispm-report-export-package-manifest.schema.json`
- `examples/aispm/enterprise-report-export-package-manifest-public.example.json`
- `src/cavra/schemas/aispm-report-schedule-policy.schema.json`
- `examples/aispm/enterprise-report-schedule-policy-public.example.json`
- `src/cavra/schemas/aispm-report-recipient-policy.schema.json`
- `examples/aispm/enterprise-report-recipient-policy-public.example.json`
- `src/cavra/schemas/aispm-report-approval-decision.schema.json`
- `examples/aispm/enterprise-report-approval-decision-public.example.json`
- `src/cavra/schemas/aispm-report-exception-lifecycle.schema.json`
- `examples/aispm/enterprise-report-exception-lifecycle-public.example.json`
- `src/cavra/schemas/aispm-report-evidence-room.schema.json`
- `examples/aispm/enterprise-report-evidence-room-public.example.json`
- `src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json`
- `examples/aispm/enterprise-report-evidence-room-access-event-public.example.json`
- `src/cavra/schemas/aispm-report-incident-packet.schema.json`
- `examples/aispm/enterprise-report-incident-packet-public.example.json`
- `src/cavra/schemas/aispm-report-incident-closure.schema.json`
- `examples/aispm/enterprise-report-incident-closure-public.example.json`
- `src/cavra/schemas/aispm-report-kpi-metrics.schema.json`
- `examples/aispm/enterprise-report-kpi-metrics-public.example.json`
- `src/cavra/schemas/aispm-report-alert-escalation.schema.json`
- `examples/aispm/enterprise-report-alert-escalation-public.example.json`
- `src/cavra/schemas/aispm-report-alert-operations-dashboard.schema.json`
- `examples/aispm/enterprise-report-alert-operations-dashboard-public.example.json`
- `src/cavra/schemas/aispm-report-alert-drilldown.schema.json`
- `examples/aispm/enterprise-report-alert-drilldown-public.example.json`
- `src/cavra/schemas/aispm-report-alert-remediation-plan.schema.json`
- `examples/aispm/enterprise-report-alert-remediation-plan-public.example.json`
- `src/cavra/schemas/aispm-report-alert-remediation-closure.schema.json`
- `examples/aispm/enterprise-report-alert-remediation-closure-public.example.json`
- `src/cavra/schemas/aispm-report-remediation-closure-operations-dashboard.schema.json`
- `examples/aispm/enterprise-report-remediation-closure-operations-dashboard-public.example.json`
- `src/cavra/schemas/aispm-report-remediation-closure-executive-digest.schema.json`
- `examples/aispm/enterprise-report-remediation-closure-executive-digest-public.example.json`
- `src/cavra/schemas/aispm-report-remediation-closure-digest-distribution.schema.json`
- `examples/aispm/enterprise-report-remediation-closure-digest-distribution-public.example.json`
- `src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json`
- `examples/aispm/enterprise-report-center-trial-validation-packet-public.example.json`
- `src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json`
- `examples/aispm/enterprise-report-center-trial-operator-dashboard-readiness-public.example.json`
- `src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json`
- `examples/aispm/enterprise-report-center-trial-operator-api-view-model-public.example.json`
- `src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json`
- `examples/aispm/enterprise-report-center-trial-evaluator-handoff-packet-public.example.json`
- `src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json`
- `examples/aispm/enterprise-report-center-trial-revocation-expiry-evidence-public.example.json`
- `src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json`
- `examples/aispm/enterprise-report-center-trial-lab-notebook-outline-public.example.json`
- `src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json`
- `examples/aispm/enterprise-report-center-trial-lab-notebook-publication-readiness-public.example.json`

The contract lists Community report downloads, locked Enterprise report packs,
private Enterprise API endpoints, delivery modes, recipient governance controls,
and setup fields. Renderer, scheduler, email delivery, tenant persistence, and
license enforcement are marked `requires_cavra_enterprise`.

## Alert Remediation Closure Contract

Enterprise alert remediation closure should prove that a report-center alert
was remediated and formally closed. The public-safe contract covers completed
task refs, final approval refs, control updates, residual-risk acceptance,
post-incident review outcomes, communications status, closure evidence, and
redaction guarantees without exposing private identities, raw report content,
customer records, provider responses, secrets, or private remediation details.

## Remediation Closure Operations Dashboard Contract

Enterprise remediation closure operations dashboards should show aggregate
closure throughput, overdue remediation, residual-risk aging, approval
bottlenecks, post-incident review completion, closure SLOs, recent closure
refs, and immutable dashboard evidence for CSO/CISO operations review. The
public contract excludes private identities, customer records, raw report
content, tenant drilldown records, provider responses, secrets, and private
remediation details.

## Remediation Closure Executive Digest Contract

Enterprise remediation closure executive digests should package closure
readiness, overdue remediation, residual risk, board talking points, audit
readiness, distribution controls, and immutable digest evidence for CSO/CISO,
board, and audit review. The public contract excludes private identities,
board member identities, customer records, raw report content, tenant
drilldown records, provider responses, secrets, and private remediation
details.

## Remediation Closure Digest Distribution Contract

Enterprise remediation closure digest distribution should control board-pack
approval, recipient governance, delivery readiness, signed manifest
requirements, immutable send evidence, and redaction guarantees. The public
contract excludes recipient addresses, private identities, board member
identities, customer records, raw report content, tenant drilldown records,
provider responses, secrets, and private remediation details.

## Enterprise Trial Validation Packet

Enterprise Trial should emit a public-safe validation packet for setup,
rendering, blocked send, approved send, scheduled run, evidence room, alert
escalation, remediation closure, executive digest distribution, revocation,
and retention checks. The packet excludes private identities, recipient
addresses, IP addresses, download URLs, raw prompts, model reasoning, raw tool
output, raw report content, provider responses, customer records, tenant
drilldown records, secrets, and source code.

## Enterprise Trial Operator Dashboard Readiness

Enterprise Trial operator dashboards should expose a public-safe readiness
summary for validation status, failed or blocked paths, approval blockers,
evidence links, operator actions, package/license state, and evaluator handoff.
The public API/view-model contract adds expected private portal routes,
operator actions, UI sections, state transitions, and required audit events for
operator review, validation packet review, evaluator handoff approval, and
validation reruns. Private Enterprise owns the live operator dashboard API,
operator session store, trial validation store, handoff workflow, package
access service, license service, support queue, and audit store.

## Enterprise Trial Evaluator Handoff Packet

Enterprise Trial evaluator handoff should give approved evaluators a
metadata-only packet for setup steps, package access status, trial license
status, support state, expiry, and revocation posture. The public contract
excludes evaluator identity, operator identity, package tokens, license keys,
download URLs, IP addresses, raw prompts, model reasoning, raw tool output,
report content, provider responses, customer records, tenant drilldown
records, secrets, and source code.

## Enterprise Trial Revocation And Expiry Evidence

Enterprise Trial revocation and expiry evidence should prove that license
validation, package pulls, trial portal access, Enterprise report rendering,
and support handoff access are blocked after revocation or expiry. Private
Enterprise owns the actual enforcement, package registry access revocation,
license blocking, support queue closure, and immutable audit storage.

## Enterprise Trial Lab Notebook Outline

The Enterprise Trial lab notebook outline defines the public-safe Wiki textbook
structure for trial users: chapters, role-specific labs, screenshots,
diagrams, flow charts, verification checkpoints, and redacted evidence refs.
Private Enterprise owns live trial portal content, package access, license
service behavior, and private lab fixtures.

## Enterprise Trial Lab Notebook Publication Readiness

The publication readiness packet gates the future GitHub Wiki lab notebook.
It requires Wiki navigation, link health, redacted screenshots, diagrams, flow
charts, checkpoint evidence, and docs/security/product review before external
evaluators use the trial labs. Private Enterprise owns private screenshot
capture, customer-specific fixtures, package access verification, license
validation, and non-public operator evidence.

Run `scripts/validate-aispm-trial-lab-notebook.py` before publication to check
the readiness packet schema, Wiki source files, `docs/wiki/Home.md`
navigation, public-safety sections, public-safe asset metadata, and required
acceptance criteria. The same validator runs in Community CI and Release
Community workflows.

Reviewer-facing readiness summaries are available at
`docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md`
and
`docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json`.

## Setup Wizard Contract

Enterprise setup should ask for organization profile, delivery provider,
recipient governance, schedule, retry, and audit settings. Secret fields are
references only, such as `CAVRA_REPORT_SMTP_PASSWORD_REF`; raw provider
credentials must stay in the tenant secret manager.

## Delivery Audit Event Contract

Enterprise report catalog, render, send, schedule, and test-delivery actions
should emit audit events with action status, recipient summary, approval link,
retry state, evidence refs, report digest ref, immutable store ref, and
redaction guarantees. Raw report content, provider responses, recipient
addresses, and secrets are excluded from the public contract.

## Operations Dashboard Contract

Enterprise should expose delivery health, failed sends, retry queues, scheduled
report status, approval bottlenecks, and immutable audit coverage to CSO/admin
users. The public contract excludes recipient addresses, provider responses,
raw report content, secrets, and private tenant payloads.

## Export Package Manifest Contract

Enterprise report packages should support board packs, GRC uploads, SIEM export
bundles, evidence rooms, and incident review packets. The public manifest
contract records bundle metadata, artifact refs, report IDs, formats, digest
refs, approved export targets, retention class, evidence refs, and integrity
refs without including report content or tenant payloads. Private Enterprise
owns package rendering, artifact storage, manifest signing, GRC connectors,
SIEM exporters, and license enforcement.

## Report Schedule Policy Contract

Enterprise report schedules should support recurring CSO, audit, GRC, and
platform reporting while preserving recipient governance. The public contract
records schedule metadata, cadence, formats, RBAC scope, allowed domains,
approval rules, blackout windows, retry policy, delivery target refs, and run
evidence. Recipient addresses, raw report content, provider responses, customer
records, secrets, and private tenant payloads stay outside the public contract.

## Recipient Policy Contract

Enterprise recipient policy should prevent reports from being sent to
unapproved domains, groups, and delivery channels. The public contract records
domain rules, recipient group refs, delivery-channel eligibility, external
recipient approval, encryption requirements, policy review evidence, and
redaction guarantees. Recipient addresses, IdP group members, provider tokens,
customer records, secrets, and private tenant payloads stay outside the public
contract.

## Approval Decision Contract

Enterprise report approvals should be explicit, durable, and reviewable. The
public contract records approval request type, requester role, resource refs,
risk level, decision state, conditions, policy context, digest refs, immutable
evidence refs, audit refs, and review deadlines. Approver identity, recipient
addresses, raw report content, private justification text, customer records,
secrets, and private tenant payloads stay outside the public contract.

## Exception Lifecycle Contract

Enterprise report exceptions should expire, renew, revoke, and close through
evidence-backed lifecycle events instead of becoming permanent bypasses. The
public contract records exception scope, status, expiry, review due date,
renewal policy, closure state, lifecycle events, immutable audit refs, and
redaction guarantees. Recipient addresses, approver identity, private
justification text, raw report content, customer records, secrets, and private
tenant payloads stay outside the public contract.

## Evidence Room Contract

Enterprise evidence rooms should share curated report packages with auditors
through scoped, expiring, watermarked access. The public contract records room
metadata, access scope, allowed domain refs, included artifacts, export package
manifest refs, digest refs, time-limited link controls, immutable access log
refs, and redaction guarantees. Recipient addresses, auditor identity, raw
report content, download URLs, customer records, secrets, and private tenant
payloads stay outside the public contract.

## Evidence Room Access Event Contract

Enterprise should create an immutable access event for every evidence room
view, download, revocation, expiry, failed authentication, failed policy
decision, and watermark action. The public contract records event type,
outcome, room ref, redacted actor class, MFA status, policy refs, artifact refs,
watermark state, signed-link usage, retention/license checks, digest-chain refs,
and evidence refs. Auditor identity, IP addresses, recipient addresses,
download URLs, raw report content, customer records, secrets, and private
tenant payloads stay outside the public contract.

## Incident Packet Contract

Enterprise should package report incidents into metadata-only review bundles
that connect report exceptions, approval decisions, evidence-room access
events, delivery audit refs, export package refs, affected artifacts,
chain-of-custody controls, evidence refs, owner role, review due date, and
closure requirements. Recipient addresses, auditor identity, approver identity,
IP addresses, download URLs, raw report content, private justification,
customer records, secrets, and private tenant payloads stay outside the public
contract.

## Incident Closure Contract

Enterprise should close report incidents only after remediation actions,
closure approval, lessons learned, follow-up tasks, and immutable closure
evidence are recorded. The public contract records final status, remediation
action refs, approver role, closure conditions, control updates, runbook refs,
follow-up task refs, closure digest, incident packet ref, closure manifest ref,
and evidence refs. Recipient addresses, auditor identity, approver identity, IP
addresses, download URLs, raw report content, private justification, customer
records, secrets, and private tenant payloads stay outside the public contract.

## KPI Metrics Contract

Enterprise should expose aggregate CSO/CISO report-center metrics for report
volume, delivery success, approval latency, exception aging, evidence-room
access, incident closure SLOs, and audit readiness trends. The public contract
records reporting window metadata, summary counters, report volume rows,
delivery health, approval latency, exception aging, evidence-room access,
incident closure SLO, audit readiness trend rows, and redaction guarantees.
Tenant drilldown records, customer records, identities, IP addresses, download
URLs, raw report content, secrets, and private tenant payloads stay outside the
public contract.

## Alert Escalation Contract

Enterprise should turn report-center KPI breaches and suspicious report
activity into routed, acknowledged, evidence-backed work. The public contract
records alert policy metadata, trigger rules, trigger evaluations, routing
channels, escalation levels, acknowledgement state, incident linkage, evidence
refs, and redaction guarantees. Recipient addresses, operator identity, auditor
identity, approver identity, IP addresses, download URLs, raw report content,
provider responses, customer records, tenant drilldown records, secrets, and
private tenant payloads stay outside the public contract.

## Alert Operations Dashboard Contract

Enterprise should give CSO, SOC, GRC, and platform owners a dashboard for
active alert operations. The public contract records dashboard counters, queue
health, active alert rows, escalation health, acknowledgement SLOs, suppression
state, incident linkage health, routing health, evidence refs, and redaction
guarantees. Recipient addresses, operator identity, auditor identity, approver
identity, IP addresses, download URLs, raw report content, provider responses,
customer records, tenant drilldown records, secrets, and private tenant
payloads stay outside the public contract.

## Alert Drilldown Contract

Enterprise should let authorized CSO, SOC, GRC, and platform owners inspect a
single alert with an ordered public-safe timeline. The public contract records
alert summary metadata, routed owner roles, acknowledgement history,
suppression history, escalation path, linked incident refs, evidence-chain
refs, and redaction guarantees. Recipient addresses, operator identity,
auditor identity, approver identity, IP addresses, download URLs, raw report
content, provider responses, customer records, tenant drilldown records,
secrets, and private tenant payloads stay outside the public contract.

## Alert Remediation Plan Contract

Enterprise should turn report-alert findings into owner-assigned remediation
work. The public contract records plan metadata, affected public-safe refs,
tasks, due dates, approval requirements, closure criteria, control updates,
communications requirements, evidence refs, and redaction guarantees. Recipient
addresses, operator identity, auditor identity, approver identity, IP
addresses, download URLs, raw report content, provider responses, customer
records, private remediation details, tenant drilldown records, secrets, and
private tenant payloads stay outside the public contract.

## Retention And Evidence Lifecycle Contract

Enterprise should track report retention windows, legal hold state, immutable
store refs, report expiry, audit export lifecycle, object-lock state, KMS
references, deletion approval, tombstones, and retention evidence refs. The
public contract excludes raw report content, recipient addresses, customer
records, secrets, and private tenant payloads.

## Search And Evidence Retrieval Contract

Enterprise should support filtered report search, immutable evidence lookup,
retention-aware access decisions, RBAC-scoped downloads, watermarked retrieval,
and audit logging for every retrieval. The public contract excludes raw report
content, signed download URLs, recipient addresses, customer records, secrets,
and private tenant payloads.
