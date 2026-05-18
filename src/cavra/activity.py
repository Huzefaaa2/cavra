from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DECISION_STATES = {"allow", "block", "require_approval", "warn", "audit_only", "allow_with_attestation"}
SESSION_STATES = {"active", "completed", "failed", "archived"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_decision_record(payload: dict[str, Any]) -> dict[str, Any]:
    decision = str(payload.get("decision", "audit_only"))
    if decision not in DECISION_STATES:
        raise ValueError(f"decision must be one of: {', '.join(sorted(DECISION_STATES))}")
    decision_id = payload.get("decision_id") or f"dec_{uuid.uuid4().hex[:12]}"
    timestamp = payload.get("timestamp") or utc_now()
    session_id = str(payload.get("session_id") or "local")
    return {
        "schema_version": "cavra.decision.v1",
        "decision_id": str(decision_id),
        "session_id": session_id,
        "agent_id": str(payload.get("agent_id", "unknown-agent")),
        "actor": str(payload.get("actor", "ai-agent")),
        "repository": payload.get("repository", "local"),
        "action_type": str(payload.get("action_type", "unknown")),
        "target": str(payload.get("target", "")),
        "requested_operation": str(payload.get("requested_operation", "")),
        "policy_pack": str(payload.get("policy_pack", "cavra-ai-agent-baseline")),
        "policy_id": str(payload.get("policy_id", payload.get("policy_pack", "cavra-ai-agent-baseline"))),
        "rule_id": str(payload.get("rule_id", "runtime.default")),
        "decision": decision,
        "severity": str(payload.get("severity", "low")),
        "reason": payload.get("reason"),
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
        "approver_group": payload.get("approver_group"),
        "timestamp": timestamp,
        "correlation_id": str(payload.get("correlation_id") or f"corr_{uuid.uuid4().hex[:12]}"),
    }


def normalize_session_record(payload: dict[str, Any], decisions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    session_id = payload.get("session_id")
    if not session_id:
        raise ValueError("session record must include session_id")
    decisions = decisions or []
    now = utc_now()
    state = str(payload.get("state", payload.get("status", "active")))
    if state not in SESSION_STATES:
        raise ValueError(f"session state must be one of: {', '.join(sorted(SESSION_STATES))}")
    timestamps = [str(item.get("timestamp")) for item in decisions if item.get("timestamp")]
    decision_count = len(decisions) if decisions else int(payload.get("decision_count", 0))
    blocked_count = _count_decisions(decisions, "block") if decisions else int(payload.get("blocked_count", 0))
    approval_required_count = (
        _count_decisions(decisions, "require_approval") if decisions else int(payload.get("approval_required_count", 0))
    )
    return {
        "schema_version": "cavra.session.v1",
        "session_id": str(session_id),
        "agent_id": str(payload.get("agent_id", _first_value(decisions, "agent_id", "unknown-agent"))),
        "actor": str(payload.get("actor", _first_value(decisions, "actor", "ai-agent"))),
        "repository": payload.get("repository", _first_value(decisions, "repository", "local")),
        "policy_pack": str(payload.get("policy_pack", _first_value(decisions, "policy_pack", "cavra-ai-agent-baseline"))),
        "state": state,
        "started_at": payload.get("started_at") or min(timestamps, default=now),
        "updated_at": payload.get("updated_at") or max(timestamps, default=now),
        "decision_count": decision_count,
        "blocked_count": blocked_count,
        "approval_required_count": approval_required_count,
        "evidence_refs": _string_list(payload.get("evidence_refs", _session_evidence_refs(decisions))),
    }


class ActivityStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list_decisions(
        self,
        *,
        session_id: str | None = None,
        agent_id: str | None = None,
        repository: str | None = None,
        policy_pack: str | None = None,
        decision: str | None = None,
        severity: str | None = None,
        action_type: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        items = self._load()["decisions"]
        items = _filter_records(
            items,
            session_id=session_id,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            decision=decision,
            severity=severity,
            action_type=action_type,
        )
        items = sorted(items, key=lambda item: (str(item.get("timestamp", "")), str(item.get("decision_id", ""))), reverse=True)
        return {"items": items[offset : offset + limit], "total": len(items), "limit": limit, "offset": offset}

    def upsert_decision(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_decision_record(payload)
        data = self._load()
        data["decisions"] = [item for item in data["decisions"] if item.get("decision_id") != record["decision_id"]]
        data["decisions"].append(record)
        self._upsert_session_summary(data, record)
        self._save(data)
        return record

    def get_decision(self, decision_id: str) -> dict[str, Any] | None:
        return next((item for item in self._load()["decisions"] if item.get("decision_id") == decision_id), None)

    def list_sessions(
        self,
        *,
        agent_id: str | None = None,
        repository: str | None = None,
        policy_pack: str | None = None,
        state: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        items = self._load()["sessions"]
        items = _filter_records(items, agent_id=agent_id, repository=repository, policy_pack=policy_pack, state=state)
        items = sorted(items, key=lambda item: (str(item.get("updated_at", "")), str(item.get("session_id", ""))), reverse=True)
        return {"items": items[offset : offset + limit], "total": len(items), "limit": limit, "offset": offset}

    def summarize_sessions(
        self,
        *,
        agent_id: str | None = None,
        repository: str | None = None,
        policy_pack: str | None = None,
        state: str | None = None,
    ) -> dict[str, Any]:
        items = self._load()["sessions"]
        items = _filter_records(items, agent_id=agent_id, repository=repository, policy_pack=policy_pack, state=state)
        return _summarize_session_records(items)

    def upsert_session(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = self._load()
        session_id = payload.get("session_id")
        decisions = [item for item in data["decisions"] if item.get("session_id") == session_id]
        record = normalize_session_record(payload, decisions)
        data["sessions"] = [item for item in data["sessions"] if item.get("session_id") != record["session_id"]]
        data["sessions"].append(record)
        self._save(data)
        return record

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        return next((item for item in self._load()["sessions"] if item.get("session_id") == session_id), None)

    def _upsert_session_summary(self, data: dict[str, list[dict[str, Any]]], decision: dict[str, Any]) -> None:
        session_id = decision["session_id"]
        existing = next((item for item in data["sessions"] if item.get("session_id") == session_id), {})
        decisions = [item for item in data["decisions"] if item.get("session_id") == session_id]
        summary = normalize_session_record({**existing, **_session_payload_from_decision(decision)}, decisions)
        data["sessions"] = [item for item in data["sessions"] if item.get("session_id") != session_id]
        data["sessions"].append(summary)

    def _load(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists():
            return {"sessions": [], "decisions": []}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return {
            "sessions": list(payload.get("sessions", [])),
            "decisions": list(payload.get("decisions", [])),
        }

    def _save(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class SQLiteActivityStore:
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
                CREATE TABLE IF NOT EXISTS activity_sessions (
                  session_id TEXT PRIMARY KEY,
                  agent_id TEXT,
                  actor TEXT,
                  repository TEXT,
                  policy_pack TEXT,
                  state TEXT NOT NULL,
                  started_at TEXT NOT NULL,
                  updated_at TEXT NOT NULL,
                  decision_count INTEGER NOT NULL DEFAULT 0,
                  blocked_count INTEGER NOT NULL DEFAULT 0,
                  approval_required_count INTEGER NOT NULL DEFAULT 0,
                  payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_sessions_agent ON activity_sessions (agent_id)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_sessions_repository ON activity_sessions (repository)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_sessions_policy ON activity_sessions (policy_pack)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_sessions_updated ON activity_sessions (updated_at)")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS activity_decisions (
                  decision_id TEXT PRIMARY KEY,
                  session_id TEXT NOT NULL,
                  agent_id TEXT,
                  actor TEXT,
                  repository TEXT,
                  policy_pack TEXT,
                  action_type TEXT,
                  target TEXT,
                  rule_id TEXT,
                  decision TEXT NOT NULL,
                  severity TEXT,
                  timestamp TEXT NOT NULL,
                  correlation_id TEXT,
                  payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_decisions_session ON activity_decisions (session_id)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_decisions_agent ON activity_decisions (agent_id)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_decisions_repository ON activity_decisions (repository)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_decisions_policy ON activity_decisions (policy_pack)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_decisions_decision ON activity_decisions (decision)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_activity_decisions_timestamp ON activity_decisions (timestamp)")

    def list_decisions(
        self,
        *,
        session_id: str | None = None,
        agent_id: str | None = None,
        repository: str | None = None,
        policy_pack: str | None = None,
        decision: str | None = None,
        severity: str | None = None,
        action_type: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        params = _optional_filter_params(session_id, agent_id, repository, policy_pack, decision, severity, action_type)
        with self._connect() as connection:
            total = connection.execute(
                """
                SELECT COUNT(*) AS count FROM activity_decisions
                WHERE (? IS NULL OR session_id = ?)
                  AND (? IS NULL OR agent_id = ?)
                  AND (? IS NULL OR repository = ?)
                  AND (? IS NULL OR policy_pack = ?)
                  AND (? IS NULL OR decision = ?)
                  AND (? IS NULL OR severity = ?)
                  AND (? IS NULL OR action_type = ?)
                """,
                params,
            ).fetchone()["count"]
            rows = connection.execute(
                """
                SELECT payload FROM activity_decisions
                WHERE (? IS NULL OR session_id = ?)
                  AND (? IS NULL OR agent_id = ?)
                  AND (? IS NULL OR repository = ?)
                  AND (? IS NULL OR policy_pack = ?)
                  AND (? IS NULL OR decision = ?)
                  AND (? IS NULL OR severity = ?)
                  AND (? IS NULL OR action_type = ?)
                ORDER BY timestamp DESC, decision_id ASC
                LIMIT ? OFFSET ?
                """,
                [*params, limit, offset],
            ).fetchall()
        return {"items": [json.loads(row["payload"]) for row in rows], "total": total, "limit": limit, "offset": offset}

    def upsert_decision(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = normalize_decision_record(payload)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO activity_decisions (
                  decision_id, session_id, agent_id, actor, repository, policy_pack, action_type,
                  target, rule_id, decision, severity, timestamp, correlation_id, payload
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(decision_id) DO UPDATE SET
                  session_id=excluded.session_id,
                  agent_id=excluded.agent_id,
                  actor=excluded.actor,
                  repository=excluded.repository,
                  policy_pack=excluded.policy_pack,
                  action_type=excluded.action_type,
                  target=excluded.target,
                  rule_id=excluded.rule_id,
                  decision=excluded.decision,
                  severity=excluded.severity,
                  timestamp=excluded.timestamp,
                  correlation_id=excluded.correlation_id,
                  payload=excluded.payload
                """,
                _decision_row(record),
            )
        self._refresh_session_summary(record["session_id"], _session_payload_from_decision(record))
        return record

    def get_decision(self, decision_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload FROM activity_decisions WHERE decision_id = ?", (decision_id,)).fetchone()
        return json.loads(row["payload"]) if row else None

    def list_sessions(
        self,
        *,
        agent_id: str | None = None,
        repository: str | None = None,
        policy_pack: str | None = None,
        state: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        params = _optional_filter_params(agent_id, repository, policy_pack, state)
        with self._connect() as connection:
            total = connection.execute(
                """
                SELECT COUNT(*) AS count FROM activity_sessions
                WHERE (? IS NULL OR agent_id = ?)
                  AND (? IS NULL OR repository = ?)
                  AND (? IS NULL OR policy_pack = ?)
                  AND (? IS NULL OR state = ?)
                """,
                params,
            ).fetchone()["count"]
            rows = connection.execute(
                """
                SELECT payload FROM activity_sessions
                WHERE (? IS NULL OR agent_id = ?)
                  AND (? IS NULL OR repository = ?)
                  AND (? IS NULL OR policy_pack = ?)
                  AND (? IS NULL OR state = ?)
                ORDER BY updated_at DESC, session_id ASC
                LIMIT ? OFFSET ?
                """,
                [*params, limit, offset],
            ).fetchall()
        return {"items": [json.loads(row["payload"]) for row in rows], "total": total, "limit": limit, "offset": offset}

    def summarize_sessions(
        self,
        *,
        agent_id: str | None = None,
        repository: str | None = None,
        policy_pack: str | None = None,
        state: str | None = None,
    ) -> dict[str, Any]:
        params = _optional_filter_params(agent_id, repository, policy_pack, state)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                  COUNT(*) AS total_sessions,
                  COALESCE(SUM(decision_count), 0) AS total_decisions,
                  COALESCE(SUM(blocked_count), 0) AS total_blocked,
                  COALESCE(SUM(approval_required_count), 0) AS total_approval_required,
                  MAX(updated_at) AS latest_session_at
                FROM activity_sessions
                WHERE (? IS NULL OR agent_id = ?)
                  AND (? IS NULL OR repository = ?)
                  AND (? IS NULL OR policy_pack = ?)
                  AND (? IS NULL OR state = ?)
                """,
                params,
            ).fetchone()
        return {
            "total_sessions": int(row["total_sessions"] or 0),
            "total_decisions": int(row["total_decisions"] or 0),
            "total_blocked": int(row["total_blocked"] or 0),
            "total_approval_required": int(row["total_approval_required"] or 0),
            "latest_session_at": row["latest_session_at"],
        }

    def upsert_session(self, payload: dict[str, Any]) -> dict[str, Any]:
        session_id = payload.get("session_id")
        if not session_id:
            raise ValueError("session record must include session_id")
        self._refresh_session_summary(str(session_id), payload)
        item = self.get_session(str(session_id))
        if item is None:
            raise ValueError("session record was not persisted")
        return item

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload FROM activity_sessions WHERE session_id = ?", (session_id,)).fetchone()
        return json.loads(row["payload"]) if row else None

    def _refresh_session_summary(self, session_id: str, payload: dict[str, Any]) -> None:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT payload FROM activity_decisions WHERE session_id = ? ORDER BY timestamp ASC",
                (session_id,),
            ).fetchall()
            existing_row = connection.execute("SELECT payload FROM activity_sessions WHERE session_id = ?", (session_id,)).fetchone()
        existing = json.loads(existing_row["payload"]) if existing_row else {}
        decisions = [json.loads(row["payload"]) for row in rows]
        record = normalize_session_record({**existing, **payload, "session_id": session_id}, decisions)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO activity_sessions (
                  session_id, agent_id, actor, repository, policy_pack, state, started_at, updated_at,
                  decision_count, blocked_count, approval_required_count, payload
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                  agent_id=excluded.agent_id,
                  actor=excluded.actor,
                  repository=excluded.repository,
                  policy_pack=excluded.policy_pack,
                  state=excluded.state,
                  started_at=excluded.started_at,
                  updated_at=excluded.updated_at,
                  decision_count=excluded.decision_count,
                  blocked_count=excluded.blocked_count,
                  approval_required_count=excluded.approval_required_count,
                  payload=excluded.payload
                """,
                _session_row(record),
            )


def _decision_row(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        record["decision_id"],
        record["session_id"],
        record["agent_id"],
        record["actor"],
        record["repository"],
        record["policy_pack"],
        record["action_type"],
        record["target"],
        record["rule_id"],
        record["decision"],
        record["severity"],
        record["timestamp"],
        record["correlation_id"],
        json.dumps(record, sort_keys=True),
    )


def _session_row(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        record["session_id"],
        record["agent_id"],
        record["actor"],
        record["repository"],
        record["policy_pack"],
        record["state"],
        record["started_at"],
        record["updated_at"],
        record["decision_count"],
        record["blocked_count"],
        record["approval_required_count"],
        json.dumps(record, sort_keys=True),
    )


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


def _summarize_session_records(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_sessions": len(items),
        "total_decisions": sum(int(item.get("decision_count", 0)) for item in items),
        "total_blocked": sum(int(item.get("blocked_count", 0)) for item in items),
        "total_approval_required": sum(int(item.get("approval_required_count", 0)) for item in items),
        "latest_session_at": max((str(item.get("updated_at", "")) for item in items if item.get("updated_at")), default=None),
    }


def _session_payload_from_decision(decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": decision.get("session_id"),
        "agent_id": decision.get("agent_id"),
        "actor": decision.get("actor"),
        "repository": decision.get("repository"),
        "policy_pack": decision.get("policy_pack"),
    }


def _first_value(items: list[dict[str, Any]], key: str, default: str) -> Any:
    return next((item.get(key) for item in items if item.get(key)), default)


def _count_decisions(items: list[dict[str, Any]], decision: str) -> int:
    return sum(1 for item in items if item.get("decision") == decision)


def _session_evidence_refs(decisions: list[dict[str, Any]]) -> list[str]:
    refs: list[str] = []
    for decision in decisions:
        for ref in decision.get("evidence_refs", []):
            if ref not in refs:
                refs.append(ref)
    return refs


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    raise ValueError("expected a string or list of strings")
