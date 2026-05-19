from pathlib import Path

from cavra.audit import AuditAction, SessionAudit
from cavra.integrations import (
    CommandInterceptor,
    GitHubPRAttestationExporter,
    IntegrationStore,
    SQLiteIntegrationStore,
    build_connector_request_specs,
    deliver_connector_event,
    export_connector_delivery_result,
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


def _connector_event() -> dict[str, object]:
    return {
        "event_type": "cavra.evidence_bundle",
        "product": "CAVRA",
        "session_id": "session-1",
        "decision_count": 3,
        "blocked_count": 1,
        "approval_required_count": 1,
        "max_severity": "high",
        "timestamp": "2026-05-18T00:00:00+00:00",
        "decisions": [],
    }


def test_connector_request_specs_build_vendor_payloads_and_headers(monkeypatch) -> None:
    monkeypatch.setenv("SPLUNK_TOKEN", "splunk-secret")
    monkeypatch.setenv("DATADOG_KEY", "datadog-secret")
    config = {
        "connectors": {
            "splunk": {"url": "https://splunk.example/services/collector", "token_env": "SPLUNK_TOKEN", "index": "cavra_prod"},
            "datadog": {
                "url": "https://http-intake.logs.datadoghq.com/api/v2/logs",
                "api_key_env": "DATADOG_KEY",
                "api_key_header": "dd-api-key",
                "service": "cavra-runtime",
            },
            "slack": {"url": "https://hooks.slack.com/services/T000/B000/SECRET"},
        }
    }

    specs = build_connector_request_specs(_connector_event(), config)

    assert specs["splunk"]["body"]["index"] == "cavra_prod"
    assert specs["splunk"]["headers"]["authorization"] == "Bearer splunk-secret"
    assert specs["datadog"]["body"]["events"][0]["service"] == "cavra-runtime"
    assert specs["datadog"]["headers"]["dd-api-key"] == "datadog-secret"
    assert specs["slack"]["body"]["blocks"][0]["type"] == "header"


def test_connector_request_specs_require_credentials_for_enterprise_providers() -> None:
    try:
        build_connector_request_specs(_connector_event(), {"connectors": {"servicenow": {"url": "https://snow.example/api/now/table/change_request"}}})
    except ValueError as exc:
        assert "must configure token_env" in str(exc)
    else:
        raise AssertionError("expected missing connector credentials to fail")


def test_deliver_connector_event_redacts_credentials_and_exports(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("JIRA_TOKEN", "jira-secret")
    calls = []

    def sender(spec, *, timeout_seconds):
        calls.append((spec, timeout_seconds))
        return {"status_code": 201, "body": "created"}

    result = deliver_connector_event(
        _connector_event(),
        {"connectors": {"jira": {"url": "https://jira.example/rest/api/3/issue?token=secret", "token_env": "JIRA_TOKEN"}}},
        provider="jira",
        retries=0,
        sender=sender,
    )
    output = export_connector_delivery_result(result, tmp_path)

    assert result["success"] is True
    assert result["event_id"] == "session-1"
    assert result["deliveries"][0]["request"]["headers"]["authorization"] == "REDACTED"
    assert result["deliveries"][0]["request"]["url"].endswith("?REDACTED")
    assert calls[0][0]["body"]["fields"]["labels"][0] == "cavra"
    assert output.exists()
