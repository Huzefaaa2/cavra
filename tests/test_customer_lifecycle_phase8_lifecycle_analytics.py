from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_lifecycle_analytics import (
    build_customer_lifecycle_phase8_lifecycle_analytics_packet,
    validate_customer_lifecycle_phase8_lifecycle_analytics_packet,
)
from cavra.customer_lifecycle_phase8_sprint1_checkpoint import (
    build_customer_lifecycle_phase8_sprint1_checkpoint_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_lifecycle_analytics_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_lifecycle_analytics_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_lifecycle_analytics() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] >= 1


def test_unready_sprint1_checkpoint_blocks_phase8_lifecycle_analytics() -> None:
    sprint1 = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(repo_root=REPO_ROOT, evidence_mode="live")
    sprint1["checkpoint_controls"]["blockers_triaged"] = False
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(sprint1, repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_lifecycle_analytics() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["analytics_owner_refs"]["product_owner_ref"]

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 1


def test_missing_analytics_input_field_blocks_phase8_lifecycle_analytics() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["analytics_input_contract"]["schema_fields"].remove("cadence_signal")

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_dashboard_output_blocks_phase8_lifecycle_analytics() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["dashboard_safe_outputs"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 1


def test_unsafe_summary_ref_blocks_phase8_lifecycle_analytics() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["lifecycle_summary_refs"]["adoption_summary_ref"] = "https://example.com/raw"

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_lifecycle_analytics() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["summary_validation"]

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_lifecycle_analytics() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["analytics_controls"]["dashboard_outputs_defined"] = False

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_lifecycle_analytics() -> None:
    packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["token"] = "private"

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-lifecycle-analytics/customer-lifecycle-phase8-lifecycle-analytics.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_lifecycle_analytics_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"] is True
