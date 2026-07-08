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

from cavra.managed_enterprise_live_validation_plan import (  # noqa: E402
    build_managed_enterprise_live_validation_plan,
    validate_managed_enterprise_live_validation_plan,
    write_managed_enterprise_live_validation_plan_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA Managed/Enterprise live validation plans.")
    parser.add_argument("--plan", type=Path, help="Managed/Enterprise live validation plan JSON.")
    parser.add_argument("--export-dir", type=Path, help="Export sample and live sanitized validation plan templates.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and sanitized=true.")
    parser.add_argument("--output", type=Path, help="Optional path for the validation result JSON.")
    args = parser.parse_args()

    if args.export_dir:
        result = write_managed_enterprise_live_validation_plan_artifacts(args.export_dir)
        exit_ok = result["ready_for_managed_enterprise_live_validation"] is True
    else:
        if args.plan:
            plan = json.loads(args.plan.read_text(encoding="utf-8"))
        else:
            plan = build_managed_enterprise_live_validation_plan(
                evidence_mode="live" if args.require_live else "sample",
            )
        result = validate_managed_enterprise_live_validation_plan(plan, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0 and (
            not args.require_live or result["ready_for_managed_enterprise_live_validation"] is True
        )

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
