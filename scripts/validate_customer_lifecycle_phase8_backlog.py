#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cavra.customer_lifecycle_phase8_backlog import (  # noqa: E402
    build_customer_lifecycle_phase8_backlog_packet,
    validate_customer_lifecycle_phase8_backlog_packet,
    write_customer_lifecycle_phase8_backlog_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA customer lifecycle Phase 8 backlog readiness.")
    parser.add_argument("--packet", type=Path, help="Optional customer lifecycle Phase 8 backlog packet JSON.")
    parser.add_argument("--retrospective", type=Path, help="Optional customer lifecycle retrospective packet JSON.")
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="Repository root used for retrospective generation.")
    parser.add_argument("--export-dir", type=Path, help="Optional directory to export sample/live Phase 8 backlog packets.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and sanitized=true.")
    parser.add_argument("--output", type=Path, help="Optional path for the validation result JSON.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    if args.export_dir:
        result = write_customer_lifecycle_phase8_backlog_artifacts(args.export_dir, repo_root)
    else:
        if args.packet:
            packet = json.loads(args.packet.read_text(encoding="utf-8"))
        else:
            retrospective = json.loads(args.retrospective.read_text(encoding="utf-8")) if args.retrospective else None
            packet = build_customer_lifecycle_phase8_backlog_packet(
                retrospective,
                repo_root=repo_root,
                evidence_mode="live" if args.require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=args.require_live)

    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")

    if args.export_dir:
        return 0 if result.get("ready_for_customer_lifecycle_phase8_backlog") else 1
    return 0 if result.get("blocker_count", 1) == 0 and (
        not args.require_live or result.get("ready_for_customer_lifecycle_phase8_backlog")
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
