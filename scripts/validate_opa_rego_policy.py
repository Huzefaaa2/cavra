#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cavra.opa_rego_policy import (  # noqa: E402
    build_rego_policy_bundle,
    evaluate_rego_compatible_policy,
    load_policy_for_rego,
    run_rego_parity_report,
    validate_opa_rego_policy_packet,
    write_rego_bundle,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate CAVRA OPA/Rego policy compatibility.")
    parser.add_argument("--policy-pack", default="cavra-ai-agent-baseline", help="Policy pack ID to compile.")
    parser.add_argument("--overlay", action="append", type=Path, default=[], help="Optional policy overlay YAML or pack dir.")
    parser.add_argument("--bundle", action="store_true", help="Build and print the full Rego compatibility bundle.")
    parser.add_argument("--export-dir", type=Path, help="Write Rego module, data, fixtures, parity report, and manifest.")
    parser.add_argument("--parity", action="store_true", help="Run Rego/Python parity fixtures.")
    parser.add_argument("--input", type=Path, help="Evaluate a single OPA input JSON file through the compatibility evaluator.")
    parser.add_argument("--packet", type=Path, help="Validate an OPA/Rego readiness packet JSON.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live for readiness packet validation.")
    parser.add_argument("--output", type=Path, help="Write JSON result to this path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result: dict[str, Any]
    if args.packet:
        result = validate_opa_rego_policy_packet(_read_json(args.packet), require_live=args.require_live)
        ok = result["blocker_count"] == 0 and (not args.require_live or result["ready_for_live_opa_rego_policy_path"])
    elif args.input:
        policy = load_policy_for_rego(args.policy_pack, overlays=args.overlay)
        result = {
            "schema_version": "cavra.opa-rego-policy.input-evaluation.v1",
            "policy_pack": args.policy_pack,
            "decision": evaluate_rego_compatible_policy(policy, _read_json(args.input)),
        }
        ok = True
    elif args.parity:
        result = run_rego_parity_report(policy_pack=args.policy_pack)
        ok = bool(result["passed"])
    else:
        bundle = build_rego_policy_bundle(args.policy_pack, overlays=args.overlay)
        if args.export_dir:
            result = write_rego_bundle(bundle, args.export_dir)
        else:
            result = bundle if args.bundle else bundle["parity_report"]
        ok = bool(bundle["parity_report"]["passed"])

    _write_result(result, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if ok else 1


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _write_result(result: dict[str, Any], output: Path | None) -> None:
    if output is None:
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
