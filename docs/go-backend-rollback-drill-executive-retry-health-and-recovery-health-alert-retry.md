# Go Backend Rollback Drill Executive Retry Health And Recovery Health Alert Retry

CAVRA now adds closed-loop health reporting for executive report delivery retries and retry planning for failed recovery retry health alert delivery.

## What This Adds

- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health` reports missed executive retry workers, stale retry plans, failed executive report deliveries, failed retry executions, disabled schedules, and alert severity.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-plan` creates retry, wait, or suppress decisions for failed recovery retry health alert deliveries.
- Rollback drill notification history and dashboards now include executive delivery retry health reports and recovery health alert delivery retry plans.
- Evidence Console now includes **Plan Health Alert Retry** and **Exec Retry Health** actions.
- All records are derived from public-safe metadata and do not contain connector credentials, private URLs, customer payloads, or enterprise source.

## Operator Flow

1. Run recovery escalation retry workers and recovery retry health reports.
2. Send recovery retry health alerts to configured connectors.
3. Use **Plan Health Alert Retry** when alert delivery fails.
4. Schedule, deliver, and retry executive recovery reports.
5. Use **Exec Retry Health** to verify executive retry worker freshness and delivery retry outcomes.
6. Escalate persistent failed delivery or failed retry execution to release governance.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-plan
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health
```

Recovery health alert retry plan request fields:

- `generated_by`: operator or automation actor.
- `retry_policy.max_retry_attempts`: maximum delivery failures before suppression.
- `retry_policy.retry_delay_minutes`: base delay before retry.
- `retry_policy.allow_immediate_retry`: allow immediate retry during drills.
- `retry_policy.backoff_multiplier`: exponential backoff multiplier.

Executive retry health query fields:

- `expected_interval_minutes`: expected executive retry worker cadence.
- `stale_metadata_minutes`: maximum acceptable retry plan age.
- `generated_by`: actor recorded on the health metadata.

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
- As an enterprise operator, I can use retry health reporting to detect stale automation before governance reports are missed.

## Enterprise Challenge Solved

Enterprise release governance needs evidence that failure notifications and executive recovery reports are not just generated, but actively monitored for delivery reliability. This phase gives operators health signals and retry plans for the final reporting loop while preserving the open-core boundary.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.svg`.

## Next Work

The next recommended implementation step is recovery health alert retry worker execution and executive retry health alert delivery.
