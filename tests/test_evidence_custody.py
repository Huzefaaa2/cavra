from __future__ import annotations

import json
from pathlib import Path

from cavra.evidence_custody import (
    build_enterprise_evidence_custody_contract,
    build_enterprise_evidence_custody_readiness,
    validate_enterprise_evidence_custody_packet,
)


SAMPLE_PACKET = Path("examples/evidence/enterprise-evidence-custody.sample.json")
LIVE_SANITIZED_PACKET = Path("examples/evidence/enterprise-evidence-custody.live.sanitized.example.json")


def test_enterprise_evidence_custody_contract_defines_required_controls() -> None:
    contract = build_enterprise_evidence_custody_contract()

    assert contract["schema_version"] == "cavra.evidence.custody.contract.v1"
    assert "azure_key_vault" in contract["supported_signing_providers"]
    assert "pkcs11_hsm" in contract["supported_signing_providers"]
    assert "Ed25519" in contract["supported_algorithms"]
    assert contract["default_rotation_cadence_days"] == 90
    assert contract["minimum_rotation_overlap_days"] == 7
    assert "cavra evidence verify" in contract["required_verifier_commands"]


def test_enterprise_evidence_custody_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_evidence_custody_packet(packet)

    assert result["ready_for_enterprise_evidence_custody_contract"] is True
    assert result["ready_for_enterprise_live_evidence_custody"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1
    assert result["blocker_count"] == 0


def test_enterprise_evidence_custody_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_evidence_custody_packet(packet, require_live=True)

    assert result["ready_for_enterprise_evidence_custody_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_enterprise_evidence_custody_live_sanitized_example_passes_require_live() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_evidence_custody_packet(packet, require_live=True)

    assert result["ready_for_enterprise_live_evidence_custody"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_enterprise_evidence_custody_blocks_exportable_key_and_weak_rotation() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))
    packet["signing_provider"]["private_key_exportable"] = True
    packet["rotation"]["cadence_days"] = 180
    packet["trust_roots"]["retired_key_ids"] = []
    packet["independent_verifier"]["sample_bundle_verified"] = False

    result = validate_enterprise_evidence_custody_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"signing_provider", "rotation_policy", "trust_roots", "independent_verifier"} <= blocker_names
    assert result["ready_for_enterprise_live_evidence_custody"] is False


def test_enterprise_evidence_custody_readiness_without_packet_is_contract_ready_with_warning() -> None:
    result = build_enterprise_evidence_custody_readiness()

    assert result["schema_version"] == "cavra.evidence.custody.readiness.v1"
    assert result["ready_for_enterprise_evidence_custody_contract"] is True
    assert result["ready_for_enterprise_live_evidence_custody"] is False
    assert result["status"] == "ready_with_warnings"


def test_enterprise_evidence_custody_workflow_runs_require_live_gate() -> None:
    workflow = Path(".github/workflows/enterprise-evidence-custody.yml").read_text(encoding="utf-8")

    assert "Validate live evidence custody packet" in workflow
    assert "--require-live" in workflow
    assert "examples/evidence/enterprise-evidence-custody.live.sanitized.example.json" in workflow


def test_enterprise_evidence_custody_closeout_docs_reference_sanitized_live_packet() -> None:
    closeout = Path("docs/evidence-custody-r3-closeout.md").read_text(encoding="utf-8")

    assert "examples/evidence/enterprise-evidence-custody.live.sanitized.example.json" in closeout
    assert "ready_for_enterprise_live_evidence_custody" in closeout
    assert "R3.2 Handoff" in closeout
