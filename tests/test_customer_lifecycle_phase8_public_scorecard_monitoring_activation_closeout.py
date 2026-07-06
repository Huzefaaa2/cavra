from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] >= 1


def test_unready_continuous_monitoring_readiness_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    readiness = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    readiness["monitoring_controls"]["link_health_monitors_defined"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        readiness,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["activation_owner_refs"]["operations_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_contract_ref_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["activation_contract"]["first_monitor_snapshot_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_contract_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["activation_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_activated_monitor_ref_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["activated_monitor_refs"]["link_health_monitor_active_ref"] = "https://example.com/raw-monitor"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_alert_route_ref_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["alert_route_refs"]["operations_alert_route_active_ref"] = "https://example.com/raw-route"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_first_snapshot_ref_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["first_snapshot_refs"]["immutable_snapshot_archive_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["snapshot_archive_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["activation_controls"]["first_monitor_snapshot_archived"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_monitoring_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["raw_snapshot"] = "private"
    packet["alert_payload"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout/customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"] is True
