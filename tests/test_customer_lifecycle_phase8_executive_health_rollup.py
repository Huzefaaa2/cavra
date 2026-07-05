from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_customer_health_review import (
    build_customer_lifecycle_phase8_customer_health_review_packet,
)
from cavra.customer_lifecycle_phase8_executive_health_rollup import (
    build_customer_lifecycle_phase8_executive_health_rollup_packet,
    validate_customer_lifecycle_phase8_executive_health_rollup_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_executive_health_rollup_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_executive_health_rollup_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_executive_health_rollup() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] >= 1


def test_unready_health_review_blocks_phase8_executive_health_rollup() -> None:
    health = build_customer_lifecycle_phase8_customer_health_review_packet(repo_root=REPO_ROOT, evidence_mode="live")
    health["health_controls"]["dashboard_refs_defined"] = False
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(
        health,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_executive_health_rollup() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["executive_owner_refs"]["executive_owner_ref"]

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 1


def test_missing_rollup_contract_ref_blocks_phase8_executive_health_rollup() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["executive_rollup_contract"]["risk_posture_ref"]

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_rollup_contract_blocks_phase8_executive_health_rollup() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["executive_rollup_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 1


def test_unsafe_brief_ref_blocks_phase8_executive_health_rollup() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["executive_brief_refs"].append("https://example.com/raw")

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_executive_health_rollup() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["executive_brief_validation"]

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_executive_health_rollup() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["rollup_controls"]["next_action_readiness_defined"] = False

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_executive_health_rollup() -> None:
    packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["pricing"] = "private"

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-executive-health-rollup/customer-lifecycle-phase8-executive-health-rollup.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_executive_health_rollup_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_executive_health_rollup"] is True
