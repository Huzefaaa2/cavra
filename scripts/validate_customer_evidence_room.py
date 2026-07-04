#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.customer_evidence_room import (  # noqa: E402
    build_customer_evidence_room_index,
    validate_customer_evidence_room_index,
    write_customer_evidence_room_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA customer evidence-room closeout indexes.")
    parser.add_argument("--index", type=Path, help="Customer evidence-room index JSON.")
    parser.add_argument("--intake-packet", type=Path, help="Optional customer-live intake packet JSON to build an index.")
    parser.add_argument("--export-dir", type=Path, help="Export sample and live sanitized evidence-room indexes.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and sanitized=true.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.export_dir:
        result = write_customer_evidence_room_artifacts(args.export_dir)
        exit_ok = result["ready_for_customer_evidence_room_closeout"] is True
    else:
        if args.index:
            index = _read_json(args.index)
        else:
            intake = _read_json(args.intake_packet) if args.intake_packet else None
            index = build_customer_evidence_room_index(
                intake,
                evidence_mode="live" if args.require_live else "sample",
            )
        result = validate_customer_evidence_room_index(index, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0 and (
            not args.require_live or result["ready_for_customer_evidence_room_closeout"] is True
        )

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
