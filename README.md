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

## Evidence and attestation

CAVRA emits decision JSON, session audit files, PR attestation markdown, compliance mapping reports, and sandbox evidence bundles. Evidence includes agent identity, user or actor, repo, branch, action attempted, decision, policy version, rule ID, rationale, approval state, timestamp, evidence refs, and correlation ID.

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

## Terraform/OpenTofu, Kubernetes, and cloud CLI governance

CAVRA allows read-only planning workflows such as `terraform plan`, while blocking or routing autonomous production-impacting operations such as `terraform apply -auto-approve`, `kubectl delete`, cloud IAM expansion, and direct protected-branch pushes.

## Enterprise integrations

The repository includes reference paths for GitHub, GitLab, Azure DevOps, pre-commit, Docker, Kubernetes, Microsoft Sentinel, Splunk, Datadog, ServiceNow, Jira, Slack, Microsoft Teams, immutable evidence stores, Entra ID, Okta, SAML, and RBAC. Planned integrations are labeled as reference architecture until implemented.

## Compliance packs

CAVRA maps runtime controls to banking change control, PCI DSS, HIPAA, SOX, NIST SSDF, ISO 27001, EU AI Act, and OWASP LLM/agentic risks.

## Interactive sandbox

The `Before the Agent Acts` sandbox lets a prospect run a simulated AI-agent scenario using real CAVRA policy decisions:

```bash
python -m http.server 5173 --directory apps/sandbox-ui
```

Open `http://127.0.0.1:5173` and click `Run Agent Scenario`.

## Demo scenarios

The flagship demo is in `examples/demos/before-the-agent-acts/` and proves CAVRA can block `.env` reads, allow `terraform plan`, block `terraform apply -auto-approve`, require approval for IAM changes, block unknown MCP filesystem servers, block push to `main`, and generate PR attestation.

## Roadmap

Near-term work focuses on parity tests, signed evidence bundles, schema-hardening, Go enforcement-plane contracts, richer FastAPI persistence, sandbox deployment, SIEM exporters, and approval workflow integrations.

## Contributing

Contributions should preserve CAVRA’s pre-action enforcement model, open evidence format, policy-as-code approach, and self-hosted enterprise deployment path.

## License

This repository is licensed under BUSL-1.1. See `LICENSE`.
