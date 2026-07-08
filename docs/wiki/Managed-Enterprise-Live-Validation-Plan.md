# CAVRA Managed And Enterprise Live Validation Plan

The Managed and Enterprise live validation plan is the operating bridge between the completed public roadmap and a real customer production environment. It does not store customer secrets or raw logs. It stores sanitized references proving that each live validator was run and that the resulting evidence is in the customer evidence room.

## What It Proves

The plan requires live sanitized references for:

- identity and access validation;
- tenant isolation and Postgres/RLS smoke validation;
- HA/DR readiness;
- evidence custody and immutable audit;
- connector and scanner delivery;
- policy lifecycle and continuous monitoring;
- runtime workflow validation against real agent/tool workflows;
- AISPM production readiness;
- SMTP/report delivery validation;
- customer evidence-room closeout;
- customer operating-review closeout.

## Generate Templates

```bash
python3 scripts/validate_managed_enterprise_live_validation_plan.py \
  --export-dir examples/managed-enterprise-live-validation
```

## Validate A Live Sanitized Plan

```bash
python3 scripts/validate_managed_enterprise_live_validation_plan.py \
  --plan examples/managed-enterprise-live-validation/managed-enterprise-live-validation-plan.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_live_validation": true,
  "blocker_count": 0
}
```

## Evidence Boundary

Do not commit tenant names, customer names, emails, SMTP credentials, tokens, raw connector responses, raw runtime logs, raw prompt samples, raw model data, customer payloads, or private policy packs.

Commit only references such as `evidence://`, `ticket://`, `audit://`, `runbook://`, `workflow://`, `vault://`, or `share://`.

## Required Stages

| Stage | Required signal |
| --- | --- |
| Identity and access | `ready_for_enterprise_live_identity` |
| Tenant isolation | `ready_for_postgres_tenant_rls_smoke` |
| HA/DR | `ready_for_enterprise_live_ha` |
| Evidence custody | `ready_for_enterprise_evidence_custody` |
| Immutable audit | `ready_for_enterprise_audit_log` |
| Connectors and scanners | `ready_for_enterprise_connectors_and_scanners` |
| Policy and monitoring | `ready_for_continuous_monitoring` |
| Runtime workflows | `ready_for_runtime_workflow_validation` |
| AISPM production gate | `ready_for_aispm_production` |
| SMTP/report delivery | `ready_for_report_delivery` |
| Customer evidence room | `ready_for_customer_evidence_room_closeout` |
| Customer operating closeout | `ready_for_customer_operating_review` |

## Relationship To The Roadmap

The public roadmap is complete for repository-visible public contracts. This plan is for the remaining deployment-specific work: running the actual validators against a real Managed or Enterprise environment and attaching the customer-safe refs to the private evidence room.
