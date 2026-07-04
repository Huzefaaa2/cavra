from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from cavra.continuous_monitoring import (
    AGENT_ACTION_EVENT,
    REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES,
    build_agent_action_monitoring_event,
    build_continuous_monitoring_readiness_packet,
    build_sample_monitoring_events,
    normalize_monitoring_event,
    replay_monitoring_events,
    validate_continuous_monitoring_packet,
    write_continuous_monitoring_artifacts,
)

SAMPLE_PACKET = Path("examples/continuous-monitoring/enterprise-continuous-monitoring.sample.json")
LIVE_PACKET = Path("examples/continuous-monitoring/enterprise-continuous-monitoring.live.sanitized.example.json")


def test_sample_monitoring_events_cover_required_event_types() -> None:
    events = build_sample_monitoring_events()

    assert REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES <= {event["event_type"] for event in events}
    assert all(event["schema_version"] == "cavra.continuous-monitoring.event.v1" for event in events)
    assert all(event["idempotency_key"] for event in events)


def test_agent_action_event_normalizes_decision_payload() -> None:
    event = build_agent_action_monitoring_event(
        {
            "decision_id": "dec_test",
            "session_id": "session_test",
            "decision": "block",
            "action_type": "execute_command",
            "target": "terraform apply",
            "timestamp": "2026-07-04T10:00:00+00:00",
            "received_at": "2026-07-04T10:00:01+00:00",
        }
    )

    assert event["event_type"] == AGENT_ACTION_EVENT
    assert event["payload"]["decision"] == "block"
    assert event["payload"]["decision_id"] == "dec_test"


def test_monitoring_replay_reports_dedupe_latency_and_freshness() -> None:
    report = replay_monitoring_events(build_sample_monitoring_events(), now="2026-07-04T10:15:00+00:00")

    assert report["accepted_event_count"] == 4
    assert report["duplicate_event_count"] == 0
    assert report["invalid_event_count"] == 0
    assert report["required_event_types_present"] is True
    assert report["latency_summary"]["violation_count"] == 0
    assert report["stale_assessment"]["stale_count"] == 0


def test_monitoring_replay_suppresses_duplicate_idempotency_keys() -> None:
    events = build_sample_monitoring_events()
    events.append(deepcopy(events[0]))

    report = replay_monitoring_events(events, now="2026-07-04T10:15:00+00:00")

    assert report["input_event_count"] == 5
    assert report["accepted_event_count"] == 4
    assert report["duplicate_event_count"] == 1
    assert report["duplicate_events"][0]["event_id"] == events[0]["event_id"]


def test_monitoring_replay_detects_latency_violations() -> None:
    events = build_sample_monitoring_events()
    events[0]["received_at"] = "2026-07-04T10:00:10+00:00"

    report = replay_monitoring_events(events, now="2026-07-04T10:15:00+00:00", latency_slo_ms=5000)

    assert report["latency_summary"]["violation_count"] == 1
    assert report["latency_summary"]["violations"][0]["event_type"] == AGENT_ACTION_EVENT


def test_monitoring_replay_detects_stale_and_missing_assessments() -> None:
    events = build_sample_monitoring_events()[:2]

    report = replay_monitoring_events(events, now="2026-07-04T12:00:00+00:00", stale_after_minutes=60)

    assert report["required_event_types_present"] is False
    assert report["stale_assessment"]["stale_count"] >= 2
    stale_types = {item["event_type"] for item in report["stale_assessment"]["items"] if item["status"] == "stale"}
    assert REQUIRED_CONTINUOUS_MONITORING_EVENT_TYPES - {event["event_type"] for event in events} <= stale_types


def test_monitoring_normalization_blocks_unsupported_event_type() -> None:
    try:
        normalize_monitoring_event(
            {
                "event_type": "cavra.unknown.event",
                "source": "test",
                "source_ref": "test",
                "occurred_at": "2026-07-04T10:00:00+00:00",
            }
        )
    except ValueError as exc:
        assert "unsupported monitoring event_type" in str(exc)
    else:
        raise AssertionError("unsupported event type should be rejected")


def test_continuous_monitoring_export_writes_artifacts(tmp_path: Path) -> None:
    events = build_sample_monitoring_events()
    replay = replay_monitoring_events(events, now="2026-07-04T10:15:00+00:00")
    packet = build_continuous_monitoring_readiness_packet(replay)

    result = write_continuous_monitoring_artifacts(
        events=events,
        replay_report=replay,
        readiness_packet=packet,
        output_dir=tmp_path,
    )

    assert Path(result["artifacts"]["events"]).exists()
    assert Path(result["artifacts"]["replay_report"]).exists()
    assert Path(result["artifacts"]["readiness_packet"]).exists()


def test_sample_continuous_monitoring_packet_validates_with_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_continuous_monitoring_packet(packet)

    assert result["ready_for_continuous_monitoring_contract"] is True
    assert result["ready_for_live_continuous_monitoring"] is False
    assert result["status"] == "ready_with_warnings"


def test_live_continuous_monitoring_packet_passes_live_gate() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))

    result = validate_continuous_monitoring_packet(packet, require_live=True)

    assert result["ready_for_live_continuous_monitoring"] is True
    assert result["blocker_count"] == 0
    assert result["status"] == "ready"


def test_continuous_monitoring_packet_blocks_missing_controls() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))
    packet["event_bus"]["replay_supported"] = False
    packet["event_triggers"].pop("drift")
    packet["replay_report"]["latency_summary"]["violation_count"] = 1
    packet["operating_evidence"]["ci_run_ref"] = ""

    result = validate_continuous_monitoring_packet(packet, require_live=True)
    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}

    assert {"event_bus", "event_triggers", "latency_slo", "operating_evidence"} <= blocker_names
    assert result["ready_for_live_continuous_monitoring"] is False
