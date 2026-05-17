# CAVRA

Controlled Agentic Verification & Runtime Authority

Before the agent acts, CAVRA decides.

## Wiki Purpose

This wiki is the operating manual for CAVRA as an enterprise AI-agent runtime governance platform. It explains the product thesis, architecture, roadmap, user stories, enterprise challenges, controls, evidence model, and implementation phases.

## Current Phase Status

Phase 1, Productization Foundation, is complete in PR #1. It establishes CAVRA identity, CLI, MCP server, Claude Code setup, policy packs, runtime decisions, Docker validation, API contract, sandbox, and enterprise documentation.

Phase 2, Policy Engine Hardening, is complete in PR #1. It adds strict schema validation, inheritance, normalized compile output, semantic diff, signature metadata, and tamper-detection tests.

Phase 3, Evidence Hub and Attestation, is the next recommended implementation phase.
Initial Phase 3 evidence bundle support is now in progress.

Transparent CAVRA engineering-agent methodology is now documented for the repository. It defines bot identities, agent roles, branch conventions, approval gates, evidence requirements, and the rule that CAVRA must never use fake human identities.

## Primary Pages

- White Paper: `White-Paper.md`
- Production Roadmap: `Production-Roadmap.md`
- Implementation Plan: `Implementation-Plan.md`
- User Stories: `User-Stories.md`
- Enterprise Challenges: `Enterprise-Challenges.md`
- Diagrams: `Diagrams.md`
- Phase Completion Log: `Phase-Completion-Log.md`
- Policy Engine Hardening: `Policy-Engine-Hardening.md`
- Evidence Hub and Attestation: `Evidence-Hub-and-Attestation.md`
- Evidence Key Management: `Evidence-Key-Management.md`
- GitHub Repository Readiness: `GitHub-Repository-Readiness.md`
- Release Documentation Policy: `Release-Documentation-Policy.md`
- Transparent Agent Methodology: `Transparent-Agent-Methodology.md`
- Agent Orchestration Architecture: `Agent-Orchestration-Architecture.md`

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
