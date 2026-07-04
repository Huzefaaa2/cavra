#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.connector_sdk import (  # noqa: E402
    build_connector_certification_packet,
    build_connector_compatibility_matrix,
    build_enterprise_connector_sdk_readiness,
    validate_connector_manifest,
    validate_enterprise_connector_sdk_packet,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA connector SDK manifests and readiness packets.")
    parser.add_argument("--manifest", type=Path, help="Connector SDK manifest JSON.")
    parser.add_argument("--packet", type=Path, help="Connector SDK readiness packet JSON.")
    parser.add_argument("--matrix", nargs="*", type=Path, help="One or more connector manifests for a compatibility matrix.")
    parser.add_argument("--certify", action="store_true", help="Emit certification packet for the selected manifest.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.matrix:
        manifests = [json.loads(path.read_text(encoding="utf-8")) for path in args.matrix]
        result = build_connector_compatibility_matrix(manifests)
        exit_ok = result["valid_connector_count"] == result["connector_count"]
    elif args.manifest and args.certify:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = build_connector_certification_packet(manifest)
        exit_ok = result["certified"] is True
    elif args.manifest:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = validate_connector_manifest(manifest)
        exit_ok = result["valid"] is True
    elif args.packet:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_enterprise_connector_sdk_packet(packet, require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0
    else:
        result = build_enterprise_connector_sdk_readiness(require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
