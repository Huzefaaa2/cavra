# CAVRA White Paper

## Executive Summary

AI coding agents are moving from suggestion to execution. They can inspect repositories, modify code, invoke tools, run shell commands, create branches, push commits, open pull requests, use MCP servers, and touch infrastructure. Traditional controls are often too late because they evaluate after code has changed or after a pull request exists.

CAVRA, Controlled Agentic Verification & Runtime Authority, is a runtime governance and authority layer for AI coding agents. Before the agent acts, CAVRA decides.

The current implementation also establishes the controlled path to low-latency enforcement. Python remains authoritative, while a bounded Go scaffold verifies critical decision parity in CI before any future promotion to local daemon, CI runner, or air-gapped binary enforcement.

## Product Thesis

Enterprises need a decision point between AI coding agents and meaningful engineering actions. CAVRA evaluates what an agent wants to read, write, execute, connect to, approve, merge, or change before execution. It returns a decision, records evidence, and routes risky actions to human approval when required.

## What CAVRA Controls

- File reads and writes.
- Shell commands.
- Git operations.
- MCP tool calls.
- Infrastructure-as-code tools.
- Kubernetes.
- AWS, Azure, and GCP CLI operations.
- CI/CD workflows.
- PR attestation.
- Evidence generation.
- Approval routing.

## Core Decisions

CAVRA decisions are:

- `allow`
- `block`
- `require_approval`
- `warn`
- `audit_only`
- `allow_with_attestation`

Each decision includes agent identity, actor, action type, target, requested operation, policy pack, policy ID, rule ID, severity, reason, evidence references, approver group, timestamp, and correlation ID.

## Architecture

CAVRA uses a dual-plane architecture.

Management plane:
- Python CLI.
- Policy registry.
- Evidence hub.
- Approval router.
- Agent Registry and MCP Trust Registry with JSON/SQLite persistence.
- Activity persistence for sessions and decisions.
- Repository inventory and policy rollout persistence.
- Integration inventory persistence.
- Persistent API backup, restore, and retention operations.
- Policy rollout drill-downs and read-only console security boundary reporting.
- FastAPI backend.
- Claude Code and MCP adapters.
- Compliance packs.
- Integrations.

Enforcement plane:
- Current Python runtime guard.
- Scaffolded Go runtime backend with shared parity fixtures, compiled-policy loading, registry-backed MCP decisions, and approval-backed release governance record checks.
- Future Unix-socket or gRPC interface.
- Future local daemon and CI runner mode.
- Future air-gapped single-binary deployment.

## Enterprise Value

CAVRA solves:

- Secret exposure.
- Unsafe infrastructure changes.
- Direct protected-branch push.
- Dangerous shell command execution.
- MCP tool sprawl.
- Audit gaps.
- Identity ambiguity.
- Approval bypass.
- Excessive agency.
- Prompt-injection-induced tool misuse.

## Regulated SDLC Fit

CAVRA maps AI-agent runtime controls to banking, PCI DSS, HIPAA, SOX, NIST SSDF, ISO 27001, EU AI Act, and OWASP LLM/agentic risk requirements.

## Claude Code Strategy

CAVRA should become the default governance layer for Claude Code users:

```bash
claude mcp add cavra -- cavra-mcp-server
```

The strategy is simple: make safe adoption easier than ungoverned adoption.

## Production Roadmap

The path to production readiness is:

1. Productization foundation.
2. Policy engine hardening. This phase is complete and adds schema validation, inheritance, semantic diff, compile output, and policy signature metadata.
3. Evidence hub and attestation. This phase is near complete and includes signed evidence, SIEM exports, retention, trust roots, metadata search, governed artifact retrieval, and console evidence views.
4. Approval router. This phase is complete for the current production-readiness slice and includes approval routing, OIDC/JWKS, repository RBAC, provider delivery, break-glass, and audit views.
5. Agent Registry and MCP Trust Registry. This phase is complete for the current production-readiness slice and includes JSON/SQLite registry persistence, agent profiles, MCP capability classification, console views, and registry-backed runtime decisions.
6. Console and persistent API. This phase has started with durable sessions, decisions, repository inventory, policy rollout persistence, policy authoring previews, rollout change workflows, production deployment validation, integration inventory persistence, evidence artifact retrieval, persistent API backup/restore/retention operations, policy rollout drill-downs, read-only console security boundary reporting, authenticated console sessions, RBAC-enforced console mutations, console Activity Explorer views, and repository/rollout/integration console views.
7. Go enforcement plane.
8. Enterprise integrations. This phase has started with GitHub required-check templates, GitLab and Azure DevOps CI/CD enforcement examples, evidence verification in branch protection, CI evidence artifact upload, approval-bound signed policy publishing, live SIEM/ITSM/ChatOps connector execution hooks, AWS/Azure immutable evidence storage references, and Entra/Okta OIDC-RBAC deployment references.
9. Public sandbox and growth loop.
10. Production readiness and release.

## Conclusion

CAVRA is not a prompt filter or static scanner. It is the enterprise runtime authority layer for autonomous engineering.
