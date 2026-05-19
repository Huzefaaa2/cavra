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

Recommended next issue: add endpoint remediation SLA breach, escalation, and executive release governance reporting.
