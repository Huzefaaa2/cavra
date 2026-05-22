# Go Backend Rollback Drill Recovery Retry Health And Executive Delivery Retry

CAVRA now adds the operations layer after recovery escalation retry execution: health reporting for the recovery escalation retry worker and retry planning for failed scheduled executive recovery report delivery.

## What This Adds

- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health` summarizes recovery escalation retry worker freshness, stale retry plans, acknowledgement gaps, failed retry execution records, and disabled retry schedules.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-plan` builds retry, wait, or suppress decisions for failed executive report delivery metadata.
- Evidence Console now includes **Retry Health** and **Plan Executive Retry** actions in the Go rollback drill notification workflow.
- Rollback drill dashboards now count recovery escalation retry health reports, health alerts, executive delivery retry plans, and retryable executive delivery attempts.
- Public-safe metadata remains the only source for these reports. Connector credentials, private incident payloads, and commercial modules stay outside the Community repository.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Build and deliver a recovery escalation plan.
2. Record provider acknowledgement for the escalation.
3. Create and run the recovery escalation retry worker.
4. Use **Retry Health** to detect missed worker runs, stale retry metadata, acknowledgement gaps, and failed retry execution.
5. Schedule and deliver an executive recovery report.
6. Use **Plan Executive Retry** when executive report delivery records show failed providers.

## API

```text
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-plan
```

Retry health query fields:

- `expected_interval_minutes`: expected recovery retry worker cadence. Defaults to `30`.
- `stale_metadata_minutes`: maximum acceptable age for retry plan metadata. Defaults to `120`.
- `generated_by`: public-safe actor label for the health report.

Executive delivery retry request fields:

- `generated_by`: public-safe actor label.
- `retry_policy.max_retry_attempts`
- `retry_policy.retry_delay_minutes`
- `retry_policy.allow_immediate_retry`
- `retry_policy.backoff_multiplier`

## User Stories

- As a release manager, I can see whether recovery escalation retries are running on schedule.
- As a platform owner, I can separate retryable executive report delivery failures from backoff waits and exhausted retry attempts.
- As an auditor, I can prove recovery retry health and executive retry plans came from redacted evidence metadata.
- As an incident lead, I can identify acknowledgement gaps before retry automation performs delivery side effects.

## Enterprise Challenge Solved

Escalation retry automation needs operational health, not just execution records. This phase gives enterprise operators a clear control surface for missed recovery workers, stale retry state, failed recovery retries, and failed executive report delivery without exposing connector secrets or private operational payloads.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-recovery-retry-health-and-executive-delivery-retry.svg`.

## Follow-On Work Completed

Automated executive report delivery retry execution and recovery escalation retry health alert delivery are now covered in [Go Backend Rollback Drill Executive Delivery Retry Execution And Recovery Health Alerts](go-backend-rollback-drill-executive-delivery-retry-execution-and-recovery-health-alerts.md).
