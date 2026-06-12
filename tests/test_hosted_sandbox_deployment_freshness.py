from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_hosted_sandbox_deployment_freshness_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-hosted-sandbox-deployment-freshness.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "Hosted sandbox deployment freshness validation passed." in result.stdout


def test_hosted_sandbox_deployment_freshness_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/hosted-sandbox-deployment-freshness.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.hosted_sandbox.deployment_freshness.v1"
    assert packet["status"] == "ready"
    assert packet["validated_target"] == "https://huzefaaa2.github.io/cavra/"
    assert packet["validator"] == "scripts/validate-hosted-sandbox-deployment-freshness.py"
    assert packet["workflow"] == ".github/workflows/deploy-sandbox.yml"
    assert packet["build_sentinel"] == "community-v1.0.0-aispm-release-evidence-index"
    assert set(packet["required_markers"]) >= {
        "AISPM Trial Lab Notebook Readiness",
        "Release Evidence Index",
        "Hosted Release Operator Status",
        "CSO Report Center",
        "cavra-aispm-report-catalog-packet.json",
        "Report Delivery Setup Readiness",
        "cavra-aispm-report-delivery-setup-packet.json",
        "Report Operations Readiness",
        "cavra-aispm-report-operations-readiness-packet.json",
        "Report Governance Readiness",
        "cavra-aispm-report-governance-readiness-packet.json",
        "Report Assurance Readiness",
        "cavra-aispm-report-assurance-readiness-packet.json",
        "Report Response Readiness",
        "cavra-aispm-report-response-readiness-packet.json",
        "Report Trial Operations Readiness",
        "cavra-aispm-report-trial-operations-readiness-packet.json",
        "cavra-aispm-release-evidence-index-packet.json",
        "cavra-hosted-sandbox-operator-status-packet.json",
        "community-v1.0.0-aispm-release-evidence-index",
    }
    assert packet["live_validation"] == "opt_in_with_CAVRA_CHECK_LIVE_SANDBOX"
    assert "Enterprise source code" in packet["public_safety_boundary"]


def test_hosted_sandbox_deployment_freshness_is_wired() -> None:
    portal = Path("apps/sandbox-ui/index.html").read_text(encoding="utf-8")
    hosted_validator = Path("scripts/validate-hosted-sandbox-pages.mjs").read_text(
        encoding="utf-8"
    )
    workflow = Path(".github/workflows/deploy-sandbox.yml").read_text(encoding="utf-8")
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
        "community-v1.0.0-aispm-release-evidence-index",
        "Release Evidence Index",
        "Hosted Release Operator Status",
        "CSO Report Center",
        "cavra-aispm-report-catalog-packet.json",
        "Report Delivery Setup Readiness",
        "cavra-aispm-report-delivery-setup-packet.json",
        "Report Operations Readiness",
        "cavra-aispm-report-operations-readiness-packet.json",
        "Report Governance Readiness",
        "cavra-aispm-report-governance-readiness-packet.json",
        "Report Assurance Readiness",
        "cavra-aispm-report-assurance-readiness-packet.json",
        "Report Response Readiness",
        "cavra-aispm-report-response-readiness-packet.json",
        "Report Trial Operations Readiness",
        "cavra-aispm-report-trial-operations-readiness-packet.json",
        "cavra-aispm-release-evidence-index-packet.json",
        "cavra-hosted-sandbox-operator-status-packet.json",
    ]:
        assert needle in portal
        assert needle in hosted_validator

    assert "python scripts/validate-hosted-sandbox-deployment-freshness.py" in workflow
    assert "CAVRA_CHECK_LIVE_SANDBOX=true" in workflow

    for doc_path in docs:
        text = Path(doc_path).read_text(encoding="utf-8")
        assert "docs/release-verifications/hosted-sandbox-deployment-freshness.md" in text
        assert "docs/release-verifications/hosted-sandbox-deployment-freshness.json" in text
        assert "scripts/validate-hosted-sandbox-deployment-freshness.py" in text
        assert "community-v1.0.0-aispm-release-evidence-index" in text
