#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.enterprise_reporting_exports import (  # noqa: E402
    build_enterprise_report_export_readiness,
    export_enterprise_reporting_package,
    validate_enterprise_report_export_packet,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA Enterprise report export readiness.")
    parser.add_argument("--packet", type=Path, help="Sample or live report export readiness packet JSON.")
    parser.add_argument("--export-dir", type=Path, help="Generate public-safe sample report exports into this directory.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.export_dir:
        result = export_enterprise_reporting_package(args.export_dir)
        exit_ok = result["artifact_count"] == 4
    elif args.packet:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_enterprise_report_export_packet(packet, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0
    else:
        result = build_enterprise_report_export_readiness(require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
