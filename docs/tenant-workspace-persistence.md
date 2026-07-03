# CAVRA Tenant And Workspace Persistence

Last updated: 2026-07-03

This page defines the first R2.2 tenant/workspace persistence contract for CAVRA. It is a public-safe foundation for tenant isolation, workspace scoping, and later production database migration.

## Scope

The public repository now includes:

- `TenantWorkspaceStore`: JSON reference store for local tenant/workspace records.
- `SQLiteTenantWorkspaceStore`: SQLite reference store for local tenant/workspace records.
- `assert_tenant_workspace_scope`: shared guard for actor/resource tenant and workspace comparisons.
- `build_tenant_persistence_contract`: public contract for required tenant/workspace fields and isolation rules.
- `build_tenant_persistence_readiness`: readiness packet for the R2.2 foundation.

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

## Validation

```bash
python3 scripts/validate_tenant_persistence_readiness.py
python3 -m pytest tests/test_tenancy.py -q
```

Expected result:

```text
tenant persistence readiness controls validated
```

## Migration Path

The next R2.2 slices should:

- bind tenant/workspace scope into activity, approvals, evidence metadata, inventory, and integrations;
- define private Postgres DDL and row-level security policies;
- add migration tests from JSON and SQLite reference stores into the production data model;
- use the `tenant_id` and `workspace_id` from the live identity validation packet as isolation inputs;
- run cross-tenant negative tests before any production readiness gate is allowed to pass.
