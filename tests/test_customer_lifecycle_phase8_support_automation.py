from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_sprint1_checkpoint import (
    build_customer_lifecycle_phase8_sprint1_checkpoint_packet,
)
from cavra.customer_lifecycle_phase8_support_automation import (
    build_customer_lifecycle_phase8_support_automation_packet,
    validate_customer_lifecycle_phase8_support_automation_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_support_automation_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_support_automation_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_support_automation() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] >= 1


def test_unready_sprint1_checkpoint_blocks_phase8_support_automation() -> None:
    sprint1 = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    sprint1["checkpoint_controls"]["blockers_triaged"] = False
    packet = build_customer_lifecycle_phase8_support_automation_packet(sprint1, repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_support_automation() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["support_owner_refs"]["customer_success_owner_ref"]

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 1


def test_missing_support_schema_field_blocks_phase8_support_automation() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["support_checkpoint_schema"]["schema_fields"].remove("support_case_ref")

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_trigger_blocks_phase8_support_automation() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["automation_trigger_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 1


def test_unsafe_escalation_ref_blocks_phase8_support_automation() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["escalation_matrix_refs"].append("https://example.com/raw")

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_support_automation() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["trigger_validation"]

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_support_automation() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["support_controls"]["automation_trigger_defined"] = False

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_support_automation() -> None:
    packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["secret"] = "private"

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-support-automation/customer-lifecycle-phase8-support-automation.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_support_automation_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_support_automation"] is True
