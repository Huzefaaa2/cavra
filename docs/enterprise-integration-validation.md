# Enterprise Integration Validation

This public-safe release gate ties CAVRA's public Enterprise integration readiness claims
to concrete Community repository artifacts. It validates that GitHub
App/orchestrator governance, GitLab CI parity, Azure DevOps parity, SAML
identity readiness, and SIEM/ITSM workflow evidence are documented without
placing Enterprise source code, provider credentials, customer data, or private
connector implementation in the public repository.

## Validation Command

Run the validator from the repository root:

```bash
python scripts/validate-enterprise-integration-readiness.py
```

Expected success output:

```text
CAVRA enterprise integration validation passed.
```

## Integration Readiness Matrix

| Area | Public Control | Evidence Artifact |
| --- | --- | --- |
| GitHub App and orchestrator production hardening | `.github/workflows/agent-orchestrator.yml` validates transparent agent manifests and keeps autonomous GitHub App execution human-gated for protected actions. | `docs/agent-orchestration-architecture.md`, `.github/agents/*.yml`, and the orchestrator workflow summary. |
| GitHub required check | `cavra-required-check` runs policy validation, tests, release validators, Go tests, evidence bundle generation, and PR attestation verification before protected merges. | `.github/workflows/cavra-governance.yml` and `examples/github-actions/cavra-required-check.yml`. |
| GitLab parity | GitLab CI templates verify policy packs, signed evidence bundles, and PR attestation artifacts with the same governance intent as GitHub required checks. | `examples/gitlab-ci/cavra-required-check.gitlab-ci.yml` and `examples/gitlab-ci/cavra-release-governance-go-runtime.gitlab-ci.yml`. |
| Azure DevOps parity | Azure Pipelines templates support Azure Repos Build validation branch policies and publish CAVRA evidence artifacts. | `examples/azure-pipelines/cavra-required-check.azure-pipelines.yml` and `examples/azure-pipelines/cavra-release-governance-go-runtime.azure-pipelines.yml`. |
| SAML identity readiness | SAML is documented as an Enterprise identity boundary. Community publishes OIDC/RBAC reference patterns and the claim-mapping requirements a private SAML bridge must satisfy. | `docs/oidc-rbac-deployment.md`, `examples/identity/entra-id-oidc-rbac/`, `examples/identity/okta-oidc-rbac/`, and this page. |
| SIEM workflow evidence | CAVRA exports provider-shaped SIEM payloads for Splunk, Microsoft Sentinel, Datadog, and generic webhooks with redacted delivery evidence. | `docs/connector-execution-hooks.md`, `docs/integrations.md`, and `examples/connectors/cavra-connectors.example.json`. |
| ITSM workflow evidence | Jira and ServiceNow request specs and delivery hooks are documented for change-management handoff without embedding live provider secrets. | `docs/connector-execution-hooks.md`, `docs/implementation-guide.md`, and `examples/connectors/cavra-connectors.example.json`. |

## Operator Runbook

1. Confirm GitHub protected branches require `cavra-required-check` and human
   maintainer review for protected actions.
2. Run the orchestrator workflow in manifest-only mode and confirm every
   declared agent has a bot identity, branch pattern, allowed paths, required
   checks, prohibited actions, and evidence requirements.
3. Run the GitHub Actions, GitLab CI, and Azure Pipelines required-check
   templates in non-production repositories and confirm each publishes CAVRA
   evidence artifacts.
4. Configure identity through Entra ID or Okta OIDC/RBAC references for
   Community deployments. For Enterprise SAML, map SAML assertions into the
   same actor, group, repository, and approval claims before CAVRA approval
   decisions are evaluated.
5. Test SIEM connector delivery with non-sensitive synthetic events for
   Splunk, Microsoft Sentinel, Datadog, or a generic webhook.
6. Test ITSM handoff with Jira or ServiceNow sandbox endpoints using
   redacted request evidence and no live customer records.
7. Run `python scripts/validate-enterprise-integration-readiness.py` before
   claiming Enterprise integration readiness in release notes, demos, or
   procurement material.

## Public Boundary

This page documents public-safe Community Edition integration readiness only. It
does not include Enterprise source code, private GitHub App service code, SAML
bridge implementation, production SIEM connectors, production ITSM connectors,
provider credentials, customer records, provider tenant identifiers, private
policy packs, commercial dashboard code, or SaaS backend code.

Enterprise implementations should connect through documented extension points:
GitHub App webhooks, CI required checks, SAML-to-OIDC/RBAC claim mapping,
connector configuration, evidence bundle verification, and private packages or
services outside this public repository.

## User Stories

- As a GitHub Enterprise administrator, I can prove CAVRA required checks and
  transparent agent manifests gate protected repository actions.
- As a platform team, I can use equivalent GitHub, GitLab, and Azure DevOps
  CI/CD controls without rewriting CAVRA policy logic.
- As an identity owner, I can see how Enterprise SAML must map into CAVRA
  approval claims without exposing IdP certificates or private configuration.
- As a SOC analyst, I can receive SIEM-ready CAVRA evidence for blocked or
  approved AI-agent actions.
- As a change manager, I can connect approvals and release governance events
  to Jira or ServiceNow while preserving redacted audit evidence.

## Enterprise Challenge Solved

Enterprise buyers rarely approve AI-agent governance products that work only in
one source-control system or only as a standalone scanner. This gate makes
CAVRA integration readiness inspectable across repository governance, CI/CD,
identity, SOC operations, and change management while keeping paid connectors
and customer-specific deployment logic out of the public Community repository.

## Next Recommendation

Archive the post-publication Community v0.1.1 verifier output and begin the
next maintenance-release readiness slice.
