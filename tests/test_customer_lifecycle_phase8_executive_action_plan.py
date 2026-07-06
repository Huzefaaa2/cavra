from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_executive_action_plan import (
    build_customer_lifecycle_phase8_executive_action_plan_packet,
    validate_customer_lifecycle_phase8_executive_action_plan_packet,
)
from cavra.customer_lifecycle_phase8_executive_health_rollup import (
    build_customer_lifecycle_phase8_executive_health_rollup_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_executive_action_plan_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_executive_action_plan_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_executive_action_plan() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] >= 1


def test_unready_executive_health_rollup_blocks_phase8_executive_action_plan() -> None:
    rollup = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")
    rollup["rollup_controls"]["next_action_readiness_defined"] = False
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(
        rollup,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_executive_action_plan() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["action_owner_refs"]["product_owner_ref"]

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 1


def test_missing_action_contract_ref_blocks_phase8_executive_action_plan() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["executive_action_plan_contract"]["due_window_ref"]

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_action_contract_blocks_phase8_executive_action_plan() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["executive_action_plan_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 1


def test_unsafe_commitment_ref_blocks_phase8_executive_action_plan() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["action_commitment_refs"]["support_action_ref"] = "https://example.com/raw-support-action"

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_executive_action_plan() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["commitment_ref_validation"]

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_executive_action_plan() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["action_plan_controls"]["due_windows_defined"] = False

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_executive_action_plan() -> None:
    packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["pricing"] = "private"

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-executive-action-plan/customer-lifecycle-phase8-executive-action-plan.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_executive_action_plan_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_executive_action_plan_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_action_plan"] is True
