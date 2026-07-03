# CAVRA Unified Enterprise Product Enhancement Roadmap

Last updated: 2026-07-03

This roadmap converts the merged product enhancement review into a numbered implementation tracker for CAVRA. It is intentionally written as a product and engineering control document, not as a marketing summary.

## Scope Decision

CAVRA is being planned as a unified AI governance control plane for two governed asset classes:

- **Agent actions:** file writes, shell commands, Git operations, MCP tool calls, CI/CD triggers, cloud operations, infrastructure changes, and production workflow actions.
- **Models and artifacts:** model registry entries, model metadata, deployment packages, AI supply-chain artifacts, assessment findings, drift signals, and compliance evidence.

The common control planes are:

- **Decision plane:** policy evaluation, approvals, action gating, promotion gating, and fail-open/fail-closed behavior.
- **Identity and trust plane:** SSO, RBAC/ABAC, workspaces, tenant boundaries, agent identity, model ownership, and trust roots.
- **Evidence plane:** signed evidence, immutable audit trails, KMS/HSM custody, attestations, and verifier tooling.
- **Posture plane:** AISPM, compliance mapping, executive reporting, red-team results, findings, blockers, and readiness gates.

![CAVRA unified enterprise roadmap](../wiki/assets/textbook/cavra-unified-enterprise-roadmap.svg)

## Status Legend

| Status | Meaning |
| --- | --- |
| Completed | Implemented or documented, pushed to the relevant repository, and verified for the stated scope. |
| In Progress | Work has started and has an active implementation path. |
| Planned | Accepted requirement, not yet implemented. |
| Blocked | Cannot proceed until a dependency or external input is available. |
| Deferred | Accepted but intentionally moved out of the current delivery window. |

## Phase Dependency Map

| Phase | Focus | Primary Dependencies | Current Status | Exit Condition |
| --- | --- | --- | --- | --- |
| 0 | Positioning and public roadmap | Review agreement, product scope decision | Completed | README, wiki, and product site describe unified agent-action plus model/artifact governance and link to this tracker. |
| 1 | Foundation trust | Phase 0 | Planned | Security governance, API contract, signed release, SBOM, and buyer trust documentation are publishable. |
| 2 | Identity, data, and multi-tenancy | Phase 1 API contract and trust model | Planned | Enterprise identity, RBAC/ABAC, tenant/workspace isolation, and production data architecture are implemented and tested. |
| 3 | Evidence, audit, and compliance | Phase 1 trust model, Phase 2 tenancy model | Planned | KMS-backed evidence, immutable audit log, and dynamic compliance mapping are production-ready. |
| 4 | Zero-trust scanning and connectors | Phase 2 tenancy, Phase 3 evidence/audit | Planned | Certified connector SDK, priority connectors, and model/artifact scanner agents work without raw model/data egress. |
| 5 | Policy lifecycle and event core | Phase 2 identity/data, Phase 4 connectors | Planned | Policy authoring, test, shadow, rollback, and event-driven continuous assessment paths are working. |
| 6 | Scale and ecosystem expansion | Phases 1-5 | Planned | Benchmarks, chaos tests, broader agent adapters, LLM guardrails, supply-chain checks, and red-team automation are validated. |

## Numbered Enhancement Tracker

| ID | Phase | Problem(s) | Requirement | Dependency | Status | Code/docs status | Tests and verification | GitHub evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R0.1 | 0 | P8, P16, P22 | Document CAVRA as one unified control plane for agent actions and models/artifacts. | None | Completed | README, wiki, and product site updated to state the unified scope. | Markdown link checks and product-site validation. | `README.md`, `docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md`, wiki roadmap, product-site roadmap section. |
| R0.2 | 0 | P1-P22 | Publish this numbered product enhancement roadmap with dependencies and status. | R0.1 | Completed | Roadmap added in public repo and mirrored into GitHub Wiki. | `git diff --check`; wiki page renders as Markdown. | This document and `CAVRA-Unified-Enterprise-Enhancement-Roadmap.md`. |
| R0.3 | 0 | P1-P22 | Add a unified architecture-roadmap diagram for the public repo and wiki. | R0.1 | Completed | Animated SVG added under textbook assets. | SVG is text-readable and motion-safe. | `docs/wiki/assets/textbook/cavra-unified-enterprise-roadmap.svg`. |
| R0.4 | 0 | P22 | Make product website point buyers to the roadmap, trust posture, and implementation sequence. | R0.1, R0.2 | Completed | Product site includes a roadmap section, roadmap nav entry, and links to the repo/wiki tracker. | Product-site Playwright validation. | `apps/product-site` equivalent in `cavra-product-site` repo. |
| R1.1 | 1 | P6, P12 | Harden public security governance: responsible disclosure, supported versions, vulnerability handling, and release security criteria. | R0.2 | Planned | Existing `SECURITY.md` is the baseline; expanded enterprise trust criteria still required. | Security-document review and release checklist validation. | `SECURITY.md`, future release verification. |
| R1.2 | 1 | P10, P12 | Establish multi-maintainer governance with CODEOWNERS, maintainer onboarding, RFC process, and release cadence. | R1.1 | Planned | Needs CODEOWNERS, governance document, RFC template, maintainer guide. | Repository governance review. | Future `CODEOWNERS`, `docs/governance/*`. |
| R1.3 | 1 | P6, P12 | Produce signed releases, SBOMs, provenance, and repeatable release attestations. | R1.2 | Planned | Needs Sigstore/cosign or equivalent workflow and SBOM artifact generation. | Release workflow run with SBOM and signature verification. | Future GitHub Actions release artifacts. |
| R1.4 | 1 | P15 | Publish OpenAPI 3.x contract and API versioning discipline. | R0.1 | Planned | FastAPI exists; formal exported OpenAPI contract and compatibility policy are required. | OpenAPI schema validation and API compatibility test. | Future `openapi/`, API docs, CI validation. |
| R1.5 | 1 | P22 | Publish CISO and buyer trust documentation: architecture, data flow, encryption, HA, compliance support, and product boundaries. | R0.4 | Planned | Wiki and product site contain baseline trust text; procurement-grade trust pack remains to be built. | Trust-pack review against buyer questionnaire. | Future `docs/trust/*`, wiki trust pages. |
| R2.1 | 2 | P1, P13 | Implement enterprise identity: OIDC/SAML, SCIM, RBAC, ABAC, break-glass, model-owner roles, and security-operator roles. | R1.4 | Planned | Existing hooks need production-grade implementation, config, tests, and docs. | SSO integration tests, RBAC matrix tests, break-glass audit tests. | Future identity modules and docs. |
| R2.2 | 2 | P2, P13 | Implement production multi-tenant persistence with workspaces, Postgres, tenant isolation, and migration path from JSON/SQLite. | R2.1 | Planned | Community JSON/SQLite remains baseline; enterprise-grade data layer required. | Tenant isolation tests, migration tests, concurrency tests. | Future persistence modules and migrations. |
| R2.3 | 2 | P11, P2, P13 | Define HA topology: stateless workers, queues, health checks, backup/DR, RTO/RPO, and data residency. | R2.2 | Planned | Azure/deployment docs exist; production HA architecture needs implementation and validation. | HA smoke, failover, restore, and data residency validation. | Future deployment modules and runbooks. |
| R3.1 | 3 | P4 | Add KMS/HSM-backed evidence signing, key rotation, custody policy, and independent verifier support. | R2.2 | Planned | Local signing exists; enterprise KMS/HSM custody is required. | KMS integration tests, signature verification, rotation tests. | Future evidence signer modules and docs. |
| R3.2 | 3 | P14 | Add immutable, append-only audit log separate from evidence bundles. | R2.2, R3.1 | Planned | Evidence bundles exist; immutable audit log is a separate requirement. | Tamper-evidence tests, append-only tests, SIEM export validation. | Future audit-log store and export artifacts. |
| R3.3 | 3 | P5, P17 | Add compliance mapping packs with clause-level mapping for NIST AI RMF, ISO/IEC 42001, OWASP LLM/GenAI, NIST SSDF, and EU AI Act. | R3.2 | Planned | AISPM reporting exists; dynamic clause mapping packs remain to be implemented. | Control-pack schema tests, finding-to-clause tests, report validation. | Future compliance pack modules and wiki docs. |
| R3.4 | 3 | P21, P5 | Build auditor, BI, executive, and board-ready reporting exports. | R3.3 | Planned | Report center foundation exists; executive reporting needs report builders and templates. | PDF/CSV/JSON export validation and sample evidence room review. | Future report builders and evidence samples. |
| R4.1 | 4 | P3, P15 | Create public connector/plugin SDK with stable interfaces, certification rules, examples, and compatibility tests. | R1.4 | Planned | Provider interfaces exist; plugin SDK and certification process are required. | SDK tests, example connector test, compatibility matrix. | Future SDK package and docs. |
| R4.2 | 4 | P3 | Deliver priority certified connectors: GitHub, GitLab, Azure Repos, GitHub Actions, Jenkins, Splunk, Sentinel, ServiceNow, Jira, Slack, and Teams. | R4.1, R2.1 | Planned | Reference connectors exist in places; certified production connectors remain planned. | Connector contract tests and live sandbox validation. | Future connector modules and certification records. |
| R4.3 | 4 | P3, P16, P20 | Add model registry connectors that work by reference: MLflow, SageMaker, Hugging Face, and Weights & Biases. | R4.1, R3.2 | Planned | Model/artifact governance scope is now accepted; connectors need implementation. | No-raw-model-egress tests, metadata hash validation. | Future model-registry connectors. |
| R4.4 | 4 | P16, P20 | Build zero-trust scanner agent that runs in customer VPC/on-prem and emits metadata, hashes, risk scores, and evidence only. | R4.3, R3.1 | Planned | Architecture principle documented; scanner agent implementation pending. | Egress tests, scanner evidence tests, reference deployment validation. | Future scanner agent package and zero-trust demo. |
| R5.1 | 5 | P9 | Add OPA/Rego policy path alongside current policy engine with testable, Git-versioned policies. | R2.1, R4.1 | Planned | YAML policy engine exists; OPA/Rego portability path planned. | Policy unit tests, Rego evaluation parity tests. | Future policy engine modules and docs. |
| R5.2 | 5 | P9 | Build policy lifecycle tooling: authoring UI, linting, versioning, shadow mode, dry run, rollback, and approval workflow builder. | R5.1 | Planned | CLI and docs exist; lifecycle UI and workflows remain planned. | Policy lifecycle integration tests and visual validation. | Future UI and workflow modules. |
| R5.3 | 5 | P18, P11 | Add event-driven continuous monitoring with event bus triggers for agent actions, model registration, drift, and production promotions. | R2.3, R4.4 | Planned | Current assessments are request/periodic oriented; event-driven core planned. | Event replay, dedupe, latency, and stale-assessment tests. | Future event modules and runbooks. |
| R6.1 | 6 | P7, P11 | Publish latency, throughput, HA, and failure-mode benchmarks with SLO regression gates. | R2.3, R5.3 | Planned | Performance claims need repeatable benchmark evidence. | Benchmark suite and CI regression thresholds. | Future benchmark reports. |
| R6.2 | 6 | P8 | Expand beyond coding agents through generic adapter SDK and action taxonomy. | R4.1, R5.1 | Planned | Runtime authority exists for coding/engineering actions; generic agent taxonomy planned. | Adapter contract tests and sample non-coding agent scenario. | Future adapter SDK and examples. |
| R6.3 | 6 | P19, P20, P21 | Add native LLM guardrail testing, AI supply-chain scanning, malicious model checks, and red-team automation. | R4.4, R5.3 | Planned | External guardrail integration is not enough; native checks remain planned. | Prompt-injection tests, serialization scan tests, red-team report validation. | Future guardrail and red-team modules. |
| R6.4 | 6 | P16, P22, P3 | Publish zero-trust quickstart demo and reference deployments for Docker Compose, Helm, Terraform, Azure, and customer-side scanner operation. | R4.4, R6.1 | Planned | Deployment docs exist; zero-trust scanner demo and reference deployments remain planned. | End-to-end reproducible demo and deployment smoke tests. | Future reference deployments and product-site demo. |

## Open Engineering Decisions

| Decision | Options | Required Before |
| --- | --- | --- |
| Tenant isolation model | Schema-per-tenant, row-level security, database-per-tenant, or hybrid. | R2.2 |
| Policy engine strategy | Replace YAML engine with OPA/Rego, run both, or compile YAML into Rego. | R5.1 |
| KMS/HSM abstraction | Cloud-provider adapters, Vault Transit first, PKCS#11 first, or adapter interface plus certified providers. | R3.1 |
| Connector certification | Core-maintained only, partner-maintained with certification, or community-maintained with trust tiers. | R4.1 |
| Zero-trust scanner packaging | Container image, Helm chart, Terraform module, air-gapped bundle, or all of the above. | R4.4 |
| Model/artifact metadata schema | Minimal hashes and risk scores only, or richer SBOM-like AI artifact schema. | R4.3 |

## Immediate Next Implementation Steps

1. Convert this roadmap into GitHub issues or a GitHub Project when the team is ready to assign owners.
2. Implement Phase 1 trust work: CODEOWNERS, governance/RFC docs, OpenAPI export, release signing/SBOM plan, and buyer trust pack.
3. Start design records for R2.2 tenant isolation, R3.1 KMS/HSM signing, R4.1 plugin SDK, and R4.4 zero-trust scanner.
4. Keep this tracker current by updating the `Status`, `Code/docs status`, `Tests and verification`, and `GitHub evidence` columns whenever code is pushed and validated.
