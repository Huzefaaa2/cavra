# Go Backend Rollback Drill Notification Escalation

CAVRA now records acknowledgements for stale or due-soon rollback drill notifications and builds escalation plans when notification acknowledgement is missing. This keeps promoted Go backend rollback governance auditable after the first connector alert is delivered.

## What This Adds

The public Community Edition now supports:

- notification acknowledgement records using schema `cavra.go-backend-pilot.rollback-drill-notification-ack.v1`;
- notification history across plans, redacted connector delivery evidence, acknowledgements, and escalation plans;
- notification dashboard counts for deliveries, failures, acknowledgements, and outstanding acknowledgement routes;
- escalation plans using schema `cavra.go-backend-pilot.rollback-drill-notification-escalation-plan.v1`;
- CLI and API workflows that never store connector secrets, private URLs, or customer data.

## CLI Usage

Build acknowledgement metadata:

```bash
cavra runtime go-rollback-drill-notification-ack go_backend_python_fallback_monthly \
  --provider slack \
  --acknowledged-by release-manager \
  --plan-id gordn_123 \
  --external-ref CHG-1234 \
  --json
```

Build an escalation plan template:

```bash
cavra runtime go-rollback-drill-escalation-plan \
  --acknowledgement-minutes 60 \
  --json
```

## API Usage

Record acknowledgement:

```bash
curl -X POST http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-notifications/go_backend_python_fallback_monthly/acknowledgements \
  -H 'content-type: application/json' \
  -d '{"provider":"slack","acknowledged_by":"release-manager","plan_id":"gordn_123"}'
```

Inspect history and dashboard:

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-notifications
curl http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-notifications/dashboard
```

Build an escalation plan:

```bash
curl -X POST http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-notifications/escalation-plan \
  -H 'content-type: application/json' \
  -d '{"policy":{"acknowledgement_minutes":60},"generated_by":"release-governance"}'
```

## Escalation Model

The escalation planner compares the latest notification plan per schedule against acknowledgement records:

- `healthy`: all selected notification routes are acknowledged or resolved.
- `warning`: selected routes are outstanding but not past the acknowledgement SLO.
- `critical`: selected routes are outstanding and older than the acknowledgement SLO.

Each route includes schedule ID, plan ID, provider, owner, acknowledgement state, age, SLO, breach state, and recommended action.

## User Stories

- As a release manager, I can prove that stale rollback drill notifications were acknowledged.
- As an incident commander, I can identify which notification route still needs owner action.
- As a platform owner, I can escalate missed drill notifications before promoted Go backend rollback confidence decays.
- As an auditor, I can review acknowledgement and escalation metadata without seeing connector credentials.

## Enterprise Challenge Solved

Connector delivery is not enough for regulated operations. CAVRA now tracks whether a human owner acknowledged stale rollback drill alerts and can produce a public-safe escalation plan when those alerts are missed.

## Next Work

The next recommended implementation step is to add Evidence Console drill notification acknowledgement and escalation drill-down views.
