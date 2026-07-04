from __future__ import annotations

import json
from pathlib import Path

from cavra.connector_sdk import validate_connector_manifest
from cavra.model_registry_connectors import (
    MODEL_REGISTRY_PROVIDER_SPECS,
    REQUIRED_MODEL_REGISTRY_PROVIDERS,
    build_model_registry_connector_manifest,
    build_model_registry_connector_registry,
    build_model_registry_metadata_event,
    validate_model_registry_connector_registry,
    validate_model_registry_connectors_packet,
    validate_model_registry_metadata,
)


MANIFEST_DIR = Path("examples/model-registries/connectors")
SAMPLE_METADATA = Path("examples/model-registries/metadata.sample.json")
INVALID_METADATA = Path("examples/model-registries/metadata.invalid-raw-content.json")
SAMPLE_PACKET = Path("examples/model-registries/enterprise-model-registry-connectors.sample.json")
LIVE_SANITIZED_PACKET = Path("examples/model-registries/enterprise-model-registry-connectors.live.sanitized.example.json")


def test_model_registry_connector_registry_covers_required_providers() -> None:
    registry = build_model_registry_connector_registry()

    assert set(registry["providers"]) == REQUIRED_MODEL_REGISTRY_PROVIDERS
    assert registry["connector_count"] == 4
    assert registry["compatibility_matrix"]["valid_connector_count"] == 4
    assert all(packet["certified"] for packet in registry["certification_packets"])


def test_checked_in_model_registry_manifests_match_registry() -> None:
    for provider in MODEL_REGISTRY_PROVIDER_SPECS:
        checked_in = json.loads((MANIFEST_DIR / f"{provider}.json").read_text(encoding="utf-8"))
        generated = build_model_registry_connector_manifest(provider)

        assert checked_in == generated
        assert validate_connector_manifest(checked_in)["valid"] is True
        assert checked_in["security"]["metadata_only"] is True
        assert checked_in["security"]["raw_model_egress_blocked"] is True


def test_manifest_directory_validates_as_complete_model_registry() -> None:
    manifests = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(MANIFEST_DIR.glob("*.json"))]

    result = validate_model_registry_connector_registry(manifests)

    assert result["valid"] is True
    assert result["blocker_count"] == 0
    assert result["provider_count"] == 4


def test_model_registry_registry_blocks_missing_provider() -> None:
    manifests = [
        build_model_registry_connector_manifest(provider)
        for provider in MODEL_REGISTRY_PROVIDER_SPECS
        if provider != "wandb"
    ]

    result = validate_model_registry_connector_registry(manifests)

    assert result["valid"] is False
    assert any(check["name"] == "providers" and "wandb" in check["message"] for check in result["checks"])


def test_model_registry_metadata_builds_metadata_only_event() -> None:
    payload = json.loads(SAMPLE_METADATA.read_text(encoding="utf-8"))

    result = validate_model_registry_metadata(payload)
    event = build_model_registry_metadata_event(payload)

    assert result["valid"] is True
    assert event["event_type"] == "cavra.model.registry.metadata"
    assert event["artifact_digest"].startswith("sha256:")
    assert "model_weights" not in event["metadata"]


def test_model_registry_metadata_blocks_raw_content_fields() -> None:
    payload = json.loads(INVALID_METADATA.read_text(encoding="utf-8"))

    result = validate_model_registry_metadata(payload)

    assert result["valid"] is False
    assert any(check["name"] == "no_raw_model_egress" and "model_weights" in check["message"] for check in result["checks"])


def test_model_registry_metadata_event_raises_on_raw_content() -> None:
    payload = json.loads(INVALID_METADATA.read_text(encoding="utf-8"))

    try:
        build_model_registry_metadata_event(payload)
    except ValueError as exc:
        assert "Raw content fields are forbidden" in str(exc)
    else:
        raise AssertionError("expected raw model metadata payload to be rejected")


def test_model_registry_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_model_registry_connectors_packet(packet)

    assert result["ready_for_model_registry_connector_contract"] is True
    assert result["ready_for_live_model_registry_connectors"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1


def test_model_registry_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_model_registry_connectors_packet(packet, require_live=True)

    assert result["ready_for_model_registry_connector_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_model_registry_live_sanitized_packet_passes_live_gate() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))

    result = validate_model_registry_connectors_packet(packet, require_live=True)

    assert result["ready_for_live_model_registry_connectors"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0
