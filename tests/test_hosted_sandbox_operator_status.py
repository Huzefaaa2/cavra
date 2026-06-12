from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_hosted_sandbox_operator_status_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-hosted-sandbox-operator-status.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "Hosted sandbox operator release status validation passed." in result.stdout


def test_hosted_sandbox_operator_status_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/hosted-sandbox-operator-release-status.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.hosted_sandbox.operator_release_status.v1"
    assert packet["status"] == "ready"
    assert packet["portal_panel"] == "apps/sandbox-ui/index.html#ai-posture"
    assert packet["portal_packet"] == "cavra-hosted-sandbox-operator-status-packet.json"
    assert packet["validator"] == "scripts/validate-hosted-sandbox-operator-status.py"
    assert {check["check_id"] for check in packet["operator_checks"]} == {
        "local_portal_freshness",
        "live_pages_freshness",
        "hosted_browser_smoke",
        "post_deploy_evidence",
        "announcement_gate",
    }
    assert packet["operator_checks"][4]["status"] == "blocked_until_live_freshness_passes"
    assert "Enterprise source code" in packet["public_safety_boundary"]


def test_hosted_sandbox_operator_status_is_wired() -> None:
    html = Path("apps/sandbox-ui/index.html").read_text(encoding="utf-8")
    js = Path("apps/sandbox-ui/sandbox.js").read_text(encoding="utf-8")
    css = Path("apps/sandbox-ui/styles.css").read_text(encoding="utf-8")
    workflows = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]
    docs = [
        "README.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]

    for needle in [
        'id="aispmHostedReleaseStatus"',
        'id="aispmHostedReleaseChecklist"',
        'id="copyAispmHostedReleaseStatusPacket"',
        'id="downloadAispmHostedReleaseStatusPacket"',
        'id="aispmHostedReleaseStatusLine"',
    ]:
        assert needle in html

    for needle in [
        "renderAispmHostedReleaseStatus",
        "currentAispmHostedReleaseStatusPacket",
        "cavra.hosted_sandbox.operator_release_status_packet.v1",
        "cavra-hosted-sandbox-operator-status-packet.json",
    ]:
        assert needle in js

    for needle in [
        ".aispm-hosted-release-panel",
        ".hosted-release-status-grid",
        ".hosted-release-checklist-grid",
        ".hosted-release-check-card",
    ]:
        assert needle in css

    for workflow_path in workflows:
        assert "python scripts/validate-hosted-sandbox-operator-status.py" in Path(
            workflow_path
        ).read_text(encoding="utf-8")

    for doc_path in docs:
        text = Path(doc_path).read_text(encoding="utf-8")
        assert "docs/release-verifications/hosted-sandbox-operator-release-status.md" in text
        assert "docs/release-verifications/hosted-sandbox-operator-release-status.json" in text
        assert "scripts/validate-hosted-sandbox-operator-status.py" in text
        assert "cavra-hosted-sandbox-operator-status-packet.json" in text
