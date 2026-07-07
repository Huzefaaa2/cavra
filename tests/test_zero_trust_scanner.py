from __future__ import annotations

import json
from pathlib import Path

from cavra.zero_trust_scanner import (
    build_zero_trust_scan_result,
    build_zero_trust_scan_result_from_file,
    find_forbidden_egress_fields,
    sanitize_scanner_payload,
    validate_zero_trust_scan_result,
    validate_zero_trust_scanner_packet,
)


SAMPLE_RESULT = Path("examples/zero-trust-scanner/scan-result.sample.json")
INVALID_RESULT = Path("examples/zero-trust-scanner/scan-result.invalid-raw-egress.json")
REFERENCE_ARTIFACT = Path("examples/zero-trust-scanner/reference-artifact.txt")
SAMPLE_PACKET = Path("examples/zero-trust-scanner/enterprise-zero-trust-scanner.sample.json")
LIVE_SANITIZED_PACKET = Path("examples/zero-trust-scanner/enterprise-zero-trust-scanner.live.sanitized.example.json")


def test_zero_trust_scan_result_validates() -> None:
    payload = json.loads(SAMPLE_RESULT.read_text(encoding="utf-8"))

    result = validate_zero_trust_scan_result(payload)
    scan_result = build_zero_trust_scan_result(payload)

    assert result["valid"] is True
    assert scan_result["schema_version"] == "cavra.zero-trust-scanner.result.v1"
    assert scan_result["artifact_digest"].startswith("sha256:")
    assert scan_result["risk_score"] == 72


def test_zero_trust_scan_result_blocks_raw_egress() -> None:
    payload = json.loads(INVALID_RESULT.read_text(encoding="utf-8"))

    result = validate_zero_trust_scan_result(payload)

    assert result["valid"] is False
    assert any(check["name"] == "no_raw_egress" and "model_weights" in check["message"] for check in result["checks"])


def test_zero_trust_scan_result_raises_on_raw_egress() -> None:
    payload = json.loads(INVALID_RESULT.read_text(encoding="utf-8"))

    try:
        build_zero_trust_scan_result(payload)
    except ValueError as exc:
        assert "Forbidden raw egress fields detected" in str(exc)
    else:
        raise AssertionError("expected raw egress payload to be rejected")


def test_zero_trust_sanitizer_removes_forbidden_fields() -> None:
    payload = {
        "metadata": {
            "safe": "value",
            "source_code": "print('secret')",
            "nested": {"credential": "token", "lineage_ref": "lineage://ok"},
        }
    }

    sanitized = sanitize_scanner_payload(payload)

    assert sanitized == {"metadata": {"safe": "value", "nested": {"lineage_ref": "lineage://ok"}}}
    assert find_forbidden_egress_fields(payload) == {"metadata.source_code", "metadata.nested.credential"}


def test_zero_trust_file_scan_uses_hash_only() -> None:
    result = build_zero_trust_scan_result_from_file(REFERENCE_ARTIFACT)

    assert result["asset_ref"] == "file://reference-artifact.txt"
    assert result["artifact_digest"].startswith("sha256:")
    assert result["metadata"]["file_size_bytes"] > 0
    assert "file_contents" not in result["metadata"]


def test_zero_trust_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_zero_trust_scanner_packet(packet)

    assert result["ready_for_zero_trust_scanner_contract"] is True
    assert result["ready_for_live_zero_trust_scanner"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1


def test_zero_trust_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_zero_trust_scanner_packet(packet, require_live=True)

    assert result["ready_for_zero_trust_scanner_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_zero_trust_live_sanitized_packet_passes_live_gate() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))

    result = validate_zero_trust_scanner_packet(packet, require_live=True)

    assert result["ready_for_live_zero_trust_scanner"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0


def test_zero_trust_packet_blocks_missing_controls() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))
    packet["deployment"]["supported_modes"] = ["container"]
    packet["scanner_artifacts"]["artifact_ids"] = ["scanner_result_contract"]
    packet["egress_controls"]["raw_model_blocked"] = False
    packet["operating_evidence"]["deployment_validation_ref"] = ""

    result = validate_zero_trust_scanner_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"deployment", "scanner_artifacts", "egress_controls", "operating_evidence"} <= blocker_names
    assert result["ready_for_live_zero_trust_scanner"] is False


def test_zero_trust_workflow_runs_require_live_gate() -> None:
    workflow = Path(".github/workflows/zero-trust-scanner.yml").read_text(encoding="utf-8")

    assert "Validate sanitized live packet" in workflow
    assert "--require-live" in workflow
    assert "examples/zero-trust-scanner/enterprise-zero-trust-scanner.live.sanitized.example.json" in workflow


def test_zero_trust_closeout_docs_reference_sanitized_live_packet() -> None:
    closeout = Path("docs/zero-trust-scanner-r4-closeout.md").read_text(encoding="utf-8")

    assert "examples/zero-trust-scanner/enterprise-zero-trust-scanner.live.sanitized.example.json" in closeout
    assert "ready_for_live_zero_trust_scanner" in closeout
    assert "raw-egress negative fixture" in closeout
    assert "Phase 4 Closeout Handoff" in closeout
