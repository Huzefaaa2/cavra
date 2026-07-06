from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_distribution_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_distribution_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_distribution_closeout_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_distribution_closeout_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] >= 1


def test_unready_distribution_readiness_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    distribution_readiness = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    distribution_readiness["distribution_controls"]["notification_refs_defined"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        distribution_readiness,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["closeout_owner_refs"]["release_manager_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_closeout_contract_ref_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["closeout_contract"]["link_check_closeout_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_closeout_contract_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["closeout_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_published_channel_ref_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["published_channel_refs"]["product_website_published_ref"] = "https://example.com/raw-publication"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_link_check_ref_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["link_check_refs"]["product_website_link_check_ref"] = "https://example.com/raw-link-check"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["link_check_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["closeout_controls"]["notifications_delivered"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_distribution_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["recipient_email"] = "security@example.com"
    packet["raw_delivery"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-distribution-closeout/customer-lifecycle-phase8-public-scorecard-distribution-closeout.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"] is True
