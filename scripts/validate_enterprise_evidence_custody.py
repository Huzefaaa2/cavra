#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.evidence_custody import build_enterprise_evidence_custody_readiness


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA Enterprise evidence custody readiness.")
    parser.add_argument("--packet", type=Path, help="Sample or live evidence custody packet JSON.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write validation result JSON.")
    args = parser.parse_args()

    packet = json.loads(args.packet.read_text(encoding="utf-8")) if args.packet else None
    result = build_enterprise_evidence_custody_readiness(packet, require_live=args.require_live)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
