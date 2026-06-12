# Private Enterprise Repo Plan

Recommended private repository: `Huzefaaa2/cavra-enterprise`

Status: created as a private GitHub repository.

Initial private implementation status:

- Python package `cavra_enterprise`
- private pilot-intake tenant store
- encrypted-at-rest payload codec
- customer/SaaS KMS-style envelope encryption contract
- authenticated update authorization
- production SSO claim binding
- managed tenant database adapter contract
- CRM/ITSM/GRC/customer-success/tenant-management handoff workers
- provider-native Salesforce, HubSpot, Jira, ServiceNow, and Archer payload adapters
- immutable audit export and retention enforcement
- provider-specific OAuth, bearer, API-key, and basic-token auth providers
- retryable provider rate-limit handling
- immutable object storage adapter contracts and local validation storage
- AWS S3, Azure Blob, and Google Cloud Storage provider-package boundaries
- cloud object-lock deployment recipes and archive health validation
- scheduled archive health workers and operator alert routing
- alert delivery connector contracts and local delivery validation
- email, ChatOps, SIEM, ITSM, and pager delivery provider-package boundaries
- archive health dashboard persistence, retry planning, and operator acknowledgements
- HTTP alert transport packages with runtime endpoint validation and retry handling
- JSON-backed archive health dashboard API persistence and query helpers
- managed database-backed archive health dashboard persistence
- live provider alert transport adapters for Slack, Teams, Splunk HEC, Jira, ServiceNow, and PagerDuty
- production deployment wiring for archive alert dashboard storage, transport selection, retry policy, and readiness validation
- archive alert deployment runbook helpers, Kubernetes examples, Helm values, and provider smoke-test guidance
- archive alert smoke-test execution jobs and post-delivery dashboard assertions
- archive alert smoke-test scheduling, evidence export, and customer-facing deployment verification reports
- archive alert verification report delivery routing and customer-success handoff automation
- audit-event persistence
- connector handoff dispatcher interfaces
- private CI workflow

Repository hardening status:

- Dependabot vulnerability alerts: enabled
- squash-only merge policy and delete-branch-on-merge: enabled
- branch protection and secret scanning: blocked by the current GitHub plan for private repositories

Suggested structure:

```text
cavra-enterprise/
  src/cavra_enterprise/
    aispm_ingestion/
    aispm_reports/
    identity/
    pilot_intake/
    sso/
    rbac/
    audit/
    dashboard/
    policy_approval/
    compliance_reports/
    ai_remediation/
    drift_monitoring/
    license_server_client/
  policy_packs/
    pci_dss/
    cis/
    azure_landing_zone/
    aws_control_tower/
    fca_emoney/
  docker/Dockerfile.enterprise
  charts/helm/
  .github/workflows/
```

The private package can plug into public CAVRA through dynamic import of
`cavra_enterprise`, Enterprise plugin manifests, private Docker images, and
private license validation.

AISPM report delivery implementation should live under
`src/cavra_enterprise/aispm_reports/` with private catalog, renderer, delivery,
scheduler, audit, and setup modules. It must implement the public-safe contract
documented in `docs/architecture/aispm-report-center.md`,
`src/cavra/schemas/aispm-report-delivery-contract.schema.json`, and
`examples/aispm/enterprise-report-delivery-contract-public.example.json`.
The setup wizard should also implement
`src/cavra/schemas/aispm-report-setup-wizard-contract.schema.json` and
`examples/aispm/enterprise-report-setup-wizard-contract-public.example.json`.
Delivery audit persistence should implement
`src/cavra/schemas/aispm-report-delivery-audit-event.schema.json` and
`examples/aispm/enterprise-report-delivery-audit-event-public.example.json`.
The report operations dashboard should implement
`src/cavra/schemas/aispm-report-operations-dashboard.schema.json` and
`examples/aispm/enterprise-report-operations-dashboard-public.example.json`.
The report retention lifecycle should implement
`src/cavra/schemas/aispm-report-retention-lifecycle.schema.json` and
`examples/aispm/enterprise-report-retention-lifecycle-public.example.json`.
The report search and evidence retrieval flow should implement
`src/cavra/schemas/aispm-report-search-retrieval.schema.json` and
`examples/aispm/enterprise-report-search-retrieval-public.example.json`.
The report export package manifest flow should implement
`src/cavra/schemas/aispm-report-export-package-manifest.schema.json` and
`examples/aispm/enterprise-report-export-package-manifest-public.example.json`.
The report schedule policy flow should implement
`src/cavra/schemas/aispm-report-schedule-policy.schema.json` and
`examples/aispm/enterprise-report-schedule-policy-public.example.json`.
The report recipient policy flow should implement
`src/cavra/schemas/aispm-report-recipient-policy.schema.json` and
`examples/aispm/enterprise-report-recipient-policy-public.example.json`.
The report approval decision flow should implement
`src/cavra/schemas/aispm-report-approval-decision.schema.json` and
`examples/aispm/enterprise-report-approval-decision-public.example.json`.
The report exception lifecycle flow should implement
`src/cavra/schemas/aispm-report-exception-lifecycle.schema.json` and
`examples/aispm/enterprise-report-exception-lifecycle-public.example.json`.
The report evidence room flow should implement
`src/cavra/schemas/aispm-report-evidence-room.schema.json` and
`examples/aispm/enterprise-report-evidence-room-public.example.json`.
The evidence room access event flow should implement
`src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json` and
`examples/aispm/enterprise-report-evidence-room-access-event-public.example.json`.
The report incident packet flow should implement
`src/cavra/schemas/aispm-report-incident-packet.schema.json` and
`examples/aispm/enterprise-report-incident-packet-public.example.json`.
The report incident closure flow should implement
`src/cavra/schemas/aispm-report-incident-closure.schema.json` and
`examples/aispm/enterprise-report-incident-closure-public.example.json`.
The report KPI metrics flow should implement
`src/cavra/schemas/aispm-report-kpi-metrics.schema.json` and
`examples/aispm/enterprise-report-kpi-metrics-public.example.json`.
The report alert escalation flow should implement
`src/cavra/schemas/aispm-report-alert-escalation.schema.json` and
`examples/aispm/enterprise-report-alert-escalation-public.example.json`.
The report alert operations dashboard flow should implement
`src/cavra/schemas/aispm-report-alert-operations-dashboard.schema.json` and
`examples/aispm/enterprise-report-alert-operations-dashboard-public.example.json`.
The report alert drilldown flow should implement
`src/cavra/schemas/aispm-report-alert-drilldown.schema.json` and
`examples/aispm/enterprise-report-alert-drilldown-public.example.json`.
The report alert remediation plan flow should implement
`src/cavra/schemas/aispm-report-alert-remediation-plan.schema.json` and
`examples/aispm/enterprise-report-alert-remediation-plan-public.example.json`.
The report alert remediation closure flow should implement
`src/cavra/schemas/aispm-report-alert-remediation-closure.schema.json` and
`examples/aispm/enterprise-report-alert-remediation-closure-public.example.json`.
The report remediation closure operations dashboard flow should implement
`src/cavra/schemas/aispm-report-remediation-closure-operations-dashboard.schema.json` and
`examples/aispm/enterprise-report-remediation-closure-operations-dashboard-public.example.json`.
The report remediation closure executive digest flow should implement
`src/cavra/schemas/aispm-report-remediation-closure-executive-digest.schema.json` and
`examples/aispm/enterprise-report-remediation-closure-executive-digest-public.example.json`.
The report remediation closure digest distribution flow should implement
`src/cavra/schemas/aispm-report-remediation-closure-digest-distribution.schema.json` and
`examples/aispm/enterprise-report-remediation-closure-digest-distribution-public.example.json`.
The AISPM Report Center Enterprise readiness checklist is tracked in
`docs/architecture/aispm-report-center-enterprise-readiness.md` and
`docs/wiki/AISPM-Report-Center-Enterprise-Readiness.md`.
The AISPM Report Center Enterprise Trial validation packet is tracked in
`src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json` and
`examples/aispm/enterprise-report-center-trial-validation-packet-public.example.json`.
The AISPM Report Center trial operator dashboard readiness contract is tracked
in
`src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json`
and
`examples/aispm/enterprise-report-center-trial-operator-dashboard-readiness-public.example.json`.
The AISPM Report Center trial operator dashboard API/view-model contract is
tracked in
`src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json`
and
`examples/aispm/enterprise-report-center-trial-operator-api-view-model-public.example.json`.
The AISPM Report Center trial evaluator handoff packet is tracked in
`src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json`
and
`examples/aispm/enterprise-report-center-trial-evaluator-handoff-packet-public.example.json`.
The AISPM Report Center trial revocation and expiry evidence contract is
tracked in
`src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json`
and
`examples/aispm/enterprise-report-center-trial-revocation-expiry-evidence-public.example.json`.
The AISPM Report Center trial lab notebook outline contract is tracked in
`src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json`
and
`examples/aispm/enterprise-report-center-trial-lab-notebook-outline-public.example.json`.
The AISPM Report Center trial lab notebook publication readiness contract is
tracked in
`src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json`
and
`examples/aispm/enterprise-report-center-trial-lab-notebook-publication-readiness-public.example.json`.
