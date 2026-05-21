# CAVRA

Controlled Agentic Verification & Runtime Authority

Before the agent acts, CAVRA decides.

## Wiki Purpose

This wiki is the operating manual for CAVRA as an enterprise AI-agent runtime governance platform. It explains the product thesis, architecture, roadmap, user stories, enterprise challenges, controls, evidence model, and implementation phases.

CAVRA is now planned as an open-core product. The public repository is the
Community Edition and product landing repo; Enterprise source, paid policy
packs, SaaS backend, and license service implementation must live in private
repositories. Start with the [Open-Core Implementation Plan](Open-Core-Implementation-Plan),
[Edition Boundaries](Edition-Boundaries), and [Private Enterprise Repo Plan](Private-Enterprise-Repo-Plan).

## Current Phase Status

Phase 1, Productization Foundation, is complete in PR #1. It establishes CAVRA identity, CLI, MCP server, Claude Code setup, policy packs, runtime decisions, Docker validation, API contract, sandbox, and enterprise documentation.

Phase 2, Policy Engine Hardening, is complete in PR #1. It adds strict schema validation, inheritance, normalized compile output, semantic diff, signature metadata, and tamper-detection tests.

Phase 3, Evidence Hub and Attestation, now includes signed evidence bundles, trust-root bundles, offline trust-root distribution packages, SIEM exports, retention controls, AWS/Azure immutable evidence storage references, SQLite and JSON evidence metadata search, governed artifact retrieval APIs for session and rollout evidence, console API wiring, and migration automation.

Phase 4, Approval Router, is complete for the current production-readiness slice. It includes JSON and SQLite approval persistence, default and repository-specific routing, claims-based approval authorization, signed OIDC/JWKS validation, repository RBAC, Entra/Okta OIDC-RBAC deployment references, provider payload and request-spec exports, secret-backed live provider delivery, console approval queue actions, console break-glass creation, approval audit detail views, and approval evidence linkage.

Phase 5, Agent Registry and MCP Trust Registry, is complete for the current production-readiness slice. It includes JSON and SQLite governed agent identities, MCP server trust records, predefined agent capability profiles, MCP capability classification, API and CLI access, console registry views, and registry-backed MCP runtime decisions.

Phase 6, Console and Persistent API, has started. It now includes JSON and SQLite activity persistence for sessions and decisions, repository inventory and policy rollout persistence, policy-pack authoring previews, approval-bound signed policy publishing, rollout change workflows, production deployment validation, integration inventory persistence, evidence artifact retrieval views, persistent API backup/restore/retention operations, policy rollout drill-downs, read-only console security boundary reporting, authenticated console sessions, RBAC-enforced console mutations, decision search filters, session summaries, and console Activity Explorer plus repository/rollout/integration views.

Phase 7, Go Enforcement Plane, has started with a bounded parity scaffold. It includes a Go module, runtime evaluator, CLI entrypoint, compiled-policy JSON loader, generated Go enforcement contracts, typed release-governance evidence contract payloads, runner authentication contract payloads, daemon and CI runner examples, signed CI runner bundle metadata, reusable release-governance runner wrappers, a GitHub composite runner action, HMAC-signed runner authentication claims, CI-provider OIDC JWT runner verification, provider-native OIDC token acquisition for GitHub Actions, GitLab CI, and Azure Pipelines wrappers, runner/evidence key custody documentation, hash-chained HMAC-signed daemon evidence streams, daemon evidence verifier CLI support, Unix-socket daemon transport, reusable daemon client helper, CLI `--daemon` mode, daemon lifecycle `start/status/stop`, request/response evidence hooks, runtime evidence references, trust-registry JSON loading, registry-backed MCP decisions, all-bundled-policy compiled parity, high-risk command and cloud/IaC parity for Cloud IAM, Kubernetes, Terraform/OpenTofu, GitHub, OWASP command-injection, and transparent delivery controls, Python/Go release governance parity for approvals, delivery failures, endpoint publication, inventory freshness, reconciliation drift, SLA reports, handoff status, rollout evidence verification, rollout artifact integrity, promotion audit export contract fixtures, and rollback audit export contract fixtures, signed release package workflow, SBOM generation, reproducibility manifests, release signing operations metadata, SLSA provenance, signed installer metadata, managed endpoint deployment manifests, release channel manifests, managed workstation updater policy, release-channel promotion approvals, Jamf/Intune/Linux endpoint-management export bundles, release channel promotion and endpoint export history views, governed endpoint export artifact downloads, checksum-enforced endpoint export integrity, endpoint export publication records, Jamf/Intune/Linux connector delivery, endpoint publication history dashboards, endpoint inventory ingestion, endpoint inventory freshness SLA reports, reconciliation automation from ingested inventory, managed endpoint reconciliation, endpoint drift dashboards, approval-bound endpoint drift remediation plans, approved remediation execution records, endpoint remediation handoff packages, endpoint remediation handoff status reconciliation, endpoint remediation SLA and executive reporting, endpoint remediation SLA notification delivery with routing policies, acknowledgements, duplicate suppression, escalation ladders, owner-specific SLOs, escalation delivery actions, owner review workflows, recurrence policies, owner calendars, maintenance-window suppression, recurrence delivery batching, suppression audit exports, recurrence retry policies, owner digest notifications, suppression trend analytics, Evidence Console recurrence operations filters and export drill-downs, scheduled recurrence automation worker runs, Evidence Console recurrence automation worker history, recurrence automation deployment templates, recurrence automation health reporting, recurrence automation health alert delivery and acknowledgements, managed endpoint rollout evidence capture, rollout evidence verification and indexing, rollout evidence search filters and console/API views, governed rollout artifact retrieval, rollout artifact integrity status, promotion readiness indicators, signed promotion approval requests, approved promotion execution records, promotion execution search and audit drill-downs, rollback evidence links, approved rollback execution records, SIEM/ITSM promotion audit exports, connector delivery for promotion audit and rollback execution records, persisted release connector delivery history, alerting dashboard summaries, installer smoke validation, GitHub keyless OIDC attestations, offline trust bootstrap metadata, air-gapped zip verification, release-candidate upgrade validation, release evidence, GitHub Release asset attachment, verifier CLI support, shared critical decision fixture, Python and Go parity tests, a dedicated `go-runtime-parity` CI job, Go test execution in the required governance check, an explicitly opt-in Go backend path with CLI/API readiness reports, production-readiness evidence, shadow/enforce/promoted modes, audited Python fallback, deployment readiness checks for CI runner and workstation rollout metadata, a promotion gate requiring approved audited parity evidence, rollback controls requiring an approved path back to Python-only mode, rollback rehearsal evidence with console visibility, fresh rollback drill history, recurring rollback drill scheduling, and stale-drill notification delivery before Go is selected as an optional backend.

Phase 8, Enterprise Integrations, has started with a GitHub required-check workflow, reusable GitHub Actions templates, GitLab CI and Azure Pipelines enforcement examples, CI evidence artifact upload for branch protection, approval-bound policy write-back, live SIEM/ITSM/ChatOps connector execution hooks, AWS/Azure immutable evidence storage references, and Entra/Okta OIDC-RBAC deployment references.

Phase 9, Public Sandbox, has started with a GitHub Pages deployment workflow for the Before the Agent Acts sandbox and evidence console. GitHub Pages is enabled for Actions publishing, and the public sandbox URL is `https://huzefaaa2.github.io/cavra/`. The workflow now includes packaged downloadable sample evidence, optional API configuration for backend-driven scenario runs, and post-deploy smoke validation for the page, JavaScript, stylesheet, brand assets, C4 diagram, and evidence JSON.

Transparent CAVRA engineering-agent methodology is now documented for the repository. It defines bot identities, agent roles, branch conventions, approval gates, evidence requirements, and the rule that CAVRA must never use fake human identities.

## Primary Pages

- White Paper: `White-Paper.md`
- CAVRA Productization Report: `CAVRA-Productization-Report.md`
- Open-Core Implementation Plan: `Open-Core-Implementation-Plan.md`
- Go Reproducible Air-Gapped Builds: `Go-Reproducible-Airgap-Builds.md`
- Release Signing Operations: `Release-Signing-Operations.md`
- High-Risk Command And Cloud/IaC Parity: `High-Risk-Command-Cloud-IaC-Parity.md`
- Edition Boundaries: `Edition-Boundaries.md`
- Private Enterprise Repo Plan: `Private-Enterprise-Repo-Plan.md`
- Production Roadmap: `Production-Roadmap.md`
- Recurrence Automation Deployment: `Recurrence-Automation-Deployment.md`
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
- Runner Auth and Evidence Key Custody: `Runner-Auth-And-Evidence-Key-Custody.md`
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
- Go Backend Pilot: `Go-Backend-Pilot.md`
- Go Backend Deployment Readiness: `Go-Backend-Deployment-Readiness.md`
- Go Backend Promotion Gate: `Go-Backend-Promotion.md`
- Go Backend Rollback Controls: `Go-Backend-Rollback.md`
- Go Backend Rollback Rehearsal Evidence: `Go-Backend-Rollback-Rehearsal.md`
- Go Backend Rollback Drill History: `Go-Backend-Rollback-Drill-History.md`
- Go Backend Rollback Drill Scheduling: `Go-Backend-Rollback-Drill-Scheduling.md`
- Go Backend Rollback Drill Notification Escalation: `Go-Backend-Rollback-Drill-Notification-Escalation.md`
- Go Backend Rollback Drill Routing: `Go-Backend-Rollback-Drill-Routing.md`
- Go Backend Rollback Drill Console: `Go-Backend-Rollback-Drill-Console.md`
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
