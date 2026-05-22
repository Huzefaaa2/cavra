# Go Backend Rollback Drill Bulk Acknowledgement Audit

CAVRA now supports bulk rollback drill acknowledgement actions and exportable acknowledgement audit packages for the Evidence Console.

## What This Adds

- Bulk **Ack Outstanding** and **Bulk Escalate Breached** controls for the currently filtered rollback drill routes.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk` for recording acknowledgement, escalation, dismissal, or resolution metadata across multiple routes.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package` for producing and persisting a public-safe route acknowledgement audit package.
- Audit packages that include route state, owner, provider, latest acknowledgement actor, acknowledgement timestamp, external reference, and operator notes.
- Local sample-mode bulk acknowledgement and audit export behavior for the Community Edition sandbox when the API is unavailable.
- Roadmap and wiki updates that move the next implementation target to scheduled acknowledgement audit delivery and SIEM/ITSM export routing.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Use filters to narrow by owner, provider, state, route action, or suppression category. Then:

- Select **Bulk Ack Outstanding** to acknowledge currently filtered outstanding routes.
- Select **Bulk Escalate Breached** to mark currently filtered breached routes as escalated.
- Select **Export Ack Audit** to download a JSON audit package for the current filter scope.

Authenticated deployments use the signed console actor for bulk acknowledgements and audit package generation.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package
```

Both endpoints require verified actor context when console OIDC or RBAC is configured. The public Community Edition implementation does not expose connector credentials, identity provider secrets, or private customer data.

## User Stories

- As a release manager, I can acknowledge many outstanding rollback drill notification routes in one operation.
- As an incident commander, I can escalate all breached routes visible in the current filter scope.
- As a platform owner, I can export a route-level acknowledgement audit package for release governance review.
- As an auditor, I can inspect actor identity, notes, external references, and route states without seeing connector secrets.

## Enterprise Challenge Solved

Large environments can generate multiple rollback drill notification routes for owners, providers, and schedules. Bulk acknowledgements reduce operator toil while audit packages preserve defensible evidence for compliance review.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-bulk-acknowledgement-audit.svg`.

## Next Work

The next recommended implementation step is to add scheduled acknowledgement audit delivery and SIEM/ITSM export routing.
