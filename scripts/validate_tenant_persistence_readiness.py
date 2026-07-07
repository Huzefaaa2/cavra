#!/usr/bin/env python3
"""Validate R2.2 tenant/workspace persistence foundation coverage."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.postgres_tenancy import build_postgres_rls_contract, build_postgres_rls_readiness
from cavra.tenancy import build_tenant_persistence_contract, build_tenant_persistence_readiness


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TEXT = {
    "src/cavra/tenancy.py": [
        "TENANT_PERSISTENCE_CONTRACT_VERSION",
        "TenantWorkspaceStore",
        "SQLiteTenantWorkspaceStore",
        "assert_tenant_workspace_scope",
        "build_tenant_persistence_readiness",
        "Postgres",
        "row-level security",
    ],
    "src/cavra/postgres_tenancy.py": [
        "POSTGRES_TENANT_RLS_CONTRACT_VERSION",
        "POSTGRES_TENANT_SESSION_CONTRACT_VERSION",
        "build_postgres_rls_contract",
        "build_postgres_session_contract",
        "build_postgres_session_statements",
        "apply_postgres_tenant_scope",
        "build_postgres_rls_smoke_plan",
        "build_postgres_import_rows",
        "ready_for_postgres_rls_contract",
        "current_setting('cavra.tenant_id', true)",
        "set_config('cavra.tenant_id', %s, true)",
        "row-level security",
    ],
    "scripts/validate_postgres_tenant_rls_smoke.py": [
        "CAVRA_ENTERPRISE_POSTGRES_DSN",
        "apply_postgres_tenant_scope",
        "build_postgres_rls_smoke_plan",
        "dsn_value_included",
        "live_rls_smoke_tested",
        "--packet",
        "--require-live",
    ],
    "migrations/postgres/001_tenant_scoped_operational_stores.sql": [
        "ENABLE ROW LEVEL SECURITY",
        "FORCE ROW LEVEL SECURITY",
        "current_setting('cavra.tenant_id', true)",
        "current_setting('cavra.workspace_id', true)",
        "cavra.activity_decisions",
        "cavra.integrations",
    ],
    "src/cavra/activity.py": [
        "tenant_id",
        "workspace_id",
        "list_decisions_for_scope",
        "list_sessions_for_scope",
        "summarize_sessions_for_scope",
        "idx_activity_decisions_tenant_workspace",
        "idx_activity_sessions_tenant_workspace",
    ],
    "src/cavra/approvals.py": [
        "tenant_id",
        "workspace_id",
        "list_for_scope",
        "idx_approvals_tenant_workspace",
    ],
    "src/cavra/evidence.py": [
        "tenant_id",
        "workspace_id",
        "list_for_scope",
        "search_for_scope",
        "idx_evidence_metadata_tenant_workspace",
    ],
    "src/cavra/inventory.py": [
        "tenant_id",
        "workspace_id",
        "list_repositories_for_scope",
        "list_policy_rollouts_for_scope",
        "idx_inventory_repositories_tenant_workspace",
        "idx_inventory_rollouts_tenant_workspace",
    ],
    "src/cavra/integrations.py": [
        "tenant_id",
        "workspace_id",
        "list_integrations_for_scope",
        "idx_integrations_tenant_workspace",
    ],
    "tests/test_tenancy.py": [
        "test_json_tenant_workspace_store_isolates_workspace_lists",
        "test_sqlite_tenant_workspace_store_isolates_workspace_lists",
        "test_tenant_scope_helpers_reject_cross_tenant_and_cross_workspace_access",
    ],
    "tests/test_activity.py": [
        "test_activity_store_filters_by_tenant_workspace_scope",
        "test_sqlite_activity_store_filters_by_tenant_workspace_scope",
    ],
    "tests/test_approvals.py": [
        "test_approval_store_filters_by_tenant_workspace_scope",
        "test_sqlite_approval_store_filters_by_tenant_workspace_scope",
    ],
    "tests/test_evidence.py": [
        "test_evidence_metadata_store_filters_by_tenant_workspace_scope",
        "test_sqlite_evidence_metadata_store_filters_by_tenant_workspace_scope",
    ],
    "tests/test_inventory.py": [
        "test_inventory_store_filters_by_tenant_workspace_scope",
        "test_sqlite_inventory_store_filters_by_tenant_workspace_scope",
    ],
    "tests/test_integrations.py": [
        "test_integration_store_filters_by_tenant_workspace_scope",
        "test_sqlite_integration_store_filters_by_tenant_workspace_scope",
    ],
    "tests/test_postgres_tenancy.py": [
        "test_postgres_rls_contract",
        "test_postgres_session_contract_and_adapter_apply_transaction_local_scope",
        "test_postgres_session_adapter_requires_executor_and_valid_scope",
        "test_postgres_rls_smoke_plan_defines_positive_and_negative_scopes",
        "test_postgres_rls_migration_sql_contains_required_tables_and_policies",
        "test_json_reference_stores_build_postgres_import_rows",
        "test_sqlite_reference_stores_build_postgres_import_rows",
        "test_postgres_import_rows_require_tenant_workspace_scope",
    ],
    "docs/tenant-workspace-persistence.md": [
        "R2.2",
        "tenant_id",
        "workspace_id",
        "JSON",
        "SQLite",
        "ActivityStore",
        "ApprovalStore",
        "EvidenceMetadataStore",
        "InventoryStore",
        "IntegrationStore",
        "Postgres",
        "row-level security",
        "migrations/postgres/001_tenant_scoped_operational_stores.sql",
        "build_postgres_import_rows",
        "apply_postgres_tenant_scope",
        "validate_postgres_tenant_rls_smoke.py",
        "cavra.tenant_id",
        "cavra.workspace_id",
        "R2.2 is public-repository complete",
        "Tenant Persistence R2.2 Closeout",
    ],
    "docs/tenant-persistence-r2-closeout.md": [
        "R2.2 is closed",
        "Sanitized live-style Postgres RLS packet",
        "R2.3 Handoff",
    ],
    "examples/postgres/enterprise-postgres-rls-smoke.live.sanitized.example.json": [
        "cavra.postgres_tenant_rls.smoke.v1",
        "\"live_rls_smoke_tested\": true",
        "\"dsn_value_included\": false",
        "\"positive_count\": 1",
        "\"negative_count\": 0",
        "tenant_b_cannot_read_tenant_a_workspace_a",
    ],
    "docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md": [
        "| R2.2 |",
        "Tenant/workspace persistence contract",
        "activity decision/session scope binding",
        "approval queue/history scope binding",
        "evidence metadata scope binding",
        "inventory scope binding",
        "integration scope binding",
        "Postgres/RLS public contract",
        "JSON/SQLite import row tests",
        "request-scoped Postgres session adapter",
        "public-safe RLS smoke harness",
        "scripts/validate_tenant_persistence_readiness.py",
    ],
    "docs/wiki/Tenant-Workspace-Persistence.md": [
        "TenantWorkspaceStore",
        "SQLiteTenantWorkspaceStore",
        "ActivityStore",
        "ApprovalStore",
        "EvidenceMetadataStore",
        "InventoryStore",
        "IntegrationStore",
        "Postgres",
        "RLS",
        "migrations/postgres/001_tenant_scoped_operational_stores.sql",
        "validate_postgres_tenant_rls_smoke.py",
        "Tenant Persistence R2.2 Closeout",
    ],
}


def validate_required_text() -> list[str]:
    failures: list[str] = []
    for relative_path, fragments in REQUIRED_TEXT.items():
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"missing {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                failures.append(f"{relative_path} missing required text: {fragment}")
    return failures


def validate_contract_shape() -> list[str]:
    failures: list[str] = []
    contract = build_tenant_persistence_contract()
    readiness = build_tenant_persistence_readiness(
        json_store_supported=True,
        sqlite_store_supported=True,
        postgres_plan_documented=True,
    )
    if contract.get("schema_version") != "cavra.tenant_persistence.contract.v1":
        failures.append("tenant persistence contract schema mismatch")
    required_keys = contract.get("required_record_keys", {})
    if "tenant_id" not in required_keys.get("tenant", []):
        failures.append("tenant contract missing tenant_id")
    if "workspace_id" not in required_keys.get("workspace", []):
        failures.append("workspace contract missing workspace_id")
    if readiness.get("schema_version") != "cavra.tenant_persistence.readiness.v1":
        failures.append("tenant persistence readiness schema mismatch")
    if readiness.get("ready_for_tenant_persistence_foundation") is not True:
        failures.append("tenant persistence foundation should be ready")
    postgres_contract = build_postgres_rls_contract()
    postgres_readiness = build_postgres_rls_readiness(
        contract_documented=True,
        migration_sql_present=True,
        import_tests_present=True,
        session_adapter_present=True,
        smoke_harness_present=True,
    )
    if postgres_contract.get("schema_version") != "cavra.postgres_tenant_rls.contract.v1":
        failures.append("Postgres RLS contract schema mismatch")
    table_names = {table.get("table") for table in postgres_contract.get("tables", [])}
    for table_name in {"cavra.activity_decisions", "cavra.integrations", "cavra.evidence_metadata"}:
        if table_name not in table_names:
            failures.append(f"Postgres RLS contract missing table: {table_name}")
    settings = postgres_contract.get("session_settings", {})
    if settings.get("tenant_id") != "cavra.tenant_id" or settings.get("workspace_id") != "cavra.workspace_id":
        failures.append("Postgres RLS session settings mismatch")
    session_contract = postgres_contract.get("session_scope_contract", {})
    if session_contract.get("schema_version") != "cavra.postgres_tenant_session.contract.v1":
        failures.append("Postgres tenant session contract schema mismatch")
    if postgres_readiness.get("schema_version") != "cavra.postgres_tenant_rls.readiness.v1":
        failures.append("Postgres RLS readiness schema mismatch")
    if postgres_readiness.get("ready_for_postgres_rls_contract") is not True:
        failures.append("Postgres RLS contract should be ready")
    return failures


def main() -> int:
    failures = validate_required_text()
    failures.extend(validate_contract_shape())
    if failures:
        print(json.dumps({"status": "failed", "failures": failures}, indent=2))
        return 1
    print("tenant persistence readiness controls validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
