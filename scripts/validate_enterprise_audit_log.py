#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.audit_log import (  # noqa: E402
    build_enterprise_audit_log_readiness,
    validate_enterprise_audit_log_packet,
    verify_append_only_audit_log,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA Enterprise append-only audit-log readiness.")
    parser.add_argument("--packet", type=Path, help="Sample or live audit-log readiness packet JSON.")
    parser.add_argument("--log", type=Path, help="Optional append-only JSONL audit log to verify.")
    parser.add_argument("--key", help="Optional HMAC key for audit record signature verification.")
    parser.add_argument("--key-id", help="Expected HMAC key ID.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write validation result JSON.")
    args = parser.parse_args()

    if args.log:
        result = verify_append_only_audit_log(args.log, key=args.key, key_id=args.key_id)
        exit_ok = result["valid"]
    elif args.packet:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_enterprise_audit_log_packet(packet, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0
    else:
        result = build_enterprise_audit_log_readiness(require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
