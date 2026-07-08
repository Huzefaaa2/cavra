from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.roadmap_intake_gate import (
    build_roadmap_intake_gate_packet,
    validate_roadmap_intake_gate_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_roadmap_intake_gate_warns_without_blocking_shape() -> None:
    packet = build_roadmap_intake_gate_packet(evidence_mode="sample")

    result = validate_roadmap_intake_gate_packet(packet)

    assert result["ready_for_roadmap_intake_decision"] is False
    assert result["decision"] == "live_operations_evidence"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1


def test_live_operating_request_stays_live_operations_evidence() -> None:
    packet = build_roadmap_intake_gate_packet(
        evidence_mode="live",
        requested_change_type="public_scorecard_refresh",
    )

    result = validate_roadmap_intake_gate_packet(packet, require_live=True)

    assert result["ready_for_roadmap_intake_decision"] is True
    assert result["decision"] == "live_operations_evidence"
    assert result["blocker_count"] == 0


def test_live_product_capability_becomes_roadmap_candidate() -> None:
    packet = build_roadmap_intake_gate_packet(
        evidence_mode="live",
        requested_change_type="new_api_or_cli",
    )

    result = validate_roadmap_intake_gate_packet(packet, require_live=True)

    assert result["ready_for_roadmap_intake_decision"] is True
    assert result["decision"] == "new_product_roadmap_candidate"
    assert result["blocker_count"] == 0


def test_require_live_rejects_sample_roadmap_intake_gate() -> None:
    packet = build_roadmap_intake_gate_packet(evidence_mode="sample")

    result = validate_roadmap_intake_gate_packet(packet, require_live=True)

    assert result["ready_for_roadmap_intake_decision"] is False
    assert result["blocker_count"] == 1


def test_operating_request_cannot_expand_roadmap() -> None:
    packet = build_roadmap_intake_gate_packet(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )
    packet["boundary_decision"]["decision"] = "new_product_roadmap_candidate"

    result = validate_roadmap_intake_gate_packet(packet, require_live=True)

    assert result["ready_for_roadmap_intake_decision"] is False
    assert result["blocker_count"] == 1
    decision_check = next(check for check in result["checks"] if check["name"] == "roadmap_boundary_decision")
    assert "routine operating requests" in decision_check["message"]


def test_product_candidate_requires_product_surface_ref() -> None:
    packet = build_roadmap_intake_gate_packet(
        evidence_mode="live",
        requested_change_type="new_product_capability",
    )
    packet["request_classification"]["product_surface_refs"] = []

    result = validate_roadmap_intake_gate_packet(packet, require_live=True)

    assert result["ready_for_roadmap_intake_decision"] is False
    assert result["blocker_count"] == 1


def test_unknown_change_type_blocks_intake_gate() -> None:
    packet = build_roadmap_intake_gate_packet(
        evidence_mode="live",
        requested_change_type="unbounded_r7_cycle",
    )

    result = validate_roadmap_intake_gate_packet(packet, require_live=True)

    assert result["ready_for_roadmap_intake_decision"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_roadmap_intake_gate() -> None:
    packet = build_roadmap_intake_gate_packet(evidence_mode="live")
    packet["tenant_name"] = "do-not-commit"

    result = validate_roadmap_intake_gate_packet(packet, require_live=True)

    assert result["ready_for_roadmap_intake_decision"] is False
    assert result["blocker_count"] == 1


def test_roadmap_intake_gate_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-intake-gate"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_intake_gate.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_packet = export_dir / "roadmap-intake-gate.product-candidate.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_intake_gate.py",
            "--packet",
            str(live_packet),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_roadmap_intake_gate_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-intake-gate"
    export_result = runner.invoke(
        app,
        ["release", "roadmap-intake-gate", "--export-dir", str(export_dir)],
    )

    assert export_result.exit_code == 0, export_result.output
    live_packet = export_dir / "roadmap-intake-gate.operating.live.sanitized.example.json"
    assert live_packet.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "roadmap-intake-gate",
            "--packet",
            str(live_packet),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_roadmap_intake_decision": true' in validate_result.output


def test_roadmap_intake_gate_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_packet = tmp_path / "sample-intake.json"
    sample_packet.write_text(
        json.dumps(build_roadmap_intake_gate_packet(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "roadmap-intake-gate",
            "--packet",
            str(sample_packet),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
