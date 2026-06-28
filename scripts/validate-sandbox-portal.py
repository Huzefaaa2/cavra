#!/usr/bin/env python3
"""Validate the public CAVRA GitHub Pages product site contract.

The hosted page is now a public product landing site with routed sections for
Overview, AISPM, Architecture, Trial, Docs, and the public demo. Legacy internal
console readiness panels are intentionally not part of the first-impression
site contract.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_file(path: str, failures: list[str]) -> None:
    require((ROOT / path).is_file(), f"missing required file: {path}", failures)


def require_contains(text: str, needle: str, label: str, failures: list[str]) -> None:
    require(needle in text, f"{label} missing {needle}", failures)


def validate_files(failures: list[str]) -> None:
    for path in [
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/styles.css",
        "apps/sandbox-ui/sandbox.js",
        "apps/sandbox-ui/config.js",
        "apps/sandbox-ui/brand/cavra-mark.svg",
        "scripts/validate-sandbox-portal.py",
        "scripts/validate-hosted-sandbox-pages.mjs",
        "scripts/validate-sandbox-visual.mjs",
        ".github/workflows/deploy-sandbox.yml",
        ".github/workflows/deploy-azure-static-ui.yml",
    ]:
        require_file(path, failures)


def validate_index(html: str, failures: list[str]) -> None:
    for needle in [
        "CAVRA | Runtime Governance for AI Coding Agents",
        "Runtime governance for AI coding agents",
        "Before the agent acts, CAVRA decides.",
        "AI Security Posture Management",
        "Run Public Demo",
        "Explore AISPM",
        "Request Enterprise Trial",
        "https://cavra-trial.mind-ops.cloud/",
        "GitHub Wiki e-book",
        "Trial Field Guide",
        'id="dashboard"',
        'id="ai-posture"',
        'id="architecture"',
        'id="policy-engine"',
        'id="evidence"',
        'id="use-cases"',
        'id="operator-experience"',
        'id="enterprise-trial"',
        'id="integrations"',
        'id="compliance"',
        'id="roadmap"',
        'id="documentation"',
        'id="demoMetrics"',
        'id="communityGaSummary"',
        'id="pilotReadinessSummary"',
        'id="aispmOverviewCards"',
        'id="aispmPilotLaunchBoardPack"',
        'id="aispmPilotLaunchBoardPackManifest"',
        'id="copyAispmPilotLaunchBoardPackPacket"',
        'id="downloadAispmPilotLaunchBoardPackPacket"',
        'id="aispmReportCenter"',
        'id="sendAispmReportEmail"',
        'id="architectureMap"',
        'id="commandPalette"',
        'id="themeSelect"',
        'class="site-footer"',
        "community-v1.1.0-public-product-site",
    ]:
        require_contains(html, needle, "public product portal DOM", failures)

    for forbidden in [
        "SMTP_PASSWORD",
        "CAVRA_AISPM_SMTP_PASSWORD",
        "provider_token",
        "private_key",
        "tenant_secret",
    ]:
        require(forbidden not in html, f"public portal must not expose {forbidden}", failures)


def validate_js(js: str, failures: list[str]) -> None:
    for needle in [
        "const navItems",
        "label: \"Overview\"",
        "label: \"AISPM\"",
        "label: \"Enterprise Trial\"",
        "routeContent",
        "setRoute",
        "history.pushState",
        "hashchange",
        "document.title",
        "applyTheme",
        "renderCommandResults",
        "buildBoardPacket",
        "downloadAispmPilotLaunchBoardPackPacket",
        "sendAispmReportEmail",
        "CAVRA AISPM",
        "Trial Field Guide",
        "copyText",
        "downloadJson",
    ]:
        require_contains(js, needle, "public product portal JS", failures)


def validate_css(css: str, failures: list[str]) -> None:
    for needle in [
        "--brand",
        "body[data-theme=\"classic\"]",
        "body[data-theme=\"retro\"]",
        "body[data-theme=\"executive\"]",
        ".product-hero",
        ".authority-orb",
        ".posture-radar",
        ".runtime-loop",
        ".site-footer",
        ".mobile-bottom",
        ".command-palette",
        "@media (max-width: 900px)",
        "@media (prefers-reduced-motion: reduce)",
    ]:
        require_contains(css, needle, "public product portal CSS", failures)


def validate_workflows(failures: list[str]) -> None:
    deploy = read(".github/workflows/deploy-sandbox.yml")
    azure_static = read(".github/workflows/deploy-azure-static-ui.yml")
    for label, workflow in [
        ("GitHub Pages workflow", deploy),
        ("Azure Static Web Apps workflow", azure_static),
    ]:
        for needle in [
            "node --check apps/sandbox-ui/config.js",
            "node --check apps/sandbox-ui/sandbox.js",
        ]:
            require_contains(workflow, needle, label, failures)

    require_contains(deploy, "python scripts/validate-sandbox-portal.py", "GitHub Pages workflow", failures)
    require_contains(deploy, "npm run validate:sandbox:visual", "GitHub Pages workflow", failures)
    require_contains(azure_static, "python3 scripts/validate-sandbox-portal.py", "Azure Static Web Apps workflow", failures)

    for needle in [
        "npm run validate:sandbox:hosted",
        "scripts/validate-hosted-sandbox-pages.mjs",
        "Runtime governance for AI coding agents",
        "AI Security Posture Management",
        "https://cavra-trial.mind-ops.cloud/",
    ]:
        require_contains(deploy, needle, "GitHub Pages hosted smoke workflow", failures)


def main() -> int:
    failures: list[str] = []
    validate_files(failures)
    html = read("apps/sandbox-ui/index.html")
    js = read("apps/sandbox-ui/sandbox.js")
    css = read("apps/sandbox-ui/styles.css")
    validate_index(html, failures)
    validate_js(js, failures)
    validate_css(css, failures)
    validate_workflows(failures)

    if failures:
      print("CAVRA public product portal validation failed:")
      for failure in failures:
          print(f"- {failure}")
      return 1

    print("CAVRA public product portal validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
