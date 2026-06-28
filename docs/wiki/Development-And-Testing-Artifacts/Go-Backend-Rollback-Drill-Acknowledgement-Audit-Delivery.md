# Go Backend Rollback Drill Acknowledgement Audit Delivery

CAVRA now supports scheduled and on-demand delivery plans for rollback drill acknowledgement audit packages across SIEM, ITSM, ChatOps, and webhook connectors.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery` for building an acknowledgement audit package, creating a delivery plan, routing it through configured connectors, and indexing redacted delivery evidence.
- Public-safe delivery plans with destination provider, cadence, schedule reference, route count, outstanding count, escalation count, and selected connector providers.
- Redacted connector events for Splunk, Microsoft Sentinel, Datadog, Jira, ServiceNow, Slack, Teams, and generic webhooks.
- Evidence Console **Audit delivery** destination selection and **Deliver Ack Audit** action.
- Metadata history support for acknowledgement audit packages, acknowledgement audit delivery plans, and connector delivery records.
- Roadmap and wiki updates that move the next implementation target to acknowledgement audit retry execution approvals and connector recovery playbooks.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

1. Filter by owner, notification provider, state, route action, or suppression category.
2. Choose an **Audit delivery** destination such as Splunk, Sentinel, Datadog, Jira, ServiceNow, Slack, Teams, or Webhook.
3. Select **Deliver Ack Audit**.
4. Review persisted delivery plan and connector delivery metadata in the notification history table.

Authenticated deployments use the signed console actor for delivery plan generation.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery
```

Example request:

```json
{
  "owner": "release-governance",
  "provider": "webhook",
  "delivery_provider": "splunk",
  "generated_by": "release-manager",
  "cadence": "hourly",
  "schedule_ref": "release-governance-hourly"
}
```

The endpoint requires connector configuration. It returns:

- `audit_package`: public-safe acknowledgement audit package for the requested filter scope.
- `delivery_plan`: selected destinations, cadence, schedule reference, route count, and outstanding count.
- `delivery`: connector delivery attempt result.
- `metadata`: redacted connector delivery evidence indexed in the evidence store.

## Security Boundary

The Community Edition implementation does not include connector secrets, private license logic, customer-specific templates, or Enterprise source code. Connector credentials remain in `CAVRA_CONNECTOR_CONFIG` or the operator's secret store. Delivery events remove route notes before sending connector payloads.

## User Stories

- As a release manager, I can deliver acknowledgement audit evidence to a release-governance connector without manually downloading and forwarding JSON.
- As a SOC analyst, I can receive rollback drill acknowledgement coverage in a SIEM event stream.
- As an ITSM owner, I can create Jira or ServiceNow evidence records for missed or escalated rollback drill routes.
- As an auditor, I can correlate acknowledgement coverage, delivery cadence, and connector evidence without seeing connector credentials.

## Enterprise Challenge Solved

Enterprise rollback assurance depends on evidence reaching the systems that auditors, incident teams, and platform owners already use. Scheduled acknowledgement audit delivery turns console-only evidence into routed operational evidence while keeping the public repository free of proprietary Enterprise implementation and secrets.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-acknowledgement-audit-delivery.svg`.

## Next Work

The next recommended implementation step is to add approval-bound live retry execution records and connector recovery closure evidence.
