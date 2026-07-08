#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cavra.roadmap_future_work_governance_index import (  # noqa: E402
    build_roadmap_future_work_governance_index,
    validate_roadmap_future_work_governance_index,
    write_roadmap_future_work_governance_index_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA roadmap future work governance indexes.")
    parser.add_argument("--index", type=Path, help="Roadmap future work governance index JSON.")
    parser.add_argument("--export-dir", type=Path, help="Export sample and live sanitized governance indexes.")
    parser.add_argument(
        "--change-type",
        default="new_product_capability",
        help="Change type to use when building a default index.",
    )
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and sanitized=true.")
    parser.add_argument("--output", type=Path, help="Optional path for the validation result JSON.")
    args = parser.parse_args()

    if args.export_dir:
        result = write_roadmap_future_work_governance_index_artifacts(args.export_dir)
        exit_ok = result["ready_for_roadmap_future_work_governance_index"] is True
    else:
        if args.index:
            index = json.loads(args.index.read_text(encoding="utf-8"))
        else:
            index = build_roadmap_future_work_governance_index(
                evidence_mode="live" if args.require_live else "sample",
                requested_change_type=args.change_type,
            )
        result = validate_roadmap_future_work_governance_index(index, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0 and (
            not args.require_live or result["ready_for_roadmap_future_work_governance_index"] is True
        )

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
