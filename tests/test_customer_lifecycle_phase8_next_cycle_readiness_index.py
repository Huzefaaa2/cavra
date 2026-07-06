from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_executive_followup_closeout import (
    build_customer_lifecycle_phase8_executive_followup_closeout_packet,
)
from cavra.customer_lifecycle_phase8_next_cycle_readiness_index import (
    build_customer_lifecycle_phase8_next_cycle_readiness_index_packet,
    validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_next_cycle_readiness_index_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_next_cycle_readiness_index_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] >= 1


def test_unready_executive_followup_closeout_blocks_phase8_next_cycle_readiness_index() -> None:
    closeout = build_customer_lifecycle_phase8_executive_followup_closeout_packet(repo_root=REPO_ROOT, evidence_mode="live")
    closeout["closeout_controls"]["next_cycle_handoff_defined"] = False
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
        closeout,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["next_cycle_owner_refs"]["program_owner_ref"]

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 1


def test_missing_index_contract_ref_blocks_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["next_cycle_readiness_index_contract"]["release_decision_gate_ref"]

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_index_contract_blocks_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["next_cycle_readiness_index_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 1


def test_unsafe_readiness_ref_blocks_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["next_cycle_readiness_refs"]["owner_readiness_ref"] = "https://example.com/raw-owner-readiness"

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 1


def test_unsafe_decision_gate_ref_blocks_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["release_decision_gate_refs"]["risk_acceptance_ref"] = "https://example.com/raw-risk-acceptance"

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")
    del packet["ci_gate_coverage"]["decision_gate_validation"]

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["readiness_controls"]["release_decision_gates_defined"] = False

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_next_cycle_readiness_index() -> None:
    packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(repo_root=REPO_ROOT, evidence_mode="live")
    packet["customer_name"] = "Example Corp"
    packet["raw_score"] = "private"

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-next-cycle-readiness-index/customer-lifecycle-phase8-next-cycle-readiness-index.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(packet, require_live=True)

    assert result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"] is True
