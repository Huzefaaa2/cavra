from pathlib import Path

from cavra.audit import AuditAction, SessionAudit
from cavra.integrations import (
    CommandInterceptor,
    GitHubPRAttestationExporter,
    IntegrationStore,
    SQLiteIntegrationStore,
)
from cavra.runtime import RuntimeGuard


def test_command_interceptor_blocks_terraform_apply() -> None:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")

    session = SessionAudit(session_id="test-001", tool="claude-code", repo=Path("."))
    interceptor = CommandInterceptor(guard, session)

    result = interceptor.execute("terraform apply -auto-approve")
    assert not result.success
    assert "blocked" in result.error.lower()
    assert len(session.actions) == 1
    assert session.actions[0].decision == "block"


def test_github_attestation_export() -> None:
    session = SessionAudit(session_id="test-001", tool="claude-code", repo=Path("."))
    session.add_action(
        AuditAction(type="execute_command", target="terraform apply", decision="block")
    )
    session.add_action(
        AuditAction(type="read_file", target=".env", decision="block")
    )

    markdown = GitHubPRAttestationExporter.export_comment(session)
    assert "CAVRA PR Attestation" in markdown
    assert "Blocked Actions" in markdown
    assert "terraform apply" in markdown
    assert ".env" in markdown


def test_attestation_artifact_export(tmp_path: Path) -> None:
    session = SessionAudit(session_id="test-002", tool="claude-code", repo=Path("."))
    session.add_action(
        AuditAction(type="execute_command", target="terraform plan", decision="allow")
    )

    artifact_path = GitHubPRAttestationExporter.save_artifact(session, tmp_path)
    assert artifact_path.exists()
    assert artifact_path.name.startswith("cavra-attestation-")

    import json

    content = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert content["session_id"] == "test-002"
    assert len(content["actions"]) == 1


def _integration() -> dict[str, object]:
    return {
        "integration_id": "github-enterprise",
        "provider": "github",
        "name": "GitHub Enterprise",
        "category": "source_control",
        "status": "active",
        "health_status": "healthy",
        "owner": "Developer Platform",
        "environment": "production",
        "auth_mode": "github_app",
        "capabilities": ["pull_request", "required_check"],
        "repositories": ["payments/api"],
    }


def test_integration_store_persists_and_filters_records(tmp_path: Path) -> None:
    store = IntegrationStore(tmp_path / "integrations.json")

    record = store.upsert_integration(_integration())
    store.upsert_integration(
        {**_integration(), "integration_id": "splunk", "provider": "splunk", "category": "siem", "owner": "SOC"}
    )

    assert record["integration_id"] == "github-enterprise"
    assert store.list_integrations(category="source_control")["total"] == 1
    assert store.list_integrations(owner="SOC")["items"][0]["provider"] == "splunk"
    assert store.get_integration("github-enterprise")["health_status"] == "healthy"


def test_sqlite_integration_store_filters_records(tmp_path: Path) -> None:
    store = SQLiteIntegrationStore(tmp_path / "integrations.db")

    store.upsert_integration(_integration())
    store.upsert_integration(
        {
            **_integration(),
            "integration_id": "jira",
            "provider": "jira",
            "category": "itsm",
            "health_status": "degraded",
        }
    )

    assert store.list_integrations(provider="github")["total"] == 1
    assert store.list_integrations(health_status="degraded")["items"][0]["provider"] == "jira"
    assert store.get_integration("jira")["category"] == "itsm"
