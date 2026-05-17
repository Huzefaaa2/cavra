# CAVRA C4 Container Diagram

This container view separates the collaboration surfaces, runtime authority, evidence plane, persistent metadata, and enterprise integrations. It is intentionally grouped so security, platform, audit, and architecture reviewers can read the system without tracing every code module.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#eef6ff", "primaryTextColor": "#17242d", "primaryBorderColor": "#3b6f8f", "lineColor": "#526777", "secondaryColor": "#f6fff0", "tertiaryColor": "#fff7eb"}}}%%
C4Container
title CAVRA Container View - Runtime Authority, Evidence, and Enterprise Integrations

Person(developer, "Developer", "Uses AI coding tools under CAVRA governance.")
Person(platform, "Platform / Security Engineer", "Authors policies, reviews approvals, and operates integrations.")
Person(auditor, "Auditor / Compliance Reviewer", "Reviews attestations, evidence bundles, retention, and decision metadata.")

System_Boundary(cavra, "CAVRA") {
  Container_Boundary(entry, "Interaction and Management Surfaces") {
    Container(cli, "CAVRA CLI", "Python Typer", "Local evaluation, policy authoring, evidence export, retention, signing, and Claude Code init.")
    Container(mcpServer, "CAVRA MCP Server", "Python stdio MCP", "Tool interface for Claude Code and MCP-aware agents.")
    Container(api, "CAVRA API", "FastAPI", "Management API for policies, decisions, sessions, evidence metadata, approvals, and sandbox.")
    Container(sandbox, "Before the Agent Acts Sandbox", "HTML/CSS/JS", "Interactive demo for buyers and developers.")
  }

  Container_Boundary(authority, "Runtime Authority") {
    Container(runtime, "Runtime Guard", "Python", "Pre-action decisions for file, command, Git, MCP, and PR-attestation requests.")
    Container(policy, "Policy Registry", "YAML + JSON Schema", "Policy packs, schema validation, inheritance, semantic diff, and signature metadata.")
    Container(approval, "Approval Router", "Python + JSON/SQLite", "Routes high-risk actions to human approvers, records approval outcomes, exports provider payloads, and supports break-glass evidence.")
    Container(registry, "Agent and MCP Trust Registry", "Planned service", "Tracks governed agents, MCP servers, trust tiers, owners, and capabilities.")
  }

  Container_Boundary(evidencePlane, "Evidence and Audit Plane") {
    Container(evidence, "Evidence Hub", "Python + JSON/Markdown", "Bundles manifests, checksums, Ed25519/HMAC signatures, PR attestations, compliance mapping, SIEM payloads, and retention policies.")
    ContainerDb(metadata, "Evidence Metadata Store", "JSON now, database planned", "Searchable evidence metadata exposed by the API.")
    ContainerDb(bundleStore, "Evidence Bundle Store", "Filesystem now, immutable object store planned", "Verifier-ready bundle artifacts and storage plans.")
  }

  Container(goRuntime, "Go Enforcement Plane", "Go / gRPC", "Planned low-latency local and CI enforcement backend with parity tests.")
}

System_Ext(agent, "AI Coding Agent")
System_Ext(mcpTools, "MCP Servers and Tools")
System_Ext(git, "Git / PR Platform", "GitHub, GitLab, Azure DevOps, Bitbucket.")
System_Ext(siem, "SIEM / SOC", "Splunk, Microsoft Sentinel, Datadog, or webhook collectors.")
System_Ext(itsm, "ITSM / ChatOps", "ServiceNow, Jira, Slack, Teams.")
System_Ext(immutable, "Immutable Evidence Storage", "S3 Object Lock, Azure immutable blob, or enterprise archive.")
System_Ext(identity, "Enterprise Identity", "OIDC, SAML, Entra ID, Okta.")
System_Ext(cloud, "Cloud / Infra Control Planes", "Terraform/OpenTofu, Kubernetes, AWS, Azure, GCP.")

Rel(developer, cli, "Runs local commands")
Rel(developer, agent, "Delegates coding work")
Rel(platform, api, "Operates policies, approvals, integrations, and evidence")
Rel(auditor, api, "Reviews evidence metadata and bundle references")
Rel(auditor, evidence, "Downloads attestations and compliance reports")

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
Rel(goRuntime, runtime, "Parity target and policy contract")

Rel(evidence, metadata, "Indexes searchable metadata")
Rel(evidence, bundleStore, "Writes verifier-ready bundles")
Rel(evidence, git, "Publishes PR attestation")
Rel(evidence, siem, "Exports SIEM payloads")
Rel(evidence, immutable, "Produces immutable storage plans")
Rel(approval, itsm, "Routes approval requests")
Rel(api, identity, "Uses enterprise identity boundary")
Rel(mcpServer, mcpTools, "Allows, blocks, or audits tool calls")
Rel(runtime, git, "Allows or blocks Git operations")
Rel(runtime, cloud, "Allows, blocks, or routes infra operations")
```

## Reading Guide

- Interaction and Management Surfaces are where users, agents, demos, and operators enter CAVRA.
- Runtime Authority is the decision boundary: CAVRA decides before files, commands, Git operations, MCP tools, or infrastructure changes happen.
- Evidence and Audit Plane converts decisions into verifier-ready artifacts, SIEM payloads, metadata, retention controls, and immutable storage plans.
- Planned containers are shown to clarify the production direction without implying that the full enterprise console and Go enforcement plane are complete today. The Approval Router now has an initial JSON/SQLite-backed implementation.
