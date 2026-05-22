# Go Backend Rollback Drill Audit Delivery Health

CAVRA now exposes acknowledgement audit delivery history filters and delivery health dashboards for rollback drill evidence routing.

## What This Adds

- History filters for acknowledgement audit delivery plans, connector delivery source, delivery success, alert level, audit ID, delivery ID, and cadence.
- Dashboard metrics for acknowledgement audit package count, delivery plan count, connector delivery attempts, failed audit deliveries, delivery success count, success rate, delivery providers, and audit delivery health.
- Evidence Console filtering for **Delivery source** across drill notifications and acknowledgement audit delivery.
- Evidence Console provider filtering for SIEM, ITSM, ChatOps, and webhook destinations.
- Evidence Console health cards for audit delivery health, audit delivery plans, audit sends, failed audit sends, and audit success rate.
- Roadmap and wiki updates that move the next implementation target to acknowledgement audit retry execution approvals and connector recovery playbooks.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Use the dashboard cards to check whether acknowledgement audit delivery is healthy. Use the history filters to isolate:

- delivery source: drill notification or acknowledgement audit
- provider: Splunk, Sentinel, Datadog, Jira, ServiceNow, Slack, Teams, or Webhook
- state: delivered, delivery failed, critical, healthy, outstanding, resolved, or escalated
- metadata kind: acknowledgement audit package, acknowledgement audit delivery plan, or connector delivery

## API

```text
GET /runtime/go-pilot/rollback-drill-notifications
GET /runtime/go-pilot/rollback-drill-notifications/dashboard
```

Additional history query fields:

```text
connector_delivery_source=go_backend_rollback_drill_acknowledgement_audit
delivery_success=false
alert_level=critical
audit_id=<audit-package-id>
delivery_id=<delivery-plan-or-connector-event-id>
cadence=hourly
```

Dashboard fields include:

- `acknowledgement_audit_delivery_plan_count`
- `acknowledgement_audit_delivery_count`
- `failed_acknowledgement_audit_delivery_count`
- `acknowledgement_audit_delivery_success_count`
- `acknowledgement_audit_delivery_success_rate`
- `acknowledgement_audit_delivery_providers`
- `acknowledgement_audit_delivery_health`

## Security Boundary

The dashboard is built from public-safe metadata only. It does not expose connector credentials, private URLs, customer payloads, Enterprise source code, or license validation secrets.

## User Stories

- As a release manager, I can see whether acknowledgement audit evidence reached its configured destinations.
- As a SOC analyst, I can filter delivery history to failed SIEM routes.
- As an ITSM owner, I can isolate Jira or ServiceNow delivery attempts for a specific audit package.
- As an auditor, I can review evidence delivery health without needing access to connector secrets.

## Enterprise Challenge Solved

Enterprise rollback evidence must be discoverable after delivery, not only sent once. Delivery health dashboards make failed acknowledgement audit routing visible, searchable, and ready for retry automation.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-audit-delivery-health.svg`.

## Next Work

The next recommended implementation step is to add acknowledgement audit retry execution approvals and connector recovery playbooks.
