# CAVRA Tenant Persistence R2.2 Closeout

Last updated: 2026-07-07

R2.2 is closed for the public CAVRA repository. Real Postgres host, runtime database role, connection secret, backup configuration, and customer tenant data evidence belongs to Managed or Enterprise deployment evidence rooms, not to public source code.

## Completed Public Controls

| Control | Status |
| --- | --- |
| Tenant/workspace persistence contract | Implemented |
| JSON and SQLite tenant/workspace reference stores | Implemented |
| Activity, approval, evidence, inventory, and integration tenant binding | Implemented |
| Postgres/RLS public table contract | Implemented |
| Forced RLS migration SQL | Implemented |
| JSON/SQLite-to-Postgres import validation | Implemented |
| Request-scoped Postgres session adapter | Implemented |
| Public-safe RLS smoke harness | Implemented |
| Sanitized live-style Postgres RLS packet | Implemented |

## Evidence Boundary

The public repository proves that CAVRA can bind and validate `tenant_id` and `workspace_id` across local stores, migration rows, and a public Postgres/RLS contract.

Private deployments must attach live Postgres, runtime role, DSN secret handling, migration application, cross-tenant negative tests, backup, restore, retention, residency, and AISPM evidence room artifacts privately.

## Verification

```bash
python3 scripts/validate_tenant_persistence_readiness.py

python3 scripts/validate_postgres_tenant_rls_smoke.py \
  --packet examples/postgres/enterprise-postgres-rls-smoke.live.sanitized.example.json \
  --require-live \
  --output dist/test/postgres-rls-smoke-live-sanitized-result.json

python3 -m pytest tests/test_postgres_tenancy.py tests/test_tenancy.py tests/test_activity.py tests/test_approvals.py tests/test_evidence.py tests/test_inventory.py tests/test_integrations.py -q
```

## R2.3 Handoff

R2.3 HA/DR readiness must consume the same tenant/workspace-scoped operational stores from R2.2. If a deployment changes tenant isolation model, database topology, RLS predicates, or migration path, the R2.2 smoke packet must be regenerated before R2.3 is accepted.
