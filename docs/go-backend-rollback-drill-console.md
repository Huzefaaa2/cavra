# Go Backend Rollback Drill Console

CAVRA now surfaces Go backend rollback drill notification history in the Evidence Console. Operators can filter notification plans, redacted connector deliveries, acknowledgements, and escalation plans without leaving the dashboard.

## What This Adds

- Evidence Console dashboard metrics for drill notification plans, deliveries, failed deliveries, acknowledgements, outstanding routes, escalation routes, and breached routes.
- Filters for provider, acknowledgement state, and notification metadata kind.
- Notification history drill-downs with JSON detail and export actions.
- Escalation route drill-downs showing schedule ID, provider, owner, acknowledgement state, route age, SLO, breach state, and recommended action.
- Routing history filters for owner, provider, action, and suppression category.
- Suppression summary rows for maintenance-window, owner-calendar, healthy-schedule, and other suppressed routes.
- Authenticated route mutation controls for **Ack**, **Escalate**, and **Resolve** actions.
- Bulk acknowledgement and escalation controls for the current route filter scope.
- Downloadable acknowledgement audit packages for route-level release governance review.
- Acknowledgement audit delivery routing to configured SIEM, ITSM, ChatOps, and webhook connectors.
- Local public-safe sample data so the Community Edition dashboard remains useful without a live API.

## How To Use

Start the sandbox UI:

```bash
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section. The dashboard automatically calls:

```text
GET /runtime/go-pilot/rollback-drill-notifications
GET /runtime/go-pilot/rollback-drill-notifications/dashboard
POST /runtime/go-pilot/rollback-drill-notifications/{schedule_id}/acknowledgements
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery
```

If the API is unavailable, the console uses bundled sample metadata. In authenticated API deployments, acknowledgement mutations require a verified console actor and are documented in [Go Backend Rollback Drill Acknowledgement Controls](go-backend-rollback-drill-acknowledgement-controls.md).

## User Stories

- As a release manager, I can review whether stale rollback drill notifications were acknowledged.
- As an incident commander, I can find the owner, provider, and route that missed the acknowledgement SLO.
- As a platform owner, I can export route-level escalation metadata for operational review.
- As an auditor, I can inspect public-safe notification evidence without seeing connector credentials.

## Enterprise Challenge Solved

Promoted runtime governance needs more than a delivered alert. This console slice turns notification history into an operator-friendly review surface, making missed rollback drill follow-up visible before backend promotion confidence decays.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-console.svg`.

## Next Work

The next recommended implementation step is to add acknowledgement audit retry execution approvals and connector recovery playbooks.
