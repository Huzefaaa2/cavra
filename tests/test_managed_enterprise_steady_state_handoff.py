from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_steady_state_handoff import (
    REQUIRED_HANDOFF_AREAS,
    build_managed_enterprise_steady_state_handoff,
    validate_managed_enterprise_steady_state_handoff,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_steady_state_handoff_warns_without_blocking_shape() -> None:
    handoff = build_managed_enterprise_steady_state_handoff(evidence_mode="sample")

    result = validate_managed_enterprise_steady_state_handoff(handoff)

    assert result["ready_for_managed_enterprise_steady_state"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["area_count"] == len(REQUIRED_HANDOFF_AREAS)


def test_live_steady_state_handoff_is_ready() -> None:
    handoff = build_managed_enterprise_steady_state_handoff(evidence_mode="live")

    result = validate_managed_enterprise_steady_state_handoff(handoff, require_live=True)

    assert result["ready_for_managed_enterprise_steady_state"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["area_count"] == result["required_area_count"]


def test_require_live_rejects_sample_steady_state_handoff() -> None:
    handoff = build_managed_enterprise_steady_state_handoff(evidence_mode="sample")

    result = validate_managed_enterprise_steady_state_handoff(handoff, require_live=True)

    assert result["ready_for_managed_enterprise_steady_state"] is False
    assert result["blocker_count"] == 1


def test_missing_handoff_area_blocks_readiness() -> None:
    handoff = build_managed_enterprise_steady_state_handoff(evidence_mode="live")
    handoff["handoff_areas"] = [
        area
        for area in handoff["handoff_areas"]
        if area["area_id"] != "aispm_operations"
    ]

    result = validate_managed_enterprise_steady_state_handoff(handoff, require_live=True)

    assert result["ready_for_managed_enterprise_steady_state"] is False
    assert result["blocker_count"] == 1
    area_check = next(check for check in result["checks"] if check["name"] == "handoff_areas")
    assert "aispm_operations" in area_check["message"]


def test_unsafe_steady_state_reference_blocks_readiness() -> None:
    handoff = build_managed_enterprise_steady_state_handoff(evidence_mode="live")
    handoff["steady_state_outcome"]["support_owner_ref"] = "https://example.com/raw-owner"

    result = validate_managed_enterprise_steady_state_handoff(handoff, require_live=True)

    assert result["ready_for_managed_enterprise_steady_state"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_steady_state_readiness() -> None:
    handoff = build_managed_enterprise_steady_state_handoff(evidence_mode="live")
    handoff["raw_contracts"] = ["do-not-commit"]

    result = validate_managed_enterprise_steady_state_handoff(handoff, require_live=True)

    assert result["ready_for_managed_enterprise_steady_state"] is False
    assert result["blocker_count"] == 1


def test_steady_state_handoff_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-steady-state"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_steady_state_handoff.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_handoff = export_dir / "managed-enterprise-steady-state-handoff.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_steady_state_handoff.py",
            "--handoff",
            str(live_handoff),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_steady_state_handoff_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-steady-state"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-steady-state-handoff",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_handoff = export_dir / "managed-enterprise-steady-state-handoff.live.sanitized.example.json"
    assert live_handoff.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-steady-state-handoff",
            "--handoff",
            str(live_handoff),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_steady_state": true' in validate_result.output


def test_steady_state_handoff_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_handoff = tmp_path / "sample-handoff.json"
    sample_handoff.write_text(
        json.dumps(build_managed_enterprise_steady_state_handoff(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-steady-state-handoff",
            "--handoff",
            str(sample_handoff),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
