from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_aispm_release_evidence_index_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-release-evidence-index.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "AISPM release evidence index validation passed." in result.stdout


def test_aispm_release_evidence_index_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/aispm-release-evidence-index.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.aispm.release_evidence_index.v1"
    assert packet["status"] == "ready"
    assert packet["portal_panel"] == "apps/sandbox-ui/index.html#ai-posture"
    assert packet["portal_packet"] == "cavra-aispm-release-evidence-index-packet.json"
    assert packet["validator"] == "scripts/validate-aispm-release-evidence-index.py"
    assert {item["title"] for item in packet["evidence_items"]} == {
        "AISPM Launch Readiness Rollup",
        "Launch Board Pack Artifact Index",
        "AISPM Report Catalog Readiness",
        "AISPM Report Delivery Setup Readiness",
        "AISPM Report Operations Readiness",
        "AISPM Report Governance Readiness",
        "AISPM Report Assurance Readiness",
        "AISPM Report Response Readiness",
        "AISPM Report Trial Operations Readiness",
        "AISPM Pilot Control Readiness",
        "AISPM v1.0 Public Release Readiness",
        "AISPM Final Announcement Readiness",
        "AISPM Visual Smoke Validation",
        "Hosted Sandbox Pages Smoke",
        "Hosted Sandbox Deployment Freshness",
        "Hosted Sandbox Operator Release Status",
        "Hosted Sandbox Post-Deploy Evidence",
        "Trial Lab Notebook Readiness",
        "Phase B Closeout Verification",
    }
    assert "Enterprise source code" in packet["public_safety_boundary"]
    assert packet["enterprise_boundary"]["tenant_evidence_room"] == (
        "requires_enterprise_evidence_store"
    )


def test_aispm_release_evidence_index_is_wired_into_portal_workflows_and_docs() -> None:
    command = "python scripts/validate-aispm-release-evidence-index.py"
    workflow_paths = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]
    doc_paths = [
        "README.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]

    portal_html = Path("apps/sandbox-ui/index.html").read_text(encoding="utf-8")
    portal_js = Path("apps/sandbox-ui/sandbox.js").read_text(encoding="utf-8")
    portal_css = Path("apps/sandbox-ui/styles.css").read_text(encoding="utf-8")

    for workflow_path in workflow_paths:
        assert command in Path(workflow_path).read_text(encoding="utf-8")

    for needle in [
        'id="aispmReleaseEvidenceIndex"',
        'id="aispmReleaseEvidenceManifest"',
        'id="copyAispmReleaseEvidenceIndexPacket"',
        'id="downloadAispmReleaseEvidenceIndexPacket"',
        'id="aispmReleaseEvidenceStatus"',
    ]:
        assert needle in portal_html

    for needle in [
        "renderAispmReleaseEvidenceIndex",
        "currentAispmReleaseEvidenceIndexPacket",
        "cavra.aispm.release_evidence_index_packet.v1",
        "cavra-aispm-release-evidence-index-packet.json",
    ]:
        assert needle in portal_js

    for needle in [
        ".aispm-release-evidence-panel",
        ".release-evidence-grid",
        ".release-evidence-manifest-grid",
        ".release-evidence-card",
    ]:
        assert needle in portal_css

    for doc_path in doc_paths:
        text = Path(doc_path).read_text(encoding="utf-8")
        assert "docs/release-verifications/aispm-release-evidence-index.md" in text
        assert "docs/release-verifications/aispm-release-evidence-index.json" in text
        assert "scripts/validate-aispm-release-evidence-index.py" in text
        assert "scripts/validate-aispm-report-catalog-readiness.py" in text
        assert "scripts/validate-aispm-report-delivery-setup-readiness.py" in text
        assert "scripts/validate-aispm-report-operations-readiness.py" in text
        assert "scripts/validate-aispm-report-governance-readiness.py" in text
        assert "scripts/validate-aispm-report-assurance-readiness.py" in text
        assert "scripts/validate-aispm-report-response-readiness.py" in text
        assert "scripts/validate-aispm-report-trial-operations-readiness.py" in text
        assert "scripts/validate-hosted-sandbox-deployment-freshness.py" in text
        assert "scripts/validate-hosted-sandbox-operator-status.py" in text
        assert "cavra-hosted-sandbox-operator-status-packet.json" in text
        assert "cavra-aispm-report-catalog-packet.json" in text
        assert "cavra-aispm-report-delivery-setup-packet.json" in text
        assert "cavra-aispm-report-operations-readiness-packet.json" in text
        assert "cavra-aispm-report-governance-readiness-packet.json" in text
        assert "cavra-aispm-report-assurance-readiness-packet.json" in text
        assert "cavra-aispm-report-response-readiness-packet.json" in text
        assert "cavra-aispm-report-trial-operations-readiness-packet.json" in text
        assert "docs/release-verifications/aispm-final-announcement-readiness.md" in text
        assert "docs/release-verifications/aispm-final-announcement-readiness.json" in text
        assert "scripts/validate-aispm-final-announcement-readiness.py" in text
        assert "cavra-aispm-final-announcement-readiness-packet.json" in text
        assert "cavra-aispm-release-evidence-index-packet.json" in text
