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

from cavra.customer_lifecycle_phase8_next_cycle_readiness_index import (  # noqa: E402
    build_customer_lifecycle_phase8_next_cycle_readiness_index_packet,
    validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet,
    write_customer_lifecycle_phase8_next_cycle_readiness_index_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA customer lifecycle Phase 8 next-cycle readiness index.")
    parser.add_argument("--packet", type=Path, help="Optional next-cycle readiness index packet JSON.")
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="Repository root for generated source packets.")
    parser.add_argument("--export-dir", type=Path, help="Write sample/live sanitized example artifacts.")
    parser.add_argument("--require-live", action="store_true", help="Require live sanitized packet readiness.")
    parser.add_argument("--output", type=Path, help="Optional path for validation JSON result.")
    args = parser.parse_args()

    if args.export_dir:
        result = write_customer_lifecycle_phase8_next_cycle_readiness_index_artifacts(args.export_dir, args.repo_root)
    else:
        if args.packet:
            packet = json.loads(args.packet.read_text(encoding="utf-8"))
        else:
            packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
                repo_root=args.repo_root,
                evidence_mode="live" if args.require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
            packet,
            require_live=args.require_live,
        )

    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if args.require_live and not result.get("ready_for_customer_lifecycle_phase8_next_cycle_readiness_index", False):
        return 1
    if result.get("blocker_count", 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
