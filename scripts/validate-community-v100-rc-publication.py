#!/usr/bin/env python3
"""Validate Community v1.0.0 RC1 publication preparation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DOC_PATH = Path("docs/community-v1.0.0-release-candidate-publication.md")
WIKI_DOC_PATH = Path("docs/wiki/Community-v1.0.0-Release-Candidate-Publication.md")
RELEASE_NOTES_PATH = Path("docs/releases/community-v1.0.0-rc.1.md")
WIKI_RELEASE_NOTES_PATH = Path("docs/wiki/Community-v1.0.0-rc.1-Release-Notes.md")
READINESS_PATH = Path("docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md")
WIKI_READINESS_PATH = Path("docs/wiki/Community-v1.0.0-rc.1-Publication-Verification.md")
PACKET_PATH = Path("docs/release-verifications/community-v1.0.0-release-candidate-publication.json")
README_PATH = Path("README.md")
WIKI_HOME_PATH = Path("docs/wiki/Home.md")
ROADMAP_PATH = Path("docs/production-roadmap.md")
INVENTORY_PATH = Path("docs/current-feature-inventory.md")
CHANGELOG_PATH = Path("CHANGELOG.md")
RELEASE_INDEX_PATH = Path("docs/community-release-index.md")
DASHBOARD_PATH = Path("docs/community-release-readiness-dashboard.md")
WIKI_DASHBOARD_PATH = Path("docs/wiki/Community-Release-Readiness-Dashboard.md")

NEXT_RECOMMENDATION = (
    "Publish Community v1.0.0 release-candidate artifacts from the completed "
    "Node 24 readiness baseline and record signed artifact checksums, provenance, "
    "GitHub Release links, and post-publication verification evidence."
)

RELEASE_URL = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1"
SCRIPT_REF = "scripts/validate-community-v100-rc-publication.py"

REQUIRED_DOC_TERMS = {
    "Community v1.0.0 RC1",
    "community-v1.0.0-rc.1",
    "Node 24 readiness baseline",
    "signed artifact verification",
    "SHA-256",
    "detached signatures",
    "keyless attestation",
    "SBOM",
    "SLSA provenance",
    "announcement-ready",
    "dry-run",
    "Evidence",
    "Public boundary",
    "Enterprise source code",
    "private signing keys",
    "customer records",
    SCRIPT_REF,
    NEXT_RECOMMENDATION,
}

REQUIRED_GATES = {
    "Node 24 readiness baseline",
    "Release notes",
    "Signed artifact verification",
    "Provenance evidence",
    "Announcement readiness",
    "Public boundary",
}

REQUIRED_BOUNDARY_TERMS = {
    "Enterprise source code",
    "paid policy packs",
    "private signing keys",
    "license-service secrets",
    "private registry credentials",
    "private trial packages",
    "customer records",
}

REQUIRED_WORKFLOWS = {
    ".github/workflows/community-ci.yml",
    ".github/workflows/security-scan.yml",
    ".github/workflows/release-community.yml",
    ".github/workflows/cavra-governance.yml",
}

REQUIRED_PUBLIC_LINKS = {
    str(DOC_PATH),
    str(RELEASE_NOTES_PATH),
    str(READINESS_PATH),
    str(PACKET_PATH),
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
        RELEASE_NOTES_PATH,
        WIKI_RELEASE_NOTES_PATH,
        READINESS_PATH,
        WIKI_READINESS_PATH,
        PACKET_PATH,
        README_PATH,
        WIKI_HOME_PATH,
        ROADMAP_PATH,
        INVENTORY_PATH,
        CHANGELOG_PATH,
        RELEASE_INDEX_PATH,
        DASHBOARD_PATH,
        WIKI_DASHBOARD_PATH,
    ]
    required_paths.extend(Path(path) for path in REQUIRED_WORKFLOWS)
    for path in required_paths:
        require_path(root, path, failures)
    if failures:
        return failures

    doc = read(root, DOC_PATH)
    wiki_doc = read(root, WIKI_DOC_PATH)
    release_notes = read(root, RELEASE_NOTES_PATH)
    wiki_release_notes = read(root, WIKI_RELEASE_NOTES_PATH)
    readiness = read(root, READINESS_PATH)
    wiki_readiness = read(root, WIKI_READINESS_PATH)
    readme = read(root, README_PATH)
    wiki_home = read(root, WIKI_HOME_PATH)
    roadmap = read(root, ROADMAP_PATH)
    inventory = read(root, INVENTORY_PATH)
    changelog = read(root, CHANGELOG_PATH)
    release_index = read(root, RELEASE_INDEX_PATH)
    dashboard = read(root, DASHBOARD_PATH)
    wiki_dashboard = read(root, WIKI_DASHBOARD_PATH)

    try:
        packet = json.loads(read(root, PACKET_PATH))
    except json.JSONDecodeError as exc:
        return [f"{PACKET_PATH}: invalid JSON: {exc}"]

    for document_name, document in (
        (str(DOC_PATH), doc),
        (str(WIKI_DOC_PATH), wiki_doc),
        (str(READINESS_PATH), readiness),
        (str(WIKI_READINESS_PATH), wiki_readiness),
    ):
        for term in REQUIRED_DOC_TERMS:
            require(document, term, f"{document_name} term", failures)
        require(document, RELEASE_URL, f"{document_name} release URL", failures)

    for document_name, document in (
        (str(RELEASE_NOTES_PATH), release_notes),
        (str(WIKI_RELEASE_NOTES_PATH), wiki_release_notes),
    ):
        for term in (
            "Community v1.0.0 RC1",
            "community-v1.0.0-rc.1",
            "Node 24 readiness baseline",
            "SHA-256",
            "provenance",
            "Public boundary",
            "Enterprise source code",
            "private signing keys",
            "customer records",
        ):
            require(document, term, f"{document_name} release-note term", failures)
        require(document, RELEASE_URL, f"{document_name} release URL", failures)

    for public_link in REQUIRED_PUBLIC_LINKS:
        require(readme, public_link, "README RC1 publication link", failures)
    for wiki_link in (
        WIKI_DOC_PATH.name,
        WIKI_RELEASE_NOTES_PATH.name,
        WIKI_READINESS_PATH.name,
    ):
        require(wiki_home, wiki_link, "wiki RC1 publication link", failures)

    for document_name, document in (
        (str(ROADMAP_PATH), roadmap),
        (str(INVENTORY_PATH), inventory),
        (str(CHANGELOG_PATH), changelog),
    ):
        require(document, "Community v1.0.0 release-candidate publication", document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)

    for document_name, document in (
        (str(RELEASE_INDEX_PATH), release_index),
        (str(DASHBOARD_PATH), dashboard),
        (str(WIKI_DASHBOARD_PATH), wiki_dashboard),
    ):
        require(document, "Community v1.0.0 RC1", document_name, failures)
        require(document, RELEASE_URL, document_name, failures)
        require(document, str(RELEASE_NOTES_PATH), document_name, failures)

    if packet.get("schema_version") != "cavra.community_v100_rc_publication.v1":
        failures.append(f"{PACKET_PATH}: invalid schema_version")
    if packet.get("status") != "dry_run_publication_ready":
        failures.append(f"{PACKET_PATH}: status must be dry_run_publication_ready")
    if packet.get("tag") != "community-v1.0.0-rc.1":
        failures.append(f"{PACKET_PATH}: tag must be community-v1.0.0-rc.1")
    if packet.get("version") != "1.0.0rc1":
        failures.append(f"{PACKET_PATH}: version must be 1.0.0rc1")
    if packet.get("planned_github_release") != RELEASE_URL:
        failures.append(f"{PACKET_PATH}: planned_github_release does not match")
    if packet.get("release_notes") != str(RELEASE_NOTES_PATH):
        failures.append(f"{PACKET_PATH}: release_notes does not match")
    if packet.get("readiness_verification") != str(READINESS_PATH):
        failures.append(f"{PACKET_PATH}: readiness_verification does not match")
    if packet.get("publication_doc") != str(DOC_PATH):
        failures.append(f"{PACKET_PATH}: publication_doc does not match")
    if packet.get("next_recommendation") != NEXT_RECOMMENDATION:
        failures.append(f"{PACKET_PATH}: next_recommendation does not match")

    gates = {
        item.get("name"): item.get("status")
        for item in packet.get("gates", [])
        if isinstance(item, dict) and item.get("name")
    }
    missing_gates = sorted(REQUIRED_GATES - set(gates))
    if missing_gates:
        failures.append(f"{PACKET_PATH}: missing gates: {', '.join(missing_gates)}")
    if gates.get("Node 24 readiness baseline") != "pass":
        failures.append(f"{PACKET_PATH}: Node 24 readiness baseline must pass")
    if gates.get("Public boundary") != "pass":
        failures.append(f"{PACKET_PATH}: Public boundary must pass")
    if gates.get("Signed artifact verification") != "pending_real_artifacts":
        failures.append(f"{PACKET_PATH}: Signed artifact verification must await real artifacts")
    if gates.get("Provenance evidence") != "pending_real_artifacts":
        failures.append(f"{PACKET_PATH}: Provenance evidence must await real artifacts")

    boundary_terms = set(packet.get("must_never_include", []))
    missing_boundary_terms = sorted(REQUIRED_BOUNDARY_TERMS - boundary_terms)
    if missing_boundary_terms:
        failures.append(f"{PACKET_PATH}: missing boundary terms: {', '.join(missing_boundary_terms)}")

    for workflow_path in REQUIRED_WORKFLOWS:
        workflow = read(root, Path(workflow_path))
        require(workflow, SCRIPT_REF, f"{workflow_path} CI validator", failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    args = parser.parse_args()

    failures = validate(args.root.resolve())
    if failures:
        print("CAVRA Community v1.0.0 RC publication validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA Community v1.0.0 RC publication validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
