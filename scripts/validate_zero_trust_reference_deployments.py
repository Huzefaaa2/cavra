#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.zero_trust_reference_deployments import (  # noqa: E402
    build_reference_deployment_catalog,
    build_reference_deployment_readiness_packet,
    validate_reference_deployment_catalog,
    validate_reference_deployment_readiness_packet,
    write_reference_deployment_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA zero-trust reference deployments.")
    parser.add_argument("--catalog", type=Path, help="Reference deployment catalog JSON.")
    parser.add_argument("--packet", type=Path, help="Reference deployment readiness packet JSON.")
    parser.add_argument("--repo-root", type=Path, help="Repository root for artifact file validation.")
    parser.add_argument("--export-dir", type=Path, help="Export generated catalog and readiness packets.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve() if args.repo_root else None
    if args.catalog:
        result = validate_reference_deployment_catalog(_read_json(args.catalog), repo_root=repo_root)
        exit_ok = result["valid"] is True
    elif args.packet:
        result = validate_reference_deployment_readiness_packet(
            _read_json(args.packet),
            repo_root=repo_root,
            require_live=args.require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not args.require_live or result["ready_for_live_zero_trust_reference_deployments"]
        )
    elif args.export_dir:
        result = write_reference_deployment_artifacts(args.export_dir)
        exit_ok = True
    else:
        catalog = build_reference_deployment_catalog()
        packet = build_reference_deployment_readiness_packet()
        result = {
            "catalog": catalog,
            "readiness_packet": packet,
        }
        exit_ok = True

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
