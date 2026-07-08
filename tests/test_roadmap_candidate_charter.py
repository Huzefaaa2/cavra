from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.roadmap_candidate_charter import (
    REQUIRED_ACCEPTANCE_CRITERIA,
    build_roadmap_candidate_charter,
    validate_roadmap_candidate_charter,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_roadmap_candidate_charter_warns_without_blocking_shape() -> None:
    charter = build_roadmap_candidate_charter(evidence_mode="sample")

    result = validate_roadmap_candidate_charter(charter)

    assert result["ready_for_roadmap_candidate_charter"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["acceptance_criteria_count"] == len(REQUIRED_ACCEPTANCE_CRITERIA)


def test_live_roadmap_candidate_charter_is_ready() -> None:
    charter = build_roadmap_candidate_charter(evidence_mode="live")

    result = validate_roadmap_candidate_charter(charter, require_live=True)

    assert result["ready_for_roadmap_candidate_charter"] is True
    assert result["decision"] == "ready_for_product_roadmap_planning"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_candidate_charter() -> None:
    charter = build_roadmap_candidate_charter(evidence_mode="sample")

    result = validate_roadmap_candidate_charter(charter, require_live=True)

    assert result["ready_for_roadmap_candidate_charter"] is False
    assert result["blocker_count"] == 2


def test_operating_evidence_intake_cannot_receive_product_charter() -> None:
    charter = build_roadmap_candidate_charter(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )

    result = validate_roadmap_candidate_charter(charter, require_live=True)

    assert result["ready_for_roadmap_candidate_charter"] is False
    assert result["blocker_count"] >= 1
    intake_check = next(check for check in result["checks"] if check["name"] == "source_intake_result")
    assert "Only new_product_roadmap_candidate" in intake_check["message"]


def test_missing_acceptance_criterion_blocks_candidate_charter() -> None:
    charter = build_roadmap_candidate_charter(evidence_mode="live")
    charter["acceptance_criteria"] = [
        criterion
        for criterion in charter["acceptance_criteria"]
        if criterion["criterion_id"] != "release_gate_defined"
    ]

    result = validate_roadmap_candidate_charter(charter, require_live=True)

    assert result["ready_for_roadmap_candidate_charter"] is False
    assert result["blocker_count"] == 1
    criteria_check = next(check for check in result["checks"] if check["name"] == "acceptance_criteria")
    assert "release_gate_defined" in criteria_check["message"]


def test_undefined_acceptance_criterion_blocks_candidate_charter() -> None:
    charter = build_roadmap_candidate_charter(evidence_mode="live")
    charter["acceptance_criteria"][0]["status"] = "todo"

    result = validate_roadmap_candidate_charter(charter, require_live=True)

    assert result["ready_for_roadmap_candidate_charter"] is False
    assert result["blocker_count"] == 1


def test_unsafe_scope_reference_blocks_candidate_charter() -> None:
    charter = build_roadmap_candidate_charter(evidence_mode="live")
    charter["candidate_scope"]["customer_value_ref"] = "https://example.com/private"

    result = validate_roadmap_candidate_charter(charter, require_live=True)

    assert result["ready_for_roadmap_candidate_charter"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_candidate_charter() -> None:
    charter = build_roadmap_candidate_charter(evidence_mode="live")
    charter["customer_name"] = "do-not-commit"

    result = validate_roadmap_candidate_charter(charter, require_live=True)

    assert result["ready_for_roadmap_candidate_charter"] is False
    assert result["blocker_count"] == 1


def test_roadmap_candidate_charter_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-candidate-charter"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_candidate_charter.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_charter = export_dir / "roadmap-candidate-charter.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_candidate_charter.py",
            "--charter",
            str(live_charter),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_roadmap_candidate_charter_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-candidate-charter"
    export_result = runner.invoke(
        app,
        ["release", "roadmap-candidate-charter", "--export-dir", str(export_dir)],
    )

    assert export_result.exit_code == 0, export_result.output
    live_charter = export_dir / "roadmap-candidate-charter.live.sanitized.example.json"
    assert live_charter.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "roadmap-candidate-charter",
            "--charter",
            str(live_charter),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_roadmap_candidate_charter": true' in validate_result.output


def test_roadmap_candidate_charter_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_charter = tmp_path / "sample-charter.json"
    sample_charter.write_text(
        json.dumps(build_roadmap_candidate_charter(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "roadmap-candidate-charter",
            "--charter",
            str(sample_charter),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 2' in result.output
