# Go Backend Rollback Drill Scheduling

CAVRA now tracks recurring rollback drill schedules for promoted Go backend pilots and can deliver stale or due-soon drill notifications through configured release-governance connectors. Drill history proves the fallback path works; drill scheduling proves the fallback path keeps getting exercised.

## What Scheduling Requires

Rollback drill scheduling requires:

- `CAVRA_GO_BACKEND_MODE=promoted` or an explicit schedule request.
- `CAVRA_GO_ROLLBACK_DRILL_SCHEDULE` points to public-safe schedule metadata.
- The schedule uses schema `cavra.go-backend-rollback-drill-schedule.v1`.
- `status=active`.
- `interval_days` is positive.
- `next_due_at` is present, or CAVRA can derive the next due date from latest drill history plus `interval_days`.
- Owners and notification providers are configured.
- A runbook reference is present.
- Optional `owner_routes`, `maintenance_windows`, and `owner_calendars` contain public-safe routing metadata only.

The public schedule schema is:

```json
{
  "schema_version": "cavra.go-backend-rollback-drill-schedule.v1",
  "schedule_id": "go_backend_python_fallback_monthly",
  "environment": "production-pilot",
  "status": "active",
  "interval_days": 30,
  "next_due_at": "2026-06-20T15:40:00Z",
  "owners": ["release-governance"],
  "notification_providers": ["slack", "teams"],
  "owner_routes": {
    "release-governance": {
      "providers": ["slack", "teams"],
      "acknowledgement_minutes": 30,
      "escalation_owner": "platform-lead"
    }
  },
  "maintenance_windows": [],
  "owner_calendars": {},
  "runbook_ref": "docs/go-backend-rollback-drill-scheduling.md"
}
```

Do not include connector secrets, private URLs, customer names, endpoint hostnames, or private automation scripts in public schedule metadata.

## Environment Variables

```bash
export CAVRA_GO_BACKEND_MODE=promoted
export CAVRA_GO_ROLLBACK_DRILL_HISTORY=/etc/cavra/go-backend-rollback-drills.json
export CAVRA_GO_ROLLBACK_DRILL_SCHEDULE=/etc/cavra/go-backend-rollback-drill-schedule.json
export CAVRA_GO_ROLLBACK_DRILL_DUE_SOON_DAYS=14
export CAVRA_CONNECTOR_CONFIG=/etc/cavra/private/connectors.json
```

`CAVRA_CONNECTOR_CONFIG` remains outside the public repository and is responsible for webhook, Slack, Teams, Jira, ServiceNow, or private connector credentials.

## CLI Usage

```bash
cavra runtime go-rollback-drill-schedule \
  --mode promoted \
  --rollback-drill-history-path /etc/cavra/go-backend-rollback-drills.json \
  --rollback-drill-schedule-path /etc/cavra/go-backend-rollback-drill-schedule.json \
  --rollback-drill-due-soon-days 14 \
  --json
```

Build a notification plan without sending connector traffic:

```bash
cavra runtime go-rollback-drill-notification-plan \
  --mode promoted \
  --rollback-drill-history-path /etc/cavra/go-backend-rollback-drills.json \
  --rollback-drill-schedule-path /etc/cavra/go-backend-rollback-drill-schedule.json \
  --routing-policy /etc/cavra/go-backend-rollback-drill-routing.json \
  --provider slack \
  --json
```

Promoted-mode evaluation checks that a schedule is configured and not stale:

```bash
cavra runtime go-pilot-evaluate execute_command "terraform plan" \
  --mode promoted \
  --runtime-path /opt/cavra/bin/cavra-runtime \
  --policy-path /etc/cavra/compiled-policy.json \
  --package-dir /opt/cavra/go-runtime-release \
  --promotion-evidence-path /etc/cavra/go-backend-promotion-evidence.json \
  --rollback-plan-path /etc/cavra/go-backend-rollback-plan.json \
  --rollback-rehearsal-path /etc/cavra/go-backend-rollback-rehearsal.json \
  --rollback-drill-history-path /etc/cavra/go-backend-rollback-drills.json \
  --rollback-drill-schedule-path /etc/cavra/go-backend-rollback-drill-schedule.json \
  --json
```

## API Usage

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-schedule
curl -X POST http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-notifications/deliver \
  -H 'content-type: application/json' \
  -d '{"provider":"slack","retries":2}'
```

The delivery endpoint builds `cavra.go-backend-pilot.rollback-drill-notification-plan.v1`, applies optional owner routing, maintenance windows, and owner calendars from `routing_policy`, emits `cavra.go_backend.rollback_drill.notification`, and indexes redacted connector delivery evidence as `release-connector-delivery` with source `go_backend_rollback_drill_notification`.

Acknowledgement and escalation follow-up is documented in [Go Backend Rollback Drill Notification Escalation](go-backend-rollback-drill-notification-escalation.md).
Owner routing and maintenance-window behavior is documented in [Go Backend Rollback Drill Routing](go-backend-rollback-drill-routing.md).

## Evidence Console

Production readiness now includes:

- `go_backend_rollback_drill_schedule`
- next drill due date
- stale and due-soon state
- configured notification providers

`ready`, `due_soon`, and `not_requested` are acceptable production-readiness states. `needs_attention` blocks readiness and promoted Go backend selection because the rollback drill schedule is missing, inactive, stale, or has no notification route.

## User Stories

- As a release manager, I can define the cadence for promoted Go backend rollback drills.
- As an incident commander, I can see when the next Python fallback drill is due.
- As a platform owner, I can route stale drill notifications to release governance connectors.
- As a release owner, I can suppress drill notifications during approved maintenance windows while preserving audit metadata.
- As an auditor, I can review schedule metadata and delivery evidence without seeing connector secrets.

## Enterprise Challenge Solved

Rollback readiness decays when teams only prove it once. CAVRA keeps rollback confidence operational by combining drill history, recurring schedules, due-soon detection, stale detection, and connector-backed notification evidence.

## Next Work

The next recommended implementation step is to add acknowledgement audit worker health alerts and retry acknowledgements.
