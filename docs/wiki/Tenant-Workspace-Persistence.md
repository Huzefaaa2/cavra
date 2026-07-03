# Tenant Workspace Persistence

CAVRA R2.2 starts with a public-safe tenant/workspace persistence contract and reference stores.

## Implemented Foundation

| Component | Purpose |
| --- | --- |
| `TenantWorkspaceStore` | JSON reference store for local tenant and workspace records. |
| `SQLiteTenantWorkspaceStore` | SQLite reference store for local tenant and workspace records. |
| `ActivityStore` / `SQLiteActivityStore` | Runtime decision and session history can carry and filter by `tenant_id` and `workspace_id`. |
| `ApprovalStore` / `SQLiteApprovalStore` | Approval queues and approval history can carry and filter by `tenant_id` and `workspace_id`. |
| `EvidenceMetadataStore` / `SQLiteEvidenceMetadataStore` | Evidence metadata can carry and filter by `tenant_id` and `workspace_id`. |
| `InventoryStore` / `SQLiteInventoryStore` | Repository and policy rollout inventory can carry and filter by `tenant_id` and `workspace_id`. |
| `IntegrationStore` / `SQLiteIntegrationStore` | Integration inventory can carry and filter by `tenant_id` and `workspace_id`. |
| `assert_tenant_workspace_scope` | Rejects actor/resource tenant or workspace mismatches. |
| `build_tenant_persistence_contract` | Publishes required tenant/workspace fields and isolation rules. |
| `build_tenant_persistence_readiness` | Produces the R2.2 foundation readiness result. |
| `build_postgres_rls_contract` | Publishes the public-safe Postgres/RLS table and session-setting contract. |
| `build_postgres_import_rows` | Converts JSON/SQLite reference rows into validated Postgres import rows. |
| `migrations/postgres/001_tenant_scoped_operational_stores.sql` | Defines the tenant-scoped Postgres tables and RLS policies. |

## Isolation Rules

- Every tenant-scoped record must include `tenant_id`.
- Every workspace-scoped record must include `tenant_id` and `workspace_id`.
- Actor `tenant_id` must match resource `tenant_id`.
- Actor `workspace_id` must match resource `workspace_id` when the resource is workspace-scoped.
- Production Managed or Enterprise deployments should bind this contract to Postgres with row-level security or equivalent tenant predicates.

## Operational Scope Queries

The current public reference implementation includes scoped helpers for local JSON and SQLite persistence:

- `list_decisions_for_scope`, `list_sessions_for_scope`, and `summarize_sessions_for_scope` on activity stores.
- `list_for_scope` on approval stores.
- `list_for_scope` and `search_for_scope` on evidence metadata stores.
- `list_repositories_for_scope` and `list_policy_rollouts_for_scope` on inventory stores.
- `list_integrations_for_scope` on integration stores.
- Nullable `tenant_id` and `workspace_id` SQLite columns with in-place migration for existing local databases.

Production deployments should carry the same predicates into the managed database layer and run cross-tenant negative tests before production readiness gates pass.

## Postgres/RLS Contract

The public R2.2 contract now defines the production table model without exposing private database endpoints or credentials.

| Source | Postgres table | Scope |
| --- | --- | --- |
| Tenant records | `cavra.tenants` | `tenant_id` |
| Workspace records | `cavra.workspaces` | `tenant_id`, `workspace_id` |
| Evidence metadata | `cavra.evidence_metadata` | `tenant_id`, `workspace_id` |
| Approval history | `cavra.approvals` | `tenant_id`, `workspace_id` |
| Activity sessions | `cavra.activity_sessions` | `tenant_id`, `workspace_id` |
| Activity decisions | `cavra.activity_decisions` | `tenant_id`, `workspace_id` |
| Repository inventory | `cavra.inventory_repositories` | `tenant_id`, `workspace_id` |
| Policy rollouts | `cavra.inventory_policy_rollouts` | `tenant_id`, `workspace_id` |
| Integrations | `cavra.integrations` | `tenant_id`, `workspace_id` |

Private Enterprise runtime code must set:

```sql
SET LOCAL cavra.tenant_id = '<tenant-id>';
SET LOCAL cavra.workspace_id = '<workspace-id>';
```

The SQL contract enables and forces RLS, with predicates bound to `current_setting('cavra.tenant_id', true)` and `current_setting('cavra.workspace_id', true)`. The runtime database role should not own these tables and should not have `BYPASSRLS`.

## Validation

```bash
python3 scripts/validate_tenant_persistence_readiness.py
python3 -m pytest tests/test_postgres_tenancy.py tests/test_tenancy.py tests/test_activity.py tests/test_approvals.py tests/test_evidence.py tests/test_inventory.py tests/test_integrations.py -q
```

Detailed repo document: [Tenant And Workspace Persistence](https://github.com/Huzefaaa2/cavra/blob/main/docs/tenant-workspace-persistence.md).
