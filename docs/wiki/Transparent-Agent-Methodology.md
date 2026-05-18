# Transparent Agent Methodology

CAVRA uses transparent AI engineering agents to build and govern CAVRA itself. The goal is not to make the repository look like many humans are working. The goal is to show an auditable AI delivery team where every automated action is clearly identified, scoped, reviewed, and governed.

## Agent Roles

- Product Manager Agent: issues, user stories, acceptance criteria, enterprise challenge mapping.
- Architect Agent: design review, runtime boundaries, policy model, technical debt.
- Backend Agent: CLI, API, policy engine, runtime guards, evidence, integrations.
- Frontend Agent: sandbox UI, console surfaces, demos.
- Test Agent: unit, integration, CLI, policy, evidence, and regression tests.
- Security Agent: secrets, dependencies, CI permissions, policy bypasses, supply-chain risk.
- Documentation Agent: README, docs, diagrams, wiki, user stories, white paper.
- Reviewer Agent: PR review for correctness, maintainability, evidence, architecture alignment.
- Release Agent: changelog, release notes, versioning, release evidence, documentation status.

## Rules

- Use transparent bot identities such as `cavra-backend[bot]`.
- Use branches such as `agent/backend/evidence-exporters`.
- Link each PR to an issue and acceptance criteria.
- Include CAVRA policy impact, test results, documentation status, and evidence.
- Require human approval for protected branches, security settings, policy relaxations, and releases.
- Do not create fake human identities or misleading authorship.

## Enterprise Value

This model demonstrates CAVRA's core promise: enterprises can adopt autonomous coding agents without losing control over identity, authorization, evidence, approvals, and audit.

See repository source page: `docs/transparent-agent-methodology.md`.
