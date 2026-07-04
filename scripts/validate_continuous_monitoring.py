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

from cavra.continuous_monitoring import (  # noqa: E402
    DEFAULT_BASE_TIME,
    build_continuous_monitoring_readiness_packet,
    build_sample_monitoring_events,
    replay_monitoring_events,
    validate_continuous_monitoring_packet,
    write_continuous_monitoring_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAVRA continuous monitoring events and readiness packets.")
    parser.add_argument("--events", type=Path, help="Continuous monitoring event stream JSON.")
    parser.add_argument("--build-sample", action="store_true", help="Build the deterministic public sample event stream.")
    parser.add_argument("--replay", action="store_true", help="Replay and validate an event stream.")
    parser.add_argument("--packet", type=Path, help="Validate a continuous monitoring readiness packet JSON.")
    parser.add_argument("--require-live", action="store_true", help="Require evidence_mode=live and fail on sample packets.")
    parser.add_argument("--latency-slo-ms", type=int, default=5000, help="Event processing latency SLO in milliseconds.")
    parser.add_argument("--stale-after-minutes", type=int, default=60, help="Stale assessment threshold in minutes.")
    parser.add_argument("--now", default=DEFAULT_BASE_TIME, help="ISO-8601 timestamp used for replay freshness checks.")
    parser.add_argument("--export-dir", type=Path, help="Write sample events, replay report, and readiness packet.")
    parser.add_argument("--output", type=Path, help="Optional path to write result JSON.")
    args = parser.parse_args()

    if args.packet:
        packet = _read_json(args.packet)
        result = validate_continuous_monitoring_packet(packet, require_live=args.require_live)
        _write_or_print(result, args.output)
        return 0 if result["blocker_count"] == 0 and (not args.require_live or result["ready_for_live_continuous_monitoring"]) else 1

    events = build_sample_monitoring_events() if args.build_sample or not args.events else _load_events(args.events)
    replay = replay_monitoring_events(
        events,
        now=args.now,
        latency_slo_ms=args.latency_slo_ms,
        stale_after_minutes=args.stale_after_minutes,
    )

    if args.export_dir:
        packet = build_continuous_monitoring_readiness_packet(replay)
        result = write_continuous_monitoring_artifacts(
            events=events,
            replay_report=replay,
            readiness_packet=packet,
            output_dir=args.export_dir,
        )
    elif args.replay:
        result = replay
    else:
        result = events

    _write_or_print(result, args.output)
    if isinstance(result, dict) and result.get("schema_version") == "cavra.continuous-monitoring.replay-report.v1":
        return 0 if _replay_ok(result) else 1
    return 0


def _load_events(path: Path) -> list[dict[str, Any]]:
    payload = _read_json(path)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("events"), list):
        return payload["events"]
    raise ValueError("events JSON must be a list or an object with an events list")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_or_print(payload: Any, output: Path | None) -> None:
    encoded = json.dumps(payload, indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
        print(f"Continuous monitoring validation written: {output}")
        return
    print(encoded, end="")


def _replay_ok(report: dict[str, Any]) -> bool:
    return (
        report.get("required_event_types_present") is True
        and int(report.get("invalid_event_count", 1)) == 0
        and int(report.get("latency_summary", {}).get("violation_count", 1)) == 0
        and int(report.get("stale_assessment", {}).get("stale_count", 1)) == 0
    )


if __name__ == "__main__":
    raise SystemExit(main())
