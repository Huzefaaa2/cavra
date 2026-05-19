from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

from cavra.audit import SessionAudit, action_from_decision, create_attestation_markdown
from cavra.evidence import build_datadog_events, build_sentinel_events, build_splunk_hec_events, build_webhook_payload
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
CONNECTOR_PROVIDERS = {"splunk", "sentinel", "datadog", "webhook", "slack", "teams", "jira", "servicenow"}


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


def load_connector_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"connector config not found: {path}")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install PyYAML to load connector config files.") from exc
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("connector config must be an object")
    return payload


def build_connector_request_specs(event: dict[str, Any], config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    connectors = _connector_config(config)
    specs: dict[str, dict[str, Any]] = {}
    for provider, provider_config in connectors.items():
        if provider not in CONNECTOR_PROVIDERS or not provider_config.get("enabled", True):
            continue
        url = _configured_value(provider_config, "url")
        if not url:
            raise ValueError(f"connector {provider} must configure url or url_env")
        headers = {"content-type": "application/json", **_configured_headers(provider_config)}
        if provider in {"splunk", "sentinel", "datadog", "jira", "servicenow"} and not _has_auth(headers, provider_config):
            raise ValueError(f"connector {provider} must configure token_env, authorization_env, api_key_env, or authorization header")
        specs[provider] = {
            "method": str(provider_config.get("method", "POST")),
            "url": url,
            "headers": headers,
            "body": _connector_body(provider, event, provider_config),
        }
    return specs


def deliver_connector_event(
    event: dict[str, Any],
    config: dict[str, Any],
    *,
    provider: str = "all",
    retries: int = 2,
    timeout_seconds: float = 10.0,
    sender: Any | None = None,
) -> dict[str, Any]:
    specs = build_connector_request_specs(event, config)
    providers = set(specs) if provider == "all" else {provider}
    unknown = providers - set(specs)
    if unknown:
        raise ValueError(f"connector provider is not configured: {', '.join(sorted(unknown))}")
    delivery_sender = sender or _send_http_json_request
    deliveries = [
        _deliver_one_connector(
            item,
            specs[item],
            retries=max(0, retries),
            timeout_seconds=max(0.1, timeout_seconds),
            sender=delivery_sender,
        )
        for item in sorted(providers)
    ]
    return {
        "schema_version": "cavra.connector.delivery.v1",
        "product": "CAVRA",
        "event_type": event.get("event_type", "cavra.connector.event"),
        "event_id": _event_identity(event),
        "session_id": event.get("session_id"),
        "generated_at": utc_now(),
        "success": all(item["success"] for item in deliveries),
        "deliveries": deliveries,
    }


def export_connector_delivery_result(result: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    event_id = str(result.get("event_id") or result.get("session_id") or result.get("event_type") or "connector").replace("/", "-")
    path = output_dir / f"{event_id}-connector-delivery.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _event_identity(event: dict[str, Any]) -> str | None:
    for key in ("session_id", "execution_id", "rollback_id", "approval_id", "request_id", "event_id"):
        if event.get(key):
            return str(event[key])
    return str(event.get("event_type")) if event.get("event_type") else None


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


def _connector_config(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    connectors = config.get("connectors", config.get("providers", config))
    if not isinstance(connectors, dict):
        raise ValueError("connector config must contain connector objects")
    normalized: dict[str, dict[str, Any]] = {}
    for provider, provider_config in connectors.items():
        if not isinstance(provider_config, dict):
            raise ValueError(f"connector {provider} config must be an object")
        normalized[str(provider)] = provider_config
    return normalized


def _configured_value(provider_config: dict[str, Any], key: str) -> str | None:
    env_value = provider_config.get(f"{key}_env")
    if env_value:
        configured = os.environ.get(str(env_value))
        if not configured:
            raise ValueError(f"environment variable {env_value} is required for connector {key}")
        return configured
    value = provider_config.get(key)
    return str(value) if value else None


def _configured_headers(provider_config: dict[str, Any]) -> dict[str, str]:
    headers = {str(key).lower(): str(value) for key, value in provider_config.get("headers", {}).items()}
    authorization = _configured_value(provider_config, "authorization")
    token = _configured_value(provider_config, "token")
    api_key = _configured_value(provider_config, "api_key")
    if authorization:
        headers["authorization"] = authorization
    elif token:
        scheme = str(provider_config.get("authorization_scheme", "Bearer"))
        headers["authorization"] = f"{scheme} {token}"
    if api_key:
        headers[str(provider_config.get("api_key_header", "x-api-key")).lower()] = api_key
    return headers


def _has_auth(headers: dict[str, str], provider_config: dict[str, Any]) -> bool:
    if "authorization" in headers or "x-api-key" in headers or "dd-api-key" in headers:
        return True
    return bool(provider_config.get("token") or provider_config.get("token_env") or provider_config.get("api_key") or provider_config.get("api_key_env"))


def _connector_body(provider: str, event: dict[str, Any], provider_config: dict[str, Any]) -> dict[str, Any]:
    title = str(provider_config.get("title") or f"CAVRA {event.get('event_type', 'event')}")
    if provider == "splunk":
        return build_splunk_hec_events(event, index=str(provider_config.get("index", "cavra")))[0]
    if provider == "sentinel":
        return {"records": build_sentinel_events(event)}
    if provider == "datadog":
        return {"events": build_datadog_events(event, service=str(provider_config.get("service", "cavra")))}
    if provider == "webhook":
        return build_webhook_payload(event)
    if provider == "slack":
        return {
            "text": title,
            "blocks": [
                {"type": "header", "text": {"type": "plain_text", "text": title}},
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Event:* {event.get('event_type', 'cavra.event')}"},
                        {"type": "mrkdwn", "text": f"*Session:* {event.get('session_id', 'n/a')}"},
                        {"type": "mrkdwn", "text": f"*Blocked:* {event.get('blocked_count', 0)}"},
                        {"type": "mrkdwn", "text": f"*Severity:* {event.get('max_severity', 'low')}"},
                    ],
                },
            ],
        }
    if provider == "teams":
        return {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title,
            "themeColor": "C62828" if event.get("blocked_count", 0) else "2E7D32",
            "sections": [
                {
                    "activityTitle": title,
                    "facts": [
                        {"name": "Event", "value": str(event.get("event_type", "cavra.event"))},
                        {"name": "Session", "value": str(event.get("session_id", "n/a"))},
                        {"name": "Blocked", "value": str(event.get("blocked_count", 0))},
                        {"name": "Severity", "value": str(event.get("max_severity", "low"))},
                    ],
                }
            ],
        }
    if provider == "jira":
        return {
            "fields": {
                "summary": title,
                "description": json.dumps(event, indent=2, sort_keys=True),
                "labels": ["cavra", "ai-agent-governance", str(event.get("event_type", "event")).replace(".", "-")],
            }
        }
    if provider == "servicenow":
        return {
            "short_description": title,
            "description": json.dumps(event, indent=2, sort_keys=True),
            "category": "software",
            "correlation_id": event.get("session_id") or event.get("event_type"),
        }
    raise ValueError(f"unsupported connector provider: {provider}")


def _deliver_one_connector(
    provider: str,
    spec: dict[str, Any],
    *,
    retries: int,
    timeout_seconds: float,
    sender: Any,
) -> dict[str, Any]:
    attempts = retries + 1
    last_result: dict[str, Any] | None = None
    for attempt in range(1, attempts + 1):
        started_at = utc_now()
        try:
            response = sender(spec, timeout_seconds=timeout_seconds)
            status_code = int(response.get("status_code", 0))
            success = 200 <= status_code < 300
            last_result = {
                "provider": provider,
                "success": success,
                "status_code": status_code,
                "attempt_count": attempt,
                "started_at": started_at,
                "completed_at": utc_now(),
                "error": None if success else response.get("error") or f"HTTP {status_code}",
                "request": _redacted_request_spec(spec),
            }
            if success:
                return last_result
        except Exception:  # pragma: no cover - exercised through sender tests
            last_result = {
                "provider": provider,
                "success": False,
                "status_code": None,
                "attempt_count": attempt,
                "started_at": started_at,
                "completed_at": utc_now(),
                "error": "connector delivery failed",
                "request": _redacted_request_spec(spec),
            }
        if attempt < attempts:
            time.sleep(min(0.25 * attempt, 1.0))
    return last_result or {
        "provider": provider,
        "success": False,
        "status_code": None,
        "attempt_count": 0,
        "started_at": utc_now(),
        "completed_at": utc_now(),
        "error": "delivery was not attempted",
        "request": _redacted_request_spec(spec),
    }


def _send_http_json_request(spec: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    body = json.dumps(spec.get("body", {})).encode("utf-8")
    headers = {str(key): str(value) for key, value in spec.get("headers", {}).items()}
    req = request.Request(str(spec["url"]), data=body, headers=headers, method=str(spec.get("method", "POST")))
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            return {"status_code": response.getcode(), "body": response.read(4096).decode("utf-8", errors="replace")}
    except error.HTTPError as exc:
        return {"status_code": exc.code, "body": exc.read(4096).decode("utf-8", errors="replace"), "error": "HTTP request failed"}
    except error.URLError:
        return {"status_code": 0, "error": "connector endpoint unreachable"}


def _redacted_request_spec(spec: dict[str, Any]) -> dict[str, Any]:
    headers = {}
    for key, value in spec.get("headers", {}).items():
        lowered = str(key).lower()
        headers[lowered] = "REDACTED" if lowered in {"authorization", "x-api-key", "api-key", "dd-api-key"} else value
    return {
        "method": spec.get("method", "POST"),
        "url": _redact_url(str(spec.get("url", ""))),
        "headers": headers,
    }


def _redact_url(url: str) -> str:
    if "hooks.slack.com/services/" in url:
        return "https://hooks.slack.com/services/REDACTED"
    if "?" in url:
        return f"{url.split('?', 1)[0]}?REDACTED"
    return url
