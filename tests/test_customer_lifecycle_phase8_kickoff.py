from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_backlog import build_customer_lifecycle_phase8_backlog_packet
from cavra.customer_lifecycle_phase8_kickoff import (
    build_customer_lifecycle_phase8_kickoff_packet,
    validate_customer_lifecycle_phase8_kickoff_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_kickoff_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_kickoff_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_kickoff() -> None:
    packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is False
    assert result["blocker_count"] >= 1


def test_unready_backlog_blocks_phase8_kickoff() -> None:
    backlog = build_customer_lifecycle_phase8_backlog_packet(repo_root=REPO_ROOT, evidence_mode="live")
    backlog["backlog_controls"]["owners_assigned"] = False
    packet = build_customer_lifecycle_phase8_kickoff_packet(backlog, repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is False
    assert result["blocker_count"] == 2


def test_missing_kickoff_owner_blocks_phase8_kickoff() -> None:
    packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["kickoff_owner_refs"]["engineering_owner_ref"]

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is False
    assert result["blocker_count"] == 1


def test_missing_first_sprint_item_blocks_phase8_kickoff() -> None:
    packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["kickoff_sections"]["first_sprint_plan"] = broken["kickoff_sections"]["first_sprint_plan"][:2]

    result = validate_customer_lifecycle_phase8_kickoff_packet(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is False
    assert result["blocker_count"] == 1


def test_short_readiness_gate_blocks_phase8_kickoff() -> None:
    packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["kickoff_sections"]["readiness_gates"] = ["short"]

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is False
    assert result["blocker_count"] == 1


def test_false_kickoff_control_blocks_phase8_kickoff() -> None:
    packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["kickoff_controls"]["first_sprint_defined"] = False

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_kickoff() -> None:
    packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_email"] = "security@example.com"
    packet["pricing"] = "private"

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT / "examples/customer-lifecycle-phase8-kickoff/customer-lifecycle-phase8-kickoff.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_kickoff_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_kickoff_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_kickoff"] is True
