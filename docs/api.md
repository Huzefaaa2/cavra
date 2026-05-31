# API

CAVRA API exposes health, version, policy packs, decisions, sessions, agents, repositories, approvals, evidence, integrations, MCP trust, risk events, compliance mappings, and sandbox endpoints. OpenAPI title: CAVRA API.

## Activity Persistence

Activity endpoints:

- `GET /sessions`: list persisted runtime sessions with optional `agent_id`, `repository`, `policy_pack`, `state`, `limit`, and `offset` filters.
- `POST /sessions`: create or update a session summary.
- `GET /sessions/{session_id}`: fetch one session summary.
- `GET /decisions`: list persisted decisions with optional `session_id`, `agent_id`, `repository`, `policy_pack`, `decision`, `severity`, `action_type`, `limit`, and `offset` filters.
- `POST /decisions`: evaluate an action and persist the resulting decision.
- `GET /decisions/{decision_id}`: fetch one decision.

Default activity path: `.cavra/api/activity.json`.

Set `CAVRA_ACTIVITY_STORE` to override the JSON path. Set `CAVRA_ACTIVITY_DB` to use SQLite-backed activity persistence. `GET /console/config` includes `activity_mode`.

## Repository Inventory and Policy Rollout

Repository inventory endpoints:

- `GET /repositories`: list governed repositories with optional `provider`, `owner`, `policy_pack`, `status`, and `risk_tier` filters.
- `POST /repositories`: create or update a repository inventory record.
- `GET /repositories/{repository_id}`: fetch one repository inventory record. The route supports slash-delimited repository names such as `payments/api`.

Policy rollout endpoints:

- `GET /policy-rollouts`: list policy rollout records with optional `repository`, `policy_pack`, `state`, `mode`, and `owner` filters.
- `POST /policy-rollouts`: create or update a policy rollout record.
- `POST /policy-rollouts/change-plan`: preview a rollout create/update operation with before/after state, risk, approval requirement, and field-level changes.
- `POST /policy-rollouts/apply-change`: persist a rollout change plan. When OIDC or RBAC is configured, verified actor context is required.
- `GET /policy-rollouts/{rollout_id}`: fetch one policy rollout record.
- `GET /policy-rollout-details/{rollout_id}`: fetch one policy rollout with repository context, policy pack metadata, activity summary, integration summary, and readiness checks.

Default inventory path: `.cavra/api/inventory.json`.

Set `CAVRA_INVENTORY_STORE` to override the JSON path. Set `CAVRA_INVENTORY_DB` to use SQLite-backed repository inventory and policy rollout persistence. `GET /console/config` includes `inventory_mode`.

Inventory records track repository ID, provider, owner, business unit, environment, active policy pack, risk tier, status, protected branches, required checks, and evidence references. Rollout records track repository, policy pack, policy version, rollout mode, rollout state, owner, coverage percentage, last evaluation time, and evidence references.

## Policy Pack Authoring

Policy authoring endpoints:

- `GET /policy-pack-catalog`: list installed policy packs with rule-count summaries.
- `POST /policy-packs/draft`: build and validate a policy pack draft without writing to the policy directory.
- `POST /policy-packs/publish-plan`: preview create/update write-back risk, diff, target path, and approval requirement for a draft.
- `POST /policy-packs/publish-request`: create a digest-bound approval request for policy write-back.
- `POST /policy-packs/publish`: write `policy.yaml` and `policy.yaml.sig.json` only after the matching approval is approved or break-glass.

Policy drafts return schema validation errors, generated policy data, rule-count summaries, and operator notes. Publish requests bind the approval to the draft policy digest. Publishing rejects pending approvals, denied approvals, and approvals created for a different draft digest. Set `CAVRA_POLICY_DIR` to control the write-back root and `CAVRA_POLICY_SIGNING_KEY` to create HMAC-backed signature metadata.

## Console Security Boundary

Security boundary endpoint:

- `GET /console/security-boundary`: return console/API deployment boundary status for OIDC, repository RBAC, CORS, browser-visible permissions, and operator notes.
- `GET /console/session`: validate an optional `Authorization: Bearer` OIDC token and return actor context, repository-scoped permissions, and console permission flags.

The security boundary endpoint is read-only and reports whether `CAVRA_APPROVAL_OIDC_CONFIG`, `CAVRA_APPROVAL_RBAC_FILE`, and `CAVRA_CORS_ORIGINS` are configured. `GET /console/session` validates signed OIDC context when a bearer token is supplied. When OIDC or RBAC is configured, approval decisions and break-glass console mutations require verified actor context from a bearer token, `actor_token`, or `actor_claims`.

## Integrations Inventory

Integration endpoints:

- `GET /integrations`: list enterprise integration records with optional `provider`, `category`, `status`, `owner`, `environment`, and `health_status` filters.
- `POST /integrations`: create or update an integration record.
- `GET /integrations/{integration_id}`: fetch one integration record.
- `POST /integrations/{integration_id}/deliver`: send an event through the integration provider using `CAVRA_CONNECTOR_CONFIG` and return redacted delivery evidence.

Default integration path: `.cavra/api/integrations.json`.

Set `CAVRA_INTEGRATION_STORE` to override the JSON path. Set `CAVRA_INTEGRATION_DB` to use SQLite-backed integration inventory persistence. `GET /console/config` includes `integration_mode`.

Integration records track provider, category, owner, environment, auth mode, endpoint reference, status, health status, capabilities, scoped repositories, last check time, and evidence references.

Set `CAVRA_CONNECTOR_CONFIG` to enable live connector execution for Splunk, Sentinel, Datadog, Slack, Teams, Jira, ServiceNow, and generic webhooks. Delivery responses use `cavra.connector.delivery.v1` and redact authorization headers, API keys, Slack webhook URLs, and query strings.

## Persistent API Operations

Read-only operations endpoints:

- `GET /operations/stores`: list active persistent API store paths, modes, configuration sources, existence, and size.
- `GET /operations/retention-plan`: return a retention, backup, and restore-test plan for persistent API stores. Optional query parameters are `retention_days`, `classification`, and `legal_hold`.
- `GET /deployment/production-readiness`: validate production controls for OIDC, RBAC, CORS, evidence artifact retrieval, policy catalog availability, persistent store presence, optional Go backend promotion, rollback, drill history, and drill schedule readiness.
- `GET /runtime/go-pilot/rollback-drill-schedule`: inspect recurring rollback drill cadence, next due date, stale state, owners, and notification routes.
- `POST /runtime/go-pilot/rollback-drill-notifications/deliver`: deliver stale or due-soon rollback drill notifications through configured connectors and index redacted delivery evidence; accepts optional public-safe `routing_policy` with owner routes, maintenance windows, and owner calendars.
- `POST /runtime/go-pilot/rollback-drill-notifications/{schedule_id}/acknowledgements`: record public-safe acknowledgement, dismissal, escalation, or resolution metadata for a drill notification route; when OIDC or RBAC is configured, this endpoint requires verified console actor context and records that actor as `acknowledged_by`.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk`: record acknowledgement, escalation, dismissal, or resolution metadata for up to 100 drill notification routes.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package`: build and persist a public-safe acknowledgement audit package with route state, actor, notes, and external references.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery`: build an acknowledgement audit package, create a public-safe scheduled delivery plan, route it through configured SIEM/ITSM/ChatOps connectors, and index redacted connector delivery evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plan`: create a governed retry plan from failed acknowledgement audit delivery metadata.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run`: run the scheduled acknowledgement audit delivery retry worker. The worker defaults to dry-run mode; non-dry-run execution records are persisted only for approved retry decisions and may use `retry_policy.allow_immediate_retry=true` for approved manual retries.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-runs`: list persisted acknowledgement audit delivery worker run metadata with optional `dry_run` filtering.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-dashboard`: summarize worker runs, dry-runs, executed runs, retryable deliveries, and selected retry deliveries.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health`: evaluate missed worker runs, stale retry metadata, retryable deliveries, connector failures, and recommended recovery actions.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/deliver`: route public-safe worker health alerts through configured connectors and index redacted delivery evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/{health_id}/acknowledgements`: record review state for a worker health alert provider.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts`: list worker health alert plans, health alert acknowledgements, and alert connector delivery records.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alert-dashboard`: summarize worker health alert delivery, acknowledgements, outstanding review, and suppression.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plans/{retry_plan_id}/acknowledgements`: record accepted, deferred, escalated, resolved, or dismissed retry decision review evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plan`: create approval plans for acknowledged retry decisions before live retry execution.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plans/{approval_plan_id}/decisions`: record approved, denied, deferred, or expired retry execution decisions.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbook`: build public-safe SIEM, ITSM, ChatOps, and webhook recovery playbooks from repeated connector failures.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbooks/{playbook_id}/closures`: record public-safe connector recovery closure evidence with state, actor, external reference, and verification references.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-recovery-report`: summarize retry execution health, provider recovery SLOs, open recoveries, SLO breaches, and closure trends.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalation-plan`: create public-safe recovery escalation plans from failed retry executions, open recoveries, and breached recovery SLOs.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/deliver`: deliver recovery escalation notifications through configured connectors and persist redacted delivery evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/acknowledgements`: record public-safe acknowledgement state for a recovery escalation provider.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-plan`: create retry plans for failed recovery escalation connector deliveries.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-worker-run`: run the dry-run-default recovery escalation retry worker; live execution requires an accepted, acknowledged, or resolved escalation acknowledgement and persists execution records.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health`: summarize recovery escalation retry worker freshness, stale retry metadata, acknowledgement gaps, failed retry execution records, and disabled schedules.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/deliver`: route public-safe recovery retry health alerts through configured connectors and index redacted delivery evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/{health_id}/acknowledgements`: record review state for a recovery retry health alert provider.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts`: list recovery retry health alert plans, acknowledgements, and connector delivery records.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alert-dashboard`: summarize recovery retry health alert delivery, acknowledgements, outstanding review, and suppression.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report`: build leadership-ready recovery status reports with key risks, provider summaries, closure trends, and recommended actions.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-run`: generate scheduled executive recovery report runs and persist report metadata.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-runs/{run_id}/deliver`: deliver a scheduled executive recovery report summary through configured connectors and index redacted delivery evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-plan`: create retry, wait, or suppress decisions for failed scheduled executive report delivery records.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-worker-run`: run dry-run-default executive report delivery retry automation and persist live execution records when `execute=true`.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health`: report missed executive retry workers, stale executive retry plans, failed executive report deliveries, and failed executive retry execution records.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-plan`: create retry, wait, or suppress decisions for failed recovery retry health alert delivery records.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-worker-run`: run dry-run-default recovery retry health alert redelivery automation and persist execution records when `execute=true`.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/deliver`: deliver executive retry health alerts through configured connectors and index redacted delivery evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/{health_id}/acknowledgements`: acknowledge executive retry health alert review outcomes.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts`: list executive retry health alert plans, acknowledgements, and delivery evidence.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alert-dashboard`: summarize executive retry health alert delivery, acknowledgements, and outstanding reviews.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-plan`: create retry, wait, or suppress decisions for failed executive retry health alert delivery records.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-worker-run`: run dry-run-default executive retry health alert redelivery automation and persist execution records when `execute=true`.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closure-dashboard`: summarize final rollback drill reporting closure state, open reporting blockers, and recommended operator actions.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness`: generate and optionally persist the public-safe release-readiness summary for final rollback drill reporting closure.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-operator-runbook-export`: generate and persist a public-safe operator runbook export with Markdown content for the final reporting package.
- `GET /runtime/go-pilot/rollback-drill-notifications`: search rollback drill notification plans, redacted delivery records, acknowledgements, escalation plans, acknowledgement audit packages, acknowledgement audit delivery plans, retry plans, worker runs, retry execution records, recovery playbooks, recovery closures, recovery escalation retry health, recovery retry health alerts, recovery health alert retry worker records, executive report delivery retry plans, executive retry worker runs, executive retry health alerts, recovery escalation retry executions, and executive report deliveries.
- `GET /runtime/go-pilot/rollback-drill-notifications/dashboard`: summarize drill notification delivery, acknowledgement, and outstanding route counts.
- Rollback drill notification history supports `connector_delivery_source`, `delivery_success`, `alert_level`, `audit_id`, `delivery_id`, and `cadence` filters; the dashboard includes acknowledgement audit delivery health, success rate, failed audit delivery count, destination provider summaries, retry-plan count, retryable count, retry acknowledgement count, retry execution approval count, live retry execution record counts, connector recovery closure counts, retry recovery report counts, recovery escalation route counts, recovery escalation acknowledgement counts, recovery escalation retry counts, recovery escalation retry health alert counts, recovery retry health alert delivery counts, recovery health alert retry-plan and retry-worker counts, recovery executive report counts, scheduled executive report counts, executive delivery retry plan counts, executive retry worker counts, executive retry execution outcomes, executive retry health counts, executive retry health alert delivery counts, executive health alert retry-plan and retry-worker counts, final closure dashboard state, release-readiness summary count, operator runbook export count, worker run count, worker dry-run count, worker health alert count, and worker health acknowledgement count.
- `GET /runtime/go-pilot/rollback-drill-notifications/routes`: flatten persisted notification plan route decisions with optional `schedule_id`, `provider`, `owner`, `action`, and `category` filters.
- `GET /runtime/go-pilot/rollback-drill-notifications/suppression-trends`: summarize and persist public-safe routing suppression trends by category, owner, provider, and schedule.
- `POST /runtime/go-pilot/rollback-drill-notifications/escalation-plan`: generate a missed-notification escalation plan from acknowledgement SLO policy.

Backup and restore are intentionally CLI-only through `cavra ops backup` and `cavra ops restore` so the unauthenticated demo API does not gain file-system restore authority.

## Agent and MCP Registry

Registry endpoints:

- `GET /agents`: list governed AI-agent identities with optional `status` and `owner` filters.
- `GET /agents/profiles`: list predefined profiles for Claude Code, Codex, Copilot, Cursor, Gemini CLI, and AWS Q Developer.
- `POST /agents`: create or update an agent identity.
- `GET /agents/{agent_id}`: fetch one agent identity.
- `GET /mcp/servers`: list MCP server trust records with optional `trust_tier`, `approval_state`, and `capability` filters.
- `POST /mcp/servers`: create or update an MCP server trust record.
- `GET /mcp/servers/{server_id}`: fetch one MCP server trust record.
- `GET /mcp/tool-classifications`: list MCP capability classifications for filesystem, shell, network, database, SaaS, cloud, and repository tools.
- `GET /mcp/trust`: evaluate a server, tool, and capability against the MCP Trust Registry.

Default registry path: `.cavra/api/registry.json`.

Set `CAVRA_REGISTRY_STORE` to override the registry JSON path.

Set `CAVRA_REGISTRY_DB` to use SQLite-backed registry persistence. `GET /console/config` includes `registry_mode`. When the registry is configured, `/decisions` uses registry-backed MCP trust decisions for `mcp_tool_call` actions.

## Evidence Metadata

Evidence metadata endpoints:

- `GET /evidence`: list persisted evidence metadata.
- `POST /evidence`: upsert metadata by `session_id`.
- `GET /evidence/{session_id}`: fetch one metadata record.
- `GET /evidence/{session_id}/artifacts`: list downloadable evidence bundle artifacts for an indexed session.
- `GET /evidence/{session_id}/artifacts/{artifact_name}`: download one allowlisted evidence artifact.
- `GET /evidence/{session_id}/artifact-bundle`: download an allowlisted ZIP bundle for the session.
- `POST /evidence/{session_id}/promotion-request`: create a signed pending approval request for a managed endpoint rollout that is ready for promotion.

Default metadata path: `.cavra/api/evidence-metadata.json`.

Set `CAVRA_EVIDENCE_METADATA_STORE` to override the metadata store path for local or self-hosted deployments.

Set `CAVRA_EVIDENCE_METADATA_DB` to use SQLite-backed metadata persistence. `GET /evidence` supports query parameters in both JSON and SQLite modes:

- `session_id`
- `signer`
- `min_blocked`
- `has_approvals`
- `limit`
- `offset`

For security, the API does not accept arbitrary server-side bundle paths. Use `cavra evidence index` locally to extract metadata from a bundle, then persist the resulting metadata with `POST /evidence`.

Set `CAVRA_EVIDENCE_ARTIFACT_ROOT` to enable hosted artifact retrieval. The artifact root is expected to contain one directory per indexed session, managed endpoint rollout, or endpoint-management export. Retrieval endpoints require metadata to exist, only serve known bundle filenames, reject path traversal, and include `x-cavra-artifact-sha256` on downloads. Endpoint-management export downloads are checksum-verified before the API serves provider files. Rollout promotion requests require `CAVRA_ROLLOUT_PROMOTION_SIGNING_KEY` or `CAVRA_GO_RELEASE_SIGNING_KEY`. Rollout promotion executions post to `/evidence/{session_id}/promotion-execution` with a signed request payload and an approved approval ID from the configured approval store. Approved execution records are indexed as `metadata_kind=rollout-promotion-execution`, searchable from `/evidence` or `/promotion-executions`, and available as audit details from `/promotion-executions/{execution_id}` with approval, request, rollout, change, and rollback evidence links. Promotion execution audit exports are available from `/promotion-executions/{execution_id}/audit-export`, and approved rollback executions post to `/promotion-executions/{execution_id}/rollback-execution` with an approved rollback approval ID. Rollback execution metadata is indexed as `metadata_kind=rollout-rollback-execution` and retrievable from `/rollback-executions/{rollback_id}`. When `CAVRA_CONNECTOR_CONFIG` is configured, `POST /promotion-executions/{execution_id}/audit-export/deliver` and `POST /rollback-executions/{execution_id}/deliver` send those release governance events through configured connectors with retry counts and credential-redacted delivery evidence. Release channel promotion request metadata is searchable from `/release-channel-promotions` and retrievable from `/release-channel-promotions/{request_id}`. Endpoint-management export metadata is searchable from `/endpoint-management-exports`, retrievable from `/endpoint-management-exports/{export_id}`, summarized by `/endpoint-management-exports/dashboard`, and exposed through `/endpoint-management-exports/{export_id}/artifacts`, `/endpoint-management-exports/{export_id}/artifacts/{artifact_name}`, and `/endpoint-management-exports/{export_id}/artifact-bundle`. `POST /endpoint-management-exports/{export_id}/publish` publishes a checksum-verified export manifest to configured Jamf, Intune, or Linux connectors and indexes `metadata_kind=endpoint-management-publication-delivery`; `/endpoint-management-publications` and `/endpoint-management-publications/dashboard` provide provider, channel, export ID, success, and alert views. `POST /endpoint-inventory/ingest` normalizes Jamf, Intune, Linux fleet, or EDR inventory exports into `cavra.endpoint-observations.v1` and indexes `metadata_kind=endpoint-inventory-ingestion`; `/endpoint-inventory-ingestions` and `/endpoint-inventory-ingestions/dashboard` expose provider, channel, target coverage, missing target, and endpoint counts. `POST /endpoint-inventory/freshness-report` evaluates indexed ingestions against warning and critical age thresholds and indexes `metadata_kind=endpoint-inventory-freshness-report`; `/endpoint-inventory-freshness` and `/endpoint-inventory-freshness/dashboard` expose SLA status by provider, channel, deployment target, and alert level. `POST /endpoint-inventory-ingestions/{inventory_id}/reconcile` reconciles a stored ingestion against a signed desired manifest, indexes `metadata_kind=endpoint-reconciliation-automation`, and opens an approval-bound remediation request when drift is detected. `/endpoint-reconciliation-automations` and `/endpoint-reconciliation-automations/dashboard` expose drift-triggered automation and pending approval counts. `POST /endpoint-deployment/reconcile` compares a signed desired endpoint deployment manifest with observed endpoint inventory and indexes `metadata_kind=managed-endpoint-reconciliation`; `/endpoint-reconciliations` and `/endpoint-reconciliations/dashboard` expose drift status, alert level, missing target observations, stale endpoint counts, and checksum or version drift summaries. `POST /endpoint-reconciliations/{reconciliation_id}/remediation-request` creates an approval-bound remediation plan and indexes `metadata_kind=endpoint-drift-remediation-request`; `POST /endpoint-remediations/{request_id}/execute` records approved remediation execution evidence as `metadata_kind=endpoint-drift-remediation-execution`. `/endpoint-remediations` and `/endpoint-remediations/dashboard` expose request, execution, approval, and planned-action history. `POST /endpoint-remediations/{request_id}/handoff` packages a remediation request for Jira, ServiceNow, Slack, Teams, or private connector queues and indexes `metadata_kind=endpoint-remediation-handoff`; `/endpoint-remediation-handoffs` and `/endpoint-remediation-handoffs/dashboard` expose provider coverage, approval state, request IDs, and delivery readiness without embedding connector credentials or executing endpoint mutations. `POST /endpoint-remediation-handoffs/{handoff_id}/status` records redacted provider callback or operator status as `metadata_kind=endpoint-remediation-handoff-status`; `/endpoint-remediation-handoff-statuses` and `/endpoint-remediation-handoff-statuses/dashboard` expose provider status, external references, blocked or failed handoffs, and completed handoff counts. `POST /endpoint-remediation-sla/report` generates executive SLA and escalation reporting from handoff and status metadata as `metadata_kind=endpoint-remediation-sla-report`; `/endpoint-remediation-sla-reports` and `/endpoint-remediation-sla-reports/dashboard` expose breached, at-risk, completed, and executive release governance summary metrics. `POST /endpoint-remediation-sla-reports/{report_id}/deliver` plans notification routing from optional policy rules, applies duplicate suppression windows, converts the report into `cavra.endpoint_remediation_sla.notification.v1`, sends unsuppressed webhook, Slack, Teams, Jira, or ServiceNow notifications, and indexes redacted delivery evidence as `metadata_kind=release-connector-delivery`. `POST /endpoint-remediation-sla-reports/{report_id}/acknowledgements` records acknowledgement, dismissal, escalation, or resolution metadata without storing connector secrets. `/endpoint-remediation-sla-notifications` and `/endpoint-remediation-sla-notifications/dashboard` expose notification plans, suppressed providers, delivery outcomes, acknowledgements, and outstanding acknowledgement counts. `POST /endpoint-remediation-sla-notifications/escalation-plan` evaluates owner-specific acknowledgement and resolution SLOs against notification metadata. `POST /endpoint-remediation-sla-escalations/{plan_id}/deliver` emits active escalation routes through configured connectors as `cavra.endpoint_remediation_sla.escalation_delivery.v1` and indexes `connector_delivery_source=endpoint_remediation_sla_escalation_delivery`; `POST /endpoint-remediation-sla-escalations/{plan_id}/reviews` records owner review evidence as `metadata_kind=endpoint-remediation-sla-escalation-review`. `POST /endpoint-remediation-sla-escalations/recurrence-plan` applies recurrence intervals, maximum recurrence counts, owner calendars, and maintenance windows and indexes `metadata_kind=endpoint-remediation-sla-escalation-recurrence-plan`. `POST /endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/deliver` emits only deliverable recurrence routes as `cavra.endpoint_remediation_sla.escalation_recurrence_delivery.v1` and indexes `connector_delivery_source=endpoint_remediation_sla_escalation_recurrence_delivery`; `GET /endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/suppression-audit` records public-safe suppression audit evidence as `metadata_kind=endpoint-remediation-sla-escalation-suppression-audit`; `POST /endpoint-remediation-sla-escalation-recurrences/retry-plan` indexes retry policies for failed recurrence delivery batches as `metadata_kind=endpoint-remediation-sla-escalation-recurrence-retry-plan`; `POST /endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/owner-digest` emits owner digest notifications as `cavra.endpoint_remediation_sla.escalation_owner_digest.v1` and indexes `connector_delivery_source=endpoint_remediation_sla_escalation_owner_digest`; `GET /endpoint-remediation-sla-escalation-recurrences/suppression-trends` indexes suppression trend analytics as `metadata_kind=endpoint-remediation-sla-escalation-suppression-trend`. `POST /endpoint-remediation-sla-escalation-recurrences/automation-run` runs one dry-run-by-default scheduled recurrence worker pass, indexes retry-plan, owner-digest, suppression-trend, and automation-run metadata, and delivers owner digests only when execution is explicitly requested and connector configuration exists. `/endpoint-remediation-sla-escalation-recurrence-automations`, `/endpoint-remediation-sla-escalation-recurrence-automations/dashboard`, and `/endpoint-remediation-sla-escalation-recurrence-automations/health` expose worker history, dry-run counts, executed counts, retryable routes, digest counts, suppression trend event counts, missed-run health, stale metadata, failed job records, and owner-digest connector delivery failures. `POST /endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/deliver` converts unhealthy recurrence automation status into connector delivery plans and redacted delivery evidence; `POST /endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/{health_id}/acknowledgements` records review state; `/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts` and `/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/dashboard` expose delivery, suppression, and acknowledgement history. `/endpoint-remediation-sla-escalations`, `/endpoint-remediation-sla-escalations/dashboard`, `/endpoint-remediation-sla-escalation-actions`, `/endpoint-remediation-sla-escalation-actions/dashboard`, `/endpoint-remediation-sla-escalation-recurrences`, and `/endpoint-remediation-sla-escalation-recurrences/dashboard` expose active escalation ladders, owner breach counts, route-level SLO state, delivery history, owner review state, recurrence readiness, recurrence delivery batches, retry plans, owner digests, suppression audit exports, suppression trends, and suppression reasons.

## Approvals

Approval endpoints:

- `GET /approvals`: list approval requests with `state`, `approver_group`, `limit`, and `offset` filters.
- `POST /approvals`: create a pending approval request from a CAVRA decision.
- `GET /approvals/{approval_id}`: fetch one approval request.
- `POST /approvals/{approval_id}/approve`: approve a pending request with actor, reason, and optional external reference.
- `POST /approvals/{approval_id}/deny`: deny a pending request with actor, reason, and optional external reference.
- `POST /approvals/{approval_id}/expire`: expire a pending request.
- `POST /approvals/{approval_id}/deliver`: send configured approval provider requests and return redacted delivery evidence.
- `POST /approvals/{approval_id}/attach-decision`: attach approval summary and evidence refs to a decision payload.
- `POST /approvals/break-glass`: create a mandatory-reason emergency override.

Default approval path: `.cavra/api/approvals.json`.

Set `CAVRA_APPROVAL_STORE` to override the approval store path for local or self-hosted deployments.

Set `CAVRA_APPROVAL_DB` to use SQLite-backed approval persistence. `GET /approvals` supports the same `state`, `approver_group`, `limit`, and `offset` filters in JSON and SQLite modes. `GET /console/config` includes `approval_mode`.

Set `CAVRA_APPROVAL_ROUTING_FILE` to load repository-specific JSON or YAML approval routing rules at API startup. `POST /approvals` uses those rules unless the request payload supplies an explicit `approver_group`.

Approval decision endpoints accept an optional `actor_claims` object with OIDC-style fields such as `email`, `preferred_username`, `sub`, `groups`, `roles`, and `iss`. They also accept `Authorization: Bearer <token>` for console sessions. When claims or a token are present, the actor must belong to the approval request's approver group or match repository-scoped RBAC before the API accepts approve or deny decisions.

Set `CAVRA_APPROVAL_OIDC_CONFIG` to enable signed OIDC JWT validation for approval decision payloads that include `actor_token`. The config must include `issuer`, `audience`, and `jwks` or `jwks_path`. RS256 signatures, issuer, audience, expiry, and not-before claims are validated before group authorization.

Set `CAVRA_APPROVAL_RBAC_FILE` to enable repository RBAC rules. The policy supports `group_mappings` and `repository_permissions` so repository owner groups can approve specific approver groups without receiving global approval authority. Break-glass console actions require a verified actor in the `Change Advisory Board` group when OIDC or RBAC is configured.

Set `CAVRA_APPROVAL_PROVIDER_CONFIG` to a JSON or YAML provider config file to enable `POST /approvals/{approval_id}/deliver`. Delivery requests accept `provider`, `retries`, and `timeout_seconds`; responses include redacted request metadata, status, attempt count, and error state for evidence.

## Console

The static console under `apps/sandbox-ui` includes backend-driven sandbox runs, activity session and decision browsing, repository inventory and policy rollout views, enterprise integration inventory views, release connector delivery history, release connector alert dashboards, endpoint remediation handoff readiness and status reconciliation, endpoint remediation SLA reporting, evidence search, evidence artifact downloads, PR attestation verification, console session validation, approval queue views, break-glass creation, approval audit details, Agent Registry views, MCP Trust Registry views, predefined agent profiles, and MCP capability classification. It can run as a standalone static demo or query the API sandbox, activity, inventory, integrations, connector delivery, release connector delivery, endpoint remediation handoff, endpoint remediation handoff status, endpoint remediation SLA, escalation action, recurrence, evidence metadata, evidence artifact, approval, agent, MCP, and console session endpoints when hosted on the same origin or an allowed cross origin.

`GET /console/config` returns the console API base URL, metadata mode, allowed CORS origins, persistence modes, and endpoint paths including rollout detail, security boundary, operations status, and retention-plan endpoints. Configure cross-origin deployments with:

- `CAVRA_PUBLIC_API_BASE_URL`
- `CAVRA_CORS_ORIGINS`

## Sandbox API

- `GET /api/sandbox/scenarios`: list runnable public sandbox scenarios.
- `POST /api/sandbox/run`: run the flagship scenario with real backend policy decisions. The API persists evidence metadata plus activity session and decision records.
- `GET /api/sandbox/runs/{run_id}`: fetch a generated sandbox run.
- `GET /api/sandbox/runs/{run_id}/events`: fetch the run decision events.
- `GET /api/sandbox/runs/{run_id}/evidence`: download run evidence JSON.
- `GET /api/sandbox/runs/{run_id}/attestation`: download the run PR attestation.
- `GET /api/sandbox/runs/{run_id}/compliance`: download compliance mapping for the run.
