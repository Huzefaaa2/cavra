from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_final_seal import (
    build_customer_lifecycle_final_seal_packet,
    validate_customer_lifecycle_final_seal_packet,
)
from cavra.customer_lifecycle_status import build_customer_lifecycle_status_packet


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_final_seal_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_final_seal_packet(evidence_mode="sample")

    result = validate_customer_lifecycle_final_seal_packet(packet)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_lifecycle_final_seal_is_ready() -> None:
    packet = build_customer_lifecycle_final_seal_packet(evidence_mode="live")

    result = validate_customer_lifecycle_final_seal_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_final_seal() -> None:
    packet = build_customer_lifecycle_final_seal_packet(evidence_mode="sample")

    result = validate_customer_lifecycle_final_seal_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is False
    assert result["blocker_count"] >= 1


def test_unready_public_status_blocks_final_seal() -> None:
    status = build_customer_lifecycle_status_packet(evidence_mode="live")
    status["publication_controls"]["support_handoff_ready"] = False
    packet = build_customer_lifecycle_final_seal_packet(status, evidence_mode="live")

    result = validate_customer_lifecycle_final_seal_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is False
    assert result["blocker_count"] == 2


def test_missing_seal_owner_blocks_final_seal() -> None:
    packet = build_customer_lifecycle_final_seal_packet(evidence_mode="live")
    del packet["seal_owner_refs"]["release_owner_ref"]

    result = validate_customer_lifecycle_final_seal_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is False
    assert result["blocker_count"] == 1


def test_unsealed_component_blocks_final_seal() -> None:
    packet = build_customer_lifecycle_final_seal_packet(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["sealed_components"][0]["status"] = "pending"

    result = validate_customer_lifecycle_final_seal_packet(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is False
    assert result["blocker_count"] == 1


def test_missing_release_publication_ref_blocks_final_seal() -> None:
    packet = build_customer_lifecycle_final_seal_packet(evidence_mode="live")
    packet["release_publication_refs"] = []

    result = validate_customer_lifecycle_final_seal_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is False
    assert result["blocker_count"] == 1


def test_false_final_release_control_blocks_final_seal() -> None:
    packet = build_customer_lifecycle_final_seal_packet(evidence_mode="live")
    packet["final_release_controls"]["security_owner_accepted"] = False

    result = validate_customer_lifecycle_final_seal_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_final_seal() -> None:
    packet = build_customer_lifecycle_final_seal_packet(evidence_mode="live")
    packet["customer_email"] = "security@example.invalid"
    packet["commercial_terms"] = "private renewal terms"

    result = validate_customer_lifecycle_final_seal_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-lifecycle-final-seal/customer-lifecycle-final-seal.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_final_seal_packet(evidence_mode="live")

    result = validate_customer_lifecycle_final_seal_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_final_release_seal"] is True
