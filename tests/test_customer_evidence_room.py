from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_evidence_room import (
    build_customer_evidence_room_index,
    validate_customer_evidence_room_index,
)
from cavra.customer_live_evidence import build_customer_live_evidence_template


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_evidence_room_warns_but_does_not_block_shape() -> None:
    index = build_customer_evidence_room_index(evidence_mode="sample")

    result = validate_customer_evidence_room_index(index)

    assert result["ready_for_customer_evidence_room_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_sanitized_customer_evidence_room_is_ready() -> None:
    index = build_customer_evidence_room_index(evidence_mode="live")

    result = validate_customer_evidence_room_index(index, require_live=True)

    assert result["ready_for_customer_evidence_room_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_index() -> None:
    index = build_customer_evidence_room_index(evidence_mode="sample")

    result = validate_customer_evidence_room_index(index, require_live=True)

    assert result["ready_for_customer_evidence_room_closeout"] is False
    assert result["blocker_count"] >= 1


def test_missing_required_section_blocks_closeout() -> None:
    index = build_customer_evidence_room_index(evidence_mode="live")
    index["sections"] = [
        section for section in index["sections"] if section["section_id"] != "phase6_ecosystem"
    ]

    result = validate_customer_evidence_room_index(index, require_live=True)

    assert result["ready_for_customer_evidence_room_closeout"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_closeout() -> None:
    index = build_customer_evidence_room_index(evidence_mode="live")
    index["tenant_name"] = "real tenant"
    index["smtp_password"] = "do-not-store"

    result = validate_customer_evidence_room_index(index, require_live=True)

    assert result["ready_for_customer_evidence_room_closeout"] is False
    assert result["blocker_count"] == 1


def test_unsafe_plain_reference_blocks_closeout() -> None:
    index = build_customer_evidence_room_index(evidence_mode="live")
    broken = copy.deepcopy(index)
    broken["sections"][0]["evidence_refs"][0] = "private share path"

    result = validate_customer_evidence_room_index(broken, require_live=True)

    assert result["ready_for_customer_evidence_room_closeout"] is False
    assert result["blocker_count"] == 1


def test_unready_source_intake_blocks_closeout() -> None:
    intake = build_customer_live_evidence_template(evidence_mode="live")
    del intake["evidence_sections"]["aispm_production"]["runtime_workflow_ref"]
    index = build_customer_evidence_room_index(intake, evidence_mode="live")

    result = validate_customer_evidence_room_index(index, require_live=True)

    assert result["ready_for_customer_evidence_room_closeout"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    index_path = REPO_ROOT / "examples/customer-evidence-room/customer-evidence-room.live.sanitized.example.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
    else:
        index = build_customer_evidence_room_index(evidence_mode="live")

    result = validate_customer_evidence_room_index(index, require_live=True)

    assert result["ready_for_customer_evidence_room_closeout"] is True
