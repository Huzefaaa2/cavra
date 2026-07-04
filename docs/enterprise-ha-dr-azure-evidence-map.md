# CAVRA Enterprise HA/DR Azure Evidence Map

Last updated: 2026-07-04

This runbook maps Azure deployment evidence into the R2.3 HA/DR packet consumed by:

```bash
python3 scripts/validate_enterprise_ha_readiness.py --require-live
```

Use this runbook for private CAVRA Managed or Enterprise Subscription deployments. Do not commit real tenant names, subscription IDs, secrets, private endpoints, customer payloads, or incident records into the public repository.

## Evidence Packet Location

Recommended private path:

```text
.cavra/enterprise/enterprise-ha-readiness-live.json
```

Recommended validation command:

```bash
python3 scripts/validate_enterprise_ha_readiness.py \
  --packet .cavra/enterprise/enterprise-ha-readiness-live.json \
  --require-live \
  --output dist/enterprise/enterprise-ha-readiness-result.json
```

## Azure Field Mapping

| Packet section | Azure evidence source | Required fields |
| --- | --- | --- |
| `deployment.api_replicas` | Azure Container Apps revisions, AKS deployment replicas, or App Service scale-out settings. | Running replica count must be at least 2. |
| `deployment.worker_replicas` | Container Apps Jobs, AKS workers, WebJobs, or queue worker deployments. | Worker count must be at least 2. |
| `deployment.stateless_api` | Architecture decision, IaC config, and state-store references. | API/control plane must not depend on local disk or in-memory session state. |
| `event_bus` | Azure Service Bus or Event Grid configuration. | Durable queue/topic, dead-letter handling, and replay support. |
| `database` | Azure Database for PostgreSQL, Azure SQL, or equivalent managed DB configuration. | Zone redundancy or equivalent, PITR enabled, RPO within target. |
| `evidence` | Azure Blob immutable storage or append-protected evidence store. | Immutability policy or append protection enabled. |
| `backup_restore` | Restore drill ticket, backup policy, and restore transcript. | Restore tested and duration within RTO. |
| `failover` | Failover drill ticket, deployment event, and post-failover validation packet. | Failover tested, failover duration within RTO, data loss within RPO. |
| `health.endpoints` | Synthetic checks, smoke tests, or Application Insights availability tests. | `/health`, `/version`, and `/console/config`. |
| `health.monitor_alerts` | Azure Monitor alert rules and Action Groups. | `api_availability`, `queue_depth`, `db_replication_lag`, `backup_failure`, `evidence_write_failure`. |
| `data_residency` | Azure Policy, resource graph, tags, deployment region inventory, and storage/database region report. | Observed regions must be a subset of allowed regions. |

## Azure Reference Collection Commands

These commands are examples only. Replace resource names in your private environment.

```bash
az containerapp show \
  --name cavra-enterprise-api \
  --resource-group cavra-enterprise-prod \
  --query "{name:name, latestRevisionName:properties.latestRevisionName, minReplicas:properties.template.scale.minReplicas}"
```

```bash
az servicebus queue show \
  --namespace-name cavra-enterprise \
  --resource-group cavra-enterprise-prod \
  --name runtime-events \
  --query "{deadLetteringOnMessageExpiration:deadLetteringOnMessageExpiration, maxDeliveryCount:maxDeliveryCount}"
```

```bash
az postgres flexible-server show \
  --name cavra-enterprise-prod \
  --resource-group cavra-enterprise-prod \
  --query "{availabilityZone:availabilityZone, backup:backup, highAvailability:highAvailability, location:location}"
```

```bash
az storage container immutability-policy show \
  --account-name cavraevidenceprod \
  --container-name evidence
```

```bash
az monitor metrics alert list \
  --resource-group cavra-enterprise-prod \
  --query "[].{name:name, enabled:enabled, scopes:scopes}"
```

## Live Packet Rules

The live packet must:

- set `evidence_mode` to `live`;
- use sanitized provider refs, not secrets;
- include only resource IDs, evidence refs, drill IDs, or ticket refs safe for the evidence room;
- prove restore and failover were actually tested;
- keep `observed_regions` inside `allowed_regions`;
- be attached to the AISPM production readiness packet.

## GitHub Workflow

The public workflow `.github/workflows/enterprise-ha-readiness.yml` validates the sample contract on push and pull request. For private live validation, run the workflow manually with:

| Input | Value |
| --- | --- |
| `packet_path` | `.cavra/enterprise/enterprise-ha-readiness-live.json` or another private packet path available to the runner. |
| `require_live` | `true` |
| `rto_minutes` | Your launch target, default `60`. |
| `rpo_minutes` | Your launch target, default `15`. |

The workflow uploads the sanitized validation result as `enterprise-ha-readiness-live`.
