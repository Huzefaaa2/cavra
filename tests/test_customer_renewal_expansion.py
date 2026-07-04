from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_operating_review import build_customer_operating_review_packet
from cavra.customer_renewal_expansion import (
    build_customer_renewal_expansion_packet,
    validate_customer_renewal_expansion_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_renewal_expansion_warns_but_does_not_block_shape() -> None:
    packet = build_customer_renewal_expansion_packet(evidence_mode="sample")

    result = validate_customer_renewal_expansion_packet(packet)

    assert result["ready_for_customer_renewal_expansion"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_renewal_expansion_is_ready() -> None:
    packet = build_customer_renewal_expansion_packet(evidence_mode="live")

    result = validate_customer_renewal_expansion_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_packet() -> None:
    packet = build_customer_renewal_expansion_packet(evidence_mode="sample")

    result = validate_customer_renewal_expansion_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is False
    assert result["blocker_count"] >= 1


def test_unready_operating_review_blocks_renewal() -> None:
    operating_review = build_customer_operating_review_packet(evidence_mode="live")
    operating_review["review_controls"]["support_sla_healthy"] = False
    packet = build_customer_renewal_expansion_packet(operating_review, evidence_mode="live")

    result = validate_customer_renewal_expansion_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is False
    assert result["blocker_count"] == 2


def test_missing_renewal_owner_blocks_renewal() -> None:
    packet = build_customer_renewal_expansion_packet(evidence_mode="live")
    del packet["renewal_owner_refs"]["commercial_owner_ref"]

    result = validate_customer_renewal_expansion_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is False
    assert result["blocker_count"] == 1


def test_unhealthy_renewal_section_blocks_renewal() -> None:
    packet = build_customer_renewal_expansion_packet(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["renewal_sections"][3]["status"] = "blocked"

    result = validate_customer_renewal_expansion_packet(broken, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is False
    assert result["blocker_count"] == 1


def test_unsafe_expansion_candidate_blocks_renewal() -> None:
    packet = build_customer_renewal_expansion_packet(evidence_mode="live")
    packet["expansion_candidates"][0]["value_ref"] = "private value note"

    result = validate_customer_renewal_expansion_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is False
    assert result["blocker_count"] == 1


def test_false_renewal_control_blocks_renewal() -> None:
    packet = build_customer_renewal_expansion_packet(evidence_mode="live")
    packet["renewal_controls"]["commercial_handoff_ready"] = False

    result = validate_customer_renewal_expansion_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_renewal() -> None:
    packet = build_customer_renewal_expansion_packet(evidence_mode="live")
    packet["customer_email"] = "buyer@example.com"
    packet["api_key"] = "do-not-store"

    result = validate_customer_renewal_expansion_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-renewal-expansion/customer-renewal-expansion.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_renewal_expansion_packet(evidence_mode="live")

    result = validate_customer_renewal_expansion_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_expansion"] is True
