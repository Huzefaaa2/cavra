# Go Backend Rollback Drill Audit Worker Health Alerts

CAVRA now exposes worker health for rollback drill acknowledgement audit retry automation, routes worker health alerts, and records retry acknowledgements.

## What This Adds

- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health` for missed worker runs, stale retry metadata, retryable delivery count, connector delivery failures, and recommendations.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/deliver` for routing public-safe worker health alerts to configured connectors.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/{health_id}/acknowledgements` for recording health alert review state.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts` and `/worker-health-alert-dashboard` for alert delivery and acknowledgement history.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plans/{retry_plan_id}/acknowledgements` for accepting, deferring, escalating, resolving, or dismissing retry decisions.
- Evidence Console actions for **Send Worker Alert** and **Ack Retry**.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Use **Plan Audit Retry** to create a retry plan from failed acknowledgement audit delivery metadata.
2. Use **Run Audit Worker** to dry-run the scheduled worker.
3. Use **Send Worker Alert** to route worker health to a configured connector.
4. Use **Ack Retry** to record the operator decision for the latest retry plan.
5. Filter by **Ack audit worker health** or retry acknowledgement kind to review public-safe evidence.

## API

```text
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/deliver
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/{health_id}/acknowledgements
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alert-dashboard
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plans/{retry_plan_id}/acknowledgements
```

Retry acknowledgement states:

- `accepted`
- `deferred`
- `escalated`
- `resolved`
- `dismissed`

Worker health alert acknowledgement states:

- `acknowledged`
- `dismissed`
- `escalated`
- `resolved`

## Security Boundary

Worker health is derived from public-safe retry plans, worker run metadata, and redacted connector delivery evidence. Alert payloads do not include connector credentials, private URLs, Enterprise source code, customer secrets, or private policy packs. Retry acknowledgements record operator review only; they do not execute retry delivery.

## User Stories

- As a release manager, I can see when retryable acknowledgement audit delivery failures still need action.
- As a platform owner, I can route worker health alerts into release-governance channels without exposing connector secrets.
- As a SOC analyst, I can verify that repeated SIEM delivery failures are acknowledged.
- As an auditor, I can review who accepted, deferred, or escalated retry decisions.

## Enterprise Challenge Solved

Enterprise rollback assurance requires evidence that failed audit delivery was noticed, routed, and reviewed. Worker health alerts and retry acknowledgements close the operational loop between failed delivery, retry planning, worker execution, and accountable review.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-audit-worker-health-alerts.svg`.

## Next Work

The next recommended implementation step is to add approval-bound live retry execution records and connector recovery closure evidence.
