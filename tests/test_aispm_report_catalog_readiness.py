from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_aispm_report_catalog_readiness_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-report-catalog-readiness.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "AISPM report catalog readiness validation passed." in result.stdout


def test_aispm_report_catalog_readiness_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/aispm-report-catalog-readiness.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.aispm.report_catalog_readiness.v1"
    assert packet["status"] == "ready"
    assert packet["portal_packet"] == "cavra-aispm-report-catalog-packet.json"
    assert packet["validator"] == "scripts/validate-aispm-report-catalog-readiness.py"
    assert len(packet["community_reports"]) == 6
    assert {report["filename"] for report in packet["community_reports"]} == {
        "cavra-aispm-executive-risk-brief.md",
        "cavra-aispm-board-kpi-pack.json",
        "cavra-aispm-soc2-audit-summary.md",
        "cavra-aispm-control-coverage.csv",
        "cavra-aispm-evidence-freshness.csv",
        "cavra-aispm-agent-risk-register.csv",
    }
    assert "PDF Board Pack" in packet["enterprise_locked_reports"]
    assert "SMTP credentials" in packet["public_safety_boundary"]


def test_aispm_report_catalog_is_wired_into_portal_workflows_and_docs() -> None:
    command = "python scripts/validate-aispm-report-catalog-readiness.py"
    workflow_paths = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]
    doc_paths = [
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/architecture/aispm-report-center.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/AISPM-CSO-Report-Center.md",
    ]

    portal_html = Path("apps/sandbox-ui/index.html").read_text(encoding="utf-8")
    portal_js = Path("apps/sandbox-ui/sandbox.js").read_text(encoding="utf-8")

    for workflow_path in workflow_paths:
        assert command in Path(workflow_path).read_text(encoding="utf-8")

    for needle in [
        'data-report-catalog-packet="cavra-aispm-report-catalog-packet.json"',
        'id="copyAispmReportCatalogPacket"',
        'id="downloadAispmReportCatalogPacket"',
        'id="aispmReportStatus"',
    ]:
        assert needle in portal_html

    for needle in [
        "currentAispmReportCatalogPacket",
        "cavra.aispm.report_catalog_readiness_packet.v1",
        "cavra-aispm-report-catalog-packet.json",
        "copyAispmReportCatalogPacket",
        "downloadAispmReportCatalogPacket",
    ]:
        assert needle in portal_js

    for doc_path in doc_paths:
        text = Path(doc_path).read_text(encoding="utf-8")
        assert "docs/release-verifications/aispm-report-catalog-readiness.md" in text
        assert "docs/release-verifications/aispm-report-catalog-readiness.json" in text
        assert "scripts/validate-aispm-report-catalog-readiness.py" in text
        assert "cavra-aispm-report-catalog-packet.json" in text
