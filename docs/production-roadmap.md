# CAVRA Production Roadmap

This roadmap turns the CAVRA product thesis into implementation phases. It is priority-based, not calendar-based. Each phase must finish with README updates, wiki updates, diagrams, user stories, validation evidence, and a clear next-phase recommendation.

Transparent CAVRA engineering agents may execute implementation work for these phases only when their bot identities, branch names, approval gates, and evidence are explicit. Fake human identities are prohibited. The agent operating model is documented in `docs/transparent-agent-methodology.md`.

## Product North Star

CAVRA becomes the enterprise runtime authority layer for AI coding agents. Enterprises can safely adopt Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, AWS Q Developer, MCP tools, Terraform, Kubernetes, cloud CLI, and AI-assisted CI/CD because CAVRA governs sensitive agent actions before execution and produces audit-ready evidence after every decision.

## Current Enterprise Batch Sync

Status: public-safe documentation synchronized after private Enterprise PRs
#56-#60.

Delivered in the private Enterprise repository:
- managed database driver package health evidence and release rollup integration;
- object storage probe scheduling, worker evidence, retry planning, dashboard
  persistence, and release-readiness approval summaries;
- managed database driver health scheduling, worker evidence, retry planning,
  dashboard persistence, and release-readiness approval summaries;
- private MVP follow-up closeout for managed storage, KMS, object-lock, and
  managed database release-readiness evidence.

Current Trial and SaaS commercialization readiness status:
- public trial-to-pilot intake plan is delivered;
- public licensing interface hardening is delivered;
- public SaaS Control Plane contract is delivered with request/response
  boundaries for tenant status, license validation, policy lookup, and evidence
  export.
- private trial package readiness gates are delivered in `cavra-enterprise`
  PR #61;
- private customer pilot handoff evidence is delivered in `cavra-enterprise`
  PR #62.
- public tenant onboarding contract is delivered;
- public entitlement status contract is delivered;
- public hosted policy registry readiness contract is delivered;
- public tenant audit-store operating contract is delivered;
- public billing/subscription boundary documentation is delivered;
- private tenant onboarding readiness evidence is delivered in
  `cavra-enterprise` PR #63;
- private entitlement and license-service handoff evidence is delivered in
  `cavra-enterprise` PR #64;
- private paid-pilot promotion evidence is delivered in `cavra-enterprise`
  PR #65;
- private customer rollout closeout evidence is delivered in
  `cavra-enterprise` PR #66;
- private hosted policy registry readiness evidence is delivered in
  `cavra-enterprise` PR #67;
- private tenant audit-store operating evidence is delivered in
  `cavra-enterprise` PR #68;
- private SaaS operating readiness rollup evidence is delivered in
  `cavra-enterprise` PR #69;
- private billing and license-service observability evidence is delivered in
  `cavra-enterprise` PR #70;
- private support and customer-success operating handoff evidence is delivered
  in `cavra-enterprise` PR #71;
- private operating dashboard and support escalation rollup evidence is
  delivered in `cavra-enterprise` PR #72;
- private final SaaS customer operating closeout evidence is delivered in
  `cavra-enterprise` PR #73;
- private SaaS operating automation plan evidence is delivered in
  `cavra-enterprise` PR #74;
- private SaaS operating automation final closure, customer-success handoff,
  executive summary, release governance, and public contract sync evidence are
  delivered in `cavra-enterprise` PRs #81-#85;
- public-safe tenant, entitlement, and commercialization batch sync is
  documented in `docs/tenant-entitlement-commercialization-batch-sync.md`.
- public-safe post-onboarding SaaS operating batch sync is documented in
  `docs/post-onboarding-saas-operating-batch-sync.md`.
- public-safe SaaS customer operating closeout batch sync is documented in
  `docs/saas-customer-operating-closeout-batch-sync.md`.
- public-safe customer operating dashboard and support handoff contracts are
  documented in
  `docs/architecture/customer-operating-dashboard-support-handoff-contract.md`.
- public-safe SaaS operating automation worker handoff guidance is documented
  in `docs/architecture/saas-operating-automation-worker-handoff.md`.
- public-safe SaaS operating automation worker handoff contract model is
  delivered in Community Edition.
- public-safe API and CLI surfaces for the worker handoff contract model are
  delivered.
- public Evidence Console and sandbox UI exposure for the worker handoff
  contract model is delivered.
- private Enterprise trial package release pipeline is delivered in
  `cavra-enterprise` PR #86 and public-safe sync is documented in
  `docs/trial-enterprise-distribution-sync.md`.
- private trial license issuance and evaluator access evidence is delivered in
  `cavra-enterprise` PR #87 and public-safe sync is documented in
  `docs/trial-license-evaluator-access-sync.md`.
- private trial access expiry evidence is delivered in `cavra-enterprise`
  PR #88 and public-safe sync is documented in
  `docs/trial-access-expiry-sync.md`.
- private expired-trial follow-up automation evidence is delivered in
  `cavra-enterprise` PR #89 and public-safe sync is documented in
  `docs/trial-expired-followup-sync.md`.
- private trial conversion readiness evidence is delivered in
  `cavra-enterprise` PR #90 and public-safe sync is documented in
  `docs/trial-conversion-readiness-sync.md`.
- private paid-pilot activation and production-conversion handoff evidence is
  delivered in `cavra-enterprise` PR #91 and public-safe sync is documented in
  `docs/trial-conversion-activation-handoff-sync.md`.
- private conversion closeout and revenue handoff rollup evidence is delivered
  in `cavra-enterprise` PR #92 and public-safe sync is documented in
  `docs/trial-conversion-closeout-revenue-sync.md`.
- private conversion closeout executive summary and renewal action evidence is
  delivered in `cavra-enterprise` PR #93 and public-safe sync is documented in
  `docs/trial-conversion-executive-renewal-sync.md`.
- private conversion customer follow-through evidence is delivered in
  `cavra-enterprise` PR #94 and public-safe sync is documented in
  `docs/trial-conversion-customer-followthrough-sync.md`.
- private conversion renewal outcome rollup evidence is delivered in
  `cavra-enterprise` PR #95 and public-safe sync is documented in
  `docs/trial-conversion-renewal-outcome-rollup-sync.md`.
- private final commercial renewal closeout package evidence is delivered in
  `cavra-enterprise` PR #96 and public-safe sync is documented in
  `docs/trial-final-commercial-renewal-closeout-sync.md`.
- private trial commercialization closure readiness summary evidence is
  delivered in `cavra-enterprise` PR #97 and public-safe sync is documented in
  `docs/trial-commercialization-closure-readiness-sync.md`.
- private commercialization closure release acceptance evidence is delivered in
  `cavra-enterprise` PR #98 and public-safe sync is documented in
  `docs/trial-commercialization-closure-release-acceptance-sync.md`.
- private commercialization closure final closeout evidence is delivered in
  `cavra-enterprise` PR #99 and public-safe sync is documented in
  `docs/trial-commercialization-closure-final-closeout-sync.md`.
- private commercial launch-readiness handoff evidence is delivered in
  `cavra-enterprise` PR #100 and public-safe sync is documented in
  `docs/trial-commercial-launch-readiness-handoff-sync.md`.
- private commercial launch-readiness final approval evidence is delivered in
  `cavra-enterprise` PR #101 and public-safe sync is documented in
  `docs/trial-commercial-launch-readiness-final-approval-sync.md`.
- private commercial launch-readiness operating transition evidence is
  delivered in `cavra-enterprise` PR #102 and public-safe sync is documented in
  `docs/trial-commercial-launch-readiness-operating-transition-sync.md`.
- private commercial launch-readiness operating closeout evidence is delivered
  in `cavra-enterprise` PR #103 and public-safe sync is documented in
  `docs/trial-commercial-launch-readiness-operating-closeout-sync.md`.
- private commercial launch-readiness executive review evidence is delivered in
  `cavra-enterprise` PR #104 and public-safe sync is documented in
  `docs/trial-commercial-launch-readiness-executive-review-sync.md`.
- private commercial launch-readiness final archive evidence is delivered in
  `cavra-enterprise` PR #105 and public-safe sync is documented in
  `docs/trial-commercial-launch-readiness-final-archive-sync.md`.
- private production observability and support runbook readiness evidence is
  delivered in `cavra-enterprise` PR #106 and public-safe sync is documented in
  `docs/trial-production-observability-support-readiness-sync.md`.
- private final release hardening and packaging readiness evidence is
  delivered in `cavra-enterprise` PR #107 and public-safe sync is documented in
  `docs/trial-final-release-hardening-packaging-readiness-sync.md`.
- private commercialization closeout and release-to-market approval evidence
  is delivered in `cavra-enterprise` PR #108 and public-safe sync is
  documented in
  `docs/trial-commercialization-closeout-release-market-approval-sync.md`.
- private post-launch operating handoff evidence is delivered in
  `cavra-enterprise` PR #109 and public-safe sync is documented in
  `docs/trial-post-launch-operating-handoff-sync.md`.
- private release retrospective and roadmap intake evidence is delivered in
  `cavra-enterprise` PR #110 and public-safe sync is documented in
  `docs/trial-release-retrospective-roadmap-intake-sync.md`.
- private final launch retrospective closeout evidence is delivered in
  `cavra-enterprise` PR #111 and public-safe sync is documented in
  `docs/trial-final-launch-retrospective-closeout-sync.md`.

Latest production-readiness slice: Community GA Control Hardening delivered
Ed25519 policy signing, golden decision snapshots, explicit runtime modes,
deployment validation updates, and public docs/wiki sync. See
`docs/community-ga-control-hardening-sync.md`.
Evidence Console closeout now surfaces the Community GA controls in the hosted
operator UI. See `docs/evidence-console-community-ga-closeout.md`.
Community GA release checklist documentation is now available at
`docs/community-ga-release-checklist.md`.
Community GA release packet template documentation and schema are now available
at `docs/community-ga-release-packet-template.md`,
`docs/release-packets/community-ga-release-packet.schema.json`, and
`examples/release-packets/community-ga-release-packet.example.json`.
Community GA dry-run release packet documentation is now available at
`docs/release-packets/community-ga-dry-run-2026-06-04.md` and
`docs/release-packets/community-ga-dry-run-2026-06-04.json`.
Automated Community GA release packet JSON schema validation is now available at
`scripts/validate-release-packets.py` and runs in Community CI, security scan,
release-community, and `cavra-required-check` workflows.
Community GA v0.1.0 release packet documentation is now available at
`docs/release-packets/community-ga-v0.1.0.md` and
`docs/release-packets/community-ga-v0.1.0.json`.
Community GA v0.1.0 is published at
`https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0` with source
distribution and wheel artifacts attached. Publication details are documented in
`docs/community-ga-v0.1.0-release-publication.md`.
Community GA v0.1.0 post-release verification is now documented at
`docs/release-verifications/community-v0.1.0-post-release-verification.md`,
with reusable verification automation in
`scripts/verify-community-release-artifacts.py` and
`.github/workflows/verify-community-release.yml`.
Community maintenance-release governance is now documented at
`docs/community-maintenance-release-checklist.md` and
`docs/community-maintenance-release-evidence-template.md`, with schema
validation in
`docs/release-verifications/community-maintenance-release.schema.json`,
`examples/release-verifications/community-maintenance-release.example.json`, and
`scripts/validate-maintenance-release-evidence.py`.
Community release-note freshness validation is now documented at
`docs/community-release-note-freshness.md` and enforced by
`scripts/validate-community-release-note-freshness.py` in Community CI, security
scan, release-community, and `cavra-required-check`.
Community v0.1.1 maintenance-release dry-run evidence is now documented at
`docs/releases/community-v0.1.1.md` and
`docs/release-verifications/community-v0.1.1-maintenance-verification.md`.
Community release index documentation is now available at
`docs/community-release-index.md`.
Community release index freshness validation is now documented at
`docs/community-release-index-freshness.md` and enforced by
`scripts/validate-community-release-index.py`.
Community release readiness dashboard documentation is now available at
`docs/community-release-readiness-dashboard.md`.
The GitHub Pages sandbox has been redesigned into a Backstage-style CAVRA
developer portal, documented at `docs/sandbox-portal-redesign.md`.
Next recommended slice: add a Community release readiness dashboard validator
that checks dashboard rows, release links, freshness controls, verification
commands, README navigation, wiki navigation, and publication state.
Public Community source remains free of Enterprise implementation details.

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

Latest completed implementation phase: private Enterprise managed infrastructure release-readiness follow-up closeout.

Next recommended implementation phase: continue the Trial and SaaS commercialization readiness slice with the public SaaS Control Plane contract.

Rationale: CAVRA now has a working CLI, MCP path, policy packs, Docker validation, sandbox, strict policy validation, policy inheritance, semantic diff, normalized compile output, evidence bundles, HMAC and Ed25519 signatures, SIEM exports, live SIEM/ITSM/ChatOps connector execution hooks, retention artifacts, immutable storage plans and deployment references, trust roots, trust-root bundles, offline trust-root distribution packages, SQLite and JSON evidence search, PR attestation verification, governed evidence artifact retrieval, hosted console views, idempotent SQLite migration automation, console API wiring, API metadata persistence, approval workflows, JSON/SQLite registry-backed agent and MCP trust governance, activity persistence, repository inventory, policy rollout persistence, persistent API backup/restore/retention operations, integration inventory persistence, policy rollout drill-downs, read-only console security boundary reporting, authenticated console session validation, RBAC-enforced console mutations, Entra/Okta OIDC-RBAC deployment references, policy authoring previews, approval-bound signed policy publishing, rollout change workflows, production deployment readiness reporting, GitHub/GitLab/Azure DevOps required-check CI/CD enforcement templates, signed Go release packages attached to GitHub Releases, verifier CLI support, signed installer metadata, managed endpoint deployment manifests, signed CI runner bundle metadata, reusable release-governance runner wrappers, runner authentication claims, hash-chained daemon evidence signatures, a GitHub composite runner action, release channel manifests, managed workstation updater policy, release-channel promotion approvals, Jamf/Intune/Linux endpoint-management export bundles, release channel promotion request history, endpoint-management export history, Evidence Console release channel publishing views, governed endpoint export downloads, checksum-enforced endpoint export integrity, endpoint export publication records, Jamf/Intune/Linux connector delivery, endpoint publication history dashboards, endpoint inventory ingestion, endpoint inventory freshness SLA reporting, reconciliation automation from ingested inventory, managed endpoint reconciliation, endpoint drift dashboards, approval-bound endpoint drift remediation plans, approved remediation execution records, endpoint remediation handoff packages, endpoint remediation handoff status reconciliation, endpoint remediation SLA and executive reporting, endpoint remediation SLA notification delivery, notification routing policies, acknowledgement tracking, duplicate suppression windows, escalation ladders, owner-specific service-level objectives, escalation delivery actions, owner review workflows, recurrence policies, owner calendars, maintenance-window suppression, recurrence delivery batching, suppression audit exports, retry policies for failed recurrence batches, owner digest notifications, suppression trend analytics, managed endpoint rollout evidence capture, rollout evidence verification and indexing, rollout evidence search filters and console/API views, governed rollout artifact retrieval, rollout artifact integrity status, promotion readiness indicators, signed promotion approval requests, approved promotion execution records, promotion execution search and audit drill-downs, rollback evidence links, approved rollback execution records, SIEM/ITSM promotion audit exports, connector delivery for promotion audit and rollback execution records, persisted release connector delivery history, alerting dashboards, open-core Community/Enterprise/Trial/SaaS boundaries, installer smoke validation, SLSA provenance, GitHub keyless OIDC attestations, air-gapped zip verification, release-candidate upgrade validation, offline trust bootstrap metadata, vulnerability disclosure/release advisory documentation, backend-driven public sandbox scenario runs, public sandbox release-note links, telemetry-free public run counters from persisted backend metadata, rollback rehearsal evidence with console visibility and fresh rollback drill history for promoted Go backend pilots, acknowledgement audit delivery retry plans, scheduled acknowledgement audit delivery worker dry-runs, worker health alert delivery, retry acknowledgement records, retry execution approval plans, retry execution approval decisions, connector recovery playbooks, approval-bound live retry execution records, and connector recovery closure evidence.

Latest completed slice:
- Added managed tenant database driver health evidence and release rollup integration.
- Added object storage probe scheduling, retry evidence, dashboards, persistence, and release-readiness approvals.
- Added managed database driver health scheduling, retry evidence, dashboards, persistence, and release-readiness approvals.
- Closed the active private MVP follow-up batch with provider credentials, customer metadata, Enterprise source code, and production driver implementation details kept outside the public Community repository.

Immediate next tasks:
- Reconcile the public roadmap, wiki-ready pages, and README with private PRs #56-#60.
- Define public SaaS Control Plane request and response shapes for tenant status, license validation boundaries, policy registry lookup, and evidence export without implementing private SaaS services.
