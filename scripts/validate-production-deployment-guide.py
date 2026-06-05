#!/usr/bin/env python3
"""Validate public production deployment guide release coverage."""

from __future__ import annotations

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
    normalized_phrase = " ".join(phrase.lower().split())
    normalized_text = " ".join(text.lower().split())
    if normalized_phrase not in normalized_text:
        failures.append(f"missing {label}: {phrase}")


def main() -> int:
    failures: list[str] = []
    required_files = [
        "docs/production-deployment-guide-validation.md",
        "docs/wiki/Production-Deployment-Guide-Validation.md",
        "docs/deployment.md",
        "docs/production-deployment-validation.md",
        "docs/persistent-api-operations.md",
        "docs/sandbox.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/console-closeout-operator-experience.md",
        "docs/community-ga-user-verifiable-path.md",
        "scripts/validate-production-deployment-guide.py",
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

    guide = read("docs/production-deployment-guide-validation.md")
    wiki_guide = read("docs/wiki/Production-Deployment-Guide-Validation.md")
    deployment = read("docs/deployment.md")
    readiness = read("docs/production-deployment-validation.md")
    persistent_ops = read("docs/persistent-api-operations.md")
    sandbox = read("docs/sandbox.md")
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    wiki_home = read("docs/wiki/Home.md")
    inventory = read("docs/current-feature-inventory.md")
    wiki_inventory = read("docs/wiki/Current-Feature-Inventory.md")
    roadmap = read("docs/production-roadmap.md")
    next_slice = read("docs/roadmap-status-next-slice.md")
    audit_next_batch = read("docs/roadmap-status-audit-next-batch.md")

    for doc in [guide, wiki_guide]:
        for needle in [
            "Install",
            "Configuration",
            "Storage",
            "Backup",
            "Restore",
            "CORS/API",
            "GitHub Pages portal",
            "Evidence artifact root",
            "Persistent stores",
            "Validation Command",
            "Operator Runbook",
            "Public Boundary",
            "User Stories",
            "Enterprise Challenge Solved",
            "python scripts/validate-production-deployment-guide.py",
            "cavra ops stores",
            "cavra ops backup",
            "cavra ops restore",
            "curl http://127.0.0.1:8000/deployment/production-readiness",
            "python scripts/validate-sandbox-portal.py",
            "python scripts/validate-console-closeout.py",
            "python scripts/validate-community-ga-path.py",
            "CAVRA_ACTIVITY_STORE",
            "CAVRA_ACTIVITY_DB",
            "CAVRA_EVIDENCE_ARTIFACT_ROOT",
            "CAVRA_PUBLIC_API_BASE_URL",
            "CAVRA_CORS_ORIGINS",
            "Enterprise source code",
            "license-service secrets",
            "provider credentials",
        ]:
            require(doc, needle, "production deployment guide documentation", failures)
        require_phrase(doc, NEXT_RECOMMENDATION, "deployment guide next recommendation", failures)

    for doc in [deployment, readiness]:
        for needle in [
            "Install",
            "Configuration",
            "Storage",
            "Backup",
            "Restore",
            "CORS/API",
            "GitHub Pages",
            "scripts/validate-production-deployment-guide.py",
        ]:
            require(doc, needle, "deployment coverage source", failures)

    for needle in [
        "cavra ops backup",
        "cavra ops restore",
        "retention-plan",
    ]:
        require(persistent_ops, needle, "persistent API operations", failures)

    for needle in [
        "CAVRA_PUBLIC_API_BASE_URL",
        "CAVRA_CORS_ORIGINS",
        "GitHub Pages",
    ]:
        require(sandbox, needle, "sandbox API and Pages configuration", failures)

    require(
        readme,
        "docs/production-deployment-guide-validation.md",
        "README deployment guide validation link",
        failures,
    )
    require(
        changelog,
        "production deployment guide validation",
        "changelog entry",
        failures,
    )
    require(
        wiki_home,
        "Production-Deployment-Guide-Validation.md",
        "wiki deployment guide validation link",
        failures,
    )
    for doc in [inventory, wiki_inventory]:
        require(
            doc,
            "Production deployment guide validation:",
            "feature inventory deployment guide validation entry",
            failures,
        )
    for doc in [roadmap, next_slice, audit_next_batch]:
        require(
            doc,
            "Production deployment guide validation is documented",
            "roadmap delivered deployment guide statement",
            failures,
        )
        require_phrase(doc, NEXT_RECOMMENDATION, "roadmap next recommendation", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/security-scan.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/cavra-governance.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require(
            read(workflow_path),
            "python scripts/validate-production-deployment-guide.py",
            f"{workflow_path} validator wiring",
            failures,
        )

    if failures:
        print("CAVRA production deployment guide validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA production deployment guide validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
