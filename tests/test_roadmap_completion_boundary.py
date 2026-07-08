from __future__ import annotations

import subprocess
from pathlib import Path

from cavra.roadmap_completion_boundary import validate_repository


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_roadmap_completion_boundary_is_ready() -> None:
    result = validate_repository(REPO_ROOT)

    assert result["ready_for_roadmap_completion_boundary"] is True
    assert result["blocker_count"] == 0
    assert result["roadmap"]["row_count"] == 91
    assert result["roadmap"]["completed_row_count"] == 91
    assert result["roadmap"]["final_row"] == "R7.61"
    assert result["roadmap"]["max_r7_row"] == 61


def test_roadmap_completion_boundary_script_passes() -> None:
    subprocess.run(
        ["python3", "scripts/validate_roadmap_completion_boundary.py", "--repo-root", "."],
        cwd=REPO_ROOT,
        check=True,
    )
