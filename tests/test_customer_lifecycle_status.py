from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_archive import build_customer_lifecycle_archive_manifest
from cavra.customer_lifecycle_status import (
    build_customer_lifecycle_status_packet,
    validate_customer_lifecycle_status_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_status_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_status_packet(evidence_mode="sample")

    result = validate_customer_lifecycle_status_packet(packet)

    assert result["ready_for_customer_lifecycle_public_status"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_lifecycle_status_is_ready() -> None:
    packet = build_customer_lifecycle_status_packet(evidence_mode="live")

    result = validate_customer_lifecycle_status_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_status() -> None:
    packet = build_customer_lifecycle_status_packet(evidence_mode="sample")

    result = validate_customer_lifecycle_status_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is False
    assert result["blocker_count"] >= 1


def test_unready_archive_blocks_status() -> None:
    archive = build_customer_lifecycle_archive_manifest(evidence_mode="live")
    archive["archive_controls"]["audit_handoff_ready"] = False
    packet = build_customer_lifecycle_status_packet(archive, evidence_mode="live")

    result = validate_customer_lifecycle_status_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is False
    assert result["blocker_count"] == 2


def test_missing_status_owner_blocks_status() -> None:
    packet = build_customer_lifecycle_status_packet(evidence_mode="live")
    del packet["status_owner_refs"]["support_owner_ref"]

    result = validate_customer_lifecycle_status_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is False
    assert result["blocker_count"] == 1


def test_bad_public_status_section_blocks_status() -> None:
    packet = build_customer_lifecycle_status_packet(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["public_status_sections"][0]["summary"] = "short"

    result = validate_customer_lifecycle_status_packet(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is False
    assert result["blocker_count"] == 1


def test_unsafe_support_ref_blocks_status() -> None:
    packet = build_customer_lifecycle_status_packet(evidence_mode="live")
    packet["support_refs"][0] = "private support escalation"

    result = validate_customer_lifecycle_status_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is False
    assert result["blocker_count"] == 1


def test_false_publication_control_blocks_status() -> None:
    packet = build_customer_lifecycle_status_packet(evidence_mode="live")
    packet["publication_controls"]["support_handoff_ready"] = False

    result = validate_customer_lifecycle_status_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_status() -> None:
    packet = build_customer_lifecycle_status_packet(evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["private_note"] = "do not publish"

    result = validate_customer_lifecycle_status_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-lifecycle-status/customer-lifecycle-status.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_status_packet(evidence_mode="live")

    result = validate_customer_lifecycle_status_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_public_status"] is True
