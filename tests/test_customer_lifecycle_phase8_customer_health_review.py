from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_customer_health_review import (
    build_customer_lifecycle_phase8_customer_health_review_packet,
    validate_customer_lifecycle_phase8_customer_health_review_packet,
)
from cavra.customer_lifecycle_phase8_support_automation import (
    build_customer_lifecycle_phase8_support_automation_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_customer_health_review_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_customer_health_review_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_customer_health_review() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] >= 1


def test_unready_support_source_blocks_phase8_customer_health_review() -> None:
    support = build_customer_lifecycle_phase8_support_automation_packet(repo_root=REPO_ROOT, evidence_mode="live")
    support["support_controls"]["automation_trigger_defined"] = False
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(
        support_packet=support,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 2


def test_missing_input_ref_blocks_phase8_customer_health_review() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["phase8_input_refs"]["support_automation_ref"]

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 1


def test_missing_owner_blocks_phase8_customer_health_review() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["health_owner_refs"]["analytics_owner_ref"]

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_review_contract_blocks_phase8_customer_health_review() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["health_review_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 1


def test_unsafe_dashboard_ref_blocks_phase8_customer_health_review() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["health_dashboard_refs"].append("https://example.com/raw")

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_customer_health_review() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["dashboard_validation"]

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_customer_health_review() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["health_controls"]["dashboard_refs_defined"] = False

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_customer_health_review() -> None:
    packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_email"] = "security@example.com"
    packet["raw_evidence"] = "private"

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-customer-health-review/customer-lifecycle-phase8-customer-health-review.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_customer_health_review_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_customer_health_review"] is True
