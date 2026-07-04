from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_closeout_handoff import build_customer_closeout_handoff_packet
from cavra.customer_operating_review import (
    build_customer_operating_review_packet,
    validate_customer_operating_review_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_operating_review_warns_but_does_not_block_shape() -> None:
    packet = build_customer_operating_review_packet(evidence_mode="sample")

    result = validate_customer_operating_review_packet(packet)

    assert result["ready_for_customer_operating_review"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_operating_review_is_ready() -> None:
    packet = build_customer_operating_review_packet(evidence_mode="live")

    result = validate_customer_operating_review_packet(packet, require_live=True)

    assert result["ready_for_customer_operating_review"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_packet() -> None:
    packet = build_customer_operating_review_packet(evidence_mode="sample")

    result = validate_customer_operating_review_packet(packet, require_live=True)

    assert result["ready_for_customer_operating_review"] is False
    assert result["blocker_count"] >= 1


def test_unready_closeout_handoff_blocks_review() -> None:
    closeout = build_customer_closeout_handoff_packet(evidence_mode="live")
    closeout["handoff_controls"]["customer_ack_required"] = False
    packet = build_customer_operating_review_packet(closeout, evidence_mode="live")

    result = validate_customer_operating_review_packet(packet, require_live=True)

    assert result["ready_for_customer_operating_review"] is False
    assert result["blocker_count"] == 2


def test_missing_review_owner_blocks_review() -> None:
    packet = build_customer_operating_review_packet(evidence_mode="live")
    del packet["review_owner_refs"]["support_owner_ref"]

    result = validate_customer_operating_review_packet(packet, require_live=True)

    assert result["ready_for_customer_operating_review"] is False
    assert result["blocker_count"] == 1


def test_unhealthy_review_section_blocks_review() -> None:
    packet = build_customer_operating_review_packet(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["review_sections"][3]["status"] = "drift_detected"

    result = validate_customer_operating_review_packet(broken, require_live=True)

    assert result["ready_for_customer_operating_review"] is False
    assert result["blocker_count"] == 1


def test_unsafe_plain_reference_blocks_review() -> None:
    packet = build_customer_operating_review_packet(evidence_mode="live")
    packet["review_sections"][0]["evidence_refs"][0] = "metric dashboard"

    result = validate_customer_operating_review_packet(packet, require_live=True)

    assert result["ready_for_customer_operating_review"] is False
    assert result["blocker_count"] == 1


def test_false_review_control_blocks_review() -> None:
    packet = build_customer_operating_review_packet(evidence_mode="live")
    packet["review_controls"]["support_sla_healthy"] = False

    result = validate_customer_operating_review_packet(packet, require_live=True)

    assert result["ready_for_customer_operating_review"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_review() -> None:
    packet = build_customer_operating_review_packet(evidence_mode="live")
    packet["customer_email"] = "buyer@example.com"
    packet["token"] = "do-not-store"

    result = validate_customer_operating_review_packet(packet, require_live=True)

    assert result["ready_for_customer_operating_review"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-operating-review/customer-operating-review.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_operating_review_packet(evidence_mode="live")

    result = validate_customer_operating_review_packet(packet, require_live=True)

    assert result["ready_for_customer_operating_review"] is True
