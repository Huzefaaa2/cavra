from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_github_actions_recurrence_automation_template_is_dry_run_by_default() -> None:
    path = ROOT / "examples/github-actions/cavra-recurrence-automation.yml"
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    triggers = workflow.get("on") or workflow.get(True)

    assert triggers["schedule"][0]["cron"] == "*/30 * * * *"
    assert triggers["workflow_dispatch"]["inputs"]["execute"]["default"] == "false"
    steps = workflow["jobs"]["recurrence-automation"]["steps"]
    dry_run_step = next(step for step in steps if step.get("name") == "Run recurrence automation in dry-run mode")
    execute_step = next(step for step in steps if step.get("name") == "Run recurrence automation in guarded execute mode")

    assert "--dry-run" in dry_run_step["run"]
    assert "--execute" in execute_step["run"]
    assert "secrets.CAVRA_CONNECTORS_JSON" in str(steps)


def test_kubernetes_recurrence_automation_cronjob_is_public_safe() -> None:
    path = ROOT / "examples/kubernetes/cavra-recurrence-automation-cronjob.yaml"
    cronjob = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert cronjob["kind"] == "CronJob"
    assert cronjob["spec"]["schedule"] == "*/30 * * * *"
    assert cronjob["spec"]["concurrencyPolicy"] == "Forbid"
    container = cronjob["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]
    env = {item["name"]: item["value"] for item in container["env"]}
    connector_volume = cronjob["spec"]["jobTemplate"]["spec"]["template"]["spec"]["volumes"][1]

    assert env["CAVRA_RECURRENCE_EXECUTE"] == "false"
    assert "--dry-run" in container["command"][-1]
    assert "--execute" in container["command"][-1]
    assert connector_volume["secret"]["optional"] is True


def test_systemd_recurrence_automation_timer_defaults_to_dry_run() -> None:
    env_path = ROOT / "examples/systemd/cavra-recurrence-automation.env.example"
    service_path = ROOT / "examples/systemd/cavra-recurrence-automation.service"
    timer_path = ROOT / "examples/systemd/cavra-recurrence-automation.timer"

    env_text = env_path.read_text(encoding="utf-8")
    service_text = service_path.read_text(encoding="utf-8")
    timer_text = timer_path.read_text(encoding="utf-8")

    assert "CAVRA_RECURRENCE_EXECUTE=false" in env_text
    assert "--dry-run" in service_text
    assert "--execute" in service_text
    assert "StateDirectory=cavra" in service_text
    assert "NoNewPrivileges=true" in service_text
    assert "OnUnitActiveSec=30min" in timer_text
