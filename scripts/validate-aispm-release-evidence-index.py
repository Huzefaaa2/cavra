#!/usr/bin/env python3
"""Validate the public-safe AISPM release evidence index."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "docs/release-verifications/aispm-release-evidence-index.json"


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
        "docs/release-verifications/aispm-release-evidence-index.json",
        "docs/release-verifications/aispm-release-evidence-index.md",
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/sandbox.js",
        "apps/sandbox-ui/styles.css",
        "scripts/validate-aispm-release-evidence-index.py",
        "scripts/validate-aispm-report-catalog-readiness.py",
        "scripts/validate-aispm-report-delivery-setup-readiness.py",
        "scripts/validate-aispm-report-operations-readiness.py",
        "scripts/validate-aispm-report-governance-readiness.py",
        "scripts/validate-aispm-report-assurance-readiness.py",
        "scripts/validate-aispm-report-response-readiness.py",
        "scripts/validate-aispm-report-trial-operations-readiness.py",
        "scripts/validate-aispm-pilot-control-readiness.py",
        "scripts/validate-aispm-v100-public-release.py",
        "scripts/validate-aispm-final-announcement-readiness.py",
        "scripts/validate-hosted-sandbox-deployment-freshness.py",
        "scripts/validate-hosted-sandbox-operator-status.py",
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
        "README.md",
        "docs/sandbox-portal-redesign.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
    ]
    for path in required_files:
        require_file(path, failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    index = load_json("docs/release-verifications/aispm-release-evidence-index.json")
    require(
        index.get("schema_version") == "cavra.aispm.release_evidence_index.v1",
        f"{INDEX_PATH}: invalid schema_version",
        failures,
    )
    require(index.get("status") == "ready", f"{INDEX_PATH}: status must be ready", failures)
    require(
        index.get("portal_packet") == "cavra-aispm-release-evidence-index-packet.json",
        f"{INDEX_PATH}: portal packet mismatch",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/hosted-sandbox-deployment-freshness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing hosted deployment freshness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/hosted-sandbox-operator-release-status.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing hosted operator release status item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-catalog-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM report catalog readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-delivery-setup-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM report delivery setup readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-operations-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM report operations readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-governance-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM report governance readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-assurance-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM report assurance readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-response-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM report response readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-trial-operations-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM report trial operations readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-pilot-control-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM pilot control readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-v1.0-public-release-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM v1.0 public release readiness item",
        failures,
    )
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-final-announcement-readiness.json"
            for item in index.get("evidence_items", [])
        ),
        f"{INDEX_PATH}: missing AISPM final announcement readiness item",
        failures,
    )
    evidence_items = index.get("evidence_items", [])
    require(len(evidence_items) >= 7, f"{INDEX_PATH}: expected at least 7 evidence items", failures)
    for item in evidence_items:
        require_file(item["markdown"], failures)
        require_file(item["machine_readable"], failures)
        require(item["status"] in {"ready", "pass", "workflow_enforced"}, f"{INDEX_PATH}: invalid status {item}", failures)

    html = read("apps/sandbox-ui/index.html")
    js = read("apps/sandbox-ui/sandbox.js")
    css = read("apps/sandbox-ui/styles.css")
    for needle in [
        'id="aispmReleaseEvidenceIndex"',
        'id="aispmReleaseEvidenceManifest"',
        'id="copyAispmReleaseEvidenceIndexPacket"',
        'id="downloadAispmReleaseEvidenceIndexPacket"',
        'id="aispmReleaseEvidenceStatus"',
        "Release Evidence Index",
    ]:
        require(needle in html, f"portal DOM missing {needle}", failures)
    for needle in [
        "aispmReleaseEvidenceIndexItems",
        "renderAispmReleaseEvidenceIndex",
        "currentAispmReleaseEvidenceIndexPacket",
        "copyAispmReleaseEvidenceIndexPacket",
        "downloadAispmReleaseEvidenceIndexPacket",
        "cavra.aispm.release_evidence_index_packet.v1",
        "cavra-aispm-release-evidence-index-packet.json",
        "scripts/validate-aispm-release-evidence-index.py",
        "scripts/validate-aispm-report-catalog-readiness.py",
        "scripts/validate-aispm-report-delivery-setup-readiness.py",
        "scripts/validate-aispm-report-operations-readiness.py",
        "scripts/validate-aispm-report-governance-readiness.py",
        "scripts/validate-aispm-report-assurance-readiness.py",
        "scripts/validate-aispm-report-response-readiness.py",
        "scripts/validate-aispm-report-trial-operations-readiness.py",
        "scripts/validate-aispm-pilot-control-readiness.py",
        "scripts/validate-aispm-v100-public-release.py",
        "scripts/validate-aispm-final-announcement-readiness.py",
        "scripts/validate-hosted-sandbox-deployment-freshness.py",
        "scripts/validate-hosted-sandbox-operator-status.py",
        "cavra-hosted-sandbox-operator-status-packet.json",
        "cavra-hosted-sandbox-post-deploy-evidence",
        "cavra-aispm-report-catalog-packet.json",
        "cavra-aispm-report-delivery-setup-packet.json",
        "cavra-aispm-report-operations-readiness-packet.json",
        "cavra-aispm-report-governance-readiness-packet.json",
        "cavra-aispm-report-assurance-readiness-packet.json",
        "cavra-aispm-report-response-readiness-packet.json",
        "cavra-aispm-report-trial-operations-readiness-packet.json",
        "cavra-aispm-pilot-control-readiness-packet.json",
        "docs/release-verifications/aispm-v1.0-public-release-readiness.json",
    ]:
        require(needle in js, f"portal JS missing {needle}", failures)
    for needle in [
        ".aispm-release-evidence-panel",
        ".release-evidence-grid",
        ".release-evidence-manifest-grid",
        ".release-evidence-card",
    ]:
        require(needle in css, f"portal CSS missing {needle}", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require_text(workflow_path, "python scripts/validate-aispm-release-evidence-index.py", workflow_path, failures)

    doc_needles = [
        "docs/release-verifications/aispm-release-evidence-index.md",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "scripts/validate-aispm-release-evidence-index.py",
        "docs/release-verifications/aispm-report-operations-readiness.md",
        "docs/release-verifications/aispm-report-operations-readiness.json",
        "docs/release-verifications/aispm-report-governance-readiness.md",
        "docs/release-verifications/aispm-report-governance-readiness.json",
        "docs/release-verifications/aispm-report-assurance-readiness.md",
        "docs/release-verifications/aispm-report-assurance-readiness.json",
        "docs/release-verifications/aispm-report-response-readiness.md",
        "docs/release-verifications/aispm-report-response-readiness.json",
        "docs/release-verifications/aispm-report-trial-operations-readiness.md",
        "docs/release-verifications/aispm-report-trial-operations-readiness.json",
        "docs/release-verifications/aispm-pilot-control-readiness.md",
        "docs/release-verifications/aispm-pilot-control-readiness.json",
        "docs/release-verifications/aispm-v1.0-public-release-readiness.md",
        "docs/release-verifications/aispm-v1.0-public-release-readiness.json",
        "docs/release-verifications/aispm-final-announcement-readiness.md",
        "docs/release-verifications/aispm-final-announcement-readiness.json",
        "scripts/validate-aispm-report-delivery-setup-readiness.py",
        "scripts/validate-aispm-report-operations-readiness.py",
        "scripts/validate-aispm-report-governance-readiness.py",
        "scripts/validate-aispm-report-assurance-readiness.py",
        "scripts/validate-aispm-report-response-readiness.py",
        "scripts/validate-aispm-report-trial-operations-readiness.py",
        "scripts/validate-aispm-pilot-control-readiness.py",
        "scripts/validate-aispm-v100-public-release.py",
        "scripts/validate-aispm-final-announcement-readiness.py",
        "scripts/validate-hosted-sandbox-deployment-freshness.py",
        "scripts/validate-hosted-sandbox-operator-status.py",
        "cavra-hosted-sandbox-operator-status-packet.json",
        "cavra-aispm-report-delivery-setup-packet.json",
        "cavra-aispm-report-operations-readiness-packet.json",
        "cavra-aispm-report-governance-readiness-packet.json",
        "cavra-aispm-report-assurance-readiness-packet.json",
        "cavra-aispm-report-response-readiness-packet.json",
        "cavra-aispm-report-trial-operations-readiness-packet.json",
        "cavra-aispm-pilot-control-readiness-packet.json",
        "cavra-aispm-final-announcement-readiness-packet.json",
        "cavra-aispm-release-evidence-index-packet.json",
    ]
    for doc_path in [
        "README.md",
        "docs/sandbox-portal-redesign.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
    ]:
        for needle in doc_needles:
            require_text(doc_path, needle, doc_path, failures)

    forbidden = [
        "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
        "license_private_key",
        "private_registry_token",
        "customer_identity_payload",
        "raw_prompt_payload",
        "tenant_telemetry_payload",
    ]
    combined = "\n".join(
        [
            read("docs/release-verifications/aispm-release-evidence-index.json"),
            read("docs/release-verifications/aispm-release-evidence-index.md"),
            html,
            js,
        ]
    )
    for term in forbidden:
        require(term not in combined, f"release evidence index must not expose {term}", failures)

    if failures:
        print("AISPM release evidence index validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM release evidence index validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
