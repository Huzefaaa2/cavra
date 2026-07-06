from __future__ import annotations

import json
from pathlib import Path

from cavra.customer_lifecycle_phase8_public_scorecard_distribution_audit_index import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet,
)
from cavra.customer_lifecycle_phase8_public_scorecard_distribution_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_warns_but_does_not_block_shape() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(packet)

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_is_ready() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="sample",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] >= 1


def test_unready_distribution_closeout_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    distribution_closeout = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    distribution_closeout["closeout_controls"]["notifications_delivered"] = False
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        distribution_closeout,
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 2


def test_missing_owner_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["audit_index_owner_refs"]["audit_owner_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 1


def test_missing_audit_index_contract_ref_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["audit_index_contract"]["delivery_proof_index_ref"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 1


def test_unsanitized_audit_index_contract_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["audit_index_contract"]["redaction_status"] = "raw"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 1


def test_unsafe_publication_snapshot_ref_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["publication_snapshot_refs"]["product_website_snapshot_ref"] = "https://example.com/raw-snapshot"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 1


def test_unsafe_delivery_proof_ref_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["delivery_proof_refs"]["release_notification_proof_ref"] = "https://example.com/raw-proof"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 1


def test_missing_ci_gate_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    del packet["ci_gate_coverage"]["delivery_proof_index_validation"]

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 1


def test_false_control_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["audit_index_controls"]["delivery_proofs_indexed"] = False

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_phase8_public_scorecard_distribution_audit_index() -> None:
    packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        repo_root=REPO_ROOT,
        evidence_mode="live",
    )
    packet["recipient_email"] = "security@example.com"
    packet["raw_proof"] = "private"

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-phase8-public-scorecard-distribution-audit-index/customer-lifecycle-phase8-public-scorecard-distribution-audit-index.live.sanitized.example.json"
    )
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
            repo_root=REPO_ROOT,
            evidence_mode="live",
        )

    result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
        packet,
        require_live=True,
    )

    assert result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"] is True
