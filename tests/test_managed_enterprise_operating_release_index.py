from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_operating_release_index import (
    REQUIRED_OPERATING_GATES,
    build_managed_enterprise_operating_release_index,
    validate_managed_enterprise_operating_release_index,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_operating_release_index_warns_without_blocking_shape() -> None:
    index = build_managed_enterprise_operating_release_index(evidence_mode="sample")

    result = validate_managed_enterprise_operating_release_index(index)

    assert result["ready_for_managed_enterprise_operating_release"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["gate_count"] == len(REQUIRED_OPERATING_GATES)


def test_live_operating_release_index_is_ready() -> None:
    index = build_managed_enterprise_operating_release_index(evidence_mode="live")

    result = validate_managed_enterprise_operating_release_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_operating_release"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["gate_count"] == result["required_gate_count"]


def test_require_live_rejects_sample_operating_release_index() -> None:
    index = build_managed_enterprise_operating_release_index(evidence_mode="sample")

    result = validate_managed_enterprise_operating_release_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_operating_release"] is False
    assert result["blocker_count"] == 1


def test_missing_operating_gate_blocks_readiness() -> None:
    index = build_managed_enterprise_operating_release_index(evidence_mode="live")
    index["operating_gates"] = [
        gate
        for gate in index["operating_gates"]
        if gate["gate_id"] != "steady_state_handoff"
    ]

    result = validate_managed_enterprise_operating_release_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_operating_release"] is False
    assert result["blocker_count"] == 1
    gate_check = next(check for check in result["checks"] if check["name"] == "operating_gates")
    assert "steady_state_handoff" in gate_check["message"]


def test_unsafe_operating_release_reference_blocks_readiness() -> None:
    index = build_managed_enterprise_operating_release_index(evidence_mode="live")
    index["operating_release_outcome"]["support_owner_ref"] = "https://example.com/raw-owner"

    result = validate_managed_enterprise_operating_release_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_operating_release"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_operating_release_readiness() -> None:
    index = build_managed_enterprise_operating_release_index(evidence_mode="live")
    index["private_release_notes"] = ["do-not-commit"]

    result = validate_managed_enterprise_operating_release_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_operating_release"] is False
    assert result["blocker_count"] == 1


def test_operating_release_index_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-operating-release"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_operating_release_index.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_index = export_dir / "managed-enterprise-operating-release-index.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_operating_release_index.py",
            "--index",
            str(live_index),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_operating_release_index_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-operating-release"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-release-index",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_index = export_dir / "managed-enterprise-operating-release-index.live.sanitized.example.json"
    assert live_index.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-release-index",
            "--index",
            str(live_index),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_operating_release": true' in validate_result.output


def test_operating_release_index_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_index = tmp_path / "sample-index.json"
    sample_index.write_text(
        json.dumps(build_managed_enterprise_operating_release_index(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-release-index",
            "--index",
            str(sample_index),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
