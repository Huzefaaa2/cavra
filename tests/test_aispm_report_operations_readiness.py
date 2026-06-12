from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_aispm_report_operations_readiness_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-report-operations-readiness.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "AISPM report operations readiness validation passed." in result.stdout


def test_aispm_report_operations_readiness_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/aispm-report-operations-readiness.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.aispm.report_operations_readiness.v1"
    assert packet["status"] == "ready"
    assert packet["portal_packet"] == "cavra-aispm-report-operations-readiness-packet.json"
    assert packet["validator"] == "scripts/validate-aispm-report-operations-readiness.py"
    assert {area["area_id"] for area in packet["operation_areas"]} == {
        "delivery_audit_events",
        "operations_dashboard",
        "retention_lifecycle",
        "search_and_retrieval",
        "export_package_manifest",
    }
    assert set(packet["enterprise_boundaries"].values()) == {"requires_cavra_enterprise"}
    assert "raw report payloads" in packet["public_safety_boundary"]


def test_aispm_report_operations_is_wired_into_portal_workflows_and_docs() -> None:
    command = "python scripts/validate-aispm-report-operations-readiness.py"
    workflow_paths = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]
    doc_paths = [
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/architecture/aispm-report-center.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/AISPM-CSO-Report-Center.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]

    portal_html = Path("apps/sandbox-ui/index.html").read_text(encoding="utf-8")
    portal_js = Path("apps/sandbox-ui/sandbox.js").read_text(encoding="utf-8")
    portal_css = Path("apps/sandbox-ui/styles.css").read_text(encoding="utf-8")

    for workflow_path in workflow_paths:
        assert command in Path(workflow_path).read_text(encoding="utf-8")

    for needle in [
        'data-report-operations-packet="cavra-aispm-report-operations-readiness-packet.json"',
        'id="aispmReportOperationsReadiness"',
        'id="copyAispmReportOperationsPacket"',
        'id="downloadAispmReportOperationsPacket"',
        'id="aispmReportOperationsStatus"',
    ]:
        assert needle in portal_html

    for needle in [
        "currentAispmReportOperationsPacket",
        "cavra.aispm.report_operations_readiness_packet.v1",
        "cavra-aispm-report-operations-readiness-packet.json",
        "copyAispmReportOperationsPacket",
        "downloadAispmReportOperationsPacket",
    ]:
        assert needle in portal_js

    for needle in [
        ".aispm-report-operations-panel",
        ".report-operations-grid",
        ".report-operations-card",
    ]:
        assert needle in portal_css

    for doc_path in doc_paths:
        text = Path(doc_path).read_text(encoding="utf-8")
        assert "docs/release-verifications/aispm-report-operations-readiness.md" in text
        assert "docs/release-verifications/aispm-report-operations-readiness.json" in text
        assert "scripts/validate-aispm-report-operations-readiness.py" in text
        assert "cavra-aispm-report-operations-readiness-packet.json" in text
