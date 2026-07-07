from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] >= 1


def test_unready_second_cycle_readiness_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    readiness = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    readiness["second_cycle_readiness_controls"]["public_surfaces_current"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        readiness,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["second_cycle_activation_owner_refs"]["operations_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_contract_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["second_cycle_activation_contract"]["initial_signal_capture_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_contract_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["second_cycle_activation_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_cycle_start_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["cycle_start_refs"]["second_cycle_start_decision_ref"] = "https://example.com/raw-activation"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_initial_signal_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["initial_signal_refs"]["scorecard_health_signal_ref"] = "https://example.com/raw-signal"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_monitor_run_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["monitor_run_refs"]["redaction_monitor_run_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_alert_route_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["alert_route_check_refs"]["no_dead_route_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["public_safe_activation_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["second_cycle_activation_controls"]["monitors_ran"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_monitoring_second_cycle_activation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["raw_signal"] = "private"
    packet["raw_on_call"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"] is True
