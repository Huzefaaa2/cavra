# Tenant Workspace Persistence

CAVRA R2.2 starts with a public-safe tenant/workspace persistence contract and reference stores.

## Implemented Foundation

| Component | Purpose |
| --- | --- |
| `TenantWorkspaceStore` | JSON reference store for local tenant and workspace records. |
| `SQLiteTenantWorkspaceStore` | SQLite reference store for local tenant and workspace records. |
| `ActivityStore` / `SQLiteActivityStore` | Runtime decision and session history can carry and filter by `tenant_id` and `workspace_id`. |
| `ApprovalStore` / `SQLiteApprovalStore` | Approval queues and approval history can carry and filter by `tenant_id` and `workspace_id`. |
| `assert_tenant_workspace_scope` | Rejects actor/resource tenant or workspace mismatches. |
| `build_tenant_persistence_contract` | Publishes required tenant/workspace fields and isolation rules. |
| `build_tenant_persistence_readiness` | Produces the R2.2 foundation readiness result. |

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
- Nullable `tenant_id` and `workspace_id` SQLite columns with in-place migration for existing local databases.

Production deployments should carry the same predicates into the managed database layer and run cross-tenant negative tests before production readiness gates pass.

## Validation

```bash
python3 scripts/validate_tenant_persistence_readiness.py
python3 -m pytest tests/test_tenancy.py tests/test_activity.py tests/test_approvals.py -q
```

Detailed repo document: [Tenant And Workspace Persistence](https://github.com/Huzefaaa2/cavra/blob/main/docs/tenant-workspace-persistence.md).
