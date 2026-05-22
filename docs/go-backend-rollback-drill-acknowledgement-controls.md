# Go Backend Rollback Drill Acknowledgement Controls

CAVRA now lets operators record rollback drill notification acknowledgements directly from the Evidence Console while preserving the authenticated console actor in deployments that enable OIDC/RBAC.

## What This Adds

- Route-level **Ack**, **Escalate**, and **Resolve** actions in the Go Rollback Drill Notifications console section.
- Console API calls that include the stored bearer token through `Authorization: Bearer ...`.
- Server-side actor enforcement for `POST /runtime/go-pilot/rollback-drill-notifications/{schedule_id}/acknowledgements` whenever console OIDC or RBAC is configured.
- Authenticated acknowledgement records that use the verified actor identity instead of trusting browser-supplied `acknowledged_by` values.
- Bulk acknowledgement and escalation actions for currently filtered drill routes.
- Acknowledgement audit package export for route state, actor identity, notes, and external references.
- Local sample-mode acknowledgement mutation so the Community Edition sandbox remains useful without a live API.
- Console session permission reporting through `acknowledge_drill_notifications`.

## How To Use

Start the API and sandbox UI, then configure a console token in the **Console Authenticated Sessions** section:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html`, save a signed console token if the API is configured with `CAVRA_APPROVAL_OIDC_CONFIG`, then use the **Go Rollback Drill Notifications** section.

The route buttons call:

```text
POST /runtime/go-pilot/rollback-drill-notifications/{schedule_id}/acknowledgements
```

When OIDC or RBAC is configured, the endpoint requires verified actor context from a bearer token, `actor_token`, or `actor_claims`. The persisted acknowledgement uses that verified actor.

## User Stories

- As a release manager, I can acknowledge a missed rollback drill notification from the console without opening a separate CLI.
- As an incident commander, I can escalate or resolve a route and preserve the actor identity that made the decision.
- As a platform owner, I can require verified console sessions for drill acknowledgement mutations.
- As an auditor, I can distinguish operator-entered notes from the authenticated actor that recorded the evidence.

## Enterprise Challenge Solved

Rollback drill governance breaks down if acknowledgement records can be spoofed from an unauthenticated browser. This slice ties drill notification mutations to the same console identity boundary used by approval and break-glass actions, while keeping connector secrets and enterprise identity provider details outside the public Community Edition.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-acknowledgement-controls.svg`.

## Next Work

The next recommended implementation step is to add acknowledgement audit delivery retry automation and scheduled worker execution.
