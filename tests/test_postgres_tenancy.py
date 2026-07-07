from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from cavra.activity import ActivityStore, SQLiteActivityStore
from cavra.approvals import ApprovalStore, SQLiteApprovalStore
from cavra.evidence import EvidenceMetadataStore, SQLiteEvidenceMetadataStore
from cavra.integrations import IntegrationStore, SQLiteIntegrationStore
from cavra.inventory import InventoryStore, SQLiteInventoryStore
from cavra.postgres_tenancy import (
    PostgresTenantSessionScope,
    TENANT_SCOPED_TABLES,
    apply_postgres_tenant_scope,
    build_postgres_import_rows,
    build_postgres_rls_contract,
    build_postgres_rls_readiness,
    build_postgres_rls_smoke_plan,
    build_postgres_session_contract,
    build_postgres_session_statements,
    postgres_table_for_source,
)
from cavra.tenancy import SQLiteTenantWorkspaceStore, TenantWorkspaceStore

LIVE_RLS_SANITIZED = Path("examples/postgres/enterprise-postgres-rls-smoke.live.sanitized.example.json")


def test_postgres_rls_contract() -> None:
    contract = build_postgres_rls_contract()

    assert contract["schema_version"] == "cavra.postgres_tenant_rls.contract.v1"
    assert contract["session_settings"]["tenant_id"] == "cavra.tenant_id"
    assert contract["session_settings"]["workspace_id"] == "cavra.workspace_id"
    assert postgres_table_for_source("activity_decision") == "cavra.activity_decisions"
    assert {table["source"] for table in contract["tables"]} == set(TENANT_SCOPED_TABLES)
    assert any("row-level security" in control for control in contract["required_controls"])

    readiness = build_postgres_rls_readiness(
        contract_documented=True,
        migration_sql_present=True,
        import_tests_present=True,
        session_adapter_present=True,
        smoke_harness_present=True,
    )

    assert readiness["ready_for_postgres_rls_contract"] is True
    assert readiness["status"] == "ready_with_warnings"
    assert readiness["warning_count"] == 1


def test_postgres_session_contract_and_adapter_apply_transaction_local_scope() -> None:
    contract = build_postgres_session_contract()
    scope = PostgresTenantSessionScope.from_values(tenant_id="tenant-a", workspace_id="prod")
    connection = _FakePostgresConnection()

    result = apply_postgres_tenant_scope(connection, tenant_id=scope.tenant_id, workspace_id=scope.workspace_id)
    statements = build_postgres_session_statements(scope)

    assert contract["schema_version"] == "cavra.postgres_tenant_session.contract.v1"
    assert "set_config('cavra.tenant_id', %s, true)" in contract["scope_binding_sql"][0]
    assert [call[0] for call in connection.calls] == [statement[0] for statement in statements]
    assert [call[1] for call in connection.calls] == [("tenant-a",), ("prod",)]
    assert result["applied"] is True
    assert result["session_settings"] == {"tenant_id": "tenant-a", "workspace_id": "prod"}


def test_postgres_session_adapter_requires_executor_and_valid_scope() -> None:
    with pytest.raises(TypeError, match="execute"):
        apply_postgres_tenant_scope(object(), tenant_id="tenant-a", workspace_id="prod")

    with pytest.raises(ValueError, match="tenant_id"):
        apply_postgres_tenant_scope(_FakePostgresConnection(), tenant_id="bad tenant", workspace_id="prod")


def test_postgres_rls_smoke_plan_defines_positive_and_negative_scopes() -> None:
    plan = build_postgres_rls_smoke_plan(
        tenant_a="tenant-a",
        workspace_a="prod",
        tenant_b="tenant-b",
        workspace_b="prod",
    )

    assert plan["schema_version"] == "cavra.postgres_tenant_rls.smoke.v1"
    assert plan["positive_scope"] == {"tenant_id": "tenant-a", "workspace_id": "prod"}
    assert plan["negative_scope"] == {"tenant_id": "tenant-b", "workspace_id": "prod"}
    assert "tenant_b_cannot_read_tenant_a_workspace_a" in plan["required_negative_assertions"]


def test_postgres_rls_sanitized_live_packet_validates(tmp_path: Path) -> None:
    result_path = tmp_path / "postgres-rls-smoke-live-sanitized-result.json"

    subprocess.run(
        [
            "python3",
            "scripts/validate_postgres_tenant_rls_smoke.py",
            "--packet",
            str(LIVE_RLS_SANITIZED),
            "--require-live",
            "--output",
            str(result_path),
        ],
        check=True,
    )

    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert result["packet_validated"] is True
    assert result["live_rls_smoke_tested"] is True
    assert result["dsn_value_included"] is False
    assert result["positive_count"] == 1
    assert result["negative_count"] == 0
    assert result["validation_failures"] == []


def test_postgres_rls_migration_sql_contains_required_tables_and_policies() -> None:
    sql = Path("migrations/postgres/001_tenant_scoped_operational_stores.sql").read_text(encoding="utf-8")

    assert "ENABLE ROW LEVEL SECURITY" in sql
    assert "FORCE ROW LEVEL SECURITY" in sql
    assert "current_setting('cavra.tenant_id', true)" in sql
    assert "current_setting('cavra.workspace_id', true)" in sql
    for config in TENANT_SCOPED_TABLES.values():
        assert config["table"] in sql


def test_json_reference_stores_build_postgres_import_rows(tmp_path: Path) -> None:
    rows = _build_import_rows(
        tenant_store=TenantWorkspaceStore(tmp_path / "tenants.json"),
        activity_store=ActivityStore(tmp_path / "activity.json"),
        approval_store=ApprovalStore(tmp_path / "approvals.json"),
        evidence_store=EvidenceMetadataStore(tmp_path / "evidence.json"),
        inventory_store=InventoryStore(tmp_path / "inventory.json"),
        integration_store=IntegrationStore(tmp_path / "integrations.json"),
    )

    assert {row["table"] for row in rows} == {
        "cavra.tenants",
        "cavra.workspaces",
        "cavra.activity_decisions",
        "cavra.activity_sessions",
        "cavra.approvals",
        "cavra.evidence_metadata",
        "cavra.inventory_repositories",
        "cavra.inventory_policy_rollouts",
        "cavra.integrations",
    }
    assert {row["tenant_id"] for row in rows} == {"tenant-a"}
    assert {row["workspace_id"] for row in rows if row["source"] != "tenant"} == {"prod"}


def test_sqlite_reference_stores_build_postgres_import_rows(tmp_path: Path) -> None:
    rows = _build_import_rows(
        tenant_store=SQLiteTenantWorkspaceStore(tmp_path / "tenants.db"),
        activity_store=SQLiteActivityStore(tmp_path / "activity.db"),
        approval_store=SQLiteApprovalStore(tmp_path / "approvals.db"),
        evidence_store=SQLiteEvidenceMetadataStore(tmp_path / "evidence.db"),
        inventory_store=SQLiteInventoryStore(tmp_path / "inventory.db"),
        integration_store=SQLiteIntegrationStore(tmp_path / "integrations.db"),
    )

    assert len(rows) == 9
    assert next(row for row in rows if row["source"] == "activity_decision")["record_id"] == "decision-1"
    assert next(row for row in rows if row["source"] == "approval")["record_id"] == "approval-1"
    assert next(row for row in rows if row["source"] == "integration")["record_id"] == "github-enterprise"


def test_postgres_import_rows_require_tenant_workspace_scope() -> None:
    with pytest.raises(ValueError, match="tenant_id"):
        build_postgres_import_rows("activity_decision", [{"decision_id": "decision-1", "workspace_id": "prod"}])

    with pytest.raises(ValueError, match="workspace_id"):
        build_postgres_import_rows("activity_decision", [{"decision_id": "decision-1", "tenant_id": "tenant-a"}])

    with pytest.raises(ValueError, match="decision_id"):
        build_postgres_import_rows("activity_decision", [{"tenant_id": "tenant-a", "workspace_id": "prod"}])

    with pytest.raises(ValueError, match="unsupported Postgres import source"):
        build_postgres_import_rows("unknown", [{"tenant_id": "tenant-a", "workspace_id": "prod"}])


def _build_import_rows(
    *,
    tenant_store,
    activity_store,
    approval_store,
    evidence_store,
    inventory_store,
    integration_store,
) -> list[dict[str, object]]:
    tenant = tenant_store.upsert_tenant(
        {
            "tenant_id": "tenant-a",
            "display_name": "Tenant A",
            "status": "active",
            "data_residency": "us",
            "identity_provider": "entra-id",
        }
    )
    workspace = tenant_store.upsert_workspace(
        {
            "tenant_id": "tenant-a",
            "workspace_id": "prod",
            "display_name": "Production",
            "status": "active",
            "environment": "production",
            "default_policy_pack": "cavra-ai-agent-baseline",
        }
    )
    activity_decision = activity_store.upsert_decision(
        {
            "decision_id": "decision-1",
            "session_id": "session-1",
            "tenant_id": "tenant-a",
            "workspace_id": "prod",
            "agent_id": "codex-agent",
            "actor": "codex-agent",
            "repository": "payments/api",
            "action_type": "execute_command",
            "target": "pytest",
            "requested_operation": "pytest",
            "policy_pack": "cavra-ai-agent-baseline",
            "rule_id": "commands.allow",
            "decision": "allow",
            "severity": "low",
            "timestamp": "2026-05-18T00:00:00+00:00",
        }
    )
    activity_session = activity_store.list_sessions(tenant_id="tenant-a", workspace_id="prod")["items"][0]
    approval = approval_store.upsert(
        {
            "approval_id": "approval-1",
            "decision_id": "decision-1",
            "session_id": "session-1",
            "tenant_id": "tenant-a",
            "workspace_id": "prod",
            "state": "pending",
            "approver_group": "Platform Security",
            "requested_by": "codex-agent",
            "requested_at": "2026-05-18T00:00:00+00:00",
            "expires_at": "2026-05-19T00:00:00+00:00",
            "history": [],
        }
    )
    evidence = evidence_store.upsert(
        {
            "session_id": "session-1",
            "tenant_id": "tenant-a",
            "workspace_id": "prod",
            "created_at": "2026-05-18T00:00:00+00:00",
            "signer": "security",
            "decision_count": 1,
            "blocked_count": 0,
            "approval_required_count": 0,
        }
    )
    repository = inventory_store.upsert_repository(
        {
            "repository": "payments/api",
            "repository_id": "payments/api",
            "tenant_id": "tenant-a",
            "workspace_id": "prod",
            "provider": "github",
            "owner": "Payments Platform",
            "business_unit": "payments",
            "environment": "production",
            "policy_pack": "cavra-ai-agent-baseline",
            "risk_tier": "high",
            "protected_branches": ["main"],
            "required_checks": ["cavra"],
        }
    )
    rollout = inventory_store.upsert_policy_rollout(
        {
            "rollout_id": "rollout-1",
            "repository": "payments/api",
            "tenant_id": "tenant-a",
            "workspace_id": "prod",
            "policy_pack": "cavra-ai-agent-baseline",
            "policy_version": "2026.05",
            "mode": "strict",
            "state": "active",
            "owner": "Platform Security",
            "coverage_percent": 100,
        }
    )
    integration = integration_store.upsert_integration(
        {
            "integration_id": "github-enterprise",
            "tenant_id": "tenant-a",
            "workspace_id": "prod",
            "provider": "github",
            "name": "GitHub Enterprise",
            "category": "source_control",
            "status": "active",
            "health_status": "healthy",
            "owner": "Developer Platform",
            "environment": "production",
            "auth_mode": "github_app",
            "capabilities": ["pull_request"],
            "repositories": ["payments/api"],
        }
    )

    rows: list[dict[str, object]] = []
    rows.extend(build_postgres_import_rows("tenant", [tenant]))
    rows.extend(build_postgres_import_rows("workspace", [workspace]))
    rows.extend(build_postgres_import_rows("activity_decision", [activity_decision]))
    rows.extend(build_postgres_import_rows("activity_session", [activity_session]))
    rows.extend(build_postgres_import_rows("approval", [approval]))
    rows.extend(build_postgres_import_rows("evidence_metadata", [evidence]))
    rows.extend(build_postgres_import_rows("inventory_repository", [repository]))
    rows.extend(build_postgres_import_rows("inventory_policy_rollout", [rollout]))
    rows.extend(build_postgres_import_rows("integration", [integration]))
    return rows


class _FakePostgresConnection:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[str]]] = []

    def execute(self, sql: str, params: tuple[str]) -> None:
        self.calls.append((sql, params))
