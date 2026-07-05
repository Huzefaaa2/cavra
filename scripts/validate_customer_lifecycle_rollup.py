#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cavra.customer_lifecycle_rollup import (  # noqa: E402
    build_customer_lifecycle_rollup_packet,
    validate_customer_lifecycle_rollup_packet,
    write_customer_lifecycle_rollup_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA customer lifecycle executive rollup readiness.")
    parser.add_argument("--packet", type=Path, help="Optional customer lifecycle rollup packet JSON.")
    parser.add_argument("--export-dir", type=Path, help="Optional directory to export sample/live rollup packets.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and sanitized=true.")
    parser.add_argument("--output", type=Path, help="Optional path for the validation result JSON.")
    args = parser.parse_args()

    if args.export_dir:
        result = write_customer_lifecycle_rollup_artifacts(args.export_dir)
    else:
        if args.packet:
            packet = json.loads(args.packet.read_text(encoding="utf-8"))
        else:
            packet = build_customer_lifecycle_rollup_packet(evidence_mode="live" if args.require_live else "sample")
        result = validate_customer_lifecycle_rollup_packet(packet, require_live=args.require_live)

    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")

    if args.export_dir:
        return 0 if result.get("ready_for_customer_lifecycle_executive_rollup") else 1
    return 0 if result.get("blocker_count", 1) == 0 and (not args.require_live or result.get("ready_for_customer_lifecycle_executive_rollup")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
