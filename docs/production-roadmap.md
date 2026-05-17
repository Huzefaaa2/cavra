# CAVRA Production Roadmap

This roadmap turns the CAVRA product thesis into implementation phases. It is priority-based, not calendar-based. Each phase must finish with README updates, wiki updates, diagrams, user stories, validation evidence, and a clear next-phase recommendation.

Transparent CAVRA engineering agents may execute implementation work for these phases only when their bot identities, branch names, approval gates, and evidence are explicit. Fake human identities are prohibited. The agent operating model is documented in `docs/transparent-agent-methodology.md`.

## Product North Star

CAVRA becomes the enterprise runtime authority layer for AI coding agents. Enterprises can safely adopt Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, AWS Q Developer, MCP tools, Terraform, Kubernetes, cloud CLI, and AI-assisted CI/CD because CAVRA governs sensitive agent actions before execution and produces audit-ready evidence after every decision.

## Phase 1: Productization Foundation

Status: complete in PR #1.

Goal: establish CAVRA identity, CLI, MCP path, core runtime guards, policy packs, API contract, sandbox, Docker assets, and enterprise documentation.

Delivered:
- CAVRA package and CLI.
- `cavra-mcp-server`.
- `cavra init claude-code`.
- Runtime decisions for files, commands, Git, MCP, and PR attestation.
- Baseline and regulated policy packs.
- FastAPI app contract.
- Before the Agent Acts sandbox.
- Docker and Docker Compose validation.

Exit criteria:
- Tests pass.
- Docker image and Compose start.
- Brand validation has no old visible product identity.
- README and wiki-ready pages describe the completed capabilities.

## Phase 2: Policy Engine Hardening

Status: complete in PR #1.

Goal: make policy behavior trustworthy enough for regulated pilots.

Delivered:
- Strict JSON Schema validation for all policy packs.
- Policy inheritance and override resolution.
- Policy test fixtures for validation, inheritance, diff, and signature tamper detection.
- `cavra policy diff` with semantic rule comparison.
- Policy compile output with stable normalized JSON.
- Policy signature metadata.
- Policy verification with digest tamper detection.

Remaining deeper hardening:
- Public/private key signing support.
- Audit-only, enforce, strict regulated, and break-glass modes.
- Golden decision snapshot suite.

User stories:
- As a platform engineer, I can validate a policy pack before rollout.
- As a CISO, I can prove a repository uses an approved policy version.
- As an auditor, I can verify that a policy was not modified after approval.

Enterprise challenge solved:
- Prevents unmanaged policy drift and creates a defensible governance baseline.

Exit criteria:
- All policy packs pass schema validation.
- Inheritance tests cover enterprise, business-unit, repository, and exception layers.
- Signed policy verification passes in CLI and Docker.

## Phase 3: Evidence Hub and Attestation

Status: in progress in PR #1.

Goal: make evidence tamper-resistant, portable, and review-ready.

Delivered:
- Evidence bundle builder with manifest, checksums, and optional signatures.
- PR attestation markdown and JSON export with risk summary.
- SIEM event format for Splunk, Sentinel, Datadog, and generic webhooks.
- Compliance mapping report per policy pack.
- Provider-specific SIEM export payloads for Splunk HEC, Microsoft Sentinel, Datadog, and generic webhooks.
- Immutable evidence storage reference plans for S3 Object Lock and Azure immutable blob.
- Ed25519 manifest signatures and evidence keypair generation.
- Evidence retention policy artifacts and minimum-retention verification.
- Evidence metadata indexing through CLI and API endpoints.
- Evidence key IDs, trust-root verification, and key rotation guidance.
- SQLite-backed evidence metadata search with filters and pagination.
- PR attestation verifier output.
- Hosted console views for evidence search and attestation verification.
- Initial SQLite migration for evidence metadata.
- Console API wiring for same-origin and cross-origin deployments.
- JSON and SQLite evidence search pagination/filter parity.
- Idempotent SQLite migration automation through `cavra evidence migrate`.
- Automated trust-root bundle generation and distribution guidance.

Remaining:
- Hosted attestation artifact download APIs backed by governed object storage.
- Production deployment guide validation.

User stories:
- As an auditor, I can download a complete evidence bundle for an AI-agent session.
- As a security engineer, I can send CAVRA decisions to my SIEM.
- As a reviewer, I can see why an AI-generated PR was allowed or blocked.

Enterprise challenge solved:
- Converts AI-agent activity into audit-ready evidence before high-risk changes reach production.

Exit criteria:
- Evidence schema validates.
- Generated bundle verifies checksums.
- PR attestation and SIEM sample exports are covered by tests.

## Phase 4: Approval Router

Status: in progress.

Goal: route risky actions to the right human approvers without blocking safe work.

Implement:
- Approval request model and JSON persistence. Delivered.
- CLI and API approval queue. Delivered.
- Approve, deny, expire, and break-glass lifecycle states. Delivered.
- Approval outcomes reflected in evidence metadata and PR attestations. Delivered.
- Approver groups and routing policies. Next.
- SQLite approval persistence. Next.
- Jira and ServiceNow reference connectors. Next.
- Slack and Teams notification reference connectors. Next.
- Console approval views. Next.

User stories:
- As an IAM owner, I receive approval requests for privilege expansion.
- As a change manager, I can see which AI-agent actions are waiting for approval.
- As a developer, I can continue safe actions while risky actions wait.

Enterprise challenge solved:
- Preserves human oversight for regulated workflows without banning AI-assisted engineering.

Exit criteria:
- Approval queue works through CLI and API.
- Approval decisions are reflected in evidence.
- Break-glass flow requires justification and generates audit records.

## Phase 5: Agent Registry and MCP Trust Registry

Goal: make agents and tools governed identities, not anonymous processes.

Implement:
- Agent registry models and API.
- Agent capability profiles for Claude Code, Codex, Copilot, Cursor, Gemini CLI, and AWS Q Developer.
- MCP server registry with trust tier, capabilities, owner, approval state, and last seen.
- MCP tool classification for filesystem, shell, network, database, SaaS, and cloud.
- Unknown MCP server default-deny mode.

User stories:
- As an AI governance lead, I can see which agents are active and what they are allowed to do.
- As a platform engineer, I can approve trusted MCP servers once and reuse that trust across repos.
- As a security engineer, I can block unknown filesystem tools by default.

Enterprise challenge solved:
- Removes identity ambiguity and MCP tool sprawl.

Exit criteria:
- Registry CRUD works through API and CLI.
- MCP decisions use registry trust state.
- Unknown filesystem MCP server remains blocked in tests.

## Phase 6: Console and Persistent API

Goal: provide the first enterprise console backed by durable data.

Implement:
- Database-backed FastAPI service.
- Repositories, sessions, decisions, agents, approvals, evidence, policy packs, integrations, and MCP trust endpoints.
- Minimal console UI for dashboards, sessions, decisions, approvals, policies, evidence, integrations, MCP trust, and agent registry.
- OIDC-ready auth boundary and RBAC model.

User stories:
- As a CISO, I can view blocked and approved AI-agent actions across repositories.
- As a platform team, I can manage policy packs and rollout status centrally.
- As an auditor, I can search decisions and evidence by repo, agent, rule, and timeframe.

Enterprise challenge solved:
- Turns local enforcement events into enterprise operational visibility.

Exit criteria:
- API has persistent storage.
- Console can browse decisions and evidence.
- RBAC model is documented and covered by tests.

## Phase 7: Go Enforcement Plane

Goal: add low-latency local and CI enforcement without replacing the Python management plane.

Implement:
- Generated protobuf clients.
- Go runtime service for file, command, Git, and MCP decisions.
- Unix-socket or gRPC local interface.
- CI runner integration mode.
- Parity tests between Python and Go decisions.
- Air-gapped single-binary packaging.

User stories:
- As a developer, I can run local enforcement with minimal latency.
- As a CI owner, I can enforce CAVRA decisions inside runners.
- As a public-sector platform team, I can deploy a single binary in an air-gapped environment.

Enterprise challenge solved:
- Makes enforcement fast, portable, and operationally acceptable for large engineering fleets.

Exit criteria:
- Go parity tests pass for all critical decisions.
- CLI can select Python or Go backend.
- Air-gapped binary build is reproducible.

## Phase 8: Enterprise Integrations

Goal: make CAVRA fit enterprise SDLC, security, identity, and audit workflows.

Implement:
- GitHub App orchestrator for transparent CAVRA agent roles.
- GitHub App and required status check.
- GitLab CI and Azure DevOps templates.
- Splunk, Sentinel, Datadog, Jira, ServiceNow, Slack, Teams, and webhook exporters.
- Entra ID and Okta OIDC reference implementation.
- SAML placeholder and RBAC policy model.
- Immutable evidence store reference deployments.

User stories:
- As a GitHub Enterprise admin, I can require CAVRA attestation before merge.
- As a SOC analyst, I can investigate blocked AI-agent actions in SIEM.
- As a change manager, I can map approvals to existing ITSM workflows.

Enterprise challenge solved:
- CAVRA becomes part of existing enterprise controls instead of another isolated security tool.

Exit criteria:
- GitHub required check demo works.
- SIEM and ITSM sample exports are tested.
- Identity docs include deployable OIDC configuration.

## Phase 9: Public Sandbox and Growth Loop

Goal: make CAVRA understandable in under three minutes.

Implement:
- Hosted sandbox deployment workflow.
- Backend-driven sandbox runs using the real policy engine.
- Downloadable evidence, PR attestation, and compliance reports.
- Persona-specific narratives for Developer, CISO, Platform Engineer, and Auditor.
- Install for Claude Code CTA and measurement hooks.

User stories:
- As a prospect, I can run the demo without credentials or cloud spend.
- As a CISO, I can see the business impact of each decision.
- As a developer, I can copy the Claude Code install command from the sandbox.

Enterprise challenge solved:
- Accelerates security review and design-partner conversations.

Exit criteria:
- Sandbox deploys from CI.
- Evidence downloads work.
- README and wiki link to the public sandbox URL.

## Phase 10: Production Readiness and Release

Goal: make CAVRA ready for enterprise pilots.

Implement:
- SBOM generation.
- Signed releases.
- Vulnerability disclosure workflow.
- Security scan and dependency audit CI.
- Backup and restore docs.
- Upgrade and migration docs.
- SOC 2 readiness roadmap.
- Performance, concurrency, and load tests.

User stories:
- As procurement, I can review deployment, support, data flow, privacy, and security posture.
- As an enterprise architect, I can deploy CAVRA self-hosted or air-gapped.
- As a security team, I can validate release integrity.

Enterprise challenge solved:
- Reduces enterprise adoption friction and procurement risk.

Exit criteria:
- Release artifacts are signed.
- SBOM is generated in CI.
- Production deployment guide is validated.

## What Should Be Implemented Next

Next recommended implementation phase: Phase 4, Approval Router, with a narrow Phase 3 follow-up for hosted attestation artifact downloads.

Rationale: CAVRA now has a working CLI, MCP path, policy packs, Docker validation, sandbox, strict policy validation, policy inheritance, semantic diff, normalized compile output, evidence bundles, HMAC and Ed25519 signatures, SIEM exports, retention artifacts, immutable storage plans, trust roots, trust-root bundles, SQLite and JSON evidence search, PR attestation verification, hosted console views, idempotent SQLite migration automation, console API wiring, and API metadata persistence.

Immediate next tasks:
- Add routing policies that map rule IDs, targets, severities, and policy packs to approver groups.
- Add SQLite approval persistence and migration automation.
- Add console approval queue views and action buttons.
- Add reference notification payloads for Slack, Teams, Jira, and ServiceNow.
