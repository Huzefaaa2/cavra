#!/usr/bin/env python3
"""Validate Community v1.0.0 GA publication package evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DOC_PATH = Path("docs/community-v1.0.0-ga-publication-package.md")
WIKI_DOC_PATH = Path("docs/wiki/Community-v1.0.0-GA-Publication-Package.md")
RELEASE_NOTES_PATH = Path("docs/releases/community-v1.0.0.md")
WIKI_RELEASE_NOTES_PATH = Path("docs/wiki/Community-v1.0.0-Release-Notes.md")
READINESS_PATH = Path("docs/release-verifications/community-v1.0.0-publication-readiness.md")
WIKI_READINESS_PATH = Path("docs/wiki/Community-v1.0.0-Publication-Verification.md")
PACKET_PATH = Path("docs/release-verifications/community-v1.0.0-ga-publication-package.json")
README_PATH = Path("README.md")
WIKI_HOME_PATH = Path("docs/wiki/Home.md")
ROADMAP_PATH = Path("docs/production-roadmap.md")
INVENTORY_PATH = Path("docs/current-feature-inventory.md")
CHANGELOG_PATH = Path("CHANGELOG.md")
RELEASE_INDEX_PATH = Path("docs/community-release-index.md")
DASHBOARD_PATH = Path("docs/community-release-readiness-dashboard.md")
WIKI_INDEX_PATH = Path("docs/wiki/Community-Release-Index.md")
WIKI_DASHBOARD_PATH = Path("docs/wiki/Community-Release-Readiness-Dashboard.md")

SCRIPT_REF = "scripts/validate-community-v100-ga-publication-package.py"
RELEASE_URL = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0"
WHEEL_SHA = "464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914"
SDIST_SHA = "851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331"
NEXT_RECOMMENDATION = (
    "Merge the Community v1.0.0 metadata bump, create the community-v1.0.0 "
    "tag from main, build and upload final GitHub Release assets, then record "
    "final checksums, provenance, verifier defaults, and post-publication "
    "verification."
)

REQUIRED_WORKFLOWS = {
    ".github/workflows/community-ci.yml",
    ".github/workflows/security-scan.yml",
    ".github/workflows/release-community.yml",
    ".github/workflows/cavra-governance.yml",
}

REQUIRED_TERMS = {
    "Community v1.0.0",
    "community-v1.0.0",
    "1.0.0",
    RELEASE_URL,
    "dry-run",
    "SHA-256",
    "provenance",
    "Enterprise source code",
    "paid policy packs",
    "private signing keys",
    "customer records",
    NEXT_RECOMMENDATION,
}

PUBLISHED_RELEASE_TERMS = {
    "Community v1.0.0",
    "community-v1.0.0",
    "1.0.0",
    RELEASE_URL,
    "SHA-256",
    "provenance",
    "Enterprise source code",
    "paid policy packs",
    "private signing keys",
    "customer records",
}

REQUIRED_PACKAGE_TERMS = {
    "Community v1.0.0 GA Publication Package",
    "final release notes",
    "artifact build plan",
    "verifier inputs",
    "announcement approval evidence",
    "Package metadata is bumped",
    "Pre-Publication Build Smoke",
    "cavra-1.0.0-py3-none-any.whl",
    "cavra-1.0.0.tar.gz",
    "cavra-1.0.0-SHA256SUMS.txt",
    "cavra-1.0.0.provenance.json",
    "python3 -m build",
    "python3 scripts/verify-community-release-artifacts.py",
    "cavra 1.0.0",
    "Signature or keyless attestation",
    "Public boundary",
    "private registry credentials",
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
    wiki_index = read(root, WIKI_INDEX_PATH)
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
        for term in REQUIRED_TERMS:
            require(document, term, f"{document_name} term", failures)

    for document_name, document in (
        (str(RELEASE_NOTES_PATH), release_notes),
        (str(WIKI_RELEASE_NOTES_PATH), wiki_release_notes),
    ):
        for term in PUBLISHED_RELEASE_TERMS:
            require(document, term, f"{document_name} term", failures)

    for document_name, document in ((str(DOC_PATH), doc),):
        for term in REQUIRED_PACKAGE_TERMS:
            require(document, term, f"{document_name} package term", failures)

    for public_path in (
        str(DOC_PATH),
        str(RELEASE_NOTES_PATH),
        str(READINESS_PATH),
        str(PACKET_PATH),
    ):
        require(readme, public_path, "README GA publication package link", failures)

    for wiki_link in (
        WIKI_DOC_PATH.name,
        WIKI_RELEASE_NOTES_PATH.name,
        WIKI_READINESS_PATH.name,
    ):
        require(wiki_home, wiki_link, "wiki GA publication package link", failures)

    for document_name, document in (
        (str(ROADMAP_PATH), roadmap),
        (str(INVENTORY_PATH), inventory),
        (str(CHANGELOG_PATH), changelog),
    ):
        require(document, "Community v1.0.0 GA publication package", document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)
        require(document, str(PACKET_PATH), document_name, failures)
        require(document, NEXT_RECOMMENDATION, f"{document_name} next recommendation", failures)

    for document_name, document in (
        (str(RELEASE_INDEX_PATH), release_index),
        (str(DASHBOARD_PATH), dashboard),
        (str(WIKI_INDEX_PATH), wiki_index),
        (str(WIKI_DASHBOARD_PATH), wiki_dashboard),
    ):
        require(document, "Community v1.0.0", document_name, failures)
        require(document, "Published", document_name, failures)
        require(document, RELEASE_URL, document_name, failures)
        require(document, str(RELEASE_NOTES_PATH), document_name, failures)
        require(
            document,
            "docs/release-verifications/community-v1.0.0-post-publication-verification.md",
            document_name,
            failures,
        )

    expected_scalars = {
        "schema_version": "cavra.community_v100_ga_publication_package.v1",
        "status": "dry_run_publication_ready",
        "release": "CAVRA Community v1.0.0",
        "target_tag": "community-v1.0.0",
        "target_version": "1.0.0",
        "baseline_release_candidate": "community-v1.0.0-rc.1",
        "ga_readiness": "docs/community-v1.0.0-ga-readiness.md",
        "publication_doc": str(DOC_PATH),
        "release_notes": str(RELEASE_NOTES_PATH),
        "publication_readiness": str(READINESS_PATH),
        "planned_github_release": RELEASE_URL,
        "next_recommendation": NEXT_RECOMMENDATION,
    }
    for key, value in expected_scalars.items():
        if packet.get(key) != value:
            failures.append(f"{PACKET_PATH}: {key} must be {value!r}")

    artifact_names = {
        item.get("planned_artifact")
        for item in packet.get("artifact_build_plan", [])
        if isinstance(item, dict)
    }
    for artifact in (
        "cavra-1.0.0-py3-none-any.whl",
        "cavra-1.0.0.tar.gz",
        "cavra-1.0.0-SHA256SUMS.txt",
        "cavra-1.0.0.provenance.json",
        "docker/Dockerfile.community",
    ):
        if artifact not in artifact_names:
            failures.append(f"{PACKET_PATH}: missing artifact plan {artifact}")

    verifier_inputs = packet.get("verifier_inputs", {})
    if verifier_inputs.get("tag") != "community-v1.0.0":
        failures.append(f"{PACKET_PATH}: verifier tag must be community-v1.0.0")
    if verifier_inputs.get("version") != "1.0.0":
        failures.append(f"{PACKET_PATH}: verifier version must be 1.0.0")
    if verifier_inputs.get("wheel_sha256") != WHEEL_SHA:
        failures.append(f"{PACKET_PATH}: verifier wheel hash must match final release")
    if verifier_inputs.get("sdist_sha256") != SDIST_SHA:
        failures.append(f"{PACKET_PATH}: verifier sdist hash must match final release")

    metadata_bump = packet.get("metadata_bump", {})
    expected_metadata = {
        "status": "pass",
        "pyproject_version": "1.0.0",
        "runtime_version": "1.0.0",
        "pre_publication_install_smoke": "cavra 1.0.0",
    }
    for key, value in expected_metadata.items():
        if metadata_bump.get(key) != value:
            failures.append(f"{PACKET_PATH}: metadata_bump.{key} must be {value!r}")

    gate_statuses = {
        item.get("name"): item.get("status")
        for item in packet.get("gates", [])
        if isinstance(item, dict) and item.get("name")
    }
    for gate in (
        "RC1 feedback baseline",
        "Node 24 readiness baseline",
        "Final release notes",
        "Artifact build plan",
        "Verifier inputs",
        "Announcement approval evidence",
        "Package metadata",
        "Pre-publication wheel smoke",
        "Artifact checksums",
        "Provenance evidence",
        "Signature or keyless attestation evidence",
        "Clean install smoke",
        "Public boundary",
    ):
        if gate not in gate_statuses:
            failures.append(f"{PACKET_PATH}: missing gate {gate}")
    for gate in (
        "Artifact checksums",
        "Provenance evidence",
        "Signature or keyless attestation evidence",
        "Clean install smoke",
    ):
        if gate_statuses.get(gate) != "pending_final_artifacts":
            failures.append(f"{PACKET_PATH}: {gate} must await final artifacts")
    for gate in ("Package metadata", "Pre-publication wheel smoke"):
        if gate_statuses.get(gate) != "pass":
            failures.append(f"{PACKET_PATH}: {gate} must pass before final artifact publication")
    if packet.get("decision", {}).get("status") != "approve_final_ga_artifact_publication_preparation":
        failures.append(f"{PACKET_PATH}: decision must approve final artifact publication preparation")

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
        require(workflow, SCRIPT_REF, f"{workflow_path} GA publication package validator", failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    args = parser.parse_args()

    failures = validate(args.root.resolve())
    if failures:
        print("CAVRA Community v1.0.0 GA publication package validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA Community v1.0.0 GA publication package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
