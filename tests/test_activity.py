from __future__ import annotations

from pathlib import Path

from cavra.activity import ActivityStore, SQLiteActivityStore
from cavra.tenancy import TenantScope


def _decision(
    session_id: str = "session-1",
    decision: str = "allow",
    *,
    tenant_id: str | None = None,
    workspace_id: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "decision_id": f"dec-{session_id}-{decision}",
        "session_id": session_id,
        "agent_id": "codex-agent",
        "actor": "codex-agent",
        "repository": "payments/api",
        "action_type": "execute_command",
        "target": "pytest",
        "requested_operation": "pytest",
        "policy_pack": "cavra-ai-agent-baseline",
        "rule_id": "commands.allow",
        "decision": decision,
        "severity": "low" if decision == "allow" else "high",
        "timestamp": "2026-05-18T00:00:00+00:00",
    }
    if tenant_id:
        payload["tenant_id"] = tenant_id
    if workspace_id:
        payload["workspace_id"] = workspace_id
    return payload


def test_activity_store_persists_decisions_and_session_summary(tmp_path: Path) -> None:
    store = ActivityStore(tmp_path / "activity.json")

    store.upsert_decision(_decision())
    store.upsert_decision(_decision(decision="block") | {"rule_id": "commands.block", "severity": "high"})

    sessions = store.list_sessions(repository="payments/api")
    decisions = store.list_decisions(session_id="session-1", decision="block")

    assert sessions["total"] == 1
    assert sessions["items"][0]["decision_count"] == 2
    assert sessions["items"][0]["blocked_count"] == 1
    assert decisions["total"] == 1
    assert store.get_decision("dec-session-1-block")["decision"] == "block"


def test_sqlite_activity_store_filters_decisions_and_sessions(tmp_path: Path) -> None:
    store = SQLiteActivityStore(tmp_path / "activity.db")

    store.upsert_decision(_decision())
    store.upsert_decision(_decision("session-2", "require_approval") | {"severity": "high", "approver_group": "Platform Security"})
    store.upsert_session({"session_id": "session-2", "state": "completed"})

    sessions = store.list_sessions(state="completed")
    approvals = store.list_decisions(decision="require_approval", repository="payments/api")

    assert sessions["total"] == 1
    assert sessions["items"][0]["session_id"] == "session-2"
    assert approvals["total"] == 1
    assert store.get_session("session-2")["approval_required_count"] == 1


def test_activity_store_filters_by_tenant_workspace_scope(tmp_path: Path) -> None:
    store = ActivityStore(tmp_path / "activity.json")

    store.upsert_decision(_decision("tenant-a-prod", tenant_id="tenant-a", workspace_id="prod"))
    store.upsert_decision(_decision("tenant-a-dev", tenant_id="tenant-a", workspace_id="dev"))
    store.upsert_decision(_decision("tenant-b-prod", tenant_id="tenant-b", workspace_id="prod"))

    tenant_a = store.list_decisions(tenant_id="tenant-a")
    prod = store.list_decisions_for_scope(TenantScope("tenant-a", "prod"))
    sessions = store.list_sessions_for_scope(TenantScope("tenant-b", "prod"))
    summary = store.summarize_sessions_for_scope(TenantScope("tenant-a"))

    assert tenant_a["total"] == 2
    assert prod["total"] == 1
    assert prod["items"][0]["session_id"] == "tenant-a-prod"
    assert sessions["total"] == 1
    assert sessions["items"][0]["tenant_id"] == "tenant-b"
    assert summary["total_sessions"] == 2


def test_sqlite_activity_store_filters_by_tenant_workspace_scope(tmp_path: Path) -> None:
    store = SQLiteActivityStore(tmp_path / "activity.db")

    store.upsert_decision(_decision("tenant-a-prod", tenant_id="tenant-a", workspace_id="prod"))
    store.upsert_decision(_decision("tenant-a-dev", tenant_id="tenant-a", workspace_id="dev"))
    store.upsert_decision(_decision("tenant-b-prod", tenant_id="tenant-b", workspace_id="prod"))

    tenant_a = store.list_decisions(tenant_id="tenant-a")
    prod = store.list_decisions_for_scope(TenantScope("tenant-a", "prod"))
    sessions = store.list_sessions_for_scope(TenantScope("tenant-b", "prod"))
    summary = store.summarize_sessions_for_scope(TenantScope("tenant-a"))

    assert tenant_a["total"] == 2
    assert prod["total"] == 1
    assert prod["items"][0]["session_id"] == "tenant-a-prod"
    assert sessions["total"] == 1
    assert sessions["items"][0]["tenant_id"] == "tenant-b"
    assert summary["total_sessions"] == 2
