from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_live_evidence import (
    build_customer_live_evidence_template,
    find_forbidden_live_evidence_fields,
    validate_customer_live_evidence_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_live_evidence_warns_but_does_not_block_shape() -> None:
    packet = build_customer_live_evidence_template(evidence_mode="sample")

    result = validate_customer_live_evidence_packet(packet)

    assert result["ready_for_customer_live_evidence_intake"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1


def test_live_sanitized_customer_evidence_is_ready() -> None:
    packet = build_customer_live_evidence_template(evidence_mode="live")

    result = validate_customer_live_evidence_packet(packet, require_live=True)

    assert result["ready_for_customer_live_evidence_intake"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_packet() -> None:
    packet = build_customer_live_evidence_template(evidence_mode="sample")

    result = validate_customer_live_evidence_packet(packet, require_live=True)

    assert result["ready_for_customer_live_evidence_intake"] is False
    assert result["blocker_count"] == 1


def test_missing_evidence_reference_blocks_intake() -> None:
    packet = build_customer_live_evidence_template(evidence_mode="live")
    del packet["evidence_sections"]["phase6_ecosystem"]["benchmark_run_ref"]

    result = validate_customer_live_evidence_packet(packet, require_live=True)

    assert result["ready_for_customer_live_evidence_intake"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_intake() -> None:
    packet = build_customer_live_evidence_template(evidence_mode="live")
    packet["customer_profile"]["tenant_name"] = "real tenant name"
    packet["evidence_sections"]["aispm_production"]["smtp_password"] = "do-not-store"

    result = validate_customer_live_evidence_packet(packet, require_live=True)

    assert result["ready_for_customer_live_evidence_intake"] is False
    assert result["blocker_count"] == 1
    assert "customer_profile.tenant_name" in find_forbidden_live_evidence_fields(packet)


def test_unsafe_plain_reference_blocks_intake() -> None:
    packet = build_customer_live_evidence_template(evidence_mode="live")
    packet["customer_profile"]["customer_ref"] = "Acme Corp"

    result = validate_customer_live_evidence_packet(packet, require_live=True)

    assert result["ready_for_customer_live_evidence_intake"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    packet_path = REPO_ROOT / "examples/customer-live-evidence/customer-live-evidence.live.sanitized.example.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        packet = build_customer_live_evidence_template(evidence_mode="live")

    result = validate_customer_live_evidence_packet(packet, require_live=True)

    assert result["ready_for_customer_live_evidence_intake"] is True


def test_redaction_control_false_blocks_intake() -> None:
    packet = build_customer_live_evidence_template(evidence_mode="live")
    broken = copy.deepcopy(packet)
    broken["redaction_controls"]["contains_no_customer_pii"] = False

    result = validate_customer_live_evidence_packet(broken, require_live=True)

    assert result["ready_for_customer_live_evidence_intake"] is False
    assert result["blocker_count"] == 1
