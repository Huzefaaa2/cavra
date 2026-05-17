# CAVRA
## Controlled Agentic Verification & Runtime Authority

Before the agent acts, CAVRA decides.

CAVRA is a runtime governance and authority layer for AI coding agents. It controls, verifies, approves, blocks, and audits what agents can read, write, execute, connect to, approve, and change across code, cloud, Git, MCP, shell, CI/CD, infrastructure, and regulated engineering workflows.

CAVRA is not a Terraform scanner. CAVRA is a runtime authority layer for autonomous engineering. Terraform/OpenTofu is one supported control surface, not the product boundary.

## What is CAVRA?

CAVRA sits between AI coding agents and meaningful engineering actions. It evaluates file access, shell commands, Git operations, MCP tool calls, infrastructure changes, approvals, and evidence generation before an agent acts.

## Why CAVRA exists

AI coding agents now inspect repositories, modify code, invoke tools, run shell commands, touch infrastructure, open pull requests, and interact with enterprise workflows. Traditional controls often arrive after the code changed or after a pull request exists. CAVRA makes pre-action enforcement the control point.

## What CAVRA controls

- File reads and writes, including secrets, state files, production config, CI/CD workflows, IAM, PCI, PHI, and regulated data fixtures.
- Commands, including Terraform/OpenTofu, Kubernetes, Azure CLI, AWS CLI, GCP CLI, Git, test runners, package managers, and dangerous shell patterns.
- Git and PR workflows, including protected branches, direct push, force push, required PR attestation, and AI-generated change evidence.
- MCP servers and tools, including filesystem, shell, network, database, SaaS, and unknown server governance.
- Evidence and approvals, including decision logs, signed bundles, PR attestations, SIEM events, and approver routing.

## How CAVRA works

1. An agent requests an action.
2. CAVRA normalizes the action into a decision request.
3. The policy registry loads the active policy pack.
4. Runtime guards evaluate the request before execution.
5. CAVRA returns `allow`, `block`, `require_approval`, `warn`, `audit_only`, or `allow_with_attestation`.
6. Evidence is written for audit, PR review, SIEM export, and compliance mapping.

## Architecture overview

CAVRA keeps the current Python management plane and introduces a Go enforcement-plane roadmap. Python owns policy authoring, evidence, integrations, FastAPI, Claude Code adapters, risk classification, and compliance mapping. Go is planned for low-latency local enforcement, CI runner enforcement, streaming audit events, and air-gapped single-binary deployment.

Architecture references:

- [C4 context diagram](docs/diagrams/c4-context.md)
- [C4 container diagram](docs/diagrams/c4-container.md)
- [C4 container SVG](docs/diagrams/c4-container.svg)
- [Runtime component diagram](docs/diagrams/c4-component-runtime.md)
- [Runtime decision flow](docs/diagrams/runtime-decision-flow.md)
- [Evidence lifecycle](docs/diagrams/evidence-lifecycle.md)
- [Architecture SVG](docs/diagrams/architecture-context.svg)
- [Runtime flow SVG](docs/diagrams/runtime-flow.svg)
- [Evidence Hub SVG](docs/diagrams/evidence-hub.svg)
- [Policy Lifecycle SVG](docs/diagrams/policy-lifecycle.svg)
- [Developer Journey SVG](docs/diagrams/developer-journey.svg)
- [Transparent Agent Orchestration SVG](docs/diagrams/agent-orchestration.svg)

## Quick start

```bash
pipx install cavra
cavra version
cavra policy list
cavra policy test
cavra evaluate read_file .env --json
```

## Claude Code quickstart

```bash
claude mcp add cavra -- cavra-mcp-server
```

Initialize a repository for Claude Code governance:

```bash
cavra init claude-code
```

CAVRA for Claude Code gives Claude Code a runtime authority layer. It evaluates sensitive agent actions before they reach files, shell commands, Git operations, MCP tools, Terraform, Kubernetes, or cloud control planes.

## CLI usage

```bash
cavra agent start --tool claude-code
cavra evaluate execute_command "terraform apply -auto-approve"
cavra policy validate policies/cavra-ai-agent-baseline
cavra policy explain execute_command "terraform plan"
cavra demo before-the-agent-acts
```

## API usage

```bash
uvicorn cavra.api:app --reload
curl http://127.0.0.1:8000/health
```

The API is published as `CAVRA API` and exposes policies, decisions, sessions, agents, approvals, evidence, integrations, MCP trust, risk events, compliance mappings, and sandbox endpoints.

## Policy packs

Policy packs live under `policies/`. Current packs cover AI-agent baseline, banking, PCI DSS, HIPAA, SOX change control, NIST SSDF, ISO 27001, EU AI Act, OWASP LLM/agentic risks, MCP enterprise governance, Kubernetes production safety, Terraform/OpenTofu production safety, cloud IAM, GitHub Enterprise, and GitLab Enterprise.

Policy engine hardening is documented in [docs/policy-engine-hardening.md](docs/policy-engine-hardening.md). CAVRA now supports JSON Schema validation, inherited policy packs, normalized policy compilation, semantic policy diffs, and policy signature metadata.

```bash
cavra policy validate policies/cavra-ai-agent-baseline
cavra policy compile --policy-pack cavra-ai-agent-baseline
cavra policy diff policies/cavra-ai-agent-baseline policies/cavra-banking-baseline
cavra policy sign policies/cavra-ai-agent-baseline/policy.yaml --signer platform-security
cavra policy verify policies/cavra-ai-agent-baseline/policy.yaml
```

## Evidence and attestation

CAVRA emits decision JSON, session audit files, PR attestation markdown, compliance mapping reports, and sandbox evidence bundles. Evidence includes agent identity, user or actor, repo, branch, action attempted, decision, policy version, rule ID, rationale, approval state, timestamp, evidence refs, and correlation ID.

Evidence Hub and Attestation is documented in [docs/evidence-hub-attestation.md](docs/evidence-hub-attestation.md). CAVRA now generates evidence bundles with manifests, checksums, HMAC or Ed25519 manifest signatures, PR attestation, compliance mapping, SIEM event output, provider-specific SIEM payloads, retention policies, immutable storage reference plans, metadata indexing, and verifier commands.

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
cavra evidence verify .cavra/evidence/latest
cavra evidence siem-event .cavra/evidence/latest
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence retention-policy .cavra/evidence/latest --output .cavra/evidence/retention
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
cavra evidence trust-root .cavra/keys/evidence-public.pem --output .cavra/keys/evidence-trust-root.json --key-id prod-evidence
cavra evidence trust-bundle .cavra/keys/evidence-trust-root.json --output .cavra/keys/evidence-trust-roots.json
cavra evidence verify-attestation .cavra/evidence/latest --output .cavra/evidence/attestation
cavra evidence migrate --sqlite .cavra/evidence/metadata.db
cavra evidence index .cavra/evidence/latest --sqlite .cavra/evidence/metadata.db
cavra evidence search --sqlite .cavra/evidence/metadata.db --min-blocked 1 --limit 25
```

Evidence key management and rotation guidance is documented in [docs/evidence-key-management.md](docs/evidence-key-management.md).

## Human approvals

Risky actions can return `require_approval` with approver groups such as Platform Security, Cloud Security, IAM, AppSec, Change Advisory Board, AI Governance, Data Protection, PCI Compliance, Healthcare Compliance, or Repository Owners.

## MCP governance

Run the MCP server:

```bash
cavra-mcp-server --list-tools
```

The server exposes CAVRA tools for evaluating actions, checking files, commands, Git operations, MCP calls, generating PR attestations, exporting evidence, and managing sessions.

## Git and PR governance

CAVRA blocks direct push to protected branches, can require PR attestation, records AI-agent metadata, and creates reviewer-ready evidence for risky diffs.

## Transparent CAVRA engineering agents

CAVRA uses a transparent AI engineering-team methodology for its own repository and for customer reference architecture. Specialized bots such as `cavra-backend[bot]`, `cavra-security[bot]`, `cavra-docs[bot]`, and `cavra-release[bot]` are declared as automation, not fake human contributors.

Agent manifests live under [.github/agents](.github/agents). They define each role's identity, allowed triggers, allowed paths, approval gates, prohibited actions, and required evidence. The [Transparent Agent Methodology](docs/transparent-agent-methodology.md) and [Agent Orchestration Architecture](docs/agent-orchestration-architecture.md) explain the operating model.

The policy pack [policies/cavra-agentic-delivery](policies/cavra-agentic-delivery/policy.yaml) governs agent-driven delivery with protected branch requirements, bot identity requirements, PR attestation, documentation freshness, and human approval for protected actions.

## Terraform/OpenTofu, Kubernetes, and cloud CLI governance

CAVRA allows read-only planning workflows such as `terraform plan`, while blocking or routing autonomous production-impacting operations such as `terraform apply -auto-approve`, `kubectl delete`, cloud IAM expansion, and direct protected-branch pushes.

## Enterprise integrations

The repository includes reference paths for GitHub, GitLab, Azure DevOps, pre-commit, Docker, Kubernetes, Microsoft Sentinel, Splunk, Datadog, ServiceNow, Jira, Slack, Microsoft Teams, immutable evidence stores, Entra ID, Okta, SAML, and RBAC. Planned integrations are labeled as reference architecture until implemented.

## Compliance packs

CAVRA maps runtime controls to banking change control, PCI DSS, HIPAA, SOX, NIST SSDF, ISO 27001, EU AI Act, and OWASP LLM/agentic risks.

## Interactive sandbox

The `Before the Agent Acts` sandbox now includes the first hosted console slice: simulated agent decisions, evidence metadata search, PR attestation verification, and operational readiness status:

```bash
python -m http.server 5173 --directory apps/sandbox-ui
```

Open `http://127.0.0.1:5173`, run the agent scenario, filter evidence metadata, and verify PR attestation coverage.

For deployed topologies, configure `window.CAVRA_API_BASE` in the hosted page or set `CAVRA_PUBLIC_API_BASE_URL` and `CAVRA_CORS_ORIGINS` on the API. The console reads `/console/config` when available and falls back to bundled sample evidence when the API is unreachable. See [docs/sandbox.md](docs/sandbox.md).

## Demo scenarios

The flagship demo is in `examples/demos/before-the-agent-acts/` and proves CAVRA can block `.env` reads, allow `terraform plan`, block `terraform apply -auto-approve`, require approval for IAM changes, block unknown MCP filesystem servers, block push to `main`, and generate PR attestation.

## Roadmap

The production roadmap is priority-based, not calendar-based. See [docs/production-roadmap.md](docs/production-roadmap.md) and [docs/implementation-plan.md](docs/implementation-plan.md).

Current phase status:

- Phase 1: Productization Foundation - complete in PR #1.
- Phase 2: Policy Engine Hardening - complete in PR #1.
- Phase 3: Evidence Hub and Attestation - in progress in PR #1.
- Phase 4: Approval Router - next recommended implementation phase after public/private key signature hardening is completed.
- Phase 5: Agent Registry and MCP Trust Registry.
- Phase 6: Console and Persistent API.
- Phase 7: Go Enforcement Plane.
- Phase 8: Enterprise Integrations.
- Phase 9: Public Sandbox and Growth Loop.
- Phase 10: Production Readiness and Release.

Next recommended implementation work:

- Add hosted attestation artifact download APIs backed by governed object storage.
- Start Phase 4 Approval Router with reviewer group routing, approval lifecycle state, and break-glass evidence.

## User stories and enterprise value

CAVRA is built around enterprise user stories for developers, CISOs, platform engineers, DevSecOps, auditors, and AI governance leads. See [docs/user-stories.md](docs/user-stories.md).

CAVRA directly addresses secret exposure, unsafe infrastructure changes, direct Git push, dangerous shell commands, MCP tool sprawl, audit gaps, identity ambiguity, approval bypass, and regulated SDLC evidence gaps. See [docs/enterprise-challenges.md](docs/enterprise-challenges.md).

## Wiki and white paper

Wiki-ready documentation is maintained under [docs/wiki](docs/wiki):

- [Home](docs/wiki/Home.md)
- [White Paper](docs/wiki/White-Paper.md)
- [Production Roadmap](docs/wiki/Production-Roadmap.md)
- [Implementation Plan](docs/wiki/Implementation-Plan.md)
- [User Stories](docs/wiki/User-Stories.md)
- [Enterprise Challenges](docs/wiki/Enterprise-Challenges.md)
- [Diagrams](docs/wiki/Diagrams.md)
- [Phase Completion Log](docs/wiki/Phase-Completion-Log.md)
- [Policy Engine Hardening](docs/wiki/Policy-Engine-Hardening.md)
- [Evidence Hub and Attestation](docs/wiki/Evidence-Hub-and-Attestation.md)
- [Evidence Key Management](docs/wiki/Evidence-Key-Management.md)
- [Evidence Trust-Root Distribution](docs/wiki/Evidence-Trust-Root-Distribution.md)
- [GitHub Repository Readiness](docs/wiki/GitHub-Repository-Readiness.md)
- [Release Documentation Policy](docs/wiki/Release-Documentation-Policy.md)
- [Transparent Agent Methodology](docs/wiki/Transparent-Agent-Methodology.md)
- [Agent Orchestration Architecture](docs/wiki/Agent-Orchestration-Architecture.md)

The wiki white paper explains why CAVRA exists, how pre-action enforcement works, the dual-plane architecture, regulated SDLC fit, Claude Code strategy, and the production roadmap.

## Contributing

Contributions should preserve CAVRA’s pre-action enforcement model, open evidence format, policy-as-code approach, and self-hosted enterprise deployment path.

## License

This repository is licensed under BUSL-1.1. See `LICENSE`.
