from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.roadmap_future_phase_opening_gate import (
    build_roadmap_future_phase_opening_gate,
    validate_roadmap_future_phase_opening_gate,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_roadmap_future_phase_opening_gate_warns_without_blocking_shape() -> None:
    gate = build_roadmap_future_phase_opening_gate(evidence_mode="sample")

    result = validate_roadmap_future_phase_opening_gate(gate)

    assert result["ready_for_roadmap_future_phase_opening"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1
    assert result["decision"] == "ready_to_open_future_product_phase"


def test_live_roadmap_future_phase_opening_gate_is_ready() -> None:
    gate = build_roadmap_future_phase_opening_gate(evidence_mode="live")

    result = validate_roadmap_future_phase_opening_gate(gate, require_live=True)

    assert result["ready_for_roadmap_future_phase_opening"] is True
    assert result["decision"] == "ready_to_open_future_product_phase"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["milestone_count"] == 3


def test_require_live_rejects_sample_future_phase_opening_gate() -> None:
    gate = build_roadmap_future_phase_opening_gate(evidence_mode="sample")

    result = validate_roadmap_future_phase_opening_gate(gate, require_live=True)

    assert result["ready_for_roadmap_future_phase_opening"] is False
    assert result["blocker_count"] >= 1


def test_operating_evidence_cannot_open_future_phase() -> None:
    gate = build_roadmap_future_phase_opening_gate(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )

    result = validate_roadmap_future_phase_opening_gate(gate, require_live=True)

    assert result["ready_for_roadmap_future_phase_opening"] is False
    assert result["blocker_count"] >= 1
    source_check = next(check for check in result["checks"] if check["name"] == "source_candidate_charter_result")
    assert "Source candidate charter has blockers" in source_check["message"]


def test_missing_milestone_refs_blocks_future_phase_opening_gate() -> None:
    gate = build_roadmap_future_phase_opening_gate(evidence_mode="live")
    gate["phase_plan"]["milestone_refs"] = []

    result = validate_roadmap_future_phase_opening_gate(gate, require_live=True)

    assert result["ready_for_roadmap_future_phase_opening"] is False
    assert result["blocker_count"] == 1
    phase_plan_check = next(check for check in result["checks"] if check["name"] == "phase_plan")
    assert "milestone_refs" in phase_plan_check["message"]


def test_unsafe_opening_control_reference_blocks_future_phase_opening_gate() -> None:
    gate = build_roadmap_future_phase_opening_gate(evidence_mode="live")
    gate["opening_controls"]["release_gate_ref"] = "https://example.com/private"

    result = validate_roadmap_future_phase_opening_gate(gate, require_live=True)

    assert result["ready_for_roadmap_future_phase_opening"] is False
    assert result["blocker_count"] == 1


def test_non_ready_decision_blocks_future_phase_opening_gate() -> None:
    gate = build_roadmap_future_phase_opening_gate(evidence_mode="live")
    gate["opening_decision"]["opening_decision"] = "needs_more_charter_detail"

    result = validate_roadmap_future_phase_opening_gate(gate, require_live=True)

    assert result["ready_for_roadmap_future_phase_opening"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_future_phase_opening_gate() -> None:
    gate = build_roadmap_future_phase_opening_gate(evidence_mode="live")
    gate["tenant_name"] = "do-not-commit"

    result = validate_roadmap_future_phase_opening_gate(gate, require_live=True)

    assert result["ready_for_roadmap_future_phase_opening"] is False
    assert result["blocker_count"] == 1


def test_roadmap_future_phase_opening_gate_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-future-phase-opening-gate"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_future_phase_opening_gate.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_gate = export_dir / "roadmap-future-phase-opening-gate.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_future_phase_opening_gate.py",
            "--gate",
            str(live_gate),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_roadmap_future_phase_opening_gate_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-future-phase-opening-gate"
    export_result = runner.invoke(
        app,
        ["release", "roadmap-future-phase-opening-gate", "--export-dir", str(export_dir)],
    )

    assert export_result.exit_code == 0, export_result.output
    live_gate = export_dir / "roadmap-future-phase-opening-gate.live.sanitized.example.json"
    assert live_gate.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "roadmap-future-phase-opening-gate",
            "--gate",
            str(live_gate),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_roadmap_future_phase_opening": true' in validate_result.output


def test_roadmap_future_phase_opening_gate_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_gate = tmp_path / "sample-gate.json"
    sample_gate.write_text(
        json.dumps(build_roadmap_future_phase_opening_gate(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "roadmap-future-phase-opening-gate",
            "--gate",
            str(sample_gate),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"ready_for_roadmap_future_phase_opening": false' in result.output
