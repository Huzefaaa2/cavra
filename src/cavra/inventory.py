from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPOSITORY_STATUSES = {"active", "archived", "disabled"}
POLICY_ROLLOUT_STATES = {"planned", "active", "paused", "retired"}
POLICY_MODES = {"audit_only", "enforce", "strict", "break_glass"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_repository_record(payload: dict[str, Any]) -> dict[str, Any]:
    name = payload.get("repository") or payload.get("name") or payload.get("repository_id")
    if not name:
        raise ValueError("repository record must include repository or name")
    status = str(payload.get("status", "active"))
    if status not in REPOSITORY_STATUSES:
        raise ValueError(f"repository status must be one of: {', '.join(sorted(REPOSITORY_STATUSES))}")
    now = utc_now()
    return {
        "schema_version": "cavra.repository.v1",
        "repository_id": str(payload.get("repository_id") or name),
        "repository": str(name),
        "provider": str(payload.get("provider", "github")),
        "default_branch": str(payload.get("default_branch", "main")),
        "owner": str(payload.get("owner", "unassigned")),
        "business_unit": payload.get("business_unit", "engineering"),
        "environment": payload.get("environment", "development"),
        "policy_pack": str(payload.get("policy_pack", "cavra-ai-agent-baseline")),
        "risk_tier": str(payload.get("risk_tier", "medium")),
        "status": status,
        "protected_branches": _string_list(payload.get("protected_branches", ["main"])),
        "required_checks": _string_list(payload.get("required_checks", [])),
        "created_at": payload.get("created_at") or now,
        "updated_at": now,
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
    }


def normalize_policy_rollout_record(payload: dict[str, Any]) -> dict[str, Any]:
    repository = payload.get("repository") or payload.get("repository_id")
    policy_pack = payload.get("policy_pack")
    if not repository:
        raise ValueError("policy rollout must include repository")
    if not policy_pack:
        raise ValueError("policy rollout must include policy_pack")
    state = str(payload.get("state", "planned"))
    mode = str(payload.get("mode", "enforce"))
    if state not in POLICY_ROLLOUT_STATES:
        raise ValueError(f"policy rollout state must be one of: {', '.join(sorted(POLICY_ROLLOUT_STATES))}")
    if mode not in POLICY_MODES:
        raise ValueError(f"policy rollout mode must be one of: {', '.join(sorted(POLICY_MODES))}")
    rollout_id = payload.get("rollout_id") or f"{repository}:{policy_pack}"
    now = utc_now()
    return {
        "schema_version": "cavra.policy_rollout.v1",
        "rollout_id": str(rollout_id),
        "repository": str(repository),
        "policy_pack": str(policy_pack),
        "policy_version": str(payload.get("policy_version", "latest")),
        "mode": mode,
        "state": state,
        "owner": str(payload.get("owner", "platform-security")),
        "coverage_percent": int(payload.get("coverage_percent", 0)),
        "last_evaluated_at": payload.get("last_evaluated_at"),
        "created_at": payload.get("created_at") or now,
        "updated_at": now,
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
    }


class InventoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list_repositories(
        self,
        *,
        provider: str | None = None,
        owner: str | None = None,
        policy_pack: str | None = None,
        status: str | None = None,
        risk_tier: str | None = None,
    ) -> dict[str, Any]:
        items = _filter_records(
            self._load()["repositories"],
            provider=provider,
            owner=owner,
            policy_pack=policy_pack,
            status=status,
            risk_tier=risk_tier,
        )
        return {"items": sorted(items, key=lambda item: item.get("repository", "")), "total": len(items)}

    def upsert_repository(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_repository_record(payload)
        data = self._load()
        data["repositories"] = [
            item for item in data["repositories"] if item.get("repository_id") != record["repository_id"]
        ]
        data["repositories"].append(record)
        self._save(data)
        return record

    def get_repository(self, repository_id: str) -> dict[str, Any] | None:
        return next(
            (
                item
                for item in self._load()["repositories"]
                if item.get("repository_id") == repository_id or item.get("repository") == repository_id
            ),
            None,
        )

    def list_policy_rollouts(
        self,
        *,
        repository: str | None = None,
        policy_pack: str | None = None,
        state: str | None = None,
        mode: str | None = None,
        owner: str | None = None,
    ) -> dict[str, Any]:
        items = _filter_records(
            self._load()["policy_rollouts"],
            repository=repository,
            policy_pack=policy_pack,
            state=state,
            mode=mode,
            owner=owner,
        )
        return {"items": sorted(items, key=lambda item: item.get("rollout_id", "")), "total": len(items)}

    def upsert_policy_rollout(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_policy_rollout_record(payload)
        data = self._load()
        data["policy_rollouts"] = [
            item for item in data["policy_rollouts"] if item.get("rollout_id") != record["rollout_id"]
        ]
        data["policy_rollouts"].append(record)
        self._save(data)
        return record

    def get_policy_rollout(self, rollout_id: str) -> dict[str, Any] | None:
        return next((item for item in self._load()["policy_rollouts"] if item.get("rollout_id") == rollout_id), None)

    def _load(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists():
            return {"repositories": [], "policy_rollouts": []}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return {
            "repositories": list(payload.get("repositories", [])),
            "policy_rollouts": list(payload.get("policy_rollouts", [])),
        }

    def _save(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class SQLiteInventoryStore:
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
                CREATE TABLE IF NOT EXISTS inventory_repositories (
                  repository_id TEXT PRIMARY KEY,
                  repository TEXT NOT NULL,
                  provider TEXT,
                  owner TEXT,
                  policy_pack TEXT,
                  risk_tier TEXT,
                  status TEXT NOT NULL,
                  updated_at TEXT NOT NULL,
                  payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_inventory_repositories_provider ON inventory_repositories (provider)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_inventory_repositories_owner ON inventory_repositories (owner)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_inventory_repositories_policy ON inventory_repositories (policy_pack)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_inventory_repositories_status ON inventory_repositories (status)")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS inventory_policy_rollouts (
                  rollout_id TEXT PRIMARY KEY,
                  repository TEXT NOT NULL,
                  policy_pack TEXT NOT NULL,
                  state TEXT NOT NULL,
                  mode TEXT NOT NULL,
                  owner TEXT,
                  updated_at TEXT NOT NULL,
                  payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_inventory_rollouts_repository ON inventory_policy_rollouts (repository)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_inventory_rollouts_policy ON inventory_policy_rollouts (policy_pack)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_inventory_rollouts_state ON inventory_policy_rollouts (state)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_inventory_rollouts_mode ON inventory_policy_rollouts (mode)")

    def list_repositories(
        self,
        *,
        provider: str | None = None,
        owner: str | None = None,
        policy_pack: str | None = None,
        status: str | None = None,
        risk_tier: str | None = None,
    ) -> dict[str, Any]:
        params = _optional_filter_params(provider, owner, policy_pack, status, risk_tier)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload FROM inventory_repositories
                WHERE (? IS NULL OR provider = ?)
                  AND (? IS NULL OR owner = ?)
                  AND (? IS NULL OR policy_pack = ?)
                  AND (? IS NULL OR status = ?)
                  AND (? IS NULL OR risk_tier = ?)
                ORDER BY repository ASC
                """,
                params,
            ).fetchall()
        items = [json.loads(row["payload"]) for row in rows]
        return {"items": items, "total": len(items)}

    def upsert_repository(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_repository_record(payload)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO inventory_repositories (
                  repository_id, repository, provider, owner, policy_pack, risk_tier, status, updated_at, payload
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(repository_id) DO UPDATE SET
                  repository=excluded.repository,
                  provider=excluded.provider,
                  owner=excluded.owner,
                  policy_pack=excluded.policy_pack,
                  risk_tier=excluded.risk_tier,
                  status=excluded.status,
                  updated_at=excluded.updated_at,
                  payload=excluded.payload
                """,
                (
                    record["repository_id"],
                    record["repository"],
                    record["provider"],
                    record["owner"],
                    record["policy_pack"],
                    record["risk_tier"],
                    record["status"],
                    record["updated_at"],
                    json.dumps(record, sort_keys=True),
                ),
            )
        return record

    def get_repository(self, repository_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM inventory_repositories WHERE repository_id = ? OR repository = ?",
                (repository_id, repository_id),
            ).fetchone()
        return json.loads(row["payload"]) if row else None

    def list_policy_rollouts(
        self,
        *,
        repository: str | None = None,
        policy_pack: str | None = None,
        state: str | None = None,
        mode: str | None = None,
        owner: str | None = None,
    ) -> dict[str, Any]:
        params = _optional_filter_params(repository, policy_pack, state, mode, owner)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload FROM inventory_policy_rollouts
                WHERE (? IS NULL OR repository = ?)
                  AND (? IS NULL OR policy_pack = ?)
                  AND (? IS NULL OR state = ?)
                  AND (? IS NULL OR mode = ?)
                  AND (? IS NULL OR owner = ?)
                ORDER BY rollout_id ASC
                """,
                params,
            ).fetchall()
        items = [json.loads(row["payload"]) for row in rows]
        return {"items": items, "total": len(items)}

    def upsert_policy_rollout(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_policy_rollout_record(payload)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO inventory_policy_rollouts (
                  rollout_id, repository, policy_pack, state, mode, owner, updated_at, payload
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(rollout_id) DO UPDATE SET
                  repository=excluded.repository,
                  policy_pack=excluded.policy_pack,
                  state=excluded.state,
                  mode=excluded.mode,
                  owner=excluded.owner,
                  updated_at=excluded.updated_at,
                  payload=excluded.payload
                """,
                (
                    record["rollout_id"],
                    record["repository"],
                    record["policy_pack"],
                    record["state"],
                    record["mode"],
                    record["owner"],
                    record["updated_at"],
                    json.dumps(record, sort_keys=True),
                ),
            )
        return record

    def get_policy_rollout(self, rollout_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload FROM inventory_policy_rollouts WHERE rollout_id = ?", (rollout_id,)).fetchone()
        return json.loads(row["payload"]) if row else None


def _optional_filter_params(*values: str | None) -> list[Any]:
    params: list[Any] = []
    for value in values:
        params.extend([value, value])
    return params


def _filter_records(items: list[dict[str, Any]], **filters: str | None) -> list[dict[str, Any]]:
    filtered = items
    for key, value in filters.items():
        if value:
            filtered = [item for item in filtered if item.get(key) == value]
    return filtered


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    raise ValueError("expected a string or list of strings")
