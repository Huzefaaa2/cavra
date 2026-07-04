#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.ai_red_team import (  # noqa: E402
    build_guardrail_test_suite,
    build_sample_ai_artifact_metadata,
    build_ai_red_team_readiness_packet,
    run_guardrail_test_suite,
    run_malicious_model_checks,
    validate_ai_red_team_readiness_packet,
    validate_ai_supply_chain_metadata,
    write_ai_red_team_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA native AI red-team and supply-chain evidence.")
    parser.add_argument("--suite", type=Path, help="Guardrail test suite JSON.")
    parser.add_argument("--artifact", type=Path, help="AI artifact metadata JSON.")
    parser.add_argument("--malicious-model-checks", type=Path, help="AI artifact metadata JSON for malicious model checks.")
    parser.add_argument("--packet", type=Path, help="AI red-team readiness packet JSON.")
    parser.add_argument("--export-dir", type=Path, help="Export reference AI red-team artifacts.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.suite:
        result = run_guardrail_test_suite(_read_json(args.suite))
        exit_ok = result["passed"] is True
    elif args.artifact:
        result = validate_ai_supply_chain_metadata(_read_json(args.artifact))
        exit_ok = result["valid"] is True
    elif args.malicious_model_checks:
        result = run_malicious_model_checks(_read_json(args.malicious_model_checks))
        exit_ok = result["passed"] is True
    elif args.packet:
        result = validate_ai_red_team_readiness_packet(_read_json(args.packet), require_live=args.require_live)
        exit_ok = result["blocker_count"] == 0 and (not args.require_live or result["ready_for_live_ai_red_team_gate"])
    elif args.export_dir:
        result = write_ai_red_team_artifacts(args.export_dir)
        exit_ok = True
    else:
        suite = build_guardrail_test_suite()
        run_report = run_guardrail_test_suite(suite)
        artifact = build_sample_ai_artifact_metadata()
        scan = validate_ai_supply_chain_metadata(artifact)
        malicious = run_malicious_model_checks(artifact)
        result = build_ai_red_team_readiness_packet(suite, run_report, scan, malicious)
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
