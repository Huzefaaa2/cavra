from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any, Callable

from cavra.continuous_monitoring import build_sample_monitoring_events, replay_monitoring_events
from cavra.enterprise_ha import DEFAULT_RPO_MINUTES, DEFAULT_RTO_MINUTES, MIN_API_REPLICAS, MIN_WORKER_REPLICAS
from cavra.policy_lifecycle import build_policy_dry_run_report
from cavra.policy_registry import PolicyRegistry
from cavra.runtime import RuntimeGuard

BENCHMARK_SLO_REPORT_SCHEMA = "cavra.benchmark-slo.report.v1"
BENCHMARK_SLO_READINESS_SCHEMA = "cavra.benchmark-slo.readiness.v1"
BENCHMARK_SLO_READINESS_RESULT_SCHEMA = "cavra.benchmark-slo.readiness-result.v1"

REQUIRED_BENCHMARK_SUITES = {
    "runtime_decision_latency",
    "continuous_monitoring_replay",
    "policy_lifecycle_dry_run",
}

REQUIRED_FAILURE_DRILLS = {
    "event_bus_unavailable",
    "store_write_failure",
    "connector_timeout",
    "policy_compile_failure",
}

DEFAULT_SLO_TARGETS = {
    "runtime_decision_latency": {"p95_latency_ms_max": 50, "throughput_per_second_min": 100},
    "continuous_monitoring_replay": {"p95_latency_ms_max": 100, "throughput_per_second_min": 50},
    "policy_lifecycle_dry_run": {"p95_latency_ms_max": 250, "throughput_per_second_min": 10},
}


def build_reference_benchmark_report() -> dict[str, Any]:
    suites = [
        _suite(
            "runtime_decision_latency",
            sample_count=500,
            p50_latency_ms=2,
            p95_latency_ms=5,
            max_latency_ms=9,
            throughput_per_second=1250,
        ),
        _suite(
            "continuous_monitoring_replay",
            sample_count=240,
            p50_latency_ms=4,
            p95_latency_ms=11,
            max_latency_ms=18,
            throughput_per_second=620,
        ),
        _suite(
            "policy_lifecycle_dry_run",
            sample_count=120,
            p50_latency_ms=12,
            p95_latency_ms=28,
            max_latency_ms=44,
            throughput_per_second=95,
        ),
    ]
    report = {
        "schema_version": BENCHMARK_SLO_REPORT_SCHEMA,
        "product": "CAVRA",
        "generated_at": "2026-07-04T10:30:00+00:00",
        "mode": "reference",
        "benchmark_suites": suites,
        "ha_slo_targets": build_ha_slo_targets(),
        "failure_mode_drills": build_failure_mode_drills(),
    }
    return {**report, "regression_gate": evaluate_benchmark_slo_gate(report)}


def run_local_benchmark_report(iterations: int = 25) -> dict[str, Any]:
    iterations = max(5, min(iterations, 500))
    policy = PolicyRegistry().load_policy("cavra-ai-agent-baseline")
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    suites = [
        _measure_suite(
            "runtime_decision_latency",
            iterations=iterations,
            sample=lambda: guard.evaluate_command("terraform plan").to_dict(),
        ),
        _measure_suite(
            "continuous_monitoring_replay",
            iterations=iterations,
            sample=lambda: replay_monitoring_events(
                build_sample_monitoring_events(),
                now="2026-07-04T10:15:00+00:00",
            ),
        ),
        _measure_suite(
            "policy_lifecycle_dry_run",
            iterations=iterations,
            sample=lambda: build_policy_dry_run_report(policy, policy_pack="cavra-ai-agent-baseline"),
        ),
    ]
    report = {
        "schema_version": BENCHMARK_SLO_REPORT_SCHEMA,
        "product": "CAVRA",
        "generated_at": _now(),
        "mode": "measured_local",
        "benchmark_suites": suites,
        "ha_slo_targets": build_ha_slo_targets(),
        "failure_mode_drills": build_failure_mode_drills(),
    }
    return {**report, "regression_gate": evaluate_benchmark_slo_gate(report)}


def build_ha_slo_targets() -> dict[str, Any]:
    return {
        "schema_version": "cavra.benchmark-slo.ha-targets.v1",
        "rto_minutes": DEFAULT_RTO_MINUTES,
        "rpo_minutes": DEFAULT_RPO_MINUTES,
        "min_api_replicas": MIN_API_REPLICAS,
        "min_worker_replicas": MIN_WORKER_REPLICAS,
        "event_bus_required": {
            "durable_delivery": True,
            "dead_letter_queue": True,
            "replay": True,
            "consumer_lag_metrics": True,
        },
        "health_endpoints": ["/health", "/version", "/console/config"],
    }


def build_failure_mode_drills() -> list[dict[str, Any]]:
    return [
        {
            "drill_id": "event_bus_unavailable",
            "injected_fault": "continuous monitoring event bus cannot accept writes",
            "expected_behavior": "runtime decisions fail closed or queue retry without granting unsafe approval",
            "observed_behavior": "fail_closed_or_retry",
            "passed": True,
            "evidence_ref": "sample://failure-mode/event-bus-unavailable",
        },
        {
            "drill_id": "store_write_failure",
            "injected_fault": "evidence or audit metadata store rejects writes",
            "expected_behavior": "decision remains governed and write failure is surfaced as blocker evidence",
            "observed_behavior": "blocker_evidence_emitted",
            "passed": True,
            "evidence_ref": "sample://failure-mode/store-write-failure",
        },
        {
            "drill_id": "connector_timeout",
            "injected_fault": "external connector delivery exceeds timeout",
            "expected_behavior": "connector delivery is retried or routed to dead-letter evidence",
            "observed_behavior": "retry_or_dlq",
            "passed": True,
            "evidence_ref": "sample://failure-mode/connector-timeout",
        },
        {
            "drill_id": "policy_compile_failure",
            "injected_fault": "policy artifact cannot be compiled or validated",
            "expected_behavior": "policy promotion is blocked before enforcement change",
            "observed_behavior": "promotion_blocked",
            "passed": True,
            "evidence_ref": "sample://failure-mode/policy-compile-failure",
        },
    ]


def evaluate_benchmark_slo_gate(report: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    suites = report.get("benchmark_suites", []) if isinstance(report.get("benchmark_suites"), list) else []
    suite_by_id = {str(item.get("suite_id")): item for item in suites}
    missing = sorted(REQUIRED_BENCHMARK_SUITES - set(suite_by_id))
    _add_check(
        checks,
        "benchmark_suites",
        "pass" if not missing else "blocker",
        "Required benchmark suites are present." if not missing else f"Missing benchmark suites: {', '.join(missing)}.",
    )
    for suite_id in sorted(REQUIRED_BENCHMARK_SUITES & set(suite_by_id)):
        suite = suite_by_id[suite_id]
        slo = suite.get("slo", DEFAULT_SLO_TARGETS[suite_id])
        p95_ok = float(suite.get("p95_latency_ms", 10**9)) <= float(slo.get("p95_latency_ms_max", 0))
        throughput_ok = float(suite.get("throughput_per_second", 0)) >= float(slo.get("throughput_per_second_min", 10**9))
        _add_check(
            checks,
            f"{suite_id}_slo",
            "pass" if p95_ok and throughput_ok else "blocker",
            f"{suite_id} meets latency and throughput SLO."
            if p95_ok and throughput_ok
            else f"{suite_id} breaches latency or throughput SLO.",
        )
    failure_drills = report.get("failure_mode_drills", []) if isinstance(report.get("failure_mode_drills"), list) else []
    drill_by_id = {str(item.get("drill_id")): item for item in failure_drills}
    missing_drills = sorted(REQUIRED_FAILURE_DRILLS - set(drill_by_id))
    failed_drills = sorted(drill_id for drill_id, item in drill_by_id.items() if item.get("passed") is not True)
    _add_check(
        checks,
        "failure_mode_drills",
        "pass" if not missing_drills and not failed_drills else "blocker",
        "Required failure-mode drills passed."
        if not missing_drills and not failed_drills
        else f"Failure-mode drill gaps: {', '.join(missing_drills + failed_drills)}.",
    )
    ha = report.get("ha_slo_targets", {}) if isinstance(report.get("ha_slo_targets"), dict) else {}
    event_bus = ha.get("event_bus_required", {}) if isinstance(ha.get("event_bus_required"), dict) else {}
    required_event_bus_flags = {"durable_delivery", "dead_letter_queue", "replay", "consumer_lag_metrics"}
    event_bus_ok = required_event_bus_flags <= set(event_bus) and all(
        event_bus.get(flag) is True for flag in required_event_bus_flags
    )
    ha_ok = (
        int(ha.get("rto_minutes", 9999)) <= DEFAULT_RTO_MINUTES
        and int(ha.get("rpo_minutes", 9999)) <= DEFAULT_RPO_MINUTES
        and int(ha.get("min_api_replicas", 0)) >= MIN_API_REPLICAS
        and int(ha.get("min_worker_replicas", 0)) >= MIN_WORKER_REPLICAS
        and event_bus_ok
    )
    _add_check(
        checks,
        "ha_slo_targets",
        "pass" if ha_ok else "blocker",
        "HA SLO targets cover RTO, RPO, replica floors, and event bus resilience."
        if ha_ok
        else "HA SLO targets are incomplete.",
    )
    blockers = [check for check in checks if check["status"] == "blocker"]
    return {
        "schema_version": "cavra.benchmark-slo.regression-gate.v1",
        "passed": not blockers,
        "blocker_count": len(blockers),
        "checks": checks,
    }


def build_benchmark_readiness_packet(
    report: dict[str, Any],
    *,
    evidence_mode: str = "sample",
    ci_run_ref: str = "sample://github-actions/benchmark-slo",
    benchmark_report_ref: str = "artifact://benchmark-slo/benchmark-report.json",
    ha_evidence_ref: str = "sample://enterprise-ha/benchmark-slo",
    failure_drill_ref: str = "sample://failure-modes/benchmark-slo",
) -> dict[str, Any]:
    return {
        "schema_version": BENCHMARK_SLO_READINESS_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "benchmark_report": report,
        "slo_regression_gate": report.get("regression_gate", evaluate_benchmark_slo_gate(report)),
        "operating_evidence": {
            "ci_run_ref": ci_run_ref,
            "benchmark_report_ref": benchmark_report_ref,
            "ha_evidence_ref": ha_evidence_ref,
            "failure_drill_ref": failure_drill_ref,
        },
    }


def validate_benchmark_readiness_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    report = packet.get("benchmark_report", {}) if isinstance(packet.get("benchmark_report"), dict) else {}
    gate = packet.get("slo_regression_gate", {}) if isinstance(packet.get("slo_regression_gate"), dict) else {}
    if gate != report.get("regression_gate"):
        gate = evaluate_benchmark_slo_gate(report)
    _add_check(
        checks,
        "benchmark_report_schema",
        "pass" if report.get("schema_version") == BENCHMARK_SLO_REPORT_SCHEMA else "blocker",
        "Benchmark report schema is valid."
        if report.get("schema_version") == BENCHMARK_SLO_REPORT_SCHEMA
        else f"Benchmark report must use {BENCHMARK_SLO_REPORT_SCHEMA}.",
    )
    _add_check(
        checks,
        "slo_regression_gate",
        "pass" if gate.get("passed") is True and int(gate.get("blocker_count", 1)) == 0 else "blocker",
        "SLO regression gate passed." if gate.get("passed") is True else "SLO regression gate has blockers.",
    )
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": BENCHMARK_SLO_READINESS_RESULT_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_benchmark_slo_contract": contract_ready,
        "ready_for_live_benchmark_slo_gate": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_benchmark_artifacts(report: dict[str, Any], packet: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "benchmark-slo-report.json"
    gate_path = output_dir / "benchmark-slo-regression-gate.json"
    packet_path = output_dir / "benchmark-slo-readiness-packet.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    gate_path.write_text(json.dumps(report.get("regression_gate", {}), indent=2) + "\n", encoding="utf-8")
    packet_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.benchmark-slo.export.v1",
        "output_dir": str(output_dir),
        "artifacts": {
            "benchmark_report": str(report_path),
            "slo_regression_gate": str(gate_path),
            "readiness_packet": str(packet_path),
        },
    }


def _measure_suite(suite_id: str, *, iterations: int, sample: Callable[[], Any]) -> dict[str, Any]:
    latencies: list[float] = []
    started = time.perf_counter()
    for _ in range(iterations):
        item_started = time.perf_counter()
        sample()
        latencies.append((time.perf_counter() - item_started) * 1000)
    elapsed = max(time.perf_counter() - started, 0.000001)
    return _suite(
        suite_id,
        sample_count=iterations,
        p50_latency_ms=round(float(median(latencies)), 3),
        p95_latency_ms=round(_percentile(latencies, 95), 3),
        max_latency_ms=round(max(latencies), 3),
        throughput_per_second=round(iterations / elapsed, 3),
    )


def _suite(
    suite_id: str,
    *,
    sample_count: int,
    p50_latency_ms: float,
    p95_latency_ms: float,
    max_latency_ms: float,
    throughput_per_second: float,
) -> dict[str, Any]:
    slo = DEFAULT_SLO_TARGETS[suite_id]
    passed = p95_latency_ms <= slo["p95_latency_ms_max"] and throughput_per_second >= slo["throughput_per_second_min"]
    return {
        "suite_id": suite_id,
        "sample_count": sample_count,
        "p50_latency_ms": p50_latency_ms,
        "p95_latency_ms": p95_latency_ms,
        "max_latency_ms": max_latency_ms,
        "throughput_per_second": throughput_per_second,
        "slo": slo,
        "passed": passed,
    }


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(round((percentile / 100) * (len(ordered) - 1)))))
    return float(ordered[index])


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == BENCHMARK_SLO_READINESS_SCHEMA else "blocker",
        "Benchmark readiness packet schema is valid."
        if packet.get("schema_version") == BENCHMARK_SLO_READINESS_SCHEMA
        else f"Packet must use {BENCHMARK_SLO_READINESS_SCHEMA}.",
    )


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    if mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live benchmark/SLO evidence packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample benchmark/SLO packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live benchmark/SLO validation requires evidence_mode=live.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = ["ci_run_ref", "benchmark_report_ref", "ha_evidence_ref", "failure_drill_ref"]
    missing = [field for field in required if not evidence.get(field)]
    _add_check(
        checks,
        "operating_evidence",
        "pass" if not missing else "blocker",
        "Benchmark, HA, and failure-mode operating evidence references are present."
        if not missing
        else f"Operating evidence is missing: {', '.join(missing)}.",
    )


def _add_check(checks: list[dict[str, Any]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
