from __future__ import annotations

import json
from pathlib import Path

from cavra.connector_sdk import (
    REQUIRED_TEST_SUITES,
    build_connector_certification_packet,
    build_connector_compatibility_matrix,
    build_enterprise_connector_sdk_readiness,
    build_reference_webhook_manifest,
    validate_connector_manifest,
    validate_enterprise_connector_sdk_packet,
)


MANIFEST = Path("examples/connectors/webhook-certified/connector-manifest.json")
SAMPLE_PACKET = Path("examples/connectors/enterprise-connector-sdk.sample.json")
LIVE_SANITIZED_PACKET = Path("examples/connectors/enterprise-connector-sdk.live.sanitized.example.json")


def test_reference_webhook_manifest_matches_checked_in_manifest() -> None:
    generated = build_reference_webhook_manifest()
    checked_in = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert generated["schema_version"] == checked_in["schema_version"]
    assert generated["connector_id"] == checked_in["connector_id"]
    assert generated["tests"]["suites"] == checked_in["tests"]["suites"]


def test_connector_manifest_validates() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    result = validate_connector_manifest(manifest)

    assert result["valid"] is True
    assert result["blocker_count"] == 0


def test_connector_manifest_rejects_missing_required_test_suite() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["tests"]["suites"] = ["unit"]

    result = validate_connector_manifest(manifest)

    assert result["valid"] is False
    assert any(check["name"] == "tests" and "auth" in check["message"] for check in result["checks"])


def test_connector_certification_packet_certifies_reference_manifest() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    packet = build_connector_certification_packet(manifest)

    assert packet["schema_version"] == "cavra.connector.sdk.certification.v1"
    assert packet["certified"] is True
    assert set(packet["probe_results"].values()) == {"pass"}


def test_connector_compatibility_matrix_marks_valid_connectors() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    matrix = build_connector_compatibility_matrix([manifest])

    assert matrix["connector_count"] == 1
    assert matrix["valid_connector_count"] == 1
    assert matrix["rows"][0]["connector_id"] == "cavra-reference-webhook"


def test_enterprise_connector_sdk_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_connector_sdk_packet(packet)

    assert result["ready_for_enterprise_connector_sdk_contract"] is True
    assert result["ready_for_enterprise_live_connector_certification"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1
    assert result["blocker_count"] == 0


def test_enterprise_connector_sdk_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_connector_sdk_packet(packet, require_live=True)

    assert result["ready_for_enterprise_connector_sdk_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_enterprise_connector_sdk_live_sanitized_example_passes_require_live() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_connector_sdk_packet(packet, require_live=True)

    assert result["ready_for_enterprise_live_connector_certification"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_enterprise_connector_sdk_blocks_missing_artifacts_and_program() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))
    packet["sdk_artifacts"]["artifact_ids"] = ["sdk_manifest_schema"]
    packet["certification_program"]["required_test_suites"] = ["unit"]
    packet["reference_connector"]["secret_redaction_tested"] = False
    packet["compatibility"]["api_contract_validated"] = False
    packet["operating_evidence"]["partner_onboarding_ref"] = ""

    result = validate_enterprise_connector_sdk_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"sdk_artifacts", "certification_program", "reference_connector", "compatibility", "operating_evidence"} <= blocker_names
    assert result["ready_for_enterprise_live_connector_certification"] is False


def test_enterprise_connector_sdk_readiness_without_packet_is_contract_ready_with_warning() -> None:
    result = build_enterprise_connector_sdk_readiness()

    assert result["schema_version"] == "cavra.connector.sdk.readiness.v1"
    assert result["ready_for_enterprise_connector_sdk_contract"] is True
    assert result["ready_for_enterprise_live_connector_certification"] is False
    assert result["status"] == "ready_with_warnings"


def test_connector_sdk_workflow_runs_require_live_gate() -> None:
    workflow = Path(".github/workflows/connector-sdk.yml").read_text(encoding="utf-8")

    assert "Validate live connector SDK packet" in workflow
    assert "--require-live" in workflow
    assert "examples/connectors/enterprise-connector-sdk.live.sanitized.example.json" in workflow
    assert all(suite in workflow for suite in REQUIRED_TEST_SUITES)
