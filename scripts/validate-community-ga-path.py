#!/usr/bin/env python3
"""Validate the public user-verifiable Community GA path."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEXT_RECOMMENDATION = (
    "Prepare Community v1.0.0 GA publication package from validated RC1 feedback "
    "and the completed Node 24 readiness baseline by drafting final release notes, "
    "v1.0.0 artifact build plan, verifier inputs, and announcement approval evidence."
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_file(path: str, failures: list[str]) -> None:
    if not (ROOT / path).is_file():
        failures.append(f"missing required file: {path}")


def require(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"missing {label}: {needle}")


def require_phrase(text: str, phrase: str, label: str, failures: list[str]) -> None:
    if " ".join(phrase.lower().split()) not in " ".join(text.lower().split()):
        failures.append(f"missing {label}: {phrase}")


def main() -> int:
    failures: list[str] = []
    required_files = [
        "docs/community-ga-user-verifiable-path.md",
        "docs/wiki/Community-GA-User-Verifiable-Path.md",
        "docs/community-ga-release-checklist.md",
        "docs/community-release-readiness-dashboard.md",
        "docs/release-packets/community-ga-v0.1.0.json",
        "docs/release-verifications/community-v0.1.0-post-release-verification.json",
        "docs/releases/community-v0.1.0.md",
        "scripts/validate-release-packets.py",
        "scripts/validate-sandbox-portal.py",
        "scripts/validate-console-closeout.py",
        "scripts/validate-community-ga-path.py",
    ]
    for path in required_files:
        require_file(path, failures)

    if failures:
        for failure in failures:
            print(failure)
        return 1

    path_doc = read("docs/community-ga-user-verifiable-path.md")
    wiki_path_doc = read("docs/wiki/Community-GA-User-Verifiable-Path.md")
    checklist = read("docs/community-ga-release-checklist.md")
    dashboard = read("docs/community-release-readiness-dashboard.md")
    release_notes = read("docs/releases/community-v0.1.0.md")
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    wiki_home = read("docs/wiki/Home.md")
    roadmap = read("docs/production-roadmap.md")
    next_slice = read("docs/roadmap-status-next-slice.md")
    audit_next_batch = read("docs/roadmap-status-audit-next-batch.md")
    portal_js = read("apps/sandbox-ui/sandbox.js")

    packet = json.loads(read("docs/release-packets/community-ga-v0.1.0.json"))
    verification = json.loads(
        read("docs/release-verifications/community-v0.1.0-post-release-verification.json")
    )

    required_gates = {
        "Public boundary",
        "Policy signing",
        "Policy validation",
        "Runtime modes",
        "Golden decisions",
        "Evidence Console",
        "Deployment validation",
        "Go runtime readiness",
        "Documentation",
        "CI evidence",
    }
    packet_gates = {gate["name"] for gate in packet["gates"]}
    if required_gates != packet_gates:
        failures.append(
            "Community GA packet gates do not match the required user-verifiable gate set."
        )

    if packet["release_state"] != "ready_for_community_ga":
        failures.append("Community GA v0.1.0 packet is not ready_for_community_ga.")
    if packet["public_boundary_review"]["enterprise_code_present"]:
        failures.append("Community GA packet reports Enterprise code in public release.")
    if verification["decision"] != "pass":
        failures.append("Community GA post-release verification did not pass.")
    if not all(artifact["checksum_match"] for artifact in verification["artifacts"]):
        failures.append("Community GA artifact checksum verification is incomplete.")

    for doc in [path_doc, wiki_path_doc]:
        for needle in [
            "Policy",
            "Evidence",
            "Console",
            "Go Runtime",
            "Release Verification",
            "Community GA v0.1.0",
            "community-v0.1.0",
            "scripts/validate-community-ga-path.py",
            "scripts/validate-release-packets.py",
            "scripts/validate-sandbox-portal.py",
            "scripts/validate-console-closeout.py",
            "scripts/validate-boundaries.sh",
            "Public Boundary",
            "Operator Runbook",
            "Validation Command",
        ]:
            require(doc, needle, "Community GA path documentation", failures)
        require_phrase(doc, NEXT_RECOMMENDATION, "Community GA path next recommendation", failures)

    for needle in [
        "policy engine, runtime modes, Evidence Console, deployment validation, and Go",
        "Go runtime readiness",
        "Public Evidence Packet",
    ]:
        require(checklist, needle, "Community GA checklist", failures)

    for needle in [
        "Community GA v0.1.0",
        "Use as the current public Community GA baseline.",
        "scripts/validate-community-ga-path.py",
    ]:
        require(dashboard, needle, "Community readiness dashboard", failures)

    for needle in [
        "Community GA v0.1.0",
        "Post-release verification",
        "Go runtime readiness",
    ]:
        require(release_notes, needle, "Community release notes", failures)

    require(readme, "docs/community-ga-user-verifiable-path.md", "README GA path link", failures)
    require(
        wiki_home,
        "Community-GA-User-Verifiable-Path.md",
        "wiki GA path link",
        failures,
    )
    require(changelog, "user-verifiable Community GA path", "changelog entry", failures)
    require(portal_js, "Community GA Path", "portal docs navigation", failures)

    for doc in [roadmap, next_slice, audit_next_batch]:
        require(
            doc,
            "Community GA user-verifiable path is documented",
            "roadmap delivered GA path statement",
            failures,
        )
        require_phrase(doc, NEXT_RECOMMENDATION, "roadmap next recommendation", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/security-scan.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/cavra-governance.yml",
    ]:
        require(
            read(workflow_path),
            "python scripts/validate-community-ga-path.py",
            f"{workflow_path} validator wiring",
            failures,
        )

    if failures:
        print("CAVRA Community GA path validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA Community GA path validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
