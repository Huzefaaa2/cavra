#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cavra.policy_engine import load_policy_file  # noqa: E402
from cavra.policy_lifecycle import (  # noqa: E402
    build_policy_dry_run_report,
    build_policy_lifecycle_plan,
    lint_policy_lifecycle,
    validate_policy_lifecycle_packet,
    write_policy_lifecycle_artifacts,
)
from cavra.policy_registry import PolicyRegistry  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and export CAVRA policy lifecycle evidence.")
    parser.add_argument("--policy-pack", default="cavra-ai-agent-baseline", help="Policy pack ID to load from the registry.")
    parser.add_argument("--policy-file", type=Path, help="Policy YAML path to validate instead of a registry policy pack.")
    parser.add_argument("--previous-policy-pack", help="Previous policy pack ID for version diff and rollback planning.")
    parser.add_argument("--previous-policy-file", type=Path, help="Previous policy YAML path for version diff and rollback planning.")
    parser.add_argument("--sample-actions", type=Path, help="Optional dry-run action fixtures JSON.")
    parser.add_argument("--requested-by", default="policy-owner@example.com", help="Policy lifecycle requestor identity.")
    parser.add_argument("--source-ref", default="git://Huzefaaa2/cavra/main/policies", help="Git/source reference for the policy.")
    parser.add_argument("--review-workflow-ref", default="github://Huzefaaa2/cavra/actions/workflows/policy-lifecycle.yml")
    parser.add_argument("--lint", action="store_true", help="Only emit a lifecycle lint report.")
    parser.add_argument("--dry-run", action="store_true", help="Only emit a lifecycle dry-run report.")
    parser.add_argument("--export-dir", type=Path, help="Write all lifecycle plan artifacts to this directory.")
    parser.add_argument("--packet", type=Path, help="Validate a policy lifecycle readiness packet JSON.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live when validating a packet.")
    parser.add_argument("--output", type=Path, help="Write result JSON to this path.")
    args = parser.parse_args()

    if args.packet:
        result = validate_policy_lifecycle_packet(_read_json(args.packet), require_live=args.require_live)
        _write_or_print(result, args.output)
        return 0 if result["blocker_count"] == 0 and (not args.require_live or result["ready_for_live_policy_lifecycle"]) else 1

    policy = _load_policy(args.policy_pack, args.policy_file)
    previous_policy = _load_previous_policy(args.previous_policy_pack, args.previous_policy_file)
    sample_actions = _load_sample_actions(args.sample_actions)

    if args.lint:
        result = lint_policy_lifecycle(policy)
        _write_or_print(result, args.output)
        return 0 if result["blocker_count"] == 0 else 1

    if args.dry_run:
        result = build_policy_dry_run_report(policy, actions=sample_actions, policy_pack=args.policy_pack)
        _write_or_print(result, args.output)
        return 0 if result["failed_count"] == 0 and result["required_cases_present"] else 1

    plan = build_policy_lifecycle_plan(
        policy,
        previous_policy=previous_policy,
        policy_pack=args.policy_pack,
        sample_actions=sample_actions,
        requested_by=args.requested_by,
        source_ref=args.source_ref,
        review_workflow_ref=args.review_workflow_ref,
    )

    if args.export_dir:
        result = write_policy_lifecycle_artifacts(plan, args.export_dir)
    else:
        result = plan
    _write_or_print(result, args.output)
    return 0


def _load_policy(policy_pack: str, policy_file: Path | None) -> dict[str, Any]:
    if policy_file:
        return load_policy_file(policy_file)
    return PolicyRegistry().load_policy(policy_pack)


def _load_previous_policy(policy_pack: str | None, policy_file: Path | None) -> dict[str, Any] | None:
    if policy_file:
        return load_policy_file(policy_file)
    if policy_pack:
        return PolicyRegistry().load_policy(policy_pack)
    return None


def _load_sample_actions(path: Path | None) -> list[dict[str, Any]] | None:
    if not path:
        return None
    payload = _read_json(path)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("actions"), list):
        return payload["actions"]
    raise ValueError("sample actions JSON must be a list or an object with an actions list")


def _read_json(path: Path) -> dict[str, Any] | list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_or_print(payload: dict[str, Any], output: Path | None) -> None:
    encoded = json.dumps(payload, indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
        print(f"Policy lifecycle validation written: {output}")
        return
    print(encoded, end="")


if __name__ == "__main__":
    raise SystemExit(main())
