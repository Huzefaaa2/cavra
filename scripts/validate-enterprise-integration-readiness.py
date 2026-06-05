#!/usr/bin/env python3
"""Validate public-safe Enterprise integration readiness coverage."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEXT_RECOMMENDATION = (
    "Start Community v1.0.0 stabilization planning from the completed Node 24 "
    "readiness baseline with release signing, reproducible provenance, "
    "GA announcement readiness, and final operator evidence."
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
        "docs/enterprise-integration-validation.md",
        "docs/wiki/Enterprise-Integration-Validation.md",
        "docs/agent-orchestration-architecture.md",
        "docs/integrations.md",
        "docs/connector-execution-hooks.md",
        "docs/oidc-rbac-deployment.md",
        ".github/workflows/agent-orchestrator.yml",
        ".github/workflows/cavra-governance.yml",
        "examples/github-actions/cavra-required-check.yml",
        "examples/gitlab-ci/cavra-required-check.gitlab-ci.yml",
        "examples/gitlab-ci/cavra-release-governance-go-runtime.gitlab-ci.yml",
        "examples/azure-pipelines/cavra-required-check.azure-pipelines.yml",
        "examples/azure-pipelines/cavra-release-governance-go-runtime.azure-pipelines.yml",
        "examples/connectors/cavra-connectors.example.json",
        "examples/identity/entra-id-oidc-rbac/README.md",
        "examples/identity/okta-oidc-rbac/README.md",
        "scripts/validate-enterprise-integration-readiness.py",
    ]
    for path in required_files:
        require_file(path, failures)

    agent_manifests = sorted((ROOT / ".github/agents").glob("*.yml"))
    if not agent_manifests:
        failures.append("missing transparent agent manifests under .github/agents")

    if failures:
        for failure in failures:
            print(failure)
        return 1

    validation_doc = read("docs/enterprise-integration-validation.md")
    wiki_doc = read("docs/wiki/Enterprise-Integration-Validation.md")
    orchestration_doc = read("docs/agent-orchestration-architecture.md")
    integrations_doc = read("docs/integrations.md")
    connector_doc = read("docs/connector-execution-hooks.md")
    identity_doc = read("docs/oidc-rbac-deployment.md")
    orchestrator_workflow = read(".github/workflows/agent-orchestrator.yml")
    governance_workflow = read(".github/workflows/cavra-governance.yml")
    github_required = read("examples/github-actions/cavra-required-check.yml")
    gitlab_required = read("examples/gitlab-ci/cavra-required-check.gitlab-ci.yml")
    gitlab_go = read("examples/gitlab-ci/cavra-release-governance-go-runtime.gitlab-ci.yml")
    azure_required = read("examples/azure-pipelines/cavra-required-check.azure-pipelines.yml")
    azure_go = read("examples/azure-pipelines/cavra-release-governance-go-runtime.azure-pipelines.yml")
    connectors = read("examples/connectors/cavra-connectors.example.json")
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    wiki_home = read("docs/wiki/Home.md")
    inventory = read("docs/current-feature-inventory.md")
    wiki_inventory = read("docs/wiki/Current-Feature-Inventory.md")
    production_roadmap = read("docs/production-roadmap.md")
    next_slice = read("docs/roadmap-status-next-slice.md")
    audit_next_batch = read("docs/roadmap-status-audit-next-batch.md")

    for doc in [validation_doc, wiki_doc]:
        for needle in [
            "GitHub App",
            "orchestrator",
            "GitLab CI",
            "Azure DevOps",
            "Azure Pipelines",
            "SAML",
            "OIDC/RBAC",
            "SIEM",
            "ITSM",
            "Splunk",
            "Microsoft Sentinel",
            "Datadog",
            "Jira",
            "ServiceNow",
            "public-safe",
            "provider credentials",
            "customer data",
            "Enterprise source code",
            "Validation Command",
            "Operator Runbook",
            "Public Boundary",
            "User Stories",
            "Enterprise Challenge Solved",
            "python scripts/validate-enterprise-integration-readiness.py",
            ".github/workflows/agent-orchestrator.yml",
            ".github/workflows/cavra-governance.yml",
            "examples/gitlab-ci/cavra-required-check.gitlab-ci.yml",
            "examples/azure-pipelines/cavra-required-check.azure-pipelines.yml",
            "examples/connectors/cavra-connectors.example.json",
        ]:
            require(doc, needle, "Enterprise integration documentation", failures)
        require_phrase(doc, NEXT_RECOMMENDATION, "Enterprise integration next recommendation", failures)

    for needle in [
        "GitHub-native delivery loop",
        "The orchestrator should not own policy decisions",
        "protected branches",
        "required CAVRA checks",
        "PR attestation",
        ".github/agents/",
    ]:
        require(orchestration_doc, needle, "agent orchestration documentation", failures)

    for manifest in agent_manifests:
        text = manifest.read_text(encoding="utf-8")
        for needle in [
            "bot_identity:",
            "allowed_branch_patterns:",
            "required_checks:",
            "prohibited_actions:",
            "evidence_required:",
        ]:
            require(text, needle, f"{manifest} transparent agent manifest", failures)

    for needle in [
        "GitHub App orchestrator",
        "GitLab CI",
        "Azure Pipelines",
        "Microsoft Sentinel",
        "Splunk",
        "Datadog",
        "ServiceNow",
        "Jira",
        "SAML",
        "RBAC",
        "live connector execution hooks",
    ]:
        require(integrations_doc, needle, "integration documentation", failures)

    for needle in [
        "Splunk HEC",
        "Microsoft Sentinel",
        "Datadog Logs",
        "Jira issue API",
        "ServiceNow change request API",
        "redacted delivery evidence",
        "As a SOC analyst",
        "As a change manager",
    ]:
        require(connector_doc, needle, "connector execution documentation", failures)

    for needle in ["Microsoft Entra ID", "Okta", "OIDC", "RBAC"]:
        require(identity_doc, needle, "identity reference documentation", failures)

    for needle in [
        "transparent agent manifests",
        "Actual autonomous GitHub App execution",
        "human-gated for protected actions",
    ]:
        require(orchestrator_workflow, needle, "agent orchestrator workflow", failures)

    for needle in [
        "cavra-required-check",
        "python scripts/validate-enterprise-integration-readiness.py",
        "go test ./...",
        "pytest -q",
        "evidence verify-attestation",
    ]:
        require(governance_workflow, needle, "governance workflow integration", failures)

    for doc, label in [
        (github_required, "GitHub required check example"),
        (gitlab_required, "GitLab required check example"),
        (azure_required, "Azure required check example"),
    ]:
        for needle in [
            "cavra-required-check",
            "evidence bundle",
            "evidence verify",
            "evidence verify-attestation",
        ]:
            require(doc, needle, label, failures)

    for needle in [
        "release-governance",
        "id_tokens",
        "CAVRA_GITLAB_OIDC_TOKEN",
        "daemon",
        "evidence",
    ]:
        require(gitlab_go, needle, "GitLab Go release governance example", failures)

    for needle in [
        "Azure Pipelines",
        "release-governance",
        "daemon",
        "evidence",
        "PublishPipelineArtifact",
    ]:
        require(azure_go, needle, "Azure Go release governance example", failures)

    for needle in [
        "splunk",
        "sentinel",
        "datadog",
        "jira",
        "servicenow",
        "token_env",
        "url_env",
    ]:
        require(connectors.lower(), needle, "connector example", failures)

    require(
        readme,
        "docs/enterprise-integration-validation.md",
        "README Enterprise integration validation link",
        failures,
    )
    require(changelog, "Enterprise integration validation", "changelog entry", failures)
    require(
        wiki_home,
        "Enterprise-Integration-Validation.md",
        "wiki Enterprise integration validation link",
        failures,
    )
    for doc in [inventory, wiki_inventory]:
        require(
            doc,
            "Enterprise integration validation:",
            "feature inventory entry",
            failures,
        )
    for doc in [production_roadmap, next_slice, audit_next_batch]:
        require(
            doc,
            "Enterprise integration validation is documented",
            "roadmap delivered Enterprise integration statement",
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
            "python scripts/validate-enterprise-integration-readiness.py",
            f"{workflow_path} validator wiring",
            failures,
        )

    if failures:
        print("CAVRA enterprise integration validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA enterprise integration validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
