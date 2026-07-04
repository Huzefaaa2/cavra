#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.certified_connectors import (  # noqa: E402
    build_priority_connector_registry,
    validate_certified_connectors_packet,
    validate_priority_connector_registry,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA priority certified connectors.")
    parser.add_argument("--registry", action="store_true", help="Validate the built-in priority certified connector registry.")
    parser.add_argument("--manifest-dir", type=Path, help="Directory containing checked-in priority connector manifests.")
    parser.add_argument("--packet", type=Path, help="Certified connector readiness packet JSON.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.packet:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_certified_connectors_packet(packet, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0
    elif args.manifest_dir:
        manifests = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(args.manifest_dir.glob("*.json"))
        ]
        result = validate_priority_connector_registry(manifests)
        exit_ok = result["valid"] is True
    else:
        registry = build_priority_connector_registry()
        result = {
            "schema_version": "cavra.certified-connectors.registry-result.v1",
            "registry": registry,
            "validation": validate_priority_connector_registry(registry["manifests"]),
        }
        exit_ok = result["validation"]["valid"] is True

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
