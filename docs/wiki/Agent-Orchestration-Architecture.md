# Agent Orchestration Architecture

CAVRA's transparent engineering agents operate through GitHub while CAVRA remains the runtime authority for file, command, Git, MCP, policy, evidence, and approval decisions.

## Delivery Loop

1. Human owner or Product Manager Agent opens an issue.
2. Architect Agent reviews design and control impact.
3. Backend or Frontend Agent implements on an `agent/{role}/{issue-slug}` branch.
4. Test Agent adds validation.
5. Security Agent reviews risk.
6. Documentation Agent updates README, docs, wiki, diagrams, and user stories.
7. Reviewer Agent comments on correctness and residual risk.
8. Human maintainer approves and merges.
9. Release Agent prepares changelog, release notes, and release evidence.

## CAVRA Responsibilities

- Evaluate actions before they happen.
- Enforce policy packs.
- Require approvals for protected actions.
- Generate evidence bundles and PR attestations.
- Preserve transparent bot identity and audit trails.

## Diagram

See `agent-orchestration.svg` in the Wiki files and `docs/diagrams/agent-orchestration.svg` in the repository.
