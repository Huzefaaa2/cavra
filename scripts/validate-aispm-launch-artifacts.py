#!/usr/bin/env python3
"""Validate public-safe AISPM launch board pack artifact freshness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "docs/release-verifications/aispm-launch-board-pack-artifact-index.json"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"missing {label}: {needle}")


def require_file(path: str, failures: list[str]) -> None:
    if not (ROOT / path).is_file():
        failures.append(f"missing required file: {path}")


def main() -> int:
    failures: list[str] = []
    require_file("docs/release-verifications/aispm-launch-board-pack-artifact-index.json", failures)
    require_file("docs/release-verifications/aispm-launch-board-pack-artifact-index.md", failures)
    require_file("docs/release-verifications/aispm-visual-smoke-validation.json", failures)
    require_file("docs/release-verifications/aispm-visual-smoke-validation.md", failures)
    require_file("apps/sandbox-ui/index.html", failures)
    require_file("apps/sandbox-ui/sandbox.js", failures)
    require_file("scripts/validate-sandbox-portal.py", failures)

    if failures:
        for failure in failures:
            print(failure)
        return 1

    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    html = read("apps/sandbox-ui/index.html")
    js = read("apps/sandbox-ui/sandbox.js")
    roadmap = read("docs/ai-security-posture-dashboard-roadmap.md")
    redesign = read("docs/sandbox-portal-redesign.md")
    smoke = read("docs/sandbox-portal-smoke-validation.md")
    visual = read("docs/release-verifications/aispm-visual-smoke-validation.json")
    visual_doc = read("docs/release-verifications/aispm-visual-smoke-validation.md")
    wiki_roadmap = read("docs/wiki/AISPM-Dashboard-Roadmap.md")
    wiki_redesign = read("docs/wiki/CAVRA-Developer-Portal-Redesign.md")
    wiki_smoke = read("docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md")
    community_ci = read(".github/workflows/community-ci.yml")
    release_ci = read(".github/workflows/release-community.yml")

    if index.get("schema_version") != "cavra.aispm.launch_board_pack_artifact_index.v1":
        failures.append(f"{INDEX_PATH}: invalid schema_version")
    if index.get("board_pack_packet") != "cavra-aispm-pilot-launch-board-pack-packet.json":
        failures.append(f"{INDEX_PATH}: board_pack_packet must match portal download filename")

    required_dom = [
        'id="aispmPilotLaunchBoardPackManifest"',
        'id="copyAispmPilotLaunchBoardPackPacket"',
        'id="downloadAispmPilotLaunchBoardPackPacket"',
        "Board pack packet",
    ]
    for needle in required_dom:
        require(html, needle, "board-pack DOM contract", failures)

    required_js = [
        "currentAispmPilotLaunchBoardPackPacket",
        "renderAispmPilotLaunchBoardPack",
        "copyAispmPilotLaunchBoardPackPacket",
        "downloadAispmPilotLaunchBoardPackPacket",
        "cavra.aispm.pilot_launch_board_pack_packet.v1",
        "artifact_manifest",
        "freshness_gate",
        "cavra-aispm-pilot-launch-board-pack-packet.json",
        "signed_board_approval",
        "board_minutes_and_attestation",
        "pdf_generation_and_delivery",
        "recipient_allowlists_and_email_audit",
        "tenant_artifact_retention",
    ]
    for needle in required_js:
        require(js, needle, "board-pack JS contract", failures)

    artifact_filenames = [artifact["filename"] for artifact in index.get("artifacts", [])]
    if len(artifact_filenames) < 8:
        failures.append(f"{INDEX_PATH}: expected at least 8 board-pack artifacts")
    for filename in artifact_filenames:
        require(js, filename, "board-pack artifact filename in portal JS", failures)
        require(redesign, filename, "board-pack artifact filename in portal redesign docs", failures)
        require(smoke, filename, "board-pack artifact filename in smoke docs", failures)

    for doc_path in index.get("required_docs", []):
        require_file(doc_path, failures)
    for doc_text, label in [
        (roadmap, "roadmap"),
        (redesign, "portal redesign"),
        (smoke, "smoke validation"),
        (wiki_roadmap, "wiki roadmap"),
        (wiki_redesign, "wiki portal redesign"),
        (wiki_smoke, "wiki smoke validation"),
    ]:
        require(doc_text, "cavra-aispm-pilot-launch-board-pack-packet.json", label, failures)
        require(doc_text, "scripts/validate-aispm-launch-artifacts.py", label, failures)

    require(community_ci, "python scripts/validate-aispm-launch-artifacts.py", "Community CI validator", failures)
    require(release_ci, "python scripts/validate-aispm-launch-artifacts.py", "Release CI validator", failures)
    require(community_ci, "npm run validate:sandbox:visual", "Community CI visual smoke command", failures)
    require(release_ci, "npm run validate:sandbox:visual", "Release CI visual smoke command", failures)
    require(community_ci, "python scripts/validate-aispm-visual-freshness.py", "Community CI visual freshness validator", failures)
    require(release_ci, "python scripts/validate-aispm-visual-freshness.py", "Release CI visual freshness validator", failures)
    require(visual, "scripts/validate-sandbox-visual.mjs", "visual smoke validation record", failures)
    require(visual_doc, "Pilot Launch Board Pack Packet", "visual smoke validation doc", failures)
    require(visual_doc, "CSO Report Center", "visual smoke validation doc", failures)

    forbidden_public_payload_terms = [
        "license_private_key",
        "customer_identity_payload",
        "raw_prompt_payload",
    ]
    combined_public_text = "\n".join([html, js, roadmap, redesign, smoke, wiki_roadmap, wiki_redesign, wiki_smoke])
    for term in forbidden_public_payload_terms:
        if term in combined_public_text:
            failures.append(f"public AISPM board-pack artifacts must not expose {term}")

    if failures:
        print("AISPM launch board pack artifact validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM launch board pack artifact validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
