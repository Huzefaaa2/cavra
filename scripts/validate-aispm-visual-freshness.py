#!/usr/bin/env python3
"""Validate AISPM visual-smoke freshness across docs, wiki, package, and CI."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VISUAL_JSON = Path("docs/release-verifications/aispm-visual-smoke-validation.json")
VISUAL_MD = Path("docs/release-verifications/aispm-visual-smoke-validation.md")
BOARD_INDEX_JSON = Path("docs/release-verifications/aispm-launch-board-pack-artifact-index.json")
BOARD_INDEX_MD = Path("docs/release-verifications/aispm-launch-board-pack-artifact-index.md")

REQUIRED_SCREENSHOTS = {
    ".cavra/visual-smoke/dashboard-desktop-classic.png",
    ".cavra/visual-smoke/aispm-desktop-sentinel.png",
    ".cavra/visual-smoke/aispm-board-pack-panel.png",
    ".cavra/visual-smoke/aispm-report-center-panel.png",
    ".cavra/visual-smoke/aispm-mobile-sentinel.png",
}

REQUIRED_COVERAGE = {
    "dashboard_desktop_classic",
    "aispm_desktop_sentinel",
    "aispm_mobile_sentinel",
    "aispm_board_pack_panel",
    "aispm_report_center_panel",
    "command_palette_board_pack_packet",
    "theme_readability_sentinel_classic_retro_executive",
}

REQUIRED_DOCS = {
    "docs/sandbox-portal-redesign.md",
    "docs/sandbox-portal-smoke-validation.md",
    "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
    "docs/wiki/Home.md",
    "docs/wiki/AISPM-Launch-Board-Pack-Artifact-Index.md",
}

REQUIRED_WORKFLOWS = {
    ".github/workflows/community-ci.yml",
    ".github/workflows/release-community.yml",
    ".github/workflows/deploy-sandbox.yml",
}


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_file(path: str | Path, failures: list[str]) -> None:
    if not (ROOT / path).is_file():
        failures.append(f"missing required file: {path}")


def require(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"missing {label}: {needle}")


def load_json(path: Path, failures: list[str]) -> dict[str, object]:
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as exc:
        failures.append(f"{path}: invalid JSON: {exc}")
        return {}


def main() -> int:
    failures: list[str] = []
    required_files = {
        VISUAL_JSON,
        VISUAL_MD,
        BOARD_INDEX_JSON,
        BOARD_INDEX_MD,
        "package.json",
        "package-lock.json",
        "scripts/validate-sandbox-visual.mjs",
        "scripts/validate-hosted-sandbox-pages.mjs",
        "scripts/validate-aispm-launch-artifacts.py",
        "scripts/validate-sandbox-portal.py",
    }
    required_files.update(REQUIRED_DOCS)
    required_files.update(REQUIRED_WORKFLOWS)
    for path in sorted(str(path) for path in required_files):
        require_file(path, failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    visual = load_json(VISUAL_JSON, failures)
    board_index = load_json(BOARD_INDEX_JSON, failures)
    package = load_json(Path("package.json"), failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    if visual.get("schema_version") != "cavra.aispm.visual_smoke_validation.v1":
        failures.append(f"{VISUAL_JSON}: invalid schema_version")
    if visual.get("status") != "pass":
        failures.append(f"{VISUAL_JSON}: status must be pass")
    if visual.get("command") != "npm run validate:sandbox:visual":
        failures.append(f"{VISUAL_JSON}: command must be npm run validate:sandbox:visual")
    if visual.get("validator") != "scripts/validate-sandbox-visual.mjs":
        failures.append(f"{VISUAL_JSON}: validator must be scripts/validate-sandbox-visual.mjs")

    coverage = set(visual.get("coverage", []))
    screenshots = set(visual.get("local_screenshots", []))
    missing_coverage = REQUIRED_COVERAGE - coverage
    missing_screenshots = REQUIRED_SCREENSHOTS - screenshots
    if missing_coverage:
        failures.append(f"{VISUAL_JSON}: missing coverage {sorted(missing_coverage)}")
    if missing_screenshots:
        failures.append(f"{VISUAL_JSON}: missing local screenshots {sorted(missing_screenshots)}")

    enterprise_boundary = visual.get("enterprise_boundary", {})
    for key in [
        "private_customer_screenshots",
        "tenant_visual_baselines",
        "signed_visual_regression_approval",
    ]:
        if key not in enterprise_boundary:
            failures.append(f"{VISUAL_JSON}: missing enterprise boundary {key}")

    board_artifacts = {artifact.get("filename") for artifact in board_index.get("artifacts", [])}
    for filename in [
        "cavra-aispm-pilot-launch-decision-packet.json",
        "cavra-aispm-pilot-evidence-room-packet.json",
        "cavra-aispm-pilot-risk-acceptance-packet.json",
        "cavra-aispm-pilot-exception-register-packet.json",
        "cavra-aispm-evidence-reviewer-checklist-packet.json",
        "cavra-aispm-executive-risk-brief.md",
        "cavra-aispm-board-kpi-pack.json",
        "cavra-aispm-soc2-audit-summary.md",
    ]:
        if filename not in board_artifacts:
            failures.append(f"{BOARD_INDEX_JSON}: missing artifact {filename}")

    scripts = package.get("scripts", {})
    if scripts.get("validate:sandbox:visual") != "node scripts/validate-sandbox-visual.mjs":
        failures.append("package.json: validate:sandbox:visual script must run scripts/validate-sandbox-visual.mjs")
    if scripts.get("validate:sandbox:hosted") != "node scripts/validate-hosted-sandbox-pages.mjs":
        failures.append("package.json: validate:sandbox:hosted script must run scripts/validate-hosted-sandbox-pages.mjs")

    visual_md = read(VISUAL_MD)
    board_md = read(BOARD_INDEX_MD)
    for screenshot in REQUIRED_SCREENSHOTS:
        require(visual_md, Path(screenshot).name, "visual smoke Markdown screenshot list", failures)
    for needle in [
        "npm run validate:sandbox:visual",
        "scripts/validate-sandbox-visual.mjs",
        "Pilot Launch Board Pack Packet",
        "CSO Report Center",
        ".cavra/visual-smoke/",
    ]:
        require(visual_md, needle, "visual smoke Markdown", failures)
        require(board_md, needle, "board-pack artifact Markdown", failures)

    for doc_path in REQUIRED_DOCS:
        text = read(doc_path)
        for needle in [
            "npm run validate:sandbox:visual",
            "scripts/validate-sandbox-visual.mjs",
        ]:
            require(text, needle, f"{doc_path} visual freshness reference", failures)
        if "Home.md" not in doc_path:
            require(text, "aispm-visual-smoke-validation", f"{doc_path} visual verification reference", failures)

    for workflow_path in REQUIRED_WORKFLOWS:
        text = read(workflow_path)
        for needle in [
            "actions/setup-node@v6",
            'node-version: "24"',
            "npm ci",
            "npx playwright install --with-deps chromium",
            "npm run validate:sandbox:visual",
            "python scripts/validate-aispm-visual-freshness.py",
        ]:
            require(text, needle, f"{workflow_path} visual freshness enforcement", failures)
        if str(workflow_path) == ".github/workflows/deploy-sandbox.yml":
            for needle in [
                "npm run validate:sandbox:hosted",
                "scripts/validate-hosted-sandbox-pages.mjs",
            ]:
                require(text, needle, f"{workflow_path} hosted Pages smoke enforcement", failures)

    sandbox_validator = read("scripts/validate-sandbox-portal.py")
    launch_validator = read("scripts/validate-aispm-launch-artifacts.py")
    for text, label in [(sandbox_validator, "sandbox portal validator"), (launch_validator, "launch artifact validator")]:
        require(text, "npm run validate:sandbox:visual", label, failures)
    require(sandbox_validator, "npm run validate:sandbox:hosted", "sandbox portal validator hosted smoke", failures)
    require(launch_validator, "docs/release-verifications/aispm-visual-smoke-validation.json", "launch artifact validator visual record", failures)

    forbidden_terms = [
        "private_customer_screenshot_payload",
        "tenant_visual_baseline_payload",
        "signed_visual_regression_secret",
    ]
    combined = "\n".join(
        [visual_md, board_md]
        + [read(path) for path in REQUIRED_DOCS]
        + [read(path) for path in REQUIRED_WORKFLOWS]
    )
    for term in forbidden_terms:
        if term in combined:
            failures.append(f"public visual freshness docs must not expose {term}")

    if failures:
        print("AISPM visual freshness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM visual freshness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
