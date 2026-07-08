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

from cavra.roadmap_completion_boundary import validate_repository  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the normalized CAVRA roadmap completion boundary.")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
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
