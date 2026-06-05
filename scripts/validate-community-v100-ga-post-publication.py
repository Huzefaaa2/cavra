#!/usr/bin/env python3
"""Validate Community v1.0.0 GA post-publication evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DOC_PATH = Path("docs/release-verifications/community-v1.0.0-post-publication-verification.md")
WIKI_DOC_PATH = Path("docs/wiki/Community-v1.0.0-Post-Publication-Verification.md")
PACKET_PATH = Path("docs/release-verifications/community-v1.0.0-post-publication-verification.json")
RELEASE_NOTES_PATH = Path("docs/releases/community-v1.0.0.md")
WIKI_RELEASE_NOTES_PATH = Path("docs/wiki/Community-v1.0.0-Release-Notes.md")
README_PATH = Path("README.md")
WIKI_HOME_PATH = Path("docs/wiki/Home.md")
RELEASE_INDEX_PATH = Path("docs/community-release-index.md")
DASHBOARD_PATH = Path("docs/community-release-readiness-dashboard.md")
WIKI_INDEX_PATH = Path("docs/wiki/Community-Release-Index.md")
WIKI_DASHBOARD_PATH = Path("docs/wiki/Community-Release-Readiness-Dashboard.md")
ROADMAP_PATH = Path("docs/production-roadmap.md")
INVENTORY_PATH = Path("docs/current-feature-inventory.md")
CHANGELOG_PATH = Path("CHANGELOG.md")
VERIFY_WORKFLOW_PATH = Path(".github/workflows/verify-community-release.yml")

SCRIPT_REF = "scripts/validate-community-v100-ga-post-publication.py"
RELEASE_URL = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0"
NEXT_RECOMMENDATION = (
    "Use Community v1.0.0 as the stable public baseline and begin the v1.0.1 "
    "maintenance planning path for post-GA fixes, release integrity hardening, "
    "detached signing or keyless attestation, and adoption feedback."
)
RELEASE_TARGET = "bb5dd1005e9c2efb6e7e4df40ad153751476a6d2"
PUBLISHED_AT = "2026-06-05T07:30:35Z"
WHEEL_SHA = "464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914"
SDIST_SHA = "851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331"
CHECKSUM_SHA = "c9049c68d23e089f2129ab3f1f130f7a8e07aecc4bb1e8b4b5360b22a5c617fd"
PROVENANCE_SHA = "38b6e2127695050e697d33dde22f111eaee5cccbcf598cb82fc60c6a795c99aa"

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
    RELEASE_TARGET,
    PUBLISHED_AT,
    WHEEL_SHA,
    SDIST_SHA,
    CHECKSUM_SHA,
    PROVENANCE_SHA,
    "cavra 1.0.0",
    "post-publication verification",
    "SHA-256",
    "provenance",
    "detached signature",
    "keyless attestation",
    "Community Docker build",
    "Enterprise source code",
    "paid policy packs",
    "private signing keys",
    "private registry credentials",
    "customer records",
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
        RELEASE_NOTES_PATH,
        WIKI_RELEASE_NOTES_PATH,
        README_PATH,
        WIKI_HOME_PATH,
        RELEASE_INDEX_PATH,
        DASHBOARD_PATH,
        WIKI_INDEX_PATH,
        WIKI_DASHBOARD_PATH,
        ROADMAP_PATH,
        INVENTORY_PATH,
        CHANGELOG_PATH,
        VERIFY_WORKFLOW_PATH,
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
    readme = read(root, README_PATH)
    wiki_home = read(root, WIKI_HOME_PATH)
    release_index = read(root, RELEASE_INDEX_PATH)
    dashboard = read(root, DASHBOARD_PATH)
    wiki_index = read(root, WIKI_INDEX_PATH)
    wiki_dashboard = read(root, WIKI_DASHBOARD_PATH)
    roadmap = read(root, ROADMAP_PATH)
    inventory = read(root, INVENTORY_PATH)
    changelog = read(root, CHANGELOG_PATH)
    verify_workflow = read(root, VERIFY_WORKFLOW_PATH)

    try:
        packet = json.loads(read(root, PACKET_PATH))
    except json.JSONDecodeError as exc:
        return [f"{PACKET_PATH}: invalid JSON: {exc}"]

    for document_name, document in (
        (str(DOC_PATH), doc),
        (str(WIKI_DOC_PATH), wiki_doc),
        (str(RELEASE_NOTES_PATH), release_notes),
        (str(WIKI_RELEASE_NOTES_PATH), wiki_release_notes),
    ):
        for term in REQUIRED_TERMS:
            require(document, term, f"{document_name} term", failures)
        require(document, NEXT_RECOMMENDATION, f"{document_name} next recommendation", failures)

    for public_path in (
        str(RELEASE_NOTES_PATH),
        str(DOC_PATH),
        str(PACKET_PATH),
        str(RELEASE_INDEX_PATH),
        str(DASHBOARD_PATH),
    ):
        require(readme, public_path, "README post-publication link", failures)

    for wiki_link in (
        WIKI_DOC_PATH.name,
        WIKI_RELEASE_NOTES_PATH.name,
        WIKI_INDEX_PATH.name,
        WIKI_DASHBOARD_PATH.name,
    ):
        require(wiki_home, wiki_link, "wiki post-publication link", failures)

    for document_name, document in (
        (str(RELEASE_INDEX_PATH), release_index),
        (str(DASHBOARD_PATH), dashboard),
        (str(WIKI_INDEX_PATH), wiki_index),
        (str(WIKI_DASHBOARD_PATH), wiki_dashboard),
    ):
        require(document, "| Community v1.0.0 | Published |", document_name, failures)
        require(document, RELEASE_URL, document_name, failures)
        require(document, str(RELEASE_NOTES_PATH), document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)
        require(document, "v1.0.1 maintenance planning", document_name, failures)

    for document_name, document in (
        (str(ROADMAP_PATH), roadmap),
        (str(INVENTORY_PATH), inventory),
        (str(CHANGELOG_PATH), changelog),
    ):
        require(document, "Community v1.0.0 post-publication verification", document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)
        require(document, NEXT_RECOMMENDATION, document_name, failures)

    for value in (WHEEL_SHA, SDIST_SHA):
        require(verify_workflow, value, f"{VERIFY_WORKFLOW_PATH} hash default", failures)

    expected_scalars = {
        "schema_version": "cavra.community_v100_ga_post_publication.v1",
        "status": "published",
        "release": "CAVRA Community v1.0.0",
        "tag": "community-v1.0.0",
        "version": "1.0.0",
        "release_url": RELEASE_URL,
        "verification_date": "2026-06-05",
        "published_at": PUBLISHED_AT,
        "release_target": RELEASE_TARGET,
        "release_notes": str(RELEASE_NOTES_PATH),
        "post_publication_verification": str(DOC_PATH),
        "next_recommendation": NEXT_RECOMMENDATION,
        "decision": "pass",
    }
    for key, value in expected_scalars.items():
        if packet.get(key) != value:
            failures.append(f"{PACKET_PATH}: {key} must be {value!r}")

    artifact_hashes = {
        item.get("name"): item.get("sha256")
        for item in packet.get("artifacts", [])
        if isinstance(item, dict)
    }
    expected_artifacts = {
        "cavra-1.0.0-py3-none-any.whl": WHEEL_SHA,
        "cavra-1.0.0.tar.gz": SDIST_SHA,
        "cavra-1.0.0-SHA256SUMS.txt": CHECKSUM_SHA,
        "cavra-1.0.0.provenance.json": PROVENANCE_SHA,
    }
    if artifact_hashes != expected_artifacts:
        failures.append(f"{PACKET_PATH}: artifact checksums do not match v1.0.0 release")

    for artifact in packet.get("artifacts", []):
        if not artifact.get("downloadable") or not artifact.get("checksum_match"):
            failures.append(f"{PACKET_PATH}: artifact {artifact.get('name')} is not verified")

    if packet.get("install_smoke", {}).get("output") != "cavra 1.0.0":
        failures.append(f"{PACKET_PATH}: install smoke output must be cavra 1.0.0")
    if packet.get("docker_build", {}).get("status") != "pass":
        failures.append(f"{PACKET_PATH}: Docker build status must pass")
    if packet.get("node24_readiness_baseline") != "pass":
        failures.append(f"{PACKET_PATH}: Node 24 readiness baseline must pass")

    public_boundary = packet.get("public_boundary", {})
    for key in (
        "enterprise_source_included",
        "paid_policy_packs_included",
        "private_signing_keys_included",
        "private_registry_credentials_included",
        "customer_records_included",
    ):
        if public_boundary.get(key) is not False:
            failures.append(f"{PACKET_PATH}: public_boundary.{key} must be false")

    signature = packet.get("signature_evidence", {})
    expected_signature = {
        "checksum_file_recorded": True,
        "provenance_file_recorded": True,
        "detached_signature_attached": False,
        "keyless_attestation_attached": False,
        "follow_up_required": True,
    }
    for key, value in expected_signature.items():
        if signature.get(key) is not value:
            failures.append(f"{PACKET_PATH}: signature_evidence.{key} must be {value!r}")

    workflow_defaults = packet.get("workflow_defaults", {})
    expected_defaults = {
        "tag": "community-v1.0.0",
        "version": "1.0.0",
        "wheel_sha256": WHEEL_SHA,
        "sdist_sha256": SDIST_SHA,
    }
    if workflow_defaults != expected_defaults:
        failures.append(f"{PACKET_PATH}: workflow defaults do not match final hashes")

    for workflow_path in REQUIRED_WORKFLOWS:
        workflow = read(root, Path(workflow_path))
        require(workflow, f"python {SCRIPT_REF}", workflow_path, failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to validate.")
    args = parser.parse_args()
    failures = validate(Path(args.root))
    if failures:
        print("CAVRA Community v1.0.0 GA post-publication validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("CAVRA Community v1.0.0 GA post-publication validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
