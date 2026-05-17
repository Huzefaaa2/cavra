# CAVRA Architecture

## Layers

1. Core policy and audit model
   - policy registry
   - runtime rule evaluation
   - audit evidence generation
2. Agent runtime wrapper
   - session lifecycle
   - command/file/git/MCP guards
   - agent identity and environment metadata
3. Integrations
   - CLI
   - webhook/API clients
   - GitHub PR attestation
   - SIEM / GRC evidence exports

## Components

- `cavra.cli`
- `cavra.agent`
- `cavra.runtime`
- `cavra.audit`
- `cavra.policy_registry`
- `.github/agents/*`
- `.github/workflows/agent-orchestrator.yml`

## Policy packs

Policy packs are stored under `policies/` and define sensitive path rules, blocked commands, and governance behaviour.

## Audit

Each AI session produces a JSON audit bundle and optional markdown attestation for PR workflows.

## Transparent agent orchestration

CAVRA models transparent engineering agents as GitHub Apps or bot identities with declarative manifests in `.github/agents/`. GitHub Issues, labels, branches, PRs, Actions, and reviews provide the collaboration surface. CAVRA remains the runtime authority that evaluates file access, commands, Git operations, MCP calls, policy changes, evidence generation, and approval requirements before an agent acts.

The orchestrator is intentionally separate from policy enforcement. A future orchestrator may route work from issues to agents, create branches, and attach evidence, but CAVRA decides whether each action is allowed, blocked, warned, attested, or routed for human approval.

See [Transparent Agent Methodology](transparent-agent-methodology.md), [Agent Orchestration Architecture](agent-orchestration-architecture.md), and [Agent Orchestration SVG](diagrams/agent-orchestration.svg).
