from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from cavra.benchmark_slo import (
    REQUIRED_BENCHMARK_SUITES,
    REQUIRED_FAILURE_DRILLS,
    BENCHMARK_SLO_REPORT_SCHEMA,
    build_benchmark_readiness_packet,
    build_reference_benchmark_report,
    evaluate_benchmark_slo_gate,
    run_local_benchmark_report,
    validate_benchmark_readiness_packet,
    write_benchmark_artifacts,
)


SAMPLE_PACKET = Path("examples/benchmark-slo/enterprise-benchmark-slo.sample.json")
LIVE_PACKET = Path("examples/benchmark-slo/enterprise-benchmark-slo.live.sanitized.example.json")


def test_reference_benchmark_report_passes_gate() -> None:
    report = build_reference_benchmark_report()

    assert report["schema_version"] == BENCHMARK_SLO_REPORT_SCHEMA
    assert REQUIRED_BENCHMARK_SUITES <= {suite["suite_id"] for suite in report["benchmark_suites"]}
    assert REQUIRED_FAILURE_DRILLS <= {drill["drill_id"] for drill in report["failure_mode_drills"]}
    assert report["regression_gate"]["passed"] is True
    assert report["regression_gate"]["blocker_count"] == 0


def test_local_measured_benchmark_report_has_required_shape() -> None:
    report = run_local_benchmark_report(iterations=5)

    assert report["schema_version"] == BENCHMARK_SLO_REPORT_SCHEMA
    assert report["mode"] == "measured_local"
    assert REQUIRED_BENCHMARK_SUITES <= {suite["suite_id"] for suite in report["benchmark_suites"]}
    assert "regression_gate" in report


def test_benchmark_gate_blocks_latency_regression() -> None:
    report = build_reference_benchmark_report()
    report["benchmark_suites"][0]["p95_latency_ms"] = 5000

    gate = evaluate_benchmark_slo_gate(report)

    assert gate["passed"] is False
    assert any(check["name"] == "runtime_decision_latency_slo" for check in gate["checks"])


def test_benchmark_gate_blocks_throughput_regression() -> None:
    report = build_reference_benchmark_report()
    report["benchmark_suites"][1]["throughput_per_second"] = 0

    gate = evaluate_benchmark_slo_gate(report)

    assert gate["passed"] is False
    assert any(check["name"] == "continuous_monitoring_replay_slo" for check in gate["checks"])


def test_benchmark_gate_blocks_incomplete_ha_targets() -> None:
    report = build_reference_benchmark_report()
    report["ha_slo_targets"]["min_api_replicas"] = 1
    report["ha_slo_targets"]["event_bus_required"] = {"durable_delivery": True}

    gate = evaluate_benchmark_slo_gate(report)

    assert gate["passed"] is False
    assert any(check["name"] == "ha_slo_targets" for check in gate["checks"])


def test_benchmark_gate_blocks_failed_failure_drill() -> None:
    report = build_reference_benchmark_report()
    report["failure_mode_drills"][0]["passed"] = False

    gate = evaluate_benchmark_slo_gate(report)

    assert gate["passed"] is False
    assert any(check["name"] == "failure_mode_drills" for check in gate["checks"])


def test_benchmark_sample_packet_validates_with_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_benchmark_readiness_packet(packet)

    assert result["ready_for_benchmark_slo_contract"] is True
    assert result["ready_for_live_benchmark_slo_gate"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1


def test_benchmark_live_packet_passes_live_gate() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))

    result = validate_benchmark_readiness_packet(packet, require_live=True)

    assert result["ready_for_benchmark_slo_contract"] is True
    assert result["ready_for_live_benchmark_slo_gate"] is True
    assert result["blocker_count"] == 0


def test_benchmark_readiness_blocks_missing_operating_evidence() -> None:
    packet = build_benchmark_readiness_packet(build_reference_benchmark_report(), evidence_mode="live")
    packet = deepcopy(packet)
    packet["operating_evidence"]["ha_evidence_ref"] = ""

    result = validate_benchmark_readiness_packet(packet, require_live=True)

    assert result["ready_for_live_benchmark_slo_gate"] is False
    assert result["blocker_count"] == 1
    assert any(check["name"] == "operating_evidence" for check in result["checks"])


def test_write_benchmark_artifacts(tmp_path: Path) -> None:
    report = build_reference_benchmark_report()
    packet = build_benchmark_readiness_packet(report)

    export = write_benchmark_artifacts(report, packet, tmp_path)

    assert Path(export["artifacts"]["benchmark_report"]).exists()
    assert Path(export["artifacts"]["slo_regression_gate"]).exists()
    assert Path(export["artifacts"]["readiness_packet"]).exists()
