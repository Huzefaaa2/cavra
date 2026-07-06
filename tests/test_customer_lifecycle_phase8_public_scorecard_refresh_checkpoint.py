from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_publication_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_refresh_checkpoint import (
    build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet,
    validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] >= 1


def test_unready_publication_closeout_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    publication_closeout = build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    publication_closeout["publication_closeout_controls"]["hold_rollback_refs_defined"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
        publication_closeout,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["refresh_owner_refs"]["communications_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_missing_index_contract_ref_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["refresh_checkpoint_contract"]["staleness_detection_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_index_contract_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["refresh_checkpoint_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_unsafe_readiness_ref_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["refresh_cadence_refs"]["next_refresh_ref"] = "https://example.com/raw-next-refresh"

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_unsafe_decision_gate_ref_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["stale_scorecard_refs"]["stale_public_notice_ref"] = "https://example.com/raw-stale-notice"

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["staleness_ref_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["refresh_checkpoint_controls"]["staleness_detection_defined"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_refresh_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["raw_score"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-refresh-checkpoint/customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"] is True
