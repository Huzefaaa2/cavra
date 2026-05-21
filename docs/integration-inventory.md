# Integration Inventory

Phase 6 now persists enterprise integration records for source control, CI/CD, SIEM, ITSM, ChatOps, identity, cloud, storage, security, and observability connectors.

## Feature Summary

CAVRA integration inventory gives platform and security teams a central view of which enterprise systems are connected or planned, who owns them, what capabilities they provide, how they authenticate, and whether the integration is healthy.

## API Surface

- `GET /integrations`
- `POST /integrations`
- `GET /integrations/{integration_id}`
- `POST /integrations/{integration_id}/deliver`

Supported filters:

- `provider`
- `category`
- `status`
- `owner`
- `environment`
- `health_status`

## Persistence

Default JSON store:

```bash
.cavra/api/integrations.json
```

Override the JSON path:

```bash
export CAVRA_INTEGRATION_STORE=.cavra/api/integrations.json
```

Use SQLite:

```bash
export CAVRA_INTEGRATION_DB=.cavra/api/integrations.db
cavra evidence migrate --sqlite .cavra/api/integrations.db
```

The migration `006_integrations_inventory.sql` creates the `integrations` table and indexes provider, category, status, owner, and health status.

## Console

The sandbox console includes an Enterprise Integrations view. It filters integration records by category, status, health, and owner, then displays provider, environment, capabilities, and operational status.

## Connector Execution

CAVRA can execute configured connector hooks for Splunk, Microsoft Sentinel, Datadog, Slack, Microsoft Teams, Jira, ServiceNow, and generic webhooks. Configure connector secrets outside the inventory record, set `CAVRA_CONNECTOR_CONFIG`, and call `POST /integrations/{integration_id}/deliver` or `cavra integration deliver`. Release governance records can use the same connector layer through `POST /promotion-executions/{execution_id}/audit-export/deliver`, `POST /rollback-executions/{rollback_id}/deliver`, `cavra release deliver-promotion-audit`, and `cavra release deliver-rollback-execution`.

Delivery evidence uses the `cavra.connector.delivery.v1` schema and redacts credentials before writing output.

## User Stories

- As a platform engineer, I can see which enterprise systems CAVRA is configured to use.
- As a SOC lead, I can track SIEM connector ownership and health status.
- As a SOC lead, I can deliver signed CAVRA evidence events into SIEM and ChatOps systems with credential-redacted delivery records.
- As a release manager, I can deliver promotion audit and rollback execution records through owned connectors with retry evidence.
- As an auditor, I can inspect whether source control, ITSM, identity, and evidence storage integrations have owners and evidence references.

## Enterprise Challenge Solved

Enterprise CAVRA deployments touch multiple control systems. Integration inventory prevents those connectors from becoming undocumented configuration drift by making ownership, status, health, and capability scope visible through the API and console. Connector execution turns those records into auditable delivery paths for SOC, ITSM, and collaboration workflows.

## Next Work

The next recommended work is continued generated enforcement contracts around release governance evidence payloads.
