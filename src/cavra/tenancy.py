from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TENANT_RECORD_SCHEMA_VERSION = "cavra.tenant.v1"
WORKSPACE_RECORD_SCHEMA_VERSION = "cavra.workspace.v1"
TENANT_PERSISTENCE_CONTRACT_VERSION = "cavra.tenant_persistence.contract.v1"
TENANT_PERSISTENCE_READINESS_VERSION = "cavra.tenant_persistence.readiness.v1"
TENANT_STATUSES = {"active", "suspended", "disabled", "archived"}
WORKSPACE_STATUSES = {"active", "paused", "disabled", "archived"}
DATA_RESIDENCY_REGIONS = {"global", "us", "eu", "uk", "in", "apac", "customer_managed"}
TENANT_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_.:-]{3,128}$")


@dataclass(frozen=True)
class TenantScope:
    tenant_id: str
    workspace_id: str | None = None

    def as_filters(self) -> dict[str, str]:
        filters = {"tenant_id": self.tenant_id}
        if self.workspace_id:
            filters["workspace_id"] = self.workspace_id
        return filters


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_tenant_id(value: Any, *, field_name: str = "tenant_id") -> str:
    identifier = str(value or "").strip()
    if not TENANT_IDENTIFIER_PATTERN.fullmatch(identifier):
        raise ValueError(f"{field_name} must be 3-128 characters using letters, numbers, dot, underscore, colon, or dash")
    return identifier


def normalize_workspace_id(value: Any, *, field_name: str = "workspace_id") -> str:
    return normalize_tenant_id(value, field_name=field_name)


def normalize_tenant_record(payload: dict[str, Any]) -> dict[str, Any]:
    tenant_id = normalize_tenant_id(payload.get("tenant_id"))
    status = str(payload.get("status", "active"))
    if status not in TENANT_STATUSES:
        raise ValueError(f"tenant status must be one of: {', '.join(sorted(TENANT_STATUSES))}")
    data_residency = str(payload.get("data_residency", "customer_managed"))
    if data_residency not in DATA_RESIDENCY_REGIONS:
        raise ValueError(f"data_residency must be one of: {', '.join(sorted(DATA_RESIDENCY_REGIONS))}")
    now = utc_now()
    return {
        "schema_version": TENANT_RECORD_SCHEMA_VERSION,
        "tenant_id": tenant_id,
        "display_name": str(payload.get("display_name") or tenant_id),
        "status": status,
        "deployment_model": str(payload.get("deployment_model", "self_hosted_enterprise")),
        "data_residency": data_residency,
        "identity_provider": str(payload.get("identity_provider", "oidc")),
        "created_at": payload.get("created_at") or now,
        "updated_at": now,
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
    }


def normalize_workspace_record(payload: dict[str, Any]) -> dict[str, Any]:
    tenant_id = normalize_tenant_id(payload.get("tenant_id"))
    workspace_id = normalize_workspace_id(payload.get("workspace_id"))
    status = str(payload.get("status", "active"))
    if status not in WORKSPACE_STATUSES:
        raise ValueError(f"workspace status must be one of: {', '.join(sorted(WORKSPACE_STATUSES))}")
    now = utc_now()
    return {
        "schema_version": WORKSPACE_RECORD_SCHEMA_VERSION,
        "tenant_id": tenant_id,
        "workspace_id": workspace_id,
        "display_name": str(payload.get("display_name") or workspace_id),
        "status": status,
        "environment": str(payload.get("environment", "production")),
        "default_policy_pack": str(payload.get("default_policy_pack", "cavra-ai-agent-baseline")),
        "created_at": payload.get("created_at") or now,
        "updated_at": now,
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
    }


def assert_tenant_workspace_scope(actor_context: dict[str, Any], resource: dict[str, Any]) -> None:
    actor_tenant = actor_context.get("tenant_id")
    resource_tenant = resource.get("tenant_id")
    if not actor_tenant or not resource_tenant:
        raise ValueError("tenant_id is required on actor and resource for tenant-scoped access")
    if str(actor_tenant) != str(resource_tenant):
        raise PermissionError("actor tenant_id does not match resource tenant_id")
    actor_workspace = actor_context.get("workspace_id")
    resource_workspace = resource.get("workspace_id")
    if resource_workspace and str(actor_workspace or "") != str(resource_workspace):
        raise PermissionError("actor workspace_id does not match resource workspace_id")


def record_matches_scope(record: dict[str, Any], scope: TenantScope) -> bool:
    if str(record.get("tenant_id") or "") != scope.tenant_id:
        return False
    if scope.workspace_id and str(record.get("workspace_id") or "") != scope.workspace_id:
        return False
    return True


def build_tenant_persistence_contract() -> dict[str, Any]:
    return {
        "schema_version": TENANT_PERSISTENCE_CONTRACT_VERSION,
        "product": "CAVRA",
        "purpose": "R2.2 public-safe tenant/workspace persistence and isolation contract.",
        "required_record_keys": {
            "tenant": ["tenant_id", "status", "data_residency", "identity_provider"],
            "workspace": ["tenant_id", "workspace_id", "status", "environment", "default_policy_pack"],
        },
        "isolation_rules": [
            "Every tenant-scoped record must include tenant_id.",
            "Every workspace-scoped record must include tenant_id and workspace_id.",
            "Actor tenant_id must match resource tenant_id before scoped data is returned or mutated.",
            "Actor workspace_id must match resource workspace_id when a resource has workspace scope.",
            "Community JSON and SQLite stores are local reference implementations; production SaaS should bind this contract to Postgres with row-level security or equivalent tenant predicates.",
        ],
        "reference_stores": ["TenantWorkspaceStore", "SQLiteTenantWorkspaceStore"],
    }


def build_tenant_persistence_readiness(
    *,
    json_store_supported: bool,
    sqlite_store_supported: bool,
    postgres_plan_documented: bool,
) -> dict[str, Any]:
    checks = [
        _check(
            "json_reference_store",
            "pass" if json_store_supported else "blocker",
            "JSON tenant/workspace reference store is implemented."
            if json_store_supported
            else "JSON tenant/workspace reference store is missing.",
        ),
        _check(
            "sqlite_reference_store",
            "pass" if sqlite_store_supported else "blocker",
            "SQLite tenant/workspace reference store is implemented."
            if sqlite_store_supported
            else "SQLite tenant/workspace reference store is missing.",
        ),
        _check(
            "postgres_migration_plan",
            "pass" if postgres_plan_documented else "warn",
            "Postgres migration path is documented for private Enterprise implementation."
            if postgres_plan_documented
            else "Postgres migration path is not documented yet.",
        ),
    ]
    blockers = [check for check in checks if check["status"] == "blocker"]
    warnings = [check for check in checks if check["status"] == "warn"]
    return {
        "schema_version": TENANT_PERSISTENCE_READINESS_VERSION,
        "product": "CAVRA",
        "ready_for_tenant_persistence_foundation": not blockers,
        "status": "blocked" if blockers else "ready_with_warnings" if warnings else "ready",
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
        "next_controls": [
            "Bind tenant/workspace scope to activity, approval, evidence, inventory, and integration stores.",
            "Add private Postgres row-level security migrations and isolation smoke tests.",
            "Use live identity packet tenant_id and workspace_id as R2.2 validation inputs.",
        ],
    }


class TenantWorkspaceStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def upsert_tenant(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_tenant_record(payload)
        data = self._load()
        data["tenants"] = [item for item in data["tenants"] if item.get("tenant_id") != record["tenant_id"]]
        data["tenants"].append(record)
        self._save(data)
        return record

    def get_tenant(self, tenant_id: str) -> dict[str, Any] | None:
        tenant = normalize_tenant_id(tenant_id)
        return next((item for item in self._load()["tenants"] if item.get("tenant_id") == tenant), None)

    def list_tenants(self, *, status: str | None = None) -> dict[str, Any]:
        items = self._load()["tenants"]
        if status:
            items = [item for item in items if item.get("status") == status]
        return {"items": sorted(items, key=lambda item: item.get("tenant_id", "")), "total": len(items)}

    def upsert_workspace(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_workspace_record(payload)
        data = self._load()
        data["workspaces"] = [
            item
            for item in data["workspaces"]
            if not (item.get("tenant_id") == record["tenant_id"] and item.get("workspace_id") == record["workspace_id"])
        ]
        data["workspaces"].append(record)
        self._save(data)
        return record

    def get_workspace(self, tenant_id: str, workspace_id: str) -> dict[str, Any] | None:
        tenant = normalize_tenant_id(tenant_id)
        workspace = normalize_workspace_id(workspace_id)
        return next(
            (
                item
                for item in self._load()["workspaces"]
                if item.get("tenant_id") == tenant and item.get("workspace_id") == workspace
            ),
            None,
        )

    def list_workspaces(self, *, tenant_id: str, status: str | None = None) -> dict[str, Any]:
        tenant = normalize_tenant_id(tenant_id)
        items = [item for item in self._load()["workspaces"] if item.get("tenant_id") == tenant]
        if status:
            items = [item for item in items if item.get("status") == status]
        return {"items": sorted(items, key=lambda item: item.get("workspace_id", "")), "total": len(items)}

    def _load(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists():
            return {"tenants": [], "workspaces": []}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return {
            "tenants": list(payload.get("tenants", [])),
            "workspaces": list(payload.get("workspaces", [])),
        }

    def _save(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class SQLiteTenantWorkspaceStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tenants (
                  tenant_id TEXT PRIMARY KEY,
                  status TEXT NOT NULL,
                  data_residency TEXT NOT NULL,
                  identity_provider TEXT NOT NULL,
                  updated_at TEXT NOT NULL,
                  payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_tenants_status ON tenants (status)")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS workspaces (
                  tenant_id TEXT NOT NULL,
                  workspace_id TEXT NOT NULL,
                  status TEXT NOT NULL,
                  environment TEXT NOT NULL,
                  default_policy_pack TEXT NOT NULL,
                  updated_at TEXT NOT NULL,
                  payload TEXT NOT NULL,
                  PRIMARY KEY (tenant_id, workspace_id)
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_workspaces_tenant ON workspaces (tenant_id)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_workspaces_status ON workspaces (status)")

    def upsert_tenant(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_tenant_record(payload)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO tenants (tenant_id, status, data_residency, identity_provider, updated_at, payload)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(tenant_id) DO UPDATE SET
                  status=excluded.status,
                  data_residency=excluded.data_residency,
                  identity_provider=excluded.identity_provider,
                  updated_at=excluded.updated_at,
                  payload=excluded.payload
                """,
                (
                    record["tenant_id"],
                    record["status"],
                    record["data_residency"],
                    record["identity_provider"],
                    record["updated_at"],
                    json.dumps(record, sort_keys=True),
                ),
            )
        return record

    def get_tenant(self, tenant_id: str) -> dict[str, Any] | None:
        tenant = normalize_tenant_id(tenant_id)
        with self._connect() as connection:
            row = connection.execute("SELECT payload FROM tenants WHERE tenant_id = ?", (tenant,)).fetchone()
        return json.loads(row["payload"]) if row else None

    def list_tenants(self, *, status: str | None = None) -> dict[str, Any]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT payload FROM tenants WHERE (? IS NULL OR status = ?) ORDER BY tenant_id ASC",
                (status, status),
            ).fetchall()
        items = [json.loads(row["payload"]) for row in rows]
        return {"items": items, "total": len(items)}

    def upsert_workspace(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_workspace_record(payload)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO workspaces (
                  tenant_id, workspace_id, status, environment, default_policy_pack, updated_at, payload
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(tenant_id, workspace_id) DO UPDATE SET
                  status=excluded.status,
                  environment=excluded.environment,
                  default_policy_pack=excluded.default_policy_pack,
                  updated_at=excluded.updated_at,
                  payload=excluded.payload
                """,
                (
                    record["tenant_id"],
                    record["workspace_id"],
                    record["status"],
                    record["environment"],
                    record["default_policy_pack"],
                    record["updated_at"],
                    json.dumps(record, sort_keys=True),
                ),
            )
        return record

    def get_workspace(self, tenant_id: str, workspace_id: str) -> dict[str, Any] | None:
        tenant = normalize_tenant_id(tenant_id)
        workspace = normalize_workspace_id(workspace_id)
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM workspaces WHERE tenant_id = ? AND workspace_id = ?",
                (tenant, workspace),
            ).fetchone()
        return json.loads(row["payload"]) if row else None

    def list_workspaces(self, *, tenant_id: str, status: str | None = None) -> dict[str, Any]:
        tenant = normalize_tenant_id(tenant_id)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload FROM workspaces
                WHERE tenant_id = ? AND (? IS NULL OR status = ?)
                ORDER BY workspace_id ASC
                """,
                (tenant, status, status),
            ).fetchall()
        items = [json.loads(row["payload"]) for row in rows]
        return {"items": items, "total": len(items)}


def _check(check_id: str, status: str, message: str) -> dict[str, str]:
    return {"check_id": check_id, "status": status, "message": message}


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value]
    return [str(value)]
