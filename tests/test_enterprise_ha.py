from __future__ import annotations

import json
from pathlib import Path

from cavra.enterprise_ha import (
    build_enterprise_ha_contract,
    build_enterprise_ha_readiness,
    validate_enterprise_ha_evidence_packet,
)


SAMPLE_PACKET = Path("examples/operations/enterprise-ha-readiness.sample.json")


def test_enterprise_ha_contract_defines_required_topology() -> None:
    contract = build_enterprise_ha_contract()

    assert contract["schema_version"] == "cavra.enterprise_ha.contract.v1"
    assert contract["targets"]["rto_minutes"] == 60
    assert contract["targets"]["rpo_minutes"] == 15
    assert "/health" in contract["required_health_endpoints"]
    assert "queue_depth" in contract["required_monitor_alerts"]
    assert {component["name"] for component in contract["topology_components"]} >= {
        "api_control_plane",
        "worker_pool",
        "event_bus",
        "database",
        "evidence_store",
        "data_residency",
    }


def test_enterprise_ha_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_ha_evidence_packet(packet)

    assert result["ready_for_enterprise_ha_contract"] is True
    assert result["ready_for_enterprise_live_ha"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1
    assert result["blocker_count"] == 0


def test_enterprise_ha_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_ha_evidence_packet(packet, require_live=True)

    assert result["ready_for_enterprise_ha_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_enterprise_ha_packet_blocks_weak_topology_and_residency() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))
    packet["evidence_mode"] = "live"
    packet["deployment"]["api_replicas"] = 1
    packet["event_bus"]["dead_letter_queue"] = False
    packet["backup_restore"]["restore_duration_minutes"] = 90
    packet["data_residency"]["observed_regions"] = ["eastus", "westus"]

    result = validate_enterprise_ha_evidence_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"replica_floor", "event_bus", "backup_restore", "data_residency"} <= blocker_names
    assert result["ready_for_enterprise_live_ha"] is False


def test_enterprise_ha_readiness_without_packet_is_contract_ready_with_warning() -> None:
    result = build_enterprise_ha_readiness()

    assert result["schema_version"] == "cavra.enterprise_ha.readiness.v1"
    assert result["ready_for_enterprise_ha_contract"] is True
    assert result["ready_for_enterprise_live_ha"] is False
    assert result["status"] == "ready_with_warnings"
