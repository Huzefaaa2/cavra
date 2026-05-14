from pathlib import Path

from terraguard_agentshield.audit import AuditAction, SessionAudit, create_attestation_markdown
from terraguard_agentshield.integrations import (
    CommandInterceptor,
    GitHubPRAttestationExporter,
)
from terraguard_agentshield.policy_registry import PolicyRegistry
from terraguard_agentshield.runtime import RuntimeGuard


def test_command_interceptor_blocks_terraform_apply() -> None:
    root = Path(__file__).resolve().parents[1] / "policies"
    registry = PolicyRegistry(root=root)
    guard = RuntimeGuard(policy_pack="ai-agent-baseline")

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
    assert "TerraGuard AgentShield Governance Report" in markdown
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
    assert artifact_path.name.startswith("agentshield-attestation-")

    import json

    content = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert content["session_id"] == "test-002"
    assert len(content["actions"]) == 1
