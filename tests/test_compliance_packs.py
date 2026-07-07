from __future__ import annotations

import json
from pathlib import Path

from cavra.compliance_packs import (
    REQUIRED_FRAMEWORKS,
    build_compliance_mapping_report,
    build_compliance_pack_registry,
    build_enterprise_compliance_pack_readiness,
    map_finding_to_clauses,
    validate_compliance_pack,
    validate_enterprise_compliance_pack_packet,
)


SAMPLE_PACKET = Path("examples/compliance/enterprise-compliance-packs.sample.json")
LIVE_SANITIZED_PACKET = Path("examples/compliance/enterprise-compliance-packs.live.sanitized.example.json")
SAMPLE_FINDINGS = Path("examples/compliance/sample-findings.json")


def test_built_in_registry_contains_required_frameworks_and_valid_packs() -> None:
    registry = build_compliance_pack_registry()

    assert set(registry["required_frameworks"]) == REQUIRED_FRAMEWORKS
    assert {pack["framework_id"] for pack in registry["packs"]} == REQUIRED_FRAMEWORKS
    assert registry["clause_count"] >= 25
    for pack in registry["packs"]:
        assert validate_compliance_pack(pack)["valid"] is True


def test_pack_validation_rejects_missing_clause_metadata() -> None:
    registry = build_compliance_pack_registry()
    pack = dict(registry["packs"][0])
    pack["clauses"] = [{"id": "broken"}]

    result = validate_compliance_pack(pack)

    assert result["valid"] is False
    assert any(check["name"] == "clauses" and check["status"] == "blocker" for check in result["checks"])


def test_finding_maps_to_clause_level_controls() -> None:
    finding = {
        "id": "finding-runtime-approval",
        "title": "High-risk command required human approval",
        "severity": "high",
        "finding_type": "approval",
        "surface": "runtime",
        "tags": ["approval", "human_oversight", "runtime"],
    }

    mapping = map_finding_to_clauses(finding)

    frameworks = {clause["framework_id"] for clause in mapping["matched_clauses"]}
    assert mapping["matched_clause_count"] >= 4
    assert {"nist_ai_rmf", "iso_iec_42001", "nist_ssdf", "eu_ai_act"} <= frameworks


def test_sample_findings_build_complete_compliance_mapping_report() -> None:
    findings = json.loads(SAMPLE_FINDINGS.read_text(encoding="utf-8"))

    report = build_compliance_mapping_report(findings)

    assert report["schema_version"] == "cavra.compliance.mapping-report.v1"
    assert report["finding_count"] == 5
    assert report["unmapped_finding_count"] == 0
    assert all(count > 0 for count in report["framework_match_counts"].values())


def test_enterprise_compliance_pack_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_compliance_pack_packet(packet)

    assert result["ready_for_enterprise_compliance_pack_contract"] is True
    assert result["ready_for_enterprise_live_compliance_mapping"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1
    assert result["blocker_count"] == 0


def test_enterprise_compliance_pack_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_compliance_pack_packet(packet, require_live=True)

    assert result["ready_for_enterprise_compliance_pack_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_enterprise_compliance_pack_live_sanitized_example_passes_require_live() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_compliance_pack_packet(packet, require_live=True)

    assert result["ready_for_enterprise_live_compliance_mapping"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_enterprise_compliance_pack_blocks_missing_frameworks_and_reporting() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))
    packet["pack_registry"]["frameworks"] = ["nist_ai_rmf"]
    packet["mapping_engine"]["deterministic_mapping_tested"] = False
    packet["coverage"]["coverage_percent"] = 50
    packet["reporting"]["formats"] = ["json"]
    packet["operating_evidence"]["auditor_handoff_ref"] = ""

    result = validate_enterprise_compliance_pack_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"pack_registry", "mapping_engine", "coverage", "reporting", "operating_evidence"} <= blocker_names
    assert result["ready_for_enterprise_live_compliance_mapping"] is False


def test_enterprise_compliance_pack_readiness_without_packet_is_contract_ready_with_warning() -> None:
    result = build_enterprise_compliance_pack_readiness()

    assert result["schema_version"] == "cavra.compliance.mapping-packs.readiness.v1"
    assert result["ready_for_enterprise_compliance_pack_contract"] is True
    assert result["ready_for_enterprise_live_compliance_mapping"] is False
    assert result["status"] == "ready_with_warnings"


def test_enterprise_compliance_pack_workflow_runs_require_live_gate() -> None:
    workflow = Path(".github/workflows/enterprise-compliance-packs.yml").read_text(encoding="utf-8")

    assert "Validate live compliance mapping-pack packet" in workflow
    assert "--require-live" in workflow
    assert "examples/compliance/enterprise-compliance-packs.live.sanitized.example.json" in workflow


def test_enterprise_compliance_pack_closeout_docs_reference_sanitized_live_packet() -> None:
    closeout = Path("docs/compliance-packs-r3-closeout.md").read_text(encoding="utf-8")

    assert "examples/compliance/enterprise-compliance-packs.live.sanitized.example.json" in closeout
    assert "ready_for_enterprise_live_compliance_mapping" in closeout
    assert "R3.4 Handoff" in closeout
