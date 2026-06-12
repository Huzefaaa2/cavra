#!/usr/bin/env python3
"""Validate the public-safe hosted sandbox operator release status."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs/release-verifications/hosted-sandbox-operator-release-status.json"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(read(path))


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
        "docs/release-verifications/hosted-sandbox-operator-release-status.json",
        "docs/release-verifications/hosted-sandbox-operator-release-status.md",
        "docs/release-verifications/hosted-sandbox-deployment-freshness.json",
        "docs/release-verifications/hosted-sandbox-pages-smoke-validation.json",
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/sandbox.js",
        "apps/sandbox-ui/styles.css",
        "scripts/validate-hosted-sandbox-operator-status.py",
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
        "README.md",
        "docs/sandbox-portal-redesign.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
    ]
    for path in required_files:
        require_file(path, failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    packet = load_json("docs/release-verifications/hosted-sandbox-operator-release-status.json")
    require(
        packet.get("schema_version") == "cavra.hosted_sandbox.operator_release_status.v1",
        f"{PACKET_PATH}: invalid schema_version",
        failures,
    )
    require(packet.get("status") == "ready", f"{PACKET_PATH}: status must be ready", failures)
    require(
        packet.get("portal_packet") == "cavra-hosted-sandbox-operator-status-packet.json",
        f"{PACKET_PATH}: portal packet mismatch",
        failures,
    )
    require(
        packet.get("validator") == "scripts/validate-hosted-sandbox-operator-status.py",
        f"{PACKET_PATH}: validator mismatch",
        failures,
    )
    checks = packet.get("operator_checks", [])
    require(len(checks) == 5, f"{PACKET_PATH}: expected 5 operator checks", failures)
    require(
        {check.get("check_id") for check in checks}
        == {
            "local_portal_freshness",
            "live_pages_freshness",
            "hosted_browser_smoke",
            "post_deploy_evidence",
            "announcement_gate",
        },
        f"{PACKET_PATH}: operator check set mismatch",
        failures,
    )

    html = read("apps/sandbox-ui/index.html")
    js = read("apps/sandbox-ui/sandbox.js")
    css = read("apps/sandbox-ui/styles.css")
    for needle in [
        'id="aispmHostedReleaseStatus"',
        'id="aispmHostedReleaseChecklist"',
        'id="copyAispmHostedReleaseStatusPacket"',
        'id="downloadAispmHostedReleaseStatusPacket"',
        'id="aispmHostedReleaseStatusLine"',
        "Hosted Release Operator Status",
        "cavra-hosted-sandbox-operator-status-packet.json",
    ]:
        require(needle in html, f"portal DOM missing {needle}", failures)
    for needle in [
        "aispmHostedReleaseStatusItems",
        "renderAispmHostedReleaseStatus",
        "currentAispmHostedReleaseStatusPacket",
        "copyAispmHostedReleaseStatusPacket",
        "downloadAispmHostedReleaseStatusPacket",
        "cavra.hosted_sandbox.operator_release_status_packet.v1",
        "blocked_until_live_freshness_passes",
    ]:
        require(needle in js, f"portal JS missing {needle}", failures)
    for needle in [
        ".aispm-hosted-release-panel",
        ".hosted-release-status-grid",
        ".hosted-release-checklist-grid",
        ".hosted-release-check-card",
    ]:
        require(needle in css, f"portal CSS missing {needle}", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require_text(workflow_path, "python scripts/validate-hosted-sandbox-operator-status.py", workflow_path, failures)

    doc_needles = [
        "docs/release-verifications/hosted-sandbox-operator-release-status.md",
        "docs/release-verifications/hosted-sandbox-operator-release-status.json",
        "scripts/validate-hosted-sandbox-operator-status.py",
        "cavra-hosted-sandbox-operator-status-packet.json",
    ]
    for doc_path in [
        "README.md",
        "docs/sandbox-portal-redesign.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
    ]:
        for needle in doc_needles:
            require_text(doc_path, needle, doc_path, failures)

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
            read("docs/release-verifications/hosted-sandbox-operator-release-status.json"),
            read("docs/release-verifications/hosted-sandbox-operator-release-status.md"),
            html,
            js,
        ]
    )
    for term in forbidden:
        require(term not in combined, f"hosted operator status must not expose {term}", failures)

    if failures:
        print("Hosted sandbox operator release status validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Hosted sandbox operator release status validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
