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
- AWS S3 Object Lock and Azure Blob immutability deployment references.
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

Recommended next issue: continue Phase 5 with SQLite registry migrations, console registry views, predefined agent capability profiles, and MCP tool classification. Evidence artifact retrieval is now delivered in Phase 6.

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

Recommended next issue: start Phase 5 with agent registry models/API, MCP server trust tiers, capability metadata, approval state, last-seen metadata, and registry-backed runtime decisions. Evidence artifact retrieval is now delivered in Phase 6.

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

Recommended next issue: start Phase 6 with durable session and decision persistence, console session/decision views, API filters, and governed evidence artifact retrieval.

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
- JSON and SQLite integration inventory stores.
- SQLite migration `006_integrations_inventory.sql`.
- `GET` and `POST` integration inventory API endpoints with provider, category, status, owner, environment, and health filters.
- Console Enterprise Integrations inventory view.
- Policy rollout detail API and console drill-downs.
- Read-only `/console/security-boundary` endpoint.
- Console security boundary panel for OIDC, RBAC, CORS, permissions, and operator notes.
- Governed evidence artifact retrieval APIs for indexed sessions.
- Console evidence artifact panel with individual artifact and bundle download links.
- `GET /console/session` for signed bearer-token validation.
- RBAC-enforced approval and break-glass console mutations when OIDC or RBAC is configured.
- Console Session panel for actor, group, permission, and repository-scope visibility.
- `GET /policy-pack-catalog` and `POST /policy-packs/draft` for read-only policy authoring previews.
- `POST /policy-packs/publish-plan`, `POST /policy-packs/publish-request`, and `POST /policy-packs/publish` for approval-bound signed policy write-back.
- `POST /policy-rollouts/change-plan` and `POST /policy-rollouts/apply-change` for governed rollout transitions.
- `GET /deployment/production-readiness` and console Production Readiness panel.

Recommended next issue: delivered below as the Phase 7 scaffold and Phase 9 deployment workflow.

## Phase 7: Go Enforcement Plane

Status: scaffold started.

Completed:
- Go module under `go/cavra-runtime/`.
- Runtime evaluator for critical file, command, Git, and MCP decisions.
- JSON request/decision CLI entrypoint.
- Compiled-policy JSON loading from `cavra policy compile`.
- Go CLI `--policy` flag for compiled policy evaluation.
- Generated Go enforcement contracts from `proto/cavra/enforcement/v1/enforcement.proto`.
- Contract conversion helpers for runtime requests and decisions.
- Unix-socket daemon transport with one JSON `EvaluateRequest` per connection.
- Reusable Go daemon client helper and CLI `--daemon` mode.
- Daemon lifecycle `start/status/stop` with PID-file tracking and socket readiness probing.
- Compiled-policy-backed daemon evaluator tests.
- Lifecycle status tests for PID-file and socket health.
- Runtime evidence references with decision IDs, correlation IDs, timestamps, and `evidence://...` refs.
- Trust-registry JSON loading for Go runtime and CLI `--registry`.
- Registry-backed MCP decisions for approved, pending, blocked, tool-scope, and capability-scope outcomes.
- All-bundled-policy compiled parity through Python-to-Go CLI validation.
- Shared parity fixture at `go/cavra-runtime/testdata/parity_cases.json`.
- MCP trust registry fixture at `go/cavra-runtime/testdata/mcp_registry.json`.
- Go unit tests that load the shared parity fixture.
- Python parity tests that validate the same fixture against authoritative `RuntimeGuard`.
- Dedicated `go-runtime-parity` GitHub Actions job.
- Required governance check execution of `go test ./...`.

Validation:
- `python3 -m pytest tests/test_go_runtime_parity.py tests/test_runtime.py tests/test_ci_templates.py -q` passed locally with Go-toolchain-dependent test skipped because Go is not installed on this Mac.
- GitHub Actions is configured with `actions/setup-go@v5` so CI can run Go tests independently of the local toolchain.

Recommended next issue: package signed Go binaries with SBOM and release evidence.

## Phase 9: Hosted Sandbox Deployment

Status: deployment workflow started.

Completed:
- GitHub Pages workflow at `.github/workflows/deploy-sandbox.yml`.
- Static artifact build from `apps/sandbox-ui`.
- JavaScript syntax validation with `node --check`.
- SVG diagram asset inclusion in the artifact.
- CAVRA brand assets included in the sandbox artifact.
- Deployment gated to `main` through `actions/deploy-pages`.
- GitHub Pages enabled for Actions publishing on the repository.
- Public sandbox verified at `https://huzefaaa2.github.io/cavra/`.
- Downloadable sample evidence packaged in the public artifact.
- Post-deploy smoke validation for the public page, JavaScript, stylesheet, brand assets, C4 diagram, and evidence JSON.
- Public post-deploy smoke run passed from `main`.

## Brand Asset System

Status: complete for the current productization slice.

Completed:
- SVG runtime authority mark, favicon, horizontal logo, stacked logo, product thumbnail, and GitHub social preview.
- PNG exports for compact icons, README/document surfaces, product thumbnails, and social previews.
- README header logo.
- Sandbox console favicon, top-left CAVRA wordmark, and larger top-right hero mark below the install CTA.
- Brand asset documentation and wiki page.

Recommended next issue: use the assets in release notes and configure the repository social preview after merge.

Validation:
- Workflow YAML parses.
- Sandbox JavaScript syntax check is covered by the workflow and local validation.

Recommended next issue: connect the public sandbox to backend-driven scenario runs.

## GitHub Required Checks and CI/CD Enforcement

Status: complete for the current production-readiness slice.

Completed:
- GitHub Actions workflow check named `cavra-required-check`.
- Policy-pack validation, lint, tests, evidence verification, and PR attestation verification in CI.
- Evidence artifact upload for reviewer and auditor inspection.
- Reusable GitHub Actions required-check and enterprise enforcement templates.
- GitLab CI enforcement example.
- Azure Pipelines required-check template for Azure Repos Build validation policies.
- Entra ID and Okta OIDC/RBAC deployment references.

Recommended next issue: expand Go parity, validate the public sandbox URL after merge, and add post-deploy smoke checks.

## Transparent Agent Methodology Enablement

Status: complete.

Completed:
- Declarative CAVRA agent manifests for product, architect, backend, frontend, test, security, docs, reviewer, and release roles.
- Agent task issue template and agent label catalog.
- Conservative GitHub Actions orchestrator scaffold that validates transparent agent manifests.
- `cavra-agentic-delivery` policy pack for bot identity, branch naming, PR attestation, approvals, and documentation requirements.
- Transparent agent methodology docs, orchestration architecture docs, wiki pages, and SVG diagram.

Recommended next issue: implement the real GitHub App orchestrator backend only after protected branch checks, evidence verification, and human approval requirements are enforced.
