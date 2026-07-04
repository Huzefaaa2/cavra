from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_closeout_handoff import (
    build_customer_closeout_handoff_packet,
    validate_customer_closeout_handoff_packet,
)
from cavra.customer_evidence_room import build_customer_evidence_room_index


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_closeout_handoff_warns_but_does_not_block_shape() -> None:
    packet = build_customer_closeout_handoff_packet(evidence_mode="sample")

    result = validate_customer_closeout_handoff_packet(packet)

    assert result["ready_for_customer_closeout_handoff"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_closeout_handoff_is_ready() -> None:
    packet = build_customer_closeout_handoff_packet(evidence_mode="live")

    result = validate_customer_closeout_handoff_packet(packet, require_live=True)

    assert result["ready_for_customer_closeout_handoff"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_packet() -> None:
    packet = build_customer_closeout_handoff_packet(evidence_mode="sample")

    result = validate_customer_closeout_handoff_packet(packet, require_live=True)

    assert result["ready_for_customer_closeout_handoff"] is False
    assert result["blocker_count"] >= 1


def test_unready_evidence_room_blocks_handoff() -> None:
    evidence_room = build_customer_evidence_room_index(evidence_mode="live")
    evidence_room["sections"] = [
        section for section in evidence_room["sections"] if section["section_id"] != "aispm_production"
    ]
    packet = build_customer_closeout_handoff_packet(evidence_room, evidence_mode="live")

    result = validate_customer_closeout_handoff_packet(packet, require_live=True)

    assert result["ready_for_customer_closeout_handoff"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_ref_blocks_handoff() -> None:
    packet = build_customer_closeout_handoff_packet(evidence_mode="live")
    del packet["handoff_owner_refs"]["release_owner_ref"]

    result = validate_customer_closeout_handoff_packet(packet, require_live=True)

    assert result["ready_for_customer_closeout_handoff"] is False
    assert result["blocker_count"] == 1


def test_unsafe_plain_reference_blocks_handoff() -> None:
    packet = build_customer_closeout_handoff_packet(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["communication_refs"]["announcement_ref"] = "customer announcement draft"

    result = validate_customer_closeout_handoff_packet(broken, require_live=True)

    assert result["ready_for_customer_closeout_handoff"] is False
    assert result["blocker_count"] == 1


def test_false_handoff_control_blocks_handoff() -> None:
    packet = build_customer_closeout_handoff_packet(evidence_mode="live")
    packet["handoff_controls"]["customer_ack_required"] = False

    result = validate_customer_closeout_handoff_packet(packet, require_live=True)

    assert result["ready_for_customer_closeout_handoff"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_handoff() -> None:
    packet = build_customer_closeout_handoff_packet(evidence_mode="live")
    packet["customer_email"] = "buyer@example.com"
    packet["api_key"] = "do-not-store"

    result = validate_customer_closeout_handoff_packet(packet, require_live=True)

    assert result["ready_for_customer_closeout_handoff"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_closeout_handoff_packet(evidence_mode="live")

    result = validate_customer_closeout_handoff_packet(packet, require_live=True)

    assert result["ready_for_customer_closeout_handoff"] is True
