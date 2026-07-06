from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] >= 1


def test_unready_monitoring_activation_closeout_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    activation = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    activation["activation_controls"]["first_monitor_snapshot_archived"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        activation,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["first_cycle_owner_refs"]["operations_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_missing_contract_ref_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["first_cycle_contract"]["public_status_refresh_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_contract_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["first_cycle_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_unsafe_findings_triage_ref_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["findings_triage_refs"]["blocker_triage_ref"] = "https://example.com/raw-triage"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_unsafe_alert_review_ref_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["alert_review_refs"]["security_alert_review_ref"] = "https://example.com/raw-alert"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_missing_snapshot_archive_ref_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["snapshot_archive_refs"]["immutable_cycle_archive_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["public_status_refresh_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["first_cycle_controls"]["public_status_refreshed"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_monitoring_first_cycle_review() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["raw_triage"] = "private"
    packet["alert_payload"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review/customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"] is True
