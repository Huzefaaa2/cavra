# Connector Execution Hooks

CAVRA now supports live connector execution hooks for SIEM, ChatOps, ITSM, and generic webhooks.

## Supported Providers

- SIEM: Splunk HEC, Microsoft Sentinel or Log Analytics ingestion endpoints, Datadog Logs, generic webhook.
- ChatOps: Slack incoming webhooks, Microsoft Teams incoming webhooks.
- ITSM: Jira issue API, ServiceNow change request API.

## Configuration

Use `examples/connectors/cavra-connectors.example.json` as a starting point. Production deployments should store secrets in environment variables and reference them with `token_env`, `api_key_env`, `authorization_env`, or `url_env`.

```bash
export CAVRA_CONNECTOR_CONFIG=.cavra/connectors.json
export SPLUNK_HEC_URL=https://splunk.example/services/collector
export SPLUNK_HEC_TOKEN=...
```

Credential-bearing headers are redacted in delivery evidence. URLs with query strings are also redacted.

## API Delivery

Register an integration record:

```bash
curl -X POST http://127.0.0.1:8000/integrations \
  -H 'content-type: application/json' \
  -d '{"integration_id":"splunk","provider":"splunk","category":"siem","status":"active","health_status":"healthy"}'
```

Deliver an event through that integration:

```bash
curl -X POST http://127.0.0.1:8000/integrations/splunk/deliver \
  -H 'content-type: application/json' \
  -d '{"event":{"event_type":"cavra.evidence_bundle","session_id":"demo-session","decision_count":7,"blocked_count":4,"approval_required_count":1,"max_severity":"high"},"retries":1}'
```

The response uses `cavra.connector.delivery.v1` and records provider, success, status code, attempt count, redacted request metadata, and errors.

## CLI Delivery

```bash
cavra integration deliver .cavra/evidence/latest/siem-event.json \
  --config .cavra/connectors.json \
  --provider splunk \
  --output .cavra/integrations/deliveries
```

## User Stories

- As a SOC analyst, I can receive CAVRA evidence events in SIEM without manually uploading JSON.
- As a platform engineer, I can send governance notifications to Slack or Teams with redacted delivery evidence.
- As a change manager, I can create Jira or ServiceNow records from CAVRA events.
- As an auditor, I can inspect delivery evidence without seeing connector secrets.

## Enterprise Value

Connector execution hooks move CAVRA from generated payloads to operational delivery. Teams can route AI-agent governance evidence into existing SOC, ChatOps, and change-management systems while preserving redacted audit trails.
