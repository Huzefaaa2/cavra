from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from cavra.tenancy import normalize_tenant_id, normalize_workspace_id


POSTGRES_TENANT_RLS_CONTRACT_VERSION = "cavra.postgres_tenant_rls.contract.v1"
POSTGRES_TENANT_RLS_READINESS_VERSION = "cavra.postgres_tenant_rls.readiness.v1"
POSTGRES_TENANT_SESSION_CONTRACT_VERSION = "cavra.postgres_tenant_session.contract.v1"
POSTGRES_TENANT_RLS_SMOKE_VERSION = "cavra.postgres_tenant_rls.smoke.v1"

POSTGRES_TENANT_SESSION_SETTING = "cavra.tenant_id"
POSTGRES_WORKSPACE_SESSION_SETTING = "cavra.workspace_id"


TENANT_SCOPED_TABLES: dict[str, dict[str, Any]] = {
    "tenant": {
        "table": "cavra.tenants",
        "record_id_field": "tenant_id",
        "requires_workspace": False,
        "scope": "tenant",
    },
    "workspace": {
        "table": "cavra.workspaces",
        "record_id_field": "workspace_id",
        "requires_workspace": True,
        "scope": "workspace",
    },
    "evidence_metadata": {
        "table": "cavra.evidence_metadata",
        "record_id_field": "session_id",
        "requires_workspace": True,
        "scope": "workspace",
    },
    "approval": {
        "table": "cavra.approvals",
        "record_id_field": "approval_id",
        "requires_workspace": True,
        "scope": "workspace",
    },
    "activity_session": {
        "table": "cavra.activity_sessions",
        "record_id_field": "session_id",
        "requires_workspace": True,
        "scope": "workspace",
    },
    "activity_decision": {
        "table": "cavra.activity_decisions",
        "record_id_field": "decision_id",
        "requires_workspace": True,
        "scope": "workspace",
    },
    "inventory_repository": {
        "table": "cavra.inventory_repositories",
        "record_id_field": "repository_id",
        "fallback_record_id_field": "repository",
        "requires_workspace": True,
        "scope": "workspace",
    },
    "inventory_policy_rollout": {
        "table": "cavra.inventory_policy_rollouts",
        "record_id_field": "rollout_id",
        "requires_workspace": True,
        "scope": "workspace",
    },
    "integration": {
        "table": "cavra.integrations",
        "record_id_field": "integration_id",
        "requires_workspace": True,
        "scope": "workspace",
    },
}


@dataclass(frozen=True)
class PostgresTenantSessionScope:
    tenant_id: str
    workspace_id: str

    @classmethod
    def from_values(cls, *, tenant_id: Any, workspace_id: Any) -> "PostgresTenantSessionScope":
        return cls(
            tenant_id=normalize_tenant_id(tenant_id),
            workspace_id=normalize_workspace_id(workspace_id),
        )

    def as_parameters(self) -> dict[str, str]:
        return {"tenant_id": self.tenant_id, "workspace_id": self.workspace_id}


def build_postgres_rls_contract() -> dict[str, Any]:
    """Return the public-safe Postgres row-level security contract.

    This is a deployable contract artifact, not a live database connection. Private
    Managed or Enterprise deployments bind the same table names, session settings,
    and import row requirements to their managed Postgres service.
    """

    return {
        "schema_version": POSTGRES_TENANT_RLS_CONTRACT_VERSION,
        "product": "CAVRA",
        "purpose": "R2.2 Postgres row-level security and JSON/SQLite migration contract.",
        "session_settings": {
            "tenant_id": POSTGRES_TENANT_SESSION_SETTING,
            "workspace_id": POSTGRES_WORKSPACE_SESSION_SETTING,
        },
        "source_stores": [
            "TenantWorkspaceStore",
            "SQLiteTenantWorkspaceStore",
            "ActivityStore",
            "SQLiteActivityStore",
            "ApprovalStore",
            "SQLiteApprovalStore",
            "EvidenceMetadataStore",
            "SQLiteEvidenceMetadataStore",
            "InventoryStore",
            "SQLiteInventoryStore",
            "IntegrationStore",
            "SQLiteIntegrationStore",
        ],
        "tables": [
            {
                "source": source,
                "table": config["table"],
                "record_id_field": config["record_id_field"],
                "scope": config["scope"],
                "required_columns": _required_columns(config),
                "rls_predicate": _rls_predicate(config),
            }
            for source, config in TENANT_SCOPED_TABLES.items()
        ],
        "required_controls": [
            "Application roles must set cavra.tenant_id before reading or writing tenant-scoped rows.",
            "Application roles must set cavra.workspace_id before reading or writing workspace-scoped rows.",
            "Every table in this contract must enable and force row-level security.",
            "Runtime application roles must not own tenant-scoped tables and must not have BYPASSRLS.",
            "Migration import rows must include tenant_id and, for workspace-scoped sources, workspace_id.",
            "Cross-tenant and cross-workspace negative tests must fail before production readiness can pass.",
        ],
        "session_scope_contract": build_postgres_session_contract(),
        "migration_sql": "migrations/postgres/001_tenant_scoped_operational_stores.sql",
    }


def build_postgres_session_contract() -> dict[str, Any]:
    return {
        "schema_version": POSTGRES_TENANT_SESSION_CONTRACT_VERSION,
        "product": "CAVRA",
        "purpose": "Request-scoped Postgres tenant/workspace session binding for RLS enforcement.",
        "session_settings": {
            "tenant_id": POSTGRES_TENANT_SESSION_SETTING,
            "workspace_id": POSTGRES_WORKSPACE_SESSION_SETTING,
        },
        "scope_binding_sql": [
            "SELECT set_config('cavra.tenant_id', %s, true)",
            "SELECT set_config('cavra.workspace_id', %s, true)",
        ],
        "runtime_requirements": [
            "Bind scope inside the request transaction before touching tenant-scoped tables.",
            "Use set_config(..., true) so scope is transaction-local and cannot leak across pooled connections.",
            "Reject requests without both tenant_id and workspace_id before opening tenant-scoped queries.",
            "Run cross-tenant and cross-workspace negative reads using the same runtime role used by the application.",
        ],
    }


def build_postgres_rls_readiness(
    *,
    contract_documented: bool,
    migration_sql_present: bool,
    import_tests_present: bool,
    session_adapter_present: bool = False,
    smoke_harness_present: bool = False,
    live_rls_smoke_tested: bool = False,
) -> dict[str, Any]:
    checks = [
        _check(
            "contract_documented",
            "pass" if contract_documented else "blocker",
            "Postgres/RLS tenant contract is documented."
            if contract_documented
            else "Postgres/RLS tenant contract is missing.",
        ),
        _check(
            "migration_sql_present",
            "pass" if migration_sql_present else "blocker",
            "Postgres tenant-scoped migration SQL is present."
            if migration_sql_present
            else "Postgres tenant-scoped migration SQL is missing.",
        ),
        _check(
            "import_tests_present",
            "pass" if import_tests_present else "blocker",
            "JSON/SQLite import row tests are present."
            if import_tests_present
            else "JSON/SQLite import row tests are missing.",
        ),
        _check(
            "session_adapter_present",
            "pass" if session_adapter_present else "warn",
            "Request-scoped Postgres session adapter is present."
            if session_adapter_present
            else "Request-scoped Postgres session adapter is not present yet.",
        ),
        _check(
            "smoke_harness_present",
            "pass" if smoke_harness_present else "warn",
            "Public-safe live RLS smoke harness is present."
            if smoke_harness_present
            else "Public-safe live RLS smoke harness is not present yet.",
        ),
        _check(
            "live_rls_smoke_tested",
            "pass" if live_rls_smoke_tested else "warn",
            "Live private Postgres RLS smoke evidence is attached."
            if live_rls_smoke_tested
            else "Live private Postgres RLS smoke evidence still belongs to the Enterprise deployment gate.",
        ),
    ]
    blockers = [check for check in checks if check["status"] == "blocker"]
    warnings = [check for check in checks if check["status"] == "warn"]
    return {
        "schema_version": POSTGRES_TENANT_RLS_READINESS_VERSION,
        "product": "CAVRA",
        "ready_for_postgres_rls_contract": not blockers,
        "status": "blocked" if blockers else "ready_with_warnings" if warnings else "ready",
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
        "next_controls": [
            "Run the public-safe smoke harness with private Enterprise Postgres credentials.",
            "Run live cross-tenant and cross-workspace negative smoke tests against the private production database.",
            "Attach live RLS smoke evidence to the AISPM production readiness gate.",
        ],
    }


def build_postgres_session_statements(scope: PostgresTenantSessionScope) -> list[tuple[str, tuple[str]]]:
    return [
        ("SELECT set_config('cavra.tenant_id', %s, true)", (scope.tenant_id,)),
        ("SELECT set_config('cavra.workspace_id', %s, true)", (scope.workspace_id,)),
    ]


def apply_postgres_tenant_scope(connection: Any, *, tenant_id: Any, workspace_id: Any) -> dict[str, Any]:
    """Apply transaction-local tenant/workspace settings to a DB-API-like connection.

    The helper intentionally uses duck typing so the public package does not require
    a Postgres driver. Private Enterprise runtimes can pass a psycopg connection or
    cursor; tests can pass a fake executor.
    """

    scope = PostgresTenantSessionScope.from_values(tenant_id=tenant_id, workspace_id=workspace_id)
    statements = build_postgres_session_statements(scope)
    executor = getattr(connection, "execute", None)
    if executor is None:
        raise TypeError("connection must provide an execute(sql, params) method")
    for sql, params in statements:
        executor(sql, params)
    return {
        "schema_version": POSTGRES_TENANT_SESSION_CONTRACT_VERSION,
        "applied": True,
        "session_settings": scope.as_parameters(),
        "statement_count": len(statements),
    }


def build_postgres_rls_smoke_plan(*, tenant_a: str, workspace_a: str, tenant_b: str, workspace_b: str) -> dict[str, Any]:
    scope_a = PostgresTenantSessionScope.from_values(tenant_id=tenant_a, workspace_id=workspace_a)
    scope_b = PostgresTenantSessionScope.from_values(tenant_id=tenant_b, workspace_id=workspace_b)
    return {
        "schema_version": POSTGRES_TENANT_RLS_SMOKE_VERSION,
        "product": "CAVRA",
        "purpose": "Live private Postgres RLS positive and negative smoke validation plan.",
        "positive_scope": scope_a.as_parameters(),
        "negative_scope": scope_b.as_parameters(),
        "steps": [
            "Apply the Postgres migration contract before running smoke checks.",
            "Open a transaction as the application runtime role.",
            "Apply tenant A/workspace A using set_config(..., true).",
            "Write a tenant A/workspace A smoke row and verify it is readable.",
            "Switch to tenant B/workspace B in a new transaction using the same runtime role.",
            "Verify tenant B/workspace B cannot read tenant A/workspace A smoke rows.",
            "Record the sanitized packet as AISPM production readiness evidence.",
        ],
        "required_negative_assertions": [
            "tenant_b_cannot_read_tenant_a_workspace_a",
            "workspace_b_cannot_read_workspace_a",
        ],
    }


def postgres_table_for_source(source: str) -> str:
    return _source_config(source)["table"]


def build_postgres_import_rows(source: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for record in records:
        rows.append(validate_postgres_import_row(source, record))
    return rows


def validate_postgres_import_row(source: str, record: dict[str, Any]) -> dict[str, Any]:
    config = _source_config(source)
    tenant_id = normalize_tenant_id(record.get("tenant_id"))
    workspace_id = None
    if config["requires_workspace"]:
        workspace_id = normalize_workspace_id(record.get("workspace_id"))
    elif record.get("workspace_id"):
        workspace_id = normalize_workspace_id(record.get("workspace_id"))

    record_id_field = config["record_id_field"]
    record_id = record.get(record_id_field)
    if not record_id and config.get("fallback_record_id_field"):
        record_id = record.get(config["fallback_record_id_field"])
    if not record_id:
        raise ValueError(f"{source} import row must include {record_id_field}")

    return {
        "source": source,
        "table": config["table"],
        "record_id": str(record_id),
        "tenant_id": tenant_id,
        "workspace_id": workspace_id,
        "payload": deepcopy(record),
    }


def _source_config(source: str) -> dict[str, Any]:
    try:
        return TENANT_SCOPED_TABLES[source]
    except KeyError as exc:
        raise ValueError(f"unsupported Postgres import source: {source}") from exc


def _required_columns(config: dict[str, Any]) -> list[str]:
    columns = ["tenant_id", config["record_id_field"], "payload", "created_at", "updated_at"]
    if config["requires_workspace"]:
        columns.insert(1, "workspace_id")
    return columns


def _rls_predicate(config: dict[str, Any]) -> str:
    tenant = "tenant_id = current_setting('cavra.tenant_id', true)"
    if not config["requires_workspace"]:
        return tenant
    return f"{tenant} AND workspace_id = current_setting('cavra.workspace_id', true)"


def _check(name: str, status: str, message: str) -> dict[str, str]:
    return {"name": name, "status": status, "message": message}
