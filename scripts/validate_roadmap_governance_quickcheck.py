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

from cavra.roadmap_governance_quickcheck import (  # noqa: E402
    validate_roadmap_governance_quickcheck,
    write_roadmap_governance_quickcheck_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the CAVRA roadmap governance quickcheck.")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--index", type=Path, help="Optional future work governance index JSON.")
    parser.add_argument("--export-dir", type=Path, help="Export sample and live quickcheck result JSON.")
    parser.add_argument(
        "--change-type",
        default="new_product_capability",
        help="Change type to use when building a default future work governance index.",
    )
    parser.add_argument("--require-live", action="store_true", help="Require live sanitized governance evidence.")
    parser.add_argument("--output", type=Path, help="Optional path for the validation result JSON.")
    args = parser.parse_args()

    if args.export_dir:
        result = write_roadmap_governance_quickcheck_artifacts(args.export_dir, repo_root=args.repo_root)
        exit_ok = result["ready_for_roadmap_governance_quickcheck"] is True
    else:
        index = json.loads(args.index.read_text(encoding="utf-8")) if args.index else None
        result = validate_roadmap_governance_quickcheck(
            repo_root=args.repo_root,
            index=index,
            require_live=args.require_live,
            change_type=args.change_type,
        )
        exit_ok = result["ready_for_roadmap_governance_quickcheck"] is True if args.require_live else (
            result["blocker_count"] == 0
        )

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
