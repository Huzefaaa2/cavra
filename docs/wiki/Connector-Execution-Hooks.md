# Connector Execution Hooks

CAVRA supports live connector execution hooks for SIEM, ChatOps, ITSM, and generic webhooks.

## Providers

- Splunk HEC
- Microsoft Sentinel or Log Analytics ingestion endpoints
- Datadog Logs
- Slack incoming webhooks
- Microsoft Teams incoming webhooks
- Jira issue API
- ServiceNow change request API
- Generic webhooks

## Configuration

Use `examples/connectors/cavra-connectors.example.json`. Set `CAVRA_CONNECTOR_CONFIG` for the API and CLI.

Secrets should come from environment variables through `token_env`, `api_key_env`, `authorization_env`, or `url_env`.

## API

- `POST /integrations/{integration_id}/deliver`

The endpoint loads the integration record, uses its provider by default, sends the event through the configured connector, and returns redacted delivery evidence.

## CLI

```bash
cavra integration deliver .cavra/evidence/latest/siem-event.json --config .cavra/connectors.json --provider splunk
```

## User Stories

- As a SOC analyst, I can receive CAVRA evidence in SIEM.
- As a platform engineer, I can notify Slack or Teams with redacted evidence.
- As a change manager, I can create Jira or ServiceNow records.
- As an auditor, I can inspect delivery attempts without seeing secrets.

## Enterprise Value

Connector hooks make CAVRA operational inside enterprise systems of record rather than stopping at generated payload files.
