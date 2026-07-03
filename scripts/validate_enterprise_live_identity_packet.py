#!/usr/bin/env python3
"""Validate a public-safe Enterprise live identity validation packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.enterprise_identity import load_enterprise_live_identity_packet, validate_enterprise_live_identity_packet


DEFAULT_PACKET = Path("examples/identity/enterprise-live-identity-validation.sample.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--packet",
        type=Path,
        default=DEFAULT_PACKET,
        help="Path to a sanitized Enterprise live identity validation packet.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the validation result JSON.",
    )
    parser.add_argument(
        "--allow-not-ready",
        action="store_true",
        help="Return success even when the packet is structurally valid but not live-ready.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = load_enterprise_live_identity_packet(args.packet)
    result = validate_enterprise_live_identity_packet(packet)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["ready_for_live_enterprise_identity"] or args.allow_not_ready:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
