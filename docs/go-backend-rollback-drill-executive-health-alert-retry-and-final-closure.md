# Go Backend Rollback Drill Executive Health Alert Retry And Final Closure

CAVRA now closes the executive retry health alert loop with retry planning, retry worker execution, execution evidence, and a final reporting closure dashboard.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-plan` creates retry, wait, or suppress decisions for failed executive retry health alert deliveries.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-worker-run` runs dry-run-default retry automation and persists execution records when `execute=true`.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closure-dashboard` summarizes whether the rollback drill reporting loop can be closed.
- Evidence Console now includes **Plan Exec Alert Retry**, **Run Exec Alert Retry**, and **Final Closure** actions.

All records are public-safe metadata. They do not contain connector credentials, private webhook URLs, customer payloads, enterprise implementation, license secrets, or SaaS backend code.

## Operator Flow

1. Build executive delivery retry health with the executive retry health endpoint.
2. Send executive retry health alerts to release governance connectors.
3. If delivery fails, run **Plan Exec Alert Retry** to create retry decisions.
4. Run **Run Exec Alert Retry** with live execution only when a connector configuration is present and the operator explicitly requests execution.
5. Use **Final Closure** to confirm whether failed alert deliveries, failed retry executions, or outstanding acknowledgements remain open.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-plan
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-worker-run
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closure-dashboard
```

Retry plan request fields:

- `generated_by`: public-safe operator or automation actor.
- `retry_policy.max_retry_attempts`: maximum failed deliveries before suppression.
- `retry_policy.retry_delay_minutes`: base delay before redelivery.
- `retry_policy.allow_immediate_retry`: supports manual drill execution without delay.
- `retry_policy.backoff_multiplier`: backoff multiplier for repeat failures.

Retry worker request fields:

- `execute`: defaults to false; must be true for live redelivery.
- `max_retry_deliveries`: caps selected retry decisions.
- `provider`: connector provider override.
- `schedule`: records cadence, interval, and enablement.
- `retries` and `timeout_seconds`: connector execution controls.

## Evidence

New metadata kinds:

- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-plan`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-worker-run`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-execution-record`

New dashboard fields:

- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retryable_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_success_count`
- `acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_failed_count`

Final closure dashboard fields:

- `closure_state`: `closed` or `open`.
- `alert_level`: `healthy` or `critical`.
- `open_items`: remaining closure blockers.
- `summary`: executive retry health alert and recovery retry health alert closure counts.
- `recommended_actions`: operator actions to resolve open items.

## User Stories

- As a release manager, I can retry failed executive retry health alert delivery with explicit worker evidence.
- As an auditor, I can verify whether the rollback drill reporting loop is closed or still has open reporting risks.
- As a platform owner, I can see failed executive alert delivery, retry execution, and acknowledgement gaps in one closure dashboard.

## Enterprise Challenge Solved

Final reporting often fails silently after lower-level recovery automation is complete. This phase makes the last mile governed: executive health alerts, their retries, execution evidence, and closure readiness are visible without exposing private connector configuration.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-executive-health-alert-retry-final-closure.svg`.

## Next Work

The next recommended implementation step is release-readiness summary and operator runbook export for the completed rollback drill reporting loop.
