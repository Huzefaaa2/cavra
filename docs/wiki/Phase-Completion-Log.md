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
- Go release package workflow with Linux/macOS/Windows binaries for `amd64` and `arm64`.
- SHA-256 checksums, SPDX-style SBOM, SLSA provenance, release evidence JSON/Markdown, and detached Ed25519 signature JSON files when signing is configured.
- Required signing for real release events and non-dry-run manual packaging.
- GitHub Release asset attachment and verifier CLI support.
- Shared parity fixture at `go/cavra-runtime/testdata/parity_cases.json`.
- MCP trust registry fixture at `go/cavra-runtime/testdata/mcp_registry.json`.
- Go unit tests that load the shared parity fixture.
- Python parity tests that validate the same fixture against authoritative `RuntimeGuard`.
- Dedicated `go-runtime-parity` GitHub Actions job.
- Required governance check execution of `go test ./...`.

Validation:
- `python3 -m pytest tests/test_go_runtime_parity.py tests/test_runtime.py tests/test_ci_templates.py -q` passed locally with Go-toolchain-dependent test skipped because Go is not installed on this Mac.
- GitHub Actions is configured with `actions/setup-go@v5` so CI can run Go tests independently of the local toolchain.

Recommended next issue: delivered below as backend-driven public sandbox runs.

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

Recommended next issue: delivered below as backend-driven public sandbox runs.

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

## License and Go Release Verification

Status: complete for the current production-readiness slice.

Completed:
- Replaced the repository `LICENSE` source with BUSL-1.1 parameters for CAVRA.
- Documented BUSL parameters in the README.
- Added `cavra release verify-go-package` for local verification of Go release package checksums, release evidence, and detached Ed25519 signatures.
- Added tamper-detection tests for signed Go release packages.
- Updated the Go release workflow to create `cavra-go-runtime-<version>.zip`.
- Updated the Go release workflow to attach signed packages directly to published GitHub Releases.
- Kept CI artifact upload for reviewer and auditor retrieval.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q` passed locally.

Recommended next issue: delivered below as SLSA provenance and release security advisory workflow.

## SLSA Provenance and Release Security Advisory Workflow

Status: complete for the current production-readiness slice.

Completed:
- Added `cavra-runtime.provenance.intoto.json` to Go release packages using an in-toto Statement and SLSA provenance predicate.
- Added provenance verification to `cavra release verify-go-package`.
- Added signature coverage for the provenance statement when release signing is configured.
- Added `SECURITY.md` with private reporting guidance, severity triage, and release advisory process.
- Added vulnerability disclosure and release security advisory documentation.
- Added `.github/workflows/release-security.yml` and `scripts/validate_release_security.py` to validate release security controls.
- Added tests for provenance generation, provenance verification, tamper detection, and release security workflow presence.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py tests/test_release_security.py -q` passed locally.
- `python3 scripts/validate_release_security.py` passed locally.

Recommended next issue: delivered below as backend-driven public sandbox runs.

## Backend-Driven Public Sandbox Runs

Status: complete for the current growth-loop slice.

Completed:
- Connected the Run Agent Scenario button to `POST /api/sandbox/run` when the CAVRA API is reachable.
- Kept static sample fallback behavior for GitHub Pages deployments without an API.
- Added deploy-time `config.js` generation from `CAVRA_PUBLIC_API_BASE_URL`.
- Added backend sandbox run persistence into evidence metadata and activity session/decision stores.
- Added sandbox run artifact links for evidence JSON, PR attestation, and compliance mapping.
- Updated console status and evidence download behavior based on the active backend or sample run.
- Added API and CI-template tests for backend sandbox runs and Pages API configuration.

Validation:
- `python3 -m pytest tests/test_api.py::test_api_sandbox_run_uses_backend_policy_and_persists_metadata tests/test_api.py::test_api_console_config_and_cors tests/test_ci_templates.py::test_sandbox_pages_workflow_builds_static_artifact -q` passed locally.
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js` passed locally.

Recommended next issue: delivered below as public sandbox release-note links.

## Public Sandbox Release-Note Links

Status: complete for the current growth-loop slice.

Completed:
- Added a Release Notes panel to the public sandbox.
- Linked design-partner demos to PR context, sandbox docs, release integrity docs, release security docs, the hosted sandbox, and the production roadmap.
- Added responsive release-note styling for desktop and mobile views.
- Updated README, sandbox docs, roadmap docs, and wiki source.
- Added sandbox smoke assertions for the release-note panel.

Validation:
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_brand_assets.py -q` passed locally.

Recommended next issue: delivered below as public telemetry-free run counters.

## Public Telemetry-Free Run Counters

Status: complete for the current growth-loop slice.

Completed:
- Added `GET /api/sandbox/metrics` for aggregate public sandbox counters sourced from persisted activity session rows.
- Added JSON and SQLite activity-store session summary support for run, decision, blocked-action, approval-required, and latest-run totals.
- Rendered compact public counters in the Evidence Console hero.
- Kept static fallback behavior explicitly non-persistent and telemetry-free when no API is reachable.
- Persisted replayed sandbox runs so repeat demos update the same backend metadata source.
- Updated README, API docs, sandbox docs, hosted deployment docs, roadmap docs, and wiki source.
- Added API and sandbox smoke assertions for the metrics endpoint and UI wiring.

Validation:
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_api.py::test_api_sandbox_run_uses_backend_policy_and_persists_metadata tests/test_brand_assets.py -q` passed locally.

Recommended next issue: delivered below as keyless release attestations.

## GitHub Keyless Release Attestations

Status: complete for the current release-integrity slice.

Completed:
- Added GitHub OIDC permissions for Go release packaging: `id-token: write`, `attestations: write`, and `artifact-metadata: write`.
- Added `actions/attest@v4` to generate a keyless provenance attestation for `cavra-go-runtime-<version>.zip`.
- Added `github-keyless-attestation.json` metadata with attestation ID, URL, issuer, and `gh attestation verify` command.
- Attached keyless attestation metadata alongside the Go runtime zip on GitHub Release events.
- Updated release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added workflow and release-security assertions for the keyless attestation path.

Validation:
- `python3 -m pytest tests/test_ci_templates.py::test_go_release_workflow_packages_signed_release_artifacts tests/test_release_security.py -q` passed locally.
- `python3 scripts/validate_release_security.py` passed locally.

Recommended next issue: delivered below as air-gapped installer bundle verification.

## Air-Gapped Installer Bundle Verification

Status: complete for the current release-integrity slice.

Completed:
- Added `offline-trust-root-bootstrap.json` to Go runtime release packages.
- Added the bootstrap manifest to checksums, SLSA provenance subjects, release evidence, and detached signature coverage.
- Added `cavra release verify-airgap-bundle` for offline verification of `cavra-go-runtime-<version>.zip`.
- Added safe zip extraction checks that reject archive path traversal before verification.
- Added offline bootstrap validation for required files and operator verification commands.
- Updated README, CLI docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added tests for signed air-gapped bundle verification, missing bootstrap detection, and unsafe archive rejection.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q` passed locally.
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py scripts/package_go_release.py tests/test_go_release_packaging.py` passed locally.

Recommended next issue: delivered below as release-candidate upgrade validation.

## Release-Candidate Upgrade Validation

Status: complete for the current release-integrity slice.

Completed:
- Added `cavra release validate-upgrade` for comparing a previously approved Go release package with a candidate package.
- Reused package verification so both previous and candidate releases must pass checksum, provenance, and detached-signature validation.
- Added rollback protection for semantic versions.
- Added regression checks for removed release artifact kinds, release controls, and Go runtime binary targets.
- Added JSON output for CI gates and human-readable output for release managers.
- Updated README, CLI docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added tests for valid release-candidate upgrades, rollback rejection, and missing target detection.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q` passed locally.

Recommended next issue: delivered below as offline trust-root distribution automation.

## Offline Trust-Root Distribution Automation

Status: complete for the current evidence-integrity slice.

Completed:
- Added `cavra evidence trust-distribution` for exporting public trust-root distribution packages.
- Generated `evidence-trust-roots.json`, `trust-root-distribution-manifest.json`, `trust-root-distribution.md`, and `checksums.txt`.
- Added distribution metadata for environment, distribution ID, approved channels, active/retired/revoked key IDs, and operator steps.
- Added checksum-protected offline operator handoff guidance for CI, reviewers, API services, audit tooling, and restricted networks.
- Updated README, CLI docs, evidence trust-root docs, roadmap docs, and wiki source.
- Added function and CLI tests for trust-root distribution package export.

Validation:
- `python3 -m pytest tests/test_evidence.py::test_export_trust_root_distribution_creates_offline_artifacts tests/test_cli.py::test_trust_distribution_cli_exports_offline_package -q` passed locally.
- `python3 -m ruff check src/cavra/evidence.py src/cavra/cli.py tests/test_evidence.py tests/test_cli.py` passed locally.

Recommended next issue: delivered below as signed installer metadata.

## Signed Installer Metadata

Status: complete for the current release-integrity slice.

Completed:
- Added `cavra-runtime.installers.json` to Go runtime release packages.
- Recorded per-target binary path, operating system, architecture, install path, install method, checksum, and verification command.
- Added installer metadata to checksums, SLSA provenance subjects, release evidence, offline trust bootstrap required files, and detached signature coverage.
- Updated release package verification to require and validate installer metadata before package approval.
- Updated README, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added tests for installer metadata generation, signature/provenance coverage, and missing metadata rejection.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q` passed locally.
- `python3 -m ruff check scripts/package_go_release.py src/cavra/release.py tests/test_go_release_packaging.py` passed locally.

Recommended next issue: delivered below as Go runtime installer smoke validation.

## Go Runtime Installer Smoke Validation

Status: complete for the current release-integrity slice.

Completed:
- Added `cavra release smoke-installers` for validating Go runtime installer metadata.
- Reused signed release package verification before installer smoke checks.
- Added static validation for every installer target, binary path, install command, install path, and checksum metadata.
- Added native runtime execution smoke testing when the current OS and architecture match a packaged target.
- Added `--skip-execution` for cross-compiled package validation on nonmatching hosts.
- Removed Terraform-specific product-boundary positioning from README and wiki white paper source.
- Updated README, CLI docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added tests for signed installer smoke validation.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q` passed locally.
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py tests/test_go_release_packaging.py scripts/package_go_release.py` passed locally.

Recommended next issue: delivered below as managed endpoint deployment manifests.

## Managed Endpoint Deployment Manifests

Status: complete for the current release-integrity slice.

Completed:
- Added `cavra-runtime.endpoint-deployment.json` to Go runtime release packages.
- Recorded approved deployment targets for CI runners and developer workstations, including platform, endpoint channel, installer target, binary path, install command, rollout gate, rollback steps, and evidence requirements.
- Added endpoint deployment metadata to checksums, SLSA provenance subjects, release evidence, offline trust bootstrap required files, and detached signature coverage.
- Updated release package verification to require and validate endpoint deployment metadata before package approval.
- Updated README, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added tests for endpoint deployment manifest generation, signature/provenance coverage, and missing metadata rejection.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q` passed locally.

Recommended next issue: delivered below as managed endpoint rollout evidence capture.

## Managed Endpoint Rollout Evidence Capture

Status: complete for the current release-integrity slice.

Completed:
- Added `cavra release capture-rollout` for capturing rollout evidence from signed Go runtime packages.
- Reused release package verification before writing rollout artifacts.
- Selected approved deployment targets from `cavra-runtime.endpoint-deployment.json`.
- Generated `managed-endpoint-rollout-evidence.json`, `managed-endpoint-rollout-evidence.md`, and rollout `checksums.txt`.
- Captured rollout ID, ring, status, actor, change record, release metadata, source artifact checksums, selected deployment targets, rollback steps, and package verification results.
- Updated README, CLI docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added tests for selected-target rollout evidence capture, CLI JSON output, and unknown target rejection.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q` passed locally.

Recommended next issue: delivered below as rollout evidence verification and indexing.

## Rollout Evidence Verification And Indexing

Status: complete for the current release-integrity slice.

Completed:
- Added `cavra release verify-rollout` for validating managed endpoint rollout evidence.
- Verified rollout artifact checksums, rollout schema, rollout status, selected deployment targets, required controls, source package artifact checksums, and referenced package verification.
- Added optional JSON and SQLite evidence metadata indexing through the existing evidence metadata stores.
- Added rollout metadata fields for rollout ID, environment, ring, status, change record, release metadata, selected deployment targets, and artifact checksum.
- Updated README, CLI docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added tests for valid rollout verification, JSON/SQLite metadata indexing, and checksum tampering rejection.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q` passed locally.

Recommended next issue: delivered below as rollout evidence search filters and views.

## Rollout Evidence Search Filters And Views

Status: complete for the current release-integrity and console-visibility slice.

Completed:
- Added rollout metadata filters to SQLite evidence search for metadata kind, rollout status, environment, and deployment target.
- Added matching JSON metadata filters to the `/evidence` API.
- Added CLI search options for rollout evidence metadata.
- Added console Evidence Search controls and columns for endpoint rollout evidence.
- Added sample managed endpoint rollout evidence to the hosted console fallback data.
- Updated README, CLI docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added tests for JSON API filters, SQLite API filters, and SQLite evidence metadata search.

Validation:
- `python3 -m pytest tests/test_api.py::test_api_filters_json_rollout_evidence_metadata tests/test_api.py::test_api_filters_sqlite_rollout_evidence_metadata tests/test_evidence.py::test_sqlite_evidence_metadata_store_filters_rollout_metadata -q` passed locally.

Recommended next issue: delivered below as governed rollout evidence artifact retrieval.

## Governed Rollout Evidence Artifact Retrieval

Status: complete for the current release-integrity and audit-retrieval slice.

Completed:
- Added a rollout-specific artifact allowlist for `managed-endpoint-rollout-evidence.json`, `managed-endpoint-rollout-evidence.md`, and `checksums.txt`.
- Extended existing evidence artifact list, download, and ZIP bundle helpers to support indexed `metadata_kind=managed-endpoint-rollout` records.
- Enforced that rollout `bundle_dir` values must resolve inside `CAVRA_EVIDENCE_ARTIFACT_ROOT`.
- Reused the existing `/evidence/{session_id}/artifacts`, `/evidence/{session_id}/artifacts/{artifact_name}`, and `/evidence/{session_id}/artifact-bundle` endpoints for rollout records.
- Updated README, evidence artifact retrieval docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added unit and API tests for rollout artifact listing, download, bundle creation, unsupported artifact rejection, and outside-root rejection.

Validation:
- `python3 -m pytest tests/test_evidence.py::test_evidence_artifact_root_lists_and_loads_rollout_files tests/test_evidence.py::test_evidence_artifact_root_rejects_rollout_bundle_outside_root tests/test_api.py::test_api_serves_configured_rollout_evidence_artifacts -q` passed locally.
- `python3 -m ruff check src/cavra/evidence.py src/cavra/api.py tests/test_evidence.py tests/test_api.py` passed locally.

Recommended next issue: delivered below as rollout artifact integrity status and promotion readiness indicators.

## Rollout Artifact Integrity And Promotion Readiness

Status: complete for the current release-integrity and console-readiness slice.

Completed:
- Added rollout artifact checksum integrity reporting to evidence artifact listings.
- Added promotion readiness status for managed endpoint rollout records based on artifact integrity and rollout state.
- Reported verified, missing, unchecked, and mismatched rollout evidence artifacts from the API.
- Added console Evidence Search readiness column for rollout records.
- Added console artifact panel details for rollout integrity, promotion readiness rationale, and rollout control status.
- Updated hosted console sample data for rollout artifact readiness.
- Updated README, evidence artifact retrieval docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added unit and API tests for verified and failed rollout artifact integrity.

Validation:
- `python3 -m pytest tests/test_evidence.py::test_evidence_artifact_root_lists_and_loads_rollout_files tests/test_evidence.py::test_evidence_artifact_root_reports_rollout_integrity_failures tests/test_api.py::test_api_serves_configured_rollout_evidence_artifacts -q` passed locally.
- `python3 -m ruff check src/cavra/evidence.py src/cavra/api.py tests/test_evidence.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.

Recommended next issue: delivered below as signed promotion approval requests.

## Signed Rollout Promotion Approval Requests

Status: complete for the current release-integrity and approval-gating slice.

Completed:
- Added signed rollout promotion approval request generation for managed endpoint rollout evidence.
- Added `cavra release request-rollout-promotion` with JSON and Markdown request artifacts.
- Required valid staged or succeeded rollout evidence before a promotion request can be generated.
- Signed promotion request payloads with Ed25519 using `CAVRA_ROLLOUT_PROMOTION_SIGNING_KEY` or `CAVRA_GO_RELEASE_SIGNING_KEY`.
- Added optional JSON and SQLite approval store persistence for generated pending approvals.
- Added `POST /evidence/{session_id}/promotion-request` for API-backed promotion approval creation from indexed rollout evidence.
- Added console promotion approval request action from the rollout artifact panel.
- Updated README, CLI docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added unit, CLI, and API tests for signed promotion approval requests.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py::test_managed_endpoint_rollout_promotion_request_is_signed_and_persisted tests/test_go_release_packaging.py::test_managed_endpoint_rollout_promotion_request_requires_ready_rollout tests/test_api.py::test_api_creates_signed_rollout_promotion_approval -q` passed locally.
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.

Recommended next issue: delivered below as approved promotion execution records.

## Approved Rollout Promotion Execution Records

Status: complete for the current release-integrity and ring-advancement slice.

Completed:
- Added approved rollout promotion execution record generation for signed promotion requests.
- Added `cavra release execute-rollout-promotion` with JSON and Markdown execution artifacts.
- Required the signed promotion request to verify before execution can be recorded.
- Required the approval record to be `approved` and bound to the rollout, request, decision, and target ring.
- Added `POST /evidence/{session_id}/promotion-execution` for API-backed promotion execution recording from indexed rollout evidence.
- Added console promotion execution recording from the rollout artifact panel.
- Updated README, CLI docs, API docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added unit, CLI, and API tests for approved promotion execution records.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py::test_managed_endpoint_rollout_promotion_execution_requires_approved_request tests/test_api.py::test_api_creates_signed_rollout_promotion_approval -q` passed locally.
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.

Recommended next issue: delivered below as promotion execution search, audit drill-downs, and rollback evidence links.

## Promotion Execution Search, Audit Drill-Downs, And Rollback Evidence Links

Status: complete for the current rollout governance and auditability slice.

Completed:
- Indexed approved promotion executions as evidence metadata with `metadata_kind=rollout-promotion-execution`.
- Added search filters for target ring, approval state, promotion execution status, rollout status, environment, and deployment target.
- Added `/promotion-executions` and `/promotion-executions/{execution_id}` API endpoints for execution search and audit detail.
- Added rollback evidence references to signed promotion requests and approved execution records.
- Added console support for promotion execution audit drill-downs from evidence search.
- Updated README, CLI docs, API docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added unit, CLI, API, and metadata-store tests for promotion execution search and audit details.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py::test_managed_endpoint_rollout_promotion_execution_requires_approved_request tests/test_api.py::test_api_creates_signed_rollout_promotion_approval tests/test_evidence.py::test_sqlite_evidence_metadata_store_filters_promotion_execution_metadata -q` passed locally.
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py src/cavra/evidence.py tests/test_go_release_packaging.py tests/test_api.py tests/test_evidence.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.

Recommended next issue: delivered below as approved rollback execution workflows and SIEM/ITSM audit export for promotion execution records.

## Approved Rollback Execution Workflows And SIEM/ITSM Promotion Audit Exports

Status: complete for the current rollback governance and audit export slice.

Completed:
- Added approved rollout rollback execution record generation for promotion execution records.
- Added `cavra release execute-rollout-rollback` with JSON and Markdown rollback artifacts.
- Required rollback approvals to be approved, authorize `release_rollback_endpoint_rollout`, and bind to the original promotion execution.
- Added rollback execution metadata indexing as `metadata_kind=rollout-rollback-execution`.
- Added `cavra release export-promotion-audit` for normalized CAVRA, Splunk, Sentinel, Datadog, webhook, Jira, and ServiceNow payloads.
- Added `/promotion-executions/{execution_id}/audit-export`, `/promotion-executions/{execution_id}/rollback-execution`, and `/rollback-executions/{rollback_id}` API endpoints.
- Added console evidence rows and audit drill-downs for rollback execution metadata.
- Updated README, CLI docs, API docs, release packaging docs, advisory docs, roadmap docs, and wiki source.
- Added unit, CLI, API, and metadata-store tests for rollback execution records and audit exports.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py::test_managed_endpoint_rollout_rollback_execution_and_audit_exports tests/test_api.py::test_api_creates_signed_rollout_promotion_approval tests/test_evidence.py::test_sqlite_evidence_metadata_store_filters_rollback_execution_metadata -q` passed locally.
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py src/cavra/evidence.py tests/test_go_release_packaging.py tests/test_api.py tests/test_evidence.py` passed locally.

Recommended next issue: delivered below as connector delivery for promotion audit exports and rollback execution records with retry evidence.

## Release Governance Connector Delivery

Status: complete for the current release connector delivery slice.

Completed:
- Added `cavra release deliver-promotion-audit` for sending normalized promotion audit events through configured connectors.
- Added `cavra release deliver-rollback-execution` for sending rollback execution audit events through configured connectors.
- Added release audit event identity fallback so connector delivery evidence records promotion execution IDs and rollback IDs.
- Added `/promotion-executions/{execution_id}/audit-export/deliver` and `/rollback-executions/{rollback_id}/deliver` API endpoints.
- Reused the existing connector retry and credential-redaction evidence schema for release governance delivery.
- Updated README, CLI docs, API docs, connector docs, integration inventory docs, release packaging docs, roadmap docs, and wiki source.
- Added CLI, API, and connector tests for retry counts, event IDs, and redacted delivery evidence.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py::test_managed_endpoint_rollout_rollback_execution_and_audit_exports tests/test_api.py::test_api_creates_signed_rollout_promotion_approval tests/test_integrations.py::test_deliver_connector_event_redacts_credentials_and_exports -q` passed locally.
- `python3 -m ruff check src/cavra/integrations.py src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py tests/test_integrations.py` passed locally.

Recommended next issue: delivered below as open-core edition boundaries and commercialization foundation.

## Open-Core Edition Boundaries And Commercialization Foundation

Status: complete for the current open-core foundation slice.

Completed:
- Replanned CAVRA as a public Community Edition with private Enterprise, Trial, and SaaS implementation boundaries.
- Added public-safe edition detection, Enterprise dynamic hooks, licensing placeholders, trial mode, feature registry, and plugin runtime interfaces.
- Added Community starter policies, Community Docker files, Community CI and release workflows, and boundary validation script.
- Added `enterprise/README.md` with explicit warning that Enterprise source belongs in the private `cavra-enterprise` repository.
- Added public Enterprise documentation, trial documentation, SaaS Control Plane design, open-core model, plugin architecture, migration report, and private repo plan.
- Updated README, root legal/community files, and wiki source with the open-core model.
- Added tests for Community mode, Enterprise feature blocking, feature registry behavior, plugin edition rejection, trial license placeholder loading, and boundary validation failures.

Validation:
- `bash scripts/validate-boundaries.sh .` passed.
- `python3 -m pytest tests/test_open_core_model.py -q` passed with 6 tests.
- `python3 -m ruff check src tests` passed.
- `python3 -m pytest -q` passed with 191 tests and 4 skipped.

Recommended next issue: delivered below as persisted delivery history views and alerting dashboards for release governance connectors.

## Release Connector Delivery History And Alerting Dashboard

Status: complete for the current release governance delivery visibility slice.

Completed:
- Added `release-connector-delivery` evidence metadata records for promotion audit and rollback execution connector deliveries.
- Added CLI indexing options for `cavra release deliver-promotion-audit` and `cavra release deliver-rollback-execution`.
- Added `cavra release connector-delivery-history` for provider, event, source ID, and success-state history filters.
- Added `cavra release connector-delivery-dashboard` for delivery totals, success rate, provider summaries, and warning or critical alerts.
- Added `/release-connector-deliveries` and `/release-connector-deliveries/dashboard` API endpoints.
- Updated the Evidence Console with a Release Connector Delivery panel showing dashboard metrics, alerts, and delivery rows.
- Updated README, CLI docs, API docs, connector docs, release packaging docs, release advisory docs, roadmap docs, and wiki source.
- Added unit, CLI, and API tests for delivery metadata, history filters, and dashboard alerts.

Validation:
- `python3 -m pytest tests/test_integrations.py::test_connector_delivery_metadata_history_and_dashboard tests/test_go_release_packaging.py::test_managed_endpoint_rollout_rollback_execution_and_audit_exports tests/test_api.py::test_api_creates_signed_rollout_promotion_approval -q` passed locally.
- `python3 -m ruff check src/cavra/integrations.py src/cavra/api.py src/cavra/cli.py tests/test_integrations.py tests/test_go_release_packaging.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.

Recommended next issue: delivered below as release channel manifests and managed workstation updater policy.

## Release Channel Manifests And Managed Workstation Updater Policy

Status: complete for the current release package channel governance slice.

Completed:
- Added `cavra-runtime.channels.json` to Go runtime release packages with canary, beta, and stable channel metadata.
- Added `cavra-runtime.updater-policy.json` with manual approval requirements, staged rollout rings, hold conditions, and rollback requirements.
- Extended release checksums, release evidence, provenance inputs, and offline bootstrap required files to include the channel manifest and updater policy.
- Extended `cavra release verify-go-package` to reject packages missing channel or updater policy artifacts and to validate approval, no-auto-update, workstation target, rollback, and verification-command controls.
- Added `cavra release channel-manifest` and `cavra release updater-policy` commands for release managers and endpoint owners to inspect generated artifacts.
- Updated README, CLI docs, release packaging docs, roadmap docs, release advisory docs, and wiki source.
- Added tests for package generation, verifier acceptance, CLI inspection, artifact signing coverage, and missing channel/updater rejection.

Validation:
- `python3 -m ruff check scripts/package_go_release.py src/cavra/release.py src/cavra/cli.py tests/test_go_release_packaging.py` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_go_release_packaging_creates_sbom_checksums_and_evidence tests/test_go_release_packaging.py::test_go_release_verifier_accepts_signed_package_and_rejects_tampering tests/test_go_release_packaging.py::test_go_release_verifier_rejects_missing_channel_and_updater_policy -q` passed locally.

Recommended next issue: delivered below as release-channel promotion approvals and endpoint-management export bundles.

## Release-Channel Promotion Approvals And Endpoint-Management Export Bundles

Status: complete for the current release channel publication slice.

Completed:
- Added signed `release-channel-promotion-request.json` artifacts for canary, beta, and stable channel promotion approval workflows.
- Bound channel promotion requests to `cavra-runtime.channels.json`, `cavra-runtime.updater-policy.json`, release evidence, signed package verification, and endpoint change approval records.
- Added `cavra release request-channel-promotion` with optional JSON and SQLite approval-store persistence.
- Added `cavra release export-endpoint-management` for Jamf, Intune, and Linux fleet export bundles.
- Generated provider artifacts including `jamf-policy.json`, `intune-win32-app.json`, `linux-fleet-manifest.json`, `linux-install-cavra-runtime.sh`, export manifest, Markdown summary, and checksums.
- Added signature verification for release-channel promotion requests and tests for provider bundle generation.
- Updated README, CLI docs, Go release packaging docs, release advisory docs, roadmap docs, and wiki source.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py tests/test_go_release_packaging.py` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_release_channel_promotion_request_and_endpoint_exports -q` passed locally.

Recommended next issue: delivered below as release channel publishing history views.

## Release Channel Publishing History Views

Status: complete for the current release channel visibility slice.

Completed:
- Added release metadata builders for `release-channel-promotion-request` and `endpoint-management-export` records.
- Added optional JSON and SQLite evidence metadata indexing to `cavra release request-channel-promotion` and `cavra release export-endpoint-management`.
- Added `/release-channel-promotions` and `/release-channel-promotions/{request_id}` API endpoints for channel, target ring, approval state, and approval ID history views.
- Added `/endpoint-management-exports`, `/endpoint-management-exports/{export_id}`, and `/endpoint-management-exports/dashboard` API endpoints for provider, channel, approval, file, and dashboard summaries.
- Updated the Evidence Console with a Release Channel Publishing panel that combines promotion request rows, endpoint export rows, provider metrics, and pending approval indicators.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, and wiki source.
- Added tests for CLI metadata indexing and API history/dashboard retrieval.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_release_channel_promotion_request_and_endpoint_exports tests/test_api.py::test_api_release_channel_and_endpoint_export_history -q` passed locally.

Recommended next issue: delivered below as governed endpoint export artifact downloads.

## Governed Endpoint Export Artifact Downloads

Status: complete for the current endpoint export artifact retrieval slice.

Completed:
- Added an endpoint-management export artifact allowlist for manifest JSON, summary Markdown, Jamf policy JSON, Intune app JSON, Linux fleet manifest JSON, Linux install script, and `checksums.txt`.
- Enforced that endpoint export `bundle_dir` values must resolve inside `CAVRA_EVIDENCE_ARTIFACT_ROOT`.
- Added endpoint export artifact integrity status with verified, missing, unchecked, and checksum-mismatched files.
- Added checksum verification before provider files are served from the API.
- Added `/endpoint-management-exports/{export_id}/artifacts`, `/endpoint-management-exports/{export_id}/artifacts/{artifact_name}`, and `/endpoint-management-exports/{export_id}/artifact-bundle`.
- Updated the Evidence Console with endpoint export artifact inspection, download readiness, integrity details, and governed download links.
- Updated README, API docs, Go release packaging docs, release advisory docs, roadmap docs, and wiki source.
- Added API tests for successful artifact listing, provider file downloads, bundle downloads, unsupported artifact rejection, tamper detection, and checksum-enforced download blocking.

Validation:
- `python3 -m ruff check src/cavra/evidence.py src/cavra/api.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_api.py::test_api_serves_endpoint_management_export_artifacts_with_integrity -q` passed locally.

Recommended next issue: add endpoint-management export publication records and connector delivery to Jamf, Intune, and Linux fleet managers.

## Endpoint Export Publication Delivery

Status: complete for the current endpoint-management publication delivery slice.

Completed:
- Added Jamf, Intune, and Linux as supported connector delivery providers.
- Added endpoint-management publication event construction with checksum-aware artifact references and provider-specific payload selection.
- Added `cavra release deliver-endpoint-export` to publish endpoint exports through configured endpoint-management connectors.
- Added `cavra release endpoint-publication-history` and `cavra release endpoint-publication-dashboard` for persisted publication delivery review.
- Added `/endpoint-management-exports/{export_id}/publish`, `/endpoint-management-publications`, and `/endpoint-management-publications/dashboard` API endpoints.
- Indexed delivery records as `metadata_kind=endpoint-management-publication-delivery` with export ID, publication ID, provider status, attempt counts, failed providers, and delivery evidence references.
- Updated the Evidence Console with an Endpoint Publication Delivery panel for provider status, failed publication alerts, and attempt history.
- Updated README, CLI docs, API docs, connector docs, Go release packaging docs, feature inventory, release advisory docs, roadmap docs, and wiki source.
- Added tests for endpoint provider payload routing, CLI publication delivery indexing, and API publication delivery history/dashboard retrieval.

Validation:
- `python3 -m ruff check src tests` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_integrations.py::test_endpoint_management_connectors_use_provider_payloads tests/test_go_release_packaging.py::test_release_channel_promotion_request_and_endpoint_exports tests/test_api.py::test_api_serves_endpoint_management_export_artifacts_with_integrity -q` passed locally.

Recommended next issue: add managed endpoint deployment reconciliation and drift monitoring for published CAVRA runtime versions.

## Managed Endpoint Reconciliation And Drift Monitoring

Status: complete for the current endpoint drift visibility slice.

Completed:
- Added managed endpoint reconciliation report generation from signed `cavra-runtime.endpoint-deployment.json` desired state and observed endpoint inventory.
- Detected runtime version drift, binary checksum drift, missing deployment target observations, unknown targets, and stale endpoint observations.
- Added `cavra release reconcile-endpoint-deployment` with JSON and Markdown reconciliation artifacts plus checksums.
- Indexed reconciliation records as `metadata_kind=managed-endpoint-reconciliation`.
- Added `cavra release endpoint-reconciliation-history` and `cavra release endpoint-reconciliation-dashboard`.
- Added `POST /endpoint-deployment/reconcile`, `/endpoint-reconciliations`, and `/endpoint-reconciliations/dashboard`.
- Updated the Evidence Console with an Endpoint Drift Monitoring panel for report status, alert level, compliant endpoints, drifted endpoints, and missing targets.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for reconciliation drift detection, CLI metadata indexing, and API reconciliation history/dashboard retrieval.

Validation:
- `python3 -m ruff check src tests` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_managed_endpoint_reconciliation_detects_drift_and_indexes_metadata tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q` passed locally.

Recommended next issue: delivered below as endpoint drift remediation plans with approval-bound republish and rollback workflows.

## Endpoint Drift Remediation Plans

Status: complete for the current approval-bound endpoint remediation slice.

Completed:
- Added endpoint drift remediation request generation from managed endpoint reconciliation reports.
- Converted version drift, binary checksum drift, missing observations, stale observations, and unknown targets into republish, rollback, refresh, or review actions.
- Added approval requests bound to reconciliation ID, request ID, drift summary, strategy, and action count.
- Added approved remediation execution records that preserve the public Community boundary by recording governance evidence without mutating endpoints.
- Added `cavra release request-endpoint-remediation`, `execute-endpoint-remediation`, `endpoint-remediation-history`, and `endpoint-remediation-dashboard`.
- Added `POST /endpoint-reconciliations/{reconciliation_id}/remediation-request`, `POST /endpoint-remediations/{request_id}/execute`, `/endpoint-remediations`, and `/endpoint-remediations/dashboard`.
- Updated the Evidence Console with an Endpoint Drift Remediation panel for request, execution, approval, strategy, and action status.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for approval-required remediation execution, CLI metadata indexing, API request/approval/execution flow, and remediation dashboard history.

Validation:
- `python3 -m py_compile src/cavra/release.py src/cavra/cli.py src/cavra/api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q` passed locally.

Recommended next issue: delivered below as endpoint inventory ingestion for Jamf, Intune, Linux fleet, and EDR exports.

## Endpoint Inventory Ingestion

Status: complete for the current public-safe endpoint inventory ingestion slice.

Completed:
- Added provider inventory normalization for Jamf, Intune, Linux fleet, and EDR export payloads.
- Emitted canonical `cavra.endpoint-observations.v1` inventory files that can feed managed endpoint reconciliation directly.
- Added ingestion evidence records indexed as `metadata_kind=endpoint-inventory-ingestion`.
- Added `cavra release ingest-endpoint-inventory`, `endpoint-inventory-history`, and `endpoint-inventory-dashboard`.
- Added `POST /endpoint-inventory/ingest`, `/endpoint-inventory-ingestions`, and `/endpoint-inventory-ingestions/dashboard`.
- Updated the Evidence Console with an Endpoint Inventory Ingestion panel for provider, channel, target, endpoint, and missing-target coverage.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for provider export normalization, CLI metadata indexing, API ingestion history/dashboard retrieval, and reconciliation using normalized inventory.

Validation:
- `python3 -m py_compile src/cavra/release.py src/cavra/cli.py src/cavra/api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_endpoint_inventory_ingestion_normalizes_provider_exports_and_indexes_metadata tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q` passed locally.

Recommended next issue: add endpoint inventory freshness SLA alerts and reconciliation automation that can open remediation requests from new ingestions.

## Endpoint Inventory Freshness And Reconciliation Automation

Status: complete for the current public-safe endpoint inventory SLA and automation slice.

Completed:
- Added endpoint inventory freshness SLA reports with warning and critical age thresholds by provider, channel, and deployment target.
- Indexed freshness reports as `metadata_kind=endpoint-inventory-freshness-report`.
- Added `cavra release endpoint-inventory-freshness`, `endpoint-inventory-freshness-history`, and `endpoint-inventory-freshness-dashboard`.
- Added reconciliation automation from indexed inventory ingestions that compares the normalized inventory with a signed desired endpoint deployment manifest.
- Added `metadata_kind=endpoint-reconciliation-automation` records and automatic pending remediation request creation when drift is detected.
- Added `cavra release automate-endpoint-reconciliation`, `endpoint-reconciliation-automation-history`, and `endpoint-reconciliation-automation-dashboard`.
- Added `POST /endpoint-inventory/freshness-report`, `/endpoint-inventory-freshness`, `/endpoint-inventory-freshness/dashboard`, `POST /endpoint-inventory-ingestions/{inventory_id}/reconcile`, `/endpoint-reconciliation-automations`, and `/endpoint-reconciliation-automations/dashboard`.
- Updated the Evidence Console with an Endpoint Inventory Freshness panel for report status, warning counts, critical counts, and alert details.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for freshness SLA evaluation, CLI metadata indexing, API freshness endpoints, and automated reconciliation with pending remediation approvals.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_endpoint_inventory_freshness_and_automation_open_remediation tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q` passed locally.

Recommended next issue: delivered below as endpoint remediation handoff packages for ITSM, ChatOps, and private endpoint connector queues.

## Endpoint Remediation Handoff Packages

Status: complete for the current public-safe endpoint remediation handoff slice.

Completed:
- Added remediation handoff package generation from endpoint drift remediation requests.
- Generated Jira, ServiceNow, Slack, Teams, and private connector queue payloads without embedding connector credentials or endpoint mutation logic.
- Preserved request ID, reconciliation ID, approval ID/state, release package metadata, channel, strategy, planned actions, evidence references, and request checksum in the handoff package.
- Added `cavra release export-endpoint-remediation-handoff`, `endpoint-remediation-handoff-history`, and `endpoint-remediation-handoff-dashboard`.
- Added `POST /endpoint-remediations/{request_id}/handoff`, `/endpoint-remediation-handoffs`, and `/endpoint-remediation-handoffs/dashboard`.
- Updated the Evidence Console with an Endpoint Remediation Handoffs panel for provider coverage, approval state, action count, and request filtering.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for handoff artifact generation, CLI metadata indexing, API handoff creation, and handoff dashboard history.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q` passed locally.

Recommended next issue: delivered below as closed-loop endpoint remediation handoff status reconciliation.

## Endpoint Remediation Handoff Status Reconciliation

Status: complete for the current public-safe handoff status reconciliation slice.

Completed:
- Added provider status records for Jira, ServiceNow, Slack, Teams, and private connector queue handoffs.
- Preserved handoff ID, request ID, reconciliation ID, provider, external reference, external URL, status, operator notes, approval context, and redacted callback payloads.
- Added credential redaction for callback payload keys such as tokens, secrets, passwords, API keys, authorization headers, and webhook values.
- Added `cavra release record-endpoint-remediation-handoff-status`, `endpoint-remediation-handoff-status-history`, and `endpoint-remediation-handoff-status-dashboard`.
- Added `POST /endpoint-remediation-handoffs/{handoff_id}/status`, `/endpoint-remediation-handoff-statuses`, and `/endpoint-remediation-handoff-statuses/dashboard`.
- Updated the Evidence Console with an Endpoint Handoff Status panel for provider state, external references, completed counts, blocked counts, and status event history.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for callback redaction, status artifact generation, CLI metadata indexing, API status creation, and status dashboard history.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q` passed locally.

Recommended next issue: delivered below as endpoint remediation SLA breach, escalation, and executive release governance reporting.

## Endpoint Remediation SLA And Executive Reporting

Status: complete for the current public-safe SLA and executive reporting slice.

Completed:
- Added endpoint remediation SLA reports that combine handoff packages with provider callback or operator status records.
- Tracked every handoff-provider pair with warning and critical age thresholds, latest status, external reference, SLA state, severity, and recommended action.
- Added public-safe escalation payloads for Slack, Teams, Jira-style tasks, and executive summaries without connector credentials.
- Added `cavra release endpoint-remediation-sla-report`, `endpoint-remediation-sla-history`, and `endpoint-remediation-sla-dashboard`.
- Added `POST /endpoint-remediation-sla/report`, `/endpoint-remediation-sla-reports`, and `/endpoint-remediation-sla-reports/dashboard`.
- Updated the Evidence Console with an Endpoint Remediation SLA panel for report alert level, tracked items, completed counts, at-risk counts, and breached counts.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for breached SLA reports, escalation payloads, CLI metadata indexing, API report creation, and SLA dashboard history.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q` passed locally.

Recommended next issue: delivered below as endpoint remediation SLA notification delivery through configured ITSM, ChatOps, and release governance connectors.

## Endpoint Remediation SLA Notification Delivery

Status: complete for the current public-safe SLA notification delivery slice.

Completed:
- Added `cavra.endpoint_remediation_sla.notification.v1` events derived from public endpoint remediation SLA reports.
- Added provider-shaped notification payloads for Slack, Teams, Jira, ServiceNow, and generic webhooks without connector credentials.
- Reused the existing connector delivery runtime so notification attempts produce redacted delivery evidence and retry metadata.
- Added `cavra release deliver-endpoint-remediation-sla` with metadata indexing as `release-connector-delivery` and source `endpoint_remediation_sla_notification`.
- Added `POST /endpoint-remediation-sla-reports/{report_id}/deliver` for API-driven notification delivery.
- Updated the Evidence Console with a Notify action on the Endpoint Remediation SLA panel.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for notification event payloads, provider payload routing, CLI delivery evidence, and API delivery indexing.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/integrations.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py tests/test_integrations.py` passed locally.
- `node --check apps/sandbox-ui/sandbox.js` passed locally.
- `python3 -m pytest tests/test_integrations.py::test_chatops_and_itsm_connectors_use_provider_payloads tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q` passed locally.

Recommended next issue: delivered below as endpoint remediation SLA notification routing policies, acknowledgement tracking, and duplicate suppression windows.

## Endpoint Remediation SLA Notification Routing, Acknowledgements, and Suppression

Status: complete for the current public-safe notification governance slice.

Completed:
- Added endpoint remediation SLA notification routing plans that select providers from policy rules, configured connectors, severity defaults, or operator-requested providers.
- Added duplicate suppression windows based on prior notification delivery metadata so repeated SLA reports avoid noisy ITSM and ChatOps events.
- Added acknowledgement records for `acknowledged`, `dismissed`, `escalated`, and `resolved` notification states.
- Added CLI commands for notification acknowledgement, notification history, and notification dashboards.
- Added API endpoints for notification acknowledgement, notification history, and notification dashboards.
- Updated the Evidence Console endpoint remediation SLA panel with notification, outstanding acknowledgement, and suppression metrics.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added focused tests for routing policy selection, duplicate suppression, acknowledgements, CLI history and dashboards, API delivery indexing, and multi-provider connector delivery.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/integrations.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py tests/test_integrations.py`
- `node --check apps/sandbox-ui/sandbox.js`
- `python3 -m pytest tests/test_integrations.py::test_deliver_connector_event_accepts_comma_separated_providers tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q`

Recommended next issue: delivered below as endpoint remediation notification escalation ladders and owner-specific service-level objectives.

## Endpoint Remediation SLA Escalation Ladders and Owner SLOs

Status: complete for the current public-safe escalation planning slice.

Completed:
- Added endpoint remediation SLA escalation plans derived from public notification plan, acknowledgement, and redacted delivery metadata.
- Added owner-specific acknowledgement and resolution SLO evaluation with configurable default SLOs and owner overrides.
- Added escalation ladder levels with age thresholds, escalation providers, and recommended actions without storing connector credentials.
- Added CLI commands for escalation plan generation, escalation history, and escalation dashboards.
- Added API endpoints for escalation plan generation, escalation history, and escalation dashboards.
- Updated the Evidence Console endpoint remediation SLA panel with active escalation and owner SLO metrics.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added focused tests for owner SLO breach evaluation, escalation metadata indexing, CLI history and dashboard output, API escalation endpoints, and console metric loading.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py`
- `node --check apps/sandbox-ui/sandbox.js`
- `python3 -m pytest tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift -q`

Recommended next issue: delivered below as endpoint remediation escalation delivery actions and owner review workflows.

## Phase 7 Endpoint Remediation Escalation Delivery And Reviews

Status: complete for the current public-safe escalation delivery and owner review slice.

Completed implementation:
- Added `cavra.endpoint_remediation_sla.escalation_delivery.v1` connector events derived from active escalation plans without connector credentials or endpoint mutation logic.
- Added escalation delivery metadata indexing through `release-connector-delivery` with `connector_delivery_source=endpoint_remediation_sla_escalation_delivery`.
- Added owner review records as `metadata_kind=endpoint-remediation-sla-escalation-review` with accepted, deferred, resolved, false-positive, and escalated states.
- Added CLI commands for escalation delivery, escalation owner review, escalation action history, and escalation action dashboards.
- Added API endpoints for escalation delivery, owner reviews, escalation action history, and escalation action dashboards.
- Updated the Evidence Console endpoint remediation SLA panel with escalation delivery and owner review metrics.
- Added tests for public-safe escalation delivery events, owner review metadata, CLI actions, API endpoints, and dashboard summaries.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py`
- `node --check apps/sandbox-ui/sandbox.js`
- `python3 -m pytest -q tests/test_go_release_packaging.py tests/test_api.py`

Recommended next issue: add endpoint remediation escalation recurrence policies, owner calendars, and maintenance-window suppression.

## Phase 7 Endpoint Remediation Escalation Recurrence And Suppression

Status: complete for the current public-safe recurrence planning slice.

Completed implementation:
- Added `cavra.endpoint_remediation_sla.escalation_recurrence_plan.v1` plans derived from escalation plans, delivery metadata, and owner review records.
- Added recurrence intervals and maximum recurrence counts so unresolved escalation routes can be re-evaluated without duplicate follow-up noise.
- Added public-safe owner calendar availability checks with business-hours and unavailable-window support.
- Added maintenance-window suppression scoped by plan, report, provider, or owner without storing connector credentials or endpoint mutation logic.
- Added CLI commands for recurrence plan generation, recurrence history, and recurrence dashboards.
- Added API endpoints for recurrence plan generation, recurrence history, and recurrence dashboards.
- Updated the Evidence Console endpoint remediation SLA panel with recurrence-ready and suppressed-route metrics.
- Added tests for recurrence metadata indexing, maintenance-window suppression, CLI recurrence commands, API recurrence endpoints, and dashboard summaries.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py`
- `node --check apps/sandbox-ui/sandbox.js`
- `python3 -m pytest -q tests/test_go_release_packaging.py tests/test_api.py`

Recommended next issue: delivered below as endpoint remediation recurrence delivery batches and suppression audits.

## Phase 7 Endpoint Remediation Recurrence Delivery Batches And Suppression Audits

Status: complete for the current public-safe recurrence delivery and suppression audit slice.

Completed implementation:
- Added `cavra.endpoint_remediation_sla.escalation_recurrence_delivery.v1` connector events derived only from recurrence routes whose action is `deliver`.
- Excluded suppressed and waiting recurrence routes from connector payloads while preserving their reasons in audit evidence.
- Added suppression audit exports with JSON, Markdown, and checksum files for maintenance windows, owner unavailability, maximum recurrence limits, and recurrence interval waits.
- Added suppression audit metadata indexing as `endpoint-remediation-sla-escalation-suppression-audit`.
- Added recurrence delivery metadata indexing through `release-connector-delivery` with `connector_delivery_source=endpoint_remediation_sla_escalation_recurrence_delivery`.
- Added CLI commands for recurrence delivery batching and suppression audit exports.
- Added API endpoints for recurrence delivery batching and suppression audit retrieval.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for recurrence delivery event filtering, suppression audit metadata, CLI export paths, API endpoints, and action dashboard summaries.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py`
- `python3 -m pytest -q tests/test_go_release_packaging.py tests/test_api.py`

Recommended next issue: delivered below as recurrence retry policies, owner digests, and suppression trends.

## Phase 7 Endpoint Remediation Recurrence Retry Digests And Trends

Status: complete for the current public-safe recurrence retry and analytics slice.

Completed implementation:
- Added recurrence retry plans derived from failed `endpoint_remediation_sla_escalation_recurrence_delivery` metadata.
- Added retry policy controls for maximum retry attempts, retry delay, and backoff without storing connector credentials.
- Added owner digest notification events that group unresolved recurrence routes by owner and provider.
- Added owner digest connector delivery metadata through `connector_delivery_source=endpoint_remediation_sla_escalation_owner_digest`.
- Added suppression trend analytics by reason category, owner, and provider.
- Added CLI commands for retry plans, owner digest delivery, and suppression trend reports.
- Added API endpoints for retry plans, owner digest delivery, and suppression trend reports.
- Updated README, CLI docs, API docs, Go release packaging docs, release advisory docs, roadmap docs, feature inventory, and wiki source.
- Added tests for retry decision planning, owner digest event generation, suppression trend metadata, CLI commands, API endpoints, and action dashboard counts.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py`
- `python3 -m pytest -q tests/test_go_release_packaging.py tests/test_api.py`

Recommended next issue: delivered below as Evidence Console recurrence operations filters and export drill-downs.

## Phase 7 Evidence Console Recurrence Operations

Status: complete for the current recurrence operations console slice.

Completed implementation:
- Added a Recurrence Operations panel to the Evidence Console.
- Added retry-plan, owner-digest, and suppression-trend tables backed by persisted `endpoint-remediation-sla-escalation-actions` metadata.
- Added owner, provider, action, and suppression category filters.
- Added dashboard counters for retry plans, retryable routes, waiting routes, suppressed routes, owner digests, unresolved owner routes, trend events, top suppression category, and failed deliveries.
- Added JSON detail drill-downs and local export actions for retry plans, owner digests, and suppression trends.
- Added public sample recurrence operations data so the static sandbox remains useful without a deployed API.
- Updated README, sandbox docs, roadmap docs, and wiki source.

Validation:
- `node --check apps/sandbox-ui/sandbox.js`
- `python3 -m ruff check src tests`
- `bash scripts/validate-boundaries.sh .`
- `git diff --check`
- `python3 -m pytest -q`

Recommended next issue: delivered below as scheduled recurrence automation workers.

## Phase 7 Scheduled Recurrence Automation Workers

Status: complete for the current public-safe recurrence automation slice.

Completed implementation:
- Added `cavra.endpoint_remediation_sla.escalation_recurrence_automation_run.v1` worker-run artifacts.
- Added dry-run-by-default worker orchestration for retry-plan creation, owner digest generation, suppression trend generation, and follow-up action planning.
- Added schedule-window idempotency keys based on the worker interval and recurrence metadata inputs.
- Added optional `--execute` delivery for owner digests through configured connectors while preserving dry-run as the safe default.
- Added metadata indexing for worker runs as `endpoint-remediation-sla-escalation-recurrence-automation-run`.
- Added CLI commands for recurrence automation run, history, and dashboard summaries.
- Added API endpoints for recurrence automation run, history, and dashboard summaries.
- Updated README, CLI docs, API docs, Go release packaging docs, roadmap docs, feature inventory, and wiki source.
- Added tests for worker artifact construction, metadata indexing, CLI execution, API execution, history, dashboard, and console config endpoint discovery.

Validation:
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py`
- `python3 -m pytest -q tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift`
- `python3 -m ruff check src tests`
- `node --check apps/sandbox-ui/sandbox.js`
- `bash scripts/validate-boundaries.sh .`
- `git diff --check`
- `python3 -m pytest -q`

Recommended next issue: delivered below as Evidence Console recurrence automation worker history.

## Phase 7 Evidence Console Recurrence Automation History

Status: complete for the current console visibility slice.

Completed implementation:
- Added a Worker Runs table to the Evidence Console Recurrence Operations panel.
- Added dry-run versus executed worker filtering.
- Added dashboard cards for worker run count, dry-run count, executed count, worker retryable routes, worker digests, and worker trend events.
- Added API-backed loading from `/endpoint-remediation-sla-escalation-recurrence-automations` and `/endpoint-remediation-sla-escalation-recurrence-automations/dashboard`.
- Added static sample automation-run evidence so the hosted sandbox remains useful without a deployed API.
- Added JSON detail drill-downs and local export actions for automation run payloads, follow-up actions, and skipped delivery reasons.
- Updated README, sandbox docs, roadmap docs, feature inventory, and wiki source.

Validation:
- `node --check apps/sandbox-ui/sandbox.js`
- `python3 -m ruff check src tests`
- `bash scripts/validate-boundaries.sh .`
- `git diff --check`
- `python3 -m pytest -q`

Recommended next issue: delivered below as recurrence automation deployment templates.

## Phase 7 Recurrence Automation Deployment Templates

Status: complete for the current public-safe deployment-template slice.

Completed implementation:
- Added a GitHub Actions scheduled workflow template for dry-run recurrence automation and guarded manual execute mode.
- Added a Kubernetes CronJob template with persistent worker state, optional connector config, non-root execution, and overlap prevention.
- Added systemd service, timer, and environment examples for self-hosted Linux workers.
- Added recurrence automation deployment documentation covering dry-run defaults, execute-mode gating, connector configuration, rollback, disable procedures, user stories, and enterprise value.
- Added tests that validate template defaults, schedule intervals, guarded execute mode, and public-safe connector handling.
- Updated README, roadmap docs, feature inventory, and wiki source.

Validation:
- `python3 -m pytest -q tests/test_recurrence_automation_deployment_templates.py`
- `python3 -m ruff check src tests`
- `node --check apps/sandbox-ui/sandbox.js`
- `bash scripts/validate-boundaries.sh .`
- `git diff --check`
- `python3 -m pytest -q`

Recommended next issue: delivered below as recurrence automation health reporting.

## Phase 7 Recurrence Automation Health Reporting

Status: complete for the current public-safe health reporting slice.

Completed implementation:
- Added recurrence automation health summaries for missed worker runs, failed run records, stale recurrence metadata, disabled schedules, and owner-digest connector delivery failures.
- Added CLI command `cavra release endpoint-remediation-sla-escalation-recurrence-automation-health`.
- Added API endpoint `/endpoint-remediation-sla-escalation-recurrence-automations/health` and console config discovery.
- Updated the Evidence Console Recurrence Operations dashboard with health status, missed run, failed job, stale metadata, connector failure, and latest-run age cards.
- Updated README, API/CLI references, roadmap docs, feature inventory, and wiki source.
- Added tests for release-layer health summaries, CLI output, API endpoint discovery, and API health responses.

Validation:
- `python3 -m pytest -q tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift`
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py`
- `node --check apps/sandbox-ui/sandbox.js`
- `bash scripts/validate-boundaries.sh .`
- `git diff --check`
- `python3 -m pytest -q`

Recommended next issue: delivered below as recurrence automation health alert delivery and acknowledgements.

## Phase 7 Recurrence Automation Health Alert Delivery

Status: complete for the current public-safe health alert delivery and acknowledgement slice.

Completed implementation:
- Added recurrence automation health alert events, routing plans, duplicate suppression, and connector delivery metadata using the existing public-safe connector framework.
- Added acknowledgement records for health alerts with provider, reviewer, state, external reference, and notes.
- Added CLI commands for health alert delivery, acknowledgement, history, and dashboard views.
- Added API endpoints for health alert delivery, acknowledgement, history, dashboard, and console config discovery.
- Updated the Evidence Console Recurrence Operations panel with health alert plan, delivery, acknowledgement, and outstanding acknowledgement metrics plus detail drill-downs.
- Updated README, API/CLI references, roadmap docs, deployment guidance, feature inventory, and wiki source.
- Added tests for release-layer health alert plans, events, acknowledgements, delivery history, dashboards, CLI, and API coverage.

Validation:
- `python3 -m pytest -q tests/test_go_release_packaging.py::test_endpoint_drift_remediation_requires_approval_and_indexes_execution tests/test_api.py::test_api_reconciles_managed_endpoint_deployment_drift`
- `python3 -m ruff check src/cavra/release.py src/cavra/cli.py src/cavra/api.py tests/test_go_release_packaging.py tests/test_api.py`
- `node --check apps/sandbox-ui/sandbox.js`

Recommended next issue: delivered below as approval-backed release governance Go parity.

## Phase 7 Approval-Backed Release Governance Go Parity

Status: complete for the current public-safe release governance record parity slice.

Completed implementation:
- Added `release_governance_record` support to the Go runtime evaluator with approval-state checks for promotion, rollback, endpoint remediation request, and endpoint remediation execution metadata.
- Added public-safe Go fixtures for pending, approved, denied, and missing-approval release governance records.
- Added Go runtime tests and Python fixture-shape validation for the new release governance parity cases.
- Updated README, Go runtime docs, roadmap docs, feature inventory, and wiki source.

Validation:
- `python3 -m pytest -q tests/test_go_runtime_parity.py`
- `python3 -m ruff check tests/test_go_runtime_parity.py`
- `node --check apps/sandbox-ui/sandbox.js`
- `bash scripts/validate-boundaries.sh .`

Note: local Go validation could not run because the Go toolchain is not installed in this environment; CI will run the Go parity job.

Recommended next issue: delivered below as sandbox deployment Node.js 24 runner compatibility.

## Phase 9 Sandbox Deployment Node.js 24 Compatibility

Status: complete for the current hosted sandbox deployment maintenance slice.

Completed implementation:
- Opted `.github/workflows/deploy-sandbox.yml` into `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` so JavaScript-based GitHub Actions run on Node.js 24 ahead of the hosted-runner Node.js 20 deprecation path.
- Added workflow-template test coverage for the Node.js 24 opt-in.
- Updated sandbox deployment documentation, README, roadmap docs, and wiki source.

Validation:
- `python3 -m pytest -q tests/test_ci_templates.py`
- `node --check apps/sandbox-ui/config.js`
- `node --check apps/sandbox-ui/sandbox.js`
- `bash scripts/validate-boundaries.sh .`
- `git diff --check`

Recommended next issue: delivered below as expanded release governance Go record parity.

## Phase 7 Expanded Release Governance Go Record Parity

Status: complete for the current public-safe release governance metadata parity slice.

Completed implementation:
- Expanded `release_governance_record` evaluation to recognize delivery failures, critical alert levels, drift states, blocked handoff status, blocked counts, SLA breach counts, failed delivery counts, and known release governance metadata kinds.
- Added fixtures for endpoint publication delivery, failed release connector delivery, endpoint inventory freshness, managed endpoint reconciliation drift, clean SLA reports, blocked handoff status, and pending endpoint remediation handoff approvals.
- Updated Go parity fixture-shape assertions, README, Go runtime docs, feature inventory, roadmap docs, and wiki source.

Validation:
- `python3 -m pytest -q tests/test_go_runtime_parity.py`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m json.tool go/cavra-runtime/testdata/release_governance_records.json`

Recommended next issue: delivered below as typed release governance enforcement contracts.

## Phase 7 Typed Release Governance Enforcement Contracts

Status: complete for the current public-safe release governance contract slice.

Completed implementation:
- Added `ReleaseGovernanceEvidence` to `proto/cavra/enforcement/v1/enforcement.proto` for public-safe release metadata fields including approval state, delivery status, alert level, drift status, handoff status, and count-based risk signals.
- Regenerated `go/cavra-runtime/enforcement/v1/contracts.go` with typed release-governance payload support and conversion into runtime release-governance records.
- Added contract-level fixtures for approved promotion execution, failed connector delivery, and critical inventory freshness report requests.
- Added Go contract tests that validate protobuf fields and evaluate typed release-governance contract fixtures through the runtime.
- Updated README, Go contract docs, roadmap docs, feature inventory, and wiki source.

Validation:
- `cd go/cavra-runtime && go test ./...`
- `python3 scripts/generate_go_enforcement_contracts.py`
- `python3 -m json.tool go/cavra-runtime/testdata/release_governance_contracts.json`

Recommended next issue: delivered below as typed release governance daemon and CI runner examples.

## Phase 7 Typed Release Governance Daemon And Runner Examples

Status: complete for the current public-safe daemon and CI runner example slice.

Completed implementation:
- Added typed release-governance `EvaluateRequest` JSON examples for approved promotion execution, failed connector delivery, and critical endpoint inventory freshness.
- Added GitHub Actions, GitLab CI, and Azure Pipelines templates that start the Go daemon, send a typed `release_governance` request through `--daemon`, validate the expected decision and rule, and publish daemon evidence artifacts.
- Updated Go daemon transport and Go enforcement contract documentation to show the typed request path and CI runner usage.
- Updated README, roadmap docs, feature inventory, phase log, and wiki source.

Validation:
- `python3 -m pytest -q tests/test_ci_templates.py tests/test_go_daemon_transport.py`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m json.tool examples/go-runtime/typed-release-governance/approved-promotion.json`
- `python3 -m json.tool examples/go-runtime/typed-release-governance/failed-connector-delivery.json`
- `python3 -m json.tool examples/go-runtime/typed-release-governance/critical-inventory-freshness.json`

Recommended next issue: delivered below as signed CI runner binary packaging and reusable runner actions.

## Phase 7 Signed CI Runner Packaging

Status: complete for the current public-safe signed runner packaging slice.

Completed implementation:
- Added a reusable release-governance runner shell wrapper that starts the Go daemon, sends a typed request, validates the expected decision and rule, fails closed on blocking decisions, and writes daemon evidence artifacts.
- Added a GitHub composite action that wraps the runner script for repository or packaged-action usage.
- Extended Go release packaging to include `cavra-runtime.ci-runner-bundles.json`, `ci-runners/cavra-release-governance-runner.sh`, and `ci-runners/github-action/action.yml` in the signed release package.
- Extended Go release verification to require and validate CI runner bundle metadata, runner wrapper digests, CI deployment target bindings, package verification guidance, keyless attestation guidance, and daemon evidence outputs.
- Updated README, Go release packaging docs, Go daemon transport docs, Go runtime README, feature inventory, roadmap, and wiki source.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py::test_go_release_packaging_creates_sbom_checksums_and_evidence tests/test_go_release_packaging.py::test_go_release_verifier_accepts_signed_package_and_rejects_tampering tests/test_go_release_packaging.py::test_go_release_verifier_rejects_missing_ci_runner_bundle_metadata -q`
- `python3 -m pytest tests/test_ci_templates.py::test_github_release_governance_composite_action_uses_packaged_runner_wrapper tests/test_ci_templates.py::test_release_governance_runner_wrapper_runs_daemon_and_fails_closed -q`
- `python3 scripts/validate_release_security.py`

Recommended next issue: delivered below as runner authentication and signed streaming evidence.

## Phase 7 Runner Authentication And Signed Evidence Streams

Status: complete for the current public-safe HMAC runner authentication and evidence stream signing slice.

Completed implementation:
- Added `RunnerAuthentication` and `RunnerIdentity` to the generated Go enforcement contract and protobuf source.
- Added optional daemon-side runner authentication with `--runner-auth-key`, `--runner-auth-key-id`, and signed `runner_auth` claims on `EvaluateRequest`.
- Added client-side `--runner-auth-claims` support so packaged runner scripts can attach signed CI provider, repository, workflow, ref, SHA, actor, job, and runner identity claims.
- Added hash-chained daemon evidence records with sequence numbers, previous hashes, record hashes, optional `HMAC-SHA256` signatures, and key IDs.
- Updated the release-governance runner wrapper and GitHub composite action to support `CAVRA_RUNNER_AUTH_HMAC_KEY`, `CAVRA_RUNNER_AUTH_KEY_ID`, `CAVRA_DAEMON_EVIDENCE_HMAC_KEY`, and `CAVRA_DAEMON_EVIDENCE_KEY_ID`.
- Extended signed CI runner bundle metadata and release verification controls to require runner authentication and signed evidence stream guidance.
- Updated README, Go daemon transport docs, Go release packaging docs, Go contract docs, Go runtime README, feature inventory, productization report, roadmap, and wiki source.

Validation:
- `cd go/cavra-runtime && go test ./...`
- `python3 -m pytest tests/test_go_release_packaging.py::test_go_release_packaging_creates_sbom_checksums_and_evidence tests/test_ci_templates.py::test_github_release_governance_composite_action_uses_packaged_runner_wrapper tests/test_ci_templates.py::test_release_governance_runner_wrapper_runs_daemon_and_fails_closed tests/test_go_daemon_transport.py tests/test_go_enforcement_contracts.py -q`
- `python3 scripts/validate_release_security.py`
- `bash -n examples/ci-runners/cavra-release-governance-runner.sh`
- Built `go/cavra-runtime/cmd/cavra-runtime` and smoke-tested `examples/ci-runners/cavra-release-governance-runner.sh` with runner auth and evidence HMAC keys.

Recommended next issue: delivered below as runner OIDC verification and daemon evidence verifier CLI.

## Phase 7 Runner OIDC Verification And Evidence Verifier CLI

Status: complete for the current public-safe runner JWT verification and daemon evidence verification slice.

Completed implementation:
- Added `OIDC-JWT` runner authentication alongside existing `HMAC-SHA256` runner signatures.
- Added daemon-side RS256/JWKS verification for CI-provider runner tokens with issuer, audience, expiry, not-before, provider, repository, and runner identity claim checks.
- Added client-side `--runner-auth-oidc-token` and `--runner-auth-oidc-token-file` support and daemon-side `--runner-oidc-issuer`, `--runner-oidc-audience`, `--runner-oidc-jwks`, and `--runner-oidc-jwks-url` configuration.
- Redacted OIDC bearer JWTs from daemon evidence records while preserving runner identity metadata.
- Added `--verify-evidence` to validate daemon evidence sequence numbers, previous hashes, record hashes, signature key IDs, and HMAC signatures.
- Updated reusable CI runner wrappers, GitHub composite action inputs, release bundle metadata, release verification controls, README, Go runtime docs, Go daemon transport docs, Go release packaging docs, feature inventory, roadmap, and wiki source.

Validation:
- `cd go/cavra-runtime && go test ./...`
- `python3 -m pytest tests/test_ci_templates.py::test_github_release_governance_composite_action_uses_packaged_runner_wrapper tests/test_ci_templates.py::test_release_governance_runner_wrapper_runs_daemon_and_fails_closed tests/test_go_release_packaging.py::test_go_release_packaging_creates_sbom_checksums_and_evidence tests/test_go_daemon_transport.py tests/test_identity_references.py tests/test_immutable_storage_references.py -q`
- `python3 scripts/validate_release_security.py`
- `bash -n examples/ci-runners/cavra-release-governance-runner.sh`

Recommended next issue: delivered below as provider-native OIDC token acquisition and runner evidence key custody.

## Phase 7 Provider OIDC Token Acquisition And Runner Key Custody

Status: complete for the current public-safe CI provider acquisition and key-custody documentation slice.

Completed implementation:
- Added runner wrapper auto-acquisition for GitHub Actions OIDC tokens through `ACTIONS_ID_TOKEN_REQUEST_URL` and `ACTIONS_ID_TOKEN_REQUEST_TOKEN`.
- Added GitLab CI `id_tokens` support through `CAVRA_GITLAB_OIDC_TOKEN`, `GITLAB_OIDC_TOKEN`, `CAVRA_RUNNER_AUTH_OIDC_TOKEN_ENV`, or `CI_JOB_JWT_V2`.
- Added Azure Pipelines token acquisition support through `SYSTEM_OIDCREQUESTURI` plus `SYSTEM_ACCESSTOKEN` or `CAVRA_AZURE_OIDC_REQUEST_TOKEN`, with `CAVRA_AZURE_OIDC_TOKEN` as an explicit fallback.
- Added GitHub composite action inputs for OIDC auto-acquisition and GitLab token environment selection.
- Updated GitHub Actions, GitLab CI, and Azure Pipelines examples to publish `release-governance-evidence-verification.json` as an audit artifact.
- Added `docs/runner-auth-evidence-key-custody.md` for OIDC preference, HMAC fallback, key IDs, rotation cadence, JWKS trust, and release-governance evidence retention.
- Extended release package metadata, release verification controls, README, Go daemon transport docs, Go release packaging docs, Go runtime README, feature inventory, roadmap, and wiki source.

Validation:
- `python3 -m pytest tests/test_ci_templates.py tests/test_go_release_packaging.py::test_go_release_packaging_creates_sbom_checksums_and_evidence tests/test_identity_references.py tests/test_immutable_storage_references.py -q`
- `python3 scripts/validate_release_security.py`
- `bash -n examples/ci-runners/cavra-release-governance-runner.sh`

Recommended next issue: delivered below as Go release-governance parity expansion and reproducible air-gapped build metadata.

## Phase 7 Go Release-Governance Parity And Reproducible Air-Gapped Builds

Status: complete for the current public-safe parity and reproducibility slice.

Completed implementation:
- Added Python `RuntimeGuard` release-governance evaluation for the same public-safe record fixture used by the Go runtime.
- Expanded Go release-governance record parity with rollout evidence verification and rollout artifact integrity cases.
- Added critical signal handling for failed rollout verification and artifact integrity mismatches.
- Added `cavra-runtime.reproducibility.json` to Go release packages with deterministic build environment, Go flags, linker flags, target binaries, SHA-256 digests, and air-gapped rebuild commands.
- Updated the Go release workflow to build with `SOURCE_DATE_EPOCH`, `CGO_ENABLED=0`, `GOFLAGS="-trimpath -mod=readonly -buildvcs=false"`, and `-ldflags="-s -w -buildid="`.
- Extended `cavra release verify-go-package` to require and validate the reproducibility manifest.
- Added `docs/go-reproducible-airgap-builds.md` and refreshed README, roadmap, feature inventory, Go parity, Go packaging, and wiki source documentation.

Validation:
- `python3 -m pytest tests/test_go_runtime_parity.py tests/test_go_release_packaging.py -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m ruff check src/cavra/runtime.py scripts/package_go_release.py tests/test_go_runtime_parity.py tests/test_go_release_packaging.py`

Recommended next issue: delivered below as high-risk release-governance contract fixtures.

## Phase 7 High-Risk Release-Governance Contract Fixtures

Status: complete for the current public-safe generated contract fixture slice.

Completed implementation:
- Extended `ReleaseGovernanceEvidence` in `proto/cavra/enforcement/v1/enforcement.proto` with typed rollout verification, artifact integrity, audit export, and rollback reference fields.
- Regenerated `go/cavra-runtime/enforcement/v1/contracts.go` through `scripts/generate_go_enforcement_contracts.py`.
- Added contract fixture cases for failed rollout evidence verification, artifact integrity mismatch, successful promotion audit export, and failed rollback audit export.
- Updated Python and Go runtime critical signal handling for audit export failures.
- Added Python parity coverage for the proto-shaped release-governance contract fixture set.
- Updated README, Go contract docs, Go parity docs, roadmap, feature inventory, and wiki source documentation.

Validation:
- `python3 -m pytest tests/test_go_enforcement_contracts.py tests/test_go_runtime_parity.py -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m ruff check src/cavra/runtime.py scripts/generate_go_enforcement_contracts.py tests/test_go_enforcement_contracts.py tests/test_go_runtime_parity.py`

Recommended next issue: add operational drill history for returning promoted environments to Python-only mode.

## Phase 7 High-Risk Command And Cloud/IaC Parity

Status: complete for the current high-risk built-in Go policy parity slice.

Completed implementation:
- Added Go built-in policy parity for `cavra-cloud-iam`, `cavra-kubernetes-prod`, `cavra-terraform-prod`, `cavra-github-enterprise`, `cavra-owasp-llm-agentic`, and `cavra-agentic-delivery`.
- Expanded `go/cavra-runtime/testdata/parity_cases.json` with high-risk Cloud IAM mutation, Kubernetes production apply, Terraform/OpenTofu destructive operation, GitHub force/admin operation, OWASP pipe-shell command injection, and agentic delivery repository-setting cases.
- Added positive read-only/test allowances for Cloud IAM, Kubernetes diff, OpenTofu plan, and agentic delivery test commands.
- Added Python fixture-shape coverage to ensure the high-risk command and cloud/IaC policy packs remain represented in the shared parity suite.
- Added `docs/high-risk-command-cloud-iac-parity.md`, wiki documentation, and a dedicated SVG diagram for parity evidence.
- Updated README, roadmap, feature inventory, Go parity docs, productization report, and wiki source documentation.

Validation:
- `python3 -m pytest tests/test_go_runtime_parity.py -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m pytest -q`
- `python3 -m ruff check src/ tests/ scripts/package_go_release.py scripts/validate_release_security.py scripts/generate_go_enforcement_contracts.py`
- `python3 scripts/validate_release_security.py && bash scripts/validate-boundaries.sh .`
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js`

Recommended next issue: add operational drill history for returning promoted environments to Python-only mode.

## Phase 7 Release Signing Operations

Status: complete for the current public-safe production signing operations slice.

Completed implementation:
- Added `cavra-runtime.signing-operations.json` to Go runtime release packages with active key ID, Ed25519 algorithm, private-key custody boundary, rotation policy, emergency revocation evidence, and operator steps.
- Added the signing operations manifest to release checksums, SLSA provenance subjects, detached signatures, release evidence artifacts, and offline trust bootstrap required files.
- Extended `cavra release verify-go-package` to require and validate signing operations controls before package promotion.
- Added tests for generated signing operations metadata, signed package verification, and missing manifest rejection.
- Added `docs/release-signing-operations.md`, wiki documentation, and a dedicated SVG diagram for users and auditors.
- Updated README, Go release packaging docs, roadmap, feature inventory, productization report, and wiki source documentation.

Validation:
- `python3 -m pytest tests/test_go_release_packaging.py -q`
- `python3 -m pytest -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m ruff check src/ tests/ scripts/package_go_release.py scripts/validate_release_security.py scripts/generate_go_enforcement_contracts.py`
- `python3 scripts/validate_release_security.py && bash scripts/validate-boundaries.sh . && git diff --check`
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js`

Recommended next issue: add operational drill history for returning promoted environments to Python-only mode.

## Phase 7 Opt-In Go Backend Pilot

Status: complete for the current public-safe pilot integration slice.

Completed implementation:
- Added `src/cavra/go_backend.py` with disabled, shadow, and enforce modes.
- Added readiness checks for runtime binary path, compiled policy path, optional registry path, Python fallback, and parity gate evidence.
- Added audited pilot evaluation that runs Python first, invokes Go only when enabled, compares `decision`, `rule_id`, and `severity`, and falls back to Python on failure or mismatch.
- Added CLI commands `cavra runtime go-pilot-readiness` and `cavra runtime go-pilot-evaluate`.
- Added FastAPI endpoints `/runtime/go-pilot/readiness` and `/runtime/go-pilot/evaluate`.
- Added Go backend pilot status to `/deployment/production-readiness`, `/console/config`, and the Evidence Console Production Readiness panel.
- Added `docs/go-backend-pilot.md`, `docs/wiki/Go-Backend-Pilot.md`, and `docs/diagrams/go-backend-pilot.svg`.
- Updated README, production roadmap, feature inventory, production deployment validation, Go parity docs, Go roadmap, productization report, and wiki navigation.

Validation:
- `python3 -m pytest tests/test_go_backend.py tests/test_policy_authoring.py::test_production_readiness_report_marks_missing_controls tests/test_api.py::test_api_deployment_production_readiness tests/test_api.py::test_api_go_backend_pilot_readiness_and_evaluation tests/test_cli.py::test_runtime_go_pilot_readiness_cli_reports_disabled -q`
- `python3 -m ruff check src/cavra/go_backend.py src/cavra/cli.py src/cavra/api.py src/cavra/policy_authoring.py tests/test_go_backend.py tests/test_api.py tests/test_cli.py tests/test_policy_authoring.py`
- `python3 -m pytest -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m ruff check src/ tests/ scripts/package_go_release.py scripts/validate_release_security.py scripts/generate_go_enforcement_contracts.py`
- `python3 scripts/validate_release_security.py && bash scripts/validate-boundaries.sh .`
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js && git diff --check`

Recommended next issue: add operational drill history for returning promoted environments to Python-only mode.

## Phase 7 Go Backend Deployment Readiness

Status: complete for the current public-safe CI runner and workstation readiness slice.

Completed implementation:
- Added Go backend deployment readiness checks to `src/cavra/go_backend.py`.
- Added environment support for `CAVRA_GO_RUNTIME_PACKAGE_DIR`, `CAVRA_GO_ENDPOINT_DEPLOYMENT_MANIFEST`, `CAVRA_GO_CI_RUNNER_BUNDLES`, `CAVRA_GO_WORKSTATION_CHANNELS`, and `CAVRA_GO_WORKSTATION_UPDATER_POLICY`.
- Added CLI command `cavra runtime go-deployment-readiness`.
- Added FastAPI endpoint `/runtime/go-pilot/deployment-readiness`.
- Added `go_backend_deployment` to `/deployment/production-readiness` and surfaced Go deployment status in the Evidence Console Production Readiness panel.
- Added tests for disabled, missing, and valid CI runner/workstation metadata readiness.
- Added `docs/go-backend-deployment-readiness.md`, `docs/wiki/Go-Backend-Deployment-Readiness.md`, and `docs/diagrams/go-backend-deployment-readiness.svg`.
- Updated README, production roadmap, current feature inventory, production deployment validation, Go parity docs, Go roadmap, productization report, and wiki navigation.

Validation:
- `python3 -m pytest tests/test_go_backend.py tests/test_api.py::test_api_deployment_production_readiness tests/test_api.py::test_api_go_backend_deployment_readiness tests/test_cli.py::test_runtime_go_deployment_readiness_cli_reports_not_configured tests/test_policy_authoring.py::test_production_readiness_report_marks_missing_controls -q`
- `python3 -m ruff check src/cavra/go_backend.py src/cavra/cli.py src/cavra/api.py src/cavra/policy_authoring.py tests/test_go_backend.py tests/test_api.py tests/test_cli.py tests/test_policy_authoring.py`
- `python3 -m pytest -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m ruff check src/ tests/ scripts/package_go_release.py scripts/validate_release_security.py scripts/generate_go_enforcement_contracts.py`
- `python3 scripts/validate_release_security.py && bash scripts/validate-boundaries.sh .`
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js && git diff --check`

Recommended next issue: add operational drill history for returning promoted environments to Python-only mode.

## Phase 7 Go Backend Promotion Gate

Status: complete for the current public-safe optional backend promotion slice.

Completed implementation:
- Added `promoted` mode to the opt-in Go backend configuration while keeping Python as the default backend.
- Added `CAVRA_GO_PROMOTION_EVIDENCE` and `promotion_evidence_path` support for approved public-safe promotion evidence.
- Added `go_promotion_readiness_report` with runtime readiness, deployment readiness, audited parity evidence, and approval checks.
- Added fail-closed promoted-mode evaluation so Go is selected only when promotion readiness is `ready`; otherwise CAVRA falls back to Python.
- Added CLI command `cavra runtime go-promotion-readiness`.
- Added FastAPI endpoint `/runtime/go-pilot/promotion-readiness`.
- Added `go_backend_promotion` to `/deployment/production-readiness`, `/console/config`, and the Evidence Console Production Readiness panel.
- Added tests for default `not_requested`, missing evidence, valid evidence, promoted-mode fallback, and promoted-mode Go selection.
- Added `docs/go-backend-promotion.md`, `docs/wiki/Go-Backend-Promotion.md`, and `docs/diagrams/go-backend-promotion.svg`.
- Updated README, feature inventory, production deployment validation, Go parity docs, pilot/deployment docs, productization docs, and wiki navigation.

Validation:
- `python3 -m pytest tests/test_go_backend.py tests/test_api.py::test_api_deployment_production_readiness tests/test_api.py::test_api_go_backend_promotion_readiness tests/test_cli.py::test_runtime_go_promotion_readiness_cli_reports_not_requested tests/test_policy_authoring.py::test_production_readiness_report_marks_missing_controls -q`
- `python3 -m ruff check src/cavra/go_backend.py src/cavra/cli.py src/cavra/api.py src/cavra/policy_authoring.py tests/test_go_backend.py tests/test_api.py tests/test_cli.py tests/test_policy_authoring.py`
- `python3 -m pytest -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m ruff check src/ tests/ scripts/package_go_release.py scripts/validate_release_security.py scripts/generate_go_enforcement_contracts.py`
- `python3 scripts/validate_release_security.py && bash scripts/validate-boundaries.sh .`
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js && git diff --check`

Recommended next issue: add operational drill history for returning promoted environments to Python-only mode.

## Phase 7 Go Backend Rollback Controls

Status: complete for the current public-safe promoted backend rollback-control slice.

Completed implementation:
- Added `CAVRA_GO_ROLLBACK_PLAN` and `rollback_plan_path` support to the Go backend configuration.
- Added `go_rollback_readiness_report` with rollback plan, approval, disabled-mode target, required control, recovery-step, and evidence-reference checks.
- Added fail-closed promoted-mode evaluation so Go is selected only when both promotion readiness and rollback readiness are `ready`.
- Added CLI command `cavra runtime go-rollback-readiness`.
- Added FastAPI endpoint `/runtime/go-pilot/rollback-readiness`.
- Added `go_backend_rollback` to `/deployment/production-readiness`, `/console/config`, and the Evidence Console Production Readiness panel.
- Added tests for default `not_requested`, missing rollback plan, valid rollback plan, promoted-mode rollback fallback, and promoted-mode Go selection with rollback controls.
- Added `docs/go-backend-rollback.md`, `docs/wiki/Go-Backend-Rollback.md`, and `docs/diagrams/go-backend-rollback.svg`.
- Updated README, feature inventory, production deployment validation, Go parity docs, pilot/promotion docs, productization docs, production roadmap, and wiki navigation.

Validation:
- `python3 -m pytest tests/test_go_backend.py tests/test_api.py::test_api_deployment_production_readiness tests/test_api.py::test_api_go_backend_rollback_readiness tests/test_cli.py::test_runtime_go_rollback_readiness_cli_reports_not_requested tests/test_policy_authoring.py::test_production_readiness_report_marks_missing_controls -q`
- `python3 -m ruff check src/cavra/go_backend.py src/cavra/cli.py src/cavra/api.py src/cavra/policy_authoring.py tests/test_go_backend.py tests/test_api.py tests/test_cli.py tests/test_policy_authoring.py`
- `python3 -m pytest -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m ruff check src/ tests/ scripts/package_go_release.py scripts/validate_release_security.py scripts/generate_go_enforcement_contracts.py`
- `python3 scripts/validate_release_security.py && bash scripts/validate-boundaries.sh .`
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js && git diff --check`

Recommended next issue: delivered below as rollback rehearsal evidence and dashboard visibility.

## Phase 7 Go Backend Rollback Rehearsal Evidence

Status: complete for the current public-safe promoted backend rollback-rehearsal slice.

Completed implementation:
- Added `CAVRA_GO_ROLLBACK_REHEARSAL_EVIDENCE` and `rollback_rehearsal_path` support to the Go backend configuration.
- Added `go_rollback_rehearsal_report` with rehearsal metadata, fallback verification, recovery SLA, runbook, approval linkage, and evidence-reference checks.
- Added fail-closed promoted-mode evaluation so Go is selected only when promotion readiness, rollback readiness, and rollback rehearsal evidence are `ready`.
- Added CLI command `cavra runtime go-rollback-rehearsal`.
- Added FastAPI endpoint `/runtime/go-pilot/rollback-rehearsal`.
- Added `go_backend_rollback_rehearsal` to `/deployment/production-readiness`, `/console/config`, and the Evidence Console Production Readiness panel.
- Added dashboard fields for rehearsal status, recovery target, and rehearsal evidence references.
- Added tests for default `not_requested`, missing rehearsal evidence, valid rehearsal evidence, promoted-mode rehearsal fallback, and promoted-mode Go selection with rehearsal evidence.
- Added `docs/go-backend-rollback-rehearsal.md`, `docs/wiki/Go-Backend-Rollback-Rehearsal.md`, and `docs/diagrams/go-backend-rollback-rehearsal.svg`.
- Updated README, feature inventory, production deployment validation, Go parity docs, pilot/promotion/rollback docs, productization docs, production roadmap, and wiki navigation.

Validation:
- `python3 -m pytest tests/test_go_backend.py tests/test_cli.py tests/test_api.py::test_api_deployment_production_readiness tests/test_api.py::test_api_go_backend_rollback_rehearsal tests/test_policy_authoring.py -q`
- `python3 -m pytest -q`
- `cd go/cavra-runtime && go test ./...`
- `python3 -m ruff check src/ tests/ scripts/package_go_release.py scripts/validate_release_security.py scripts/generate_go_enforcement_contracts.py`
- `python3 scripts/validate_release_security.py && bash scripts/validate-boundaries.sh .`
- `node --check apps/sandbox-ui/config.js && node --check apps/sandbox-ui/sandbox.js && git diff --check`

User stories:
- As an incident commander, I can prove rollback has been rehearsed before Go becomes the selected optional backend.
- As a platform owner, I can see rehearsal status, recovery time, and evidence references in the Evidence Console.
- As a security reviewer, I can require that rehearsal evidence maps to the approved rollback plan.
- As an auditor, I can attach public-safe rehearsal metadata to release evidence without exposing private endpoint details.

Enterprise challenge solved:
- Turns rollback from a written plan into exercised evidence before promoted Go backend use.
- Gives enterprise reviewers dashboard visibility into recovery timing and fallback verification.
- Keeps private runbooks, secrets, endpoint scripts, and customer data outside the public Community Edition.

Recommended next issue: delivered below as rollback drill history.

## Phase 7 Go Backend Rollback Drill History

Status: complete for the current public-safe promoted backend drill-history slice.

Completed implementation:
- Added `CAVRA_GO_ROLLBACK_DRILL_HISTORY`, `CAVRA_GO_ROLLBACK_DRILL_MAX_AGE_DAYS`, and Go backend configuration fields for rollback drill history.
- Added `go_rollback_drill_history_report` with latest drill, target mode, fallback verification, recovery SLA, freshness, runbook, and evidence-reference checks.
- Added fail-closed promoted-mode evaluation so Go is selected only when promotion readiness, rollback readiness, rollback rehearsal evidence, and drill history are `ready`.
- Added CLI command `cavra runtime go-rollback-drills`.
- Added FastAPI endpoint `/runtime/go-pilot/rollback-drills`.
- Added `go_backend_rollback_drill_history` to `/deployment/production-readiness`, `/console/config`, and the Evidence Console Production Readiness panel.
- Added dashboard fields for drill status, latest drill ID, timestamp, and evidence references.
- Added tests for default `not_requested`, missing drill history, valid fresh drill history, promoted-mode drill fallback, and promoted-mode Go selection with drill history.
- Added `docs/go-backend-rollback-drill-history.md`, `docs/wiki/Go-Backend-Rollback-Drill-History.md`, and `docs/diagrams/go-backend-rollback-drill-history.svg`.
- Updated README, feature inventory, production deployment validation, Go parity docs, pilot/promotion/rehearsal docs, productization docs, production roadmap, and wiki navigation.

Validation:
- `python3 -m pytest tests/test_go_backend.py tests/test_cli.py tests/test_api.py::test_api_deployment_production_readiness tests/test_api.py::test_api_go_backend_rollback_drills tests/test_policy_authoring.py -q`

User stories:
- As an incident commander, I can prove that return-to-Python rollback is practiced on an operational cadence.
- As a platform owner, I can see the latest drill ID, timestamp, recovery target, and evidence references in the Evidence Console.
- As a security reviewer, I can block promoted mode when rollback drills become stale.
- As an auditor, I can review drill history without exposing private customer or endpoint details.

Enterprise challenge solved:
- Converts rollback practice into a production readiness gate instead of informal operational memory.
- Gives enterprise reviewers evidence that promoted Go backend use remains reversible over time.
- Keeps private runbooks, endpoint identifiers, customer names, and secrets outside the public Community Edition.

Recommended next issue: add recurring rollback drill scheduling and stale-drill notification delivery.
