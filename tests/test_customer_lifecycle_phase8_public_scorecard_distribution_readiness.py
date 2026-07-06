from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_distribution_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_executive_summary_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_distribution_readiness_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_distribution_readiness_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] >= 1


def test_unready_executive_summary_closeout_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    executive_summary_closeout = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    executive_summary_closeout["executive_summary_controls"]["publication_refs_defined"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        executive_summary_closeout,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["distribution_owner_refs"]["web_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 1


def test_missing_distribution_contract_ref_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["distribution_contract"]["website_linkage_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_distribution_contract_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["distribution_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsafe_channel_ref_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["channel_refs"]["website_channel_ref"] = "https://example.com/raw-channel"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 1


def test_unsafe_linkage_ref_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["linkage_refs"]["product_website_link_ref"] = "https://example.com/raw-linkage"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["linkage_ref_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["distribution_controls"]["notification_refs_defined"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_distribution_readiness() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["customer_name"] = "Example Corp"
    packet["raw_distribution"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-distribution-readiness/customer-lifecycle-phase8-public-scorecard-distribution-readiness.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"] is True
