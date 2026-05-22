# Go Backend Rollback Drill Executive Delivery Retry Execution And Recovery Health Alerts

CAVRA now closes the next rollback drill operations loop by delivering recovery retry health alerts and executing scheduled executive report delivery retries from public-safe metadata.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/deliver` builds and routes a recovery escalation retry health alert plan.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/{health_id}/acknowledgements` records operator acknowledgement for health alert destinations.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts` lists health alert plan, acknowledgement, and delivery history.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alert-dashboard` summarizes sent, failed, suppressed, acknowledged, and outstanding retry health alerts.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-worker-run` runs executive report delivery retry automation in dry-run mode by default, or live mode when `execute=true`.
- Rollback drill dashboards now count recovery retry health alert plans and acknowledgements, executive delivery retry worker runs, and executive delivery retry execution outcomes.
- Evidence Console now includes **Send Retry Health Alert** and **Run Executive Retry** actions in the Go rollback drill notification workflow.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Run recovery escalation retry health after escalation retry workers execute.
2. Use **Send Retry Health Alert** to route missed-worker, stale-plan, acknowledgement-gap, or failed-execution alerts.
3. Record health alert acknowledgements for providers that need review evidence.
4. Schedule and deliver executive recovery reports.
5. Use **Plan Executive Retry** to inspect failed executive delivery attempts.
6. Use **Run Executive Retry** after reviewing retry decisions; live execution requires connector configuration and `execute=true`.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/deliver
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/{health_id}/acknowledgements
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alert-dashboard
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-worker-run
```

Recovery retry health alert delivery fields:

- `provider`: connector destination or `all`.
- `force`: bypass duplicate suppression when `true`.
- `expected_interval_minutes`: expected recovery retry worker cadence.
- `stale_metadata_minutes`: maximum acceptable retry plan metadata age.
- `suppression_window_minutes`: duplicate alert suppression window.
- `max_alerts`: maximum alert details to include in the event payload.

Executive delivery retry worker fields:

- `dry_run`: defaults to `true`.
- `execute`: set to `true` for live retry delivery.
- `max_retry_deliveries`: maximum selected retry decisions.
- `retry_policy.max_retry_attempts`
- `retry_policy.retry_delay_minutes`
- `retry_policy.allow_immediate_retry`
- `retry_policy.backoff_multiplier`

## User Stories

- As a release manager, I can route recovery retry health alerts to the same operational destinations used by rollback governance.
- As a platform owner, I can acknowledge health alerts without exposing connector credentials or private incident content.
- As an executive stakeholder, I can receive retried recovery reports after transient connector delivery failures.
- As an auditor, I can trace executive delivery retry execution back to retry plans, worker runs, schedule runs, and redacted connector delivery metadata.

## Enterprise Challenge Solved

Regulated release operations need proof that operational reporting is delivered, retried, and acknowledged when connector delivery fails. This phase adds the missing automation around recovery retry health alert delivery and executive report delivery retry execution while keeping all side effects governed by runtime connector configuration.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-executive-delivery-retry-execution-and-recovery-health-alerts.svg`.

## Follow-On Work Completed

Closed-loop executive delivery retry health reporting and recovery health alert retry planning are documented in `docs/go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.md`.
