from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_rollup import (
    build_customer_lifecycle_rollup_packet,
    validate_customer_lifecycle_rollup_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_rollup_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_rollup_packet(evidence_mode="sample")

    result = validate_customer_lifecycle_rollup_packet(packet)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_lifecycle_rollup_is_ready() -> None:
    packet = build_customer_lifecycle_rollup_packet(evidence_mode="live")

    result = validate_customer_lifecycle_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_rollup() -> None:
    packet = build_customer_lifecycle_rollup_packet(evidence_mode="sample")

    result = validate_customer_lifecycle_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is False
    assert result["blocker_count"] >= 1


def test_missing_lifecycle_gate_blocks_rollup() -> None:
    packet = build_customer_lifecycle_rollup_packet(evidence_mode="live")
    packet["lifecycle_gates"] = packet["lifecycle_gates"][:-1]

    result = validate_customer_lifecycle_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is False
    assert result["blocker_count"] == 1


def test_unready_lifecycle_gate_blocks_rollup() -> None:
    packet = build_customer_lifecycle_rollup_packet(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["lifecycle_gates"][0]["readiness_result"]["blocker_count"] = 1
    broken["lifecycle_gates"][0]["ready"] = False

    result = validate_customer_lifecycle_rollup_packet(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is False
    assert result["blocker_count"] == 1


def test_unsafe_summary_ref_blocks_rollup() -> None:
    packet = build_customer_lifecycle_rollup_packet(evidence_mode="live")
    packet["executive_summary_sections"][0]["evidence_refs"][0] = "private implementation notes"

    result = validate_customer_lifecycle_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is False
    assert result["blocker_count"] == 1


def test_false_rollup_control_blocks_rollup() -> None:
    packet = build_customer_lifecycle_rollup_packet(evidence_mode="live")
    packet["rollup_controls"]["archive_refs_present"] = False

    result = validate_customer_lifecycle_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_rollup() -> None:
    packet = build_customer_lifecycle_rollup_packet(evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["contract_value"] = "$1"

    result = validate_customer_lifecycle_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-lifecycle-rollup/customer-lifecycle-rollup.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_rollup_packet(evidence_mode="live")

    result = validate_customer_lifecycle_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_executive_rollup"] is True
