from __future__ import annotations

import json
from pathlib import Path

from cavra.opa_rego_policy import (
    REQUIRED_PARITY_CASES,
    build_default_rego_parity_fixtures,
    build_rego_policy_bundle,
    evaluate_rego_compatible_policy,
    load_policy_for_rego,
    run_rego_parity_report,
    validate_opa_rego_policy_packet,
    write_rego_bundle,
)

SAMPLE_PACKET = Path("examples/opa-rego/enterprise-opa-rego-policy.sample.json")
LIVE_PACKET = Path("examples/opa-rego/enterprise-opa-rego-policy.live.sanitized.example.json")


def test_rego_bundle_contains_module_data_and_required_fixtures() -> None:
    bundle = build_rego_policy_bundle("cavra-ai-agent-baseline")

    assert bundle["schema_version"] == "cavra.opa-rego-policy.bundle.v1"
    assert "package cavra.policy" in bundle["rego_module"]
    assert "default decision" in bundle["rego_module"]
    assert "glob.match" in bundle["rego_module"]
    assert bundle["rego_data"]["cavra"]["policy"]["metadata"]["id"] == "cavra-ai-agent-baseline"
    assert REQUIRED_PARITY_CASES <= {item["case_id"] for item in bundle["opa_input_fixtures"]}
    assert bundle["parity_report"]["passed"] is True


def test_rego_compatible_evaluator_matches_core_decisions() -> None:
    policy = load_policy_for_rego("cavra-ai-agent-baseline")

    for fixture in build_default_rego_parity_fixtures():
        decision = evaluate_rego_compatible_policy(policy, fixture["input"])
        assert decision["decision"] == fixture["expected_decision"]


def test_rego_parity_report_passes_required_cases() -> None:
    report = run_rego_parity_report("cavra-ai-agent-baseline")

    assert report["passed"] is True
    assert report["failed_count"] == 0
    assert report["required_cases_present"] is True
    assert report["case_count"] >= len(REQUIRED_PARITY_CASES)


def test_rego_bundle_export_writes_expected_artifacts(tmp_path: Path) -> None:
    bundle = build_rego_policy_bundle("cavra-ai-agent-baseline")
    result = write_rego_bundle(bundle, tmp_path)

    assert Path(result["artifacts"]["rego_module"]).exists()
    assert Path(result["artifacts"]["rego_data"]).exists()
    assert Path(result["artifacts"]["opa_input_fixtures"]).exists()
    assert Path(result["artifacts"]["parity_report"]).exists()
    assert Path(result["artifacts"]["policy_version_manifest"]).exists()


def test_sample_opa_rego_packet_validates_with_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_opa_rego_policy_packet(packet)

    assert result["ready_for_opa_rego_policy_contract"] is True
    assert result["ready_for_live_opa_rego_policy_path"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1


def test_live_opa_rego_packet_passes_live_gate() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))

    result = validate_opa_rego_policy_packet(packet, require_live=True)

    assert result["ready_for_live_opa_rego_policy_path"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0


def test_opa_rego_packet_blocks_missing_parity_and_lifecycle() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))
    packet["parity_tests"]["failed_count"] = 1
    packet["policy_lifecycle"]["rollback_ref"] = ""
    packet["operating_evidence"]["ci_run_ref"] = ""

    result = validate_opa_rego_policy_packet(packet, require_live=True)
    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}

    assert {"parity_tests", "policy_lifecycle", "operating_evidence"} <= blocker_names
    assert result["ready_for_live_opa_rego_policy_path"] is False
