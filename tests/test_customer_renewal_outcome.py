from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_renewal_expansion import build_customer_renewal_expansion_packet
from cavra.customer_renewal_outcome import (
    build_customer_renewal_outcome_packet,
    validate_customer_renewal_outcome_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_renewal_outcome_warns_but_does_not_block_shape() -> None:
    packet = build_customer_renewal_outcome_packet(evidence_mode="sample")

    result = validate_customer_renewal_outcome_packet(packet)

    assert result["ready_for_customer_renewal_outcome_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_renewal_outcome_is_ready() -> None:
    packet = build_customer_renewal_outcome_packet(evidence_mode="live")

    result = validate_customer_renewal_outcome_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_packet() -> None:
    packet = build_customer_renewal_outcome_packet(evidence_mode="sample")

    result = validate_customer_renewal_outcome_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is False
    assert result["blocker_count"] >= 1


def test_unready_renewal_expansion_blocks_outcome() -> None:
    renewal_expansion = build_customer_renewal_expansion_packet(evidence_mode="live")
    renewal_expansion["renewal_controls"]["commercial_handoff_ready"] = False
    packet = build_customer_renewal_outcome_packet(renewal_expansion, evidence_mode="live")

    result = validate_customer_renewal_outcome_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is False
    assert result["blocker_count"] == 2


def test_missing_outcome_owner_blocks_outcome() -> None:
    packet = build_customer_renewal_outcome_packet(evidence_mode="live")
    del packet["outcome_owner_refs"]["finance_operations_ref"]

    result = validate_customer_renewal_outcome_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is False
    assert result["blocker_count"] == 1


def test_unhealthy_outcome_section_blocks_outcome() -> None:
    packet = build_customer_renewal_outcome_packet(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["outcome_sections"][2]["status"] = "blocked"

    result = validate_customer_renewal_outcome_packet(broken, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_expansion_outcome_blocks_outcome() -> None:
    packet = build_customer_renewal_outcome_packet(evidence_mode="live")
    packet["expansion_outcomes"][0]["decision_ref"] = "private expansion decision"

    result = validate_customer_renewal_outcome_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is False
    assert result["blocker_count"] == 1


def test_false_outcome_control_blocks_outcome() -> None:
    packet = build_customer_renewal_outcome_packet(evidence_mode="live")
    packet["outcome_controls"]["archive_ready"] = False

    result = validate_customer_renewal_outcome_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_outcome() -> None:
    packet = build_customer_renewal_outcome_packet(evidence_mode="live")
    packet["contract_value"] = "$1"
    packet["private_note"] = "do not store"

    result = validate_customer_renewal_outcome_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-renewal-outcome/customer-renewal-outcome.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_renewal_outcome_packet(evidence_mode="live")

    result = validate_customer_renewal_outcome_packet(packet, require_live=True)

    assert result["ready_for_customer_renewal_outcome_closeout"] is True
