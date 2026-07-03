#!/usr/bin/env python3
"""Validate the R2.3 Enterprise HA/DR readiness contract and evidence packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.enterprise_ha import build_enterprise_ha_readiness, validate_enterprise_ha_evidence_packet  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, help="HA/DR evidence packet JSON.")
    parser.add_argument("--output", type=Path, help="Optional path for the readiness result JSON.")
    parser.add_argument("--require-live", action="store_true", help="Require live evidence_mode instead of sample evidence.")
    parser.add_argument("--rto-minutes", type=int, default=60)
    parser.add_argument("--rpo-minutes", type=int, default=15)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.packet:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_enterprise_ha_evidence_packet(
            packet,
            require_live=args.require_live,
            rto_minutes=args.rto_minutes,
            rpo_minutes=args.rpo_minutes,
        )
    else:
        result = build_enterprise_ha_readiness(require_live=args.require_live)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2, sort_keys=True))
    if args.require_live:
        return 0 if result.get("ready_for_enterprise_live_ha") is True else 1
    return 0 if result.get("ready_for_enterprise_ha_contract") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
