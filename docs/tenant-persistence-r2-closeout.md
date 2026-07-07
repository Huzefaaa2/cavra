# CAVRA Tenant Persistence R2.2 Closeout

Last updated: 2026-07-07

R2.2 is closed for the public CAVRA repository. The remaining real Postgres host, runtime database role, connection secret, backup configuration, and customer tenant data evidence belongs to Managed or Enterprise deployment evidence rooms, not to public source code.

## What Is Complete

| Control | Public Status |
| --- | --- |
| Tenant/workspace persistence contract | Implemented |
| JSON tenant/workspace reference store | Implemented |
| SQLite tenant/workspace reference store | Implemented |
| Tenant/workspace scope helper | Implemented |
| Activity decision/session tenant binding | Implemented |
| Approval queue/history tenant binding | Implemented |
| Evidence metadata tenant binding | Implemented |
| Inventory tenant binding | Implemented |
| Integration tenant binding | Implemented |
| Postgres/RLS public table contract | Implemented |
| Postgres migration SQL with forced RLS | Implemented |
| JSON/SQLite-to-Postgres import row validation | Implemented |
| Request-scoped Postgres session adapter | Implemented |
| Public-safe RLS smoke harness | Implemented |
| Sanitized live-style Postgres RLS packet | Implemented |

## Evidence Boundary

The public repository proves CAVRA can:

- bind tenant and workspace identifiers across local operational stores;
- reject cross-tenant and cross-workspace scope mismatches;
- expose a production Postgres/RLS table and session-setting contract;
- validate JSON and SQLite migration rows before promotion to Postgres;
- apply transaction-local `cavra.tenant_id` and `cavra.workspace_id` settings;
- validate a sanitized live-style RLS smoke packet without storing DSNs or database host details.

Private Managed or Enterprise deployments must still attach their own:

- live Postgres database and runtime role evidence;
- private DSN secret handling evidence;
- migration application evidence;
- cross-tenant and cross-workspace negative test logs;
- backup, restore, retention, and residency evidence;
- production AISPM readiness evidence room references.

Those artifacts must stay private or be sanitized before publication.

## Verification

```bash
python3 scripts/validate_tenant_persistence_readiness.py

python3 scripts/validate_postgres_tenant_rls_smoke.py \
  --packet examples/postgres/enterprise-postgres-rls-smoke.live.sanitized.example.json \
  --require-live \
  --output dist/test/postgres-rls-smoke-live-sanitized-result.json

python3 -m pytest tests/test_postgres_tenancy.py tests/test_tenancy.py tests/test_activity.py tests/test_approvals.py tests/test_evidence.py tests/test_inventory.py tests/test_integrations.py -q
```

Expected live-style packet result:

```json
{
  "status": "pass",
  "live_rls_smoke_tested": true,
  "packet_validated": true,
  "validation_failures": []
}
```

## R2.3 Handoff

R2.3 HA/DR readiness must consume the same tenant/workspace-scoped operational stores from R2.2. If a deployment changes the tenant isolation model, database topology, RLS predicates, or tenant/workspace migration path, the R2.2 smoke packet must be regenerated before R2.3 is accepted.
