#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_PHASES = {str(index): "Completed" for index in range(8)}
EXPECTED_ROW_COUNT = 91
EXPECTED_LAST_ROW = "R7.61"
MAX_PHASE7_ROW = 61


@dataclass(frozen=True)
class RoadmapRow:
    row_id: str
    phase: str
    status: str


def _read(path: Path, blockers: list[str]) -> str:
    if not path.exists():
        blockers.append(f"missing required file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def _parse_phase_table(text: str) -> dict[str, str]:
    phases: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 4 and cells[0].isdigit():
            phases[cells[0]] = cells[3]
    return phases


def _parse_roadmap_rows(text: str) -> list[RoadmapRow]:
    rows: list[RoadmapRow] = []
    for line in text.splitlines():
        if not line.startswith("| R"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 6 and re.fullmatch(r"R\d+\.\d+", cells[0]):
            rows.append(RoadmapRow(row_id=cells[0], phase=cells[1], status=cells[5]))
    return rows


def _require_fragments(path: Path, text: str, fragments: list[str], blockers: list[str]) -> None:
    normalized_text = " ".join(text.split())
    for fragment in fragments:
        normalized_fragment = " ".join(fragment.split())
        if normalized_fragment not in normalized_text:
            blockers.append(f"{path} missing required roadmap boundary text: {fragment}")


def _validate_roadmap(path: Path, text: str, blockers: list[str]) -> dict[str, Any]:
    phases = _parse_phase_table(text)
    rows = _parse_roadmap_rows(text)
    r7_numbers = [
        int(row.row_id.split(".", 1)[1])
        for row in rows
        if row.row_id.startswith("R7.")
    ]

    if phases != EXPECTED_PHASES:
        blockers.append(f"{path} phase summary is not normalized: {phases}")

    if len(rows) != EXPECTED_ROW_COUNT:
        blockers.append(f"{path} expected {EXPECTED_ROW_COUNT} numbered rows, found {len(rows)}")

    non_completed = [row.row_id for row in rows if row.status != "Completed"]
    if non_completed:
        blockers.append(f"{path} contains non-completed rows: {', '.join(non_completed)}")

    if rows and rows[-1].row_id != EXPECTED_LAST_ROW:
        blockers.append(f"{path} expected final row {EXPECTED_LAST_ROW}, found {rows[-1].row_id}")

    over_boundary = [row.row_id for row in rows if row.row_id.startswith("R7.") and int(row.row_id.split(".", 1)[1]) > MAX_PHASE7_ROW]
    if over_boundary:
        blockers.append(f"{path} contains rows beyond the Phase 7 closeout boundary: {', '.join(over_boundary)}")

    _require_fragments(
        path,
        text,
        [
            "not another R7 implementation loop",
            "live Managed or Enterprise deployment execution",
            "Routine customer monitoring, scorecard refresh, drift remediation",
            "new API",
            "validator family",
        ],
        blockers,
    )

    return {
        "phase_statuses": phases,
        "row_count": len(rows),
        "completed_row_count": sum(1 for row in rows if row.status == "Completed"),
        "final_row": rows[-1].row_id if rows else None,
        "max_r7_row": max(r7_numbers) if r7_numbers else None,
    }


def validate_repository(repo_root: Path) -> dict[str, Any]:
    blockers: list[str] = []

    roadmap_path = repo_root / "docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md"
    wiki_roadmap_path = repo_root / "docs/wiki/CAVRA-Unified-Enterprise-Enhancement-Roadmap.md"
    status_path = repo_root / "docs/product/cavra-unified-enterprise-status-report.md"
    wiki_status_path = repo_root / "docs/wiki/CAVRA-Unified-Enterprise-Status-Report.md"
    closeout_path = repo_root / "docs/phase7-roadmap-closeout.md"
    wiki_closeout_path = repo_root / "docs/wiki/Phase-7-Roadmap-Closeout.md"
    intake_gate_path = repo_root / "docs/roadmap-intake-gate.md"
    wiki_intake_gate_path = repo_root / "docs/wiki/Roadmap-Intake-Gate.md"
    candidate_charter_path = repo_root / "docs/roadmap-candidate-charter.md"
    wiki_candidate_charter_path = repo_root / "docs/wiki/Roadmap-Candidate-Charter.md"
    readme_path = repo_root / "README.md"

    roadmap_text = _read(roadmap_path, blockers)
    wiki_roadmap_text = _read(wiki_roadmap_path, blockers)
    status_text = _read(status_path, blockers)
    wiki_status_text = _read(wiki_status_path, blockers)
    closeout_text = _read(closeout_path, blockers)
    wiki_closeout_text = _read(wiki_closeout_path, blockers)
    intake_gate_text = _read(intake_gate_path, blockers)
    wiki_intake_gate_text = _read(wiki_intake_gate_path, blockers)
    candidate_charter_text = _read(candidate_charter_path, blockers)
    wiki_candidate_charter_text = _read(wiki_candidate_charter_path, blockers)
    readme_text = _read(readme_path, blockers)

    roadmap_result = _validate_roadmap(roadmap_path, roadmap_text, blockers)
    wiki_roadmap_result = _validate_roadmap(wiki_roadmap_path, wiki_roadmap_text, blockers)

    for path, text in (
        (status_path, status_text),
        (wiki_status_path, wiki_status_text),
    ):
        _require_fragments(
            path,
            text,
            [
                "91 of 91 numbered rows",
                "phases 0-7 are complete",
                "Phase 7 closes at R7.61",
                "not public repository blockers",
                "live Managed or Enterprise operating tasks",
                "roadmap intake gate",
                "roadmap candidate charter",
                "Create a new roadmap item only when the work changes CAVRA itself",
            ],
            blockers,
        )

    for path, text in (
        (closeout_path, closeout_text),
        (wiki_closeout_path, wiki_closeout_text),
    ):
        _require_fragments(
            path,
            text,
            [
                "R7.1 through R7.4",
                "Future work should not add R7.62",
                "Phase 7 closes at R7.61",
                "Roadmap Intake Gate",
                "Roadmap Candidate Charter",
                "live operations evidence",
            ],
            blockers,
        )

    for path, text in (
        (intake_gate_path, intake_gate_text),
        (wiki_intake_gate_path, wiki_intake_gate_text),
    ):
        _require_fragments(
            path,
            text,
            [
                "live_operations_evidence",
                "new_product_roadmap_candidate",
                "needs_architect_review",
                "Phase 7 closes at `R7.61`",
            ],
            blockers,
        )

    for path, text in (
        (candidate_charter_path, candidate_charter_text),
        (wiki_candidate_charter_path, wiki_candidate_charter_text),
    ):
        _require_fragments(
            path,
            text,
            [
                "ready_for_roadmap_candidate_charter",
                "ready_for_product_roadmap_planning",
                "new_product_roadmap_candidate",
                "The charter is not itself a new product phase",
            ],
            blockers,
        )

    _require_fragments(
        readme_path,
        readme_text,
        [
            "CAVRA Unified Enterprise Status Report",
            "every numbered row currently in the tracker is completed",
            "Phase 7 Roadmap Closeout",
            "CAVRA Roadmap Intake Gate",
            "CAVRA Roadmap Candidate Charter",
            "Future repeated customer monitoring",
        ],
        blockers,
    )

    result: dict[str, Any] = {
        "ready_for_roadmap_completion_boundary": not blockers,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "roadmap": roadmap_result,
        "wiki_roadmap": wiki_roadmap_result,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the normalized CAVRA roadmap completion boundary.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="Optional path for validation JSON output.")
    args = parser.parse_args()

    result = validate_repository(args.repo_root)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["ready_for_roadmap_completion_boundary"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
