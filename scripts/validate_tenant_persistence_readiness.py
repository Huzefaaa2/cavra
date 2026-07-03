#!/usr/bin/env python3
"""Validate R2.2 tenant/workspace persistence foundation coverage."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

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
    ],
    "docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md": [
        "| R2.2 |",
        "Tenant/workspace persistence contract",
        "activity decision/session scope binding",
        "approval queue/history scope binding",
        "evidence metadata scope binding",
        "inventory scope binding",
        "integration scope binding",
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
