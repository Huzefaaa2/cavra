from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] >= 1


def test_unready_drift_remediation_closeout_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    drift_closeout = build_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    drift_closeout["drift_remediation_controls"]["next_cycle_blockers_cleared"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        drift_closeout,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["second_cycle_owner_refs"]["operations_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_missing_contract_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["second_cycle_readiness_contract"]["public_surface_currency_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_contract_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["second_cycle_readiness_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsafe_remediated_state_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["remediated_state_refs"]["no_open_critical_drift_ref"] = "https://example.com/raw-drift"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsafe_accepted_risk_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["accepted_risk_boundary_refs"]["accepted_risk_register_ref"] = "https://example.com/raw-risk"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_missing_monitoring_input_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["monitoring_input_refs"]["redaction_posture_input_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["second_cycle_schedule_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["second_cycle_readiness_controls"]["public_surfaces_current"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_monitoring_second_cycle_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["raw_schedule"] = "private"
    packet["accepted_risk_detail"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-readiness/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-readiness.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"] is True
