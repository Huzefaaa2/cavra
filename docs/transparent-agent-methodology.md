# Transparent Agent Methodology

CAVRA uses transparent AI engineering agents to build and govern CAVRA itself. The model is not to simulate a large human team. The model is to make automation explicit, scoped, reviewable, and auditable.

Positioning statement:

> CAVRA is a runtime authority layer for transparent AI engineering teams. It turns issues into branches, code, tests, security reviews, documentation, evidence, and release notes through specialized agents governed by policy.

## Operating Principle

Every automated contributor must be identifiable as automation. Bot identities such as `cavra-backend[bot]`, `cavra-security[bot]`, and `cavra-docs[bot]` are acceptable because the identity, permissions, and audit trail are explicit.

Fake human developer identities are prohibited. GitHub contribution graphs, commit history, reviews, and authorship are trust signals. CAVRA must preserve those trust signals by clearly labeling automated work.

## CAVRA Agent Roles

| Role | Primary responsibility | Typical branch |
| --- | --- | --- |
| Product Manager Agent | Converts product intent into issues, user stories, acceptance criteria, and enterprise challenge mapping. | `agent/product/{issue-slug}` |
| Architect Agent | Reviews runtime boundaries, policy model, API contracts, C4 diagrams, and technical debt. | `agent/architect/{issue-slug}` |
| Backend Agent | Implements CLI, API, policy engine, runtime guards, evidence, and integrations. | `agent/backend/{issue-slug}` |
| Frontend Agent | Builds sandbox UI, developer console surfaces, and guided demos. | `agent/frontend/{issue-slug}` |
| Test Agent | Adds unit, integration, CLI, policy, evidence, and regression tests. | `agent/tests/{issue-slug}` |
| Security Agent | Reviews secrets, dependencies, workflow permissions, policy bypasses, and supply-chain risk. | `agent/security/{issue-slug}` |
| Documentation Agent | Updates README, docs, diagrams, wiki pages, user stories, and white paper. | `agent/docs/{issue-slug}` |
| Reviewer Agent | Reviews pull requests for correctness, maintainability, evidence quality, and architecture alignment. | `agent/reviewer/{issue-slug}` |
| Release Agent | Prepares changelog, release notes, versioning, release evidence, and documentation status. | `agent/release/{issue-slug}` |

Declarative manifests live in `.github/agents/`. Each manifest defines the agent identity, allowed triggers, allowed paths, branch patterns, human approval gates, prohibited actions, and evidence required.

## GitHub App Model

Production use should create one GitHub App per role. Each app gets narrowly scoped permissions and a clear bot identity:

- `cavra-product-manager[bot]`
- `cavra-architect[bot]`
- `cavra-backend[bot]`
- `cavra-frontend[bot]`
- `cavra-test[bot]`
- `cavra-security[bot]`
- `cavra-docs[bot]`
- `cavra-reviewer[bot]`
- `cavra-release[bot]`

GitHub Actions can route events, validate manifests, and publish governance summaries. A separate orchestrator service can later decide which agent should act, but it must still obey CAVRA policies, protected branches, required reviews, and release approvals.

## Delivery Lifecycle

1. A human owner or product agent opens an issue with acceptance criteria.
2. The Product Manager Agent clarifies user stories and enterprise value.
3. The Architect Agent reviews the proposed design and affected controls.
4. A developer agent creates a branch using `agent/{role}/{issue-slug}`.
5. CAVRA evaluates file, command, Git, MCP, and policy actions before execution.
6. The Test Agent adds focused validation and records commands.
7. The Security Agent reviews workflow permissions, secrets risk, dependencies, and bypass paths.
8. The Documentation Agent updates README, docs, wiki-ready pages, diagrams, user stories, and challenge mapping.
9. The Reviewer Agent comments on correctness and residual risk.
10. A human maintainer approves and merges.
11. The Release Agent prepares release notes, changelog entries, evidence bundles, and wiki updates.

## Authorship and Branch Rules

Branches must be descriptive and transparent:

```text
agent/backend/evidence-exporters
agent/security/workflow-permissions
agent/docs/approval-router-guide
```

Commits should identify the bot:

```text
Author: cavra-backend[bot] <cavra-backend[bot]@users.noreply.github.com>
Co-authored-by: Huzefa Husain <maintainer-email>
```

Co-authorship should be used only when a real human materially contributed or directed a specific change. It must not be used to fabricate team size.

## Required Evidence

Every agent-delivered PR should include:

- Linked issue and assigned agent role.
- Branch name and bot identity.
- Changed files and scope boundaries.
- CAVRA policy impact.
- Tests or validation commands.
- Security review status.
- Documentation, README, wiki, and diagram update status.
- Human approval references for protected actions.

The policy pack `policies/cavra-agentic-delivery` captures these requirements as CAVRA runtime governance.

## Acceptable Automation

- Transparent GitHub Apps or bot accounts.
- Bot-authored branches, commits, PRs, and comments.
- Role-specific permissions and audit trails.
- CAVRA evidence bundles and PR attestations.
- Human approvals for protected branches, security settings, releases, and policy relaxations.

## Prohibited Automation

- Fake human identities.
- Misleading commit authorship.
- Self-approval or autonomous merge to protected branches.
- Disabling CodeQL, Dependabot, secret scanning, branch protection, or required review.
- Hiding that AI generated or reviewed a change.
- Publishing releases without human approval.

## Enterprise Value

This model shows enterprises how CAVRA can govern autonomous engineering rather than merely describe it. It addresses the core concerns buyers raise about AI coding agents:

- Who acted?
- What changed?
- Was the action allowed before it happened?
- Which policy approved or blocked it?
- Was a human approval required?
- Were tests, security, and documentation completed?
- Can audit, compliance, or change management reconstruct the decision?

By using transparent agents inside its own repository, CAVRA demonstrates the operating model it sells: agentic engineering with authority, evidence, and trust.
