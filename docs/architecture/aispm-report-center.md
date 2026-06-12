# AISPM CSO Report Center

This document defines the public-safe design for the CAVRA AISPM CSO Report
Center and Enterprise report delivery service.

The private implementation readiness checklist is maintained in
[AISPM Report Center Enterprise Readiness Checklist](aispm-report-center-enterprise-readiness.md).

## Product Goal

CSO/CISO users need decision-ready reports, not only dashboards. The report
center should let leadership, auditors, GRC teams, and platform owners download
or receive the exact report they need for board updates, risk committees,
audit evidence, exception review, and AI-agent governance operations.

## Community Edition

Community provides browser-generated reports from public-safe sample or local
activity metadata. These reports do not require a backend, SMTP integration, or
tenant storage.

Implemented Community downloads:

| Report | Format | Audience |
| --- | --- | --- |
| Executive Risk Brief | Markdown | CSO/CISO |
| Board KPI Pack | JSON | Leadership |
| SOC 2-style Audit Summary | Markdown | Audit / GRC |
| Control Coverage Export | CSV | Security engineering |
| Evidence Freshness Export | CSV | Audit / GRC |
| Agent Risk Register | CSV | Platform security |

Community reports exclude raw prompts, model reasoning, raw tool output,
tenant secrets, private connector payloads, customer records, private
policy-pack implementation, and Enterprise source code.

## Enterprise Edition

Enterprise should add a report service with:

- PDF board packs;
- XLSX evidence workbooks;
- DOCX audit narratives;
- HTML executive summaries;
- signed JSON evidence packets;
- SIEM-ready JSONL exports;
- GRC upload packages;
- incident packets;
- exception reports;
- policy-drift reports;
- live-agent activity digests;
- scheduled delivery and recipient governance.

## Enterprise Email Delivery

Enterprise should support on-demand and scheduled delivery through:

- SMTP;
- Microsoft 365 Graph mail;
- Google Workspace Gmail API;
- AWS SES;
- SendGrid;
- private webhook or GRC connectors.

Delivery must be tenant-scoped, RBAC-controlled, and audited.

## Setup Configuration

During CAVRA Enterprise setup, collect organization-specific settings without
storing secrets in public files:

| Setting | Purpose |
| --- | --- |
| `CAVRA_REPORT_DELIVERY_MODE` | `smtp`, `microsoft365`, `google_workspace`, `ses`, `sendgrid`, `webhook`, or `disabled` |
| `CAVRA_REPORT_FROM_ADDRESS` | Approved sender address, such as `cavra-reports@example.com` |
| `CAVRA_REPORT_REPLY_TO` | Optional reply-to address |
| `CAVRA_REPORT_ALLOWED_RECIPIENT_DOMAINS` | Comma-separated recipient domain allowlist |
| `CAVRA_REPORT_DEFAULT_TIMEZONE` | Timezone for scheduled reports |
| `CAVRA_REPORT_RETENTION_DAYS` | Report retention policy |
| `CAVRA_REPORT_BRAND_PROFILE` | Tenant logo, footer, and legal disclaimer profile |
| `CAVRA_REPORT_SMTP_HOST` | SMTP host when SMTP mode is used |
| `CAVRA_REPORT_SMTP_PORT` | SMTP port |
| `CAVRA_REPORT_SMTP_USERNAME_REF` | Secret-manager reference for SMTP username |
| `CAVRA_REPORT_SMTP_PASSWORD_REF` | Secret-manager reference for SMTP password |
| `CAVRA_REPORT_PROVIDER_TOKEN_REF` | Secret-manager reference for provider API token |

Do not put SMTP passwords, provider tokens, private keys, or customer secrets in
the public repository.

## Security Controls

- Enforce recipient domain allowlists.
- Require RBAC permission to send or schedule reports.
- Optionally require approval before external delivery.
- Redact private prompts and model reasoning unless the tenant explicitly
  enables authorized private report packs.
- Attach immutable evidence references rather than raw sensitive payloads.
- Record delivery attempts, failures, retries, bounces, and recipient metadata.
- Support DKIM/SPF/DMARC alignment guidance for customer domains.
- Support encrypted report attachments for regulated tenants.

## Enterprise API Shape

Private Enterprise may expose endpoints similar to:

| Endpoint | Purpose |
| --- | --- |
| `GET /enterprise/aispm/reports/catalog` | List tenant-enabled report types and formats. |
| `POST /enterprise/aispm/reports/render` | Render a selected report package. |
| `POST /enterprise/aispm/reports/send` | Send a rendered report to approved recipients. |
| `GET /enterprise/aispm/reports/deliveries` | Search delivery audit history. |
| `POST /enterprise/aispm/reports/schedules` | Create scheduled delivery rules. |

These endpoints are not implemented in the public Community repository.

## Public Contract Artifacts

The public repository now carries a stable, public-safe report delivery
contract so Community, documentation, and the private Enterprise package can
agree on behavior without exposing commercial source code:

| Artifact | Purpose |
| --- | --- |
| `src/cavra/aispm_reports.py` | Public helper that emits the report delivery contract object. |
| `src/cavra/schemas/aispm-report-delivery-contract.schema.json` | Packaged JSON Schema for the contract. |
| `examples/aispm/enterprise-report-delivery-contract-public.example.json` | Redacted public example used by tests and Enterprise implementers. |
| `src/cavra/schemas/aispm-report-setup-wizard-contract.schema.json` | Packaged JSON Schema for the Enterprise setup wizard contract. |
| `examples/aispm/enterprise-report-setup-wizard-contract-public.example.json` | Redacted public setup wizard example. |
| `src/cavra/schemas/aispm-report-delivery-audit-event.schema.json` | Packaged JSON Schema for Enterprise report delivery audit events. |
| `examples/aispm/enterprise-report-delivery-audit-event-public.example.json` | Redacted public audit event example. |
| `src/cavra/schemas/aispm-report-operations-dashboard.schema.json` | Packaged JSON Schema for the Enterprise report operations dashboard. |
| `examples/aispm/enterprise-report-operations-dashboard-public.example.json` | Redacted public operations dashboard example. |
| `src/cavra/schemas/aispm-report-retention-lifecycle.schema.json` | Packaged JSON Schema for report retention and evidence lifecycle. |
| `examples/aispm/enterprise-report-retention-lifecycle-public.example.json` | Redacted public retention lifecycle example. |
| `src/cavra/schemas/aispm-report-search-retrieval.schema.json` | Packaged JSON Schema for report search and evidence retrieval. |
| `examples/aispm/enterprise-report-search-retrieval-public.example.json` | Redacted public search/retrieval example. |
| `src/cavra/schemas/aispm-report-export-package-manifest.schema.json` | Packaged JSON Schema for Enterprise export package manifests. |
| `examples/aispm/enterprise-report-export-package-manifest-public.example.json` | Redacted public export package manifest example. |
| `src/cavra/schemas/aispm-report-schedule-policy.schema.json` | Packaged JSON Schema for Enterprise report schedules. |
| `examples/aispm/enterprise-report-schedule-policy-public.example.json` | Redacted public report schedule policy example. |
| `src/cavra/schemas/aispm-report-recipient-policy.schema.json` | Packaged JSON Schema for Enterprise report recipient policy. |
| `examples/aispm/enterprise-report-recipient-policy-public.example.json` | Redacted public recipient policy example. |
| `src/cavra/schemas/aispm-report-approval-decision.schema.json` | Packaged JSON Schema for Enterprise report approval decisions. |
| `examples/aispm/enterprise-report-approval-decision-public.example.json` | Redacted public approval decision example. |
| `src/cavra/schemas/aispm-report-exception-lifecycle.schema.json` | Packaged JSON Schema for report exception lifecycle. |
| `examples/aispm/enterprise-report-exception-lifecycle-public.example.json` | Redacted public exception lifecycle example. |
| `src/cavra/schemas/aispm-report-evidence-room.schema.json` | Packaged JSON Schema for Enterprise report evidence rooms. |
| `examples/aispm/enterprise-report-evidence-room-public.example.json` | Redacted public evidence room example. |
| `src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json` | Packaged JSON Schema for evidence room access events. |
| `examples/aispm/enterprise-report-evidence-room-access-event-public.example.json` | Redacted public evidence room access event example. |
| `src/cavra/schemas/aispm-report-incident-packet.schema.json` | Packaged JSON Schema for Enterprise report incident packets. |
| `examples/aispm/enterprise-report-incident-packet-public.example.json` | Redacted public incident packet example. |
| `src/cavra/schemas/aispm-report-incident-closure.schema.json` | Packaged JSON Schema for Enterprise report incident closure. |
| `examples/aispm/enterprise-report-incident-closure-public.example.json` | Redacted public incident closure example. |
| `src/cavra/schemas/aispm-report-kpi-metrics.schema.json` | Packaged JSON Schema for Enterprise report-center KPI metrics. |
| `examples/aispm/enterprise-report-kpi-metrics-public.example.json` | Redacted public report KPI metrics example. |
| `src/cavra/schemas/aispm-report-alert-escalation.schema.json` | Packaged JSON Schema for Enterprise report alert escalation. |
| `examples/aispm/enterprise-report-alert-escalation-public.example.json` | Redacted public report alert escalation example. |
| `src/cavra/schemas/aispm-report-alert-operations-dashboard.schema.json` | Packaged JSON Schema for Enterprise report alert operations dashboards. |
| `examples/aispm/enterprise-report-alert-operations-dashboard-public.example.json` | Redacted public report alert operations dashboard example. |
| `src/cavra/schemas/aispm-report-alert-drilldown.schema.json` | Packaged JSON Schema for Enterprise report alert drilldowns. |
| `examples/aispm/enterprise-report-alert-drilldown-public.example.json` | Redacted public report alert drilldown example. |
| `src/cavra/schemas/aispm-report-alert-remediation-plan.schema.json` | Packaged JSON Schema for Enterprise report alert remediation plans. |
| `examples/aispm/enterprise-report-alert-remediation-plan-public.example.json` | Redacted public report alert remediation plan example. |
| `src/cavra/schemas/aispm-report-alert-remediation-closure.schema.json` | Packaged JSON Schema for Enterprise report alert remediation closure. |
| `examples/aispm/enterprise-report-alert-remediation-closure-public.example.json` | Redacted public report alert remediation closure example. |
| `src/cavra/schemas/aispm-report-remediation-closure-operations-dashboard.schema.json` | Packaged JSON Schema for Enterprise remediation closure operations dashboards. |
| `examples/aispm/enterprise-report-remediation-closure-operations-dashboard-public.example.json` | Redacted public remediation closure operations dashboard example. |
| `src/cavra/schemas/aispm-report-remediation-closure-executive-digest.schema.json` | Packaged JSON Schema for Enterprise remediation closure executive digests. |
| `examples/aispm/enterprise-report-remediation-closure-executive-digest-public.example.json` | Redacted public remediation closure executive digest example. |
| `src/cavra/schemas/aispm-report-remediation-closure-digest-distribution.schema.json` | Packaged JSON Schema for Enterprise remediation closure digest distribution. |
| `examples/aispm/enterprise-report-remediation-closure-digest-distribution-public.example.json` | Redacted public remediation closure digest distribution example. |
| `src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json` | Packaged JSON Schema for Enterprise Trial Report Center validation packets. |
| `examples/aispm/enterprise-report-center-trial-validation-packet-public.example.json` | Redacted public Report Center trial validation packet example. |
| `src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json` | Packaged JSON Schema for Enterprise Trial operator dashboard readiness. |
| `examples/aispm/enterprise-report-center-trial-operator-dashboard-readiness-public.example.json` | Redacted public operator dashboard readiness example. |
| `src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json` | Packaged JSON Schema for the Enterprise Trial operator dashboard API/view-model contract. |
| `examples/aispm/enterprise-report-center-trial-operator-api-view-model-public.example.json` | Redacted public operator dashboard API/view-model example. |
| `src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json` | Packaged JSON Schema for Enterprise Trial evaluator handoff packets. |
| `examples/aispm/enterprise-report-center-trial-evaluator-handoff-packet-public.example.json` | Redacted public evaluator handoff packet example. |
| `src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json` | Packaged JSON Schema for Enterprise Trial revocation and expiry evidence. |
| `examples/aispm/enterprise-report-center-trial-revocation-expiry-evidence-public.example.json` | Redacted public revocation and expiry evidence example. |
| `src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json` | Packaged JSON Schema for Enterprise Trial lab notebook outlines. |
| `examples/aispm/enterprise-report-center-trial-lab-notebook-outline-public.example.json` | Redacted public lab notebook outline example. |
| `src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json` | Packaged JSON Schema for Enterprise Trial lab notebook publication readiness. |
| `examples/aispm/enterprise-report-center-trial-lab-notebook-publication-readiness-public.example.json` | Redacted public lab notebook publication readiness example. |

The contract defines:

- Community report IDs, titles, audiences, and formats;
- Enterprise report IDs and locked availability markers;
- private Enterprise API endpoints for catalog, render, send, delivery history,
  and schedules;
- supported delivery modes: SMTP, Microsoft 365, Google Workspace, AWS SES,
  SendGrid, webhook, and disabled;
- recipient governance controls: domain allowlists, RBAC, approval gates, and
  delivery audit evidence;
- setup settings and secret-manager reference fields.

The contract explicitly marks renderer, scheduler, email delivery, tenant
persistence, and license enforcement as `requires_cavra_enterprise`.

## Release Verification

Report catalog readiness is tracked by
`docs/release-verifications/aispm-report-catalog-readiness.md` and
`docs/release-verifications/aispm-report-catalog-readiness.json`, enforced by
`scripts/validate-aispm-report-catalog-readiness.py`, and exported from the
AISPM portal as `cavra-aispm-report-catalog-packet.json`.

Report delivery setup readiness is tracked by
`docs/release-verifications/aispm-report-delivery-setup-readiness.md` and
`docs/release-verifications/aispm-report-delivery-setup-readiness.json`,
enforced by `scripts/validate-aispm-report-delivery-setup-readiness.py`, and
exported from the AISPM portal as
`cavra-aispm-report-delivery-setup-packet.json`.

Report operations readiness is tracked by
`docs/release-verifications/aispm-report-operations-readiness.md` and
`docs/release-verifications/aispm-report-operations-readiness.json`, enforced
by `scripts/validate-aispm-report-operations-readiness.py`, and exported from
the AISPM portal as
`cavra-aispm-report-operations-readiness-packet.json`.

Report governance readiness is tracked by
`docs/release-verifications/aispm-report-governance-readiness.md` and
`docs/release-verifications/aispm-report-governance-readiness.json`, enforced
by `scripts/validate-aispm-report-governance-readiness.py`, and exported from
the AISPM portal as
`cavra-aispm-report-governance-readiness-packet.json`.

Report assurance readiness is tracked by
`docs/release-verifications/aispm-report-assurance-readiness.md` and
`docs/release-verifications/aispm-report-assurance-readiness.json`, enforced
by `scripts/validate-aispm-report-assurance-readiness.py`, and exported from
the AISPM portal as
`cavra-aispm-report-assurance-readiness-packet.json`.

Report response readiness is tracked by
`docs/release-verifications/aispm-report-response-readiness.md` and
`docs/release-verifications/aispm-report-response-readiness.json`, enforced
by `scripts/validate-aispm-report-response-readiness.py`, and exported from
the AISPM portal as
`cavra-aispm-report-response-readiness-packet.json`.

Report trial operations readiness is tracked by
`docs/release-verifications/aispm-report-trial-operations-readiness.md` and
`docs/release-verifications/aispm-report-trial-operations-readiness.json`,
enforced by `scripts/validate-aispm-report-trial-operations-readiness.py`, and
exported from the AISPM portal as
`cavra-aispm-report-trial-operations-readiness-packet.json`.

The release gate verifies the six Community report downloads, Enterprise-only
PDF/XLSX/DOCX rendering and scheduled email boundaries, recipient governance,
delivery audit evidence, README/wiki links, workflow wiring, and public-safety
exclusions.

## Setup Wizard Contract

The public setup wizard contract defines the information Enterprise should ask
for during tenant setup while keeping secret values outside public files.

Wizard steps:

| Step | Purpose |
| --- | --- |
| Organization Profile | Sender address, reply-to, timezone, retention, and branding profile reference. |
| Delivery Provider | SMTP or provider mode, host/port, and secret-manager references. |
| Recipient Governance | Allowed recipient domains, approval requirement, and RBAC roles. |
| Schedule And Audit | Default schedule, retry policy, audit retention, and audit export reference. |

The wizard accepts references such as `CAVRA_REPORT_SMTP_PASSWORD_REF`; it must
not accept raw SMTP passwords, provider tokens, private keys, customer records,
or tenant payloads in public configuration.

Private Enterprise must implement:

- setup wizard UI;
- settings persistence;
- secret reference resolution;
- provider validation;
- test delivery;
- license enforcement.

## Delivery Audit Event Contract

Every Enterprise report catalog, render, send, schedule, and test-delivery
operation should emit a delivery audit event. The public contract captures only
metadata and opaque references:

| Section | Purpose |
| --- | --- |
| `audit_event` | Action, status, report ID, format, actor ref, tenant ref, and delivery mode. |
| `recipient_summary` | Recipient count, allowed domains, external-domain count, and redaction status. |
| `approval` | Whether approval was required and the opaque approval reference/decision. |
| `retry` | Attempt number, max attempts, next retry timestamp, and terminal status. |
| `evidence` | Evidence refs, report digest ref, delivery audit ref, and immutable store ref. |
| `redaction` | Guarantees that raw report content, provider responses, recipient addresses, and secrets are excluded. |

Private Enterprise must persist provider responses, retry state, immutable
evidence objects, delivery history, and tenant-scoped audit searches outside
this public repository.

## Operations Dashboard Contract

The Enterprise report operations dashboard should give CSO, security admin,
audit, and platform teams one operational view of report delivery health.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `summary` | Delivery health, scheduled report count, pending approvals, retry queue depth, failed deliveries, and immutable audit coverage. |
| `queues` | Render, delivery, retry, audit export, and schedule queue depth and age. |
| `scheduled_reports` | Report schedule status and next run metadata. |
| `approval_bottlenecks` | Pending approval refs, report IDs, approver group, and pending time. |
| `failed_deliveries` | Failed delivery refs, failure class, retry state, and last attempt time. |
| `audit_coverage` | Expected events, persisted events, missing immutable refs, and coverage status. |

The dashboard contract excludes recipient addresses, provider responses, raw
report content, secrets, and private tenant payloads. Private Enterprise owns
live queue inspection, provider health probes, retry controls, audit search,
dashboard persistence, and license enforcement.

## Retention And Evidence Lifecycle Contract

The Enterprise retention lifecycle contract defines how rendered reports,
delivery audit events, audit exports, and immutable evidence references are
retained, archived, placed under legal hold, expired, or deleted.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `policy` | Default retention, audit-event retention, immutable storage, legal hold support, and deletion approval requirement. |
| `report_lifecycle` | Report refs, report IDs, creation/expiry timestamps, lifecycle state, immutable refs, and legal-hold refs. |
| `audit_export_lifecycle` | Audit export ref, archive state, object-lock state, and KMS key reference. |
| `deletion_policy` | Allowed and blocked deletion states, approval requirement, and tombstone requirement. |
| `evidence` | Retention evidence refs, archive manifest ref, and evidence-chain ref. |

The lifecycle contract excludes raw report content, recipient addresses,
customer records, secrets, and private tenant payloads. Private Enterprise owns
retention workers, legal hold storage, immutable archives, KMS integration,
deletion approval workflows, and license enforcement.

## Search And Evidence Retrieval Contract

The Enterprise search and retrieval contract defines how authorized users find
reports, resolve immutable evidence references, and download report artifacts
under RBAC and retention controls.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `query` | Actor ref, filters, RBAC scope, lifecycle states, format filters, and retention mode. |
| `results` | Report refs, report IDs, formats, lifecycle state, evidence ref, immutable ref, and download eligibility. |
| `retrieval` | Retrieval ref, access decision, signed URL reference, expiry, and watermark requirement. |
| `access_controls` | RBAC, retention, legal-hold, download audit, and approval checks. |
| `audit` | Retrieval audit ref, log timestamp, and evidence refs. |

The contract excludes raw report content, signed download URLs, recipient
addresses, customer records, secrets, and private tenant payloads. Private
Enterprise owns search indexing, RBAC authorization, immutable reference
resolution, signed download URLs, retrieval audit storage, and license
enforcement.

## Export Package Manifest Contract

Enterprise report packages should be portable across board packs, GRC uploads,
SIEM exports, evidence rooms, and incident reviews. The public export package
manifest contract defines the metadata needed to prove what was bundled without
including report content or tenant payloads.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `package` | Package ref, bundle type, requester role, creation time, retention class, watermark requirement, and signed-manifest requirement. |
| `artifacts` | Artifact refs, report IDs, formats, private content refs, digest refs, and sizes. |
| `delivery_targets` | Approved export target refs, target type, delivery mode, recipient scope, and approval requirement. |
| `integrity` | Manifest digest ref, signature ref, evidence-chain ref, and checksum requirement. |
| `evidence` | Source evidence refs, export audit ref, and immutable package store ref. |

The manifest excludes raw report content, recipient addresses, signed download
URLs, customer records, secrets, and private tenant payloads. Private Enterprise
owns package rendering, artifact storage, manifest signing, GRC connectors,
SIEM exporters, and license enforcement.

## Report Schedule Policy Contract

Enterprise report schedules should support recurring CSO, audit, GRC, and
platform reports without bypassing recipient governance. The public scheduling
contract defines how schedule metadata, delivery settings, approval policy,
blackout windows, retry behavior, and run evidence fit together.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `schedule` | Schedule ref, name, status, report IDs, formats, cadence, timezone, next run, and creator role. |
| `recipient_governance` | Recipient scope, allowed domains, RBAC scope, external-delivery flag, and redaction guarantee. |
| `delivery` | Delivery mode, target ref, package manifest requirement, watermark requirement, and encrypted attachment requirement. |
| `approval_policy` | Approval requirement, approver group, approval ref, change approval, and external-recipient approval rules. |
| `blackout_windows` | Deferred, skipped, or manually approved schedule windows. |
| `retry_policy` | Maximum attempts, backoff, retry window, and dead-letter requirement. |
| `run_evidence` | Last run ref, status, timestamp, evidence refs, and schedule audit ref. |

The schedule contract excludes recipient addresses, raw report content,
provider responses, customer records, secrets, and private tenant payloads.
Private Enterprise owns scheduler workers, blackout calendar evaluation,
recipient resolution, provider delivery, schedule persistence, and license
enforcement.

## Recipient Policy Contract

Enterprise recipient policy should prevent reports from being delivered to
unapproved people, domains, and channels. The public recipient policy contract
defines how domain allowlists, recipient groups, channel eligibility, approval
policy, encryption policy, and review evidence fit together.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `policy` | Policy ref, status, owner role, default action, and external-delivery default. |
| `domain_rules` | Domain classification, allow/deny status, approval requirement, and encryption requirement. |
| `recipient_groups` | Opaque group refs, display names, role scope, member count, source, and address redaction. |
| `delivery_channel_eligibility` | Delivery channel allow status, verified-sender requirement, and encryption requirement. |
| `approval_policy` | External recipient, new domain, and recipient group change approval requirements. |
| `encryption_policy` | Attachment encryption, minimum transport, KMS reference, and customer-managed key support. |
| `audit` | Policy-change audit ref, last review timestamp, and review evidence refs. |

The recipient policy contract excludes recipient addresses, IdP group members,
provider tokens, customer records, secrets, and private tenant payloads.
Private Enterprise owns recipient directory sync, IdP group resolution, domain
verification, encryption key resolution, approval workflow, and license
enforcement.

## Approval Decision Contract

Enterprise report delivery should make approval decisions explicit, durable,
and reviewable. The public approval decision contract defines how report-send
approvals, schedule-change approvals, new-domain approvals, recipient-group
changes, and external-delivery exceptions are recorded.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `approval_request` | Approval ref, request type, requester role, resource ref, risk level, and reason code. |
| `decision` | Decision ref, approved/rejected state, decider role, timestamp, expiry, and conditions. |
| `subject` | Report IDs, formats, delivery mode, recipient scope, and recipient redaction guarantee. |
| `policy_context` | Recipient policy, schedule, domain rule, and approval policy refs. |
| `evidence` | Approval evidence refs, request digest, decision digest, and immutable store ref. |
| `audit` | Approval audit event ref, log timestamp, and review deadline. |

The approval decision contract excludes approver identity, recipient addresses,
raw report content, private justification text, customer records, secrets, and
private tenant payloads. Private Enterprise owns approval workflow execution,
approver identity resolution, policy exception storage, immutable decision
audit, notification delivery, and license enforcement.

## Exception Lifecycle Contract

Enterprise report exceptions should not become permanent unmanaged bypasses.
The public exception lifecycle contract defines how approved exceptions expire,
renew, revoke, close, and carry evidence-backed review events.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `exception` | Exception ref, type, status, open/expiry timestamps, owner role, and linked approval ref. |
| `scope` | Report IDs, recipient scope, domain rule ref, schedule ref, and delivery modes covered by the exception. |
| `lifecycle_events` | Open, review, renew, expire, revoke, and close events with actor refs and evidence refs. |
| `review_policy` | Review due date, renewal approval requirement, revocation reason requirement, and closure evidence requirement. |
| `renewal` | Renewal allowance, renewal limit, renewal window, and renewal approval ref. |
| `closure` | Closure state, timestamp, reason, and closure evidence refs. |
| `evidence` | Exception digest, lifecycle audit ref, immutable store ref, and lifecycle evidence refs. |

The exception lifecycle contract excludes recipient addresses, approver
identity, private justification text, raw report content, customer records,
secrets, and private tenant payloads. Private Enterprise owns exception
storage, renewal workflow, revocation workflow, review notifications, immutable
lifecycle audit, and license enforcement.

## Evidence Room Contract

Enterprise evidence rooms should let teams share curated report packages with
auditors without exposing raw tenant data or uncontrolled downloads. The public
evidence room contract defines room metadata, scoped access, included artifacts,
watermarking, time-limited links, and immutable access logs.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `room` | Evidence room ref, title, purpose, status, creator role, creation time, and expiry. |
| `access_scope` | Audience, recipient scope, allowed domain refs, RBAC scope, MFA requirement, and download permission. |
| `artifacts` | Artifact refs, report IDs, formats, export package manifest refs, digest refs, and watermark requirements. |
| `controls` | Signed manifest, time-limited link, access log, watermark, and revocation controls. |
| `access_log` | Access log ref, last access timestamp, access count, immutable store ref, and evidence refs. |

The evidence room contract excludes recipient addresses, auditor identity,
raw report content, download URLs, customer records, secrets, and private
tenant payloads. Private Enterprise owns the evidence room portal, auditor
identity resolution, signed download links, watermarking, immutable access
logs, and license enforcement.

## Evidence Room Access Event Contract

Every evidence room view, download, revocation, expiry, failed authentication,
failed policy decision, and watermark action should create an immutable audit
event. The public access event contract defines event metadata, redacted actor
classification, policy decision refs, artifact refs, watermark status, signed
link usage, retention and license checks, digest chain refs, and evidence refs.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `event` | Event ref, room ref, event type, outcome, timestamp, source, and correlation ref. |
| `actor` | Redacted actor ref, actor type, organization ref, MFA status, and IP redaction marker. |
| `access_decision` | Allow/block/revoke/expire decision, reason, policy refs, expiry, and revocation ref. |
| `artifacts` | Artifact refs, report IDs, formats, digest refs, and watermark application state. |
| `controls` | Signed-link, watermark, access-log, immutable-audit, retention, and license checks. |
| `integrity` | Event digest, previous event digest, manifest ref, audit-store ref, and evidence refs. |

The access event contract excludes recipient addresses, auditor identity, IP
addresses, download URLs, raw report content, customer records, secrets, and
private tenant payloads. Private Enterprise owns identity resolution, signed
download links, watermarking, immutable access event storage, revocation
workflow, and license enforcement.

## Incident Packet Contract

Enterprise report incidents should be reviewable without forcing security,
audit, and leadership users to search individual logs. The public incident
packet contract bundles report exceptions, approval decisions, evidence-room
access events, delivery audit refs, export package refs, affected artifacts,
chain-of-custody controls, and review status into one metadata-only packet.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `incident` | Incident ref, title, type, severity, status, open time, and detector. |
| `scope` | Room refs, report IDs, artifact refs, and policy refs in scope. |
| `related_records` | Exception, approval, access event, delivery audit, and export package refs. |
| `evidence` | Packet digest, manifest ref, timeline ref, immutable-store ref, and evidence refs. |
| `review` | Owner role, due date, approval requirement, closure requirement, and recommended actions. |
| `controls` | Signed packet, immutable audit, chain-of-custody, redaction review, and post-incident review controls. |

The incident packet contract excludes recipient addresses, auditor identity,
approver identity, IP addresses, download URLs, raw report content, private
justification, customer records, secrets, and private tenant payloads. Private
Enterprise owns packet building, timeline correlation, identity resolution,
signed packet generation, immutable incident storage, and license enforcement.

## Incident Closure Contract

Enterprise report incidents should close only after remediation, closure
approval, lessons learned, follow-up tracking, and immutable closure evidence
exist. The public incident closure contract defines final status, remediation
actions, closure approval, lessons learned, follow-up tasks, closure manifests,
and immutable evidence refs.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `incident` | Incident ref, type, severity, final status, open time, and close time. |
| `remediation` | Public-safe remediation summary, action refs, action types, status, and evidence refs. |
| `closure_approval` | Closure approval ref, decision, approver role, decision time, and conditions. |
| `lessons_learned` | Summary, control update refs, and runbook refs. |
| `follow_up_tasks` | Follow-up task refs, owner roles, due dates, status, and evidence requirements. |
| `evidence` | Closure digest, incident packet ref, closure manifest ref, immutable-store ref, and evidence refs. |
| `controls` | Closure approval, remediation evidence, lessons learned, follow-up tracking, and immutable closure controls. |

The incident closure contract excludes recipient addresses, auditor identity,
approver identity, IP addresses, download URLs, raw report content, private
justification, customer records, secrets, and private tenant payloads. Private
Enterprise owns closure workflow, remediation tracking, approval identity
resolution, lessons-learned workflow, immutable closure storage, and license
enforcement.

## KPI Metrics Contract

Enterprise report-center metrics should give CSO/CISO users a concise operating
view of report volume, delivery reliability, approval latency, exception age,
evidence-room access, incident closure SLOs, and audit readiness. The public KPI
metrics contract defines aggregate reporting windows, trend rows, and dashboard
summary metrics only.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `window` | Metrics window ref, start, end, timezone, and reporting grain. |
| `summary` | Generated and delivered report counts, delivery rate, open exceptions, open incidents, and audit readiness score. |
| `report_volume` | Generated and delivered counts by report ID. |
| `delivery_health` | Success, failure, retry, dead-letter, median delivery, and p95 delivery metrics. |
| `approval_latency` | Approval counts, pending count, latency, and SLO breach count. |
| `exception_aging` | Active, expiring, expired, median age, and oldest age metrics. |
| `evidence_room_access` | Active rooms, access events, downloads, failures, revocations, and watermarked downloads. |
| `incident_closure_slo` | Opened, closed, within-SLO, breached-SLO, and median closure metrics. |
| `audit_readiness_trend` | Period score and evidence gap trend rows. |

The KPI metrics contract excludes recipient addresses, auditor identity,
approver identity, IP addresses, download URLs, raw report content, customer
records, tenant drilldown records, secrets, and private tenant payloads. Private
Enterprise owns metric aggregation workers, tenant metrics storage, dashboard
projection, private trend history, RBAC filtering, and license enforcement.

## Alert Escalation Contract

Enterprise report-center alerts should turn KPI breaches and suspicious report
activity into routed, acknowledged, evidence-backed work. The public alert
escalation contract defines how threshold rules, trigger evaluations, routing,
escalation levels, acknowledgements, incident linkage, and immutable evidence
fit together without exposing operator identities or notification provider
payloads.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `alert_policy` | Policy ref, status, owner role, evaluation cadence, suppression window, and acknowledgement requirement. |
| `trigger_rules` | Failed delivery, suspicious access, aging exception, approval latency, and SLO rule metadata. |
| `evaluations` | Trigger status, observed value, severity, trigger time, and opaque correlation refs. |
| `routing` | Primary and secondary channels, integration refs, recipient redaction, and external-delivery approval requirement. |
| `escalation` | Current level, maximum level, next escalation time, owner roles, timeouts, and actions. |
| `acknowledgement` | Acknowledgement requirement, status, due time, owner role, and evidence ref. |
| `incident_linkage` | Incident requirement, incident ref, incident packet ref, and closure requirement. |
| `evidence` | Metrics ref, alert digest, routing audit ref, immutable-store ref, and evidence refs. |

The alert escalation contract excludes recipient addresses, operator identity,
auditor identity, approver identity, IP addresses, download URLs, raw report
content, provider responses, customer records, tenant drilldown records,
secrets, and private tenant payloads. Private Enterprise owns alert evaluation,
routing, escalation workers, notification delivery, incident creation,
acknowledgement and suppression stores, and license enforcement.

## Alert Operations Dashboard Contract

Enterprise report alert operations dashboards should let CSO, SOC, GRC, and
platform owners see whether alert handling is healthy without exposing private
tenant payloads. The public contract defines dashboard summary counters, queue
health, active alert rows, escalation health, acknowledgement SLOs, suppression
state, incident linkage health, routing health, evidence refs, and redaction
guarantees.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `dashboard` | Dashboard status, open alert counts, severity counts, overdue acknowledgements, suppressed alerts, incident linkage, and mean acknowledgement time. |
| `queues` | Alert evaluation, routing, escalation, acknowledgement, and incident creation queue depth and age. |
| `active_alerts` | Alert refs, rule IDs, severity, status, owner role, route ref, age, acknowledgement due time, and incident ref. |
| `escalation_health` | Active escalation counts by level, next escalation due time, and breached escalations. |
| `acknowledgement_slos` | Required, pending, overdue, acknowledged, median, and p95 acknowledgement metrics. |
| `suppression_summary` | Active suppressions, expired suppressions, review count, and audit coverage. |
| `incident_linkage_health` | Linked, unlinked, open, closure-required, and stale incident counts. |
| `routing_health` | Channel health, pending routes, and failed routes. |
| `evidence` | Dashboard digest, latest alert ref, routing audit ref, immutable store ref, and evidence refs. |

The alert operations dashboard contract excludes recipient addresses, operator
identity, auditor identity, approver identity, IP addresses, download URLs, raw
report content, provider responses, customer records, tenant drilldown records,
secrets, and private tenant payloads. Private Enterprise owns dashboard
projection, queue persistence, alert event storage, routing health checks,
acknowledgement, incident linkage and suppression stores, and license
enforcement.

## Alert Drilldown Contract

Enterprise report alert drilldowns should let an authorized CSO, SOC, GRC, or
platform owner inspect one alert without exposing raw report data or private
identities. The public contract defines alert summary metadata, ordered
timeline rows, routing history, acknowledgement history, suppression history,
escalation path, linked incident refs, evidence-chain refs, controls, and
redaction guarantees.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `alert` | Alert ref, rule ID, title, severity, status, owner role, source metric, observed value, and threshold. |
| `timeline` | Ordered detected, routed, acknowledged, escalated, suppressed, incident-linked, and closed events. |
| `routing` | Route refs, channels, owner roles, status, and delivery timestamps. |
| `acknowledgement_history` | Acknowledgement refs, status, owner role, due time, decision ref, and evidence ref. |
| `suppression_history` | Suppression refs, status, reason code, owner role, expiry, and audit ref. |
| `escalation_path` | Current level, next level, next escalation time, owner roles, and level status. |
| `linked_incident` | Incident requirement, incident ref, packet ref, closure ref, closure requirement, and incident status. |
| `evidence_chain` | Metrics ref, alert digest, routing audit ref, timeline digest, immutable-store ref, and evidence refs. |

The alert drilldown contract excludes recipient addresses, operator identity,
auditor identity, approver identity, IP addresses, download URLs, raw report
content, provider responses, customer records, tenant drilldown records,
secrets, and private tenant payloads. Private Enterprise owns drilldown
projection, timeline event storage, routing detail storage, acknowledgement and
suppression stores, incident linkage, evidence-chain storage, and license
enforcement.

## Alert Remediation Plan Contract

Enterprise report alert remediation plans should convert alert findings into
tracked work with owner roles, due dates, approval gates, evidence refs, closure
criteria, and post-incident control updates. The public contract defines plan
metadata, affected public-safe refs, tasks, approval requirements, closure
criteria, control updates, communications requirements, evidence refs, controls,
and redaction guarantees.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `plan` | Plan ref, status, priority, owner role, opened/due times, source alert ref, and source incident ref. |
| `scope` | Finding type, affected report/evidence-room/integration refs, and customer-record redaction guarantee. |
| `tasks` | Task refs, titles, owner roles, status, due dates, approval requirements, evidence requirements, and evidence refs. |
| `approval_requirements` | Approval refs, approval type, approver role, status, and due time. |
| `closure_criteria` | Task, approval, evidence-chain, incident-closure, and post-incident review requirements. |
| `control_updates` | Control refs, update type, owner roles, status, and evidence refs. |
| `communications` | Internal, executive, customer notification, and external message references. |
| `evidence` | Plan digest, alert drilldown ref, incident packet ref, closure manifest ref, immutable-store ref, and evidence refs. |

The remediation plan contract excludes recipient addresses, operator identity,
auditor identity, approver identity, IP addresses, download URLs, raw report
content, provider responses, customer records, private remediation details,
tenant drilldown records, secrets, and private tenant payloads. Private
Enterprise owns remediation workflow, task storage, approval workflow, owner
resolution, control update workflow, notification workflow, immutable plan
storage, and license enforcement.

## Alert Remediation Closure Contract

Enterprise report alert remediation closure should prove that alert findings
were resolved through completed tasks, final approvals, control updates,
residual-risk decisions, post-incident review, communications, and immutable
closure evidence. The public contract defines closure metadata, completed task
refs, final approval refs, control update outcomes, residual risk, review
outcomes, communications status, evidence refs, controls, and redaction
guarantees.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `closure` | Closure ref, source plan/alert/incident refs, final status, closed time, owner role, and residual risk level. |
| `completed_tasks` | Completed task refs, titles, owner roles, completion times, evidence refs, and approval refs. |
| `final_approvals` | Final approval refs, approval type, approver role, decision, decision time, and evidence refs. |
| `control_updates` | Control refs, update type, owner roles, final status, and evidence refs. |
| `residual_risk` | Risk level, acceptance status, accepting role, acceptance ref, review due time, and public-safe rationale. |
| `post_incident_review` | Review ref, completion status, completion time, facilitator role, lesson refs, and follow-up signal. |
| `communications` | Internal, executive, customer notification, and communication refs. |
| `evidence` | Closure digest, remediation plan ref, alert drilldown ref, incident packet ref, closure manifest, immutable-store ref, and evidence refs. |

The remediation closure contract excludes recipient addresses, operator
identity, auditor identity, approver identity, IP addresses, download URLs, raw
report content, provider responses, customer records, private remediation
details, tenant drilldown records, secrets, and private tenant payloads.
Private Enterprise owns closure workflow, approval identity resolution,
residual-risk storage, post-incident review storage, communication delivery,
immutable closure storage, evidence-chain storage, and license enforcement.

## Remediation Closure Operations Dashboard Contract

Enterprise remediation closure operations dashboards should give CSO, CISO,
GRC, and security operations users a public-safe aggregate view of closure
throughput, overdue remediation, residual-risk aging, approval bottlenecks,
post-incident review completion, closure SLOs, and recent closure evidence.
The public contract defines only aggregate and opaque-reference fields so
Community can document and validate the interface without exposing tenant
records or private remediation details.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `dashboard` | Closure readiness, closure counts, overdue tasks, overdue closures, due-soon closures, and close-time statistics. |
| `throughput` | Opened, closed, reopened, closure rate, and SLO met/breached counts for a reporting period. |
| `queues` | Closure approval, residual-risk review, post-incident review, and evidence finalization queue health. |
| `residual_risk_aging` | Accepted residual-risk totals, severity distribution, overdue reviews, and next review due time. |
| `approval_bottlenecks` | Pending closure approvals by approver role and age. |
| `post_incident_review_health` | Required, completed, overdue, completion rate, and follow-up counts. |
| `closure_slo` | Target close time, met/breached/at-risk counts, and SLO health. |
| `recent_closures` | Opaque closure refs, plan refs, source alert refs, owner roles, residual-risk level, close time, and evidence refs. |
| `evidence` | Dashboard digest, latest closure/plan refs, immutable-store ref, and evidence refs. |

The remediation closure operations dashboard excludes recipient addresses,
operator identity, auditor identity, approver identity, IP addresses, download
URLs, raw report content, provider responses, customer records, private
remediation details, tenant drilldown records, secrets, and private tenant
payloads. Private Enterprise owns closure operations projections, closure event
storage, SLO evaluation, residual-risk review storage, approval queue storage,
post-incident review storage, immutable dashboard storage, and license
enforcement.

## Remediation Closure Executive Digest Contract

Enterprise remediation closure executive digests should translate closure
operations into board, CSO, CISO, and audit-ready report metadata. The public
contract defines digest metadata, executive summary, closure metrics,
residual-risk summary, remediation queue health, board talking points, audit
readiness, distribution controls, evidence refs, controls, and redaction
guarantees.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `digest` | Digest ref, title, reporting period, audience, readiness status, prepared time, and public-safe visibility marker. |
| `executive_summary` | Headline, closure readiness, key message, material risk, and recommended executive action. |
| `metrics` | Closed/open plans, overdue closures/tasks, closure rate, SLO breaches, residual-risk acceptances, overdue reviews, and post-incident review completion rate. |
| `risk_summary` | Residual-risk level, high/critical residual-risk count, top risk themes, and next accepted-risk review due time. |
| `remediation_status` | Queue health for closure approvals, residual-risk review, post-incident review, evidence finalization, and closure SLOs. |
| `board_talking_points` | Public-safe bullets suitable for board/audit packet rendering. |
| `audit_readiness` | Auditor readiness, immutable evidence availability, exceptions count, report package refs, and evidence refs. |
| `distribution` | Future Enterprise formats, delivery modes, approval requirement, and recipient policy ref. |
| `evidence` | Digest ref, operations dashboard ref, latest closure ref, immutable-store ref, and evidence refs. |

The remediation closure executive digest excludes recipient addresses,
operator identity, auditor identity, approver identity, board member identity,
IP addresses, download URLs, raw report content, provider responses, customer
records, private remediation details, tenant drilldown records, secrets, and
private tenant payloads. Private Enterprise owns digest rendering, board-pack
rendering, tenant metrics storage, report delivery, approval workflow,
evidence-package building, and license enforcement.

## Remediation Closure Digest Distribution Contract

Enterprise remediation closure digest distribution should govern the final
approval, recipient policy, delivery readiness, and send evidence for CSO/CISO,
board, audit, and GRC report packs. The public contract defines approval-before-
send gates, recipient audience controls, delivery mode readiness, signed
manifest requirements, immutable send evidence, and redaction guarantees
without exposing recipient addresses or private report content.

The public contract includes:

| Section | Purpose |
| --- | --- |
| `distribution` | Distribution ref, digest ref, status, board-pack delivery window, prepared time, send-after time, and expiration time. |
| `approval` | Approval ref, approval type, approver role, approval status, due time, and approval evidence ref. |
| `recipient_governance` | Recipient policy ref, allowed audiences, external-recipient posture, domain allowlist requirement, RBAC scope requirement, and recipient-address redaction. |
| `delivery_plan` | Formats, delivery modes, provider refs, retry policy ref, watermark requirement, and signed manifest requirement. |
| `delivery_status` | Per-channel readiness for portal, email, and GRC upload delivery with delivery evidence refs. |
| `send_evidence` | Distribution digest, executive digest, manifest, immutable-store ref, and send evidence refs. |

The remediation closure digest distribution contract excludes recipient
addresses, operator identity, auditor identity, approver identity, board member
identity, IP addresses, download URLs, raw report content, provider responses,
customer records, private remediation details, tenant drilldown records,
secrets, and private tenant payloads. Private Enterprise owns approval
workflow, recipient directory, delivery providers, signed package building,
send workers, delivery audit storage, and license enforcement.

## Enterprise Trial Validation Packet

Enterprise Trial should produce a public-safe Report Center validation packet
that proves evaluator paths without exposing private implementation details.
The packet covers setup wizard, report rendering, policy-blocked send, approved
send, scheduled run, evidence room, alert escalation, remediation closure,
executive digest distribution, revocation, and retention verification.

The public packet includes:

| Section | Purpose |
| --- | --- |
| `validation_summary` | Overall trial validation status, path counts, evidence packet ref, and validation time. |
| `package_under_test` | Trial package ref, version, image ref, license status, validation mode, and source exclusion. |
| `validation_paths` | Per-path status, assertions, evidence refs, and public artifact refs. |
| `artifacts` | Validated schema names, packet digest ref, immutable-store ref, and operator dashboard ref. |
| `controls` | License, tenant scope, approval-before-send, recipient policy, retention, revocation, immutable evidence, and raw payload exclusion checks. |
| `redaction` | Proof that recipient addresses, private identities, IP addresses, download URLs, raw prompts, model reasoning, raw tool output, raw report content, provider responses, customer records, private remediation details, tenant drilldown records, secrets, and source code are excluded. |

Private Enterprise owns trial license validation, report rendering, delivery
workers, schedulers, evidence-room workers, alert evaluators, remediation
workflows, digest distribution workers, tenant stores, and the actual trial
package runtime.

## Enterprise Trial Operator Dashboard Readiness

Enterprise Trial operators should have a dashboard-ready contract that shows
the current validation packet status, failed or blocked paths, approval
blockers, evidence refs, operator actions, package/license state, and evaluator
handoff readiness. The public contract is metadata-only and excludes evaluator
identity, operator identity, recipient addresses, IP addresses, download URLs,
raw prompts, model reasoning, raw tool output, report content, provider
responses, customer records, tenant drilldown records, secrets, and source
code.

The public packet includes:

| Section | Purpose |
| --- | --- |
| `dashboard` | Dashboard ref, readiness status, review requirement, validation packet ref, refresh time, and next review due time. |
| `validation_rollup` | Path totals, pass/warn/block/fail counts, critical blocker count, handoff readiness, and packet ref. |
| `path_status` | Per-path status, operator state, and evidence refs. |
| `approval_blockers` | Open blocker metadata when a handoff cannot be approved. |
| `evidence_links` | Redacted evidence and artifact refs for operator review. |
| `operator_actions` | Recommended or available operator actions and approval requirements. |
| `evaluator_handoff` | Handoff state, package access state, license state, support state, and expiry. |

The public API/view-model contract adds expected private portal routes,
operator actions, UI sections, state transitions, and required audit events for
`GET /dashboard`, `GET /validation-packet/{packet_ref}`,
`POST /handoffs/{handoff_ref}/approve`, and
`POST /validation-runs/{run_ref}/rerun`. The contract is public-safe and does
not implement those endpoints in Community.

Private Enterprise owns the operator dashboard API, operator session store,
trial validation store, handoff workflow, package access service, license
service, support queue, and audit store.

## Enterprise Trial Evaluator Handoff Packet

Enterprise Trial evaluator handoff should give approved evaluators a clear
metadata-only packet describing trial state, setup steps, package access
status, license status, support state, expiry, and revocation posture. The
public contract excludes evaluator identity, operator identity, package tokens,
license keys, download URLs, IP addresses, raw prompts, model reasoning, raw
tool output, report content, provider responses, customer records, tenant
drilldown records, secrets, and source code.

The public packet includes:

| Section | Purpose |
| --- | --- |
| `evaluator_experience` | Approved evaluator state, audience, setup duration, instructions ref, and setup steps. |
| `package_access` | Registry provider, opaque package ref, access state, required permissions, expiry, and proof that image refs, package tokens, and download URLs are excluded. |
| `license_status` | Opaque license ref, trial status, issue/expiry times, revocation state, and proof that license keys are excluded. |
| `support` | Metadata-only support state, channel labels, response SLO, and opaque support ticket ref. |
| `revocation` | Revocation support, current state, opaque revocation ref, blocked-after-revocation flag, and audit requirement. |
| `onboarding_checks` | Operator approval, package access, license, and validation-packet readiness checks with redacted evidence refs. |

Private Enterprise owns trial portal rendering, package access grants, license
creation and validation, revocation enforcement, support queue integration,
and immutable audit storage.

## Enterprise Trial Revocation And Expiry Evidence

Enterprise Trial revocation and expiry evidence should prove that trial access
is blocked after operator revocation or automatic expiry. The public contract
captures metadata-only checks for license validation, package pulls, trial
portal access, Enterprise report rendering, and support handoff access. It
excludes evaluator identity, operator identity, package tokens, license keys,
download URLs, IP addresses, provider responses, customer records, tenant
drilldown records, secrets, source code, and raw payloads.

The public packet includes:

| Section | Purpose |
| --- | --- |
| `revocation_expiry` | Trigger, state, reason code, opaque approval ref, and audit ref. |
| `blocked_access_checks` | Expected and actual blocked results for license, package, portal, report, and support surfaces. |
| `access_state` | Final revoked or expired state for license, package, portal, support, and handoff surfaces. |
| `audit_chain` | Immutable request, revocation, and blocked-access verification events. |
| `operator_summary` | Blocked check count, failure count, follow-up state, and evidence readiness. |

Private Enterprise owns license blocking, package registry access revocation,
trial portal enforcement, support queue closure, and immutable audit storage.

## Enterprise Trial Lab Notebook Outline

The Enterprise Trial lab notebook outline should define the public-safe Wiki
textbook structure for approved evaluators after AISPM reaches production-ready
status. It captures chapters, role-specific labs, screenshots, diagrams, flow
charts, verification checkpoints, and evidence refs without exposing
Enterprise source code, license secrets, package URLs, private fixtures,
customer data, identities, IP addresses, raw prompts, model reasoning, raw tool
output, provider responses, tenant drilldown records, or secrets.

The public outline includes:

| Section | Purpose |
| --- | --- |
| `notebook` | Audience, publication target, status, estimated duration, and public-safe requirements. |
| `chapters` | Orientation, trial access, agent enforcement, AISPM dashboard, report center, and closeout structure. |
| `labs` | Role-specific exercises with expected duration, checkpoint refs, and redacted evidence refs. |
| `visual_assets` | Required screenshot, diagram, and flow-chart assets for the future Wiki notebook. |
| `verification_checkpoints` | Expected outcomes and evidence refs for trial setup, policy decisions, and revocation checks. |
| `role_paths` | Developer, auditor, and CSO/CISO lab paths. |

Private Enterprise owns live trial portal content, package access, license
service behavior, and any private lab fixtures used during customer trials.

## Enterprise Trial Lab Notebook Publication Readiness

The lab notebook publication readiness packet is the public-safe gate before a
trial-user textbook is copied into the GitHub Wiki. It verifies that every
required Wiki page has navigation, link-health coverage, redacted screenshots,
diagrams, flow charts, and checkpoint evidence before publication.

The public packet includes:

| Section | Purpose |
| --- | --- |
| `publication_readiness` | Release gate, Wiki target, required reviews, and no-private-artifact requirement. |
| `wiki_pages` | Required Wiki pages, source refs, navigation requirements, link checks, asset refs, and checkpoint refs. |
| `visual_assets` | Screenshot, diagram, and flow-chart assets that must be public-safe and have alt text. |
| `link_checks` | Public docs, trial portal, and repository links that must be reachable before release. |
| `navigation_checks` | Wiki navigation entries that must include the notebook pages. |
| `checkpoint_evidence` | Redacted evidence refs proving lab outcomes without exposing trial secrets. |

Publication readiness is validated by
`scripts/validate-aispm-trial-lab-notebook.py`, which checks the readiness
packet schema, Wiki source files, `docs/wiki/Home.md` navigation, required
public-safety sections, public-safe visual asset metadata, and required
acceptance criteria. The validator runs in Community CI and Release Community
workflows so future public releases cannot drift from the notebook readiness
packet.

Reviewer-facing readiness summaries are generated at
`docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md`
and
`docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json`.
They show the checked pages, navigation status, public-safety section status,
visual asset status, acceptance criteria, and remaining blockers.

Private Enterprise owns private screenshot capture, customer-specific lab
fixtures, package access verification, license validation, and any non-public
operator evidence used during trial publication review.

## Acceptance Criteria

The report center is production-ready when:

- Community downloads render from public-safe posture data;
- Enterprise report rendering supports tenant branding and common formats;
- email delivery is tenant-scoped and RBAC-controlled;
- recipient allowlists and approval gates are enforced;
- all deliveries emit immutable audit evidence;
- failed deliveries are retryable and visible in operations dashboards;
- retention, legal hold, archive, and deletion workflows are visible and
  backed by immutable evidence;
- report search and retrieval are retention-aware, RBAC-scoped, and audited;
- export packages carry signed manifests, artifact digests, evidence refs, and
  retention classes;
- recurring report schedules enforce approval, blackout, retry, and recipient
  governance policies;
- recipient policies enforce domain allowlists, delivery-channel eligibility,
  encryption requirements, and external-recipient approvals;
- approval decisions for sends, schedule changes, new domains, and external
  delivery exceptions are immutable and evidence-backed;
- report exceptions expire, renew, revoke, and close through evidence-backed
  lifecycle events;
- trial operator dashboard readiness exposes validation rollup, blockers,
  evidence links, operator actions, and evaluator handoff state with
  public-safe redaction;
- trial operator dashboard API/view-model output maps readiness packets to
  authenticated private portal routes, UI sections, approval actions, state
  transitions, and immutable audit events;
- trial evaluator handoff packets expose setup steps, package access status,
  trial license status, support state, expiry, and revocation posture without
  exposing package URLs, license keys, identities, secrets, or source code;
- trial revocation and expiry evidence proves license validation, package
  access, trial portal access, report rendering, and support handoff are
  blocked after revocation or expiry;
- trial lab notebook outlines define public-safe chapters, role paths, labs,
  screenshots, diagrams, flow charts, and verification checkpoints for the
  future Wiki trial textbook;
- trial lab notebook publication readiness verifies Wiki navigation, link
  health, redacted screenshots, diagrams, flow charts, checkpoint evidence, and
  required reviews before public Wiki publication;
- evidence rooms provide scoped, expiring, watermarked report access with
  immutable access logs;
- evidence room access events record view, download, revocation, expiry, failed
  authentication, failed policy, and watermark actions with digest-chain refs;
- incident packets bundle exceptions, approvals, access events, affected
  artifacts, chain-of-custody evidence, and review state without exposing raw
  report content;
- incident closure records capture remediation, approval, lessons learned,
  follow-up tasks, and immutable closure evidence before closure;
- KPI metrics aggregate report volume, delivery health, approval latency,
  exception aging, evidence-room access, incident closure SLOs, and audit
  readiness trends without exposing tenant drilldown records;
- alert escalation turns failed-delivery spikes, suspicious evidence-room
  access, aging exceptions, approval latency breaches, and SLO breaches into
  routed, acknowledged, incident-linked, immutable evidence;
- alert operations dashboards expose active alerts, escalation queues, overdue
  acknowledgements, suppressions, incident linkage, and routing health through
  RBAC-scoped public-safe metadata;
- alert drilldowns expose a single alert timeline, routed owner roles,
  acknowledgement and suppression history, linked incident refs, and evidence
  chain without exposing private identities or payloads;
- alert remediation plans assign owner-scoped tasks, approval gates, due dates,
  closure criteria, control updates, and immutable evidence for alert findings;
- alert remediation closures record completed tasks, final approvals,
  residual risk, post-incident review outcomes, communications, and immutable
  closure evidence;
- remediation closure operations dashboards expose aggregate closure
  throughput, overdue remediation, residual-risk aging, approval bottlenecks,
  post-incident review health, closure SLOs, and immutable dashboard evidence;
- remediation closure executive digests summarize closure readiness, material
  residual risk, board talking points, audit readiness, distribution controls,
  and immutable digest evidence without exposing private tenant records;
- remediation closure digest distribution enforces approval-before-send,
  recipient governance, delivery readiness, signed manifests, immutable send
  evidence, and redaction guarantees;
- setup docs clearly separate public settings from secret-manager references.

## Private Enterprise Next Step

The private `cavra-enterprise` repository should implement the contract with:

```text
src/cavra_enterprise/
  aispm_reports/
    api.py
    catalog.py
    renderer.py
    delivery.py
    scheduler.py
    audit.py
    distribution.py
    setup.py
```

The public Community repository should only receive schema-compatible examples,
operator documentation, and public-safe dashboard affordances.
