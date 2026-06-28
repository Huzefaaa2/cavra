#!/usr/bin/env python3
"""Validate public-safe hosted sandbox deployment freshness markers."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs/release-verifications/hosted-sandbox-deployment-freshness.json"
CURRENT_BUILD_SENTINEL = "community-v1.1.0-public-product-site"
LEGACY_BUILD_SENTINEL = "community-v1.0.0-aispm-release-evidence-index"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(read(path))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_file(path: str, failures: list[str]) -> None:
    require((ROOT / path).is_file(), f"missing required file: {path}", failures)


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "cavra-hosted-freshness-validator"})
    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def main() -> int:
    failures: list[str] = []
    required_files = [
        "docs/release-verifications/hosted-sandbox-deployment-freshness.json",
        "docs/release-verifications/hosted-sandbox-deployment-freshness.md",
        "apps/sandbox-ui/index.html",
        "scripts/validate-hosted-sandbox-deployment-freshness.py",
        "scripts/validate-hosted-sandbox-pages.mjs",
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

    packet = load_json("docs/release-verifications/hosted-sandbox-deployment-freshness.json")
    require(
        packet.get("schema_version") == "cavra.hosted_sandbox.deployment_freshness.v1",
        f"{PACKET_PATH}: invalid schema_version",
        failures,
    )
    require(packet.get("status") == "ready", f"{PACKET_PATH}: status must be ready", failures)
    require(
        packet.get("validator") == "scripts/validate-hosted-sandbox-deployment-freshness.py",
        f"{PACKET_PATH}: validator mismatch",
        failures,
    )
    require(
        packet.get("build_sentinel") == CURRENT_BUILD_SENTINEL,
        f"{PACKET_PATH}: build sentinel mismatch",
        failures,
    )

    markers = packet.get("required_markers", [])
    require(len(markers) >= 4, f"{PACKET_PATH}: required_markers incomplete", failures)

    index_html = read("apps/sandbox-ui/index.html")
    for marker in markers:
        require(marker in index_html, f"local portal missing marker: {marker}", failures)

    hosted_validator = read("scripts/validate-hosted-sandbox-pages.mjs")
    for marker in markers:
        require(marker in hosted_validator, f"hosted Pages validator missing marker: {marker}", failures)

    workflow_needles = [
        "python scripts/validate-hosted-sandbox-deployment-freshness.py",
        "npm run validate:sandbox:hosted",
        "CAVRA_SANDBOX_URL",
    ]
    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        workflow = read(workflow_path)
        for needle in workflow_needles[:1]:
            require(needle in workflow, f"{workflow_path} missing {needle}", failures)
        if workflow_path == ".github/workflows/deploy-sandbox.yml":
            for needle in workflow_needles:
                require(needle in workflow, f"{workflow_path} missing {needle}", failures)

    doc_needles = [
        "docs/release-verifications/hosted-sandbox-deployment-freshness.md",
        "docs/release-verifications/hosted-sandbox-deployment-freshness.json",
        "scripts/validate-hosted-sandbox-deployment-freshness.py",
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
        text = read(doc_path)
        for needle in doc_needles:
            require(needle in text, f"{doc_path} missing {needle}", failures)
        require(
            CURRENT_BUILD_SENTINEL in text or LEGACY_BUILD_SENTINEL in text,
            f"{doc_path} missing hosted freshness build sentinel",
            failures,
        )

    if os.environ.get("CAVRA_CHECK_LIVE_SANDBOX", "").lower() in {"1", "true", "yes"}:
        target = os.environ.get("CAVRA_SANDBOX_URL") or packet["validated_target"]
        try:
            hosted_index = fetch_text(target)
        except (urllib.error.URLError, TimeoutError) as error:
            failures.append(f"live hosted sandbox fetch failed for {target}: {error}")
        else:
            for marker in markers:
                require(marker in hosted_index, f"live hosted sandbox missing marker: {marker}", failures)

    forbidden = [
        "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
        "license_private_key",
        "private_registry_token",
        "customer_identity_payload",
        "raw_prompt_payload",
        "tenant_telemetry_payload",
    ]
    combined = "\n".join(
        [
            read("docs/release-verifications/hosted-sandbox-deployment-freshness.json"),
            read("docs/release-verifications/hosted-sandbox-deployment-freshness.md"),
        ]
    )
    for term in forbidden:
        require(term not in combined, f"hosted freshness packet must not expose {term}", failures)

    if failures:
        print("Hosted sandbox deployment freshness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Hosted sandbox deployment freshness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
