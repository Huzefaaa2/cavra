#!/usr/bin/env python3
"""Validate the public Community v1.0.0 release-candidate hardening packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DOC_PATH = Path("docs/community-v1.0.0-release-candidate-hardening.md")
WIKI_DOC_PATH = Path("docs/wiki/Community-v1.0.0-Release-Candidate-Hardening.md")
PACKET_PATH = Path("docs/release-verifications/community-v1.0.0-release-candidate-hardening.json")
README_PATH = Path("README.md")
WIKI_HOME_PATH = Path("docs/wiki/Home.md")
ROADMAP_PATH = Path("docs/production-roadmap.md")
INVENTORY_PATH = Path("docs/current-feature-inventory.md")
CHANGELOG_PATH = Path("CHANGELOG.md")

NEXT_RECOMMENDATION = (
    "Prepare Community v1.0.0 release-candidate publication from the completed "
    "Node 24 readiness baseline with signed artifact verification, provenance "
    "evidence, release notes, and announcement readiness."
)

REQUIRED_DOC_TERMS = {
    "Community v1.0.0",
    "release-candidate",
    "Node 24 readiness baseline",
    "Signed artifacts",
    "SHA-256",
    "detached signatures",
    "keyless attestation",
    "Reproducible provenance verification",
    "SLSA provenance",
    "SBOM",
    "GA announcement checklist",
    "Final operator evidence",
    "Evidence Console",
    "Public boundary",
    "Enterprise source code",
    "private signing keys",
    "customer records",
    "scripts/validate-community-v100-rc-hardening.py",
    NEXT_RECOMMENDATION,
}

REQUIRED_WORKSTREAMS = {
    "signed_artifacts",
    "reproducible_provenance_verification",
    "ga_announcement_checklist",
    "final_operator_evidence",
}

REQUIRED_GATES = {
    "Node 24 readiness baseline",
    "Signed artifacts",
    "Reproducible provenance verification",
    "GA announcement checklist",
    "Final operator evidence",
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

    try:
        packet = json.loads(read(root, PACKET_PATH))
    except json.JSONDecodeError as exc:
        return [f"{PACKET_PATH}: invalid JSON: {exc}"]

    for document_name, document in (
        (str(DOC_PATH), doc),
        (str(WIKI_DOC_PATH), wiki_doc),
    ):
        for term in REQUIRED_DOC_TERMS:
            require(document, term, f"{document_name} term", failures)

    require(readme, str(DOC_PATH), "README RC hardening link", failures)
    require(readme, str(PACKET_PATH), "README RC hardening packet link", failures)
    require(wiki_home, WIKI_DOC_PATH.name, "wiki RC hardening link", failures)

    for document_name, document in (
        (str(ROADMAP_PATH), roadmap),
        (str(INVENTORY_PATH), inventory),
        (str(CHANGELOG_PATH), changelog),
    ):
        require(document, "Community v1.0.0 release-candidate hardening", document_name, failures)
        require(document, str(DOC_PATH), document_name, failures)
        require(document, NEXT_RECOMMENDATION, f"{document_name} next recommendation", failures)

    if packet.get("schema_version") != "cavra.community_v100_rc_hardening.v1":
        failures.append(f"{PACKET_PATH}: invalid schema_version")
    if packet.get("status") != "ready_for_rc_publication":
        failures.append(f"{PACKET_PATH}: status must be ready_for_rc_publication")
    if packet.get("target_tag") != "community-v1.0.0":
        failures.append(f"{PACKET_PATH}: target_tag must be community-v1.0.0")
    if packet.get("baseline_release") != "community-v0.1.3":
        failures.append(f"{PACKET_PATH}: baseline_release must be community-v0.1.3")
    if packet.get("next_recommendation") != NEXT_RECOMMENDATION:
        failures.append(f"{PACKET_PATH}: next_recommendation does not match")

    workstreams = {
        item.get("name")
        for item in packet.get("required_workstreams", [])
        if isinstance(item, dict)
    }
    missing_workstreams = sorted(REQUIRED_WORKSTREAMS - workstreams)
    if missing_workstreams:
        failures.append(f"{PACKET_PATH}: missing workstreams: {', '.join(missing_workstreams)}")

    gates = {
        item.get("name"): item.get("status")
        for item in packet.get("gates", [])
        if isinstance(item, dict) and item.get("name")
    }
    missing_gates = sorted(REQUIRED_GATES - set(gates))
    if missing_gates:
        failures.append(f"{PACKET_PATH}: missing gates: {', '.join(missing_gates)}")
    if gates.get("Node 24 readiness baseline") != "ready":
        failures.append(f"{PACKET_PATH}: Node 24 readiness baseline must be ready")
    if gates.get("Public boundary") != "ready":
        failures.append(f"{PACKET_PATH}: Public boundary must be ready")

    boundary_terms = set(packet.get("must_never_include", []))
    missing_boundary_terms = sorted(REQUIRED_BOUNDARY_TERMS - boundary_terms)
    if missing_boundary_terms:
        failures.append(f"{PACKET_PATH}: missing boundary terms: {', '.join(missing_boundary_terms)}")

    script_ref = "scripts/validate-community-v100-rc-hardening.py"
    for workflow_path in REQUIRED_WORKFLOWS:
        workflow = read(root, Path(workflow_path))
        require(workflow, script_ref, f"{workflow_path} CI validator", failures)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    args = parser.parse_args()

    failures = validate(args.root.resolve())
    if failures:
        print("CAVRA Community v1.0.0 RC hardening validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA Community v1.0.0 RC hardening validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
