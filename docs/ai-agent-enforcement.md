# AI Agent Enforcement And Anti-Bypass Model

CAVRA must be enforced at trusted engineering boundaries, not only inside the AI coding agent prompt or local wrapper. An agent can ignore instructions if it has raw shell, Git, cloud, or API credentials. The production model is therefore layered: CAVRA should guide agents before action, and repository, CI, runner, package, and deployment controls must reject work that does not carry valid CAVRA evidence.

## Research Summary

Current platform and supply-chain guidance supports this model:

- GitHub branch protection and rulesets can require pull requests, reviews, required status checks, signed commits, conversation resolution, deployment success, restricted pushes, and no bypass for administrators or roles with bypass permission.
- GitHub required status checks can be bound to a specific GitHub App as the expected source, reducing the risk of an arbitrary actor spoofing a status name.
- SLSA source requirements describe the source-control system as the trusted foundation for authentication, authorization, change management, mandatory reviews, and passing status checks before protected branches advance.
- OPA CI/CD guidance supports policy-as-code checks inside pull request workflows and a summary required check that branch protection can enforce.

Sources:

- GitHub protected branches: `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches`
- SLSA source requirements: `https://slsa.dev/spec/v1.2/source-requirements`
- OPA pull request check policies: `https://www.openpolicyagent.org/docs/cicd/pr-checks`
- OPA in CI/CD: `https://www.openpolicyagent.org/docs/cicd`

## Required Position

CAVRA should be documented and sold as an enforcement architecture, not as an optional agent plugin.

The defensible claim is:

> AI agents may choose whether to cooperate locally, but protected branches, required checks, governed runners, and deployment gates must reject unverified work that did not pass through CAVRA.

The non-defensible claim is:

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
| CI runner | Re-evaluate in trusted automation | CAVRA required-check workflow verifies policy, evidence, PR attestation, tests, and boundary rules. |
| Release/package | Prevent unverified artifacts | Signed release package, SBOM, provenance, release evidence, keyless attestations. |
| Deployment | Prevent unverified rollout | Environment protection, deployment approvals, rollout evidence, immutable evidence storage. |

## Minimum GitHub Enforcement Baseline

For repositories that use AI coding agents, configure `main` and release branches with:

- Require pull request before merge.
- Require at least one non-author review.
- Dismiss stale approvals when new commits are pushed.
- Require conversation resolution.
- Require CodeQL or equivalent security checks.
- Require `cavra-required-check`.
- Require branch to be up to date before merge for high-risk repositories.
- Restrict who can push to protected branches.
- Disable force pushes and branch deletion.
- Enable **Do not allow bypassing the above settings** where available.
- Bind required status checks to the expected GitHub App or workflow source when the platform supports it.

For GitLab and Azure DevOps, use equivalent protected branch, merge request approval, required pipeline, and build validation policies.

## CAVRA Required Check Contract

The required check should fail unless it can verify:

- The PR has a CAVRA attestation.
- The actor or bot identity is declared in `.github/agents/` or the enterprise agent registry.
- Branch naming matches an approved agent or human workflow.
- Policy packs validate and compile.
- High-risk changes have approval evidence.
- Protected files, workflow changes, policy relaxations, release settings, and security settings have required reviewers.
- Evidence bundle exists, verifies, and is uploaded as a CI artifact.
- The run happened in an approved CI runner context with OIDC or signed runner claims when configured.

## Anti-Bypass Controls

CAVRA should explicitly recommend these controls:

- Do not give AI agents direct write access to protected branches.
- Do not give AI agents repository admin permission.
- Do not give AI agents tokens that can edit branch protection, rulesets, workflow permissions, secrets, environments, or required checks.
- Do not let agents approve their own PRs or dismiss blocking reviews.
- Use short-lived OIDC credentials instead of long-lived tokens.
- Use environment-specific least-privilege credentials.
- Keep cloud deployment credentials out of agent workstations.
- Require CI-generated evidence for merge, release, and deployment.
- Alert on branch protection changes, required-check removal, workflow permission expansion, and secret changes.

## Bypass Scenarios And Response

| Bypass attempt | Expected result |
| --- | --- |
| Agent edits files without calling local CAVRA | PR fails because `cavra-required-check` cannot verify evidence. |
| Agent pushes directly to `main` | Branch protection rejects the push. |
| Agent opens PR without attestation | Required check fails. |
| Agent disables workflow or required check | Repository permission model blocks it; security monitoring alerts if an admin changes it. |
| Agent uses a personal access token | Token should lack protected-branch, ruleset, secret, and workflow-admin permissions. |
| Agent uses local shell to run cloud commands | Cloud IAM and deployment gates should require separate approved identities and evidence. |
| Agent modifies CAVRA policy to allow itself | CODEOWNERS, required review, and policy-relaxation approval block merge. |

## Product Requirement

This feature is required for CAVRA to be credible as an enterprise AI-agent governance product.

Community Edition should provide:

- Required-check templates.
- Agent manifests.
- PR attestation generation and verification.
- Public-safe policy packs.
- Documentation for protected branches and CI enforcement.

Enterprise Edition should later add:

- Central agent registry and tenant policies.
- Enforced agent identity binding.
- Hosted policy decision service.
- Organization-wide required-check rollout.
- SIEM alerts for bypass attempts.
- Managed runner enforcement.
- SaaS dashboards for non-compliant repositories.

## Implementation Status

Implemented today:

- Transparent agent methodology.
- Agent orchestration architecture.
- Agent manifests under `.github/agents/`.
- `cavra-required-check` workflow.
- GitHub/GitLab/Azure DevOps required-check templates.
- PR attestation and evidence bundle workflows.
- Runner authentication and evidence key custody guidance.

Newly documented in this page:

- The anti-bypass architecture.
- Minimum enforcement baseline.
- Bypass scenarios and expected controls.
- Product requirement split between Community and Enterprise.

## Automated Readiness Report

CAVRA now includes an automated **agent enforcement readiness report** that inspects repository enforcement files and optional exported platform settings:

```bash
cavra agent enforcement-readiness --json
```

The API exposes the same report:

```text
GET /agents/enforcement-readiness
```

For provider-side controls that cannot be trusted from local files alone, pass a JSON export with branch protection, required checks, and security checks:

```bash
cavra agent enforcement-readiness --settings agent-enforcement-settings.json --json
```

Or set:

```bash
export CAVRA_AGENT_ENFORCEMENT_SETTINGS=agent-enforcement-settings.json
```

The report checks:

- required `cavra-required-check` workflow and evidence artifact;
- declared transparent agent manifests;
- PR template and CODEOWNERS coverage;
- `cavra-agentic-delivery` policy pack presence;
- exported branch protection controls for reviews, stale approval dismissal, conversation resolution, restricted pushes, force-push prevention, deletion prevention, and bypass prevention;
- exported required status checks and security checks;
- risky workflow permission patterns such as `permissions: write-all`.

This is a Community Edition control. Enterprise Edition should later add organization-wide collection, provider API ingestion, SIEM alerts, drift detection, and centrally enforced agent registry policy.
