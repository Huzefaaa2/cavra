from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_hosted_sandbox_pages_smoke_record_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/hosted-sandbox-pages-smoke-validation.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.hosted_sandbox.pages_smoke_validation.v1"
    assert packet["status"] == "workflow_enforced"
    assert packet["command"] == "npm run validate:sandbox:hosted"
    assert packet["validator"] == "scripts/validate-hosted-sandbox-pages.mjs"
    assert packet["workflow"] == ".github/workflows/deploy-sandbox.yml"
    assert set(packet["coverage"]) >= {
        "hosted_index_http",
        "hosted_javascript_css_config",
        "hosted_brand_assets",
        "hosted_c4_container_diagram",
        "hosted_evidence_samples",
        "hosted_deployment_freshness_marker",
        "hosted_operator_release_status_marker",
        "aispm_report_catalog_packet_marker",
        "aispm_report_delivery_setup_packet_marker",
        "aispm_report_operations_readiness_packet_marker",
        "aispm_report_governance_readiness_packet_marker",
        "aispm_report_assurance_readiness_packet_marker",
        "aispm_report_response_readiness_packet_marker",
        "aispm_report_trial_operations_readiness_packet_marker",
        "dashboard_route_browser_render",
        "ai_posture_route_browser_render",
        "command_palette_board_pack_packet",
        "aispm_report_center_render",
        "aispm_board_pack_render",
    }


def test_hosted_sandbox_pages_smoke_script_and_workflow_are_wired() -> None:
    package = json.loads(Path("package.json").read_text(encoding="utf-8"))
    workflow = Path(".github/workflows/deploy-sandbox.yml").read_text(encoding="utf-8")
    script = Path("scripts/validate-hosted-sandbox-pages.mjs").read_text(encoding="utf-8")

    assert (
        package["scripts"]["validate:sandbox:hosted"]
        == "node scripts/validate-hosted-sandbox-pages.mjs"
    )
    assert "npm run validate:sandbox:hosted" in workflow
    assert "CAVRA_SANDBOX_URL" in workflow
    assert "needs.deploy.outputs.page_url" in workflow
    assert "python scripts/validate-hosted-sandbox-deployment-freshness.py" in workflow
    assert "CAVRA_CHECK_LIVE_SANDBOX=true" in workflow
    assert "https://huzefaaa2.github.io/cavra/" in script
    assert "#dashboard" in script
    assert "#ai-posture" in script
    assert "community-v1.0.0-aispm-release-evidence-index" in script
    assert "Hosted Release Operator Status" in script
    assert "cavra-hosted-sandbox-operator-status-packet.json" in script
    assert "Report Delivery Setup Readiness" in script
    assert "cavra-aispm-report-delivery-setup-packet.json" in script
    assert "Report Operations Readiness" in script
    assert "cavra-aispm-report-operations-readiness-packet.json" in script
    assert "Report Governance Readiness" in script
    assert "cavra-aispm-report-governance-readiness-packet.json" in script
    assert "Report Assurance Readiness" in script
    assert "cavra-aispm-report-assurance-readiness-packet.json" in script
    assert "Report Response Readiness" in script
    assert "cavra-aispm-report-response-readiness-packet.json" in script
    assert "Report Trial Operations Readiness" in script
    assert "cavra-aispm-report-trial-operations-readiness-packet.json" in script


def test_hosted_sandbox_post_deploy_evidence_contract_and_validator() -> None:
    packet = json.loads(
        Path("docs/release-verifications/hosted-sandbox-post-deploy-evidence.json").read_text(
            encoding="utf-8"
        )
    )
    result = subprocess.run(
        [sys.executable, "scripts/validate-hosted-sandbox-deploy-evidence.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "Hosted sandbox post-deploy evidence validation passed." in result.stdout
    assert packet["schema_version"] == "cavra.hosted_sandbox.post_deploy_evidence_contract.v1"
    assert packet["generator"] == "scripts/generate-hosted-sandbox-deploy-evidence.py"
    assert packet["validator"] == "scripts/validate-hosted-sandbox-deploy-evidence.py"
    assert packet["artifact_name"] == "cavra-hosted-sandbox-post-deploy-evidence"


def test_hosted_sandbox_post_deploy_evidence_generator_outputs_packet(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate-hosted-sandbox-deploy-evidence.py",
            "--output-dir",
            str(tmp_path),
            "--page-url",
            "https://huzefaaa2.github.io/cavra/",
            "--hosted-smoke-status",
            "pass",
            "--commit-sha",
            "abc123",
            "--repository",
            "Huzefaaa2/cavra",
            "--run-id",
            "123456",
            "--run-attempt",
            "1",
            "--workflow",
            "Deploy Sandbox",
            "--ref-name",
            "main",
            "--generated-at",
            "2026-06-12T00:00:00Z",
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    packet = json.loads((tmp_path / "hosted-sandbox-post-deploy-evidence.json").read_text())
    markdown = (tmp_path / "hosted-sandbox-post-deploy-evidence.md").read_text()

    assert packet["schema_version"] == "cavra.hosted_sandbox.post_deploy_evidence.v1"
    assert packet["status"] == "pass"
    assert packet["commit_sha"] == "abc123"
    assert packet["workflow_run_url"] == "https://github.com/Huzefaaa2/cavra/actions/runs/123456"
    assert packet["hosted_smoke"]["validator"] == "scripts/validate-hosted-sandbox-pages.mjs"
    assert "Hosted Sandbox Post-Deploy Evidence" in markdown
    assert "abc123" in markdown
