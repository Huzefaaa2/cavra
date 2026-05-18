# CAVRA C4 Container Diagram

This container view separates the collaboration surfaces, runtime authority, evidence plane, persistent metadata, and enterprise integrations. It is intentionally grouped so security, platform, audit, and architecture reviewers can read the system without tracing every code module.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#eef6ff", "primaryTextColor": "#17242d", "primaryBorderColor": "#3b6f8f", "lineColor": "#526777", "secondaryColor": "#f6fff0", "tertiaryColor": "#fff7eb"}}}%%
C4Container
title CAVRA Container View - Runtime Authority, Evidence, CI/CD Enforcement, and Enterprise Integrations

Person(developer, "Developer", "Uses AI coding tools under CAVRA governance.")
Person(platform, "Platform / Security Engineer", "Authors policies, reviews approvals, and operates integrations.")
Person(auditor, "Auditor / Compliance Reviewer", "Reviews attestations, evidence bundles, retention, and decision metadata.")

System_Boundary(cavra, "CAVRA") {
  Container_Boundary(entry, "Interaction and Management Surfaces") {
    Container(cli, "CAVRA CLI", "Python Typer", "Local evaluation, policy authoring, evidence export, retention, signing, and Claude Code init.")
    Container(mcpServer, "CAVRA MCP Server", "Python stdio MCP", "Tool interface for Claude Code and MCP-aware agents.")
    Container(api, "CAVRA API", "FastAPI", "Management API for policies, authoring drafts, signed policy publishing, rollout changes, deployment readiness, persisted decisions, sessions, repositories, rollout drill-downs, integrations, evidence metadata and artifacts, console session context, security boundary, operations status, approvals, registry, and sandbox.")
    Container(sandbox, "Before the Agent Acts Sandbox", "HTML/CSS/JS + GitHub Pages", "Interactive demo and console for buyers, developers, platform teams, and auditors, with Pages deployment workflow.")
  }

  Container_Boundary(authority, "Runtime Authority") {
    Container(runtime, "Runtime Guard", "Python", "Pre-action decisions for file, command, Git, MCP, and PR-attestation requests.")
    Container(policy, "Policy Registry", "YAML + JSON Schema", "Policy packs, schema validation, inheritance, semantic diff, approval-bound write-back, and signature metadata.")
    Container(approval, "Approval Router", "Python + JSON/SQLite", "Routes high-risk actions with default or repository rules, validates signed OIDC/JWKS identity and repository RBAC, includes Entra/Okta deployment references, exports and delivers provider requests, records approval outcomes, and supports console break-glass and audit details.")
    Container(registry, "Agent and MCP Trust Registry", "Python + JSON/SQLite", "Tracks governed agents, MCP servers, trust tiers, owners, capabilities, approval state, agent profiles, MCP tool classifications, and runtime trust decisions.")
  }

  Container_Boundary(evidencePlane, "Evidence and Audit Plane") {
    Container(evidence, "Evidence Hub", "Python + JSON/Markdown", "Bundles manifests, checksums, Ed25519/HMAC signatures, PR attestations, required-check evidence, compliance mapping, SIEM payloads, and retention policies.")
    Container(connectorDelivery, "Connector Delivery Hooks", "Python + HTTP", "Executes configured SIEM, ITSM, ChatOps, and webhook deliveries with retry handling and credential-redacted evidence.")
    ContainerDb(metadata, "Metadata, Activity, and Inventory Stores", "JSON/SQLite", "Searchable evidence, session, decision, approval, registry, repository inventory, policy rollout, integration inventory, backup manifests, and retention plans.")
    ContainerDb(bundleStore, "Evidence Bundle Store", "Filesystem + immutable storage references", "Verifier-ready bundle artifacts, governed retrieval root, ZIP bundle downloads, AWS S3 Object Lock references, Azure Blob immutability references, and storage plans.")
  }

  Container(goRuntime, "Go Enforcement Plane", "Go", "Scaffolded low-latency enforcement backend with compiled-policy loading, shared Python/Go parity fixtures, and CI checks; daemon transport remains next.")
}

System_Ext(agent, "AI Coding Agent")
System_Ext(mcpTools, "MCP Servers and Tools")
System_Ext(git, "Git / PR and CI/CD Platforms", "GitHub required checks, GitHub Actions, GitLab CI, Azure DevOps, Bitbucket.")
System_Ext(siem, "SIEM / SOC", "Splunk, Microsoft Sentinel, Datadog, or webhook collectors.")
System_Ext(itsm, "ITSM / ChatOps", "ServiceNow, Jira, Slack, Teams.")
System_Ext(immutable, "Immutable Evidence Storage", "S3 Object Lock, Azure immutable blob, or enterprise archive.")
System_Ext(identity, "Enterprise Identity", "OIDC, SAML, Entra ID, Okta.")
System_Ext(cloud, "Cloud / Infra Control Planes", "Terraform/OpenTofu, Kubernetes, AWS, Azure, GCP.")

Rel(developer, cli, "Runs local commands")
Rel(developer, agent, "Delegates coding work")
Rel(platform, api, "Operates policies, repositories, rollout state, approvals, integrations, and evidence")
Rel(auditor, api, "Reviews evidence metadata, repository coverage, rollout state, and bundle references")
Rel(auditor, evidence, "Downloads attestations, compliance reports, and bundle artifacts")

Rel(agent, mcpServer, "Requests governed tool calls")
Rel(agent, cli, "Can be wrapped by local CLI workflows")
Rel(mcpServer, runtime, "Submits file, command, Git, and MCP decisions")
Rel(cli, runtime, "Evaluates local actions")
Rel(api, runtime, "Requests decisions")
Rel(sandbox, api, "Runs demo scenarios")

Rel(runtime, policy, "Loads compiled policy rules")
Rel(runtime, approval, "Requires human approval for risky actions")
Rel(runtime, registry, "Checks agent and MCP trust state")
Rel(runtime, evidence, "Writes decision evidence")
Rel(goRuntime, runtime, "Critical decision parity fixture")

Rel(evidence, metadata, "Indexes searchable evidence metadata")
Rel(evidence, connectorDelivery, "Builds signed evidence events")
Rel(cli, connectorDelivery, "Delivers configured connector events")
Rel(api, connectorDelivery, "Delivers integration events")
Rel(connectorDelivery, metadata, "Writes redacted delivery evidence")
Rel(api, metadata, "Persists sessions, decisions, repositories, rollout state, integrations, approvals, registry records, and operations status")
Rel(evidence, bundleStore, "Writes and serves verifier-ready bundles through governed retrieval")
Rel(evidence, git, "Publishes PR attestation and required-check artifacts")
Rel(evidence, siem, "Exports SIEM payloads")
Rel(connectorDelivery, siem, "Sends SIEM events")
Rel(connectorDelivery, itsm, "Sends ITSM and ChatOps events")
Rel(evidence, immutable, "Produces storage plans and operator deployment references")
Rel(approval, itsm, "Delivers approval requests")
Rel(approval, identity, "Validates OIDC/JWKS identity and RBAC")
Rel(api, identity, "Validates console bearer tokens and uses enterprise identity boundary")
Rel(mcpServer, mcpTools, "Allows, blocks, or audits tool calls")
Rel(runtime, git, "Allows or blocks Git operations")
Rel(runtime, cloud, "Allows, blocks, or routes infra operations")
```

## Reading Guide

- Interaction and Management Surfaces are where users, agents, demos, and operators enter CAVRA.
- Runtime Authority is the decision boundary: CAVRA decides before files, commands, Git operations, MCP tools, or infrastructure changes happen.
- Evidence and Audit Plane converts decisions into verifier-ready artifacts, searchable session and decision records, governed artifact downloads, CI/CD required-check artifacts for GitHub, GitLab, and Azure DevOps, policy draft, signed publish, and rollout change metadata, repository inventory, policy rollout state and drill-downs, integration inventory, connector delivery records, security boundary and console session metadata, deployment readiness checks, backup/restore manifests, SIEM payloads, metadata, retention controls, and immutable storage plans.
- Planned containers are shown to clarify the production direction without implying that the full enterprise console is complete today. The Go enforcement plane now has a scaffolded Go module, runtime evaluator, CLI entrypoint, compiled-policy loader, shared parity fixture, Go unit tests, and CI execution, but generated contracts, daemon transport, and signed binary packaging remain future work. The Approval Router now has JSON/SQLite persistence, repository routing files, signed OIDC/JWKS validation, repository RBAC policy checks, console queue actions, console break-glass creation, audit detail views, credential-free provider request specs, and live provider delivery evidence. The Agent and MCP Trust Registry now has JSON/SQLite persistence, predefined agent profiles, MCP tool classifications, console registry views, and registry-backed trust decisions.
