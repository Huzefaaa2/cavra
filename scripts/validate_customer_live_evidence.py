#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.customer_live_evidence import (  # noqa: E402
    build_customer_live_evidence_template,
    validate_customer_live_evidence_packet,
    write_customer_live_evidence_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA customer-live evidence intake packets.")
    parser.add_argument("--packet", type=Path, help="Customer-live evidence packet JSON.")
    parser.add_argument("--export-dir", type=Path, help="Export sample and live sanitized evidence templates.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and sanitized=true.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.export_dir:
        result = write_customer_live_evidence_artifacts(args.export_dir)
        exit_ok = result["ready_for_customer_live_evidence_intake"] is True
    else:
        packet = _read_json(args.packet) if args.packet else build_customer_live_evidence_template()
        result = validate_customer_live_evidence_packet(packet, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0 and (
            not args.require_live or result["ready_for_customer_live_evidence_intake"] is True
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
