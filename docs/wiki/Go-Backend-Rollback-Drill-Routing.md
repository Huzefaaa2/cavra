# Go Backend Rollback Drill Routing

CAVRA now applies public-safe owner routing, owner calendars, and maintenance windows before delivering promoted Go backend rollback drill notifications. This keeps stale or due-soon drill follow-up accountable without exposing connector credentials, private calendars, or customer-specific routing logic.

## Routing Policy

Rollback drill routing policy can be stored in the public schedule metadata or supplied separately to CLI/API calls:

```json
{
  "owner_routes": {
    "release-governance": {
      "providers": ["slack", "teams"],
      "acknowledgement_minutes": 30,
      "escalation_owner": "platform-lead"
    }
  },
  "maintenance_windows": [
    {
      "window_id": "production-change-freeze",
      "start_at": "2026-05-21T18:00:00Z",
      "end_at": "2026-05-21T20:00:00Z",
      "owners": ["release-governance"],
      "providers": ["slack"],
      "reason": "production change freeze"
    }
  ],
  "owner_calendars": {
    "release-governance": {
      "unavailable_windows": [
        {
          "start_at": "2026-05-22T00:00:00Z",
          "end_at": "2026-05-22T08:00:00Z",
          "reason": "regional holiday"
        }
      ]
    }
  }
}
```

The public policy must contain only routing labels, public-safe owner names, provider names, public maintenance-window reasons, and timestamps. Connector secrets, private webhook URLs, customer names, hostnames, and internal calendar exports must stay outside this repository.

## CLI Usage

```bash
cavra runtime go-rollback-drill-notification-plan \
  --mode promoted \
  --rollback-drill-history-path /etc/cavra/go-backend-rollback-drills.json \
  --rollback-drill-schedule-path /etc/cavra/go-backend-rollback-drill-schedule.json \
  --routing-policy /etc/cavra/go-backend-rollback-drill-routing.json \
  --provider all \
  --json
```

The plan now includes:

- `owner_routes`
- `route_decisions`
- `deliverable_route_count`
- `suppressed_route_count`
- `maintenance_suppressed_count`
- `calendar_suppressed_count`

Routes with active maintenance windows or unavailable owner calendars are suppressed before connector delivery. Remaining deliverable routes define `selected_providers` and `acknowledgement_required_providers`.

## API Usage

```bash
curl -X POST http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-notifications/deliver \
  -H 'content-type: application/json' \
  -d '{
    "provider": "all",
    "routing_policy": {
      "owner_routes": {
        "release-governance": {
          "providers": ["slack"],
          "acknowledgement_minutes": 30
        }
      }
    }
  }'
```

The API accepts the same public-safe routing policy object. Private connector credentials still come only from `CAVRA_CONNECTOR_CONFIG` or private secret stores.

## Persisted Route History

CAVRA now flattens persisted notification plan route decisions into a filterable route history:

```bash
curl 'http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-notifications/routes?owner=release-governance&action=suppress&category=maintenance_window'
```

Each route row includes plan ID, schedule ID, owner, escalation owner, provider, action, suppression category, acknowledgement SLO, reason, maintenance-window ID, owner availability, and creation time. Supported categories are `maintenance_window`, `owner_calendar`, `healthy_schedule`, `other`, and the delivered action category.

## Suppression Trends

CAVRA also builds and persists suppression trend metadata:

```bash
curl 'http://127.0.0.1:8000/runtime/go-pilot/rollback-drill-notifications/suppression-trends?owner=release-governance'
```

The trend summarizes suppressed routes by category, owner, provider, and schedule. It writes metadata kind `go-backend-rollback-drill-routing-suppression-trend` so auditors can review suppression activity later without private connector credentials or internal calendar exports.

## Escalation SLOs

Owner-specific `acknowledgement_minutes` values are used by rollback drill notification escalation plans. This lets one owner route use a shorter acknowledgement SLO without changing the global default:

```bash
cavra runtime go-rollback-drill-escalation-plan \
  --routing-policy /etc/cavra/go-backend-rollback-drill-routing.json \
  --json
```

## User Stories

- As a release manager, I can route rollback drill notifications to different providers per owner.
- As an incident commander, I can suppress drill notifications during approved maintenance windows while preserving audit evidence.
- As a platform owner, I can apply owner-specific acknowledgement SLOs for promoted backend rollback confidence.
- As an auditor, I can review route decisions without seeing private connector credentials or customer calendar data.

## Enterprise Challenge Solved

Enterprise release teams need rollback drills to respect change freezes, owner availability, and team-specific escalation paths. CAVRA records those routing decisions as public-safe metadata so promoted Go backend pilots remain accountable without leaking private operational details.

## Next Work

The next recommended implementation step is to add acknowledgement audit worker health alerts and retry acknowledgements.
