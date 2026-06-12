from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_aispm_pilot_control_readiness_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-pilot-control-readiness.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "AISPM pilot control readiness validation passed." in result.stdout


def test_aispm_pilot_control_readiness_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/aispm-pilot-control-readiness.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.aispm.pilot_control_readiness.v1"
    assert packet["status"] == "ready"
    assert packet["portal_packet"] == "cavra-aispm-pilot-control-readiness-packet.json"
    assert packet["validator"] == "scripts/validate-aispm-pilot-control-readiness.py"
    assert {area["area_id"] for area in packet["control_areas"]} == {
        "pilot_exception_register",
        "pilot_risk_acceptance",
        "pilot_launch_board_pack",
        "board_pack_artifact_freshness",
        "launch_readiness_rollup",
    }
    assert set(packet["enterprise_boundaries"].values()) == {
        "requires_cavra_enterprise_or_saas",
        "requires_cavra_enterprise_report_service",
        "requires_enterprise_evidence_store",
    }
    assert "board minutes" in packet["public_safety_boundary"]


def test_aispm_pilot_control_readiness_is_wired_into_portal_workflows_and_docs() -> None:
    command = "python scripts/validate-aispm-pilot-control-readiness.py"
    workflow_paths = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]
    doc_paths = [
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
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
        'data-pilot-control-packet="cavra-aispm-pilot-control-readiness-packet.json"',
        'id="aispmPilotControlReadiness"',
        'id="copyAispmPilotControlReadinessPacket"',
        'id="downloadAispmPilotControlReadinessPacket"',
        'id="aispmPilotControlStatus"',
    ]:
        assert needle in portal_html

    for needle in [
        "currentAispmPilotControlReadinessPacket",
        "cavra.aispm.pilot_control_readiness_packet.v1",
        "cavra-aispm-pilot-control-readiness-packet.json",
        "copyAispmPilotControlReadinessPacket",
        "downloadAispmPilotControlReadinessPacket",
    ]:
        assert needle in portal_js

    for needle in [
        ".aispm-pilot-control-panel",
        ".pilot-control-grid",
        ".pilot-control-card",
    ]:
        assert needle in portal_css

    for doc_path in doc_paths:
        text = Path(doc_path).read_text(encoding="utf-8")
        assert "docs/release-verifications/aispm-pilot-control-readiness.md" in text
        assert "docs/release-verifications/aispm-pilot-control-readiness.json" in text
        assert "scripts/validate-aispm-pilot-control-readiness.py" in text
        assert "cavra-aispm-pilot-control-readiness-packet.json" in text
