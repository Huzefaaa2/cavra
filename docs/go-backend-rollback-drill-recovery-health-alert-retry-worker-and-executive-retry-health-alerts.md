# Go Backend Rollback Drill Recovery Health Alert Retry Worker And Executive Retry Health Alerts

CAVRA now executes recovery retry health alert redelivery through a governed worker and routes executive delivery retry health alerts to release governance connectors.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-worker-run` executes or dry-runs failed recovery retry health alert delivery decisions.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/deliver` builds executive retry health alert plans and delivers them through configured connectors.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/{health_id}/acknowledgements` records review outcomes for executive retry health alerts.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts` lists executive retry health alert plans, acknowledgements, and connector delivery evidence.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alert-dashboard` summarizes outstanding executive retry health acknowledgements and delivery health.
- Evidence Console now includes **Run Health Alert Retry** and **Send Exec Health Alert** actions.

All records are derived from public-safe metadata. They do not store connector credentials, private URLs, customer payloads, enterprise implementation, or SaaS license secrets.

## Operator Flow

1. Send recovery retry health alerts after recovery escalation retry health detects a failure.
2. Use **Plan Health Alert Retry** when delivery fails.
3. Use **Run Health Alert Retry** to execute selected retry decisions with `execute=true`.
4. Run executive delivery retry workers and build executive delivery retry health reports.
5. Use **Send Exec Health Alert** to route executive retry health alerts to release governance.
6. Acknowledge executive retry health alerts after release governance reviews the issue.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-worker-run
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/deliver
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/{health_id}/acknowledgements
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alert-dashboard
```

Recovery health alert retry worker request fields:

- `execute`: defaults to false; must be true for live connector redelivery.
- `max_retry_deliveries`: caps selected retry decisions for a worker run.
- `retry_policy`: sets retry attempts, delay, immediate retry, and backoff.
- `schedule`: records cadence, interval, and worker enablement.
- `provider`: optional connector provider override.

Executive retry health alert request fields:

- `provider`: connector provider or `all`.
- `force`: bypass duplicate suppression for controlled drills.
- `expected_interval_minutes`: expected executive retry worker cadence.
- `stale_metadata_minutes`: maximum acceptable retry plan age.
- `suppression_window_minutes`: duplicate delivery suppression window.

## Evidence

New metadata kinds:

- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-worker-run`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-execution-record`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-plan`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-ack`

New dashboard fields:

- `acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run_count`
- `acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_ack_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_count`
- `failed_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_count`

## User Stories

- As a release manager, I can execute a governed retry for failed recovery health alert delivery.
- As an executive stakeholder, I can receive a concise alert when executive report delivery retry health is degraded.
- As an auditor, I can trace retry worker run, connector delivery, execution record, alert plan, and acknowledgement evidence.
- As a platform owner, I can keep health alert retry and executive reporting loops observable without exposing private connector configuration.

## Enterprise Challenge Solved

Enterprise rollback governance fails when the final alerting path is not itself governed. This phase closes the loop for recovery health alert delivery failures and executive retry health escalation, giving release governance a complete public-safe evidence chain for notification reliability.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-recovery-health-alert-retry-worker-and-executive-retry-health-alerts.svg`.

## Next Work

The next recommended implementation step is executive retry health alert retry planning, retry worker execution, and final reporting closure dashboards.
