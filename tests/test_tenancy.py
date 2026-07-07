from __future__ import annotations

from pathlib import Path

import pytest

from cavra.tenancy import (
    SQLiteTenantWorkspaceStore,
    TenantScope,
    TenantWorkspaceStore,
    assert_tenant_workspace_scope,
    build_tenant_persistence_contract,
    build_tenant_persistence_readiness,
    record_matches_scope,
)


def _tenant(tenant_id: str = "tenant-a") -> dict[str, object]:
    return {
        "tenant_id": tenant_id,
        "display_name": f"Tenant {tenant_id}",
        "status": "active",
        "data_residency": "customer_managed",
        "identity_provider": "Microsoft Entra ID",
        "evidence_refs": [f"evidence://tenant/{tenant_id}"],
    }


def _workspace(tenant_id: str, workspace_id: str) -> dict[str, object]:
    return {
        "tenant_id": tenant_id,
        "workspace_id": workspace_id,
        "display_name": f"{tenant_id}/{workspace_id}",
        "status": "active",
        "environment": "production",
        "default_policy_pack": "cavra-enterprise-baseline",
    }


def _exercise_store(store: TenantWorkspaceStore | SQLiteTenantWorkspaceStore) -> None:
    store.upsert_tenant(_tenant("tenant-a"))
    store.upsert_tenant(_tenant("tenant-b"))
    store.upsert_workspace(_workspace("tenant-a", "workspace-prod"))
    store.upsert_workspace(_workspace("tenant-a", "workspace-dev"))
    store.upsert_workspace(_workspace("tenant-b", "workspace-prod"))

    tenant_a = store.list_workspaces(tenant_id="tenant-a")
    tenant_b = store.list_workspaces(tenant_id="tenant-b")

    assert store.get_tenant("tenant-a")["tenant_id"] == "tenant-a"
    assert store.list_tenants(status="active")["total"] == 2
    assert tenant_a["total"] == 2
    assert {item["tenant_id"] for item in tenant_a["items"]} == {"tenant-a"}
    assert tenant_b["total"] == 1
    assert tenant_b["items"][0]["tenant_id"] == "tenant-b"
    assert store.get_workspace("tenant-a", "workspace-prod")["display_name"] == "tenant-a/workspace-prod"
    assert store.get_workspace("tenant-a", "workspace-missing") is None


def test_json_tenant_workspace_store_isolates_workspace_lists(tmp_path: Path) -> None:
    _exercise_store(TenantWorkspaceStore(tmp_path / "tenants.json"))


def test_sqlite_tenant_workspace_store_isolates_workspace_lists(tmp_path: Path) -> None:
    _exercise_store(SQLiteTenantWorkspaceStore(tmp_path / "tenants.db"))


def test_tenant_scope_helpers_reject_cross_tenant_and_cross_workspace_access() -> None:
    resource = {"tenant_id": "tenant-a", "workspace_id": "workspace-prod"}

    assert_tenant_workspace_scope({"tenant_id": "tenant-a", "workspace_id": "workspace-prod"}, resource)
    assert record_matches_scope(resource, TenantScope("tenant-a", "workspace-prod"))
    assert not record_matches_scope(resource, TenantScope("tenant-b"))

    with pytest.raises(PermissionError):
        assert_tenant_workspace_scope({"tenant_id": "tenant-b", "workspace_id": "workspace-prod"}, resource)
    with pytest.raises(PermissionError):
        assert_tenant_workspace_scope({"tenant_id": "tenant-a", "workspace_id": "workspace-dev"}, resource)
    with pytest.raises(ValueError):
        assert_tenant_workspace_scope({"workspace_id": "workspace-prod"}, resource)


def test_tenant_persistence_contract_and_readiness_shape() -> None:
    contract = build_tenant_persistence_contract()
    readiness = build_tenant_persistence_readiness(
        json_store_supported=True,
        sqlite_store_supported=True,
        postgres_plan_documented=True,
    )

    assert contract["schema_version"] == "cavra.tenant_persistence.contract.v1"
    assert "tenant_id" in contract["required_record_keys"]["tenant"]
    assert "workspace_id" in contract["required_record_keys"]["workspace"]
    assert readiness["ready_for_tenant_persistence_foundation"] is True
    assert readiness["status"] == "ready"


def test_tenant_persistence_closeout_docs_reference_sanitized_rls_packet() -> None:
    closeout = Path("docs/tenant-persistence-r2-closeout.md").read_text(encoding="utf-8")
    packet = Path("examples/postgres/enterprise-postgres-rls-smoke.live.sanitized.example.json")

    assert str(packet) in closeout
    assert "live_rls_smoke_tested" in closeout
    assert "R2.3 Handoff" in closeout


def test_tenant_ids_are_validated(tmp_path: Path) -> None:
    store = TenantWorkspaceStore(tmp_path / "tenants.json")

    with pytest.raises(ValueError):
        store.upsert_tenant({"tenant_id": "x"})
    with pytest.raises(ValueError):
        store.upsert_workspace({"tenant_id": "tenant-a", "workspace_id": "invalid space"})
