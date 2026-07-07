# CAVRA Enterprise HA/DR Readiness

Last updated: 2026-07-07

This page defines the R2.3 public-safe high availability, disaster recovery, and data residency contract for CAVRA Enterprise and Managed deployments.

The public repository defines the contract, sample packet, and validators. Private Enterprise deployments must supply the live failover, restore, health, queue, database, and residency evidence.

## Scope

R2.3 covers:

- stateless API and control-plane topology;
- asynchronous worker redundancy;
- durable event bus or queue requirements;
- database redundancy, point-in-time restore, RPO, and tenant-scoped persistence;
- immutable or append-protected evidence store availability;
- health endpoints and production monitor alerts;
- backup/restore drill evidence;
- failover drill evidence;
- data residency policy validation.

## Public Artifacts

| Artifact | Purpose |
| --- | --- |
| `src/cavra/enterprise_ha.py` | Defines the HA/DR contract, readiness packet, and evidence packet validator. |
| `scripts/validate_enterprise_ha_readiness.py` | Validates a sample or live Enterprise HA/DR evidence packet. |
| `examples/operations/enterprise-ha-readiness.sample.json` | Public-safe sample packet showing the expected evidence shape. |
| `examples/operations/enterprise-ha-readiness.live.sanitized.example.json` | Sanitized live-mode example that passes `--require-live` without exposing real customer infrastructure. |
| `.github/workflows/enterprise-ha-readiness.yml` | CI workflow for sample validation and manual strict live validation. |
| `tests/test_enterprise_ha.py` | Contract, sample, live-mode, blocker, and readiness tests. |
| `docs/enterprise-ha-dr-azure-evidence-map.md` | Azure evidence mapping runbook for private Managed and Enterprise deployments. |

## Target SLOs

The public default targets are:

| Target | Default |
| --- | --- |
| API replicas | At least 2 |
| Worker replicas | At least 2 |
| RTO | 60 minutes |
| RPO | 15 minutes |
| API model | Stateless |
| Queue/event bus | Durable, replay-capable, with dead-letter handling |
| Evidence store | Immutable or append-protected |

Enterprise deployments may set stricter RTO/RPO values, but cannot pass the default public readiness gate with weaker values.

## Required Topology

| Component | Requirement |
| --- | --- |
| API/control plane | Stateless replicas behind a managed ingress, load balancer, Front Door, WAF, or equivalent. |
| Worker pool | Redundant workers for connector jobs, report jobs, posture updates, and evidence tasks. |
| Event bus | Durable queue or event bus with replay and dead-letter queues. |
| Database | Managed Postgres or equivalent with zone redundancy, PITR, and tenant isolation. |
| Evidence store | Immutable Blob/Object Lock or append-protected store for audit evidence. |
| Observability | Health endpoints, SLO alerts, queue-depth alerts, DB lag alerts, backup failure alerts, and evidence-write alerts. |
| Data residency | Observed storage, database, queue, and evidence locations must remain inside the tenant policy. |

## Evidence Packet

The packet schema is:

```json
{
  "schema_version": "cavra.enterprise_ha.evidence.v1",
  "evidence_mode": "sample",
  "deployment": {
    "api_replicas": 2,
    "worker_replicas": 2,
    "stateless_api": true
  },
  "event_bus": {
    "durable": true,
    "dead_letter_queue": true,
    "replay_supported": true
  },
  "database": {
    "multi_az": true,
    "point_in_time_restore": true,
    "rpo_minutes": 15
  },
  "backup_restore": {
    "restore_tested": true,
    "restore_duration_minutes": 45
  },
  "failover": {
    "tested": true,
    "failover_minutes": 30,
    "data_loss_minutes": 5
  },
  "health": {
    "endpoints": ["/health", "/version", "/console/config"],
    "monitor_alerts": [
      "api_availability",
      "queue_depth",
      "db_replication_lag",
      "backup_failure",
      "evidence_write_failure"
    ]
  },
  "data_residency": {
    "allowed_regions": ["eastus", "eastus2"],
    "observed_regions": ["eastus"]
  },
  "evidence": {
    "immutable_store_enabled": true
  }
}
```

`evidence_mode: sample` validates the packet shape only. Production readiness requires `evidence_mode: live` and `--require-live`.

## Validation

Public/sample validation:

```bash
python3 scripts/validate_enterprise_ha_readiness.py \
  --packet examples/operations/enterprise-ha-readiness.sample.json \
  --output dist/test/enterprise-ha-readiness-sample.json
```

Private live validation:

```bash
python3 scripts/validate_enterprise_ha_readiness.py \
  --packet .cavra/enterprise/enterprise-ha-readiness-live.json \
  --require-live \
  --output dist/enterprise/enterprise-ha-readiness-result.json
```

Sanitized live-mode template validation:

```bash
python3 scripts/validate_enterprise_ha_readiness.py \
  --packet examples/operations/enterprise-ha-readiness.live.sanitized.example.json \
  --require-live
```

Unit tests:

```bash
python3 -m pytest tests/test_enterprise_ha.py -q
```

## Completion Criteria

R2.3 is public-repository complete. The public code exposes and validates the HA/DR contract, sample packet, sanitized live-mode packet, strict workflow, Azure evidence map runbook, RTO/RPO checks, failover checks, restore checks, health endpoint checks, monitor alert checks, data residency checks, and immutable evidence-store checks.

Real cloud topology, runtime failover logs, restore transcripts, monitor alert histories, private network details, database identifiers, and customer residency evidence remain deployment-specific and belong in private Managed or Enterprise evidence rooms.

See [Enterprise HA/DR R2.3 Closeout](Enterprise-HA-DR-R2.3-Closeout.md) for the completion boundary.

Production deployment readiness requires a private live packet that returns:

```json
{
  "ready_for_enterprise_live_ha": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

Until then, the public contract is complete but the Enterprise deployment remains pending private live HA/DR evidence.

## AISPM Production Gate Link

The final AISPM production readiness gate should include the live HA/DR packet as operating evidence. A deployment is not launch-ready if:

- failover was not tested;
- restore was not tested;
- RTO/RPO targets were missed;
- queue replay or dead-letter handling is missing;
- data residency evidence is missing or out of policy;
- evidence store immutability is not enabled.

## Azure Evidence Map

For Azure Managed or Enterprise Subscription deployments, use [CAVRA Enterprise HA/DR Azure Evidence Map](Enterprise-HA-DR-Azure-Evidence-Map.md) to translate Container Apps or AKS, Service Bus or Event Grid, Postgres, Blob immutable storage, Monitor/Application Insights, and Front Door/WAF evidence into the validator packet.
