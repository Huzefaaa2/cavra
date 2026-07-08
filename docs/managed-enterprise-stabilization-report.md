# CAVRA Managed And Enterprise Stabilization Report

The Managed and Enterprise stabilization report closes the first post-cutover production window. It proves that the environment stayed healthy after activation, support and alert queues were triaged, rollback status was recorded, and customer-safe closeout evidence was archived.

Use it after the [Managed And Enterprise Cutover Runbook](managed-enterprise-cutover-runbook.md) is complete.

## What It Proves

The report requires sanitized references for:

- API uptime and health;
- identity, RBAC, break-glass, and operator access health;
- tenant isolation health;
- connector and scanner delivery health;
- runtime agent/tool control health;
- SMTP/report delivery health;
- AISPM posture generation health;
- audit, evidence custody, and archive health;
- support alerts, incidents, and customer-visible items;
- rollback status, open blockers, customer acceptance, and next operating review.

## Generate Templates

```bash
python3 scripts/validate_managed_enterprise_stabilization_report.py \
  --export-dir examples/managed-enterprise-stabilization
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-stabilization-report \
  --export-dir examples/managed-enterprise-stabilization
```

## Validate A Live Sanitized Stabilization Report

```bash
python3 scripts/validate_managed_enterprise_stabilization_report.py \
  --report examples/managed-enterprise-stabilization/managed-enterprise-stabilization-report.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-stabilization-report \
  --report examples/managed-enterprise-stabilization/managed-enterprise-stabilization-report.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_stabilization_closeout": true,
  "blocker_count": 0
}
```

## Required Health Signals

| Signal | Purpose |
| --- | --- |
| API health | API health and uptime are within the agreed stabilization window. |
| Identity health | SSO, RBAC, break-glass, and operator access are stable. |
| Tenant isolation health | Tenant isolation checks remain clean after activation. |
| Connector health | Connectors and scanners are delivering expected evidence references. |
| Runtime control health | Runtime agent/tool controls are evaluating expected workflows. |
| SMTP report health | SMTP/report delivery has no unresolved blocker. |
| AISPM health | AISPM posture generation has no production-readiness blocker. |
| Audit evidence health | Audit, evidence custody, and archive refs are complete. |
| Support alert health | Alerts, incidents, and customer-visible support items are triaged. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, private incident details, pricing, contracts, or legal terms.

Commit only sanitized references such as `evidence://`, `ticket://`, `audit://`, `runbook://`, `workflow://`, `vault://`, or `share://`.

## Relationship To Cutover

The cutover runbook proves activation was controlled. The stabilization report proves the activated environment remained healthy long enough to exit cutover mode and enter the normal Managed or Enterprise operating cadence.
