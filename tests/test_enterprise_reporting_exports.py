from __future__ import annotations

import csv
import json
from pathlib import Path

from cavra.enterprise_reporting_exports import (
    REQUIRED_EXPORTS,
    build_enterprise_report_export_readiness,
    export_enterprise_reporting_package,
    validate_enterprise_report_export_packet,
)


SAMPLE_PACKET = Path("examples/reports/enterprise-report-exports.sample.json")
LIVE_SANITIZED_PACKET = Path("examples/reports/enterprise-report-exports.live.sanitized.example.json")


def test_enterprise_reporting_package_writes_expected_artifacts(tmp_path: Path) -> None:
    manifest = export_enterprise_reporting_package(tmp_path)

    filenames = {artifact["filename"] for artifact in manifest["artifacts"]}
    export_ids = {artifact["export_id"] for artifact in manifest["artifacts"]}
    assert export_ids == REQUIRED_EXPORTS
    assert filenames == {
        "executive-summary.json",
        "bi-metrics.csv",
        "auditor-narrative.md",
        "board-pack-pdf-manifest.json",
    }
    assert manifest["manifest_sha256"]
    assert (tmp_path / "enterprise-report-export-manifest.json").exists()


def test_enterprise_reporting_exports_have_parseable_json_csv_and_markdown(tmp_path: Path) -> None:
    export_enterprise_reporting_package(tmp_path, generated_at="2026-07-04T00:00:00Z")

    executive = json.loads((tmp_path / "executive-summary.json").read_text(encoding="utf-8"))
    board_manifest = json.loads((tmp_path / "board-pack-pdf-manifest.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "auditor-narrative.md").read_text(encoding="utf-8")
    with (tmp_path / "bi-metrics.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert executive["schema_version"] == "cavra.enterprise.executive-summary.v1"
    assert board_manifest["format"] == "pdf"
    assert board_manifest["renderer"] == "requires_cavra_enterprise"
    assert "# CAVRA Auditor Narrative" in markdown
    assert {row["metric"] for row in rows} >= {"runtime_decisions", "audit_readiness_score"}


def test_enterprise_report_export_sample_packet_validates_with_live_warning() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_report_export_packet(packet)

    assert result["ready_for_enterprise_report_export_contract"] is True
    assert result["ready_for_enterprise_live_report_exports"] is False
    assert result["status"] == "ready_with_warnings"
    assert result["warning_count"] == 1
    assert result["blocker_count"] == 0


def test_enterprise_report_export_live_requirement_blocks_sample_packet() -> None:
    packet = json.loads(SAMPLE_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_report_export_packet(packet, require_live=True)

    assert result["ready_for_enterprise_report_export_contract"] is False
    assert result["status"] == "blocked"
    assert any(check["name"] == "evidence_mode" and check["status"] == "blocker" for check in result["checks"])


def test_enterprise_report_export_live_sanitized_example_passes_require_live() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))

    result = validate_enterprise_report_export_packet(packet, require_live=True)

    assert result["ready_for_enterprise_live_report_exports"] is True
    assert result["status"] == "ready"
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0


def test_enterprise_report_export_blocks_missing_artifacts_and_controls() -> None:
    packet = json.loads(LIVE_SANITIZED_PACKET.read_text(encoding="utf-8"))
    packet["export_catalog"]["formats"] = ["json"]
    packet["artifacts"]["generated_exports"] = ["executive_json"]
    packet["distribution"]["channels"] = ["portal"]
    packet["controls"]["watermarking_enabled"] = False
    packet["operating_evidence"]["auditor_handoff_ref"] = ""

    result = validate_enterprise_report_export_packet(packet, require_live=True)

    blocker_names = {check["name"] for check in result["checks"] if check["status"] == "blocker"}
    assert {"export_catalog", "artifacts", "distribution", "controls", "operating_evidence"} <= blocker_names
    assert result["ready_for_enterprise_live_report_exports"] is False


def test_enterprise_report_export_readiness_without_packet_is_contract_ready_with_warning() -> None:
    result = build_enterprise_report_export_readiness()

    assert result["schema_version"] == "cavra.enterprise.report-exports.readiness.v1"
    assert result["ready_for_enterprise_report_export_contract"] is True
    assert result["ready_for_enterprise_live_report_exports"] is False
    assert result["status"] == "ready_with_warnings"


def test_enterprise_report_export_workflow_runs_require_live_gate() -> None:
    workflow = Path(".github/workflows/enterprise-report-exports.yml").read_text(encoding="utf-8")

    assert "Validate live report export packet" in workflow
    assert "--require-live" in workflow
    assert "examples/reports/enterprise-report-exports.live.sanitized.example.json" in workflow


def test_enterprise_report_export_closeout_docs_reference_sanitized_live_packet() -> None:
    closeout = Path("docs/reporting-exports-r3-closeout.md").read_text(encoding="utf-8")

    assert "examples/reports/enterprise-report-exports.live.sanitized.example.json" in closeout
    assert "ready_for_enterprise_live_report_exports" in closeout
    assert "R4.1 Handoff" in closeout
