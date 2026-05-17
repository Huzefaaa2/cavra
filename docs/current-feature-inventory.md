# Current Feature Inventory

Implemented modules: policy registry, runtime guard, session audit, command interceptor, PR attestation exporter, webhook exporter, approval router, evidence hub, Typer CLI, MCP server, FastAPI app, sandbox decision model.

Existing CLI commands: `version`, `evaluate`, `agent start`, `agent exec`, `agent attest`, `policy list`, `policy describe`, `policy validate`, `policy test`, `policy explain`, `policy compile`, `policy diff`, `policy sign`, `policy verify`, `policy simulate`, `policy dry-run`, `policy init`, `init claude-code`, `demo before-the-agent-acts`.

Policy engine hardening: `policy validate` uses JSON Schema, `policy compile` emits normalized output and accepts overlays, `policy diff` reports semantic added/removed/changed paths, `policy sign` emits signature metadata, `policy verify` detects digest tampering, and policy packs can inherit parent packs through `metadata.inherits`.

Evidence hub: `evidence bundle` creates `manifest.json`, `evidence.json`, `pr-attestation.md`, `compliance-mapping.md`, `siem-event.json`, and `sandbox-run-summary.json`; `evidence verify` validates checksums plus optional HMAC or Ed25519 signatures; trust-root bundles, retention artifacts, immutable storage plans, SQLite metadata indexing, and PR attestation verification are available through the CLI.

Approval router: `approval create`, `list`, `approve`, `deny`, `expire`, `break-glass`, `route`, `migrate`, `export-notifications`, `provider-requests`, and `deliver` support JSON or SQLite stores, repository routing files, local claims authorization, signed OIDC/JWKS validation, repository RBAC policies, provider payload exports, credential-free provider request specs, live provider delivery with redacted evidence, console break-glass creation, and approval audit detail views.

Existing API endpoints: `/health`, `/version`, `/policies`, `/policy-packs`, `/decisions`, `/sessions`, `/agents`, `/repositories`, `/approvals`, `/evidence`, `/integrations`, `/mcp/servers`, `/mcp/trust`, `/risk/events`, `/compliance/mappings`, and sandbox endpoints under `/api/sandbox`.

Agent and MCP registry: `registry agent-register`, `registry agent-list`, `registry profiles`, `registry mcp-register`, `registry mcp-list`, `registry mcp-check`, `registry mcp-classifications`, and `registry migrate` support JSON/SQLite governed agent identities, MCP trust tiers, approved tools, capabilities, owner, approval state, last-seen metadata, predefined agent capability profiles, MCP tool classifications, console registry views, and registry-backed MCP runtime decisions.

Existing policy packs: CAVRA baseline, banking, PCI DSS, HIPAA, SOX, NIST SSDF, ISO 27001, EU AI Act, OWASP LLM/agentic, MCP enterprise, Kubernetes prod, Terraform/OpenTofu prod, cloud IAM, GitHub Enterprise, GitLab Enterprise.

Current controls: file reads, file writes, shell commands, Terraform/OpenTofu, Kubernetes, cloud IAM commands, Git protected branch push, MCP unknown server blocking, audit evidence, approval routing, claims-aware approval decisions, and PR attestation.

Known gaps: full persistent API storage for sessions and decisions, packaged Go backend, hosted sandbox deployment, hosted attestation artifact retrieval, and vendor-specific hooks beyond the MCP/CLI path.

Refactor recommendations: typed policy models, JSON Schema validation in command path, persistent evidence store, policy inheritance resolver, and parity test suite for future Go enforcement.
