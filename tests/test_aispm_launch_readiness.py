from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_aispm_launch_readiness_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-launch-readiness.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "AISPM launch readiness validation passed." in result.stdout


def test_aispm_launch_readiness_rollup_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/aispm-launch-readiness-rollup.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.aispm.launch_readiness_rollup.v1"
    assert packet["overall_status"] == "ready"
    assert packet["source_route"] == "apps/sandbox-ui/index.html#ai-posture"
    assert {source["source_id"] for source in packet["required_sources"]} == {
        "phase_b_closeout",
        "board_pack_artifact_index",
        "visual_smoke",
        "visual_freshness",
        "trial_lab_notebook",
        "github_pages_workflow",
        "hosted_pages_smoke",
        "hosted_deployment_freshness",
        "hosted_operator_status",
        "post_deploy_evidence",
        "release_evidence_index",
        "report_catalog_readiness",
        "report_delivery_setup_readiness",
        "report_operations_readiness",
        "report_governance_readiness",
        "report_assurance_readiness",
        "report_response_readiness",
        "report_trial_operations_readiness",
        "pilot_control_readiness",
    }
    assert {gate["gate_id"] for gate in packet["readiness_gates"]} == {
        "public_portal_contract",
        "board_pack_freshness",
        "visual_smoke_and_theme_readability",
        "trial_lab_notebook_publication",
        "github_pages_release_path",
        "hosted_pages_browser_smoke",
        "hosted_deployment_freshness",
        "hosted_operator_status",
        "post_deploy_evidence_artifact",
        "release_evidence_index",
        "report_catalog_readiness",
        "report_delivery_setup_readiness",
        "report_operations_readiness",
        "report_governance_readiness",
        "report_assurance_readiness",
        "report_response_readiness",
        "report_trial_operations_readiness",
        "pilot_control_readiness",
    }
    assert "Enterprise source code" in packet["public_safety_boundary"]
    assert "Private policy packs" in packet["enterprise_boundaries"]


def test_aispm_launch_readiness_is_wired_into_workflows_and_docs() -> None:
    command = "python scripts/validate-aispm-launch-readiness.py"
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

    for workflow_path in workflow_paths:
        assert command in Path(workflow_path).read_text(encoding="utf-8")

    for doc_path in doc_paths:
        text = Path(doc_path).read_text(encoding="utf-8")
        assert "docs/release-verifications/aispm-launch-readiness-rollup.md" in text
        assert "docs/release-verifications/aispm-launch-readiness-rollup.json" in text
        assert "scripts/validate-aispm-launch-readiness.py" in text
        assert "docs/release-verifications/hosted-sandbox-pages-smoke-validation.md" in text
        assert "docs/release-verifications/hosted-sandbox-pages-smoke-validation.json" in text
        assert "scripts/validate-hosted-sandbox-pages.mjs" in text
        assert "docs/release-verifications/hosted-sandbox-deployment-freshness.md" in text
        assert "docs/release-verifications/hosted-sandbox-deployment-freshness.json" in text
        assert "scripts/validate-hosted-sandbox-deployment-freshness.py" in text
        assert "community-v1.0.0-aispm-release-evidence-index" in text
        assert "docs/release-verifications/hosted-sandbox-operator-release-status.md" in text
        assert "docs/release-verifications/hosted-sandbox-operator-release-status.json" in text
        assert "scripts/validate-hosted-sandbox-operator-status.py" in text
        assert "cavra-hosted-sandbox-operator-status-packet.json" in text
        assert "docs/release-verifications/hosted-sandbox-post-deploy-evidence.md" in text
        assert "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json" in text
        assert "scripts/generate-hosted-sandbox-deploy-evidence.py" in text
        assert "scripts/validate-hosted-sandbox-deploy-evidence.py" in text
        assert "cavra-hosted-sandbox-post-deploy-evidence" in text
        assert "docs/release-verifications/aispm-release-evidence-index.md" in text
        assert "docs/release-verifications/aispm-release-evidence-index.json" in text
        assert "scripts/validate-aispm-release-evidence-index.py" in text
        assert "cavra-aispm-release-evidence-index-packet.json" in text
        assert "docs/release-verifications/aispm-report-catalog-readiness.md" in text
        assert "docs/release-verifications/aispm-report-catalog-readiness.json" in text
        assert "scripts/validate-aispm-report-catalog-readiness.py" in text
        assert "cavra-aispm-report-catalog-packet.json" in text
        assert "docs/release-verifications/aispm-report-delivery-setup-readiness.md" in text
        assert "docs/release-verifications/aispm-report-delivery-setup-readiness.json" in text
        assert "scripts/validate-aispm-report-delivery-setup-readiness.py" in text
        assert "cavra-aispm-report-delivery-setup-packet.json" in text
        assert "docs/release-verifications/aispm-report-operations-readiness.md" in text
        assert "docs/release-verifications/aispm-report-operations-readiness.json" in text
        assert "scripts/validate-aispm-report-operations-readiness.py" in text
        assert "cavra-aispm-report-operations-readiness-packet.json" in text
        assert "docs/release-verifications/aispm-report-governance-readiness.md" in text
        assert "docs/release-verifications/aispm-report-governance-readiness.json" in text
        assert "scripts/validate-aispm-report-governance-readiness.py" in text
        assert "cavra-aispm-report-governance-readiness-packet.json" in text
        assert "docs/release-verifications/aispm-report-assurance-readiness.md" in text
        assert "docs/release-verifications/aispm-report-assurance-readiness.json" in text
        assert "scripts/validate-aispm-report-assurance-readiness.py" in text
        assert "cavra-aispm-report-assurance-readiness-packet.json" in text
        assert "docs/release-verifications/aispm-report-response-readiness.md" in text
        assert "docs/release-verifications/aispm-report-response-readiness.json" in text
        assert "scripts/validate-aispm-report-response-readiness.py" in text
        assert "cavra-aispm-report-response-readiness-packet.json" in text
        assert "docs/release-verifications/aispm-report-trial-operations-readiness.md" in text
        assert "docs/release-verifications/aispm-report-trial-operations-readiness.json" in text
        assert "scripts/validate-aispm-report-trial-operations-readiness.py" in text
        assert "cavra-aispm-report-trial-operations-readiness-packet.json" in text
