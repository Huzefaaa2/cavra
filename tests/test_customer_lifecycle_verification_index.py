from __future__ import annotations

import copy
import json
from pathlib import Path

from cavra.customer_lifecycle_verification_index import (
    build_customer_lifecycle_verification_index,
    validate_customer_lifecycle_verification_index,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_sample_customer_lifecycle_verification_index_warns_but_does_not_block_shape() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_verification_index(index, repo_root=REPO_ROOT)

    assert result["ready_for_customer_lifecycle_verification_index"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] >= 1


def test_live_customer_lifecycle_verification_index_is_ready() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_verification_index(index, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_customer_lifecycle_verification_index"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_require_live_rejects_sample_verification_index() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="sample")

    result = validate_customer_lifecycle_verification_index(index, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_customer_lifecycle_verification_index"] is False
    assert result["blocker_count"] >= 1


def test_missing_gate_blocks_verification_index() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="live")
    index["gates"] = index["gates"][:-1]
    index["gate_count"] = len(index["gates"])

    result = validate_customer_lifecycle_verification_index(index, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_customer_lifecycle_verification_index"] is False
    assert result["blocker_count"] >= 1


def test_not_ready_gate_blocks_verification_index() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="live")
    broken = copy.deepcopy(index)
    broken["gates"][0]["ready"] = False

    result = validate_customer_lifecycle_verification_index(broken, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_customer_lifecycle_verification_index"] is False
    assert result["blocker_count"] == 1


def test_missing_artifact_blocks_verification_index() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="live")
    broken = copy.deepcopy(index)
    broken["gates"][0]["artifact_presence"]["workflow"] = False

    result = validate_customer_lifecycle_verification_index(broken, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_customer_lifecycle_verification_index"] is False
    assert result["blocker_count"] == 1


def test_command_drift_blocks_verification_index() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="live")
    broken = copy.deepcopy(index)
    broken["gates"][0]["validator_command"] = "python3 wrong.py"

    result = validate_customer_lifecycle_verification_index(broken, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_customer_lifecycle_verification_index"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_verification_index() -> None:
    index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="live")
    index["customer_name"] = "Example Corp"
    index["raw_evidence"] = {"private": True}

    result = validate_customer_lifecycle_verification_index(index, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_customer_lifecycle_verification_index"] is False
    assert result["blocker_count"] == 1


def test_checked_in_live_sanitized_example_validates() -> None:
    index_path = (
        REPO_ROOT
        / "examples/customer-lifecycle-verification-index/customer-lifecycle-verification-index.live.sanitized.example.json"
    )
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
    else:
        index = build_customer_lifecycle_verification_index(REPO_ROOT, evidence_mode="live")

    result = validate_customer_lifecycle_verification_index(index, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_customer_lifecycle_verification_index"] is True
