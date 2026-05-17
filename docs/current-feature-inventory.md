# Current Feature Inventory

Implemented modules: policy registry, runtime guard, session audit, command interceptor, PR attestation exporter, webhook exporter, Typer CLI, MCP server, FastAPI app, sandbox decision model.

Existing CLI commands: `version`, `evaluate`, `agent start`, `agent exec`, `agent attest`, `policy list`, `policy describe`, `policy validate`, `policy test`, `policy explain`, `policy compile`, `policy diff`, `policy sign`, `policy verify`, `policy simulate`, `policy dry-run`, `policy init`, `init claude-code`, `demo before-the-agent-acts`.

Existing API endpoints: `/health`, `/version`, `/policies`, `/policy-packs`, `/decisions`, `/sessions`, `/agents`, `/repositories`, `/approvals`, `/evidence`, `/integrations`, `/mcp/servers`, `/mcp/trust`, `/risk/events`, `/compliance/mappings`, and sandbox endpoints under `/api/sandbox`.

Existing policy packs: CAVRA baseline, banking, PCI DSS, HIPAA, SOX, NIST SSDF, ISO 27001, EU AI Act, OWASP LLM/agentic, MCP enterprise, Kubernetes prod, Terraform/OpenTofu prod, cloud IAM, GitHub Enterprise, GitLab Enterprise.

Current controls: file reads, file writes, shell commands, Terraform/OpenTofu, Kubernetes, cloud IAM commands, Git protected branch push, MCP unknown server blocking, audit evidence, approval routing hints, and PR attestation.

Known gaps: persistent API storage, real approval provider integrations, cryptographic signing beyond local SHA-256 signatures, packaged Go backend, hosted sandbox deployment, and vendor-specific hooks beyond the MCP/CLI path.

Refactor recommendations: typed policy models, JSON Schema validation in command path, persistent evidence store, policy inheritance resolver, and parity test suite for future Go enforcement.
