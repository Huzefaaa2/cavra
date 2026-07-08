from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_live_validation_plan import (
    REQUIRED_VALIDATION_STAGES,
    build_managed_enterprise_live_validation_plan,
    validate_managed_enterprise_live_validation_plan,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_managed_enterprise_live_validation_plan_warns_without_blocking_shape() -> None:
    plan = build_managed_enterprise_live_validation_plan(evidence_mode="sample")

    result = validate_managed_enterprise_live_validation_plan(plan)

    assert result["ready_for_managed_enterprise_live_validation"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["stage_count"] == len(REQUIRED_VALIDATION_STAGES)


def test_live_managed_enterprise_live_validation_plan_is_ready() -> None:
    plan = build_managed_enterprise_live_validation_plan(evidence_mode="live")

    result = validate_managed_enterprise_live_validation_plan(plan, require_live=True)

    assert result["ready_for_managed_enterprise_live_validation"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["stage_count"] == result["required_stage_count"]


def test_require_live_rejects_sample_managed_enterprise_live_validation_plan() -> None:
    plan = build_managed_enterprise_live_validation_plan(evidence_mode="sample")

    result = validate_managed_enterprise_live_validation_plan(plan, require_live=True)

    assert result["ready_for_managed_enterprise_live_validation"] is False
    assert result["blocker_count"] == 1


def test_missing_validation_stage_blocks_readiness() -> None:
    plan = build_managed_enterprise_live_validation_plan(evidence_mode="live")
    plan["validation_stages"] = [
        stage
        for stage in plan["validation_stages"]
        if stage["stage_id"] != "smtp_report_delivery"
    ]

    result = validate_managed_enterprise_live_validation_plan(plan, require_live=True)

    assert result["ready_for_managed_enterprise_live_validation"] is False
    assert result["blocker_count"] == 1
    validation_stage_check = next(check for check in result["checks"] if check["name"] == "validation_stages")
    assert "smtp_report_delivery" in validation_stage_check["message"]


def test_wrong_ready_flag_blocks_readiness() -> None:
    plan = build_managed_enterprise_live_validation_plan(evidence_mode="live")
    plan["validation_stages"][0]["ready_flag"] = "ready_for_wrong_gate"

    result = validate_managed_enterprise_live_validation_plan(plan, require_live=True)

    assert result["ready_for_managed_enterprise_live_validation"] is False
    assert result["blocker_count"] == 1


def test_unsafe_ref_blocks_readiness() -> None:
    plan = build_managed_enterprise_live_validation_plan(evidence_mode="live")
    plan["validation_stages"][0]["result_ref"] = "https://example.com/raw-result"

    result = validate_managed_enterprise_live_validation_plan(plan, require_live=True)

    assert result["ready_for_managed_enterprise_live_validation"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_readiness() -> None:
    plan = build_managed_enterprise_live_validation_plan(evidence_mode="live")
    plan["smtp_password"] = "do-not-commit"

    result = validate_managed_enterprise_live_validation_plan(plan, require_live=True)

    assert result["ready_for_managed_enterprise_live_validation"] is False
    assert result["blocker_count"] == 1


def test_managed_enterprise_live_validation_plan_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-live-validation"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_live_validation_plan.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_plan = export_dir / "managed-enterprise-live-validation-plan.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_live_validation_plan.py",
            "--plan",
            str(live_plan),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_managed_enterprise_live_validation_plan_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-live-validation"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-live-validation-plan",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_plan = export_dir / "managed-enterprise-live-validation-plan.live.sanitized.example.json"
    assert live_plan.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-live-validation-plan",
            "--plan",
            str(live_plan),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_live_validation": true' in validate_result.output


def test_managed_enterprise_live_validation_plan_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_plan = tmp_path / "sample-plan.json"
    sample_plan.write_text(
        json.dumps(build_managed_enterprise_live_validation_plan(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-live-validation-plan",
            "--plan",
            str(sample_plan),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
