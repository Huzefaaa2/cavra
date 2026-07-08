from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.roadmap_future_work_governance_index import build_roadmap_future_work_governance_index
from cavra.roadmap_governance_quickcheck import validate_roadmap_governance_quickcheck


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_roadmap_governance_quickcheck_warns_without_blockers() -> None:
    result = validate_roadmap_governance_quickcheck(repo_root=REPO_ROOT)

    assert result["ready_for_roadmap_governance_quickcheck"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1
    assert result["roadmap_completion_boundary"]["ready_for_roadmap_completion_boundary"] is True


def test_live_roadmap_governance_quickcheck_is_ready() -> None:
    result = validate_roadmap_governance_quickcheck(repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_roadmap_governance_quickcheck"] is True
    assert result["decision"] == "ready_to_operate_closed_roadmap_governance"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_non_ready_future_work_index_blocks_quickcheck() -> None:
    index = build_roadmap_future_work_governance_index(
        evidence_mode="live",
        requested_change_type="customer_monitoring_cycle",
    )

    result = validate_roadmap_governance_quickcheck(
        repo_root=REPO_ROOT,
        index=index,
        require_live=True,
    )

    assert result["ready_for_roadmap_governance_quickcheck"] is False
    assert result["blocker_count"] >= 1
    assert "Roadmap future work governance index is not live and ready." in result["blockers"]


def test_roadmap_governance_quickcheck_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "roadmap-governance-quickcheck"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_governance_quickcheck.py",
            "--repo-root",
            ".",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_result = export_dir / "roadmap-governance-quickcheck.live.sanitized.result.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_roadmap_governance_quickcheck.py",
            "--repo-root",
            ".",
            "--require-live",
            "--output",
            str(live_result),
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    payload = json.loads(live_result.read_text(encoding="utf-8"))
    assert payload["ready_for_roadmap_governance_quickcheck"] is True


def test_roadmap_governance_quickcheck_cli_validates_live() -> None:
    result = runner.invoke(
        app,
        [
            "release",
            "roadmap-governance-quickcheck",
            "--repo-root",
            str(REPO_ROOT),
            "--require-live",
        ],
    )

    assert result.exit_code == 0, result.output
    assert '"ready_for_roadmap_governance_quickcheck": true' in result.output


def test_roadmap_governance_quickcheck_cli_rejects_bad_index(tmp_path: Path) -> None:
    rejected_index = tmp_path / "rejected-index.json"
    rejected_index.write_text(
        json.dumps(
            build_roadmap_future_work_governance_index(
                evidence_mode="live",
                requested_change_type="customer_monitoring_cycle",
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "roadmap-governance-quickcheck",
            "--repo-root",
            str(REPO_ROOT),
            "--index",
            str(rejected_index),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"ready_for_roadmap_governance_quickcheck": false' in result.output
