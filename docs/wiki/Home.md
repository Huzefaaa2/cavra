# CAVRA

Controlled Agentic Verification & Runtime Authority

Before the agent acts, CAVRA decides.

## Wiki Purpose

This wiki is the operating manual for CAVRA as an enterprise AI-agent runtime governance platform. It explains the product thesis, architecture, roadmap, user stories, enterprise challenges, controls, evidence model, and implementation phases.

## Current Phase Status

Phase 1, Productization Foundation, is complete in PR #1. It establishes CAVRA identity, CLI, MCP server, Claude Code setup, policy packs, runtime decisions, Docker validation, API contract, sandbox, and enterprise documentation.

Phase 2, Policy Engine Hardening, is complete in PR #1. It adds strict schema validation, inheritance, normalized compile output, semantic diff, signature metadata, and tamper-detection tests.

Phase 3, Evidence Hub and Attestation, now includes signed evidence bundles, trust-root bundles, SIEM exports, retention controls, SQLite and JSON evidence metadata search, governed artifact retrieval APIs, console API wiring, and migration automation.

Phase 4, Approval Router, is complete for the current production-readiness slice. It includes JSON and SQLite approval persistence, default and repository-specific routing, claims-based approval authorization, signed OIDC/JWKS validation, repository RBAC, provider payload and request-spec exports, secret-backed live provider delivery, console approval queue actions, console break-glass creation, approval audit detail views, and approval evidence linkage.

Phase 5, Agent Registry and MCP Trust Registry, is complete for the current production-readiness slice. It includes JSON and SQLite governed agent identities, MCP server trust records, predefined agent capability profiles, MCP capability classification, API and CLI access, console registry views, and registry-backed MCP runtime decisions.

Phase 6, Console and Persistent API, has started. It now includes JSON and SQLite activity persistence for sessions and decisions, repository inventory and policy rollout persistence, policy-pack authoring previews, rollout change workflows, production deployment validation, integration inventory persistence, evidence artifact retrieval views, persistent API backup/restore/retention operations, policy rollout drill-downs, read-only console security boundary reporting, authenticated console sessions, RBAC-enforced console mutations, decision search filters, session summaries, and console Activity Explorer plus repository/rollout/integration views.

Transparent CAVRA engineering-agent methodology is now documented for the repository. It defines bot identities, agent roles, branch conventions, approval gates, evidence requirements, and the rule that CAVRA must never use fake human identities.

## Primary Pages

- White Paper: `White-Paper.md`
- Production Roadmap: `Production-Roadmap.md`
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
- Release Documentation Policy: `Release-Documentation-Policy.md`
- Transparent Agent Methodology: `Transparent-Agent-Methodology.md`
- Agent Orchestration Architecture: `Agent-Orchestration-Architecture.md`
- Agent Registry and MCP Trust Registry: `Agent-Registry-and-MCP-Trust.md`
- Activity Persistence: `Activity-Persistence.md`
- Repository Inventory and Policy Rollout: `Repository-Policy-Rollout.md`
- Persistent API Operations: `Persistent-API-Operations.md`
- Integration Inventory: `Integration-Inventory.md`
- Console Security Boundary: `Console-Security-Boundary.md`
- Console Authenticated Sessions: `Console-Authenticated-Sessions.md`
- Evidence Artifact Retrieval: `Evidence-Artifact-Retrieval.md`
- Policy Pack Authoring Workflows: `Policy-Pack-Authoring-Workflows.md`
- Production Deployment Validation: `Production-Deployment-Validation.md`

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
