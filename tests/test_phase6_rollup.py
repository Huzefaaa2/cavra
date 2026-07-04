from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.phase6_rollup import build_phase6_rollup_packet, validate_phase6_rollup_packet


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_phase6_rollup_marks_public_contract_release_ready() -> None:
    packet = build_phase6_rollup_packet(REPO_ROOT)

    result = validate_phase6_rollup_packet(packet, repo_root=REPO_ROOT)

    assert result["ready_for_phase6_public_contract_release"] is True
    assert result["ready_for_customer_live_phase6_closeout"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 4


def test_phase6_rollup_requires_all_gates() -> None:
    packet = build_phase6_rollup_packet(REPO_ROOT)
    packet["gates"] = [gate for gate in packet["gates"] if gate["gate_id"] != "R6.4"]

    result = validate_phase6_rollup_packet(packet, repo_root=REPO_ROOT)

    assert result["ready_for_phase6_public_contract_release"] is False
    assert result["blocker_count"] == 1


def test_phase6_rollup_customer_live_closeout_requires_customer_refs() -> None:
    packet = build_phase6_rollup_packet(REPO_ROOT)

    result = validate_phase6_rollup_packet(packet, repo_root=REPO_ROOT, require_customer_live=True)

    assert result["ready_for_customer_live_phase6_closeout"] is False
    assert result["blocker_count"] == 4


def test_phase6_rollup_customer_live_closeout_can_pass_with_refs() -> None:
    packet = build_phase6_rollup_packet(REPO_ROOT)
    for gate in packet["gates"]:
        gate["customer_live_evidence"] = {
            field: f"evidence://customer/{gate['gate_id']}/{field}" for field in gate["customer_live_evidence_required"]
        }

    result = validate_phase6_rollup_packet(packet, repo_root=REPO_ROOT, require_customer_live=True)

    assert result["ready_for_phase6_public_contract_release"] is True
    assert result["ready_for_customer_live_phase6_closeout"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_phase6_rollup_detects_gate_not_ready() -> None:
    packet = build_phase6_rollup_packet(REPO_ROOT)
    broken = copy.deepcopy(packet)
    broken["gates"][0]["public_contract_ready"] = False

    result = validate_phase6_rollup_packet(broken, repo_root=REPO_ROOT)

    assert result["ready_for_phase6_public_contract_release"] is False
    assert result["blocker_count"] == 1


def test_checked_in_phase6_rollup_packet_validates() -> None:
    packet_path = REPO_ROOT / "examples/phase6-rollup/phase6-ecosystem-rollup.json"
    if not packet_path.exists():
        packet = build_phase6_rollup_packet(REPO_ROOT)
    else:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))

    result = validate_phase6_rollup_packet(packet, repo_root=REPO_ROOT)

    assert result["ready_for_phase6_public_contract_release"] is True
    assert result["blocker_count"] == 0
