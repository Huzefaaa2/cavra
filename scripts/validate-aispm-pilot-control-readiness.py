#!/usr/bin/env python3
"""Validate public-safe AISPM pilot control readiness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs/release-verifications/aispm-pilot-control-readiness.json"


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
        "docs/release-verifications/aispm-pilot-control-readiness.json",
        "docs/release-verifications/aispm-pilot-control-readiness.md",
        "docs/release-verifications/aispm-launch-board-pack-artifact-index.json",
        "docs/release-verifications/aispm-launch-readiness-rollup.json",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/sandbox.js",
        "apps/sandbox-ui/styles.css",
        "scripts/validate-aispm-pilot-control-readiness.py",
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]
    for path in required_files:
        require_file(path, failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    packet = load_json("docs/release-verifications/aispm-pilot-control-readiness.json")
    require(
        packet.get("schema_version") == "cavra.aispm.pilot_control_readiness.v1",
        f"{PACKET_PATH}: invalid schema_version",
        failures,
    )
    require(packet.get("status") == "ready", f"{PACKET_PATH}: status must be ready", failures)
    require(
        packet.get("portal_packet") == "cavra-aispm-pilot-control-readiness-packet.json",
        f"{PACKET_PATH}: portal packet mismatch",
        failures,
    )
    require(
        packet.get("validator") == "scripts/validate-aispm-pilot-control-readiness.py",
        f"{PACKET_PATH}: validator mismatch",
        failures,
    )
    areas = packet.get("control_areas", [])
    require(len(areas) == 5, f"{PACKET_PATH}: expected 5 control areas", failures)
    require(
        {area.get("area_id") for area in areas}
        == {
            "pilot_exception_register",
            "pilot_risk_acceptance",
            "pilot_launch_board_pack",
            "board_pack_artifact_freshness",
            "launch_readiness_rollup",
        },
        f"{PACKET_PATH}: control area set mismatch",
        failures,
    )
    require(
        all(area.get("status") == "ready" for area in areas),
        f"{PACKET_PATH}: all control areas must be ready",
        failures,
    )
    require(
        all(value.startswith("requires_") for value in packet.get("enterprise_boundaries", {}).values()),
        f"{PACKET_PATH}: Enterprise boundaries must require private capabilities",
        failures,
    )

    release_index = load_json("docs/release-verifications/aispm-release-evidence-index.json")
    require(
        any(
            item.get("machine_readable") == "docs/release-verifications/aispm-pilot-control-readiness.json"
            for item in release_index.get("evidence_items", [])
        ),
        "release evidence index missing pilot control readiness item",
        failures,
    )
    launch_rollup = load_json("docs/release-verifications/aispm-launch-readiness-rollup.json")
    require(
        any(
            source.get("path") == "docs/release-verifications/aispm-pilot-control-readiness.json"
            for source in launch_rollup.get("required_sources", [])
        ),
        "launch readiness rollup missing pilot control readiness source",
        failures,
    )

    html = read("apps/sandbox-ui/index.html")
    js = read("apps/sandbox-ui/sandbox.js")
    css = read("apps/sandbox-ui/styles.css")
    for needle in [
        "Pilot Control Readiness",
        'data-pilot-control-packet="cavra-aispm-pilot-control-readiness-packet.json"',
        'id="aispmPilotControlReadiness"',
        'id="copyAispmPilotControlReadinessPacket"',
        'id="downloadAispmPilotControlReadinessPacket"',
        'id="aispmPilotControlStatus"',
    ]:
        require(needle in html, f"portal DOM missing {needle}", failures)
    for needle in [
        "currentAispmPilotControlReadinessPacket",
        "aispmPilotControlReadinessItems",
        "renderAispmPilotControlReadiness",
        "cavra.aispm.pilot_control_readiness_packet.v1",
        "cavra-aispm-pilot-control-readiness-packet.json",
        "copyAispmPilotControlReadinessPacket",
        "downloadAispmPilotControlReadinessPacket",
        "scripts/validate-aispm-pilot-control-readiness.py",
        "docs/release-verifications/aispm-pilot-control-readiness.json",
    ]:
        require(needle in js, f"portal JS missing {needle}", failures)
    for needle in [
        ".aispm-pilot-control-panel",
        ".pilot-control-grid",
        ".pilot-control-card",
    ]:
        require(needle in css, f"portal CSS missing {needle}", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require_text(
            workflow_path,
            "python scripts/validate-aispm-pilot-control-readiness.py",
            workflow_path,
            failures,
        )
    for needle in [
        'grep -q "Pilot Control Readiness"',
        'grep -q "cavra-aispm-pilot-control-readiness-packet.json"',
    ]:
        require_text(".github/workflows/deploy-sandbox.yml", needle, "deploy workflow", failures)

    doc_needles = [
        "docs/release-verifications/aispm-pilot-control-readiness.md",
        "docs/release-verifications/aispm-pilot-control-readiness.json",
        "scripts/validate-aispm-pilot-control-readiness.py",
        "cavra-aispm-pilot-control-readiness-packet.json",
    ]
    for doc_path in [
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]:
        for needle in doc_needles:
            require_text(doc_path, needle, doc_path, failures)

    forbidden = [
        "named_approver@example",
        "board_minutes_payload",
        "private_telemetry_payload",
        "customer_identity_payload",
        "license_key=",
        '"license_key":',
        "private_package_token=",
        '"private_package_token":',
        "enterprise_source_code_payload",
        "tenant_workflow_state_payload",
        "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
    ]
    combined = "\n".join(
        [
            read("docs/release-verifications/aispm-pilot-control-readiness.json"),
            read("docs/release-verifications/aispm-pilot-control-readiness.md"),
            html,
            js,
        ]
    )
    for term in forbidden:
        require(term not in combined, f"pilot control readiness must not expose {term}", failures)

    if failures:
        print("AISPM pilot control readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM pilot control readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
