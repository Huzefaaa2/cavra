#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cavra.customer_lifecycle_verification_index import (  # noqa: E402
    build_customer_lifecycle_verification_index,
    validate_customer_lifecycle_verification_index,
    write_customer_lifecycle_verification_index_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA customer lifecycle verification index readiness.")
    parser.add_argument("--index", type=Path, help="Optional customer lifecycle verification index JSON.")
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="Repository root used to verify artifact paths.")
    parser.add_argument("--export-dir", type=Path, help="Optional directory to export sample/live verification indexes.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and sanitized=true.")
    parser.add_argument("--output", type=Path, help="Optional path for the validation result JSON.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    if args.export_dir:
        result = write_customer_lifecycle_verification_index_artifacts(args.export_dir, repo_root)
    else:
        if args.index:
            index = json.loads(args.index.read_text(encoding="utf-8"))
        else:
            index = build_customer_lifecycle_verification_index(
                repo_root,
                evidence_mode="live" if args.require_live else "sample",
            )
        result = validate_customer_lifecycle_verification_index(index, repo_root=repo_root, require_live=args.require_live)

    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")

    if args.export_dir:
        return 0 if result.get("ready_for_customer_lifecycle_verification_index") else 1
    return 0 if result.get("blocker_count", 1) == 0 and (
        not args.require_live or result.get("ready_for_customer_lifecycle_verification_index")
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
