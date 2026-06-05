#!/usr/bin/env python3
"""Validate Community v1.0.0 RC1 post-publication evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DOC_PATH = Path(
    "docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md"
)
WIKI_DOC_PATH = Path(
    "docs/wiki/Community-v1.0.0-rc.1-Post-Publication-Verification.md"
)
PACKET_PATH = Path(
    "docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.json"
)
RELEASE_NOTES_PATH = Path("docs/releases/community-v1.0.0-rc.1.md")
WIKI_RELEASE_NOTES_PATH = Path("docs/wiki/Community-v1.0.0-rc.1-Release-Notes.md")
README_PATH = Path("README.md")
WIKI_HOME_PATH = Path("docs/wiki/Home.md")
RELEASE_INDEX_PATH = Path("docs/community-release-index.md")
DASHBOARD_PATH = Path("docs/community-release-readiness-dashboard.md")
WIKI_INDEX_PATH = Path("docs/wiki/Community-Release-Index.md")
WIKI_DASHBOARD_PATH = Path("docs/wiki/Community-Release-Readiness-Dashboard.md")
ROADMAP_PATH = Path("docs/production-roadmap.md")
INVENTORY_PATH = Path("docs/current-feature-inventory.md")
CHANGELOG_PATH = Path("CHANGELOG.md")

SCRIPT_REF = "scripts/validate-community-v100-rc-post-publication.py"
RELEASE_URL = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1"
NEXT_RECOMMENDATION = (
    "Advance Community v1.0.0 RC1 feedback from the completed Node 24 readiness "
    "baseline into GA release readiness by validating upgrade notes, installer "
    "paths, announcement copy, and final GA evidence gates."
)
WHEEL_SHA = "6d06bd04965d3b1340ecacf007bc39111c8a8d5d0a73ee32f44aeb06ebb1be01"
SDIST_SHA = "f4312e51a4d4180387982eafa86f301c584be5af147ba09098d733d187662e0c"
CHECKSUM_SHA = "73a4f20e42ea4823a8087bfb9d703bf224cd8e9128ed5590a9eaad047a8ea166"
PROVENANCE_SHA = "fdb69a24e6f76a737e225b2d259c8842a08172cd929fdf3f5e41020ad5d32217"

REQUIRED_WORKFLOWS = {
    ".github/workflows/community-ci.yml",
    ".github/workflows/security-scan.yml",
    ".github/workflows/release-community.yml",
    ".github/workflows/cavra-governance.yml",
}

REQUIRED_TERMS = {
    "Community v1.0.0 RC1",
    "community-v1.0.0-rc.1",
    "1.0.0rc1",
    RELEASE_URL,
    "e04ba0025f00b13bf05ab468669bcb3fb494eb89",
    "2026-06-05T05:49:28Z",
    WHEEL_SHA,
    SDIST_SHA,
    CHECKSUM_SHA,
    PROVENANCE_SHA,
    "cavra 1.0.0rc1",
    "Node 24 readiness baseline",
    "post-publication verification",
    "SHA-256",
    "provenance",
    "detached signature",
    "keyless attestation",
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
        require(document, "Community v1.0.0 RC1", document_name, failures)
        require(document, "Published", document_name, failures)
        require(document, RELEASE_URL, document_name, failures)
        require(document, str(RELEASE_NOTES_PATH), document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)

    for document_name, document in (
        (str(ROADMAP_PATH), roadmap),
        (str(INVENTORY_PATH), inventory),
        (str(CHANGELOG_PATH), changelog),
    ):
        require(document, "Community v1.0.0 RC1 post-publication verification", document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)

    expected_scalars = {
        "schema_version": "cavra.community_v100_rc_post_publication.v1",
        "status": "published",
        "release": "CAVRA Community v1.0.0 RC1",
        "tag": "community-v1.0.0-rc.1",
        "version": "1.0.0rc1",
        "release_url": RELEASE_URL,
        "verification_date": "2026-06-05",
        "published_at": "2026-06-05T05:49:28Z",
        "release_target": "e04ba0025f00b13bf05ab468669bcb3fb494eb89",
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
        "cavra-1.0.0rc1-py3-none-any.whl": WHEEL_SHA,
        "cavra-1.0.0rc1.tar.gz": SDIST_SHA,
        "cavra-1.0.0rc1-SHA256SUMS.txt": CHECKSUM_SHA,
        "cavra-1.0.0rc1.provenance.json": PROVENANCE_SHA,
    }
    if artifact_hashes != expected_artifacts:
        failures.append(f"{PACKET_PATH}: artifact checksums do not match RC1 release")

    for artifact in packet.get("artifacts", []):
        if not artifact.get("downloadable") or not artifact.get("checksum_match"):
            failures.append(f"{PACKET_PATH}: artifact {artifact.get('name')} is not verified")

    if packet.get("install_smoke", {}).get("output") != "cavra 1.0.0rc1":
        failures.append(f"{PACKET_PATH}: install smoke output must be cavra 1.0.0rc1")
    if packet.get("node24_readiness_baseline") != "pass":
        failures.append(f"{PACKET_PATH}: Node 24 readiness baseline must pass")

    signature_evidence = packet.get("signature_evidence", {})
    if not signature_evidence.get("checksum_file_recorded"):
        failures.append(f"{PACKET_PATH}: checksum file must be recorded")
    if not signature_evidence.get("provenance_file_recorded"):
        failures.append(f"{PACKET_PATH}: provenance file must be recorded")
    if signature_evidence.get("detached_signature_attached") is not False:
        failures.append(f"{PACKET_PATH}: detached signature status must be explicit")
    if signature_evidence.get("keyless_attestation_attached") is not False:
        failures.append(f"{PACKET_PATH}: keyless attestation status must be explicit")

    workflow_urls = {
        item.get("url")
        for item in packet.get("workflow_evidence", [])
        if isinstance(item, dict)
    }
    for url in (
        "https://github.com/Huzefaaa2/cavra/actions/runs/26997968188",
        "https://github.com/Huzefaaa2/cavra/actions/runs/26997968186",
        "https://github.com/Huzefaaa2/cavra/actions/runs/26997989076",
    ):
        if url not in workflow_urls:
            failures.append(f"{PACKET_PATH}: missing workflow evidence {url}")

    public_boundary = packet.get("public_boundary", {})
    for key in (
        "community_artifacts_only",
        "enterprise_source_included",
        "paid_policy_packs_included",
        "private_signing_keys_included",
        "private_registry_credentials_included",
        "customer_records_included",
    ):
        if key not in public_boundary:
            failures.append(f"{PACKET_PATH}: missing public boundary key {key}")
    if public_boundary.get("community_artifacts_only") is not True:
        failures.append(f"{PACKET_PATH}: community_artifacts_only must be true")
    for key in (
        "enterprise_source_included",
        "paid_policy_packs_included",
        "private_signing_keys_included",
        "private_registry_credentials_included",
        "customer_records_included",
    ):
        if public_boundary.get(key) is not False:
            failures.append(f"{PACKET_PATH}: {key} must be false")

    for workflow_path in REQUIRED_WORKFLOWS:
        workflow = read(root, Path(workflow_path))
        require(workflow, SCRIPT_REF, f"{workflow_path} post-publication validator", failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    args = parser.parse_args()

    failures = validate(args.root.resolve())
    if failures:
        print("CAVRA Community v1.0.0 RC1 post-publication validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA Community v1.0.0 RC1 post-publication validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
