from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_audit_review_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] >= 1


def test_unready_audit_review_closeout_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    audit_review_closeout = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    audit_review_closeout["audit_review_controls"]["owner_acknowledgements_complete"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        audit_review_closeout,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["monitoring_owner_refs"]["operations_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 1


def test_missing_contract_ref_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["monitoring_contract"]["link_health_monitor_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_contract_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["monitoring_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsafe_scorecard_health_ref_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["scorecard_health_refs"]["public_scorecard_availability_ref"] = "https://example.com/raw-health"

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsafe_alert_routing_ref_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["alert_routing_refs"]["operations_alert_ref"] = "https://example.com/raw-alert"

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["link_health_monitor_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["monitoring_controls"]["link_health_monitors_defined"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_continuous_monitoring_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["raw_monitor"] = "private"
    packet["alert_payload"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness/customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"] is True
