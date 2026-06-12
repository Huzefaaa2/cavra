#!/usr/bin/env python3
"""Validate the public-safe AISPM launch readiness rollup."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLLUP_PATH = ROOT / "docs/release-verifications/aispm-launch-readiness-rollup.json"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_file(path: str, failures: list[str]) -> None:
    require((ROOT / path).is_file(), f"missing required file: {path}", failures)


def require_text(path: str, needle: str, label: str, failures: list[str]) -> None:
    require(needle in read(path), f"{label} missing {needle}", failures)


def main() -> int:
    failures: list[str] = []
    required_files = [
        "docs/release-verifications/aispm-launch-readiness-rollup.json",
        "docs/release-verifications/aispm-launch-readiness-rollup.md",
        "docs/aispm-phase-b-closeout-verification.md",
        "docs/release-verifications/aispm-launch-board-pack-artifact-index.json",
        "docs/release-verifications/aispm-visual-smoke-validation.json",
        "docs/release-verifications/hosted-sandbox-pages-smoke-validation.json",
        "docs/release-verifications/hosted-sandbox-pages-smoke-validation.md",
        "docs/release-verifications/hosted-sandbox-deployment-freshness.json",
        "docs/release-verifications/hosted-sandbox-deployment-freshness.md",
        "docs/release-verifications/hosted-sandbox-operator-release-status.json",
        "docs/release-verifications/hosted-sandbox-operator-release-status.md",
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json",
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.md",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "docs/release-verifications/aispm-release-evidence-index.md",
        "docs/release-verifications/aispm-report-catalog-readiness.json",
        "docs/release-verifications/aispm-report-catalog-readiness.md",
        "docs/release-verifications/aispm-report-delivery-setup-readiness.json",
        "docs/release-verifications/aispm-report-delivery-setup-readiness.md",
        "docs/release-verifications/aispm-report-operations-readiness.json",
        "docs/release-verifications/aispm-report-operations-readiness.md",
        "docs/release-verifications/aispm-report-governance-readiness.json",
        "docs/release-verifications/aispm-report-governance-readiness.md",
        "docs/release-verifications/aispm-report-assurance-readiness.json",
        "docs/release-verifications/aispm-report-assurance-readiness.md",
        "docs/release-verifications/aispm-report-response-readiness.json",
        "docs/release-verifications/aispm-report-response-readiness.md",
        "docs/release-verifications/aispm-report-trial-operations-readiness.json",
        "docs/release-verifications/aispm-report-trial-operations-readiness.md",
        "docs/release-verifications/aispm-pilot-control-readiness.json",
        "docs/release-verifications/aispm-pilot-control-readiness.md",
        "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json",
        "scripts/validate-aispm-launch-readiness.py",
        "scripts/validate-aispm-launch-artifacts.py",
        "scripts/validate-aispm-visual-freshness.py",
        "scripts/validate-aispm-trial-lab-notebook.py",
        "scripts/validate-sandbox-portal.py",
        "scripts/generate-hosted-sandbox-deploy-evidence.py",
        "scripts/validate-hosted-sandbox-deploy-evidence.py",
        "scripts/validate-hosted-sandbox-deployment-freshness.py",
        "scripts/validate-hosted-sandbox-operator-status.py",
        "scripts/validate-aispm-release-evidence-index.py",
        "scripts/validate-aispm-report-catalog-readiness.py",
        "scripts/validate-aispm-report-delivery-setup-readiness.py",
        "scripts/validate-aispm-report-operations-readiness.py",
        "scripts/validate-aispm-report-governance-readiness.py",
        "scripts/validate-aispm-report-assurance-readiness.py",
        "scripts/validate-aispm-report-response-readiness.py",
        "scripts/validate-aispm-report-trial-operations-readiness.py",
        "scripts/validate-aispm-pilot-control-readiness.py",
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
        "README.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]
    for path in required_files:
        require_file(path, failures)

    if failures:
        for failure in failures:
            print(failure)
        return 1

    rollup = load_json("docs/release-verifications/aispm-launch-readiness-rollup.json")
    board_index = load_json(
        "docs/release-verifications/aispm-launch-board-pack-artifact-index.json"
    )
    visual = load_json("docs/release-verifications/aispm-visual-smoke-validation.json")
    hosted = load_json("docs/release-verifications/hosted-sandbox-pages-smoke-validation.json")
    hosted_freshness = load_json(
        "docs/release-verifications/hosted-sandbox-deployment-freshness.json"
    )
    hosted_operator = load_json(
        "docs/release-verifications/hosted-sandbox-operator-release-status.json"
    )
    post_deploy = load_json("docs/release-verifications/hosted-sandbox-post-deploy-evidence.json")
    release_index = load_json("docs/release-verifications/aispm-release-evidence-index.json")
    report_catalog = load_json("docs/release-verifications/aispm-report-catalog-readiness.json")
    report_setup = load_json("docs/release-verifications/aispm-report-delivery-setup-readiness.json")
    report_operations = load_json("docs/release-verifications/aispm-report-operations-readiness.json")
    report_governance = load_json("docs/release-verifications/aispm-report-governance-readiness.json")
    report_assurance = load_json("docs/release-verifications/aispm-report-assurance-readiness.json")
    report_response = load_json("docs/release-verifications/aispm-report-response-readiness.json")
    report_trial_ops = load_json("docs/release-verifications/aispm-report-trial-operations-readiness.json")
    pilot_control = load_json("docs/release-verifications/aispm-pilot-control-readiness.json")
    trial_lab = load_json(
        "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json"
    )

    require(
        rollup.get("schema_version") == "cavra.aispm.launch_readiness_rollup.v1",
        f"{ROLLUP_PATH}: invalid schema_version",
        failures,
    )
    require(rollup.get("overall_status") == "ready", f"{ROLLUP_PATH}: not ready", failures)
    require(
        rollup.get("source_route") == "apps/sandbox-ui/index.html#ai-posture",
        f"{ROLLUP_PATH}: source_route must point at the AISPM portal",
        failures,
    )

    expected_sources = {
        "phase_b_closeout": "docs/aispm-phase-b-closeout-verification.md",
        "board_pack_artifact_index": (
            "docs/release-verifications/aispm-launch-board-pack-artifact-index.json"
        ),
        "visual_smoke": "docs/release-verifications/aispm-visual-smoke-validation.json",
        "visual_freshness": "scripts/validate-aispm-visual-freshness.py",
        "trial_lab_notebook": (
            "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json"
        ),
        "github_pages_workflow": ".github/workflows/deploy-sandbox.yml",
        "hosted_pages_smoke": "docs/release-verifications/hosted-sandbox-pages-smoke-validation.json",
        "hosted_deployment_freshness": (
            "docs/release-verifications/hosted-sandbox-deployment-freshness.json"
        ),
        "hosted_operator_status": (
            "docs/release-verifications/hosted-sandbox-operator-release-status.json"
        ),
        "post_deploy_evidence": "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json",
        "release_evidence_index": "docs/release-verifications/aispm-release-evidence-index.json",
        "report_catalog_readiness": "docs/release-verifications/aispm-report-catalog-readiness.json",
        "report_delivery_setup_readiness": "docs/release-verifications/aispm-report-delivery-setup-readiness.json",
        "report_operations_readiness": "docs/release-verifications/aispm-report-operations-readiness.json",
        "report_governance_readiness": "docs/release-verifications/aispm-report-governance-readiness.json",
        "report_assurance_readiness": "docs/release-verifications/aispm-report-assurance-readiness.json",
        "report_response_readiness": "docs/release-verifications/aispm-report-response-readiness.json",
        "report_trial_operations_readiness": "docs/release-verifications/aispm-report-trial-operations-readiness.json",
        "pilot_control_readiness": "docs/release-verifications/aispm-pilot-control-readiness.json",
    }
    sources = {source.get("source_id"): source for source in rollup.get("required_sources", [])}
    require(set(sources) == set(expected_sources), f"{ROLLUP_PATH}: source set mismatch", failures)
    for source_id, source_path in expected_sources.items():
        source = sources.get(source_id, {})
        require(source.get("path") == source_path, f"{ROLLUP_PATH}: bad path for {source_id}", failures)
        require(
            source.get("status") in {"pass", "ready", "workflow_enforced"},
            f"{ROLLUP_PATH}: bad status for {source_id}",
            failures,
        )
        require_file(source_path, failures)

    gates = {gate.get("gate_id"): gate for gate in rollup.get("readiness_gates", [])}
    expected_gates = {
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
    require(set(gates) == expected_gates, f"{ROLLUP_PATH}: readiness gate set mismatch", failures)
    for gate_id, gate in gates.items():
        require(
            gate.get("status") in {"pass", "ready", "workflow_enforced"},
            f"{ROLLUP_PATH}: bad gate {gate_id}",
            failures,
        )

    require(
        board_index.get("visual_smoke_record")
        == "docs/release-verifications/aispm-visual-smoke-validation.json",
        "board-pack index must reference visual smoke record",
        failures,
    )
    require(
        board_index.get("visual_freshness_validator")
        == "scripts/validate-aispm-visual-freshness.py",
        "board-pack index must reference visual freshness validator",
        failures,
    )

    require(visual.get("status") == "pass", "visual smoke record must pass", failures)
    require(
        set(visual.get("coverage", []))
        >= {
            "dashboard_desktop_classic",
            "aispm_desktop_sentinel",
            "aispm_mobile_sentinel",
            "aispm_board_pack_panel",
            "aispm_report_center_panel",
            "command_palette_board_pack_packet",
            "theme_readability_sentinel_classic_retro_executive",
        },
        "visual smoke coverage is incomplete",
        failures,
    )

    require(trial_lab.get("overall_status") == "ready", "trial lab summary must be ready", failures)
    require(trial_lab.get("blockers") == [], "trial lab summary must not have blockers", failures)

    require(
        hosted.get("schema_version") == "cavra.hosted_sandbox.pages_smoke_validation.v1",
        "hosted Pages smoke record has invalid schema_version",
        failures,
    )
    require(
        hosted.get("status") == "workflow_enforced",
        "hosted Pages smoke record must be workflow_enforced",
        failures,
    )
    require(
        hosted.get("command") == "npm run validate:sandbox:hosted",
        "hosted Pages smoke command mismatch",
        failures,
    )
    require(
        hosted.get("validator") == "scripts/validate-hosted-sandbox-pages.mjs",
        "hosted Pages smoke validator mismatch",
        failures,
    )
    require(
        hosted_freshness.get("schema_version") == "cavra.hosted_sandbox.deployment_freshness.v1",
        "hosted deployment freshness record has invalid schema_version",
        failures,
    )
    require(
        hosted_freshness.get("build_sentinel")
        == "community-v1.0.0-aispm-release-evidence-index",
        "hosted deployment freshness sentinel mismatch",
        failures,
    )
    require(
        hosted_operator.get("schema_version") == "cavra.hosted_sandbox.operator_release_status.v1",
        "hosted operator status record has invalid schema_version",
        failures,
    )
    require(
        hosted_operator.get("portal_packet") == "cavra-hosted-sandbox-operator-status-packet.json",
        "hosted operator status portal packet mismatch",
        failures,
    )
    require(
        post_deploy.get("schema_version")
        == "cavra.hosted_sandbox.post_deploy_evidence_contract.v1",
        "hosted post-deploy evidence contract has invalid schema_version",
        failures,
    )
    require(
        post_deploy.get("generator") == "scripts/generate-hosted-sandbox-deploy-evidence.py",
        "hosted post-deploy evidence generator mismatch",
        failures,
    )
    require(
        release_index.get("schema_version") == "cavra.aispm.release_evidence_index.v1",
        "release evidence index has invalid schema_version",
        failures,
    )
    require(
        release_index.get("portal_packet") == "cavra-aispm-release-evidence-index-packet.json",
        "release evidence index portal packet mismatch",
        failures,
    )
    require(
        report_catalog.get("schema_version") == "cavra.aispm.report_catalog_readiness.v1",
        "report catalog readiness has invalid schema_version",
        failures,
    )
    require(
        report_catalog.get("portal_packet") == "cavra-aispm-report-catalog-packet.json",
        "report catalog readiness portal packet mismatch",
        failures,
    )
    require(
        report_setup.get("schema_version") == "cavra.aispm.report_delivery_setup_readiness.v1",
        "report delivery setup readiness has invalid schema_version",
        failures,
    )
    require(
        report_setup.get("portal_packet") == "cavra-aispm-report-delivery-setup-packet.json",
        "report delivery setup readiness portal packet mismatch",
        failures,
    )
    require(
        report_operations.get("schema_version") == "cavra.aispm.report_operations_readiness.v1",
        "report operations readiness has invalid schema_version",
        failures,
    )
    require(
        report_operations.get("portal_packet") == "cavra-aispm-report-operations-readiness-packet.json",
        "report operations readiness portal packet mismatch",
        failures,
    )
    require(
        report_governance.get("schema_version") == "cavra.aispm.report_governance_readiness.v1",
        "report governance readiness has invalid schema_version",
        failures,
    )
    require(
        report_governance.get("portal_packet") == "cavra-aispm-report-governance-readiness-packet.json",
        "report governance readiness portal packet mismatch",
        failures,
    )
    require(
        report_assurance.get("schema_version") == "cavra.aispm.report_assurance_readiness.v1",
        "report assurance readiness has invalid schema_version",
        failures,
    )
    require(
        report_assurance.get("portal_packet") == "cavra-aispm-report-assurance-readiness-packet.json",
        "report assurance readiness portal packet mismatch",
        failures,
    )
    require(
        report_response.get("schema_version") == "cavra.aispm.report_response_readiness.v1",
        "report response readiness has invalid schema_version",
        failures,
    )
    require(
        report_response.get("portal_packet") == "cavra-aispm-report-response-readiness-packet.json",
        "report response readiness portal packet mismatch",
        failures,
    )
    require(
        report_trial_ops.get("schema_version") == "cavra.aispm.report_trial_operations_readiness.v1",
        "report trial operations readiness has invalid schema_version",
        failures,
    )
    require(
        report_trial_ops.get("portal_packet") == "cavra-aispm-report-trial-operations-readiness-packet.json",
        "report trial operations readiness portal packet mismatch",
        failures,
    )
    require(
        pilot_control.get("schema_version") == "cavra.aispm.pilot_control_readiness.v1",
        "pilot control readiness has invalid schema_version",
        failures,
    )
    require(
        pilot_control.get("portal_packet") == "cavra-aispm-pilot-control-readiness-packet.json",
        "pilot control readiness portal packet mismatch",
        failures,
    )

    workflow_needles = [
        "python scripts/validate-sandbox-portal.py",
        "python scripts/validate-aispm-launch-artifacts.py",
        "npm run validate:sandbox:visual",
        "python scripts/validate-aispm-visual-freshness.py",
        "python scripts/validate-aispm-launch-readiness.py",
        "python scripts/validate-aispm-release-evidence-index.py",
        "python scripts/validate-aispm-report-catalog-readiness.py",
        "python scripts/validate-aispm-report-delivery-setup-readiness.py",
        "python scripts/validate-aispm-report-operations-readiness.py",
        "python scripts/validate-aispm-report-governance-readiness.py",
        "python scripts/validate-aispm-report-assurance-readiness.py",
        "python scripts/validate-aispm-report-response-readiness.py",
        "python scripts/validate-aispm-report-trial-operations-readiness.py",
        "python scripts/validate-aispm-pilot-control-readiness.py",
        "python scripts/validate-hosted-sandbox-deployment-freshness.py",
        "python scripts/validate-hosted-sandbox-operator-status.py",
        "python scripts/validate-hosted-sandbox-deploy-evidence.py",
    ]
    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        workflow = read(workflow_path)
        for needle in workflow_needles:
            require(needle in workflow, f"{workflow_path} missing {needle}", failures)
        if workflow_path == ".github/workflows/deploy-sandbox.yml":
            for needle in [
                "npm run validate:sandbox:hosted",
                "scripts/validate-hosted-sandbox-pages.mjs",
                "python scripts/generate-hosted-sandbox-deploy-evidence.py",
                "actions/upload-artifact@v4",
                "cavra-hosted-sandbox-post-deploy-evidence",
                "CAVRA_SANDBOX_URL",
                "needs.deploy.outputs.page_url",
            ]:
                require(needle in workflow, f"{workflow_path} missing {needle}", failures)

    doc_needles = [
        "docs/release-verifications/aispm-launch-readiness-rollup.md",
        "docs/release-verifications/aispm-launch-readiness-rollup.json",
        "scripts/validate-aispm-launch-readiness.py",
        "docs/release-verifications/hosted-sandbox-pages-smoke-validation.md",
        "docs/release-verifications/hosted-sandbox-pages-smoke-validation.json",
        "scripts/validate-hosted-sandbox-pages.mjs",
        "docs/release-verifications/hosted-sandbox-deployment-freshness.md",
        "docs/release-verifications/hosted-sandbox-deployment-freshness.json",
        "scripts/validate-hosted-sandbox-deployment-freshness.py",
        "community-v1.0.0-aispm-release-evidence-index",
        "docs/release-verifications/hosted-sandbox-operator-release-status.md",
        "docs/release-verifications/hosted-sandbox-operator-release-status.json",
        "scripts/validate-hosted-sandbox-operator-status.py",
        "cavra-hosted-sandbox-operator-status-packet.json",
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.md",
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json",
        "scripts/generate-hosted-sandbox-deploy-evidence.py",
        "scripts/validate-hosted-sandbox-deploy-evidence.py",
        "cavra-hosted-sandbox-post-deploy-evidence",
        "docs/release-verifications/aispm-release-evidence-index.md",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "scripts/validate-aispm-release-evidence-index.py",
        "cavra-aispm-release-evidence-index-packet.json",
        "docs/release-verifications/aispm-report-operations-readiness.md",
        "docs/release-verifications/aispm-report-operations-readiness.json",
        "scripts/validate-aispm-report-operations-readiness.py",
        "cavra-aispm-report-operations-readiness-packet.json",
        "docs/release-verifications/aispm-report-governance-readiness.md",
        "docs/release-verifications/aispm-report-governance-readiness.json",
        "scripts/validate-aispm-report-governance-readiness.py",
        "cavra-aispm-report-governance-readiness-packet.json",
        "docs/release-verifications/aispm-report-assurance-readiness.md",
        "docs/release-verifications/aispm-report-assurance-readiness.json",
        "scripts/validate-aispm-report-assurance-readiness.py",
        "cavra-aispm-report-assurance-readiness-packet.json",
        "docs/release-verifications/aispm-report-response-readiness.md",
        "docs/release-verifications/aispm-report-response-readiness.json",
        "scripts/validate-aispm-report-response-readiness.py",
        "cavra-aispm-report-response-readiness-packet.json",
        "docs/release-verifications/aispm-report-trial-operations-readiness.md",
        "docs/release-verifications/aispm-report-trial-operations-readiness.json",
        "scripts/validate-aispm-report-trial-operations-readiness.py",
        "cavra-aispm-report-trial-operations-readiness-packet.json",
        "docs/release-verifications/aispm-pilot-control-readiness.md",
        "docs/release-verifications/aispm-pilot-control-readiness.json",
        "scripts/validate-aispm-pilot-control-readiness.py",
        "cavra-aispm-pilot-control-readiness-packet.json",
    ]
    for doc_path in [
        "README.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]:
        for needle in doc_needles:
            require_text(doc_path, needle, doc_path, failures)

    forbidden_terms = [
        "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
        "CAVRA_TRIAL_OPERATOR_SESSION_SECRET",
        "license_private_key",
        "private_registry_token",
        "customer_identity_payload",
        "raw_prompt_payload",
        "hosted_telemetry_payload",
    ]
    combined_public_text = "\n".join(
        [
            read("docs/release-verifications/aispm-launch-readiness-rollup.json"),
            read("docs/release-verifications/aispm-launch-readiness-rollup.md"),
        ]
    )
    for term in forbidden_terms:
        require(term not in combined_public_text, f"rollup must not expose {term}", failures)

    if failures:
        print("AISPM launch readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM launch readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
