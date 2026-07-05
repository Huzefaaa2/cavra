from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_announcement import build_customer_lifecycle_announcement_packet
from cavra.customer_lifecycle_retrospective import (
    build_customer_lifecycle_retrospective_packet,
    validate_customer_lifecycle_retrospective_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_retrospective_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_retrospective_packet(packet)

    assert result["ready_for_customer_lifecycle_retrospective"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_retrospective_is_ready() -> None:
    packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_retrospective_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_retrospective() -> None:
    packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_retrospective_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is False
    assert result["blocker_count"] >= 1


def test_unready_announcement_blocks_retrospective() -> None:
    announcement = build_customer_lifecycle_announcement_packet(repo_root=REPO_ROOT, evidence_mode="live")
    announcement["announcement_controls"]["support_path_verified"] = False
    packet = build_customer_lifecycle_retrospective_packet(announcement, repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_retrospective_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is False
    assert result["blocker_count"] == 2


def test_missing_retrospective_owner_blocks_retrospective() -> None:
    packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["retrospective_owner_refs"]["product_owner_ref"]

    result = validate_customer_lifecycle_retrospective_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is False
    assert result["blocker_count"] == 1


def test_short_retrospective_section_blocks_retrospective() -> None:
    packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["retrospective_sections"][0]["summary"] = "too short"

    result = validate_customer_lifecycle_retrospective_packet(broken, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is False
    assert result["blocker_count"] == 1


def test_bad_follow_up_action_blocks_retrospective() -> None:
    packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["follow_up_actions"][0]["owner_ref"] = "private owner"

    result = validate_customer_lifecycle_retrospective_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is False
    assert result["blocker_count"] == 1


def test_false_retrospective_control_blocks_retrospective() -> None:
    packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["retrospective_controls"]["phase8_inputs_triaged"] = False

    result = validate_customer_lifecycle_retrospective_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_retrospective() -> None:
    packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_email"] = "security@example.invalid"
    packet["renewal_amount"] = "private"

    result = validate_customer_lifecycle_retrospective_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-retrospective/customer-lifecycle-retrospective.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_retrospective_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_retrospective_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_retrospective"] is True
