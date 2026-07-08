from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_stabilization_report import (
    REQUIRED_HEALTH_SIGNALS,
    build_managed_enterprise_stabilization_report,
    validate_managed_enterprise_stabilization_report,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_stabilization_report_warns_without_blocking_shape() -> None:
    report = build_managed_enterprise_stabilization_report(evidence_mode="sample")

    result = validate_managed_enterprise_stabilization_report(report)

    assert result["ready_for_managed_enterprise_stabilization_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["signal_count"] == len(REQUIRED_HEALTH_SIGNALS)


def test_live_stabilization_report_is_ready() -> None:
    report = build_managed_enterprise_stabilization_report(evidence_mode="live")

    result = validate_managed_enterprise_stabilization_report(report, require_live=True)

    assert result["ready_for_managed_enterprise_stabilization_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["signal_count"] == result["required_signal_count"]


def test_require_live_rejects_sample_stabilization_report() -> None:
    report = build_managed_enterprise_stabilization_report(evidence_mode="sample")

    result = validate_managed_enterprise_stabilization_report(report, require_live=True)

    assert result["ready_for_managed_enterprise_stabilization_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_health_signal_blocks_readiness() -> None:
    report = build_managed_enterprise_stabilization_report(evidence_mode="live")
    report["health_signals"] = [
        signal
        for signal in report["health_signals"]
        if signal["signal_id"] != "smtp_report_health"
    ]

    result = validate_managed_enterprise_stabilization_report(report, require_live=True)

    assert result["ready_for_managed_enterprise_stabilization_closeout"] is False
    assert result["blocker_count"] == 1
    signal_check = next(check for check in result["checks"] if check["name"] == "health_signals")
    assert "smtp_report_health" in signal_check["message"]


def test_unsafe_stabilization_reference_blocks_readiness() -> None:
    report = build_managed_enterprise_stabilization_report(evidence_mode="live")
    report["stabilization_outcome"]["customer_acceptance_ref"] = "https://example.com/raw-acceptance"

    result = validate_managed_enterprise_stabilization_report(report, require_live=True)

    assert result["ready_for_managed_enterprise_stabilization_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_stabilization_readiness() -> None:
    report = build_managed_enterprise_stabilization_report(evidence_mode="live")
    report["raw_logs"] = ["do-not-commit"]

    result = validate_managed_enterprise_stabilization_report(report, require_live=True)

    assert result["ready_for_managed_enterprise_stabilization_closeout"] is False
    assert result["blocker_count"] == 1


def test_stabilization_report_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-stabilization"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_stabilization_report.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_report = export_dir / "managed-enterprise-stabilization-report.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_stabilization_report.py",
            "--report",
            str(live_report),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_stabilization_report_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-stabilization"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-stabilization-report",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_report = export_dir / "managed-enterprise-stabilization-report.live.sanitized.example.json"
    assert live_report.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-stabilization-report",
            "--report",
            str(live_report),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_stabilization_closeout": true' in validate_result.output


def test_stabilization_report_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_report = tmp_path / "sample-report.json"
    sample_report.write_text(
        json.dumps(build_managed_enterprise_stabilization_report(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-stabilization-report",
            "--report",
            str(sample_report),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
