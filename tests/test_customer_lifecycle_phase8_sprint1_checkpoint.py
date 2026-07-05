from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_kickoff import build_customer_lifecycle_phase8_kickoff_packet
from cavra.customer_lifecycle_phase8_sprint1_checkpoint import (
    build_customer_lifecycle_phase8_sprint1_checkpoint_packet,
    validate_customer_lifecycle_phase8_sprint1_checkpoint_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_sprint1_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_sprint1_checkpoint_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_sprint1_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] >= 1


def test_unready_kickoff_blocks_phase8_sprint1_checkpoint() -> None:
    kickoff = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="live")
    kickoff["kickoff_controls"]["first_sprint_defined"] = False
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(kickoff, repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] == 2


def test_missing_checkpoint_owner_blocks_phase8_sprint1_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["checkpoint_owner_refs"]["engineering_owner_ref"]

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_missing_progress_item_blocks_phase8_sprint1_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["checkpoint_sections"]["sprint_progress"] = broken["checkpoint_sections"]["sprint_progress"][:2]

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_open_blocker_blocks_phase8_sprint1_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["checkpoint_sections"]["blocker_review"]["open_blocker_count"] = 1

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_blocked_progress_status_blocks_phase8_sprint1_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["checkpoint_sections"]["sprint_progress"][0]["status"] = "blocked"

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_false_checkpoint_control_blocks_phase8_sprint1_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["checkpoint_controls"]["blockers_triaged"] = False

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_sprint1_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["raw_evidence"] = "private"

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-sprint1-checkpoint/customer-lifecycle-phase8-sprint1-checkpoint.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"] is True
