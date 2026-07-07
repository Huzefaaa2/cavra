from __future__ import annotations

import json
from pathlib import Path

from cavra.certified_connectors import (
    PRIORITY_CONNECTOR_SPECS,
    REQUIRED_PRIORITY_CONNECTORS,
    build_priority_connector_manifest,
    build_priority_connector_registry,
    validate_certified_connectors_packet,
    validate_priority_connector_registry,
)
from cavra.connector_sdk import validate_connector_manifest
from cavra.integrations import build_connector_request_specs


MANIFEST_DIR = Path("examples/connectors/priority-certified")
SAMPLE_PACKET = Path("examples/connectors/enterprise-priority-connectors.sample.json")
LIVE_SANITIZED_PACKET = Path("examples/connectors/enterprise-priority-connectors.live.sanitized.example.json")


def _event() -> dict[str, object]:
    return {
        "event_type": "cavra.runtime.decision",
        "product": "CAVRA",
        "session_id": "session-42",
        "decision_count": 4,
        "blocked_count": 1,
        "approval_required_count": 1,
        "max_severity": "high",
    }


def test_priority_connector_registry_covers_required_providers() -> None:
    registry = build_priority_connector_registry()

    assert set(registry["providers"]) == REQUIRED_PRIORITY_CONNECTORS
    assert registry["connector_count"] == 11
    assert registry["compatibility_matrix"]["valid_connector_count"] == 11
    assert all(packet["certified"] for packet in registry["certification_packets"])


def test_checked_in_priority_manifests_match_registry() -> None:
    for provider in PRIORITY_CONNECTOR_SPECS:
        checked_in = json.loads((MANIFEST_DIR / f"{provider}.json").read_text(encoding="utf-8"))
        generated = build_priority_connector_manifest(provider)

        assert checked_in == generated
        assert validate_connector_manifest(checked_in)["valid"] is True


def test_manifest_directory_validates_as_complete_registry() -> None:
    manifests = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(MANIFEST_DIR.glob("*.json"))]

    result = validate_priority_connector_registry(manifests)

    assert result["valid"] is True
    assert result["blocker_count"] == 0
    assert result["provider_count"] == 11


def test_priority_connector_registry_blocks_missing_provider() -> None:
    manifests = [
        build_priority_connector_manifest(provider)
        for provider in PRIORITY_CONNECTOR_SPECS
        if provider != "jenkins"
    ]

    result = validate_priority_connector_registry(manifests)

    assert result["valid"] is False
    assert any(check["name"] == "priority_providers" and "jenkins" in check["message"] for check in result["checks"])


def test_priority_connector_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_certified_connectors_packet(packet)

    assert result["ready_for_priority_connector_contract"] is True
    assert result["ready_for_live_priority_connectors"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1


def test_priority_connector_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_certified_connectors_packet(packet, require_live=True)

    assert result["ready_for_priority_connector_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_priority_connector_live_sanitized_packet_passes_live_gate() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))

    result = validate_certified_connectors_packet(packet, require_live=True)

    assert result["ready_for_live_priority_connectors"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0


def test_scm_and_ci_cd_connector_request_specs(monkeypatch) -> None:
    monkeypatch.setenv("CONNECTOR_TOKEN", "connector-secret")
    config = {
        "connectors": {
            "github": {"url": "https://api.github.com/repos/acme/app/dispatches", "token_env": "CONNECTOR_TOKEN"},
            "gitlab": {"url": "https://gitlab.example/api/v4/projects/1/trigger/pipeline", "token_env": "CONNECTOR_TOKEN"},
            "azure_repos": {"url": "https://dev.azure.com/acme/_apis/hooks", "token_env": "CONNECTOR_TOKEN"},
            "github_actions": {"url": "https://api.github.com/repos/acme/app/actions/workflows/cavra.yml/dispatches", "token_env": "CONNECTOR_TOKEN"},
            "jenkins": {"url": "https://jenkins.example/job/cavra/buildWithParameters", "api_key_env": "CONNECTOR_TOKEN"},
        }
    }

    specs = build_connector_request_specs(_event(), config)

    assert specs["github"]["body"]["client_payload"]["event_id"] == "session-42"
    assert specs["gitlab"]["body"]["variables"]["CAVRA_EVENT_ID"] == "session-42"
    assert specs["azure_repos"]["body"]["publisherId"] == "cavra"
    assert specs["github_actions"]["body"]["inputs"]["cavra_EVENT_ID"] == "session-42"
    assert specs["jenkins"]["body"]["parameters"][0]["name"] == "CAVRA_EVENT_TYPE"
    assert specs["jenkins"]["headers"]["x-api-key"] == "connector-secret"


def test_priority_connector_request_specs_require_auth() -> None:
    try:
        build_connector_request_specs(
            _event(),
            {"connectors": {"github": {"url": "https://api.github.com/repos/acme/app/dispatches"}}},
        )
    except ValueError as exc:
        assert "connector github must configure" in str(exc)
    else:
        raise AssertionError("expected missing GitHub connector credentials to fail")


def test_priority_connector_workflow_runs_require_live_gate() -> None:
    workflow = Path(".github/workflows/priority-connectors.yml").read_text(encoding="utf-8")

    assert "Validate sanitized live packet" in workflow
    assert "--require-live" in workflow
    assert "examples/connectors/enterprise-priority-connectors.live.sanitized.example.json" in workflow


def test_priority_connector_closeout_docs_reference_sanitized_live_packet() -> None:
    closeout = Path("docs/priority-connectors-r4-closeout.md").read_text(encoding="utf-8")

    assert "examples/connectors/enterprise-priority-connectors.live.sanitized.example.json" in closeout
    assert "ready_for_live_priority_connectors" in closeout
    assert "R4.3 Handoff" in closeout
