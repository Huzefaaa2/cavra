# AI Agent Enforcement And Anti-Bypass Model

CAVRA must be enforced at trusted engineering boundaries, not only inside an AI coding agent prompt or local wrapper. An agent can ignore local instructions if it has raw shell, Git, cloud, or API credentials. The production model is layered: CAVRA guides agents before action, and repository, CI, runner, package, and deployment controls reject work that lacks valid CAVRA evidence.

## Required Position

Defensible claim:

> AI agents may choose whether to cooperate locally, but protected branches, required checks, governed runners, and deployment gates must reject unverified work that did not pass through CAVRA.

Non-defensible claim:

> No agent can bypass CAVRA anywhere.

That is only true in a fully controlled environment where the agent has no direct credentials, no unrestricted shell, no unmanaged network path, no direct repository write access, and no ability to disable policy gates.

## Enforcement Layers

| Layer | Goal | CAVRA control |
| --- | --- | --- |
| Agent adapter | Encourage pre-action evaluation | Claude Code/Codex/MCP wrappers call CAVRA before file, command, Git, and MCP actions. |
| Local runtime | Reduce accidental bypass | Go/Python runtime guard, daemon mode, command wrappers, policy packs, and evidence generation. |
| Git identity | Prevent anonymous automation | Transparent bot identities, `.github/agents/` manifests, branch naming, signed commits where available. |
| Pull request | Block ungoverned changes | PR template, CAVRA attestation, required review, CODEOWNERS, docs and test evidence. |
| Branch protection | Enforce merge boundary | Required `cavra-required-check`, required reviews, stale review dismissal, no direct push, no force push, no bypass. |
| CI runner | Re-evaluate in trusted automation | Required workflow verifies policy, evidence, PR attestation, tests, and boundary rules. |
| Release/package | Prevent unverified artifacts | Signed release package, SBOM, provenance, release evidence, keyless attestations. |
| Deployment | Prevent unverified rollout | Environment protection, deployment approvals, rollout evidence, immutable evidence storage. |

## Minimum GitHub Enforcement Baseline

- Require pull request before merge.
- Require at least one non-author review.
- Dismiss stale approvals when new commits are pushed.
- Require conversation resolution.
- Require CodeQL or equivalent security checks.
- Require `cavra-required-check`.
- Restrict who can push to protected branches.
- Disable force pushes and branch deletion.
- Enable **Do not allow bypassing the above settings** where available.
- Bind required status checks to the expected GitHub App or workflow source when supported.

## Bypass Scenarios

| Bypass attempt | Expected result |
| --- | --- |
| Agent edits files without calling local CAVRA | PR fails because `cavra-required-check` cannot verify evidence. |
| Agent pushes directly to `main` | Branch protection rejects the push. |
| Agent opens PR without attestation | Required check fails. |
| Agent disables workflow or required check | Permission model blocks it; security monitoring alerts if an admin changes it. |
| Agent uses a personal access token | Token lacks protected-branch, ruleset, secret, and workflow-admin permissions. |
| Agent modifies CAVRA policy to allow itself | CODEOWNERS, required review, and policy-relaxation approval block merge. |

## Product Requirement

This is required for CAVRA to be credible as an enterprise AI-agent governance product.

Community Edition should provide required-check templates, agent manifests, PR attestation, evidence verification, public-safe policies, and protected-branch documentation.

Enterprise Edition should later add central agent registry enforcement, hosted policy decisions, organization-wide rollout, SIEM bypass alerts, managed runner enforcement, and SaaS dashboards for non-compliant repositories.

## Automated Readiness Report

CAVRA includes an automated **agent enforcement readiness report**:

```bash
cavra agent enforcement-readiness --json
```

The API exposes the same report:

```text
GET /agents/enforcement-readiness
```

Use `--settings agent-enforcement-settings.json` or `CAVRA_AGENT_ENFORCEMENT_SETTINGS` to include exported branch protection, required checks, and security checks. The report verifies required-check workflow coverage, agent manifests, PR template evidence language, CODEOWNERS, agentic-delivery policies, branch protection expectations, security checks, and risky workflow permission patterns.
