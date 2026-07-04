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

from cavra.benchmark_slo import (  # noqa: E402
    build_benchmark_readiness_packet,
    build_reference_benchmark_report,
    evaluate_benchmark_slo_gate,
    run_local_benchmark_report,
    validate_benchmark_readiness_packet,
    write_benchmark_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA benchmark and SLO regression evidence.")
    parser.add_argument("--measured", action="store_true", help="Run a measured local benchmark instead of reference fixtures.")
    parser.add_argument("--iterations", type=int, default=25, help="Iterations for measured local benchmark mode.")
    parser.add_argument("--report", type=Path, help="Validate a benchmark report JSON.")
    parser.add_argument("--packet", type=Path, help="Validate a benchmark readiness packet JSON.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--export-dir", type=Path, help="Write benchmark report, gate, and readiness packet artifacts.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.packet:
        result = validate_benchmark_readiness_packet(_read_json(args.packet), require_live=args.require_live)
        _write_or_print(result, args.output)
        return 0 if result["blocker_count"] == 0 and (not args.require_live or result["ready_for_live_benchmark_slo_gate"]) else 1

    if args.report:
        report = _read_json(args.report)
        result = evaluate_benchmark_slo_gate(report)
        _write_or_print(result, args.output)
        return 0 if result["passed"] else 1

    report = run_local_benchmark_report(args.iterations) if args.measured else build_reference_benchmark_report()
    packet = build_benchmark_readiness_packet(report)
    result: dict[str, Any]
    if args.export_dir:
        result = write_benchmark_artifacts(report, packet, args.export_dir)
    else:
        result = report
    _write_or_print(result, args.output)
    return 0 if report.get("regression_gate", {}).get("passed") else 1


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_or_print(payload: dict[str, Any], output: Path | None) -> None:
    encoded = json.dumps(payload, indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
        print(f"Benchmark/SLO validation written: {output}")
        return
    print(encoded, end="")


if __name__ == "__main__":
    raise SystemExit(main())
