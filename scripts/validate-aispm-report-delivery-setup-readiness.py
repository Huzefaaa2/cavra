#!/usr/bin/env python3
"""Validate public-safe AISPM report delivery setup readiness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs/release-verifications/aispm-report-delivery-setup-readiness.json"


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
        "docs/release-verifications/aispm-report-delivery-setup-readiness.json",
        "docs/release-verifications/aispm-report-delivery-setup-readiness.md",
        "docs/release-verifications/aispm-report-catalog-readiness.json",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "docs/release-verifications/aispm-release-evidence-index.md",
        "docs/release-verifications/aispm-launch-readiness-rollup.json",
        "docs/release-verifications/aispm-launch-readiness-rollup.md",
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/sandbox.js",
        "apps/sandbox-ui/styles.css",
        "scripts/validate-aispm-report-delivery-setup-readiness.py",
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/architecture/aispm-report-center.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/AISPM-CSO-Report-Center.md",
    ]
    for path in required_files:
        require_file(path, failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    packet = load_json("docs/release-verifications/aispm-report-delivery-setup-readiness.json")
    require(
        packet.get("schema_version") == "cavra.aispm.report_delivery_setup_readiness.v1",
        f"{PACKET_PATH}: invalid schema_version",
        failures,
    )
    require(packet.get("status") == "ready", f"{PACKET_PATH}: status must be ready", failures)
    require(
        packet.get("portal_packet") == "cavra-aispm-report-delivery-setup-packet.json",
        f"{PACKET_PATH}: portal packet mismatch",
        failures,
    )
    setup_areas = packet.get("setup_areas", [])
    require(len(setup_areas) == 5, f"{PACKET_PATH}: expected 5 setup areas", failures)
    require(
        {area.get("step_id") for area in setup_areas}
        == {
            "organization_profile",
            "delivery_provider",
            "recipient_governance",
            "schedule_and_audit",
            "validation_and_test_delivery",
        },
        f"{PACKET_PATH}: setup area set mismatch",
        failures,
    )
    require(
        "CAVRA_REPORT_SMTP_PASSWORD_REF" in packet.get("secret_reference_settings", []),
        f"{PACKET_PATH}: missing SMTP password secret reference",
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
            == "docs/release-verifications/aispm-report-delivery-setup-readiness.json"
            for item in release_index.get("evidence_items", [])
        ),
        "release evidence index missing report delivery setup readiness item",
        failures,
    )
    launch_rollup = load_json("docs/release-verifications/aispm-launch-readiness-rollup.json")
    require(
        any(
            source.get("path")
            == "docs/release-verifications/aispm-report-delivery-setup-readiness.json"
            for source in launch_rollup.get("required_sources", [])
        ),
        "launch readiness rollup missing report delivery setup readiness source",
        failures,
    )

    html = read("apps/sandbox-ui/index.html")
    js = read("apps/sandbox-ui/sandbox.js")
    css = read("apps/sandbox-ui/styles.css")
    for needle in [
        "Report Delivery Setup Readiness",
        'data-report-setup-packet="cavra-aispm-report-delivery-setup-packet.json"',
        'id="aispmReportSetupReadiness"',
        'id="copyAispmReportSetupPacket"',
        'id="downloadAispmReportSetupPacket"',
        'id="aispmReportSetupStatus"',
    ]:
        require(needle in html, f"portal DOM missing {needle}", failures)
    for needle in [
        "currentAispmReportSetupPacket",
        "aispmReportSetupReadinessItems",
        "renderAispmReportSetupReadiness",
        "cavra.aispm.report_delivery_setup_readiness_packet.v1",
        "cavra-aispm-report-delivery-setup-packet.json",
        "copyAispmReportSetupPacket",
        "downloadAispmReportSetupPacket",
        "scripts/validate-aispm-report-delivery-setup-readiness.py",
        "CAVRA_REPORT_SMTP_PASSWORD_REF",
    ]:
        require(needle in js, f"portal JS missing {needle}", failures)
    for needle in [
        ".aispm-report-setup-panel",
        ".report-setup-grid",
        ".report-setup-card",
        ".report-setup-boundary",
    ]:
        require(needle in css, f"portal CSS missing {needle}", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require_text(
            workflow_path,
            "python scripts/validate-aispm-report-delivery-setup-readiness.py",
            workflow_path,
            failures,
        )

    doc_needles = [
        "docs/release-verifications/aispm-report-delivery-setup-readiness.md",
        "docs/release-verifications/aispm-report-delivery-setup-readiness.json",
        "scripts/validate-aispm-report-delivery-setup-readiness.py",
        "cavra-aispm-report-delivery-setup-packet.json",
    ]
    for doc_path in [
        "README.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/architecture/aispm-report-center.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/AISPM-CSO-Report-Center.md",
    ]:
        for needle in doc_needles:
            require_text(doc_path, needle, doc_path, failures)

    forbidden = [
        "CAVRA_REPORT_SMTP_PASSWORD=",
        "CAVRA_REPORT_PROVIDER_TOKEN=",
        "security-lead@example.com",
        "ciso@example.com",
        "recipient_email=",
        '"recipient_email":',
        "raw_report_payload",
        "provider_response_payload",
        "customer_identity_payload",
        "tenant_telemetry_payload",
    ]
    combined = "\n".join(
        [
            read("docs/release-verifications/aispm-report-delivery-setup-readiness.json"),
            read("docs/release-verifications/aispm-report-delivery-setup-readiness.md"),
            html,
            js,
        ]
    )
    for term in forbidden:
        require(term not in combined, f"report delivery setup readiness must not expose {term}", failures)

    if failures:
        print("AISPM report delivery setup readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM report delivery setup readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
