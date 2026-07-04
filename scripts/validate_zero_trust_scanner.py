#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.zero_trust_scanner import (  # noqa: E402
    build_zero_trust_scan_result,
    build_zero_trust_scan_result_from_file,
    validate_zero_trust_scan_result,
    validate_zero_trust_scanner_packet,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA zero-trust scanner contract and evidence.")
    parser.add_argument("--scan-result", type=Path, help="Scanner result JSON payload.")
    parser.add_argument("--scan-file", type=Path, help="Build a metadata-only scan result for a local file.")
    parser.add_argument("--build-result", action="store_true", help="Build sanitized scanner result from JSON payload.")
    parser.add_argument("--packet", type=Path, help="Scanner readiness packet JSON.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.packet:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_zero_trust_scanner_packet(packet, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0
    elif args.scan_file:
        result = build_zero_trust_scan_result_from_file(args.scan_file)
        exit_ok = True
    elif args.scan_result and args.build_result:
        payload = json.loads(args.scan_result.read_text(encoding="utf-8"))
        result = build_zero_trust_scan_result(payload)
        exit_ok = True
    elif args.scan_result:
        payload = json.loads(args.scan_result.read_text(encoding="utf-8"))
        result = validate_zero_trust_scan_result(payload)
        exit_ok = result["valid"] is True
    else:
        result = validate_zero_trust_scanner_packet({})
        exit_ok = False

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
