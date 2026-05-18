# CAVRA

Controlled Agentic Verification & Runtime Authority

Before the agent acts, CAVRA decides.

## Wiki Purpose

This wiki is the operating manual for CAVRA as an enterprise AI-agent runtime governance platform. It explains the product thesis, architecture, roadmap, user stories, enterprise challenges, controls, evidence model, and implementation phases.

## Current Phase Status

Phase 1, Productization Foundation, is complete in PR #1. It establishes CAVRA identity, CLI, MCP server, Claude Code setup, policy packs, runtime decisions, Docker validation, API contract, sandbox, and enterprise documentation.

Phase 2, Policy Engine Hardening, is complete in PR #1. It adds strict schema validation, inheritance, normalized compile output, semantic diff, signature metadata, and tamper-detection tests.

Phase 3, Evidence Hub and Attestation, now includes signed evidence bundles, trust-root bundles, SIEM exports, retention controls, AWS/Azure immutable evidence storage references, SQLite and JSON evidence metadata search, governed artifact retrieval APIs, console API wiring, and migration automation.

Phase 4, Approval Router, is complete for the current production-readiness slice. It includes JSON and SQLite approval persistence, default and repository-specific routing, claims-based approval authorization, signed OIDC/JWKS validation, repository RBAC, Entra/Okta OIDC-RBAC deployment references, provider payload and request-spec exports, secret-backed live provider delivery, console approval queue actions, console break-glass creation, approval audit detail views, and approval evidence linkage.

Phase 5, Agent Registry and MCP Trust Registry, is complete for the current production-readiness slice. It includes JSON and SQLite governed agent identities, MCP server trust records, predefined agent capability profiles, MCP capability classification, API and CLI access, console registry views, and registry-backed MCP runtime decisions.

Phase 6, Console and Persistent API, has started. It now includes JSON and SQLite activity persistence for sessions and decisions, repository inventory and policy rollout persistence, policy-pack authoring previews, approval-bound signed policy publishing, rollout change workflows, production deployment validation, integration inventory persistence, evidence artifact retrieval views, persistent API backup/restore/retention operations, policy rollout drill-downs, read-only console security boundary reporting, authenticated console sessions, RBAC-enforced console mutations, decision search filters, session summaries, and console Activity Explorer plus repository/rollout/integration views.

Phase 7, Go Enforcement Plane, has started with a bounded parity scaffold. It includes a Go module, runtime evaluator, CLI entrypoint, compiled-policy JSON loader, generated Go enforcement contracts, Unix-socket daemon transport, reusable daemon client helper, CLI `--daemon` mode, daemon lifecycle `start/status/stop`, request/response evidence hooks, runtime evidence references, trust-registry JSON loading, registry-backed MCP decisions, all-bundled-policy compiled parity, signed release package workflow, SBOM generation, SLSA provenance, release evidence, GitHub Release asset attachment, verifier CLI support, shared critical decision fixture, Python and Go parity tests, a dedicated `go-runtime-parity` CI job, and Go test execution in the required governance check.

Phase 8, Enterprise Integrations, has started with a GitHub required-check workflow, reusable GitHub Actions templates, GitLab CI and Azure Pipelines enforcement examples, CI evidence artifact upload for branch protection, approval-bound policy write-back, live SIEM/ITSM/ChatOps connector execution hooks, AWS/Azure immutable evidence storage references, and Entra/Okta OIDC-RBAC deployment references.

Phase 9, Public Sandbox, has started with a GitHub Pages deployment workflow for the static Before the Agent Acts sandbox and evidence console. GitHub Pages is enabled for Actions publishing, and the public sandbox URL is `https://huzefaaa2.github.io/cavra/`. The workflow now includes packaged downloadable sample evidence plus post-deploy smoke validation for the page, JavaScript, stylesheet, brand assets, C4 diagram, and evidence JSON.

Transparent CAVRA engineering-agent methodology is now documented for the repository. It defines bot identities, agent roles, branch conventions, approval gates, evidence requirements, and the rule that CAVRA must never use fake human identities.

## Primary Pages

- White Paper: `White-Paper.md`
- Production Roadmap: `Production-Roadmap.md`
- Go Release Packaging: `Go-Release-Packaging.md`
- Vulnerability Disclosure: `Vulnerability-Disclosure.md`
- Release Security Advisories: `Release-Security-Advisories.md`
- Implementation Plan: `Implementation-Plan.md`
- User Stories: `User-Stories.md`
- Enterprise Challenges: `Enterprise-Challenges.md`
- Diagrams: `Diagrams.md`
- Phase Completion Log: `Phase-Completion-Log.md`
- Approval Workflows: `Approval-Workflows.md`
- Policy Engine Hardening: `Policy-Engine-Hardening.md`
- Evidence Hub and Attestation: `Evidence-Hub-and-Attestation.md`
- Evidence Key Management: `Evidence-Key-Management.md`
- Evidence Trust-Root Distribution: `Evidence-Trust-Root-Distribution.md`
- Evidence Metadata Migrations: `Evidence-Metadata-Migrations.md`
- GitHub Repository Readiness: `GitHub-Repository-Readiness.md`
- GitHub Required Checks and CI/CD Enforcement: `GitHub-Required-Checks-and-CI-CD-Enforcement.md`
- Release Documentation Policy: `Release-Documentation-Policy.md`
- Transparent Agent Methodology: `Transparent-Agent-Methodology.md`
- Agent Orchestration Architecture: `Agent-Orchestration-Architecture.md`
- Agent Registry and MCP Trust Registry: `Agent-Registry-and-MCP-Trust.md`
- Activity Persistence: `Activity-Persistence.md`
- Repository Inventory and Policy Rollout: `Repository-Policy-Rollout.md`
- Persistent API Operations: `Persistent-API-Operations.md`
- Integration Inventory: `Integration-Inventory.md`
- Connector Execution Hooks: `Connector-Execution-Hooks.md`
- Console Security Boundary: `Console-Security-Boundary.md`
- Console Authenticated Sessions: `Console-Authenticated-Sessions.md`
- OIDC/RBAC Deployment: `OIDC-RBAC-Deployment.md`
- Evidence Artifact Retrieval: `Evidence-Artifact-Retrieval.md`
- Immutable Evidence Storage: `Immutable-Evidence-Storage.md`
- Policy Pack Authoring Workflows: `Policy-Pack-Authoring-Workflows.md`
- Production Deployment Validation: `Production-Deployment-Validation.md`
- Go Enforcement Parity: `Go-Enforcement-Parity.md`
- Go Enforcement Contracts: `Go-Enforcement-Contracts.md`
- Go Daemon Transport: `Go-Daemon-Transport.md`
- Vulnerability Disclosure: `Vulnerability-Disclosure.md`
- Release Security Advisories: `Release-Security-Advisories.md`
- Hosted Sandbox Deployment: `Hosted-Sandbox-Deployment.md`
- Brand Assets: `Brand-Assets.md`

## Quick Start

```bash
pipx install cavra
cavra policy test
cavra evaluate read_file .env --json
cavra init claude-code
claude mcp add cavra -- cavra-mcp-server
```

## Sandbox

Run the local sandbox:

```bash
docker compose up -d --build
```

Open `http://127.0.0.1:5173`.

After merge to `main`, deploy the hosted sandbox with:

```bash
gh workflow run deploy-sandbox.yml --repo Huzefaaa2/cavra --ref main
```
