from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_aispm_v100_public_release_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-v100-public-release.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "AISPM v1.0 public release readiness validation passed." in result.stdout


def test_aispm_v100_public_release_packet_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/aispm-v1.0-public-release-readiness.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.aispm_v100_public_release_readiness.v1"
    assert packet["edition"] == "community"
    assert packet["status"] == "ready_for_pr_and_pages_deploy"
    assert packet["portal_route"] == "https://huzefaaa2.github.io/cavra/#ai-posture"
    assert packet["validator"] == "scripts/validate-aispm-v100-public-release.py"
    assert {item["item_id"] for item in packet["readiness_items"]} == {
        "package_current_work",
        "github_pages_deploy",
        "release_notes_walkthrough",
        "lab_notebook_assets",
        "final_release_verification",
    }
    assert "private Huzefaaa2/cavra-enterprise repository" in packet["enterprise_boundary"]
    assert "private signing keys" in packet["public_safety_boundary"]


def test_aispm_v100_public_release_is_wired_into_docs_workflows_and_lab() -> None:
    required_needles = [
        "docs/releases/community-v1.0.0-aispm.md",
        "docs/aispm-v1.0-public-walkthrough.md",
        "docs/release-verifications/aispm-v1.0-public-release-readiness.md",
        "docs/release-verifications/aispm-v1.0-public-release-readiness.json",
        "scripts/validate-aispm-v100-public-release.py",
    ]
    docs = [
        "README.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/sandbox-portal-redesign.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
    ]
    workflows = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]

    for doc in docs:
        text = Path(doc).read_text(encoding="utf-8")
        for needle in required_needles:
            assert needle in text

    for workflow in workflows:
        assert "python scripts/validate-aispm-v100-public-release.py" in Path(
            workflow
        ).read_text(encoding="utf-8")

    lab = Path("docs/wiki/AISPM-Enterprise-Trial-Lab-Notebook.md").read_text(
        encoding="utf-8"
    )
    for asset in [
        "assets/aispm-lab/dashboard-desktop-classic.png",
        "assets/aispm-lab/aispm-desktop-sentinel.png",
        "assets/aispm-lab/aispm-report-center-panel.png",
        "assets/aispm-lab/aispm-board-pack-panel.png",
        "assets/aispm-lab/aispm-trial-flow.svg",
        "## Step-By-Step Lab",
    ]:
        assert asset in lab
