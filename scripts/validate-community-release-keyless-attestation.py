#!/usr/bin/env python3
"""Validate Community release keyless attestation workflow documentation."""

from __future__ import annotations

import argparse
from pathlib import Path


WORKFLOW_PATH = Path(".github/workflows/attest-community-release.yml")
DOC_PATH = Path("docs/community-release-keyless-attestation.md")
WIKI_DOC_PATH = Path("docs/wiki/Community-Release-Keyless-Attestation.md")
README_PATH = Path("README.md")
WIKI_HOME_PATH = Path("docs/wiki/Home.md")
RELEASE_NOTES_PATH = Path("docs/releases/community-v1.0.0.md")
POST_PUBLICATION_PATH = Path(
    "docs/release-verifications/community-v1.0.0-post-publication-verification.md"
)
POST_PUBLICATION_JSON_PATH = Path(
    "docs/release-verifications/community-v1.0.0-post-publication-verification.json"
)

WHEEL_SHA = "464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914"
SDIST_SHA = "851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331"
CHECKSUM_SHA = "c9049c68d23e089f2129ab3f1f130f7a8e07aecc4bb1e8b4b5360b22a5c617fd"
PROVENANCE_SHA = "38b6e2127695050e697d33dde22f111eaee5cccbcf598cb82fc60c6a795c99aa"

WORKFLOW_TERMS = {
    "Attest Community Release",
    ".github/workflows/attest-community-release.yml",
    "actions/attest@v4",
    "id-token: write",
    "attestations: write",
    "artifact-metadata: write",
    "gh attestation verify",
    "community-v1.0.0",
    "1.0.0",
    WHEEL_SHA,
    SDIST_SHA,
    CHECKSUM_SHA,
    PROVENANCE_SHA,
    "deny-self-hosted-runners",
    "community-release-keyless-attestation-evidence.json",
}

DOC_TERMS = {
    *WORKFLOW_TERMS,
    "Huzefaaa2/cavra/.github/workflows/attest-community-release.yml",
    "27003626701",
    "29988580",
    "https://github.com/Huzefaaa2/cavra/attestations/29988580",
    "a06d996927117e59ad012b7b575b386ef9b9d663",
    "https://slsa.dev/provenance/v1",
    "2026-06-05T08:13:01Z",
    "Pass",
    "Enterprise source code",
    "private signing keys",
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
    for path in (
        WORKFLOW_PATH,
        DOC_PATH,
        WIKI_DOC_PATH,
        README_PATH,
        WIKI_HOME_PATH,
        RELEASE_NOTES_PATH,
        POST_PUBLICATION_PATH,
        POST_PUBLICATION_JSON_PATH,
    ):
        require_path(root, path, failures)
    if failures:
        return failures

    workflow = read(root, WORKFLOW_PATH)
    doc = read(root, DOC_PATH)
    wiki_doc = read(root, WIKI_DOC_PATH)
    readme = read(root, README_PATH)
    wiki_home = read(root, WIKI_HOME_PATH)
    release_notes = read(root, RELEASE_NOTES_PATH)
    post_publication = read(root, POST_PUBLICATION_PATH)
    post_publication_json = read(root, POST_PUBLICATION_JSON_PATH)

    for term in WORKFLOW_TERMS:
        require(workflow, term, str(WORKFLOW_PATH), failures)

    for term in DOC_TERMS:
        require(doc, term, str(DOC_PATH), failures)
        require(wiki_doc, term, str(WIKI_DOC_PATH), failures)

    for linked_document in (str(DOC_PATH), str(WIKI_DOC_PATH.name)):
        haystack = readme if linked_document.startswith("docs/") else wiki_home
        require(haystack, linked_document, "navigation", failures)

    for document_name, document in (
        (str(RELEASE_NOTES_PATH), release_notes),
        (str(POST_PUBLICATION_PATH), post_publication),
        (str(POST_PUBLICATION_JSON_PATH), post_publication_json),
    ):
        require(document, "keyless attestation", document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)
        require(document, ".github/workflows/attest-community-release.yml", document_name, failures)
        require(document, "27003626701", document_name, failures)
        require(document, "29988580", document_name, failures)
        require(document, "https://github.com/Huzefaaa2/cavra/attestations/29988580", document_name, failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to validate.")
    args = parser.parse_args()
    failures = validate(Path(args.root))
    if failures:
        print("CAVRA Community release keyless attestation validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("CAVRA Community release keyless attestation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
