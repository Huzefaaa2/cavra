from __future__ import annotations

import json
from pathlib import Path

from cavra.zero_trust_reference_deployments import (
    build_reference_deployment_catalog,
    build_reference_deployment_readiness_packet,
    validate_reference_deployment_catalog,
    validate_reference_deployment_files,
    validate_reference_deployment_readiness_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_reference_deployment_catalog_lists_required_artifacts_and_controls() -> None:
    catalog = build_reference_deployment_catalog()

    result = validate_reference_deployment_catalog(catalog, repo_root=REPO_ROOT)

    assert result["valid"] is True
    assert result["blocker_count"] == 0


def test_reference_deployment_files_have_zero_trust_markers() -> None:
    result = validate_reference_deployment_files(REPO_ROOT)

    assert result["valid"] is True
    assert result["blocker_count"] == 0


def test_sample_readiness_packet_warns_but_does_not_block_contract() -> None:
    packet = build_reference_deployment_readiness_packet(evidence_mode="sample")

    result = validate_reference_deployment_readiness_packet(packet, repo_root=REPO_ROOT)

    assert result["ready_for_zero_trust_reference_deployment_contract"] is True
    assert result["ready_for_live_zero_trust_reference_deployments"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1


def test_live_readiness_packet_passes_live_gate() -> None:
    packet = json.loads(
        (REPO_ROOT / "examples/reference-deployments/zero-trust-reference-deployments.live.sanitized.example.json").read_text(
            encoding="utf-8"
        )
    )

    result = validate_reference_deployment_readiness_packet(packet, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_live_zero_trust_reference_deployments"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_missing_required_control_blocks_readiness() -> None:
    packet = build_reference_deployment_readiness_packet(evidence_mode="live")
    packet["security_controls"] = [control for control in packet["security_controls"] if control != "no_raw_model_egress"]

    result = validate_reference_deployment_readiness_packet(packet, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_live_zero_trust_reference_deployments"] is False
    assert result["blocker_count"] == 1


def test_require_live_rejects_sample_packet() -> None:
    packet = build_reference_deployment_readiness_packet(evidence_mode="sample")

    result = validate_reference_deployment_readiness_packet(packet, repo_root=REPO_ROOT, require_live=True)

    assert result["ready_for_live_zero_trust_reference_deployments"] is False
    assert result["blocker_count"] == 1
