#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.compliance_packs import (  # noqa: E402
    build_compliance_mapping_report,
    build_compliance_pack_registry,
    build_enterprise_compliance_pack_readiness,
    validate_compliance_pack,
    validate_enterprise_compliance_pack_packet,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA Enterprise compliance mapping-pack readiness.")
    parser.add_argument("--packet", type=Path, help="Sample or live compliance mapping-pack readiness packet JSON.")
    parser.add_argument("--findings", type=Path, help="Optional findings JSON array to map to compliance clauses.")
    parser.add_argument("--registry", action="store_true", help="Emit built-in compliance pack registry.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.registry:
        result = build_compliance_pack_registry()
        exit_ok = all(validate_compliance_pack(pack)["valid"] for pack in result["packs"])
    elif args.findings:
        findings = json.loads(args.findings.read_text(encoding="utf-8"))
        result = build_compliance_mapping_report(findings)
        exit_ok = result["unmapped_finding_count"] == 0
    elif args.packet:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_enterprise_compliance_pack_packet(packet, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0
    else:
        result = build_enterprise_compliance_pack_readiness(require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
