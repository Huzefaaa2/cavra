from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_action_followup_checkpoint import (
    build_customer_lifecycle_phase8_action_followup_checkpoint_packet,
    validate_customer_lifecycle_phase8_action_followup_checkpoint_packet,
)
from cavra.customer_lifecycle_phase8_executive_action_plan import (
    build_customer_lifecycle_phase8_executive_action_plan_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_action_followup_checkpoint_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_action_followup_checkpoint_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] >= 1


def test_unready_executive_action_plan_blocks_phase8_action_followup_checkpoint() -> None:
    action_plan = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")
    action_plan["action_plan_controls"]["due_windows_defined"] = False
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(
        action_plan,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["followup_owner_refs"]["customer_success_owner_ref"]

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_missing_followup_contract_ref_blocks_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["followup_checkpoint_contract"]["review_cadence_ref"]

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_followup_contract_blocks_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["followup_checkpoint_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_unsafe_status_ref_blocks_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["checkpoint_status_refs"]["support_status_ref"] = "https://example.com/raw-support-status"

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_unsafe_blocker_ref_blocks_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["checkpoint_blocker_refs"]["support_blocker_ref"] = "https://example.com/raw-support-blocker"

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["status_ref_validation"]

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["followup_controls"]["review_cadence_defined"] = False

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_action_followup_checkpoint() -> None:
    packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["raw_status"] = "private"

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-action-followup-checkpoint/customer-lifecycle-phase8-action-followup-checkpoint.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"] is True
