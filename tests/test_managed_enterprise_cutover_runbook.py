from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_cutover_runbook import (
    REQUIRED_CUTOVER_STEPS,
    build_managed_enterprise_cutover_runbook,
    validate_managed_enterprise_cutover_runbook,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_cutover_runbook_warns_without_blocking_shape() -> None:
    runbook = build_managed_enterprise_cutover_runbook(evidence_mode="sample")

    result = validate_managed_enterprise_cutover_runbook(runbook)

    assert result["ready_for_managed_enterprise_cutover"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["step_count"] == len(REQUIRED_CUTOVER_STEPS)


def test_live_cutover_runbook_is_ready() -> None:
    runbook = build_managed_enterprise_cutover_runbook(evidence_mode="live")

    result = validate_managed_enterprise_cutover_runbook(runbook, require_live=True)

    assert result["ready_for_managed_enterprise_cutover"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["step_count"] == result["required_step_count"]


def test_require_live_rejects_sample_cutover_runbook() -> None:
    runbook = build_managed_enterprise_cutover_runbook(evidence_mode="sample")

    result = validate_managed_enterprise_cutover_runbook(runbook, require_live=True)

    assert result["ready_for_managed_enterprise_cutover"] is False
    assert result["blocker_count"] == 1


def test_missing_cutover_step_blocks_readiness() -> None:
    runbook = build_managed_enterprise_cutover_runbook(evidence_mode="live")
    runbook["cutover_steps"] = [
        step
        for step in runbook["cutover_steps"]
        if step["step_id"] != "rollback_rehearsal"
    ]

    result = validate_managed_enterprise_cutover_runbook(runbook, require_live=True)

    assert result["ready_for_managed_enterprise_cutover"] is False
    assert result["blocker_count"] == 1
    cutover_check = next(check for check in result["checks"] if check["name"] == "cutover_steps")
    assert "rollback_rehearsal" in cutover_check["message"]


def test_unsafe_cutover_reference_blocks_readiness() -> None:
    runbook = build_managed_enterprise_cutover_runbook(evidence_mode="live")
    runbook["cutover_controls"]["go_no_go_ref"] = "https://example.com/private-approval"

    result = validate_managed_enterprise_cutover_runbook(runbook, require_live=True)

    assert result["ready_for_managed_enterprise_cutover"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_cutover_readiness() -> None:
    runbook = build_managed_enterprise_cutover_runbook(evidence_mode="live")
    runbook["smtp_password"] = "do-not-commit"

    result = validate_managed_enterprise_cutover_runbook(runbook, require_live=True)

    assert result["ready_for_managed_enterprise_cutover"] is False
    assert result["blocker_count"] == 1


def test_cutover_runbook_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-cutover"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_cutover_runbook.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_runbook = export_dir / "managed-enterprise-cutover-runbook.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_cutover_runbook.py",
            "--runbook",
            str(live_runbook),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_cutover_runbook_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-cutover"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-cutover-runbook",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_runbook = export_dir / "managed-enterprise-cutover-runbook.live.sanitized.example.json"
    assert live_runbook.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-cutover-runbook",
            "--runbook",
            str(live_runbook),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_cutover": true' in validate_result.output


def test_cutover_runbook_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_runbook = tmp_path / "sample-runbook.json"
    sample_runbook.write_text(
        json.dumps(build_managed_enterprise_cutover_runbook(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-cutover-runbook",
            "--runbook",
            str(sample_runbook),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
