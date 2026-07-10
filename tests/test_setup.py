from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient
from typer.testing import CliRunner

from cavra.api import create_app
from cavra.cli import app
from cavra.setup import (
    bootstrap_setup,
    build_policy_action_catalog,
    create_demo_workspace,
    plan_policy_action_change,
    setup_status,
    smtp_test_plan,
    validate_setup,
)


runner = CliRunner()


def test_setup_bootstrap_demo_workspace_and_validation(monkeypatch, tmp_path: Path) -> None:
    state_path = tmp_path / "setup-state.json"
    demo_path = tmp_path / "demo-workspace"
    monkeypatch.setenv("CAVRA_SETUP_STATE_STORE", str(state_path))

    bootstrap = bootstrap_setup(workspace_name="pytest-workspace")
    demo = create_demo_workspace(demo_path)
    validation = validate_setup()
    status = setup_status()

    assert bootstrap["status"] == "created"
    assert state_path.exists()
    assert demo_path.joinpath(".env").exists()
    assert demo_path.joinpath("iam/admin-role.tf").exists()
    assert demo["schema_version"] == "cavra.demo-workspace.v1"
    assert validation["status"] in {"ready", "needs_attention"}
    assert validation["summary"]["scenario_pass_count"] == validation["summary"]["scenario_count"]
    assert status["configured"] is True
    assert status["policy"]["available"] is True


def test_smtp_test_plan_never_requires_password_value() -> None:
    result = smtp_test_plan(
        {
            "host": "smtp.example.invalid",
            "port": 587,
            "from_email": "hello@example.invalid",
            "recipient_allowlist": ["security@example.invalid"],
            "password_ref": "CAVRA_REPORT_SMTP_PASSWORD",
        }
    )

    assert result["status"] == "ready"
    assert result["configuration"]["password_ref"] == "CAVRA_REPORT_SMTP_PASSWORD"
    assert "password_value" not in json.dumps(result).lower()


def test_policy_action_catalog_and_change_plan() -> None:
    catalog = build_policy_action_catalog("cavra-ai-agent-baseline")
    plan = plan_policy_action_change(
        {"operation": "add", "section": "commands", "action": "block", "value": "rm -rf /"},
        policy_pack="cavra-ai-agent-baseline",
    )

    assert catalog["total"] > 0
    assert any(item["section"] == "commands" and item["action"] == "block" for item in catalog["items"])
    assert plan["publish_required"] is True
    assert plan["draft"]["valid"] is True
    assert "rm -rf /" in plan["draft"]["policy_pack"]["commands"]["block"]


def test_setup_cli_init_demo_validate_and_policy_actions(monkeypatch, tmp_path: Path) -> None:
    state_path = tmp_path / "setup-state.json"
    activity_path = tmp_path / "activity.json"
    demo_path = tmp_path / "demo-workspace"
    monkeypatch.setenv("CAVRA_SETUP_STATE_STORE", str(state_path))

    init_result = runner.invoke(app, ["setup", "init", "--workspace-name", "cli-test"])
    demo_result = runner.invoke(app, ["setup", "demo-env", "--output", str(demo_path)])
    validate_result = runner.invoke(
        app,
        ["setup", "validate", "--record-decisions", "--activity-store", str(activity_path)],
    )
    catalog_result = runner.invoke(app, ["setup", "policy-actions"])
    action_test_result = runner.invoke(
        app,
        ["setup", "policy-action-test", "--action-type", "execute_command", "--target", "terraform apply -auto-approve"],
    )
    action_plan_result = runner.invoke(
        app,
        [
            "setup",
            "policy-action-plan",
            "--operation",
            "add",
            "--section",
            "commands",
            "--action",
            "block",
            "--value",
            "rm -rf /",
        ],
    )

    assert init_result.exit_code == 0, init_result.output
    assert demo_result.exit_code == 0, demo_result.output
    assert validate_result.exit_code == 0, validate_result.output
    assert catalog_result.exit_code == 0, catalog_result.output
    assert action_test_result.exit_code == 0, action_test_result.output
    assert action_plan_result.exit_code == 0, action_plan_result.output
    assert demo_path.joinpath(".env").exists()
    assert activity_path.exists()
    assert json.loads(catalog_result.output)["schema_version"] == "cavra.policy-action-catalog.v1"
    assert json.loads(action_test_result.output)["decision"]["decision"] == "block"
    assert json.loads(action_plan_result.output)["publish_required"] is True


def test_setup_api_endpoints(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CAVRA_SETUP_STATE_STORE", str(tmp_path / "setup-state.json"))
    monkeypatch.setenv("CAVRA_ACTIVITY_STORE", str(tmp_path / "activity.json"))
    client = TestClient(create_app())

    config = client.get("/console/config").json()
    bootstrap = client.post("/setup/bootstrap", json={"workspace_name": "api-test"})
    demo = client.post("/setup/demo-workspace", json={"output": str(tmp_path / "demo-workspace")})
    validation = client.post("/setup/validate", json={"record_decisions": True, "session_id": "api-setup-validation"})
    posture = client.get("/aispm/posture")
    smtp = client.post(
        "/setup/smtp/test",
        json={
            "host": "smtp.example.invalid",
            "from_email": "hello@example.invalid",
            "recipient_allowlist": ["security@example.invalid"],
            "password_ref": "CAVRA_REPORT_SMTP_PASSWORD",
        },
    )
    catalog = client.get("/policy-action-catalog")
    plan = client.post(
        "/policy-action-catalog",
        json={"section": "commands", "action": "block", "value": "rm -rf /"},
    )
    action_test = client.post(
        "/policy-action-catalog/test",
        json={"action_type": "execute_command", "target": "terraform apply -auto-approve"},
    )

    assert config["endpoints"]["setup_status"] == "/setup/status"
    assert bootstrap.status_code == 200
    assert bootstrap.json()["status"] == "created"
    assert demo.status_code == 200
    assert validation.status_code == 200
    assert validation.json()["summary"]["scenario_pass_count"] == validation.json()["summary"]["scenario_count"]
    assert posture.json()["overview"]["blocked_actions"] >= 1
    assert smtp.json()["status"] == "ready"
    assert catalog.json()["total"] > 0
    assert plan.json()["publish_required"] is True
    assert action_test.json()["decision"]["decision"] == "block"
