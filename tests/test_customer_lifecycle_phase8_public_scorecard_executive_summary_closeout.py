from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_executive_summary_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_operating_loop_index import (
    build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] >= 1


def test_unready_operating_loop_index_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    operating_loop_index = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    operating_loop_index["operating_loop_controls"]["loop_health_refs_defined"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        operating_loop_index,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["executive_summary_owner_refs"]["legal_review_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_executive_summary_contract_ref_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["executive_summary_contract"]["approval_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_executive_summary_contract_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["executive_summary_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_summary_ref_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["summary_refs"]["decision_summary_ref"] = "https://example.com/raw-summary"

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_publication_ref_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["publication_refs"]["published_summary_ref"] = "https://example.com/raw-publication"

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["approval_ref_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["executive_summary_controls"]["approval_refs_defined"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_executive_summary_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["customer_name"] = "Example Corp"
    packet["raw_summary"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-executive-summary-closeout/customer-lifecycle-phase8-public-scorecard-executive-summary-closeout.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"] is True
