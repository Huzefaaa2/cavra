from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_aispm_visual_freshness_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-visual-freshness.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "AISPM visual freshness validation passed." in result.stdout


def test_aispm_visual_smoke_record_matches_public_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/aispm-visual-smoke-validation.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.aispm.visual_smoke_validation.v1"
    assert packet["status"] == "pass"
    assert packet["command"] == "npm run validate:sandbox:visual"
    assert packet["validator"] == "scripts/validate-sandbox-visual.mjs"
    assert set(packet["coverage"]) >= {
        "dashboard_desktop_classic",
        "aispm_desktop_sentinel",
        "aispm_mobile_sentinel",
        "aispm_board_pack_panel",
        "aispm_report_center_panel",
        "command_palette_board_pack_packet",
        "theme_readability_sentinel_classic_retro_executive",
    }
    assert set(packet["local_screenshots"]) == {
        ".cavra/visual-smoke/dashboard-desktop-classic.png",
        ".cavra/visual-smoke/aispm-desktop-sentinel.png",
        ".cavra/visual-smoke/aispm-board-pack-panel.png",
        ".cavra/visual-smoke/aispm-report-center-panel.png",
        ".cavra/visual-smoke/aispm-mobile-sentinel.png",
    }
    assert packet["enterprise_boundary"]["private_customer_screenshots"] == "requires_cavra_enterprise"
    assert packet["enterprise_boundary"]["tenant_visual_baselines"] == "requires_cavra_enterprise"
    assert (
        packet["enterprise_boundary"]["signed_visual_regression_approval"]
        == "requires_cavra_enterprise_or_saas"
    )


def test_aispm_visual_freshness_is_wired_into_release_workflows() -> None:
    workflow_paths = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]

    for workflow_path in workflow_paths:
        text = Path(workflow_path).read_text(encoding="utf-8")
        assert "actions/setup-node@v6" in text
        assert 'node-version: "24"' in text
        assert "npm ci" in text
        assert "npx playwright install --with-deps chromium" in text
        assert "npm run validate:sandbox:visual" in text
        assert "python scripts/validate-aispm-visual-freshness.py" in text
        if workflow_path == ".github/workflows/deploy-sandbox.yml":
            assert "npm run validate:sandbox:hosted" in text
            assert "scripts/validate-hosted-sandbox-pages.mjs" in text
