# Integration Inventory

Phase 6 now includes durable enterprise integration inventory.

## What It Provides

- JSON and SQLite persistence for integration records.
- API filters for provider, category, status, owner, environment, and health status.
- Console view for source control, CI/CD, SIEM, ITSM, ChatOps, identity, storage, security, and observability connectors.
- Evidence references so integration records can link to setup reviews, delivery tests, or operational checks.
- Live connector execution hooks for Splunk, Microsoft Sentinel, Datadog, Slack, Microsoft Teams, Jira, ServiceNow, and generic webhooks.

## How To Use

Configure JSON persistence:

```bash
export CAVRA_INTEGRATION_STORE=.cavra/api/integrations.json
```

Configure SQLite persistence:

```bash
export CAVRA_INTEGRATION_DB=.cavra/api/integrations.db
cavra evidence migrate --sqlite .cavra/api/integrations.db
```

Create or update an integration:

```bash
curl -X POST http://127.0.0.1:8000/integrations \
  -H 'content-type: application/json' \
  -d '{"integration_id":"github-enterprise","provider":"github","category":"source_control","status":"active","health_status":"healthy","owner":"Developer Platform"}'
```

Deliver an event through a configured connector:

```bash
export CAVRA_CONNECTOR_CONFIG=.cavra/connectors.json
curl -X POST http://127.0.0.1:8000/integrations/splunk/deliver \
  -H 'content-type: application/json' \
  -d '{"event":{"event_type":"cavra.evidence_bundle","session_id":"release-42"},"provider":"splunk"}'
```

Or from the CLI:

```bash
cavra integration deliver .cavra/evidence/latest/siem-event.json --config .cavra/connectors.json --provider splunk
```

## User Stories

- As a platform engineer, I can see which enterprise systems CAVRA is configured to use.
- As a SOC lead, I can track SIEM connector status and ownership.
- As a SOC lead, I can deliver CAVRA evidence events into SIEM, ITSM, and ChatOps systems with credential-redacted delivery records.
- As an auditor, I can confirm that enterprise integration records have owners, health state, and evidence references.

## Enterprise Challenge Solved

Integration inventory prevents source control, SIEM, ITSM, identity, and storage connectors from becoming undocumented deployment drift. It gives operators one API and console view for connector ownership, health, capability scope, and delivery evidence.

## Next

The next recommended work is Azure DevOps required-check enforcement, immutable evidence store deployment references, and OIDC/RBAC deployment bundles.
