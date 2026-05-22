# Go Backend Rollback Drill Routing History

CAVRA now promotes rollback drill notification route decisions into a persisted, filterable history and a suppression trend artifact. This makes owner routing, maintenance-window suppression, and owner-calendar suppression reviewable after connector delivery.

## What This Adds

- `GET /runtime/go-pilot/rollback-drill-notifications/routes` flattens persisted notification plan route decisions.
- Route filters support `schedule_id`, `provider`, `owner`, `action`, and `category`.
- `GET /runtime/go-pilot/rollback-drill-notifications/suppression-trends` summarizes suppressed routes and persists metadata kind `go-backend-rollback-drill-routing-suppression-trend`.
- The Evidence Console now shows routing history and suppression summary tables in the Go Rollback Drill Notifications section.
- Public-safe sample data keeps the Community Edition console useful without a live API.

## Suppression Categories

- `maintenance_window`: route suppressed because an approved maintenance window matched the owner/provider.
- `owner_calendar`: route suppressed because owner availability metadata marked the owner unavailable.
- `healthy_schedule`: route suppressed because the rollback drill schedule did not need notification.
- `other`: route suppressed for another public-safe reason.

## User Stories

- As a release manager, I can filter rollback drill route decisions by owner, provider, and action.
- As an incident commander, I can explain why a drill notification was suppressed during a change freeze.
- As a platform owner, I can trend suppression causes across owner routes.
- As an auditor, I can review suppression evidence without seeing connector secrets or private calendar exports.

## Enterprise Challenge Solved

Enterprise change governance often needs to prove why an alert did not fire. CAVRA now preserves route-level suppression decisions and trend summaries as public-safe evidence, reducing audit ambiguity without exposing private operational systems.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-routing-history.svg`.

## Next Work

The next recommended implementation step is to add acknowledgement audit retry execution approvals and connector recovery playbooks.
