#!/usr/bin/env python3
"""Validate public-safe AISPM final announcement readiness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs/release-verifications/aispm-final-announcement-readiness.json"
MARKDOWN_PATH = ROOT / "docs/release-verifications/aispm-final-announcement-readiness.md"


FORBIDDEN = (
    "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
    "LICENSE_SIGNING_KEY",
    "private_registry_token",
    "customer_identity_payload",
    "raw_prompt_payload",
    "tenant_telemetry_payload",
    "license_private_key",
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(read(path))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_file(path: str, failures: list[str]) -> None:
    require((ROOT / path).is_file(), f"missing required file: {path}", failures)


def main() -> int:
    failures: list[str] = []
    require_file("docs/release-verifications/aispm-final-announcement-readiness.json", failures)
    require_file("docs/release-verifications/aispm-final-announcement-readiness.md", failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")

    require(
        packet.get("schema_version") == "cavra.aispm.final_announcement_readiness.v1",
        f"{PACKET_PATH}: invalid schema_version",
        failures,
    )
    require(packet.get("status") == "ready", f"{PACKET_PATH}: status must be ready", failures)
    require(
        packet.get("announcement_decision") == "ready_for_public_announcement",
        f"{PACKET_PATH}: announcement decision must be ready_for_public_announcement",
        failures,
    )
    require(
        packet.get("portal_packet") == "cavra-aispm-final-announcement-readiness-packet.json",
        f"{PACKET_PATH}: portal packet mismatch",
        failures,
    )
    require(
        packet.get("validator") == "scripts/validate-aispm-final-announcement-readiness.py",
        f"{PACKET_PATH}: validator mismatch",
        failures,
    )

    required_source_ids = {
        "launch_readiness_rollup",
        "release_evidence_index",
        "public_release_readiness",
        "trial_field_guide",
        "hosted_operator_status",
        "hosted_post_deploy_evidence",
        "community_release_verification",
        "release_notes",
    }
    sources = {source.get("source_id"): source for source in packet.get("required_sources", [])}
    require(set(sources) == required_source_ids, f"{PACKET_PATH}: source set mismatch", failures)
    for source_id, source in sources.items():
        path = source.get("path")
        require_file(path, failures)
        require(
            source.get("status") in {"ready", "pass", "workflow_enforced"},
            f"{PACKET_PATH}: invalid source status for {source_id}",
            failures,
        )
        require(bool(source.get("validator")), f"{PACKET_PATH}: missing validator for {source_id}", failures)

    gates = {gate.get("gate_id"): gate for gate in packet.get("announcement_gates", [])}
    require(
        set(gates)
        == {
            "community_portal_ready",
            "release_evidence_ready",
            "field_guide_published",
            "hosted_release_operator_ready",
            "public_release_notes_ready",
            "public_safety_boundary_verified",
        },
        f"{PACKET_PATH}: gate set mismatch",
        failures,
    )
    for gate_id, gate in gates.items():
        require(gate.get("status") == "ready", f"{PACKET_PATH}: gate {gate_id} not ready", failures)
        require_file(gate.get("evidence"), failures)

    launch = load_json("docs/release-verifications/aispm-launch-readiness-rollup.json")
    evidence_index = load_json("docs/release-verifications/aispm-release-evidence-index.json")
    public_release = load_json("docs/release-verifications/aispm-v1.0-public-release-readiness.json")
    trial_guide = load_json(
        "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json"
    )
    hosted_operator = load_json("docs/release-verifications/hosted-sandbox-operator-release-status.json")

    require(launch.get("overall_status") == "ready", "launch readiness rollup must be ready", failures)
    require(evidence_index.get("status") == "ready", "release evidence index must be ready", failures)
    require(
        public_release.get("status") in {"ready", "ready_for_pr_and_pages_deploy"},
        "AISPM v1.0 public release must be ready",
        failures,
    )
    require(trial_guide.get("overall_status") == "ready", "Trial Field Guide must be ready", failures)
    require(hosted_operator.get("status") == "ready", "hosted operator status must be ready", failures)

    for section in (
        "## Included Gates",
        "## Announcement Decision",
        "## Required Sources",
        "## Operator Commands",
        "## Public Safety Boundary",
        "## Enterprise Boundary",
    ):
        require(section in markdown, f"{MARKDOWN_PATH}: missing {section}", failures)
    for needle in (
        "ready_for_public_announcement",
        "docs/release-verifications/aispm-launch-readiness-rollup.json",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "docs/wiki/CAVRA-Trial-Field-Guide.md",
        "cavra-aispm-final-announcement-readiness-packet.json",
    ):
        require(needle in json.dumps(packet) + markdown, f"missing {needle}", failures)

    combined = json.dumps(packet) + "\n" + markdown
    for term in FORBIDDEN:
        require(term not in combined, f"final announcement packet must not expose {term}", failures)

    if failures:
        print("AISPM final announcement readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM final announcement readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
