from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.roadmap_future_work_governance_index import (
    build_roadmap_future_work_governance_index,
    validate_roadmap_future_work_governance_index,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_roadmap_future_work_governance_index_warns_without_blocking_shape() -> None:
    index = build_roadmap_future_work_governance_index(evidence_mode="sample")

    result = validate_roadmap_future_work_governance_index(index)

    assert result["ready_for_roadmap_future_work_governance_index"] is False
    assert result["decision"] == "ready_to_close_future_work_governance_chain"
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1
    assert result["source_gate_count"] == 4


def test_live_roadmap_future_work_governance_index_is_ready() -> None:
    index = build_roadmap_future_work_governance_index(evidence_mode="live")

    result = validate_roadmap_future_work_governance_index(index, require_live=True)

    assert result["ready_for_roadmap_future_work_governance_index"] is True
    assert result["decision"] == "ready_to_close_future_work_governance_chain"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_future_work_governance_index() -> None:
    index = build_roadmap_future_work_governance_index(evidence_mode="sample")

    result = validate_roadmap_future_work_governance_index(index, require_live=True)

    assert result["ready_for_roadmap_future_work_governance_index"] is False
    assert result["blocker_count"] >= 1


def test_operating_evidence_cannot_close_future_work_governance_index() -> None:
    index = build_roadmap_future_work_governance_index(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )

    result = validate_roadmap_future_work_governance_index(index, require_live=True)

    assert result["ready_for_roadmap_future_work_governance_index"] is False
    assert result["blocker_count"] >= 1
    source_check = next(check for check in result["checks"] if check["name"] == "source_results")
    assert "roadmap_intake_gate" in source_check["message"]


def test_unsafe_governance_control_reference_blocks_future_work_governance_index() -> None:
    index = build_roadmap_future_work_governance_index(evidence_mode="live")
    index["governance_controls"]["release_guard_ref"] = "https://example.com/private"

    result = validate_roadmap_future_work_governance_index(index, require_live=True)

    assert result["ready_for_roadmap_future_work_governance_index"] is False
    assert result["blocker_count"] == 1


def test_non_ready_governance_decision_blocks_future_work_governance_index() -> None:
    index = build_roadmap_future_work_governance_index(evidence_mode="live")
    index["governance_decision"]["governance_decision"] = "rejected_to_prior_gate"

    result = validate_roadmap_future_work_governance_index(index, require_live=True)

    assert result["ready_for_roadmap_future_work_governance_index"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_future_work_governance_index() -> None:
    index = build_roadmap_future_work_governance_index(evidence_mode="live")
    index["token"] = "do-not-commit"

    result = validate_roadmap_future_work_governance_index(index, require_live=True)

    assert result["ready_for_roadmap_future_work_governance_index"] is False
    assert result["blocker_count"] == 1


def test_roadmap_future_work_governance_index_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-future-work-governance-index"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_future_work_governance_index.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_index = export_dir / "roadmap-future-work-governance-index.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_future_work_governance_index.py",
            "--index",
            str(live_index),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_roadmap_future_work_governance_index_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-future-work-governance-index"
    export_result = runner.invoke(
        app,
        ["release", "roadmap-future-work-governance-index", "--export-dir", str(export_dir)],
    )

    assert export_result.exit_code == 0, export_result.output
    live_index = export_dir / "roadmap-future-work-governance-index.live.sanitized.example.json"
    assert live_index.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "roadmap-future-work-governance-index",
            "--index",
            str(live_index),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_roadmap_future_work_governance_index": true' in validate_result.output


def test_roadmap_future_work_governance_index_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_index = tmp_path / "sample-index.json"
    sample_index.write_text(
        json.dumps(build_roadmap_future_work_governance_index(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "roadmap-future-work-governance-index",
            "--index",
            str(sample_index),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"ready_for_roadmap_future_work_governance_index": false' in result.output
