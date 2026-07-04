from __future__ import annotations

import json
from pathlib import Path

from cavra.generic_agent_adapter import (
    ACTION_TAXONOMY,
    GENERIC_ACTION_TAXONOMY_SCHEMA,
    GENERIC_ADAPTER_MANIFEST_SCHEMA,
    build_action_taxonomy,
    build_generic_adapter_readiness_packet,
    build_sample_adapter_manifest,
    build_sample_generic_actions,
    evaluate_generic_action,
    evaluate_generic_actions,
    validate_adapter_manifest,
    validate_generic_adapter_readiness_packet,
    write_generic_adapter_artifacts,
)


TAXONOMY = Path("examples/generic-adapters/action-taxonomy.json")
MANIFEST = Path("examples/generic-adapters/reference-business-agent.manifest.json")
ACTIONS = Path("examples/generic-adapters/non-coding-agent-actions.sample.json")
SAMPLE_PACKET = Path("examples/generic-adapters/enterprise-generic-agent-adapter.sample.json")
LIVE_PACKET = Path("examples/generic-adapters/enterprise-generic-agent-adapter.live.sanitized.example.json")


def test_action_taxonomy_matches_checked_in_taxonomy() -> None:
    generated = build_action_taxonomy()
    checked_in = json.loads(TAXONOMY.read_text(encoding="utf-8"))

    assert generated["schema_version"] == GENERIC_ACTION_TAXONOMY_SCHEMA
    assert checked_in["schema_version"] == generated["schema_version"]
    assert {item["action_type"] for item in checked_in["actions"]} == set(ACTION_TAXONOMY)


def test_sample_adapter_manifest_validates() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    result = validate_adapter_manifest(manifest)

    assert manifest["schema_version"] == GENERIC_ADAPTER_MANIFEST_SCHEMA
    assert result["valid"] is True
    assert result["blocker_count"] == 0


def test_adapter_manifest_blocks_unknown_actions_and_unsafe_security() -> None:
    manifest = build_sample_adapter_manifest()
    manifest["supported_actions"].append("unknown.business_action")
    manifest["security"]["raw_customer_data_egress_allowed"] = True

    result = validate_adapter_manifest(manifest)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"supported_actions", "security"} <= blocker_names
    assert result["valid"] is False


def test_generic_action_evaluation_covers_allow_approval_and_block() -> None:
    payload = json.loads(ACTIONS.read_text(encoding="utf-8"))

    report = evaluate_generic_actions(payload["actions"])

    assert report["decision_counts"]["allow"] == 1
    assert report["decision_counts"]["require_approval"] == 2
    assert report["decision_counts"]["block"] == 1
    assert {item["schema_version"] for item in report["evaluations"]} == {"cavra.generic-agent-adapter.evaluation.v1"}


def test_generic_action_maps_runtime_action_to_runtime_guard() -> None:
    result = evaluate_generic_action(
        {
            "action_id": "runtime-001",
            "adapter_id": "engineering-agent",
            "action_type": "execute_command",
            "target": "terraform apply -auto-approve",
            "requested_operation": "terraform apply -auto-approve",
            "agent_id": "iac-agent",
        }
    )

    assert result["decision"] == "block"
    assert result["rule_id"] == "commands.block"
    assert result["adapter_id"] == "engineering-agent"


def test_unknown_generic_action_requires_approval() -> None:
    result = evaluate_generic_action(
        {
            "action_id": "unknown-001",
            "adapter_id": "new-agent",
            "action_type": "new_domain.side_effect",
            "target": "system/resource",
            "requested_operation": "mutate resource",
        }
    )

    assert result["decision"] == "require_approval"
    assert result["rule_id"] == "generic_adapter.taxonomy.unknown.require_approval"


def test_sample_readiness_packet_validates_with_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_generic_adapter_readiness_packet(packet)

    assert result["ready_for_generic_adapter_contract"] is True
    assert result["ready_for_live_generic_adapter_sdk"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1


def test_live_sanitized_readiness_packet_passes_require_live() -> None:
    packet = json.loads(LIVE_PACKET.read_text(encoding="utf-8"))

    result = validate_generic_adapter_readiness_packet(packet, require_live=True)

    assert result["ready_for_generic_adapter_contract"] is True
    assert result["ready_for_live_generic_adapter_sdk"] is True
    assert result["blocker_count"] == 0


def test_readiness_packet_blocks_incomplete_scenario_and_missing_evidence() -> None:
    manifest = build_sample_adapter_manifest()
    actions = [build_sample_generic_actions()[0]]
    report = evaluate_generic_actions(actions)
    packet = build_generic_adapter_readiness_packet(manifest, report, evidence_mode="live")
    packet["operating_evidence"]["ci_run_ref"] = ""

    result = validate_generic_adapter_readiness_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"non_coding_scenario", "operating_evidence"} <= blocker_names
    assert result["ready_for_live_generic_adapter_sdk"] is False


def test_write_generic_adapter_artifacts(tmp_path: Path) -> None:
    export = write_generic_adapter_artifacts(build_sample_adapter_manifest(), build_sample_generic_actions(), tmp_path)

    assert Path(export["artifacts"]["taxonomy"]).exists()
    assert Path(export["artifacts"]["adapter_manifest"]).exists()
    assert Path(export["artifacts"]["sample_actions"]).exists()
    assert Path(export["artifacts"]["evaluation_report"]).exists()
    assert Path(export["artifacts"]["readiness_packet"]).exists()
