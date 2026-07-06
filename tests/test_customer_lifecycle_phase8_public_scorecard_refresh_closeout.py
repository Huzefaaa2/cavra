from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_refresh_checkpoint import (
    build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_refresh_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_refresh_closeout_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_refresh_closeout_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] >= 1


def test_unready_refresh_checkpoint_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    refresh_checkpoint = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    refresh_checkpoint["refresh_checkpoint_controls"]["staleness_detection_defined"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
        refresh_checkpoint,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["refresh_closeout_owner_refs"]["communications_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_refresh_closeout_contract_ref_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["refresh_closeout_contract"]["stale_resolution_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_refresh_closeout_contract_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["refresh_closeout_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_updated_scorecard_ref_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["updated_scorecard_publication_refs"]["scorecard_delta_ref"] = "https://example.com/raw-delta"

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_stale_resolution_ref_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["stale_resolution_refs"]["public_notice_resolution_ref"] = "https://example.com/raw-resolution"

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["stale_resolution_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["refresh_closeout_controls"]["stale_resolution_refs_defined"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_refresh_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["raw_score"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-refresh-closeout/customer-lifecycle-phase8-public-scorecard-refresh-closeout.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"] is True
