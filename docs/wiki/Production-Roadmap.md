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
- Hosted evidence artifact retrieval APIs for indexed sessions through a governed artifact root.
- Console evidence artifact panel and bundle download links.

Remaining:
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

Status: complete for the current production-readiness slice.

Goal: route risky actions to the right human approvers without blocking safe work.

Implement:
- Approval request model and JSON persistence. Delivered.
- CLI and API approval queue. Delivered.
- Approve, deny, expire, and break-glass lifecycle states. Delivered.
- Approval outcomes reflected in evidence metadata and PR attestations. Delivered.
- Default approver group routing policies. Delivered.
- SQLite approval persistence and migration. Delivered.
- Slack, Teams, Jira, ServiceNow, and webhook reference payloads. Delivered.
- Console approval queue view. Delivered.
- Repository-specific routing policy configuration. Delivered.
- Credential-free provider request specs for Slack, Teams, Jira, ServiceNow, and webhooks. Delivered.
- Secret-backed live provider delivery with retry, timeout, and redacted delivery evidence. Delivered.
- Approval RBAC and OIDC-style actor mapping. Delivered for local claims objects.
- Signed OIDC token validation with JWKS, issuer, audience, expiry, and not-before checks. Delivered.
- Repository RBAC policy files with group mappings and repository-scoped approval permissions. Delivered.
- Console approval actions for approve, deny, and expire. Delivered.
- Console break-glass creation. Delivered.
- Approval audit detail views. Delivered.

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

Status: complete for the current production-readiness slice.

Goal: make agents and tools governed identities, not anonymous processes.

Implement:
- Agent registry models and API. Delivered.
- Agent registry CLI commands. Delivered.
- MCP server registry with trust tier, capabilities, owner, approval state, and last seen. Delivered.
- MCP trust CLI commands. Delivered.
- Registry-backed runtime decisions for MCP tool calls. Delivered.
- Unknown MCP server default-deny mode. Delivered.
- Agent capability profiles for Claude Code, Codex, Copilot, Cursor, Gemini CLI, and AWS Q Developer. Delivered.
- MCP tool classification for filesystem, shell, network, database, SaaS, cloud, and repository capabilities. Delivered.
- SQLite registry persistence and migrations. Delivered.
- Console registry views. Delivered.

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
- Console can browse agent identities, MCP trust records, profiles, and capability classifications.

## Phase 6: Console and Persistent API

Status: started.

Goal: provide the first enterprise console backed by durable data.

Implement:
- JSON and SQLite activity persistence for sessions and decisions. Delivered.
- Activity session and decision API filters. Delivered.
- Console Activity Explorer for sessions and decisions. Delivered.
- Repository inventory and policy rollout JSON/SQLite persistence. Delivered.
- Repository and rollout API filters for owner, policy pack, status, risk tier, state, and mode. Delivered.
- Console repository inventory and policy rollout views. Delivered.
- Persistent API store status, backup, restore, and retention-plan operations. Delivered.
- Read-only operations API endpoints for store status and retention planning. Delivered.
- Integration inventory JSON/SQLite persistence. Delivered.
- Integration inventory API filters and console view. Delivered.
- Policy rollout detail API and console drill-downs. Delivered.
- Read-only console security boundary for OIDC, RBAC, and CORS readiness. Delivered.
- Authenticated console session endpoint with signed bearer-token validation. Delivered.
- RBAC enforcement for approval and break-glass console mutations. Delivered.
- Policy-pack catalog summaries and read-only authoring drafts. Delivered.
- Rollout change planning and apply workflows. Delivered.
- Production deployment readiness report. Delivered.
- Minimal console UI for dashboards, repositories, policies, evidence, integrations, MCP trust, and agent registry. In progress.

User stories:
- As a CISO, I can view blocked and approved AI-agent actions across repositories.
- As a platform team, I can manage policy packs and rollout status centrally.
- As an auditor, I can search decisions and evidence by repo, agent, rule, and timeframe.

Enterprise challenge solved:
- Turns local enforcement events into enterprise operational visibility.

Exit criteria:
- API has persistent storage.
- Console can browse sessions, decisions, and evidence.
- Console can list and download allowlisted evidence artifacts for indexed sessions.
- Console mutations require verified actor context when OIDC or RBAC is configured.
- Console can preview policy drafts, plan/apply rollout changes, and validate deployment readiness.
- RBAC model is documented and covered by tests.

## Phase 7: Go Enforcement Plane

Status: scaffold started.

Goal: add low-latency local and CI enforcement without replacing the Python management plane.

Implement:
- Go runtime service for file, command, Git, and MCP decisions. Scaffold delivered.
- Compiled-policy JSON loading from `cavra policy compile`. Delivered for mirrored filesystem, command, and MCP sections.
- Generated Go request and response types from the enforcement protobuf contract. Delivered as lightweight JSON transport contracts.
- Local Unix-socket daemon transport. Initial one-request-per-connection transport delivered.
- Reusable Go daemon client helper and CLI `--daemon` one-shot client mode. Delivered.
- Daemon lifecycle `start/status/stop` with PID-file tracking, socket readiness probing, and graceful signal cleanup. Delivered.
- Registry-backed MCP decisions from CAVRA trust-registry JSON. Delivered for approved, pending, blocked, tool-scope, and capability-scope outcomes.
- Runtime evidence reference metadata in Go decisions. Delivered.
- Parity tests between Python and Go decisions. Critical fixture scaffold expanded for approvals, evidence references, and registry-backed MCP decisions.
- All-bundled-policy compiled parity. Delivered with Python-to-Go CLI validation across every bundled policy pack.
- Signed Go release package workflow. Delivered with checksums, SPDX-style SBOM, SLSA provenance, detached Ed25519 signatures when configured, release evidence, GitHub Release asset attachment, and verifier CLI support.
- Signed CI runner binary packaging. Delivered with `cavra-runtime.ci-runner-bundles.json`, packaged release-governance runner wrappers, and verifier checks that bind wrappers to signed runtime binaries and CI deployment targets.
- Reusable runner actions. Delivered with a public-safe shell wrapper for GitHub Actions, GitLab CI, Azure Pipelines, and a GitHub composite action for typed release-governance daemon checks.
- Runner authentication. Delivered with `RunnerAuthentication` and `RunnerIdentity` contract payloads, `--runner-auth-key`, `--runner-auth-key-id`, `--runner-auth-claims`, and HMAC-signed CI runner claims.
- Signed daemon evidence streams. Delivered with `--evidence-signing-key`, `--evidence-signing-key-id`, sequence numbers, previous hashes, record hashes, and HMAC signatures for JSONL evidence records.
- CI-provider OIDC runner verification. Delivered with `OIDC-JWT`, `--runner-auth-oidc-token`, `--runner-auth-oidc-token-file`, `--runner-oidc-issuer`, `--runner-oidc-audience`, `--runner-oidc-jwks`, `--runner-oidc-jwks-url`, RS256/JWKS signature checks, issuer/audience/time validation, runner identity claim matching, and OIDC bearer token redaction from daemon evidence.
- Daemon evidence verifier CLI. Delivered with `--verify-evidence` for JSONL sequence validation, previous-hash checks, record-hash recomputation, signature key ID checks, and HMAC verification.
- Provider-native runner OIDC token acquisition. Delivered with wrapper support for GitHub Actions `ACTIONS_ID_TOKEN_REQUEST_URL`, GitLab `id_tokens`, Azure Pipelines `SYSTEM_OIDCREQUESTURI`, explicit token-file fallbacks, and evidence-verification artifact publication.
- Runner and evidence key custody. Delivered with `docs/runner-auth-evidence-key-custody.md` covering OIDC preference, HMAC fallback, key IDs, rotation cadence, JWKS trust, and release-governance evidence retention.
- CI runner integration mode. Initial `go-runtime-parity`, required-check execution, typed daemon examples, and packaged runner wrappers delivered.
- Unix-socket or gRPC local interface.
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

Delivered in the current slice:
- GitHub required-check workflow named `cavra-required-check`.
- GitHub Actions required-check template and stricter enterprise enforcement template.
- GitLab CI enforcement example.
- Azure Pipelines required-check template for Azure Repos Build validation branch policies.
- CI evidence artifact upload with evidence and PR attestation verification.
- Approval-bound signed policy publishing before write-back.
- AWS S3 Object Lock and Azure Blob immutability deployment references.
- Entra ID and Okta OIDC/RBAC deployment references.

Exit criteria:
- GitHub required check demo works.
- SIEM and ITSM sample exports are tested.
- Identity docs include deployable OIDC configuration.

## Phase 9: Public Sandbox and Growth Loop

Status: deployment workflow started.

Goal: make CAVRA understandable in under three minutes.

Implement:
- Hosted sandbox deployment workflow. Delivered for GitHub Pages from `main`.
- Public sandbox URL. Verified at `https://huzefaaa2.github.io/cavra/`.
- Static evidence packaging and post-deploy smoke validation for the public page and core assets.
- Public post-deploy smoke run. Passed from `main`.
- Backend-driven sandbox runs using the real policy engine. Delivered with optional API-backed Pages config, `/api/sandbox/run`, persisted evidence metadata, activity records, and telemetry-free public run counters from `/api/sandbox/metrics`.
- Downloadable evidence, PR attestation, and compliance reports.
- Persona-specific narratives for Developer, CISO, Platform Engineer, and Auditor.
- Install for Claude Code CTA and telemetry-free adoption counters.

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

Latest completed implementation phase: private Enterprise managed archive dashboard storage and live alert transports.

Next recommended implementation phase: add production deployment wiring for managed archive dashboard storage and live alert transport providers.

Rationale: CAVRA now has a working CLI, MCP path, policy packs, Docker validation, sandbox, strict policy validation, policy inheritance, semantic diff, normalized compile output, evidence bundles, HMAC and Ed25519 signatures, SIEM exports, live SIEM/ITSM/ChatOps connector execution hooks, retention artifacts, immutable storage plans and deployment references, trust roots, trust-root bundles, offline trust-root distribution packages, SQLite and JSON evidence search, PR attestation verification, governed evidence artifact retrieval, hosted console views, idempotent SQLite migration automation, console API wiring, API metadata persistence, approval workflows, JSON/SQLite registry-backed agent and MCP trust governance, activity persistence, repository inventory, policy rollout persistence, persistent API backup/restore/retention operations, integration inventory persistence, policy rollout drill-downs, read-only console security boundary reporting, authenticated console session validation, RBAC-enforced console mutations, Entra/Okta OIDC-RBAC deployment references, policy authoring previews, approval-bound signed policy publishing, rollout change workflows, production deployment readiness reporting, GitHub/GitLab/Azure DevOps required-check CI/CD enforcement templates, signed Go release packages attached to GitHub Releases, verifier CLI support, signed installer metadata, managed endpoint deployment manifests, signed CI runner bundle metadata, reusable release-governance runner wrappers, runner authentication claims, hash-chained daemon evidence signatures, a GitHub composite runner action, release channel manifests, managed workstation updater policy, release-channel promotion approvals, Jamf/Intune/Linux endpoint-management export bundles, release channel promotion request history, endpoint-management export history, Evidence Console release channel publishing views, governed endpoint export downloads, checksum-enforced endpoint export integrity, endpoint export publication records, Jamf/Intune/Linux connector delivery, endpoint publication history dashboards, endpoint inventory ingestion, endpoint inventory freshness SLA reporting, reconciliation automation from ingested inventory, managed endpoint reconciliation, endpoint drift dashboards, approval-bound endpoint drift remediation plans, approved remediation execution records, endpoint remediation handoff packages, endpoint remediation handoff status reconciliation, endpoint remediation SLA and executive reporting, endpoint remediation SLA notification delivery, notification routing policies, acknowledgement tracking, duplicate suppression windows, escalation ladders, owner-specific service-level objectives, escalation delivery actions, owner review workflows, recurrence policies, owner calendars, maintenance-window suppression, recurrence delivery batching, suppression audit exports, retry policies for failed recurrence batches, owner digest notifications, suppression trend analytics, managed endpoint rollout evidence capture, rollout evidence verification and indexing, rollout evidence search filters and console/API views, governed rollout artifact retrieval, rollout artifact integrity status, promotion readiness indicators, signed promotion approval requests, approved promotion execution records, promotion execution search and audit drill-downs, rollback evidence links, approved rollback execution records, SIEM/ITSM promotion audit exports, connector delivery for promotion audit and rollback execution records, persisted release connector delivery history, alerting dashboards, open-core Community/Enterprise/Trial/SaaS boundaries, installer smoke validation, SLSA provenance, GitHub keyless OIDC attestations, air-gapped zip verification, release-candidate upgrade validation, offline trust bootstrap metadata, vulnerability disclosure/release advisory documentation, backend-driven public sandbox scenario runs, public sandbox release-note links, telemetry-free public run counters from persisted backend metadata, rollback rehearsal evidence with console visibility and fresh rollback drill history for promoted Go backend pilots, acknowledgement audit delivery retry plans, scheduled acknowledgement audit delivery worker dry-runs, worker health alert delivery, retry acknowledgement records, retry execution approval plans, retry execution approval decisions, connector recovery playbooks, approval-bound live retry execution records, and connector recovery closure evidence.

Latest completed slice:
- Added managed database-backed archive health dashboard persistence through the tenant database adapter contract.
- Added a shared dashboard persistence protocol so JSON and managed database storage use the same API surface.
- Added live provider alert transport adapters for Slack, Teams, Splunk HEC, Jira, ServiceNow, and PagerDuty.
- Added webhook/no-token delivery support and runtime-auth provider delivery support for live transport adapters.
- Added tests for managed database dashboard persistence, provider-shaped payloads, webhook delivery, and runtime-auth delivery.

Immediate next tasks:
- Add production deployment wiring for managed archive dashboard storage and live alert transport providers.
