# Current Feature Inventory

Implemented modules: policy registry, policy authoring preview, approval-bound signed policy publishing, rollout change planning, runtime guard, session audit, command interceptor, PR attestation exporter, webhook exporter, connector execution hooks, approval router, evidence hub, evidence artifact retrieval, CI/CD required-check templates, activity persistence, repository inventory, policy rollout persistence, integration inventory, persistent API operations, production deployment validation, Typer CLI, MCP server, FastAPI app, sandbox decision model.

Existing CLI commands: `version`, `evaluate`, `agent start`, `agent exec`, `agent attest`, `policy list`, `policy describe`, `policy validate`, `policy test`, `policy explain`, `policy compile`, `policy diff`, `policy sign`, `policy verify`, `policy simulate`, `policy dry-run`, `policy init`, `integration deliver`, `ops stores`, `ops backup`, `ops restore`, `ops retention-plan`, `init claude-code`, `demo before-the-agent-acts`.

Policy engine hardening: `policy validate` uses JSON Schema, `policy compile` emits normalized output and accepts overlays, `policy diff` reports semantic added/removed/changed paths, `policy sign` emits signature metadata, `policy verify` detects digest tampering, and policy packs can inherit parent packs through `metadata.inherits`.

Evidence hub: `evidence bundle` creates `manifest.json`, `evidence.json`, `pr-attestation.md`, `compliance-mapping.md`, `siem-event.json`, and `sandbox-run-summary.json`; `evidence verify` validates checksums plus optional HMAC or Ed25519 signatures; trust-root bundles, retention artifacts, immutable storage plans, AWS S3 Object Lock and Azure Blob immutability deployment references, SQLite metadata indexing, PR attestation verification, and governed artifact retrieval are available.

Approval router: `approval create`, `list`, `approve`, `deny`, `expire`, `break-glass`, `route`, `migrate`, `export-notifications`, `provider-requests`, and `deliver` support JSON or SQLite stores, repository routing files, local claims authorization, signed OIDC/JWKS validation, repository RBAC policies, provider payload exports, credential-free provider request specs, live provider delivery with redacted evidence, console break-glass creation, and approval audit detail views.

Existing API endpoints: `/health`, `/version`, `/policies`, `/policy-packs`, `/policy-pack-catalog`, `/policy-packs/draft`, `/policy-packs/publish-plan`, `/policy-packs/publish-request`, `/policy-packs/publish`, `/policy-rollouts/change-plan`, `/policy-rollouts/apply-change`, `/deployment/production-readiness`, `/decisions`, `/sessions`, `/agents`, `/repositories`, `/approvals`, `/evidence`, `/evidence/{session_id}/artifacts`, `/integrations`, `/integrations/{integration_id}/deliver`, `/mcp/servers`, `/mcp/trust`, `/risk/events`, `/compliance/mappings`, and sandbox endpoints under `/api/sandbox`.

Activity persistence: `POST /decisions` evaluates and persists decisions, `GET /decisions` searches decisions by session, agent, repository, policy pack, outcome, severity, and action type, and `GET /sessions` searches session summaries. JSON and SQLite stores are supported through `CAVRA_ACTIVITY_STORE` and `CAVRA_ACTIVITY_DB`.

Repository inventory and policy rollout persistence: `POST /repositories` upserts repository scope, ownership, status, protected branch, required check, risk tier, and active policy metadata; `GET /repositories` searches by provider, owner, policy pack, status, and risk tier; `POST /policy-rollouts` upserts rollout mode, state, owner, version, coverage, and evidence references; and `GET /policy-rollouts` searches by repository, policy pack, state, mode, and owner. JSON and SQLite stores are supported through `CAVRA_INVENTORY_STORE` and `CAVRA_INVENTORY_DB`.

Policy rollout drill-downs: `GET /policy-rollout-details/{rollout_id}` joins rollout state with repository inventory, policy pack metadata, matching decision activity, integration inventory, and readiness checks. The console shows rollout detail from each policy rollout row.

Policy authoring and rollout changes: `GET /policy-pack-catalog` summarizes installed policy packs, `POST /policy-packs/draft` validates read-only policy drafts, `POST /policy-packs/publish-plan` previews approval-bound write-back, `POST /policy-packs/publish-request` creates a digest-bound approval request, `POST /policy-packs/publish` writes `policy.yaml` and signature metadata only after matching approval, `POST /policy-rollouts/change-plan` previews rollout transitions, and `POST /policy-rollouts/apply-change` persists rollout changes with verified actor context when OIDC or RBAC is configured.

Integration inventory persistence: `POST /integrations` upserts provider, category, owner, environment, auth mode, endpoint reference, status, health status, capability, repository scope, and evidence metadata; `GET /integrations` searches by provider, category, status, owner, environment, and health status. JSON and SQLite stores are supported through `CAVRA_INTEGRATION_STORE` and `CAVRA_INTEGRATION_DB`.

Connector execution hooks: `POST /integrations/{integration_id}/deliver` and `cavra integration deliver` send events through configured Splunk, Sentinel, Datadog, Slack, Teams, Jira, ServiceNow, or webhook connectors and return redacted delivery evidence. `CAVRA_CONNECTOR_CONFIG` points the API at connector configuration.

Persistent API operations: `ops stores` reports active JSON/SQLite persistence paths, `ops backup` writes checksum-backed JSON and SQLite backups, `ops restore` validates backup checksums before copying stores to a test or live path, and `ops retention-plan` exports JSON and Markdown retention controls. The API exposes read-only `/operations/stores` and `/operations/retention-plan`, and operations now include integration inventory stores.

Production deployment validation: `GET /deployment/production-readiness` checks OIDC, RBAC, CORS, evidence artifact root, policy catalog availability, and persistent store presence. The console includes a Production Readiness panel.

CI/CD required-check templates: `.github/workflows/cavra-governance.yml` exposes `cavra-required-check` for branch protection, validates policy packs, runs lint/tests, generates and verifies evidence, verifies PR attestation, and uploads CI evidence artifacts. Reusable GitHub Actions, GitLab CI, and Azure Pipelines examples live under `examples/`.

Console security boundary and sessions: `GET /console/security-boundary` reports OIDC, repository RBAC, CORS, console permission categories, and operator notes for deployed console/API topologies. `GET /console/session` validates bearer-token OIDC context, returns actor identity, repository permissions, and console permission flags, and console approval or break-glass mutations require verified actor context when OIDC or RBAC is configured.

Evidence artifact retrieval: `GET /evidence/{session_id}/artifacts`, `GET /evidence/{session_id}/artifacts/{artifact_name}`, and `GET /evidence/{session_id}/artifact-bundle` expose allowlisted bundle files for indexed sessions when `CAVRA_EVIDENCE_ARTIFACT_ROOT` is configured. The console shows artifact lists and bundle download links from evidence rows.

Agent and MCP registry: `registry agent-register`, `registry agent-list`, `registry profiles`, `registry mcp-register`, `registry mcp-list`, `registry mcp-check`, `registry mcp-classifications`, and `registry migrate` support JSON/SQLite governed agent identities, MCP trust tiers, approved tools, capabilities, owner, approval state, last-seen metadata, predefined agent capability profiles, MCP tool classifications, console registry views, and registry-backed MCP runtime decisions.

Existing policy packs: CAVRA baseline, banking, PCI DSS, HIPAA, SOX, NIST SSDF, ISO 27001, EU AI Act, OWASP LLM/agentic, MCP enterprise, Kubernetes prod, Terraform/OpenTofu prod, cloud IAM, GitHub Enterprise, GitLab Enterprise.

Current controls: file reads, file writes, shell commands, Terraform/OpenTofu, Kubernetes, cloud IAM commands, Git protected branch push, MCP unknown server blocking, audit evidence, approval routing, claims-aware approval decisions, and PR attestation.

Known gaps: packaged Go backend, hosted sandbox deployment, and OIDC/RBAC deployment reference bundles.

Refactor recommendations: typed policy models, JSON Schema validation in command path, persistent evidence store, policy inheritance resolver, and parity test suite for future Go enforcement.
