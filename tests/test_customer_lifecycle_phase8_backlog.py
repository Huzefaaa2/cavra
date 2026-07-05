from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_backlog import (
    build_customer_lifecycle_phase8_backlog_packet,
    validate_customer_lifecycle_phase8_backlog_packet,
)
from cavra.customer_lifecycle_retrospective import build_customer_lifecycle_retrospective_packet


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_backlog_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_backlog_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_backlog_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_backlog() -> None:
    packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is False
    assert result["blocker_count"] >= 1


def test_unready_retrospective_blocks_phase8_backlog() -> None:
    retrospective = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="live")
    retrospective["retrospective_controls"]["phase8_inputs_triaged"] = False
    packet = build_customer_lifecycle_phase8_backlog_packet(retrospective, repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is False
    assert result["blocker_count"] == 2


def test_missing_backlog_owner_blocks_phase8_backlog() -> None:
    packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["backlog_owner_refs"]["product_owner_ref"]

    result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is False
    assert result["blocker_count"] == 1


def test_bad_priority_blocks_phase8_backlog() -> None:
    packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["backlog_items"][0]["priority"] = "P9"

    result = validate_customer_lifecycle_phase8_backlog_packet(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is False
    assert result["blocker_count"] == 1


def test_missing_acceptance_gate_blocks_phase8_backlog() -> None:
    packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["backlog_items"][0]["acceptance_gates"] = ["too short"]

    result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is False
    assert result["blocker_count"] == 1


def test_false_backlog_control_blocks_phase8_backlog() -> None:
    packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["backlog_controls"]["dependencies_mapped"] = False

    result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_backlog() -> None:
    packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["raw_contract"] = "private"

    result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT / "examples/customer-lifecycle-phase8-backlog/customer-lifecycle-phase8-backlog.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_backlog_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_backlog"] is True
