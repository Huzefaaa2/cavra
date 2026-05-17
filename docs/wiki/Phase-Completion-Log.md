# Phase Completion Log

## Phase 1: Productization Foundation

Status: complete.

Completed:
- CAVRA identity and README.
- Python package rename to `cavra`.
- CLI command `cavra`.
- MCP command `cavra-mcp-server`.
- Claude Code setup command `cavra init claude-code`.
- Runtime decisions for file, command, Git, MCP, and PR attestation.
- Regulated policy packs.
- FastAPI app contract.
- Before the Agent Acts sandbox.
- Docker image and Compose validation.
- Enterprise docs and wiki-ready pages.

Validation:
- `python3 -m pytest -q` passed.
- Docker image build passed.
- Docker CLI and MCP commands passed.
- Docker Compose API and sandbox startup passed.
- Brand validation passed.

## Next Phase

Phase 2: Policy Engine Hardening.

Status: complete.

Completed:
- Strict JSON Schema validation for CAVRA policy packs.
- Policy inheritance through `metadata.inherits`.
- Normalized compiled policy output.
- Semantic policy diff output.
- Policy signature metadata.
- Policy verification with tamper detection.
- Tests for validation, inheritance, diff, and signatures.

## Next Phase

Phase 3: Evidence Hub and Attestation.

Status: complete for the current production-readiness slice.

Completed:
- Evidence bundle manifest generation.
- Bundle checksums.
- Optional HMAC manifest signature.
- PR attestation output.
- Compliance mapping output.
- SIEM event output.
- Evidence verification command.
- Splunk HEC, Microsoft Sentinel, Datadog, and generic webhook SIEM export payloads.
- S3 Object Lock and Azure immutable blob immutable storage reference plans.
- Ed25519 evidence manifest signatures and key generation.
- Evidence retention policy artifacts and minimum-retention verification.
- Evidence metadata indexing and API persistence.
- More elaborate C4 container diagram for enterprise architecture review.
- Evidence key IDs, trust-root verification, and rotation guidance.
- SQLite-backed evidence metadata search with filters and pagination.
- PR attestation verification reports.
- Hosted evidence console views for search and PR attestation verification.
- Initial SQLite migration for evidence metadata.
- Console API wiring for same-origin and cross-origin deployments.
- JSON and SQLite evidence search filter/pagination parity.
- Idempotent SQLite migration automation with `cavra evidence migrate`.
- Trust-root bundle generation and enterprise distribution guidance.

Recommended next issue: continue Phase 5 with SQLite registry migrations, console registry views, predefined agent capability profiles, and MCP tool classification. Keep a narrow Phase 3 follow-up for hosted attestation artifact downloads backed by governed object storage.

## Phase 4: Approval Router

Status: in progress.

Completed:
- Approval request model and JSON persistence.
- API approval queue with list, create, fetch, approve, deny, expire, attach-decision, and break-glass endpoints.
- CLI approval queue with create, list, approve, deny, expire, and break-glass commands.
- Mandatory reason, actor, approver group, expiry, and optional external reference for break-glass overrides.
- Approval outcome linkage into evidence metadata and PR attestations.
- Default approver group routing policies.
- SQLite approval persistence and migration.
- Slack, Teams, Jira, ServiceNow, and webhook reference payload exports.
- Console approval queue view.
- Repository-specific JSON/YAML routing configuration.
- Claims-based approval authorization for local OIDC-style actor claims.
- Signed OIDC/JWKS token validation with issuer, audience, expiry, and not-before checks.
- Repository RBAC policy files with group mappings and repository-scoped approval permissions.
- Credential-free Slack, Teams, Jira, ServiceNow, and webhook request specs.
- Secret-backed live provider delivery with retry, timeout, and redacted delivery evidence.
- Console approval actions for approve, deny, and expire.
- Console break-glass creation.
- Approval audit detail views for lifecycle history, evidence references, decision context, and external references.

Recommended next issue: start Phase 5 with agent registry models/API, MCP server trust tiers, capability metadata, approval state, last-seen metadata, and registry-backed runtime decisions. Keep hosted attestation artifact retrieval as a narrow Phase 3 follow-up.

## Phase 5: Agent Registry and MCP Trust Registry

Status: complete for the current production-readiness slice.

Completed:
- JSON-backed registry store for governed AI-agent identities.
- Agent records with ID, type, vendor, version, capabilities, scopes, allowed repositories, allowed tools, risk tier, owner, status, last seen, and evidence references.
- MCP server trust records with server ID, trust tier, capabilities, owner, approval state, approved tools, last seen, and evidence references.
- CLI commands for registering and listing agents and MCP servers.
- API endpoints for `/agents`, `/agents/{agent_id}`, `/mcp/servers`, `/mcp/servers/{server_id}`, and `/mcp/trust`.
- Registry-backed MCP runtime decisions for approved, unknown, blocked, pending, and out-of-scope MCP tool calls.
- Unknown MCP server default-deny behavior covered by tests.
- SQLite registry persistence and migration.
- Predefined agent capability profiles for Claude Code, Codex, Copilot, Cursor, Gemini CLI, and AWS Q Developer.
- MCP tool classification for filesystem, shell, network, database, SaaS, cloud, and repository capabilities.
- Console registry views for agent identities, MCP trust records, profiles, and classifications.

Recommended next issue: start Phase 6 with durable session and decision persistence, console session/decision views, API filters, and hosted attestation artifact retrieval.

## Phase 6: Console and Persistent API

Status: started.

Completed:
- JSON activity store for runtime sessions and decisions.
- SQLite activity store and migration.
- `POST /decisions` persistence with automatic session summary updates.
- `GET /decisions` filters for session, agent, repository, policy pack, outcome, severity, and action type.
- `GET /sessions` filters for agent, repository, policy pack, and state.
- Console Activity Explorer for persisted sessions and decisions.
- JSON and SQLite repository inventory stores.
- JSON and SQLite policy rollout stores.
- SQLite migration `005_repository_policy_rollout.sql`.
- `GET` and `POST` repository inventory API endpoints with provider, owner, policy pack, status, and risk-tier filters.
- `GET` and `POST` policy rollout API endpoints with repository, policy pack, state, mode, and owner filters.
- Console repository inventory and policy rollout views.
- `cavra ops stores` for persistent API store status.
- `cavra ops backup` for checksum-backed JSON and SQLite store backups.
- `cavra ops restore` for checksum-validated restore to test or live paths.
- `cavra ops retention-plan` for JSON and Markdown retention-control artifacts.
- Read-only `/operations/stores` and `/operations/retention-plan` API endpoints.

Recommended next issue: add integrations inventory persistence, policy-pack catalog drill-downs, OIDC-ready console auth/RBAC boundaries, and hosted attestation artifact retrieval.

## Transparent Agent Methodology Enablement

Status: complete.

Completed:
- Declarative CAVRA agent manifests for product, architect, backend, frontend, test, security, docs, reviewer, and release roles.
- Agent task issue template and agent label catalog.
- Conservative GitHub Actions orchestrator scaffold that validates transparent agent manifests.
- `cavra-agentic-delivery` policy pack for bot identity, branch naming, PR attestation, approvals, and documentation requirements.
- Transparent agent methodology docs, orchestration architecture docs, wiki pages, and SVG diagram.

Recommended next issue: implement the real GitHub App orchestrator backend only after protected branch checks, evidence verification, and human approval requirements are enforced.
