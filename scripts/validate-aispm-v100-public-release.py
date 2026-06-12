#!/usr/bin/env python3
"""Validate CAVRA Community AISPM v1.0 public release readiness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs/release-verifications/aispm-v1.0-public-release-readiness.json"


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
        "docs/release-verifications/aispm-v1.0-public-release-readiness.json",
        "docs/release-verifications/aispm-v1.0-public-release-readiness.md",
        "docs/releases/community-v1.0.0-aispm.md",
        "docs/aispm-v1.0-public-walkthrough.md",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "docs/release-verifications/aispm-launch-readiness-rollup.json",
        "docs/release-verifications/aispm-pilot-control-readiness.json",
        "docs/wiki/AISPM-Enterprise-Trial-Lab-Notebook.md",
        "docs/wiki/assets/aispm-lab/dashboard-desktop-classic.png",
        "docs/wiki/assets/aispm-lab/aispm-desktop-sentinel.png",
        "docs/wiki/assets/aispm-lab/aispm-report-center-panel.png",
        "docs/wiki/assets/aispm-lab/aispm-board-pack-panel.png",
        "docs/wiki/assets/aispm-lab/aispm-trial-flow.svg",
        "README.md",
        "CHANGELOG.md",
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]
    for path in required_files:
        require_file(path, failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    packet = load_json("docs/release-verifications/aispm-v1.0-public-release-readiness.json")
    require(
        packet.get("schema_version") == "cavra.aispm_v100_public_release_readiness.v1",
        f"{PACKET}: invalid schema_version",
        failures,
    )
    require(
        packet.get("status") == "ready_for_pr_and_pages_deploy",
        f"{PACKET}: invalid status",
        failures,
    )
    require(
        packet.get("validator") == "scripts/validate-aispm-v100-public-release.py",
        f"{PACKET}: validator mismatch",
        failures,
    )
    items = packet.get("readiness_items", [])
    require(len(items) == 5, f"{PACKET}: expected five readiness items", failures)
    require(
        {item.get("item_id") for item in items}
        == {
            "package_current_work",
            "github_pages_deploy",
            "release_notes_walkthrough",
            "lab_notebook_assets",
            "final_release_verification",
        },
        f"{PACKET}: readiness item set mismatch",
        failures,
    )
    for artifact in packet.get("required_artifacts", []):
        require_file(artifact, failures)

    for doc_path in [
        "README.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
    ]:
        for needle in [
            "docs/releases/community-v1.0.0-aispm.md",
            "docs/aispm-v1.0-public-walkthrough.md",
            "docs/release-verifications/aispm-v1.0-public-release-readiness.md",
            "docs/release-verifications/aispm-v1.0-public-release-readiness.json",
            "scripts/validate-aispm-v100-public-release.py",
        ]:
            require_text(doc_path, needle, doc_path, failures)

    lab = read("docs/wiki/AISPM-Enterprise-Trial-Lab-Notebook.md")
    for needle in [
        "assets/aispm-lab/dashboard-desktop-classic.png",
        "assets/aispm-lab/aispm-desktop-sentinel.png",
        "assets/aispm-lab/aispm-report-center-panel.png",
        "assets/aispm-lab/aispm-board-pack-panel.png",
        "assets/aispm-lab/aispm-trial-flow.svg",
        "## Step-By-Step Lab",
    ]:
        require(needle in lab, f"lab notebook missing {needle}", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require_text(
            workflow_path,
            "python scripts/validate-aispm-v100-public-release.py",
            workflow_path,
            failures,
        )

    release_notes = read("docs/releases/community-v1.0.0-aispm.md")
    for needle in [
        "CAVRA Community AISPM v1.0",
        "https://huzefaaa2.github.io/cavra/#ai-posture",
        "docs/aispm-v1.0-public-walkthrough.md",
        "docs/release-verifications/aispm-v1.0-public-release-readiness.json",
        "Boundary Notice",
    ]:
        require(needle in release_notes, f"release notes missing {needle}", failures)

    forbidden = [
        "license_key=",
        '"license_key":',
        "private_package_token=",
        '"private_package_token":',
        "customer_identity_payload",
        "raw_prompt_payload",
        "model_reasoning_payload",
        "tenant_telemetry_payload",
        "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
    ]
    combined = "\n".join(
        [
            read("docs/release-verifications/aispm-v1.0-public-release-readiness.json"),
            read("docs/release-verifications/aispm-v1.0-public-release-readiness.md"),
            read("docs/releases/community-v1.0.0-aispm.md"),
            read("docs/aispm-v1.0-public-walkthrough.md"),
            lab,
        ]
    )
    for term in forbidden:
        require(term not in combined, f"AISPM public release readiness must not expose {term}", failures)

    if failures:
        print("AISPM v1.0 public release readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM v1.0 public release readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
