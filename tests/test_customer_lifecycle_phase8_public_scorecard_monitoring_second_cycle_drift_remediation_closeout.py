from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] >= 1


def test_unready_second_cycle_first_review_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    second_cycle_first_review = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    second_cycle_first_review["second_cycle_first_review_controls"]["public_status_refreshed"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        second_cycle_first_review,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["drift_remediation_owner_refs"]["operations_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_contract_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["drift_remediation_contract"]["public_status_update_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_contract_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["drift_remediation_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_drift_register_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["drift_register_refs"]["broken_link_drift_ref"] = "https://example.com/raw-drift"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_remediation_disposition_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["remediation_disposition_refs"]["remediated_item_register_ref"] = "https://example.com/raw-remediation"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_archive_ref_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["remediation_archive_refs"]["immutable_remediation_archive_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["next_cycle_blocker_clearance_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["drift_remediation_controls"]["next_cycle_blockers_cleared"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["raw_drift"] = "private"
    packet["remediation_detail"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"] is True
