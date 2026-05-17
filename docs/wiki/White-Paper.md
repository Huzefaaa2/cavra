# CAVRA White Paper

## Executive Summary

AI coding agents are moving from suggestion to execution. They can inspect repositories, modify code, invoke tools, run shell commands, create branches, push commits, open pull requests, use MCP servers, and touch infrastructure. Traditional controls are often too late because they evaluate after code has changed or after a pull request exists.

CAVRA, Controlled Agentic Verification & Runtime Authority, is a runtime governance and authority layer for AI coding agents. Before the agent acts, CAVRA decides.

## Product Thesis

Enterprises need a decision point between AI coding agents and meaningful engineering actions. CAVRA evaluates what an agent wants to read, write, execute, connect to, approve, merge, or change before execution. It returns a decision, records evidence, and routes risky actions to human approval when required.

## What CAVRA Controls

- File reads and writes.
- Shell commands.
- Git operations.
- MCP tool calls.
- Terraform/OpenTofu.
- Kubernetes.
- AWS, Azure, and GCP CLI operations.
- CI/CD workflows.
- PR attestation.
- Evidence generation.
- Approval routing.

Terraform/OpenTofu is one supported control surface, not the product boundary.

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
- FastAPI backend.
- Claude Code and MCP adapters.
- Compliance packs.
- Integrations.

Enforcement plane:
- Current Python runtime guard.
- Future Go runtime backend.
- Unix-socket or gRPC interface.
- Local daemon and CI runner mode.
- Air-gapped single-binary deployment.

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
3. Evidence hub and attestation. This is the next recommended phase.
4. Approval router.
5. Agent Registry and MCP Trust Registry.
6. Console and persistent API.
7. Go enforcement plane.
8. Enterprise integrations.
9. Public sandbox and growth loop.
10. Production readiness and release.

## Conclusion

CAVRA is not a prompt filter or static scanner. It is the enterprise runtime authority layer for autonomous engineering.
