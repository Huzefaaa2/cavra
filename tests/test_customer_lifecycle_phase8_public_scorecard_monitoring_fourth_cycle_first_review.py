from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_activation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_activation_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] >= 1


def test_unready_fourth_cycle_activation_closeout_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    activation = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    activation["fourth_cycle_activation_controls"]["monitors_ran"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        activation,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["fourth_cycle_first_review_owner_refs"]["operations_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_missing_contract_ref_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["fourth_cycle_first_review_contract"]["public_status_refresh_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_contract_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["fourth_cycle_first_review_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_unsafe_review_window_ref_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["review_window_refs"]["review_minutes_summary_ref"] = "https://example.com/raw-minutes"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_unsafe_findings_triage_ref_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["findings_triage_refs"]["new_findings_register_ref"] = "https://example.com/raw-finding"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_missing_signal_review_ref_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["signal_review_refs"]["redaction_posture_signal_review_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_missing_public_status_refresh_ref_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["public_status_refresh_refs"]["wiki_status_refresh_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["next_review_schedule_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["fourth_cycle_first_review_controls"]["public_status_refreshed"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_monitoring_fourth_cycle_first_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["raw_minutes"] = "private"
    packet["accepted_finding_detail"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-monitoring-fourth-cycle-first-review/customer-lifecycle-phase8-public-scorecard-monitoring-fourth-cycle-first-review.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_fourth_cycle_first_review"] is True
