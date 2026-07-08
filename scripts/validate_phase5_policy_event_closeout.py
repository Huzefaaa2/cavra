#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.phase5_closeout import (  # noqa: E402
    build_phase5_closeout_packet,
    validate_phase5_closeout_packet,
    write_phase5_closeout_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the CAVRA Phase 5 policy and event core closeout.")
    parser.add_argument("--packet", type=Path, help="Phase 5 closeout packet JSON.")
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root for artifact validation.")
    parser.add_argument("--export-dir", type=Path, help="Export generated closeout packet and validation result.")
    parser.add_argument(
        "--require-customer-live",
        action="store_true",
        help="Require customer live deployment evidence refs for every R5 gate.",
    )
    parser.add_argument("--output", type=Path, help="Optional validation result JSON.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    if args.export_dir:
        result = write_phase5_closeout_artifacts(repo_root, args.export_dir)
        exit_ok = result["ready_for_phase5_public_contract_release"] is True
    else:
        packet = _read_json(args.packet) if args.packet else build_phase5_closeout_packet(repo_root)
        result = validate_phase5_closeout_packet(
            packet,
            repo_root=repo_root,
            require_customer_live=args.require_customer_live,
        )
        exit_ok = result["ready_for_phase5_public_contract_release"] is True and (
            not args.require_customer_live or result["ready_for_customer_live_phase5_closeout"] is True
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
