from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.roadmap_completion_boundary import validate_repository
from cavra.roadmap_future_work_governance_index import (
    build_roadmap_future_work_governance_index,
    validate_roadmap_future_work_governance_index,
)


ROADMAP_GOVERNANCE_QUICKCHECK_RESULT_SCHEMA = "cavra.roadmap-governance-quickcheck.result.v1"


def validate_roadmap_governance_quickcheck(
    *,
    repo_root: Path,
    index: dict[str, Any] | None = None,
    require_live: bool = False,
    change_type: str = "new_product_capability",
) -> dict[str, Any]:
    boundary_result = validate_repository(repo_root)
    governance_index = index or build_roadmap_future_work_governance_index(
        evidence_mode="live" if require_live else "sample",
        requested_change_type=change_type,
    )
    governance_result = validate_roadmap_future_work_governance_index(
        governance_index,
        require_live=require_live,
    )

    blockers: list[str] = []
    if boundary_result.get("ready_for_roadmap_completion_boundary") is not True:
        blockers.extend(str(blocker) for blocker in boundary_result.get("blockers", []))
        if not blockers:
            blockers.append("Roadmap completion boundary is not ready.")
    if governance_result.get("blocker_count", 0) > 0 or (
        require_live and governance_result.get("ready_for_roadmap_future_work_governance_index") is not True
    ):
        blockers.append("Roadmap future work governance index is not live and ready.")

    warning_count = int(governance_result.get("warning_count", 0))
    if not require_live and governance_result.get("evidence_mode") == "sample":
        warning_count = max(warning_count, 1)

    ready = not blockers and warning_count == 0 and require_live
    return {
        "schema_version": ROADMAP_GOVERNANCE_QUICKCHECK_RESULT_SCHEMA,
        "product": "CAVRA",
        "ready_for_roadmap_governance_quickcheck": ready,
        "decision": "ready_to_operate_closed_roadmap_governance" if ready else "blocked",
        "require_live": require_live,
        "blocker_count": len(blockers),
        "warning_count": warning_count,
        "blockers": blockers,
        "checks": [
            {
                "name": "roadmap_completion_boundary",
                "status": "pass"
                if boundary_result.get("ready_for_roadmap_completion_boundary") is True
                else "blocker",
                "message": "R7.61 completion boundary is intact."
                if boundary_result.get("ready_for_roadmap_completion_boundary") is True
                else "R7.61 completion boundary is blocked.",
            },
            {
                "name": "roadmap_future_work_governance_index",
                "status": "pass"
                if governance_result.get("ready_for_roadmap_future_work_governance_index") is True
                else ("warn" if governance_result.get("blocker_count") == 0 else "blocker"),
                "message": "Future-work governance chain is live and ready."
                if governance_result.get("ready_for_roadmap_future_work_governance_index") is True
                else "Future-work governance chain is not live-ready.",
            },
        ],
        "roadmap_completion_boundary": boundary_result,
        "roadmap_future_work_governance_index": governance_result,
    }


def write_roadmap_governance_quickcheck_artifacts(output_dir: Path, *, repo_root: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_result = validate_roadmap_governance_quickcheck(repo_root=repo_root)
    live_result = validate_roadmap_governance_quickcheck(repo_root=repo_root, require_live=True)
    written = {
        "sample_result": output_dir / "roadmap-governance-quickcheck.sample.result.json",
        "live_result": output_dir / "roadmap-governance-quickcheck.live.sanitized.result.json",
    }
    payloads = {
        "sample_result": sample_result,
        "live_result": live_result,
    }
    for name, payload in payloads.items():
        written[name].write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.roadmap-governance-quickcheck.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_roadmap_governance_quickcheck": live_result[
            "ready_for_roadmap_governance_quickcheck"
        ],
    }
