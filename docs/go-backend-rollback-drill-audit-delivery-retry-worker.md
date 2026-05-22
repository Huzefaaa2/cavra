# Go Backend Rollback Drill Audit Delivery Retry Worker

CAVRA now plans governed retries for failed rollback drill acknowledgement audit delivery and records scheduled worker dry-runs for recurring retry operations.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plan` for creating a public-safe retry plan from failed acknowledgement audit delivery metadata.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run` for running a scheduled retry worker. The worker defaults to `dry_run=true`.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-runs` for reviewing worker execution history.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-dashboard` for worker run count, dry-run count, executed count, retryable count, and selected retry count.
- Evidence Console actions for **Plan Audit Retry** and **Run Audit Worker**.
- Dashboard cards for audit retry plans, retryable audit deliveries, worker runs, and worker dry-runs.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Use **Deliver Ack Audit** to route an acknowledgement audit package.
2. Use the dashboard and filters to find failed audit delivery attempts.
3. Use **Plan Audit Retry** to create a retry plan from failed delivery metadata.
4. Use **Run Audit Worker** to dry-run the scheduled retry worker.
5. Review worker history and retry decisions before executing non-dry-run retry delivery in a governed deployment.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plan
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-runs
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-dashboard
```

Example retry plan request:

```json
{
  "generated_by": "release-manager",
  "retry_policy": {
    "max_retry_attempts": 3,
    "retry_delay_minutes": 15,
    "backoff_multiplier": 2
  }
}
```

Example worker request:

```json
{
  "generated_by": "release-manager",
  "dry_run": true,
  "max_retry_deliveries": 5,
  "retry_policy": {
    "max_retry_attempts": 3,
    "retry_delay_minutes": 15,
    "backoff_multiplier": 2
  },
  "schedule": {
    "interval_minutes": 30,
    "cadence": "every_30_minutes",
    "enabled": true
  }
}
```

## Security Boundary

Retry planning is derived from redacted connector delivery metadata only. Worker records contain retry decisions, schedule windows, dry-run state, and public-safe result summaries. They do not expose connector credentials, private URLs, customer payloads, Enterprise source code, license validation secrets, or private policy packs.

## User Stories

- As a release manager, I can see which failed acknowledgement audit delivery attempts are eligible for retry.
- As a platform owner, I can dry-run a scheduled retry worker before allowing it to execute delivery.
- As a SOC analyst, I can verify that failed SIEM audit delivery attempts are queued for governed recovery.
- As an auditor, I can review retry decisions and worker evidence without needing connector secrets.

## Enterprise Challenge Solved

Enterprise rollback evidence cannot depend on a single delivery attempt. Governed retry plans and dry-run worker evidence make failed acknowledgement audit delivery recoverable while preserving clear operator control and a public-safe Community Edition boundary.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-audit-delivery-retry-worker.svg`.

## Next Work

The next recommended implementation step is to add acknowledgement audit retry execution approvals and connector recovery playbooks.
