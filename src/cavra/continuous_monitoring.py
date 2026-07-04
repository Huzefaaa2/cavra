from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from math import ceil
from pathlib import Path
from typing import Any

CONTINUOUS_MONITORING_EVENT_SCHEMA = "cavra.continuous-monitoring.event.v1"
CONTINUOUS_MONITORING_REPLAY_SCHEMA = "cavra.continuous-monitoring.replay-report.v1"
CONTINUOUS_MONITORING_READINESS_SCHEMA = "cavra.continuous-monitoring.readiness.v1"
CONTINUOUS_MONITORING_READINESS_RESULT_SCHEMA = "cavra.continuous-monitoring.readiness-result.v1"

AGENT_ACTION_EVENT = "cavra.agent.action.decided"
MODEL_REGISTRATION_EVENT = "cavra.model.registry.metadata"
DRIFT_EVENT = "cavra.model.drift.detected"
PRODUCTION_PROMOTION_EVENT = "cavra.production.promotion.requested"

REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES = {
    AGENT_ACTION_EVENT,
    MODEL_REGISTRATION_EVENT,
    DRIFT_EVENT,
    PRODUCTION_PROMOTION_EVENT,
}

REQUIRED_EVENT_BUS_CAPABILITIES = {
    "durable_delivery",
    "dead_letter_queue",
    "replay",
    "idempotency_key",
    "consumer_lag_metrics",
}

DEFAULT_LATENCY_SLO_MS = 5000
DEFAULT_STALE_AFTER_MINUTES = 60
DEFAULT_BASE_TIME = "2026-07-04T10:00:00+00:00"


def build_agent_action_monitoring_event(decision: dict[str, Any]) -> dict[str, Any]:
    return normalize_monitoring_event(
        {
            "event_type": AGENT_ACTION_EVENT,
            "source": "runtime-authority",
            "source_ref": decision.get("decision_id") or decision.get("session_id") or "decision",
            "tenant_id": decision.get("tenant_id", "tenant-public-example"),
            "workspace_id": decision.get("workspace_id", "workspace-ai-governance"),
            "occurred_at": decision.get("timestamp", DEFAULT_BASE_TIME),
            "received_at": decision.get("received_at", decision.get("timestamp", DEFAULT_BASE_TIME)),
            "severity": decision.get("severity", "high"),
            "correlation_id": decision.get("correlation_id", decision.get("session_id", "corr-agent-action")),
            "payload": {
                "decision_id": decision.get("decision_id"),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id"),
                "action_type": decision.get("action_type"),
                "target": decision.get("target"),
                "decision": decision.get("decision"),
                "rule_id": decision.get("rule_id"),
                "evidence_refs": _string_list(decision.get("evidence_refs", [])),
            },
        }
    )


def build_model_registration_monitoring_event(metadata_event: dict[str, Any]) -> dict[str, Any]:
    return normalize_monitoring_event(
        {
            "event_type": MODEL_REGISTRATION_EVENT,
            "source": "model-registry-connector",
            "source_ref": metadata_event.get("model_ref", "model-ref"),
            "tenant_id": metadata_event.get("tenant_id", "tenant-public-example"),
            "workspace_id": metadata_event.get("workspace_id", "workspace-ai-governance"),
            "occurred_at": metadata_event.get("occurred_at", DEFAULT_BASE_TIME),
            "received_at": metadata_event.get("received_at", metadata_event.get("occurred_at", DEFAULT_BASE_TIME)),
            "severity": _risk_to_severity(str(metadata_event.get("risk_tier", "medium"))),
            "correlation_id": metadata_event.get("model_ref", "corr-model-registry"),
            "payload": {
                "registry_provider": metadata_event.get("registry_provider"),
                "model_ref": metadata_event.get("model_ref"),
                "model_version": metadata_event.get("model_version"),
                "artifact_digest": metadata_event.get("artifact_digest"),
                "owner_ref": metadata_event.get("owner_ref"),
                "risk_tier": metadata_event.get("risk_tier"),
                "evidence_ref": metadata_event.get("evidence_ref"),
            },
        }
    )


def build_drift_monitoring_event(payload: dict[str, Any]) -> dict[str, Any]:
    return normalize_monitoring_event(
        {
            "event_type": DRIFT_EVENT,
            "source": payload.get("source", "zero-trust-scanner"),
            "source_ref": payload.get("finding_ref", payload.get("model_ref", "drift-finding")),
            "tenant_id": payload.get("tenant_id", "tenant-public-example"),
            "workspace_id": payload.get("workspace_id", "workspace-ai-governance"),
            "occurred_at": payload.get("occurred_at", DEFAULT_BASE_TIME),
            "received_at": payload.get("received_at", payload.get("occurred_at", DEFAULT_BASE_TIME)),
            "severity": payload.get("severity", "high"),
            "correlation_id": payload.get("correlation_id", payload.get("model_ref", "corr-drift")),
            "payload": {
                "model_ref": payload.get("model_ref"),
                "finding_ref": payload.get("finding_ref"),
                "drift_type": payload.get("drift_type", "risk_score_increase"),
                "risk_score": payload.get("risk_score"),
                "evidence_ref": payload.get("evidence_ref"),
            },
        }
    )


def build_production_promotion_monitoring_event(payload: dict[str, Any]) -> dict[str, Any]:
    return normalize_monitoring_event(
        {
            "event_type": PRODUCTION_PROMOTION_EVENT,
            "source": payload.get("source", "release-governance"),
            "source_ref": payload.get("promotion_ref", payload.get("release_ref", "promotion-request")),
            "tenant_id": payload.get("tenant_id", "tenant-public-example"),
            "workspace_id": payload.get("workspace_id", "workspace-ai-governance"),
            "occurred_at": payload.get("occurred_at", DEFAULT_BASE_TIME),
            "received_at": payload.get("received_at", payload.get("occurred_at", DEFAULT_BASE_TIME)),
            "severity": payload.get("severity", "medium"),
            "correlation_id": payload.get("correlation_id", payload.get("promotion_ref", "corr-promotion")),
            "payload": {
                "promotion_ref": payload.get("promotion_ref"),
                "release_ref": payload.get("release_ref"),
                "target_environment": payload.get("target_environment", "production"),
                "approval_state": payload.get("approval_state", "approved"),
                "evidence_ref": payload.get("evidence_ref"),
            },
        }
    )


def build_sample_monitoring_events() -> list[dict[str, Any]]:
    return [
        build_agent_action_monitoring_event(
            {
                "decision_id": "dec_public_001",
                "session_id": "session_public_001",
                "agent_id": "claude-code",
                "action_type": "execute_command",
                "target": "terraform apply -auto-approve",
                "decision": "block",
                "rule_id": "commands.block",
                "severity": "critical",
                "timestamp": "2026-07-04T10:00:00+00:00",
                "received_at": "2026-07-04T10:00:02+00:00",
                "evidence_refs": ["evidence://runtime/session_public_001"],
            }
        ),
        build_model_registration_monitoring_event(
            {
                "registry_provider": "mlflow",
                "model_ref": "mlflow://workspace-public/fraud-model",
                "model_version": "17",
                "artifact_digest": "sha256:" + "a" * 64,
                "owner_ref": "team-risk",
                "risk_tier": "high",
                "evidence_ref": "evidence://model/fraud-model/17",
                "occurred_at": "2026-07-04T10:04:00+00:00",
                "received_at": "2026-07-04T10:04:03+00:00",
            }
        ),
        build_drift_monitoring_event(
            {
                "model_ref": "mlflow://workspace-public/fraud-model",
                "finding_ref": "finding-public-drift-001",
                "drift_type": "risk_score_increase",
                "risk_score": 82,
                "severity": "high",
                "evidence_ref": "evidence://scanner/finding-public-drift-001",
                "occurred_at": "2026-07-04T10:08:00+00:00",
                "received_at": "2026-07-04T10:08:04+00:00",
            }
        ),
        build_production_promotion_monitoring_event(
            {
                "promotion_ref": "promotion-public-001",
                "release_ref": "cavra-runtime-v1.0.0",
                "target_environment": "production",
                "approval_state": "approved",
                "severity": "medium",
                "evidence_ref": "evidence://release/promotion-public-001",
                "occurred_at": "2026-07-04T10:12:00+00:00",
                "received_at": "2026-07-04T10:12:01+00:00",
            }
        ),
    ]


def normalize_monitoring_event(payload: dict[str, Any]) -> dict[str, Any]:
    event_type = str(payload.get("event_type", "")).strip()
    if event_type not in REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES:
        raise ValueError(f"unsupported monitoring event_type: {event_type}")
    occurred_at = _parse_time(payload.get("occurred_at"), "occurred_at")
    received_at = _parse_time(payload.get("received_at", occurred_at.isoformat()), "received_at")
    if received_at < occurred_at:
        raise ValueError("received_at must be greater than or equal to occurred_at")
    source = str(payload.get("source", "")).strip()
    source_ref = str(payload.get("source_ref", "")).strip()
    if not source or not source_ref:
        raise ValueError("monitoring event requires source and source_ref")
    normalized = {
        "schema_version": CONTINUOUS_MONITORING_EVENT_SCHEMA,
        "event_id": str(payload.get("event_id") or _event_id(event_type, source, source_ref, occurred_at.isoformat())),
        "event_type": event_type,
        "source": source,
        "source_ref": source_ref,
        "tenant_id": str(payload.get("tenant_id", "tenant-public-example")),
        "workspace_id": str(payload.get("workspace_id", "workspace-ai-governance")),
        "occurred_at": occurred_at.isoformat(),
        "received_at": received_at.isoformat(),
        "severity": str(payload.get("severity", "medium")),
        "correlation_id": str(payload.get("correlation_id", source_ref)),
        "idempotency_key": str(payload.get("idempotency_key") or _event_id(event_type, source, source_ref, occurred_at.isoformat())),
        "payload": deepcopy(payload.get("payload", {})) if isinstance(payload.get("payload"), dict) else {},
    }
    if isinstance(payload.get("labels"), dict):
        normalized["labels"] = payload["labels"]
    return normalized


def replay_monitoring_events(
    events: list[dict[str, Any]],
    *,
    now: str | datetime | None = None,
    latency_slo_ms: int = DEFAULT_LATENCY_SLO_MS,
    stale_after_minutes: int = DEFAULT_STALE_AFTER_MINUTES,
) -> dict[str, Any]:
    observed_at = _parse_time(now or DEFAULT_BASE_TIME, "now")
    accepted: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    seen: set[str] = set()

    for index, event in enumerate(events):
        try:
            normalized = normalize_monitoring_event(event)
        except ValueError as exc:
            invalid.append({"index": index, "message": str(exc)})
            continue
        dedupe_key = str(normalized.get("idempotency_key") or normalized["event_id"])
        if dedupe_key in seen:
            duplicates.append({"index": index, "event_id": normalized["event_id"], "idempotency_key": dedupe_key})
            continue
        seen.add(dedupe_key)
        accepted.append(normalized)

    latencies = [_latency_ms(event) for event in accepted]
    violations = [
        {
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "latency_ms": _latency_ms(event),
        }
        for event in accepted
        if _latency_ms(event) > latency_slo_ms
    ]
    counts: dict[str, int] = {}
    latest: dict[str, datetime] = {}
    for event in accepted:
        event_type = str(event["event_type"])
        counts[event_type] = counts.get(event_type, 0) + 1
        occurred = _parse_time(event["occurred_at"], "occurred_at")
        if event_type not in latest or occurred > latest[event_type]:
            latest[event_type] = occurred

    stale_items = _stale_assessment(latest, now=observed_at, stale_after_minutes=stale_after_minutes)
    stale_count = sum(1 for item in stale_items if item["status"] == "stale")
    return {
        "schema_version": CONTINUOUS_MONITORING_REPLAY_SCHEMA,
        "product": "CAVRA",
        "generated_at": observed_at.isoformat(),
        "input_event_count": len(events),
        "accepted_event_count": len(accepted),
        "duplicate_event_count": len(duplicates),
        "invalid_event_count": len(invalid),
        "required_event_types_present": REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES <= set(counts),
        "event_type_counts": {event_type: counts.get(event_type, 0) for event_type in sorted(REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES)},
        "accepted_events": accepted,
        "duplicate_events": duplicates,
        "invalid_events": invalid,
        "latency_summary": {
            "slo_ms": latency_slo_ms,
            "max_latency_ms": max(latencies, default=0),
            "p95_latency_ms": _percentile(latencies, 95),
            "violation_count": len(violations),
            "violations": violations,
        },
        "stale_assessment": {
            "stale_after_minutes": stale_after_minutes,
            "stale_count": stale_count,
            "monitored_event_types": sorted(REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES),
            "items": stale_items,
        },
    }


def build_continuous_monitoring_readiness_packet(
    replay_report: dict[str, Any],
    *,
    evidence_mode: str = "sample",
    event_bus_ref: str = "sample://event-bus/cavra-continuous-monitoring",
    ci_run_ref: str = "sample://github-actions/continuous-monitoring",
    monitor_dashboard_ref: str = "sample://dashboard/continuous-monitoring",
) -> dict[str, Any]:
    return {
        "schema_version": CONTINUOUS_MONITORING_READINESS_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "event_bus": {
            "event_bus_ref": event_bus_ref,
            "capabilities": sorted(REQUIRED_EVENT_BUS_CAPABILITIES),
            "durable": True,
            "dead_letter_queue": True,
            "replay_supported": True,
            "idempotency_supported": True,
            "consumer_lag_metrics": True,
            "latency_slo_ms": replay_report.get("latency_summary", {}).get("slo_ms", DEFAULT_LATENCY_SLO_MS),
        },
        "event_triggers": {
            "agent_actions": AGENT_ACTION_EVENT,
            "model_registration": MODEL_REGISTRATION_EVENT,
            "drift": DRIFT_EVENT,
            "production_promotions": PRODUCTION_PROMOTION_EVENT,
        },
        "replay_report": replay_report,
        "operating_evidence": {
            "ci_run_ref": ci_run_ref,
            "event_bus_ref": event_bus_ref,
            "replay_report_ref": "artifact://continuous-monitoring/replay-report.json",
            "monitor_dashboard_ref": monitor_dashboard_ref,
        },
    }


def validate_continuous_monitoring_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_event_bus(packet.get("event_bus", {}), checks)
    _check_triggers(packet.get("event_triggers", {}), checks)
    _check_replay_report(packet.get("replay_report", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CONTINUOUS_MONITORING_READINESS_RESULT_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_continuous_monitoring_contract": contract_ready,
        "ready_for_live_continuous_monitoring": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_continuous_monitoring_artifacts(
    *,
    events: list[dict[str, Any]],
    replay_report: dict[str, Any],
    readiness_packet: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "events": output_dir / "continuous-monitoring-events.json",
        "replay_report": output_dir / "continuous-monitoring-replay-report.json",
        "readiness_packet": output_dir / "continuous-monitoring-readiness-packet.json",
    }
    artifacts["events"].write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
    artifacts["replay_report"].write_text(json.dumps(replay_report, indent=2) + "\n", encoding="utf-8")
    artifacts["readiness_packet"].write_text(json.dumps(readiness_packet, indent=2) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.continuous-monitoring.export.v1",
        "output_dir": str(output_dir),
        "artifacts": {name: str(path) for name, path in artifacts.items()},
    }


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CONTINUOUS_MONITORING_READINESS_SCHEMA else "blocker",
        "Continuous monitoring packet schema is valid."
        if packet.get("schema_version") == CONTINUOUS_MONITORING_READINESS_SCHEMA
        else f"Packet must use {CONTINUOUS_MONITORING_READINESS_SCHEMA}.",
    )


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    if mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live continuous monitoring evidence packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample continuous monitoring packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live continuous monitoring validation requires evidence_mode=live.")


def _check_event_bus(event_bus: dict[str, Any], checks: list[dict[str, str]]) -> None:
    capabilities = set(event_bus.get("capabilities", []))
    flags = {
        "durable": event_bus.get("durable") is True,
        "dead_letter_queue": event_bus.get("dead_letter_queue") is True,
        "replay_supported": event_bus.get("replay_supported") is True,
        "idempotency_supported": event_bus.get("idempotency_supported") is True,
        "consumer_lag_metrics": event_bus.get("consumer_lag_metrics") is True,
    }
    missing = sorted(REQUIRED_EVENT_BUS_CAPABILITIES - capabilities)
    if not missing and all(flags.values()) and event_bus.get("event_bus_ref"):
        _add_check(checks, "event_bus", "pass", "Event bus is durable, replayable, idempotent, and observable.")
        return
    problems = [name for name, ok in flags.items() if not ok]
    if missing:
        problems.append(f"capabilities: {', '.join(missing)}")
    if not event_bus.get("event_bus_ref"):
        problems.append("event_bus_ref")
    _add_check(checks, "event_bus", "blocker", f"Event bus evidence is incomplete: {', '.join(problems)}.")


def _check_triggers(triggers: dict[str, Any], checks: list[dict[str, str]]) -> None:
    observed = {str(value) for value in triggers.values()}
    missing = sorted(REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES - observed)
    _add_check(
        checks,
        "event_triggers",
        "pass" if not missing else "blocker",
        "Required event triggers are registered."
        if not missing
        else f"Missing event triggers: {', '.join(missing)}.",
    )


def _check_replay_report(report: dict[str, Any], checks: list[dict[str, str]]) -> None:
    latency = report.get("latency_summary", {}) if isinstance(report.get("latency_summary"), dict) else {}
    stale = report.get("stale_assessment", {}) if isinstance(report.get("stale_assessment"), dict) else {}
    required_counts = report.get("required_event_types_present") is True
    clean_replay = int(report.get("invalid_event_count", 1)) == 0
    has_accepted = int(report.get("accepted_event_count", 0)) >= len(REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES)
    latency_ok = int(latency.get("violation_count", 1)) == 0
    stale_ok = int(stale.get("stale_count", 1)) == 0
    _add_check(
        checks,
        "event_replay",
        "pass" if required_counts and clean_replay and has_accepted else "blocker",
        "Replay covers required events with no invalid inputs."
        if required_counts and clean_replay and has_accepted
        else "Replay must cover all required events with no invalid inputs.",
    )
    _add_check(
        checks,
        "latency_slo",
        "pass" if latency_ok else "blocker",
        "Event processing latency is within SLO." if latency_ok else "Event processing latency has SLO violations.",
    )
    _add_check(
        checks,
        "stale_assessment",
        "pass" if stale_ok else "blocker",
        "Continuous assessments are fresh." if stale_ok else "One or more continuous assessments are stale or missing.",
    )


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = ["ci_run_ref", "event_bus_ref", "replay_report_ref", "monitor_dashboard_ref"]
    missing = [field for field in required if not evidence.get(field)]
    _add_check(
        checks,
        "operating_evidence",
        "pass" if not missing else "blocker",
        "Continuous monitoring operating evidence references are present."
        if not missing
        else f"Operating evidence is missing: {', '.join(missing)}.",
    )


def _stale_assessment(latest: dict[str, datetime], *, now: datetime, stale_after_minutes: int) -> list[dict[str, Any]]:
    items = []
    for event_type in sorted(REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES):
        timestamp = latest.get(event_type)
        if timestamp is None:
            items.append({"event_type": event_type, "status": "stale", "age_minutes": None, "reason": "missing"})
            continue
        age_minutes = max(0, int((now - timestamp).total_seconds() // 60))
        status = "fresh" if age_minutes <= stale_after_minutes else "stale"
        items.append(
            {
                "event_type": event_type,
                "status": status,
                "age_minutes": age_minutes,
                "latest_event_at": timestamp.isoformat(),
                "reason": "within_threshold" if status == "fresh" else "older_than_threshold",
            }
        )
    return items


def _latency_ms(event: dict[str, Any]) -> int:
    occurred = _parse_time(event["occurred_at"], "occurred_at")
    received = _parse_time(event["received_at"], "received_at")
    return int((received - occurred).total_seconds() * 1000)


def _percentile(values: list[int], percentile: int) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, ceil((percentile / 100) * len(ordered)) - 1))
    return ordered[index]


def _parse_time(value: str | datetime | None, field: str) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if value is None:
        raise ValueError(f"{field} is required")
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO-8601") from exc
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _event_id(event_type: str, source: str, source_ref: str, occurred_at: str) -> str:
    digest = hashlib.sha256(f"{event_type}|{source}|{source_ref}|{occurred_at}".encode("utf-8")).hexdigest()[:16]
    return f"evt_{digest}"


def _risk_to_severity(risk_tier: str) -> str:
    return {"critical": "critical", "high": "high", "medium": "medium", "low": "low"}.get(risk_tier.lower(), "medium")


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item not in {None, ""}]


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
