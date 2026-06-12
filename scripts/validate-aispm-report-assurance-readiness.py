#!/usr/bin/env python3
"""Validate public-safe AISPM report assurance readiness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs/release-verifications/aispm-report-assurance-readiness.json"


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
        "docs/release-verifications/aispm-report-assurance-readiness.json",
        "docs/release-verifications/aispm-report-assurance-readiness.md",
        "docs/release-verifications/aispm-report-governance-readiness.json",
        "docs/release-verifications/aispm-report-operations-readiness.json",
        "docs/release-verifications/aispm-report-delivery-setup-readiness.json",
        "docs/release-verifications/aispm-report-catalog-readiness.json",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "docs/release-verifications/aispm-release-evidence-index.md",
        "docs/release-verifications/aispm-launch-readiness-rollup.json",
        "docs/release-verifications/aispm-launch-readiness-rollup.md",
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/sandbox.js",
        "apps/sandbox-ui/styles.css",
        "scripts/validate-aispm-report-assurance-readiness.py",
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/architecture/aispm-report-center.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/AISPM-CSO-Report-Center.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]
    for path in required_files:
        require_file(path, failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    packet = load_json("docs/release-verifications/aispm-report-assurance-readiness.json")
    require(
        packet.get("schema_version") == "cavra.aispm.report_assurance_readiness.v1",
        f"{PACKET_PATH}: invalid schema_version",
        failures,
    )
    require(packet.get("status") == "ready", f"{PACKET_PATH}: status must be ready", failures)
    require(
        packet.get("portal_packet") == "cavra-aispm-report-assurance-readiness-packet.json",
        f"{PACKET_PATH}: portal packet mismatch",
        failures,
    )
    assurance_areas = packet.get("assurance_areas", [])
    require(len(assurance_areas) == 5, f"{PACKET_PATH}: expected 5 assurance areas", failures)
    require(
        {area.get("area_id") for area in assurance_areas}
        == {
            "evidence_room_access_events",
            "incident_packet",
            "incident_closure",
            "kpi_metrics",
            "alert_escalation",
        },
        f"{PACKET_PATH}: assurance area set mismatch",
        failures,
    )
    for area in assurance_areas:
        require_file(area["schema"], failures)
        require_file(area["example"], failures)
        require(
            area.get("status") == "requires_cavra_enterprise",
            f"{PACKET_PATH}: assurance area must require Enterprise: {area}",
            failures,
        )
    require(
        all(value == "requires_cavra_enterprise" for value in packet.get("enterprise_boundaries", {}).values()),
        f"{PACKET_PATH}: Enterprise boundaries must require Enterprise",
        failures,
    )

    release_index = load_json("docs/release-verifications/aispm-release-evidence-index.json")
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-assurance-readiness.json"
            for item in release_index.get("evidence_items", [])
        ),
        "release evidence index missing report assurance readiness item",
        failures,
    )
    launch_rollup = load_json("docs/release-verifications/aispm-launch-readiness-rollup.json")
    require(
        any(
            source.get("path")
            == "docs/release-verifications/aispm-report-assurance-readiness.json"
            for source in launch_rollup.get("required_sources", [])
        ),
        "launch readiness rollup missing report assurance readiness source",
        failures,
    )

    html = read("apps/sandbox-ui/index.html")
    js = read("apps/sandbox-ui/sandbox.js")
    css = read("apps/sandbox-ui/styles.css")
    for needle in [
        "Report Assurance Readiness",
        'data-report-assurance-packet="cavra-aispm-report-assurance-readiness-packet.json"',
        'id="aispmReportAssuranceReadiness"',
        'id="copyAispmReportAssurancePacket"',
        'id="downloadAispmReportAssurancePacket"',
        'id="aispmReportAssuranceStatus"',
    ]:
        require(needle in html, f"portal DOM missing {needle}", failures)
    for needle in [
        "currentAispmReportAssurancePacket",
        "aispmReportAssuranceReadinessItems",
        "renderAispmReportAssuranceReadiness",
        "cavra.aispm.report_assurance_readiness_packet.v1",
        "cavra-aispm-report-assurance-readiness-packet.json",
        "copyAispmReportAssurancePacket",
        "downloadAispmReportAssurancePacket",
        "scripts/validate-aispm-report-assurance-readiness.py",
        "src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json",
        "src/cavra/schemas/aispm-report-alert-escalation.schema.json",
    ]:
        require(needle in js, f"portal JS missing {needle}", failures)
    for needle in [
        ".aispm-report-assurance-panel",
        ".report-assurance-grid",
        ".report-assurance-card",
    ]:
        require(needle in css, f"portal CSS missing {needle}", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require_text(
            workflow_path,
            "python scripts/validate-aispm-report-assurance-readiness.py",
            workflow_path,
            failures,
        )
    for needle in [
        'grep -q "Report Assurance Readiness"',
        'grep -q "cavra-aispm-report-assurance-readiness-packet.json"',
    ]:
        require_text(".github/workflows/deploy-sandbox.yml", needle, "deploy workflow", failures)

    doc_needles = [
        "docs/release-verifications/aispm-report-assurance-readiness.md",
        "docs/release-verifications/aispm-report-assurance-readiness.json",
        "scripts/validate-aispm-report-assurance-readiness.py",
        "cavra-aispm-report-assurance-readiness-packet.json",
    ]
    for doc_path in [
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/architecture/aispm-report-center.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/sandbox-portal-redesign.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/AISPM-CSO-Report-Center.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
    ]:
        for needle in doc_needles:
            require_text(doc_path, needle, doc_path, failures)

    forbidden = [
        "auditor@example",
        "approver@example",
        "ip_address=",
        '"ip_address":',
        "raw_report_payload",
        "download_url=",
        '"download_url":',
        "customer_identity_payload",
        "tenant_telemetry_payload",
        "private_remediation_detail=",
        '"private_remediation_detail":',
        "CAVRA_REPORT_SMTP_PASSWORD=",
        "CAVRA_REPORT_PROVIDER_TOKEN=",
    ]
    combined = "\n".join(
        [
            read("docs/release-verifications/aispm-report-assurance-readiness.json"),
            read("docs/release-verifications/aispm-report-assurance-readiness.md"),
            html,
            js,
        ]
    )
    for term in forbidden:
        require(term not in combined, f"report assurance readiness must not expose {term}", failures)

    if failures:
        print("AISPM report assurance readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM report assurance readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
