from __future__ import annotations

import json
from pathlib import Path

from cavra.audit_log import (
    append_audit_event,
    build_enterprise_audit_log_contract,
    build_enterprise_audit_log_readiness,
    validate_enterprise_audit_log_packet,
    verify_append_only_audit_log,
)


SAMPLE_PACKET = Path("examples/audit/enterprise-audit-log.sample.json")
LIVE_SANITIZED_PACKET = Path("examples/audit/enterprise-audit-log.live.sanitized.example.json")


def test_append_only_audit_log_hash_chain_verifies(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    append_audit_event(
        path,
        event_type="runtime.decision",
        actor="agent:claude-code",
        action="write_file",
        target="iam/admin-role.tf",
        decision="require_approval",
        tenant_id="tenant-a",
        workspace_id="workspace-prod",
        evidence_refs=["evidence://session-1"],
        key="secret",
        key_id="audit-key-1",
    )
    append_audit_event(
        path,
        event_type="approval.decision",
        actor="security-operator",
        action="approve",
        target="approval-1",
        decision="approved",
        tenant_id="tenant-a",
        workspace_id="workspace-prod",
        evidence_refs=["evidence://approval-1"],
        key="secret",
        key_id="audit-key-1",
    )

    result = verify_append_only_audit_log(path, key="secret", key_id="audit-key-1")

    assert result["valid"] is True
    assert result["record_count"] == 2
    assert result["first_sequence"] == 1
    assert result["last_sequence"] == 2
    assert result["last_record_hash"]


def test_append_only_audit_log_detects_tampering(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    append_audit_event(
        path,
        event_type="runtime.decision",
        actor="agent:claude-code",
        action="run_command",
        target="terraform apply",
        decision="block",
        key="secret",
    )
    record = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    record["decision"] = "allow"
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    result = verify_append_only_audit_log(path, key="secret")

    assert result["valid"] is False
    assert any("record_hash mismatch" in error for error in result["errors"])
    assert any("signature mismatch" in error for error in result["errors"])


def test_enterprise_audit_log_contract_defines_required_controls() -> None:
    contract = build_enterprise_audit_log_contract()

    assert contract["schema_version"] == "cavra.audit-log.contract.v1"
    assert "azure_immutable_blob" in contract["supported_immutable_stores"]
    assert "audit_integrity_failure" in contract["required_alerts"]
    assert "auditor_package" in contract["required_exports"]


def test_enterprise_audit_log_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_audit_log_packet(packet)

    assert result["ready_for_enterprise_audit_log_contract"] is True
    assert result["ready_for_enterprise_live_audit_log"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1
    assert result["blocker_count"] == 0


def test_enterprise_audit_log_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_audit_log_packet(packet, require_live=True)

    assert result["ready_for_enterprise_audit_log_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_enterprise_audit_log_live_sanitized_example_passes_require_live() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_audit_log_packet(packet, require_live=True)

    assert result["ready_for_enterprise_live_audit_log"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_enterprise_audit_log_blocks_weak_storage_and_retention() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))
    packet["storage"]["separate_from_evidence_bundles"] = False
    packet["integrity"]["tamper_detection_tested"] = False
    packet["retention"]["retention_days"] = 30
    packet["exports"]["formats"] = ["jsonl"]
    packet["monitoring"]["alerts"] = ["audit_write_failure"]

    result = validate_enterprise_audit_log_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"storage", "integrity", "retention", "exports", "monitoring"} <= blocker_names
    assert result["ready_for_enterprise_live_audit_log"] is False


def test_enterprise_audit_log_readiness_without_packet_is_contract_ready_with_warning() -> None:
    result = build_enterprise_audit_log_readiness()

    assert result["schema_version"] == "cavra.audit-log.readiness.v1"
    assert result["ready_for_enterprise_audit_log_contract"] is True
    assert result["ready_for_enterprise_live_audit_log"] is False
    assert result["status"] == "ready_with_warnings"


def test_enterprise_audit_log_workflow_runs_require_live_gate() -> None:
    workflow = Path(".github/workflows/enterprise-audit-log.yml").read_text(encoding="utf-8")

    assert "Validate live audit-log packet" in workflow
    assert "--require-live" in workflow
    assert "examples/audit/enterprise-audit-log.live.sanitized.example.json" in workflow
