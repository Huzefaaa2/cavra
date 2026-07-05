from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_announcement import (
    build_customer_lifecycle_announcement_packet,
    validate_customer_lifecycle_announcement_packet,
)
from cavra.customer_lifecycle_verification_index import build_customer_lifecycle_verification_index


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_announcement_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_announcement_packet(packet)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_announcement_is_ready() -> None:
    packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_announcement_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_announcement() -> None:
    packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_announcement_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is False
    assert result["blocker_count"] >= 1


def test_unready_verification_index_blocks_announcement() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="live")
    index["gates"][0]["ready"] = False
    packet = build_customer_lifecycle_announcement_packet(index, repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_announcement_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is False
    assert result["blocker_count"] == 2


def test_missing_announcement_owner_blocks_announcement() -> None:
    packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["announcement_owner_refs"]["communications_owner_ref"]

    result = validate_customer_lifecycle_announcement_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is False
    assert result["blocker_count"] == 1


def test_short_announcement_copy_blocks_announcement() -> None:
    packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["announcement_sections"][0]["copy"] = "Done"

    result = validate_customer_lifecycle_announcement_packet(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is False
    assert result["blocker_count"] == 1


def test_unsafe_operator_handoff_ref_blocks_announcement() -> None:
    packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["operator_handoff_refs"][0] = "private handoff notes"

    result = validate_customer_lifecycle_announcement_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is False
    assert result["blocker_count"] == 1


def test_false_announcement_control_blocks_announcement() -> None:
    packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["announcement_controls"]["release_notes_approved"] = False

    result = validate_customer_lifecycle_announcement_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_announcement() -> None:
    packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["pricing"] = "private"

    result = validate_customer_lifecycle_announcement_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-lifecycle-announcement/customer-lifecycle-announcement.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_announcement_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_announcement_packet"] is True
