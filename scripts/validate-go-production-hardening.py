#!/usr/bin/env python3
"""Validate Go enforcement-plane production hardening coverage."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEXT_RECOMMENDATION = (
    "Prepare Community v0.1.3 maintenance planning and GitHub Actions Node 24 "
    "readiness."
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
        "docs/go-enforcement-production-hardening.md",
        "docs/wiki/Go-Enforcement-Production-Hardening.md",
        "docs/go-daemon-transport.md",
        "docs/go-reproducible-airgap-builds.md",
        "docs/go-release-packaging.md",
        "docs/go-backend-deployment-readiness.md",
        "docs/go-enforcement-roadmap.md",
        "go/cavra-runtime/README.md",
        "go/cavra-runtime/runtime/decision_test.go",
        "go/cavra-runtime/daemon/client.go",
        "go/cavra-runtime/daemon/server.go",
        "go/cavra-runtime/cmd/cavra-runtime/main.go",
        ".github/workflows/go-release.yml",
        "scripts/package_go_release.py",
        "scripts/validate-go-production-hardening.py",
    ]
    for path in required_files:
        require_file(path, failures)

    if failures:
        for failure in failures:
            print(failure)
        return 1

    hardening_doc = read("docs/go-enforcement-production-hardening.md")
    wiki_doc = read("docs/wiki/Go-Enforcement-Production-Hardening.md")
    daemon_doc = read("docs/go-daemon-transport.md")
    airgap_doc = read("docs/go-reproducible-airgap-builds.md")
    release_doc = read("docs/go-release-packaging.md")
    deployment_doc = read("docs/go-backend-deployment-readiness.md")
    roadmap_doc = read("docs/go-enforcement-roadmap.md")
    runtime_readme = read("go/cavra-runtime/README.md")
    decision_tests = read("go/cavra-runtime/runtime/decision_test.go")
    workflow = read(".github/workflows/go-release.yml")
    package_script = read("scripts/package_go_release.py")
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    wiki_home = read("docs/wiki/Home.md")
    inventory = read("docs/current-feature-inventory.md")
    wiki_inventory = read("docs/wiki/Current-Feature-Inventory.md")
    production_roadmap = read("docs/production-roadmap.md")
    next_slice = read("docs/roadmap-status-next-slice.md")
    audit_next_batch = read("docs/roadmap-status-audit-next-batch.md")

    for doc in [hardening_doc, wiki_doc]:
        for needle in [
            "Unix-socket",
            "gRPC",
            "air-gapped",
            "reproducibility",
            "upgrade validation",
            "performance",
            "operational readiness",
            "Validation Command",
            "Operator Runbook",
            "Public Boundary",
            "User Stories",
            "Enterprise Challenge Solved",
            "python scripts/validate-go-production-hardening.py",
            "go test ./...",
            "go test -bench BenchmarkEvaluateAllowCommand ./runtime",
            "go run ./cmd/cavra-runtime --lifecycle start",
            "go run ./cmd/cavra-runtime --lifecycle status",
            "go run ./cmd/cavra-runtime --lifecycle stop",
            "cavra release verify-airgap-bundle",
            "cavra release validate-upgrade",
            "cavra release verify-go-package",
            "BenchmarkEvaluateAllowCommand",
            "Python remains authoritative",
            "Enterprise source code",
        ]:
            require(doc, needle, "Go production hardening documentation", failures)
        require_phrase(doc, NEXT_RECOMMENDATION, "Go hardening next recommendation", failures)

    for doc, label in [
        (daemon_doc, "daemon transport documentation"),
        (runtime_readme, "Go runtime README"),
    ]:
        for needle in [
            "Unix-socket",
            "gRPC",
            "BenchmarkEvaluateAllowCommand",
            "go test -bench",
            "operational readiness",
        ]:
            require(doc, needle, label, failures)

    for doc, label in [
        (airgap_doc, "air-gapped reproducibility documentation"),
        (release_doc, "Go release packaging documentation"),
    ]:
        for needle in [
            "air-gapped",
            "reproducibility",
            "cavra release verify-airgap-bundle",
            "cavra release validate-upgrade",
            "cavra-runtime.reproducibility.json",
        ]:
            require(doc, needle, label, failures)

    for needle in [
        "CI runner bundle metadata",
        "workstation channel manifest",
        "updater policy",
    ]:
        require(deployment_doc, needle, "Go deployment readiness documentation", failures)

    for needle in [
        "BenchmarkEvaluateAllowCommand",
        "b.N",
        "terraform plan",
    ]:
        require(decision_tests, needle, "Go performance benchmark", failures)

    for needle in [
        "CGO_ENABLED=0",
        "-trimpath",
        "python scripts/package_go_release.py",
        "cavra-go-runtime-${version}.zip",
        "actions/attest",
    ]:
        require(workflow, needle, "Go release workflow", failures)

    for needle in [
        "reproducibility",
        "airgap",
        "cavra-runtime.reproducibility.json",
        "offline-trust-root-bootstrap.json",
    ]:
        require(package_script, needle, "Go package script controls", failures)

    require(
        roadmap_doc,
        "Go enforcement production hardening is documented",
        "Go roadmap delivered statement",
        failures,
    )
    require(readme, "docs/go-enforcement-production-hardening.md", "README Go hardening link", failures)
    require(changelog, "Go enforcement production hardening", "changelog entry", failures)
    require(
        wiki_home,
        "Go-Enforcement-Production-Hardening.md",
        "wiki Go hardening link",
        failures,
    )
    for doc in [inventory, wiki_inventory]:
        require(doc, "Go enforcement production hardening:", "feature inventory entry", failures)
    for doc in [production_roadmap, next_slice, audit_next_batch]:
        require(
            doc,
            "Go enforcement production hardening is documented",
            "roadmap delivered Go hardening statement",
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
            "python scripts/validate-go-production-hardening.py",
            f"{workflow_path} validator wiring",
            failures,
        )

    if failures:
        print("CAVRA Go production hardening validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA Go production hardening validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
