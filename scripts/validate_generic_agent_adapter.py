#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.generic_agent_adapter import (  # noqa: E402
    build_action_taxonomy,
    build_generic_adapter_readiness_packet,
    build_sample_adapter_manifest,
    build_sample_generic_actions,
    evaluate_generic_actions,
    validate_adapter_manifest,
    validate_generic_adapter_readiness_packet,
    write_generic_adapter_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA generic agent adapter taxonomy and evidence.")
    parser.add_argument("--taxonomy", action="store_true", help="Emit the public generic action taxonomy.")
    parser.add_argument("--manifest", type=Path, help="Validate a generic adapter manifest JSON.")
    parser.add_argument("--actions", type=Path, help="Evaluate generic agent actions JSON.")
    parser.add_argument("--packet", type=Path, help="Validate a generic adapter readiness packet JSON.")
    parser.add_argument("--export-dir", type=Path, help="Export reference manifest, action, evaluation, and packet artifacts.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.manifest:
        result = validate_adapter_manifest(_read_json(args.manifest))
        exit_ok = result["valid"] is True
    elif args.actions:
        payload = _read_json(args.actions)
        actions = payload.get("actions", payload) if isinstance(payload, dict) else payload
        result = evaluate_generic_actions(actions)
        counts = result["decision_counts"]
        exit_ok = counts.get("allow", 0) >= 1 and counts.get("require_approval", 0) >= 1 and counts.get("block", 0) >= 1
    elif args.packet:
        result = validate_generic_adapter_readiness_packet(_read_json(args.packet), require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0 and (not args.require_live or result["ready_for_live_generic_adapter_sdk"])
    elif args.export_dir:
        manifest = build_sample_adapter_manifest()
        actions = build_sample_generic_actions()
        export = write_generic_adapter_artifacts(manifest, actions, args.export_dir)
        result = export
        exit_ok = True
    elif args.taxonomy:
        result = build_action_taxonomy()
        exit_ok = True
    else:
        manifest = build_sample_adapter_manifest()
        actions = build_sample_generic_actions()
        evaluations = evaluate_generic_actions(actions)
        result = build_generic_adapter_readiness_packet(manifest, evaluations)
        exit_ok = True

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if exit_ok else 1


def _read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
