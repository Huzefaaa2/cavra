# CAVRA Tenant And Workspace Persistence

Last updated: 2026-07-03

This page defines the first R2.2 tenant/workspace persistence contract for CAVRA. It is a public-safe foundation for tenant isolation, workspace scoping, and later production database migration.

## Scope

The public repository now includes:

- `TenantWorkspaceStore`: JSON reference store for local tenant/workspace records.
- `SQLiteTenantWorkspaceStore`: SQLite reference store for local tenant/workspace records.
- Tenant/workspace-aware activity stores for runtime decisions and session summaries.
- Tenant/workspace-aware approval stores for approval queues and decision history.
- Tenant/workspace-aware evidence metadata, inventory, and integration stores for local operating evidence.
- `assert_tenant_workspace_scope`: shared guard for actor/resource tenant and workspace comparisons.
- `build_tenant_persistence_contract`: public contract for required tenant/workspace fields and isolation rules.
- `build_tenant_persistence_readiness`: readiness packet for the R2.2 foundation.
- `build_postgres_rls_contract`: public-safe Postgres/RLS production data model contract.
- `build_postgres_import_rows`: JSON/SQLite import row builder that rejects missing tenant/workspace scope.
- `migrations/postgres/001_tenant_scoped_operational_stores.sql`: Postgres DDL and row-level security policy contract for the tenant-scoped operational stores.

This is not the final Enterprise SaaS data plane. Production Managed or Enterprise deployments should bind the same contract to Postgres, row-level security, encrypted backups, immutable audit, and tenant-specific retention.

## Record Contract

Tenant records require:

| Field | Purpose |
| --- | --- |
| `tenant_id` | Required tenant boundary used by identity, persistence, evidence, policy, and report surfaces. |
| `status` | Tenant lifecycle state: `active`, `suspended`, `disabled`, or `archived`. |
| `data_residency` | Public-safe residency intent such as `us`, `eu`, `in`, or `customer_managed`. |
| `identity_provider` | Identity provider family used for R2.1 claims and actor context. |

Workspace records require:

| Field | Purpose |
| --- | --- |
| `tenant_id` | Tenant boundary inherited by the workspace. |
| `workspace_id` | Workspace boundary inside the tenant. |
| `status` | Workspace lifecycle state. |
| `environment` | Environment label such as production, staging, or development. |
| `default_policy_pack` | Default policy pack for scoped activity. |

## Isolation Rules

R2.2 starts with these rules:

1. Every tenant-scoped record must include `tenant_id`.
2. Every workspace-scoped record must include `tenant_id` and `workspace_id`.
3. Actor `tenant_id` must match resource `tenant_id` before scoped data is returned or mutated.
4. Actor `workspace_id` must match resource `workspace_id` when the resource has workspace scope.
5. JSON and SQLite are Community-safe reference implementations; production SaaS should enforce the same predicates in Postgres with row-level security or an equivalent tenant predicate layer.

## Operational Store Binding

The R2.2 foundation now binds tenant/workspace scope into these operational stores:

| Store | Tenant fields | Scoped query helpers |
| --- | --- | --- |
| `ActivityStore` | Runtime decision records and session summaries include optional `tenant_id` and `workspace_id`. | `list_decisions_for_scope`, `list_sessions_for_scope`, `summarize_sessions_for_scope`. |
| `SQLiteActivityStore` | SQLite `activity_decisions` and `activity_sessions` tables include nullable `tenant_id` and `workspace_id` columns plus tenant/workspace indexes. Existing local DBs are migrated in place. | `list_decisions_for_scope`, `list_sessions_for_scope`, `summarize_sessions_for_scope`. |
| `ApprovalStore` | Approval records copy scope from the decision/resource context and can still filter legacy approvals where scope only exists inside `decision`. | `list_for_scope`. |
| `SQLiteApprovalStore` | SQLite `approvals` table includes nullable `tenant_id` and `workspace_id` columns plus a tenant/workspace index. Existing local DBs are migrated in place. | `list_for_scope`. |
| `EvidenceMetadataStore` | Evidence metadata records include optional `tenant_id` and `workspace_id`. | `list_for_scope`. |
| `SQLiteEvidenceMetadataStore` | SQLite `evidence_metadata` includes nullable `tenant_id` and `workspace_id` columns plus a tenant/workspace index. Existing local DBs are migrated in place. | `search_for_scope`. |
| `InventoryStore` | Repository and policy rollout records include optional `tenant_id` and `workspace_id`. | `list_repositories_for_scope`, `list_policy_rollouts_for_scope`. |
| `SQLiteInventoryStore` | SQLite repository and rollout inventory tables include nullable `tenant_id` and `workspace_id` columns plus tenant/workspace indexes. Existing local DBs are migrated in place. | `list_repositories_for_scope`, `list_policy_rollouts_for_scope`. |
| `IntegrationStore` | Integration inventory records include optional `tenant_id` and `workspace_id`. | `list_integrations_for_scope`. |
| `SQLiteIntegrationStore` | SQLite integration inventory includes nullable `tenant_id` and `workspace_id` columns plus a tenant/workspace index. Existing local DBs are migrated in place. | `list_integrations_for_scope`. |

These stores remain local reference implementations. The production Enterprise implementation should map the same fields into Postgres with mandatory tenant predicates, row-level security, encrypted backups, retention policy, and cross-tenant negative tests.

## Postgres/RLS Production Contract

The public repo now defines the production database contract without exposing private database hosts, credentials, or deployment topology. Private Managed and Enterprise deployments should use the same table names, record keys, and session settings.

Contract source:

| Artifact | Purpose |
| --- | --- |
| `src/cavra/postgres_tenancy.py` | Defines `POSTGRES_TENANT_RLS_CONTRACT_VERSION`, the tenant-scoped table map, required session settings, readiness checks, and JSON/SQLite import row validation. |
| `migrations/postgres/001_tenant_scoped_operational_stores.sql` | Creates the public-safe Postgres schema, enables and forces row-level security, and binds policies to the `cavra.tenant_id` and `cavra.workspace_id` session settings. |
| `tests/test_postgres_tenancy.py` | Verifies the contract shape, SQL policy coverage, JSON import rows, SQLite import rows, and negative validation for missing tenant/workspace scope. |

The contract covers these tables:

| Source | Postgres table | Scope |
| --- | --- | --- |
| Tenant records | `cavra.tenants` | `tenant_id` |
| Workspace records | `cavra.workspaces` | `tenant_id`, `workspace_id` |
| Evidence metadata | `cavra.evidence_metadata` | `tenant_id`, `workspace_id` |
| Approval queue/history | `cavra.approvals` | `tenant_id`, `workspace_id` |
| Activity sessions | `cavra.activity_sessions` | `tenant_id`, `workspace_id` |
| Activity decisions | `cavra.activity_decisions` | `tenant_id`, `workspace_id` |
| Repository inventory | `cavra.inventory_repositories` | `tenant_id`, `workspace_id` |
| Policy rollout inventory | `cavra.inventory_policy_rollouts` | `tenant_id`, `workspace_id` |
| Integration inventory | `cavra.integrations` | `tenant_id`, `workspace_id` |

Private runtime code must set the request scope before accessing tenant-scoped tables:

```sql
SET LOCAL cavra.tenant_id = '<tenant-id>';
SET LOCAL cavra.workspace_id = '<workspace-id>';
```

The application runtime role should not own these tables and should not have `BYPASSRLS`. The migration contract uses `ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY` so reads and writes are filtered through `current_setting('cavra.tenant_id', true)` and `current_setting('cavra.workspace_id', true)`.

`build_postgres_import_rows` creates normalized import rows from JSON and SQLite reference stores. It rejects production operational records unless `tenant_id`, `workspace_id`, and the required source record ID are present. This prevents unscoped local artifacts from being silently promoted into the Enterprise database.

## Validation

```bash
python3 scripts/validate_tenant_persistence_readiness.py
python3 -m pytest tests/test_postgres_tenancy.py tests/test_tenancy.py tests/test_activity.py tests/test_approvals.py tests/test_evidence.py tests/test_inventory.py tests/test_integrations.py -q
```

Expected result:

```text
tenant persistence readiness controls validated
```

## Migration Path

Completed in the public R2.2 foundation:

- JSON and SQLite tenant/workspace reference stores;
- tenant/workspace scope binding across activity, approvals, evidence metadata, inventory, and integrations;
- public Postgres/RLS DDL contract for the production operational stores;
- JSON/SQLite to Postgres import row validation tests.

Remaining Enterprise deployment work:

- wire the private Postgres driver/connection layer to set `cavra.tenant_id` and `cavra.workspace_id` for every request;
- use the `tenant_id` and `workspace_id` from the live identity validation packet as isolation inputs;
- run live cross-tenant and cross-workspace negative tests before any production readiness gate is allowed to pass;
- attach live RLS smoke evidence to the AISPM production readiness gate.
