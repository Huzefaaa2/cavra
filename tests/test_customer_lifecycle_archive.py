from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_archive import (
    build_customer_lifecycle_archive_manifest,
    validate_customer_lifecycle_archive_manifest,
)
from cavra.customer_lifecycle_rollup import build_customer_lifecycle_rollup_packet


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_archive_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_archive_manifest(evidence_mode="sample")

    result = validate_customer_lifecycle_archive_manifest(packet)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_lifecycle_archive_is_ready() -> None:
    packet = build_customer_lifecycle_archive_manifest(evidence_mode="live")

    result = validate_customer_lifecycle_archive_manifest(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_archive() -> None:
    packet = build_customer_lifecycle_archive_manifest(evidence_mode="sample")

    result = validate_customer_lifecycle_archive_manifest(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is False
    assert result["blocker_count"] >= 1


def test_unready_rollup_blocks_archive() -> None:
    rollup = build_customer_lifecycle_rollup_packet(evidence_mode="live")
    rollup["rollup_controls"]["archive_refs_present"] = False
    packet = build_customer_lifecycle_archive_manifest(rollup, evidence_mode="live")

    result = validate_customer_lifecycle_archive_manifest(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is False
    assert result["blocker_count"] == 2


def test_missing_archive_owner_blocks_archive() -> None:
    packet = build_customer_lifecycle_archive_manifest(evidence_mode="live")
    del packet["archive_owner_refs"]["compliance_owner_ref"]

    result = validate_customer_lifecycle_archive_manifest(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is False
    assert result["blocker_count"] == 1


def test_unhealthy_archive_section_blocks_archive() -> None:
    packet = build_customer_lifecycle_archive_manifest(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["archive_sections"][0]["status"] = "missing"

    result = validate_customer_lifecycle_archive_manifest(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is False
    assert result["blocker_count"] == 1


def test_unsafe_retention_ref_blocks_archive() -> None:
    packet = build_customer_lifecycle_archive_manifest(evidence_mode="live")
    packet["retention_controls"]["immutability_policy_ref"] = "private retention note"

    result = validate_customer_lifecycle_archive_manifest(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is False
    assert result["blocker_count"] == 1


def test_false_archive_control_blocks_archive() -> None:
    packet = build_customer_lifecycle_archive_manifest(evidence_mode="live")
    packet["archive_controls"]["audit_handoff_ready"] = False

    result = validate_customer_lifecycle_archive_manifest(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_archive() -> None:
    packet = build_customer_lifecycle_archive_manifest(evidence_mode="live")
    packet["raw_evidence"] = "do not store"
    packet["customer_email"] = "security@example.test"

    result = validate_customer_lifecycle_archive_manifest(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-lifecycle-archive/customer-lifecycle-archive.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_archive_manifest(evidence_mode="live")

    result = validate_customer_lifecycle_archive_manifest(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_archive_manifest"] is True
