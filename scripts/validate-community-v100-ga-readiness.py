#!/usr/bin/env python3
"""Validate Community v1.0.0 GA readiness evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DOC_PATH = Path("docs/community-v1.0.0-ga-readiness.md")
WIKI_DOC_PATH = Path("docs/wiki/Community-v1.0.0-GA-Readiness.md")
PACKET_PATH = Path("docs/release-verifications/community-v1.0.0-ga-readiness.json")
README_PATH = Path("README.md")
WIKI_HOME_PATH = Path("docs/wiki/Home.md")
ROADMAP_PATH = Path("docs/production-roadmap.md")
INVENTORY_PATH = Path("docs/current-feature-inventory.md")
CHANGELOG_PATH = Path("CHANGELOG.md")
RELEASE_NOTES_PATH = Path("docs/releases/community-v1.0.0-rc.1.md")
WIKI_RELEASE_NOTES_PATH = Path("docs/wiki/Community-v1.0.0-rc.1-Release-Notes.md")
RELEASE_INDEX_PATH = Path("docs/community-release-index.md")
DASHBOARD_PATH = Path("docs/community-release-readiness-dashboard.md")
WIKI_INDEX_PATH = Path("docs/wiki/Community-Release-Index.md")
WIKI_DASHBOARD_PATH = Path("docs/wiki/Community-Release-Readiness-Dashboard.md")

SCRIPT_REF = "scripts/validate-community-v100-ga-readiness.py"
NEXT_RECOMMENDATION = (
    "Prepare Community v1.0.0 GA publication package from validated RC1 feedback "
    "and the completed Node 24 readiness baseline by drafting final release notes, "
    "v1.0.0 artifact build plan, verifier inputs, and announcement approval evidence."
)

REQUIRED_WORKFLOWS = {
    ".github/workflows/community-ci.yml",
    ".github/workflows/security-scan.yml",
    ".github/workflows/release-community.yml",
    ".github/workflows/cavra-governance.yml",
}

REQUIRED_TERMS = {
    "Community v1.0.0 GA Readiness",
    "community-v1.0.0",
    "1.0.0",
    "RC1 feedback baseline",
    "Node 24 readiness baseline",
    "Upgrade notes",
    "Installer paths",
    "Announcement copy",
    "Final GA evidence gates",
    "python3 -m pip install cavra-1.0.0-py3-none-any.whl",
    "python3 -m pip install cavra-1.0.0.tar.gz",
    "docker build -f docker/Dockerfile.community .",
    ".github/workflows/verify-community-release.yml",
    "cavra 1.0.0",
    "SHA-256",
    "provenance",
    "Detached signatures",
    "keyless attestation",
    "Public boundary",
    "Enterprise source code",
    "paid policy packs",
    "private signing keys",
    "private registry credentials",
    "customer records",
    SCRIPT_REF,
}


def read(root: Path, path: Path) -> str:
    return (root / path).read_text(encoding="utf-8")


def require_path(root: Path, path: Path, failures: list[str]) -> None:
    if not (root / path).is_file():
        failures.append(f"missing required file: {path}")


def require(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"missing {label}: {needle}")


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    required_paths = [
        DOC_PATH,
        WIKI_DOC_PATH,
        PACKET_PATH,
        README_PATH,
        WIKI_HOME_PATH,
        ROADMAP_PATH,
        INVENTORY_PATH,
        CHANGELOG_PATH,
        RELEASE_NOTES_PATH,
        WIKI_RELEASE_NOTES_PATH,
        RELEASE_INDEX_PATH,
        DASHBOARD_PATH,
        WIKI_INDEX_PATH,
        WIKI_DASHBOARD_PATH,
    ]
    required_paths.extend(Path(path) for path in REQUIRED_WORKFLOWS)
    for path in required_paths:
        require_path(root, path, failures)
    if failures:
        return failures

    doc = read(root, DOC_PATH)
    wiki_doc = read(root, WIKI_DOC_PATH)
    readme = read(root, README_PATH)
    wiki_home = read(root, WIKI_HOME_PATH)
    roadmap = read(root, ROADMAP_PATH)
    inventory = read(root, INVENTORY_PATH)
    changelog = read(root, CHANGELOG_PATH)
    release_notes = read(root, RELEASE_NOTES_PATH)
    wiki_release_notes = read(root, WIKI_RELEASE_NOTES_PATH)
    release_index = read(root, RELEASE_INDEX_PATH)
    dashboard = read(root, DASHBOARD_PATH)
    wiki_index = read(root, WIKI_INDEX_PATH)
    wiki_dashboard = read(root, WIKI_DASHBOARD_PATH)

    try:
        packet = json.loads(read(root, PACKET_PATH))
    except json.JSONDecodeError as exc:
        return [f"{PACKET_PATH}: invalid JSON: {exc}"]

    for document_name, document in (
        (str(DOC_PATH), doc),
        (str(WIKI_DOC_PATH), wiki_doc),
    ):
        for term in REQUIRED_TERMS:
            require(document, term, f"{document_name} term", failures)

    for public_path in (str(DOC_PATH), str(PACKET_PATH)):
        require(readme, public_path, "README GA readiness link", failures)
    require(wiki_home, WIKI_DOC_PATH.name, "wiki GA readiness link", failures)

    for document_name, document in (
        (str(ROADMAP_PATH), roadmap),
        (str(INVENTORY_PATH), inventory),
        (str(CHANGELOG_PATH), changelog),
    ):
        require(document, "Community v1.0.0 GA readiness", document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)
        require(document, str(PACKET_PATH), document_name, failures)

    for document_name, document in (
        (str(RELEASE_NOTES_PATH), release_notes),
        (str(WIKI_RELEASE_NOTES_PATH), wiki_release_notes),
    ):
        require(document, "Community v1.0.0 RC1", document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)

    for document_name, document in (
        (str(RELEASE_INDEX_PATH), release_index),
        (str(DASHBOARD_PATH), dashboard),
        (str(WIKI_INDEX_PATH), wiki_index),
        (str(WIKI_DASHBOARD_PATH), wiki_dashboard),
    ):
        require(document, "Community v1.0.0 RC1", document_name, failures)
        require(document, "Published", document_name, failures)

    expected_scalars = {
        "schema_version": "cavra.community_v100_ga_readiness.v1",
        "status": "ready_for_ga_publication_package",
        "release": "CAVRA Community v1.0.0",
        "target_tag": "community-v1.0.0",
        "target_version": "1.0.0",
        "baseline_release_candidate": "community-v1.0.0-rc.1",
        "baseline_evidence": "docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md",
        "public_plan": str(DOC_PATH),
        "wiki_plan": str(WIKI_DOC_PATH),
        "next_recommendation": NEXT_RECOMMENDATION,
    }
    for key, value in expected_scalars.items():
        if packet.get(key) != value:
            failures.append(f"{PACKET_PATH}: {key} must be {value!r}")

    upgrade_notes = packet.get("upgrade_notes", {})
    for key in ("from_0_1_3", "from_1_0_0rc1", "enterprise_boundary"):
        if not upgrade_notes.get(key):
            failures.append(f"{PACKET_PATH}: missing upgrade note {key}")

    installer_paths = {
        item.get("name"): item
        for item in packet.get("installer_paths", [])
        if isinstance(item, dict) and item.get("name")
    }
    for name in (
        "python_wheel",
        "source_distribution",
        "github_release_download",
        "community_docker_image",
        "github_actions_verifier",
        "source_checkout",
    ):
        if name not in installer_paths:
            failures.append(f"{PACKET_PATH}: missing installer path {name}")

    required_gates = {
        "final_tag",
        "package_version",
        "artifact_checksums",
        "provenance_metadata",
        "signatures_or_attestations",
        "clean_install_smoke",
        "release_notes_freshness",
        "dashboard_freshness",
        "public_boundary",
        "announcement_approval",
    }
    gates = set(packet.get("final_ga_evidence_gates", []))
    missing_gates = sorted(required_gates - gates)
    if missing_gates:
        failures.append(f"{PACKET_PATH}: missing final GA gates: {', '.join(missing_gates)}")

    if packet.get("announcement_copy_status") != "ready_for_maintainer_approval":
        failures.append(f"{PACKET_PATH}: announcement copy must be ready for approval")
    if packet.get("decision", {}).get("status") != "approve_ga_publication_package_preparation":
        failures.append(f"{PACKET_PATH}: decision must approve GA publication package preparation")

    boundary_terms = set(packet.get("must_never_include", []))
    for term in (
        "Enterprise source code",
        "paid policy packs",
        "private signing keys",
        "license-service secrets",
        "private registry credentials",
        "customer records",
    ):
        if term not in boundary_terms:
            failures.append(f"{PACKET_PATH}: missing boundary term {term}")

    for workflow_path in REQUIRED_WORKFLOWS:
        workflow = read(root, Path(workflow_path))
        require(workflow, SCRIPT_REF, f"{workflow_path} GA readiness validator", failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    args = parser.parse_args()

    failures = validate(args.root.resolve())
    if failures:
        print("CAVRA Community v1.0.0 GA readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA Community v1.0.0 GA readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
