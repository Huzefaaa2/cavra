from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_operating_loop_index import (
    build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet,
    validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_refresh_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_operating_loop_index_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_operating_loop_index_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] >= 1


def test_unready_refresh_closeout_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    refresh_closeout = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    refresh_closeout["refresh_closeout_controls"]["stale_resolution_refs_defined"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        refresh_closeout,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["operating_loop_owner_refs"]["communications_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 1


def test_missing_operating_loop_contract_ref_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["operating_loop_contract"]["next_cycle_trigger_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_operating_loop_contract_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["operating_loop_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 1


def test_unsafe_dependency_ref_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["loop_dependency_refs"]["refresh_closeout_ref"] = "https://example.com/raw-dependency"

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 1


def test_unsafe_next_cycle_trigger_ref_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["next_cycle_trigger_refs"]["next_closeout_trigger_ref"] = "https://example.com/raw-trigger"

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["loop_health_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["operating_loop_controls"]["next_cycle_trigger_refs_defined"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_operating_loop_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["customer_name"] = "Example Corp"
    packet["raw_loop"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-operating-loop-index/customer-lifecycle-phase8-public-scorecard-operating-loop-index.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"] is True
