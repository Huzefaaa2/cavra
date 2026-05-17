from __future__ import annotations

import json
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.audit import SessionAudit, action_from_decision, create_attestation_markdown
from cavra.runtime import RuntimeGuard


@dataclass
class ExecutionResult:
    success: bool
    output: str
    error: str | None = None


class CommandInterceptor:
    def __init__(self, guard: RuntimeGuard, audit: SessionAudit) -> None:
        self.guard = guard
        self.audit = audit

    def execute(self, command: str) -> ExecutionResult:
        decision = self.guard.evaluate_command(command)
        self.audit.add_action(action_from_decision(decision))

        if decision.decision == "block":
            return ExecutionResult(
                success=False, output="", error=f"Command blocked: {decision.reason}"
            )

        if decision.decision == "require_approval":
            return ExecutionResult(
                success=False,
                output="",
                error=f"Command requires approval: {decision.reason}",
            )

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=False
            )
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
            )
        except Exception as exc:
            return ExecutionResult(success=False, output="", error=str(exc))


class GitHubPRAttestationExporter:
    @staticmethod
    def export_comment(audit: SessionAudit) -> str:
        markdown = create_attestation_markdown(audit)
        return markdown

    @staticmethod
    def export_json(audit: SessionAudit) -> str:
        return json.dumps(audit.to_dict(), indent=2)

    @staticmethod
    def save_artifact(audit: SessionAudit, destination: Path) -> Path:
        destination.mkdir(parents=True, exist_ok=True)
        artifact_path = destination / f"cavra-attestation-{audit.session_id}.json"
        artifact_path.write_text(
            GitHubPRAttestationExporter.export_json(audit), encoding="utf-8"
        )
        return artifact_path


class WebhookExporter:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def export(self, audit: SessionAudit) -> bool:
        try:
            import requests

            response = requests.post(
                self.webhook_url,
                json=audit.to_dict(),
                timeout=10,
            )
            return response.status_code in (200, 201, 204)
        except Exception:
            return False


INTEGRATION_CATEGORIES = {
    "source_control",
    "ci_cd",
    "siem",
    "itsm",
    "chatops",
    "identity",
    "cloud",
    "storage",
    "security",
    "observability",
}
INTEGRATION_STATUSES = {"planned", "configured", "active", "paused", "disabled"}
INTEGRATION_HEALTH = {"unknown", "healthy", "degraded", "failed", "not_checked"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_integration_record(payload: dict[str, Any]) -> dict[str, Any]:
    provider = payload.get("provider")
    if not provider:
        raise ValueError("integration record must include provider")
    integration_id = payload.get("integration_id") or payload.get("id") or _slug(
        str(provider), str(payload.get("environment", "global"))
    )
    category = str(payload.get("category", "security"))
    status = str(payload.get("status", "planned"))
    health_status = str(payload.get("health_status", "not_checked"))
    if category not in INTEGRATION_CATEGORIES:
        raise ValueError("invalid integration category")
    if status not in INTEGRATION_STATUSES:
        raise ValueError("invalid integration status")
    if health_status not in INTEGRATION_HEALTH:
        raise ValueError("invalid integration health status")
    now = utc_now()
    return {
        "schema_version": "cavra.integration.v1",
        "integration_id": str(integration_id),
        "name": str(payload.get("name") or provider),
        "provider": str(provider),
        "category": category,
        "status": status,
        "health_status": health_status,
        "owner": str(payload.get("owner", "platform-security")),
        "environment": str(payload.get("environment", "global")),
        "auth_mode": str(payload.get("auth_mode", "not_configured")),
        "endpoint_ref": payload.get("endpoint_ref"),
        "capabilities": _string_list(payload.get("capabilities", [])),
        "repositories": _string_list(payload.get("repositories", [])),
        "last_checked_at": payload.get("last_checked_at"),
        "created_at": payload.get("created_at") or now,
        "updated_at": now,
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
    }


class IntegrationStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list_integrations(
        self,
        *,
        provider: str | None = None,
        category: str | None = None,
        status: str | None = None,
        owner: str | None = None,
        environment: str | None = None,
        health_status: str | None = None,
    ) -> dict[str, Any]:
        items = _filter_records(
            self._load()["integrations"],
            provider=provider,
            category=category,
            status=status,
            owner=owner,
            environment=environment,
            health_status=health_status,
        )
        return {"items": sorted(items, key=lambda item: item.get("integration_id", "")), "total": len(items)}

    def upsert_integration(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_integration_record(payload)
        data = self._load()
        data["integrations"] = [
            item for item in data["integrations"] if item.get("integration_id") != record["integration_id"]
        ]
        data["integrations"].append(record)
        self._save(data)
        return record

    def get_integration(self, integration_id: str) -> dict[str, Any] | None:
        return next(
            (
                item
                for item in self._load()["integrations"]
                if item.get("integration_id") == integration_id or item.get("provider") == integration_id
            ),
            None,
        )

    def _load(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists():
            return {"integrations": []}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return {"integrations": list(payload.get("integrations", []))}

    def _save(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class SQLiteIntegrationStore:
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
                CREATE TABLE IF NOT EXISTS integrations (
                  integration_id TEXT PRIMARY KEY,
                  provider TEXT NOT NULL,
                  category TEXT NOT NULL,
                  status TEXT NOT NULL,
                  owner TEXT,
                  environment TEXT,
                  health_status TEXT,
                  updated_at TEXT NOT NULL,
                  payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_integrations_provider ON integrations (provider)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_integrations_category ON integrations (category)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_integrations_status ON integrations (status)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_integrations_owner ON integrations (owner)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_integrations_health ON integrations (health_status)")

    def list_integrations(
        self,
        *,
        provider: str | None = None,
        category: str | None = None,
        status: str | None = None,
        owner: str | None = None,
        environment: str | None = None,
        health_status: str | None = None,
    ) -> dict[str, Any]:
        params = _optional_filter_params(provider, category, status, owner, environment, health_status)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload FROM integrations
                WHERE (? IS NULL OR provider = ?)
                  AND (? IS NULL OR category = ?)
                  AND (? IS NULL OR status = ?)
                  AND (? IS NULL OR owner = ?)
                  AND (? IS NULL OR environment = ?)
                  AND (? IS NULL OR health_status = ?)
                ORDER BY integration_id ASC
                """,
                params,
            ).fetchall()
        items = [json.loads(row["payload"]) for row in rows]
        return {"items": items, "total": len(items)}

    def upsert_integration(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_integration_record(payload)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO integrations (
                  integration_id, provider, category, status, owner, environment, health_status, updated_at, payload
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(integration_id) DO UPDATE SET
                  provider=excluded.provider,
                  category=excluded.category,
                  status=excluded.status,
                  owner=excluded.owner,
                  environment=excluded.environment,
                  health_status=excluded.health_status,
                  updated_at=excluded.updated_at,
                  payload=excluded.payload
                """,
                (
                    record["integration_id"],
                    record["provider"],
                    record["category"],
                    record["status"],
                    record["owner"],
                    record["environment"],
                    record["health_status"],
                    record["updated_at"],
                    json.dumps(record, sort_keys=True),
                ),
            )
        return record

    def get_integration(self, integration_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM integrations WHERE integration_id = ? OR provider = ?",
                (integration_id, integration_id),
            ).fetchone()
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


def _slug(*parts: str) -> str:
    raw = "-".join(parts).lower()
    return "".join(char if char.isalnum() else "-" for char in raw).strip("-")
