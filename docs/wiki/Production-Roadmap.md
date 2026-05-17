# Production Roadmap

The CAVRA roadmap is priority-based, not calendar-based.

## Phase 1: Productization Foundation

Status: complete in PR #1.

Delivered CAVRA identity, CLI, MCP server, Claude Code setup, policy packs, runtime decisions, FastAPI app contract, sandbox, Docker validation, enterprise docs, and CAVRA diagrams.

## Phase 2: Policy Engine Hardening

Status: complete.

Implemented strict policy schema validation, policy inheritance, signature metadata, policy tests, semantic policy diff, and stable compiled policy output.

## Phase 3: Evidence Hub and Attestation

Status: near complete; remaining follow-up is hosted attestation artifact retrieval.

Implemented evidence bundle manifests, checksums, HMAC and Ed25519 signatures, trust-root bundles, PR attestation output and verification, SIEM export payloads, compliance reports, retention controls, immutable storage reference exporters, SQLite and JSON evidence metadata search, API persistence, console API wiring, and idempotent migration automation.

## Phase 4: Approval Router

Status: in progress.

Implemented approval request JSON persistence, API and CLI approval queue, approve/deny/expire lifecycle state, break-glass override evidence, and approval outcome linkage into evidence and PR attestations.

Next: routing policies, SQLite approval persistence, console approval views, Jira/ServiceNow references, and Slack/Teams notification payloads.

## Phase 5: Agent Registry and MCP Trust Registry

Implement governed agent identities, MCP server trust tiers, tool capability classification, default-deny unknown server mode, and registry-backed runtime decisions.

## Phase 6: Console and Persistent API

Implement database-backed API and initial console for sessions, decisions, approvals, policies, evidence, integrations, MCP trust, and agents.

## Phase 7: Go Enforcement Plane

Implement Go runtime backend, generated protobuf clients, local daemon, CI runner mode, parity tests, and air-gapped binary.

## Phase 8: Enterprise Integrations

Implement GitHub required check, GitLab/Azure DevOps templates, SIEM exporters, ITSM connectors, OIDC/RBAC, and immutable evidence store references.

## Phase 9: Public Sandbox

Deploy a public Before the Agent Acts sandbox with real policy decisions and downloadable evidence.

## Phase 10: Production Release

Implement SBOM, signed releases, vulnerability disclosure, security scans, dependency audit, backup/restore docs, upgrade docs, performance tests, and procurement readiness.
