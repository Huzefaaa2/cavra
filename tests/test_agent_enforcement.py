from __future__ import annotations

import json
from pathlib import Path

from cavra.agent_enforcement import agent_enforcement_readiness_report


def _write_repo_baseline(root: Path, *, workflow_text: str | None = None) -> None:
    workflow_dir = root / ".github" / "workflows"
    workflow_dir.mkdir(parents=True)
    (root / ".github" / "agents").mkdir(parents=True)
    (root / ".github" / "agents" / "backend-agent.yml").write_text("name: backend-agent\n", encoding="utf-8")
    (root / ".github" / "pull_request_template.md").write_text("CAVRA evidence required.\n", encoding="utf-8")
    (root / ".github" / "CODEOWNERS").write_text("* @platform-security\n", encoding="utf-8")
    (root / "policies" / "cavra-agentic-delivery").mkdir(parents=True)
    (root / "policies" / "cavra-agentic-delivery" / "policy.yaml").write_text(
        "id: cavra-agentic-delivery\n",
        encoding="utf-8",
    )
    (workflow_dir / "cavra-governance.yml").write_text(
        workflow_text
        or """
name: AI Agent Governance Check
jobs:
  cavra:
    name: cavra-required-check
    steps:
      - name: Upload required-check evidence
        with:
          name: cavra-required-check-evidence
""",
        encoding="utf-8",
    )


def _ready_settings() -> dict[str, object]:
    return {
        "provider": "github",
        "repository": "Huzefaaa2/cavra",
        "protected_branch": "main",
        "branch_protection": {
            "pull_request_required": True,
            "required_reviews": 1,
            "dismiss_stale_reviews": True,
            "conversation_resolution_required": True,
            "restricted_pushes": True,
            "force_pushes_allowed": False,
            "deletions_allowed": False,
            "bypass_allowed": False,
        },
        "required_checks": ["cavra-required-check", "Test"],
        "security_checks": ["CodeQL"],
    }


def test_agent_enforcement_readiness_reports_ready_with_required_controls(tmp_path: Path) -> None:
    _write_repo_baseline(tmp_path)

    report = agent_enforcement_readiness_report(repo_root=tmp_path, settings=_ready_settings())

    assert report["schema_version"] == "cavra.agent-enforcement-readiness.v1"
    assert report["status"] == "ready"
    assert report["summary"]["failed_count"] == 0
    assert any(check["id"] == "branch_bypass_disabled" and check["status"] == "pass" for check in report["checks"])


def test_agent_enforcement_readiness_blocks_missing_required_workflow(tmp_path: Path) -> None:
    _write_repo_baseline(tmp_path)
    (tmp_path / ".github" / "workflows" / "cavra-governance.yml").unlink()

    report = agent_enforcement_readiness_report(repo_root=tmp_path, settings=_ready_settings())

    assert report["status"] == "blocked"
    assert any(check["id"] == "required_check_workflow" and check["status"] == "fail" for check in report["checks"])


def test_agent_enforcement_readiness_warns_without_external_branch_settings(tmp_path: Path) -> None:
    _write_repo_baseline(tmp_path)

    report = agent_enforcement_readiness_report(repo_root=tmp_path)

    assert report["status"] == "needs_attention"
    assert any(check["id"] == "branch_protection_settings" and check["status"] == "warn" for check in report["checks"])


def test_agent_enforcement_readiness_blocks_write_all_workflow_permission(tmp_path: Path) -> None:
    _write_repo_baseline(
        tmp_path,
        workflow_text="""
name: AI Agent Governance Check
permissions: write-all
jobs:
  cavra:
    name: cavra-required-check
    steps:
      - name: Upload required-check evidence
        with:
          name: cavra-required-check-evidence
""",
    )

    report = agent_enforcement_readiness_report(repo_root=tmp_path, settings=_ready_settings())

    assert report["status"] == "blocked"
    assert any(
        check["id"] == "workflow_permission_write_all:cavra-governance.yml" and check["status"] == "fail"
        for check in report["checks"]
    )


def test_agent_enforcement_readiness_loads_settings_file(tmp_path: Path) -> None:
    _write_repo_baseline(tmp_path)
    settings_path = tmp_path / "agent-enforcement-settings.json"
    settings_path.write_text(json.dumps(_ready_settings()), encoding="utf-8")

    report = agent_enforcement_readiness_report(repo_root=tmp_path, settings_path=settings_path)

    assert report["status"] == "ready"
