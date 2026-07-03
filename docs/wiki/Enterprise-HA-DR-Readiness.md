# Enterprise HA/DR Readiness

CAVRA R2.3 defines a public-safe high availability, disaster recovery, and data residency contract for Enterprise and Managed deployments.

## Implemented Foundation

| Component | Purpose |
| --- | --- |
| `build_enterprise_ha_contract` | Defines the required HA topology, health checks, queue/event bus expectations, backup/restore, RTO/RPO, and residency controls. |
| `validate_enterprise_ha_evidence_packet` | Validates sample or live HA/DR evidence packets. |
| `scripts/validate_enterprise_ha_readiness.py` | CLI validator for public sample packets and private live packets. |
| `examples/operations/enterprise-ha-readiness.sample.json` | Public-safe packet showing the expected HA/DR evidence shape. |
| `tests/test_enterprise_ha.py` | Contract, sample, live-mode, blocker, and readiness tests. |

## Default Targets

| Target | Default |
| --- | --- |
| API replicas | At least 2 |
| Worker replicas | At least 2 |
| RTO | 60 minutes |
| RPO | 15 minutes |
| Event bus | Durable, replay-capable, with dead-letter handling |
| Evidence store | Immutable or append-protected |

## Required Evidence

- Stateless API/control-plane replicas.
- Redundant workers for connector, report, posture, and evidence jobs.
- Durable event bus or queue with replay and dead-letter handling.
- Database redundancy, point-in-time restore, and RPO proof.
- Backup restore drill inside RTO.
- Failover drill inside RTO/RPO.
- Health endpoints: `/health`, `/version`, `/console/config`.
- Alerts for API availability, queue depth, database replication lag, backup failures, and evidence write failures.
- Data residency proof where observed regions are inside allowed regions.

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

R2.3 is production-complete only when the live packet returns `ready_for_enterprise_live_ha: true`, `blocker_count: 0`, and `warning_count: 0`.

Detailed repo document: [Enterprise HA/DR Readiness](https://github.com/Huzefaaa2/cavra/blob/main/docs/enterprise-ha-dr-readiness.md).
