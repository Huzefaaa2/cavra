#!/usr/bin/env python3
"""Validate public-safe AISPM report catalog readiness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "docs/release-verifications/aispm-report-catalog-readiness.json"


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
        "docs/release-verifications/aispm-report-catalog-readiness.json",
        "docs/release-verifications/aispm-report-catalog-readiness.md",
        "docs/release-verifications/aispm-release-evidence-index.json",
        "docs/release-verifications/aispm-release-evidence-index.md",
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/sandbox.js",
        "apps/sandbox-ui/styles.css",
        "scripts/validate-aispm-report-catalog-readiness.py",
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

    catalog = load_json("docs/release-verifications/aispm-report-catalog-readiness.json")
    require(
        catalog.get("schema_version") == "cavra.aispm.report_catalog_readiness.v1",
        f"{CATALOG_PATH}: invalid schema_version",
        failures,
    )
    require(catalog.get("status") == "ready", f"{CATALOG_PATH}: status must be ready", failures)
    require(
        catalog.get("portal_packet") == "cavra-aispm-report-catalog-packet.json",
        f"{CATALOG_PATH}: portal packet mismatch",
        failures,
    )
    community_reports = catalog.get("community_reports", [])
    require(len(community_reports) == 6, f"{CATALOG_PATH}: expected 6 Community reports", failures)
    expected_filenames = {
        "cavra-aispm-executive-risk-brief.md",
        "cavra-aispm-board-kpi-pack.json",
        "cavra-aispm-soc2-audit-summary.md",
        "cavra-aispm-control-coverage.csv",
        "cavra-aispm-evidence-freshness.csv",
        "cavra-aispm-agent-risk-register.csv",
    }
    require(
        {item.get("filename") for item in community_reports} == expected_filenames,
        f"{CATALOG_PATH}: Community report filenames do not match portal contract",
        failures,
    )
    require(
        set(catalog.get("enterprise_locked_reports", []))
        >= {"PDF Board Pack", "XLSX Evidence Workbook", "Scheduled Email Delivery", "Recipient Governance"},
        f"{CATALOG_PATH}: missing Enterprise locked report capabilities",
        failures,
    )
    for boundary_value in catalog.get("enterprise_boundaries", {}).values():
        require(
            boundary_value == "requires_cavra_enterprise",
            f"{CATALOG_PATH}: Enterprise boundaries must be locked to Enterprise",
            failures,
        )

    release_index = load_json("docs/release-verifications/aispm-release-evidence-index.json")
    require(
        any(
            item.get("machine_readable")
            == "docs/release-verifications/aispm-report-catalog-readiness.json"
            for item in release_index.get("evidence_items", [])
        ),
        "release evidence index missing AISPM report catalog readiness item",
        failures,
    )

    html = read("apps/sandbox-ui/index.html")
    js = read("apps/sandbox-ui/sandbox.js")
    css = read("apps/sandbox-ui/styles.css")
    for needle in [
        "CSO Report Center",
        'data-report-catalog-packet="cavra-aispm-report-catalog-packet.json"',
        'id="copyAispmReportCatalogPacket"',
        'id="downloadAispmReportCatalogPacket"',
        'id="aispmReportStatus"',
    ]:
        require(needle in html, f"portal DOM missing {needle}", failures)
    for needle in [
        "currentAispmReportCatalogPacket",
        "cavra.aispm.report_catalog_readiness_packet.v1",
        "cavra-aispm-report-catalog-packet.json",
        "copyAispmReportCatalogPacket",
        "downloadAispmReportCatalogPacket",
        "scripts/validate-aispm-report-catalog-readiness.py",
        "CSO Report Catalog Readiness",
        "Report Catalog Readiness Packet",
    ]:
        require(needle in js, f"portal JS missing {needle}", failures)
    for needle in [
        ".aispm-report-center-panel",
        ".report-center-grid",
        ".report-card",
        ".report-delivery-panel",
    ]:
        require(needle in css, f"portal CSS missing {needle}", failures)

    for filename in expected_filenames:
        require(filename in js, f"portal JS missing report filename {filename}", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require_text(workflow_path, "python scripts/validate-aispm-report-catalog-readiness.py", workflow_path, failures)

    doc_needles = [
        "docs/release-verifications/aispm-report-catalog-readiness.md",
        "docs/release-verifications/aispm-report-catalog-readiness.json",
        "scripts/validate-aispm-report-catalog-readiness.py",
        "cavra-aispm-report-catalog-packet.json",
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
        "smtp_password=",
        '"smtp_password":',
        "private_smtp_secret",
        "recipient@example.private",
        "customer_identity_payload",
        "raw_prompt_payload",
        "model_reasoning_payload",
        "tenant_telemetry_payload",
    ]
    combined = "\n".join(
        [
            read("docs/release-verifications/aispm-report-catalog-readiness.json"),
            read("docs/release-verifications/aispm-report-catalog-readiness.md"),
            html,
            js,
        ]
    )
    for term in forbidden:
        require(term not in combined, f"report catalog readiness must not expose {term}", failures)

    if failures:
        print("AISPM report catalog readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AISPM report catalog readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
