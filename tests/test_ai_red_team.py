from __future__ import annotations

import json
from pathlib import Path

from cavra.ai_red_team import (
    REQUIRED_GUARDRAIL_TESTS,
    build_ai_red_team_readiness_packet,
    build_guardrail_test_suite,
    find_forbidden_ai_fields,
    run_guardrail_test_suite,
    run_malicious_model_checks,
    validate_ai_red_team_readiness_packet,
    validate_ai_supply_chain_metadata,
    write_ai_red_team_artifacts,
)


SUITE = Path("examples/ai-red-team/guardrail-test-suite.sample.json")
ARTIFACT = Path("examples/ai-red-team/ai-artifact-metadata.sample.json")
INVALID_ARTIFACT = Path("examples/ai-red-team/ai-artifact-metadata.invalid.json")
SAMPLE_PACKET = Path("examples/ai-red-team/enterprise-ai-red-team.sample.json")
LIVE_PACKET = Path("examples/ai-red-team/enterprise-ai-red-team.live.sanitized.example.json")


def test_guardrail_test_suite_contains_required_tests() -> None:
    suite = build_guardrail_test_suite()

    assert suite["schema_version"] == "cavra.ai-red-team.test-suite.v1"
    assert REQUIRED_GUARDRAIL_TESTS <= {test["test_id"] for test in suite["tests"]}


def test_guardrail_test_suite_run_passes() -> None:
    suite = json.loads(SUITE.read_text(encoding="utf-8"))

    result = run_guardrail_test_suite(suite)

    assert result["passed"] is True
    assert result["passed_count"] == len(suite["tests"])
    assert result["missing_required_tests"] == []


def test_guardrail_suite_blocks_missing_required_test() -> None:
    suite = build_guardrail_test_suite()
    suite["tests"] = suite["tests"][:1]

    result = run_guardrail_test_suite(suite)

    assert result["passed"] is False
    assert "secret_exfiltration_request" in result["missing_required_tests"]


def test_supply_chain_metadata_validates_reference_artifact() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    result = validate_ai_supply_chain_metadata(artifact)

    assert result["valid"] is True
    assert result["blocker_count"] == 0


def test_supply_chain_metadata_blocks_raw_and_unsafe_artifact() -> None:
    artifact = json.loads(INVALID_ARTIFACT.read_text(encoding="utf-8"))

    result = validate_ai_supply_chain_metadata(artifact)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"serialization_safety", "dependency_allowlist", "no_raw_model_egress"} <= blocker_names
    assert "raw_prompt" in find_forbidden_ai_fields(artifact)


def test_malicious_model_checks_pass_reference_artifact() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    result = run_malicious_model_checks(artifact)

    assert result["passed"] is True
    assert result["blocker_count"] == 0


def test_malicious_model_checks_block_invalid_artifact() -> None:
    artifact = json.loads(INVALID_ARTIFACT.read_text(encoding="utf-8"))

    result = run_malicious_model_checks(artifact)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"unsafe_serialization", "remote_code_execution", "hidden_prompt_payload", "dependency_confusion"} <= blocker_names
    assert result["passed"] is False


def test_sample_ai_red_team_packet_validates_with_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_ai_red_team_readiness_packet(packet)

    assert result["ready_for_ai_red_team_contract"] is True
    assert result["ready_for_live_ai_red_team_gate"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1


def test_live_ai_red_team_packet_passes_require_live() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))

    result = validate_ai_red_team_readiness_packet(packet, require_live=True)

    assert result["ready_for_ai_red_team_contract"] is True
    assert result["ready_for_live_ai_red_team_gate"] is True
    assert result["blocker_count"] == 0


def test_ai_red_team_packet_blocks_failed_scan_and_missing_evidence() -> None:
    suite = build_guardrail_test_suite()
    run_report = run_guardrail_test_suite(suite)
    invalid_artifact = json.loads(INVALID_ARTIFACT.read_text(encoding="utf-8"))
    scan = validate_ai_supply_chain_metadata(invalid_artifact)
    malicious = run_malicious_model_checks(invalid_artifact)
    packet = build_ai_red_team_readiness_packet(suite, run_report, scan, malicious, evidence_mode="live")
    packet["operating_evidence"]["ci_run_ref"] = ""

    result = validate_ai_red_team_readiness_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"supply_chain_scan", "malicious_model_checks", "operating_evidence"} <= blocker_names
    assert result["ready_for_live_ai_red_team_gate"] is False


def test_write_ai_red_team_artifacts(tmp_path: Path) -> None:
    export = write_ai_red_team_artifacts(tmp_path)

    for path in export["artifacts"].values():
        assert Path(path).exists()
