from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.roadmap_future_phase_registry import (
    build_roadmap_future_phase_registry,
    validate_roadmap_future_phase_registry,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_roadmap_future_phase_registry_warns_without_blocking_shape() -> None:
    registry = build_roadmap_future_phase_registry(evidence_mode="sample")

    result = validate_roadmap_future_phase_registry(registry)

    assert result["ready_for_roadmap_future_phase_registry"] is False
    assert result["decision"] == "ready_to_register_future_phase"
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1
    assert result["future_phase_entry_count"] == 1


def test_live_roadmap_future_phase_registry_is_ready() -> None:
    registry = build_roadmap_future_phase_registry(evidence_mode="live")

    result = validate_roadmap_future_phase_registry(registry, require_live=True)

    assert result["ready_for_roadmap_future_phase_registry"] is True
    assert result["decision"] == "ready_to_register_future_phase"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_future_phase_registry() -> None:
    registry = build_roadmap_future_phase_registry(evidence_mode="sample")

    result = validate_roadmap_future_phase_registry(registry, require_live=True)

    assert result["ready_for_roadmap_future_phase_registry"] is False
    assert result["blocker_count"] >= 1


def test_operating_evidence_cannot_register_future_phase() -> None:
    registry = build_roadmap_future_phase_registry(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )

    result = validate_roadmap_future_phase_registry(registry, require_live=True)

    assert result["ready_for_roadmap_future_phase_registry"] is False
    assert result["blocker_count"] >= 1
    source_check = next(check for check in result["checks"] if check["name"] == "source_opening_gate_result")
    assert "Source future phase opening gate has blockers" in source_check["message"]


def test_duplicate_phase_id_blocks_future_phase_registry() -> None:
    registry = build_roadmap_future_phase_registry(evidence_mode="live")
    registry["future_phase_entries"].append(dict(registry["future_phase_entries"][0]))

    result = validate_roadmap_future_phase_registry(registry, require_live=True)

    assert result["ready_for_roadmap_future_phase_registry"] is False
    assert result["blocker_count"] == 1
    entries_check = next(check for check in result["checks"] if check["name"] == "future_phase_entries")
    assert "duplicate phase_id_ref" in entries_check["message"]


def test_unsafe_registry_reference_blocks_future_phase_registry() -> None:
    registry = build_roadmap_future_phase_registry(evidence_mode="live")
    registry["registry_profile"]["registry_ref"] = "https://example.com/private"

    result = validate_roadmap_future_phase_registry(registry, require_live=True)

    assert result["ready_for_roadmap_future_phase_registry"] is False
    assert result["blocker_count"] == 1


def test_non_ready_entry_status_blocks_future_phase_registry() -> None:
    registry = build_roadmap_future_phase_registry(evidence_mode="live")
    registry["future_phase_entries"][0]["phase_status"] = "rejected_to_opening_gate"

    result = validate_roadmap_future_phase_registry(registry, require_live=True)

    assert result["ready_for_roadmap_future_phase_registry"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_future_phase_registry() -> None:
    registry = build_roadmap_future_phase_registry(evidence_mode="live")
    registry["customer_email"] = "do-not-commit@example.com"

    result = validate_roadmap_future_phase_registry(registry, require_live=True)

    assert result["ready_for_roadmap_future_phase_registry"] is False
    assert result["blocker_count"] == 1


def test_roadmap_future_phase_registry_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-future-phase-registry"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_future_phase_registry.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_registry = export_dir / "roadmap-future-phase-registry.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_future_phase_registry.py",
            "--registry",
            str(live_registry),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_roadmap_future_phase_registry_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-future-phase-registry"
    export_result = runner.invoke(
        app,
        ["release", "roadmap-future-phase-registry", "--export-dir", str(export_dir)],
    )

    assert export_result.exit_code == 0, export_result.output
    live_registry = export_dir / "roadmap-future-phase-registry.live.sanitized.example.json"
    assert live_registry.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "roadmap-future-phase-registry",
            "--registry",
            str(live_registry),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_roadmap_future_phase_registry": true' in validate_result.output


def test_roadmap_future_phase_registry_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_registry = tmp_path / "sample-registry.json"
    sample_registry.write_text(
        json.dumps(build_roadmap_future_phase_registry(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "roadmap-future-phase-registry",
            "--registry",
            str(sample_registry),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"ready_for_roadmap_future_phase_registry": false' in result.output
