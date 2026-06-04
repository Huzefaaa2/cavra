#!/usr/bin/env python3
"""Validate production readiness and procurement closeout coverage."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEXT_RECOMMENDATION = (
    "Prepare the next official Community maintenance release by converting the "
    "v0.1.1 dry-run packet into real release artifacts, verification evidence, "
    "release notes, README links, and wiki navigation."
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
        "docs/production-readiness-procurement-closeout.md",
        "docs/wiki/Production-Readiness-Procurement-Closeout.md",
        "docs/procurement-readiness.md",
        "docs/persistent-api-operations.md",
        "docs/evidence-metadata-migrations.md",
        "docs/release-security-advisories.md",
        "docs/vulnerability-disclosure.md",
        "docs/release-signing-operations.md",
        "docs/go-release-packaging.md",
        "docs/go-enforcement-production-hardening.md",
        "docs/enterprise-integration-validation.md",
        "docs/community-release-readiness-dashboard.md",
        "SECURITY.md",
        ".github/workflows/release-security.yml",
        ".github/workflows/go-release.yml",
        "scripts/package_go_release.py",
        "scripts/verify-community-release-artifacts.py",
        "scripts/validate_release_security.py",
        "scripts/validate-production-readiness-procurement-closeout.py",
        "scripts/validate-boundaries.sh",
        "go/cavra-runtime/runtime/decision_test.go",
        "examples/kubernetes/cavra-recurrence-automation-cronjob.yaml",
    ]
    for path in required_files:
        require_file(path, failures)

    if failures:
        for failure in failures:
            print(failure)
        return 1

    closeout_doc = read("docs/production-readiness-procurement-closeout.md")
    wiki_doc = read("docs/wiki/Production-Readiness-Procurement-Closeout.md")
    procurement_doc = read("docs/procurement-readiness.md")
    operations_doc = read("docs/persistent-api-operations.md")
    migrations_doc = read("docs/evidence-metadata-migrations.md")
    advisory_doc = read("docs/release-security-advisories.md")
    vulnerability_doc = read("docs/vulnerability-disclosure.md")
    signing_doc = read("docs/release-signing-operations.md")
    go_release_doc = read("docs/go-release-packaging.md")
    go_hardening_doc = read("docs/go-enforcement-production-hardening.md")
    enterprise_integration_doc = read("docs/enterprise-integration-validation.md")
    dashboard_doc = read("docs/community-release-readiness-dashboard.md")
    security_policy = read("SECURITY.md")
    release_security_workflow = read(".github/workflows/release-security.yml")
    go_release_workflow = read(".github/workflows/go-release.yml")
    package_script = read("scripts/package_go_release.py")
    release_verifier = read("scripts/verify-community-release-artifacts.py")
    release_security_validator = read("scripts/validate_release_security.py")
    boundary_script = read("scripts/validate-boundaries.sh")
    benchmark_test = read("go/cavra-runtime/runtime/decision_test.go")
    recurrence_cronjob = read("examples/kubernetes/cavra-recurrence-automation-cronjob.yaml")
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    wiki_home = read("docs/wiki/Home.md")
    inventory = read("docs/current-feature-inventory.md")
    wiki_inventory = read("docs/wiki/Current-Feature-Inventory.md")
    production_roadmap = read("docs/production-roadmap.md")
    next_slice = read("docs/roadmap-status-next-slice.md")
    audit_next_batch = read("docs/roadmap-status-audit-next-batch.md")

    for doc in [closeout_doc, wiki_doc]:
        for needle in [
            "performance",
            "concurrency",
            "backup",
            "restore",
            "upgrade",
            "migration",
            "SOC 2",
            "security advisory drill",
            "vulnerability response",
            "final release integrity",
            "SBOM",
            "SLSA provenance",
            "detached signatures",
            "GitHub keyless attestations",
            "BenchmarkEvaluateAllowCommand",
            "cavra ops backup",
            "cavra ops restore",
            "cavra evidence migrate",
            "cavra release verify-go-package",
            "cavra release verify-airgap-bundle",
            "cavra release validate-upgrade",
            "python scripts/validate-production-readiness-procurement-closeout.py",
            "bash scripts/validate-boundaries.sh .",
            "Public Boundary",
            "Operator Runbook",
            "User Stories",
            "Enterprise Challenge Solved",
        ]:
            require_phrase(doc, needle, "production readiness procurement closeout documentation", failures)
        require_phrase(doc, NEXT_RECOMMENDATION, "production closeout next recommendation", failures)

    procurement_lower = procurement_doc.lower()
    for needle in [
        "required buyer evidence",
        "soc 2 readiness roadmap",
        "security",
        "availability",
        "processing integrity",
        "confidentiality",
        "privacy",
        "procurement closeout checklist",
        "release integrity",
        "vulnerability response",
        "public-safe",
    ]:
        require(procurement_lower, needle, "procurement readiness documentation", failures)

    for needle in [
        "cavra ops stores",
        "cavra ops backup",
        "cavra ops restore",
        "SQLite backups use the SQLite backup API",
        "Retention Plan",
    ]:
        require(operations_doc, needle, "persistent API operations documentation", failures)

    for needle in [
        "cavra evidence migrate",
        "schema_migrations",
        "idempotent",
        "Production Path",
    ]:
        require(migrations_doc, needle, "migration documentation", failures)

    for doc, label in [
        (advisory_doc, "release security advisory documentation"),
        (security_policy, "security policy"),
        (vulnerability_doc, "vulnerability disclosure documentation"),
    ]:
        for needle in [
            "vulnerability",
            "advisory",
            "remediation",
            "verification",
        ]:
            require(doc.lower(), needle, label, failures)

    for needle in [
        "cavra-runtime.sbom.spdx.json",
        "cavra-runtime.provenance.intoto.json",
        "detached",
        "github-keyless-attestation.json",
        "cavra release verify-go-package",
        "cavra release validate-upgrade",
    ]:
        require(advisory_doc, needle, "advisory release integrity evidence", failures)

    for needle in [
        "cavra-runtime.signing-operations.json",
        "quarterly-key-rotation-policy",
        "emergency-revocation-evidence-required",
        "private keys",
    ]:
        require(signing_doc, needle, "release signing operations documentation", failures)

    for needle in [
        "SBOM",
        "SLSA provenance",
        "detached signatures",
        "GitHub OIDC-backed keyless attestations",
        "release-candidate upgrade validation",
    ]:
        require(go_release_doc, needle, "Go release packaging documentation", failures)

    for needle in ["BenchmarkEvaluateAllowCommand", "go test -bench BenchmarkEvaluateAllowCommand ./runtime"]:
        require(go_hardening_doc, needle, "Go hardening performance documentation", failures)
    require(benchmark_test, "BenchmarkEvaluateAllowCommand", "Go benchmark test", failures)

    for needle in ["concurrencyPolicy: Forbid", "CronJob"]:
        require(recurrence_cronjob, needle, "recurrence automation concurrency example", failures)

    for needle in [
        "GitHub App",
        "GitLab CI",
        "Azure DevOps",
        "SAML",
        "SIEM",
        "ITSM",
    ]:
        require(enterprise_integration_doc, needle, "Enterprise integration closeout dependency", failures)

    for needle in [
        "publication state",
        "verification packets",
        "ci evidence",
    ]:
        require(dashboard_doc.lower(), needle, "release readiness dashboard", failures)

    for needle in [
        "Release Security Readiness",
        "scripts/validate_release_security.py",
        "docs/release-security-advisories.md",
    ]:
        require(release_security_workflow, needle, "release security workflow", failures)

    for needle in [
        "actions/attest",
        "github-keyless-attestation.json",
        "python scripts/package_go_release.py",
    ]:
        require(go_release_workflow, needle, "Go release workflow integrity controls", failures)

    for needle in [
        "cavra-runtime.sbom.spdx.json",
        "cavra-runtime.provenance.intoto.json",
        "cavra-runtime.signing-operations.json",
        "offline-trust-root-bootstrap.json",
    ]:
        require(package_script, needle, "Go package release script", failures)

    for needle in ["pip", "sha256_match", "install_smoke"]:
        require(release_verifier, needle, "community release verifier", failures)

    for needle in ["SECURITY.md", "docs/release-security-advisories.md"]:
        require(release_security_validator, needle, "release security validator", failures)

    for needle in ["ENTERPRISE_PRIVATE_KEY", "LICENSE_SIGNING_KEY", "STRIPE_SECRET"]:
        require(boundary_script, needle, "boundary validator risky term coverage", failures)

    require(
        readme,
        "docs/production-readiness-procurement-closeout.md",
        "README production closeout link",
        failures,
    )
    require(
        changelog.lower(),
        "production readiness procurement closeout",
        "changelog entry",
        failures,
    )
    require(
        wiki_home,
        "Production-Readiness-Procurement-Closeout.md",
        "wiki production closeout link",
        failures,
    )
    for doc in [inventory, wiki_inventory]:
        require(
            doc,
            "Production readiness procurement closeout:",
            "feature inventory entry",
            failures,
        )
    for doc in [production_roadmap, next_slice, audit_next_batch]:
        require(
            doc,
            "Production readiness procurement closeout is documented",
            "roadmap delivered production closeout statement",
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
            "python scripts/validate-production-readiness-procurement-closeout.py",
            f"{workflow_path} validator wiring",
            failures,
        )

    if failures:
        print("CAVRA production readiness procurement closeout validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA production readiness procurement closeout validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
