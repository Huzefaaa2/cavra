# Go Backend Rollback Drill Executive Retry Health And Recovery Health Alert Retry

CAVRA now adds closed-loop health reporting for executive report delivery retries and retry planning for failed recovery retry health alert delivery.

## What This Adds

- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health` reports missed executive retry workers, stale retry plans, failed executive report deliveries, failed retry executions, disabled schedules, and alert severity.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-plan` creates retry, wait, or suppress decisions for failed recovery retry health alert deliveries.
- Rollback drill notification history and dashboards now include executive delivery retry health reports and recovery health alert delivery retry plans.
- Evidence Console now includes **Plan Health Alert Retry** and **Exec Retry Health** actions.

## Operator Flow

1. Run recovery escalation retry workers and recovery retry health reports.
2. Send recovery retry health alerts to configured connectors.
3. Use **Plan Health Alert Retry** when alert delivery fails.
4. Schedule, deliver, and retry executive recovery reports.
5. Use **Exec Retry Health** to verify executive retry worker freshness and delivery retry outcomes.

## Evidence

New metadata kinds:

- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-plan`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health`

New dashboard fields:

- `acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan_count`
- `acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retryable_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_count`

## User Stories

- As a release manager, I can see whether executive retry automation is current before I trust delivery recovery evidence.
- As a platform owner, I can plan retries for failed recovery health alert notifications without exposing connector secrets.
- As an auditor, I can prove that failed executive report delivery and failed health alert delivery are tracked through public-safe evidence records.

## Diagram

See `go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.svg`.

## Next Work

Delivered in later phases: recovery health alert retry worker execution, executive retry health alert delivery, executive health alert retry planning, retry worker execution, and final reporting closure dashboards.
