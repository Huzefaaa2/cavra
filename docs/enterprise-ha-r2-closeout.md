# CAVRA Enterprise HA/DR R2.3 Closeout

Last updated: 2026-07-07

R2.3 is closed for the public CAVRA repository. The remaining real cloud topology, runtime failover logs, restore transcripts, monitor alert histories, private network details, database identifiers, and customer residency evidence belongs to Managed or Enterprise deployment evidence rooms, not to public source code.

## What Is Complete

| Control | Public Status |
| --- | --- |
| HA/DR contract | Implemented |
| Readiness validator | Implemented |
| Public sample evidence packet | Implemented |
| Sanitized live-mode evidence packet | Implemented |
| Strict live validation workflow | Implemented |
| API/control-plane replica floor checks | Implemented |
| Worker replica floor checks | Implemented |
| Stateless API check | Implemented |
| Durable event bus, DLQ, and replay checks | Implemented |
| Database redundancy, PITR, and RPO checks | Implemented |
| Backup restore drill and RTO checks | Implemented |
| Failover drill and RTO/RPO checks | Implemented |
| Health endpoint and monitor alert checks | Implemented |
| Data residency checks | Implemented |
| Immutable evidence store checks | Implemented |
| Azure evidence map runbook | Implemented |

## Evidence Boundary

The public repository proves CAVRA can:

- define the HA/DR topology and default SLO targets;
- validate sample and live-mode evidence packets;
- reject weak topology, missing failover, missing restore, missed RTO/RPO, and out-of-policy residency;
- validate a sanitized live-mode HA/DR packet without exposing real customer infrastructure;
- map Azure Container Apps or AKS, Service Bus or Event Grid, Postgres, Blob immutable storage, Monitor/Application Insights, and Front Door/WAF evidence into the packet.

Private Managed or Enterprise deployments must still attach their own:

- live API, worker, ingress, and event-bus configuration evidence;
- backup restore transcript;
- failover drill transcript;
- database redundancy and PITR evidence;
- monitor alert export;
- immutable evidence-store evidence;
- data residency policy assignment and observed-region evidence;
- final AISPM production readiness evidence room reference.

Those artifacts must stay private or be sanitized before publication.

## Verification

```bash
python3 scripts/validate_enterprise_ha_readiness.py \
  --packet examples/operations/enterprise-ha-readiness.sample.json \
  --output dist/test/enterprise-ha-readiness-sample.json

python3 scripts/validate_enterprise_ha_readiness.py \
  --packet examples/operations/enterprise-ha-readiness.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-ha-readiness-live-sanitized-result.json

python3 -m pytest tests/test_enterprise_ha.py -q
```

Expected live-style packet result:

```json
{
  "ready_for_enterprise_live_ha": true,
  "status": "ready",
  "blocker_count": 0,
  "warning_count": 0
}
```

## R3.1 And R3.2 Handoff

R3.1 KMS/HSM evidence custody and R3.2 immutable audit logging must consume the same evidence-store and HA/DR assumptions from R2.3. If a deployment changes the evidence store, database topology, event bus, residency policy, RTO/RPO, or failover model, the R2.3 HA/DR packet must be regenerated before R3 evidence custody or immutable audit gates are accepted.
