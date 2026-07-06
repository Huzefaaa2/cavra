from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_audit_review_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_distribution_audit_index import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] >= 1


def test_unready_distribution_audit_index_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    distribution_audit_index = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    distribution_audit_index["audit_index_controls"]["delivery_proofs_indexed"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        distribution_audit_index,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["audit_review_owner_refs"]["release_manager_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_contract_ref_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["audit_review_contract"]["remediation_plan_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_contract_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["audit_review_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_owner_ack_ref_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["owner_acknowledgement_refs"]["executive_ack_ref"] = "https://example.com/raw-ack"

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_remediation_ref_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["remediation_refs"]["remediation_plan_ref"] = "https://example.com/raw-remediation"

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["remediation_plan_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["audit_review_controls"]["owner_acknowledgements_complete"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_audit_review_closeout() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["finding_detail"] = "private"
    packet["raw_remediation"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-audit-review-closeout/customer-lifecycle-phase8-public-scorecard-audit-review-closeout.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"] is True
