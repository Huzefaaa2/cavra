# Production Roadmap

The CAVRA roadmap is priority-based, not calendar-based.

## Phase 1: Productization Foundation

Status: complete in PR #1.

Delivered CAVRA identity, CLI, MCP server, Claude Code setup, policy packs, runtime decisions, FastAPI app contract, sandbox, Docker validation, enterprise docs, and CAVRA diagrams.

## Phase 2: Policy Engine Hardening

Status: complete.

Implemented strict policy schema validation, policy inheritance, signature metadata, policy tests, semantic policy diff, and stable compiled policy output.

## Phase 3: Evidence Hub and Attestation

Status: near complete with governed artifact retrieval and production deployment validation delivered.

Implemented evidence bundle manifests, checksums, HMAC and Ed25519 signatures, trust-root bundles, PR attestation output and verification, SIEM export payloads, compliance reports, retention controls, immutable storage reference exporters, SQLite and JSON evidence metadata search, governed artifact retrieval APIs, API persistence, console API wiring, and idempotent migration automation.

## Phase 4: Approval Router

Status: complete for the current production-readiness slice.

Implemented approval request JSON and SQLite persistence, API and CLI approval queue, approve/deny/expire lifecycle state, break-glass override evidence, default routing policies, repository-specific routing files, local claims-based approval authorization, signed OIDC/JWKS validation, repository RBAC policy files, reference notification payloads, credential-free provider request specs, secret-backed live provider delivery with redacted evidence, console approval queue actions, console break-glass creation, approval audit detail views, and approval outcome linkage into evidence and PR attestations.

Next: continue Phase 8 with immutable evidence store deployment references and OIDC/RBAC deployment bundles.

## Phase 5: Agent Registry and MCP Trust Registry

Status: complete for the current production-readiness slice.

Implemented JSON/SQLite governed agent identities, MCP server trust tiers, owner/capability/approval-state metadata, API and CLI access, default-deny unknown server mode, predefined profiles for Claude Code, Codex, Copilot, Cursor, Gemini CLI, and AWS Q Developer, MCP tool classification for filesystem, shell, network, database, SaaS, cloud, and repository capabilities, console registry views, and registry-backed MCP runtime decisions.

Next: immutable evidence store deployment references and OIDC/RBAC deployment bundles.

## Phase 6: Console and Persistent API

Status: started.

Implemented JSON and SQLite activity persistence for sessions and decisions, API filters for session, agent, repository, policy pack, outcome, severity, and action type, repository inventory and policy rollout JSON/SQLite persistence, repository and rollout API filters, policy rollout detail API and console drill-downs, policy-pack authoring previews, rollout change planning/apply workflows, production deployment validation, integration inventory JSON/SQLite persistence, integration API filters, evidence artifact retrieval and console download views, persistent API store status, backup, restore, retention-plan operations, read-only operations API endpoints, read-only console security boundary reporting, authenticated console session validation, RBAC-enforced console mutations, console Activity Explorer views, and console repository/rollout/integration views.

Next: immutable evidence store deployment references and OIDC/RBAC deployment bundles.

## Phase 7: Go Enforcement Plane

Implement Go runtime backend, generated protobuf clients, local daemon, CI runner mode, parity tests, and air-gapped binary.

## Phase 8: Enterprise Integrations

Started with a GitHub required check, reusable GitHub Actions templates, GitLab CI and Azure Pipelines enforcement examples, evidence verification in branch protection, CI evidence artifact upload, approval-bound signed policy publishing, and live SIEM/ITSM/ChatOps connector execution hooks.

Next: OIDC/RBAC deployment references and immutable evidence store references.

## Phase 9: Public Sandbox

Deploy a public Before the Agent Acts sandbox with real policy decisions and downloadable evidence.

## Phase 10: Production Release

Implement SBOM, signed releases, vulnerability disclosure, security scans, dependency audit, backup/restore docs, upgrade docs, performance tests, and procurement readiness.
