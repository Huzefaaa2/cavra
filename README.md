<p align="center">
  <img src="assets/brand/cavra-logo-horizontal.svg" alt="CAVRA - Controlled Agentic Verification and Runtime Authority" width="760">
</p>

# CAVRA
## Controlled Agentic Verification & Runtime Authority

Before the agent acts, CAVRA decides.

CAVRA is a runtime governance and authority layer for AI coding agents. It controls, verifies, approves, blocks, and audits what agents can read, write, execute, connect to, approve, and change across code, cloud, Git, MCP, shell, CI/CD, infrastructure, and regulated engineering workflows.

## What is CAVRA?

CAVRA sits between AI coding agents and meaningful engineering actions. It evaluates file access, shell commands, Git operations, MCP tool calls, infrastructure changes, approvals, and evidence generation before an agent acts.

## Editions and Open-Core Model

This public repository is the CAVRA Community Edition and public product landing repository. Enterprise source code is maintained separately in a private repository and is not part of this public Community Edition.

Community Edition is free to use and includes core local governance, CLI execution, starter policies, public examples, GitHub Action support, evidence formats, and public plugin interfaces. Community runs without a license key.

Enterprise Edition is a paid extension model for SSO, RBAC, private policy packs, central dashboards, compliance reports, organization-wide enforcement, drift monitoring, AI remediation, and SaaS Control Plane integration. Public code exposes only safe hooks for future private modules such as the `cavra_enterprise` package.

Trial Edition should be distributed as a private binary, private Docker image, or hosted SaaS trial. This repository includes trial instructions and public-safe placeholder license interfaces only.

| Feature | Community | Enterprise |
| --- | --- | --- |
| Local scan | Yes | Yes |
| CLI | Yes | Yes |
| Starter policies | Yes | Yes |
| GitHub Action | Yes | Yes |
| SSO | No | Yes |
| RBAC | No | Yes |
| Audit exports | No | Yes |
| Compliance reports | No | Yes |
| Private policy packs | No | Yes |
| Central dashboard | No | Yes |
| Drift monitoring | No | Yes |
| AI remediation | No | Yes |
| SaaS control plane | No | Yes |

Open-core architecture and boundaries:

- [Open-core model](docs/architecture/open-core-model.md)
- [Edition boundaries](docs/architecture/edition-boundaries.md)
- [Plugin architecture](docs/architecture/plugin-architecture.md)
- [SaaS Control Plane design](docs/architecture/saas-control-plane.md)
- [SaaS Control Plane contract](docs/architecture/saas-control-plane-contract.md)
- [Tenant onboarding contract](docs/architecture/tenant-onboarding-contract.md)
- [Entitlement status contract](docs/architecture/entitlement-status-contract.md)
- [Hosted policy registry readiness contract](docs/architecture/hosted-policy-registry-readiness-contract.md)
- [Tenant audit-store operating contract](docs/architecture/tenant-audit-store-operating-contract.md)
- [Billing and subscription boundary](docs/architecture/billing-subscription-boundary.md)
- [Customer operating dashboard and support handoff contract](docs/architecture/customer-operating-dashboard-support-handoff-contract.md)
- [SaaS operating automation contract](docs/architecture/saas-operating-automation-contract.md)
- [SaaS operating automation worker handoff](docs/architecture/saas-operating-automation-worker-handoff.md)
- [SaaS operating automation public contract sync](docs/saas-operating-automation-public-contract-sync.md)
- [Trial and SaaS commercialization batch sync](docs/trial-saas-commercialization-batch-sync.md)
- [Tenant, entitlement, and commercialization batch sync](docs/tenant-entitlement-commercialization-batch-sync.md)
- [Post-onboarding SaaS operating readiness](docs/post-onboarding-saas-operating-readiness.md)
- [Post-onboarding SaaS operating batch sync](docs/post-onboarding-saas-operating-batch-sync.md)
- [SaaS customer operating closeout batch sync](docs/saas-customer-operating-closeout-batch-sync.md)
- [SaaS operating automation batch sync](docs/saas-operating-automation-batch-sync.md)
- [Enterprise trial distribution sync](docs/trial-enterprise-distribution-sync.md)
- [Trial license and evaluator access sync](docs/trial-license-evaluator-access-sync.md)
- [Trial access expiry sync](docs/trial-access-expiry-sync.md)
- [Trial expired follow-up sync](docs/trial-expired-followup-sync.md)
- [Trial conversion readiness sync](docs/trial-conversion-readiness-sync.md)
- [Trial conversion activation handoff sync](docs/trial-conversion-activation-handoff-sync.md)
- [Trial conversion closeout revenue sync](docs/trial-conversion-closeout-revenue-sync.md)
- [Trial conversion executive renewal sync](docs/trial-conversion-executive-renewal-sync.md)
- [Trial conversion customer follow-through sync](docs/trial-conversion-customer-followthrough-sync.md)
- [Trial conversion renewal outcome rollup sync](docs/trial-conversion-renewal-outcome-rollup-sync.md)
- [Trial final commercial renewal closeout sync](docs/trial-final-commercial-renewal-closeout-sync.md)
- [Trial commercialization closure readiness sync](docs/trial-commercialization-closure-readiness-sync.md)
- [Trial commercialization closure release acceptance sync](docs/trial-commercialization-closure-release-acceptance-sync.md)
- [Trial commercialization closure final closeout sync](docs/trial-commercialization-closure-final-closeout-sync.md)
- [Trial commercial launch-readiness handoff sync](docs/trial-commercial-launch-readiness-handoff-sync.md)
- [Trial commercial launch-readiness final approval sync](docs/trial-commercial-launch-readiness-final-approval-sync.md)
- [Trial commercial launch-readiness operating transition sync](docs/trial-commercial-launch-readiness-operating-transition-sync.md)
- [Trial commercial launch-readiness operating closeout sync](docs/trial-commercial-launch-readiness-operating-closeout-sync.md)
- [Trial commercial launch-readiness executive review sync](docs/trial-commercial-launch-readiness-executive-review-sync.md)
- [Trial commercial launch-readiness final archive sync](docs/trial-commercial-launch-readiness-final-archive-sync.md)
- [Trial production observability and support readiness sync](docs/trial-production-observability-support-readiness-sync.md)
- [Trial final release hardening and packaging readiness sync](docs/trial-final-release-hardening-packaging-readiness-sync.md)
- [Trial commercialization closeout and release-to-market approval sync](docs/trial-commercialization-closeout-release-market-approval-sync.md)
- [Trial post-launch operating handoff sync](docs/trial-post-launch-operating-handoff-sync.md)
- [Trial release retrospective and roadmap intake sync](docs/trial-release-retrospective-roadmap-intake-sync.md)
- [Trial final launch retrospective closeout sync](docs/trial-final-launch-retrospective-closeout-sync.md)
- [Roadmap status audit and next batch](docs/roadmap-status-audit-next-batch.md)
- [Roadmap status and next slice](docs/roadmap-status-next-slice.md)
- [Community GA control hardening sync](docs/community-ga-control-hardening-sync.md)
- [Evidence Console Community GA closeout](docs/evidence-console-community-ga-closeout.md)
- [Community GA release checklist](docs/community-ga-release-checklist.md)
- [Community GA release packet template](docs/community-ga-release-packet-template.md)
- [Community GA dry-run release packet](docs/release-packets/community-ga-dry-run-2026-06-04.md)
- [Community GA release packet validation](docs/community-ga-release-packet-validation.md)
- [Community GA v0.1.0 release packet](docs/release-packets/community-ga-v0.1.0.md)
- [Community GA v0.1.0 GitHub Release](https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0)
- [Community GA v0.1.0 release publication](docs/community-ga-v0.1.0-release-publication.md)
- [Community GA v0.1.0 post-release verification](docs/release-verifications/community-v0.1.0-post-release-verification.md)
- [Community GA user-verifiable path](docs/community-ga-user-verifiable-path.md)
- [Production deployment guide validation](docs/production-deployment-guide-validation.md)
- [Go enforcement production hardening](docs/go-enforcement-production-hardening.md)
- [Enterprise integration validation](docs/enterprise-integration-validation.md)
- [Production readiness procurement closeout](docs/production-readiness-procurement-closeout.md)
- [Community release verification runbook](docs/community-release-verification-runbook.md)
- [Community GA v0.1.0 release notes](docs/releases/community-v0.1.0.md)
- [Community maintenance release checklist](docs/community-maintenance-release-checklist.md)
- [Community maintenance release evidence template](docs/community-maintenance-release-evidence-template.md)
- [Community release note freshness](docs/community-release-note-freshness.md)
- [Community v0.1.1 GitHub Release](https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1)
- [Community v0.1.1 release notes](docs/releases/community-v0.1.1.md)
- [Community v0.1.1 maintenance verification](docs/release-verifications/community-v0.1.1-maintenance-verification.md)
- [Community v0.1.1 post-release verification](docs/release-verifications/community-v0.1.1-post-release-verification.md)
- [Community v0.1.2 readiness](docs/community-v0.1.2-readiness.md)
- [Community v0.1.2 release notes](docs/releases/community-v0.1.2.md)
- [Community v0.1.2 maintenance verification](docs/release-verifications/community-v0.1.2-maintenance-verification.md)
- [Community v0.1.2 post-release verification](docs/release-verifications/community-v0.1.2-post-release-verification.md)
- [Community v0.1.3 maintenance planning](docs/community-v0.1.3-maintenance-planning.md)
- [Community v0.1.3 release notes](docs/releases/community-v0.1.3.md)
- [Community v0.1.3 maintenance verification](docs/release-verifications/community-v0.1.3-maintenance-verification.md)
- [Community v0.1.3 post-release verification](docs/release-verifications/community-v0.1.3-post-release-verification.md)
- [Community v1.0.0 stabilization plan](docs/community-v1.0.0-stabilization-plan.md)
- [Community v1.0.0 stabilization packet](docs/release-verifications/community-v1.0.0-stabilization-plan.json)
- [Community v1.0.0 release-candidate hardening](docs/community-v1.0.0-release-candidate-hardening.md)
- [Community v1.0.0 release-candidate hardening packet](docs/release-verifications/community-v1.0.0-release-candidate-hardening.json)
- [Community v1.0.0 release-candidate publication preparation](docs/community-v1.0.0-release-candidate-publication.md)
- [Community v1.0.0 RC1 release notes](docs/releases/community-v1.0.0-rc.1.md)
- [Community v1.0.0 RC1 publication readiness](docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md)
- [Community v1.0.0 release-candidate publication packet](docs/release-verifications/community-v1.0.0-release-candidate-publication.json)
- [Community v1.0.0 RC1 post-publication verification](docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md)
- [Community v1.0.0 RC1 post-publication packet](docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.json)
- [Community v1.0.0 GA readiness](docs/community-v1.0.0-ga-readiness.md)
- [Community v1.0.0 GA readiness packet](docs/release-verifications/community-v1.0.0-ga-readiness.json)
- [Community v1.0.0 GA publication package](docs/community-v1.0.0-ga-publication-package.md)
- [Community v1.0.0 release notes](docs/releases/community-v1.0.0.md)
- [Community v1.0.0 publication readiness](docs/release-verifications/community-v1.0.0-publication-readiness.md)
- [Community v1.0.0 GA publication package packet](docs/release-verifications/community-v1.0.0-ga-publication-package.json)
- [Community v1.0.0 post-publication verification](docs/release-verifications/community-v1.0.0-post-publication-verification.md)
- [Community v1.0.0 post-publication packet](docs/release-verifications/community-v1.0.0-post-publication-verification.json)
- [Community release keyless attestation](docs/community-release-keyless-attestation.md)
- [Community release index](docs/community-release-index.md)
- [Community release index freshness](docs/community-release-index-freshness.md)
- [Community release readiness dashboard](docs/community-release-readiness-dashboard.md)
- [Community release readiness dashboard validation](docs/community-release-readiness-dashboard-validation.md)
- [CAVRA developer portal redesign](docs/sandbox-portal-redesign.md)
- [CAVRA developer portal smoke validation](docs/sandbox-portal-smoke-validation.md)
- [Console closeout operator experience](docs/console-closeout-operator-experience.md)
- [Policy signing key workflow](docs/policy-signing-key-workflow.md)
- [Runtime policy modes](docs/runtime-policy-modes.md)
- [Enterprise features](docs/enterprise/features.md)
- [Enterprise trial](docs/enterprise/trial.md)
- [Enterprise trial self-service access](docs/enterprise/trial-self-service-access.md)
- [Private Enterprise repo plan](docs/architecture/private-enterprise-repo-plan.md)
- [AI Security Posture Dashboard roadmap](docs/ai-security-posture-dashboard-roadmap.md)
- [AI Security Posture Dashboard contract](docs/ai-security-posture-dashboard-contract.md)

## Why CAVRA exists

AI coding agents now inspect repositories, modify code, invoke tools, run shell commands, touch infrastructure, open pull requests, and interact with enterprise workflows. Traditional controls often arrive after the code changed or after a pull request exists. CAVRA makes pre-action enforcement the control point.

## What CAVRA controls

- File reads and writes, including secrets, state files, production config, CI/CD workflows, IAM, PCI, PHI, and regulated data fixtures.
- Commands, including Terraform/OpenTofu, Kubernetes, Azure CLI, AWS CLI, GCP CLI, Git, test runners, package managers, and dangerous shell patterns.
- Git and PR workflows, including protected branches, direct push, force push, required PR attestation, and AI-generated change evidence.
- MCP servers and tools, including filesystem, shell, network, database, SaaS, and unknown server governance.
- Evidence and approvals, including decision logs, signed bundles, PR attestations, SIEM events, and approver routing.

## How CAVRA works

1. An agent requests an action.
2. CAVRA normalizes the action into a decision request.
3. The policy registry loads the active policy pack.
4. Runtime guards evaluate the request before execution.
5. CAVRA returns `allow`, `block`, `require_approval`, `warn`, `audit_only`, or `allow_with_attestation`.
6. Evidence is written for audit, PR review, SIEM export, and compliance mapping.

## Architecture overview

CAVRA keeps the current Python management plane and introduces a Go enforcement-plane roadmap. Python owns policy authoring, evidence, integrations, FastAPI, Claude Code adapters, risk classification, and compliance mapping. Go is planned for low-latency local enforcement, CI runner enforcement, streaming audit events, and air-gapped single-binary deployment. The current Go backend path is explicitly opt-in, defaults to disabled, falls back to Python unless readiness and parity checks pass, and requires separate promotion evidence, rollback controls, rollback rehearsal evidence, and fresh rollback drill history before `promoted` mode can select Go as an optional backend.

Architecture references:

- [C4 context diagram](docs/diagrams/c4-context.md)
- [C4 container diagram](docs/diagrams/c4-container.md)
- [C4 container SVG](docs/diagrams/c4-container.svg)
- [Runtime component diagram](docs/diagrams/c4-component-runtime.md)
- [Runtime decision flow](docs/diagrams/runtime-decision-flow.md)
- [Evidence lifecycle](docs/diagrams/evidence-lifecycle.md)
- [Architecture SVG](docs/diagrams/architecture-context.svg)
- [Runtime flow SVG](docs/diagrams/runtime-flow.svg)
- [Evidence Hub SVG](docs/diagrams/evidence-hub.svg)
- [Policy Lifecycle SVG](docs/diagrams/policy-lifecycle.svg)
- [Developer Journey SVG](docs/diagrams/developer-journey.svg)
- [Transparent Agent Orchestration SVG](docs/diagrams/agent-orchestration.svg)
- [Go parity and sandbox deployment SVG](docs/diagrams/go-parity-sandbox-deployment.svg)
- [Opt-in Go backend pilot SVG](docs/diagrams/go-backend-pilot.svg)
- [Go backend deployment readiness SVG](docs/diagrams/go-backend-deployment-readiness.svg)
- [Go backend promotion gate SVG](docs/diagrams/go-backend-promotion.svg)
- [Go backend rollback controls SVG](docs/diagrams/go-backend-rollback.svg)
- [Go backend rollback rehearsal SVG](docs/diagrams/go-backend-rollback-rehearsal.svg)
- [Go backend rollback drill history SVG](docs/diagrams/go-backend-rollback-drill-history.svg)
- [Go backend rollback drill scheduling SVG](docs/diagrams/go-backend-rollback-drill-scheduling.svg)
- [Go backend rollback drill notification escalation SVG](docs/diagrams/go-backend-rollback-drill-notification-escalation.svg)
- [Go backend rollback drill routing SVG](docs/diagrams/go-backend-rollback-drill-routing.svg)
- [Go backend rollback drill routing history SVG](docs/diagrams/go-backend-rollback-drill-routing-history.svg)
- [Go backend rollback drill console SVG](docs/diagrams/go-backend-rollback-drill-console.svg)
- [Go backend rollback drill acknowledgement controls SVG](docs/diagrams/go-backend-rollback-drill-acknowledgement-controls.svg)
- [Go backend rollback drill bulk acknowledgement audit SVG](docs/diagrams/go-backend-rollback-drill-bulk-acknowledgement-audit.svg)
- [Go backend rollback drill audit delivery retry worker SVG](docs/diagrams/go-backend-rollback-drill-audit-delivery-retry-worker.svg)
- [Go backend rollback drill audit worker health alerts SVG](docs/diagrams/go-backend-rollback-drill-audit-worker-health-alerts.svg)
- [Go backend rollback drill live retry closure evidence SVG](docs/diagrams/go-backend-rollback-drill-live-retry-closure-evidence.svg)
- [Go backend rollback drill retry recovery reporting SVG](docs/diagrams/go-backend-rollback-drill-retry-recovery-reporting.svg)
- [Go backend rollback drill recovery escalation and executive reporting SVG](docs/diagrams/go-backend-rollback-drill-recovery-escalation-executive-reporting.svg)
- [Go backend rollback drill recovery escalation acknowledgement and scheduling SVG](docs/diagrams/go-backend-rollback-drill-recovery-escalation-ack-retry-scheduling.svg)
- [Go backend rollback drill recovery retry health and executive delivery retry SVG](docs/diagrams/go-backend-rollback-drill-recovery-retry-health-and-executive-delivery-retry.svg)
- [Go backend rollback drill executive delivery retry execution and recovery health alerts SVG](docs/diagrams/go-backend-rollback-drill-executive-delivery-retry-execution-and-recovery-health-alerts.svg)
- [Go backend rollback drill executive retry health and recovery health alert retry SVG](docs/diagrams/go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.svg)
- [Go backend rollback drill recovery health alert retry worker and executive retry health alerts SVG](docs/diagrams/go-backend-rollback-drill-recovery-health-alert-retry-worker-and-executive-retry-health-alerts.svg)
- [Go backend rollback drill executive health alert retry and final closure SVG](docs/diagrams/go-backend-rollback-drill-executive-health-alert-retry-final-closure.svg)
- [Go backend rollback drill final readiness and runbook export SVG](docs/diagrams/go-backend-rollback-drill-final-readiness-runbook-export.svg)
- [Go backend rollback drill readiness approval and release record SVG](docs/diagrams/go-backend-rollback-drill-readiness-approval-release-record.svg)
- [Go backend rollback drill closure packet and auditor export SVG](docs/diagrams/go-backend-rollback-drill-closure-packet-auditor-export.svg)
- [Go backend rollback drill auditor export routing and archive SVG](docs/diagrams/go-backend-rollback-drill-auditor-export-routing-archive.svg)
- [Go backend rollback drill auditor export retry and archive health SVG](docs/diagrams/go-backend-rollback-drill-auditor-export-retry-archive-health.svg)
- [Go backend rollback drill auditor retry worker and archive alert acknowledgements SVG](docs/diagrams/go-backend-rollback-drill-auditor-export-retry-worker-archive-alert-acks.svg)
- [Go backend rollback drill final closeout delivery and retention SVG](docs/diagrams/go-backend-rollback-drill-final-closeout-delivery-retention.svg)
- [Go backend rollback drill final closeout health and retry SVG](docs/diagrams/go-backend-rollback-drill-final-closeout-health-retry.svg)
- [Release governance final closeout operator guide SVG](docs/diagrams/release-governance-final-closeout-operator-guide.svg)
- [Final closeout trial onboarding SVG](docs/diagrams/final-closeout-trial-onboarding.svg)
- [Final closeout production pilot intake SVG](docs/diagrams/final-closeout-production-pilot-intake.svg)

Brand assets:

- [CAVRA brand assets](assets/brand/README.md)
- [CAVRA mark SVG](assets/brand/cavra-mark.svg)
- [CAVRA horizontal logo SVG](assets/brand/cavra-logo-horizontal.svg)
- [CAVRA GitHub social preview PNG](assets/brand/png/cavra-github-social-preview-1200x630.png)

## Quick start

```bash
pipx install cavra
cavra version
cavra policy list
cavra policy test
cavra evaluate read_file .env --json
```

Community Docker:

```bash
docker compose -f docker/docker-compose.community.yml up --build
```

Trial access:

- Trial source code is not public.
- Enterprise Trial package `2026.06.05` is ready for approved private evaluators.
- The public portal now includes a self-service Enterprise Trial request page for approved access workflows.
- Trial artifacts are distributed through private Docker images, binaries, or hosted SaaS access.
- The current private distribution target is gated GHCR image `ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05`.
- Public-safe image digest: `sha256:2d5f0d338a5528205f11674917d1526db7aa9732ef2af6ca3bd957b6230b4b47`.
- Trial release approval requires private license-service readiness, source exclusion, customer-data exclusion, private registry push/pull validation, signed license validation, revoked-license failure validation, and runtime license enforcement.
- Approved trial package releases are followed by private license issuance and evaluator access evidence; public docs record references only.
- Private expiry evidence records whether evaluator access was revoked, renewed, or escalated at the end of the approved trial window.
- Private expired-trial follow-up evidence records notification, grace-period, and commercial handoff references after expiry.
- Private conversion readiness evidence records paid-pilot or production conversion gates for renewed or escalated trials.
- Private conversion activation and production handoff evidence records paid-pilot activation or production handoff gates for approved conversions.
- Private conversion closeout and revenue handoff evidence records customer-success, support, release-management, finance, revenue, billing, subscription/order, renewal forecast, and revenue-recognition gates for activated conversions.
- Private conversion executive summary and renewal action evidence records leadership, account-team, customer-success, risk-owner, renewal-owner, expansion, commercial follow-up, and action due-date gates for closed-out conversions.
- Trial license validation is implemented by the private Enterprise license service and exposed to evaluators only through approved trial access.
- See [docs/enterprise/trial.md](docs/enterprise/trial.md).
- See [docs/enterprise/trial-availability.md](docs/enterprise/trial-availability.md).
- See [docs/enterprise/trial-self-service-access.md](docs/enterprise/trial-self-service-access.md).
- See [docs/trial-enterprise-distribution-sync.md](docs/trial-enterprise-distribution-sync.md).
- See [docs/trial-license-evaluator-access-sync.md](docs/trial-license-evaluator-access-sync.md).
- See [docs/trial-access-expiry-sync.md](docs/trial-access-expiry-sync.md).
- See [docs/trial-expired-followup-sync.md](docs/trial-expired-followup-sync.md).
- See [docs/trial-conversion-readiness-sync.md](docs/trial-conversion-readiness-sync.md).
- See [docs/trial-conversion-activation-handoff-sync.md](docs/trial-conversion-activation-handoff-sync.md).
- See [docs/trial-conversion-closeout-revenue-sync.md](docs/trial-conversion-closeout-revenue-sync.md).
- See [docs/trial-conversion-executive-renewal-sync.md](docs/trial-conversion-executive-renewal-sync.md).

## Claude Code quickstart

```bash
claude mcp add cavra -- cavra-mcp-server
```

Initialize a repository for Claude Code governance:

```bash
cavra init claude-code
```

CAVRA for Claude Code gives Claude Code a runtime authority layer. It evaluates sensitive agent actions before they reach files, shell commands, Git operations, MCP tools, Terraform, Kubernetes, or cloud control planes.

## CLI usage

```bash
cavra agent start --tool claude-code
cavra evaluate execute_command "terraform apply -auto-approve"
cavra policy validate policies/cavra-ai-agent-baseline
cavra policy explain execute_command "terraform plan"
cavra demo before-the-agent-acts
```

## API usage

```bash
uvicorn cavra.api:app --reload
curl http://127.0.0.1:8000/health
```

The API is published as `CAVRA API` and exposes policies, decisions, sessions, agents, approvals, evidence, integrations, MCP trust, risk events, compliance mappings, and sandbox endpoints.

Set `CAVRA_EVIDENCE_ARTIFACT_ROOT` to expose read-only evidence artifact retrieval for indexed sessions, managed endpoint rollout records, and endpoint-management export records. Session and rollout artifacts are available through `/evidence/{session_id}/artifacts`, `/evidence/{session_id}/artifacts/{artifact_name}`, and `/evidence/{session_id}/artifact-bundle`. Endpoint export artifacts are available through `/endpoint-management-exports/{export_id}/artifacts`, `/endpoint-management-exports/{export_id}/artifacts/{artifact_name}`, and `/endpoint-management-exports/{export_id}/artifact-bundle`. The API only serves allowlisted files under the configured root, verifies endpoint export checksums before download, and requires matching evidence metadata.

Set `CAVRA_APPROVAL_OIDC_CONFIG` and `CAVRA_APPROVAL_RBAC_FILE` to enable authenticated console sessions through `/console/session`. Approval decisions and break-glass console mutations then require verified actor context from a bearer token, `actor_token`, or `actor_claims`.

OIDC/RBAC deployment references for Microsoft Entra ID and Okta are documented in [docs/oidc-rbac-deployment.md](docs/oidc-rbac-deployment.md). Reference bundles live under `examples/identity/`.

Policy authoring and rollout workflows are exposed through `/policy-pack-catalog`, `/policy-packs/draft`, `/policy-rollouts/change-plan`, and `/policy-rollouts/apply-change`. Production deployment validation is exposed through `/deployment/production-readiness`.

The Go enforcement-plane scaffold lives under `go/cavra-runtime/` and currently mirrors critical Python runtime decisions for file, command, Git, approval-required writes, evidence references, policy-backed MCP, registry-backed MCP actions, release governance records, high-risk cloud/IaC command controls, and representative cases across every bundled compiled policy pack. It can load normalized compiled policy JSON from `cavra policy compile` through the Go CLI `--policy` flag and trust-registry JSON through `--registry`. Release governance record parity now has Python and Go expectations for approval states, delivery failures, endpoint publication delivery, inventory freshness, reconciliation drift, SLA reports, handoff status, rollout evidence verification, rollout artifact integrity, promotion audit export contract fixtures, and rollback audit export contract fixtures. Generated Go enforcement contracts live under `go/cavra-runtime/enforcement/v1` and are generated from `proto/cavra/enforcement/v1/enforcement.proto`; they now include typed public-safe `ReleaseGovernanceEvidence`, `RunnerAuthentication`, and `RunnerIdentity` payloads. The Go runtime now includes an initial Unix-socket daemon mode with `--serve`, a reusable `daemon.Client`, CLI `--daemon` one-shot client mode, daemon lifecycle `start/status/stop`, daemon evidence hooks, HMAC-signed runner authentication claims, CI-provider OIDC JWT runner verification, hash-chained HMAC-signed daemon evidence records, daemon evidence verifier CLI support, typed release-governance daemon and CI runner examples, signed CI runner bundle metadata, a reusable runner wrapper, a GitHub composite action, and a release packaging workflow for checksums, SPDX SBOM metadata, reproducibility manifests, release signing operations metadata, SLSA provenance, detached Ed25519 signatures, GitHub keyless OIDC attestations, offline trust bootstrap metadata, air-gapped zip verification, and release evidence. The opt-in Go backend path adds `CAVRA_GO_BACKEND_MODE=disabled|shadow|enforce|promoted`, CLI readiness, deployment, promotion, rollback, rollback rehearsal, rollback drill history, rollback drill schedule, drill notification acknowledgement, drill escalation, drill owner routing, maintenance-window suppression, routing history filters, suppression trend summaries, authenticated console acknowledgement controls, bulk acknowledgement workflows, acknowledgement audit packages, acknowledgement audit delivery routing, acknowledgement audit delivery health dashboards, acknowledgement audit delivery retry plans, scheduled audit delivery worker runs, worker health alerts, retry acknowledgements, retry execution approvals, connector recovery playbooks, approval-bound live retry execution records, connector recovery closure evidence, recovery escalation retry health, recovery retry health alert delivery, retry planning, retry worker execution, executive delivery retry planning, executive delivery retry worker execution, executive retry health reporting, executive retry health alert delivery and acknowledgements, executive health alert retry planning, executive health alert retry worker execution, final reporting closure dashboards, release-readiness summaries, operator runbook exports, readiness approval decisions, release record attachments, closure packet verifications, auditor exports, auditor export delivery routing, immutable archive references, auditor export retry planning, auditor export retry worker execution records, archive reference health checks, archive health alert delivery acknowledgements, and evaluation commands, FastAPI endpoints, production-readiness evidence, and an audited Python fallback when Go is unavailable or diverges. Deployment readiness validates CI runner bundle metadata, workstation channel manifests, and updater policy. Promotion readiness requires runtime readiness, deployment readiness, approved audited parity evidence, and `CAVRA_GO_PROMOTION_EVIDENCE`; rollback readiness requires `CAVRA_GO_ROLLBACK_PLAN`, approved rollback controls, and `target_mode=disabled`; rollback rehearsal requires `CAVRA_GO_ROLLBACK_REHEARSAL_EVIDENCE`, verified Python fallback restoration, and recovery-time evidence; rollback drill history requires `CAVRA_GO_ROLLBACK_DRILL_HISTORY` with a fresh passing drill; rollback drill scheduling requires `CAVRA_GO_ROLLBACK_DRILL_SCHEDULE`, active cadence metadata, owners, and notification routes before `promoted` mode selects Go as an optional backend. High-risk parity is documented in [docs/high-risk-command-cloud-iac-parity.md](docs/high-risk-command-cloud-iac-parity.md), air-gapped reproducible build guidance is documented in [docs/go-reproducible-airgap-builds.md](docs/go-reproducible-airgap-builds.md), signing operations guidance is documented in [docs/release-signing-operations.md](docs/release-signing-operations.md), the opt-in pilot is documented in [docs/go-backend-pilot.md](docs/go-backend-pilot.md), deployment readiness is documented in [docs/go-backend-deployment-readiness.md](docs/go-backend-deployment-readiness.md), promotion readiness is documented in [docs/go-backend-promotion.md](docs/go-backend-promotion.md), rollback controls are documented in [docs/go-backend-rollback.md](docs/go-backend-rollback.md), rollback rehearsal evidence is documented in [docs/go-backend-rollback-rehearsal.md](docs/go-backend-rollback-rehearsal.md), rollback drill history is documented in [docs/go-backend-rollback-drill-history.md](docs/go-backend-rollback-drill-history.md), rollback drill scheduling is documented in [docs/go-backend-rollback-drill-scheduling.md](docs/go-backend-rollback-drill-scheduling.md), rollback drill notification escalation is documented in [docs/go-backend-rollback-drill-notification-escalation.md](docs/go-backend-rollback-drill-notification-escalation.md), rollback drill routing is documented in [docs/go-backend-rollback-drill-routing.md](docs/go-backend-rollback-drill-routing.md), rollback drill routing history is documented in [docs/go-backend-rollback-drill-routing-history.md](docs/go-backend-rollback-drill-routing-history.md), acknowledgement controls are documented in [docs/go-backend-rollback-drill-acknowledgement-controls.md](docs/go-backend-rollback-drill-acknowledgement-controls.md), bulk acknowledgement audits are documented in [docs/go-backend-rollback-drill-bulk-acknowledgement-audit.md](docs/go-backend-rollback-drill-bulk-acknowledgement-audit.md), acknowledgement audit delivery is documented in [docs/go-backend-rollback-drill-acknowledgement-audit-delivery.md](docs/go-backend-rollback-drill-acknowledgement-audit-delivery.md), acknowledgement audit delivery health is documented in [docs/go-backend-rollback-drill-audit-delivery-health.md](docs/go-backend-rollback-drill-audit-delivery-health.md), acknowledgement audit delivery retry workers are documented in [docs/go-backend-rollback-drill-audit-delivery-retry-worker.md](docs/go-backend-rollback-drill-audit-delivery-retry-worker.md), worker health alerts are documented in [docs/go-backend-rollback-drill-audit-worker-health-alerts.md](docs/go-backend-rollback-drill-audit-worker-health-alerts.md), retry approvals and recovery playbooks are documented in [docs/go-backend-rollback-drill-retry-approvals-recovery-playbooks.md](docs/go-backend-rollback-drill-retry-approvals-recovery-playbooks.md), live retry closure evidence is documented in [docs/go-backend-rollback-drill-live-retry-closure-evidence.md](docs/go-backend-rollback-drill-live-retry-closure-evidence.md), recovery retry health is documented in [docs/go-backend-rollback-drill-recovery-retry-health-and-executive-delivery-retry.md](docs/go-backend-rollback-drill-recovery-retry-health-and-executive-delivery-retry.md), executive retry execution is documented in [docs/go-backend-rollback-drill-executive-delivery-retry-execution-and-recovery-health-alerts.md](docs/go-backend-rollback-drill-executive-delivery-retry-execution-and-recovery-health-alerts.md), executive retry health is documented in [docs/go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.md](docs/go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.md), recovery health alert retry workers are documented in [docs/go-backend-rollback-drill-recovery-health-alert-retry-worker-and-executive-retry-health-alerts.md](docs/go-backend-rollback-drill-recovery-health-alert-retry-worker-and-executive-retry-health-alerts.md), final closure is documented in [docs/go-backend-rollback-drill-executive-health-alert-retry-and-final-closure.md](docs/go-backend-rollback-drill-executive-health-alert-retry-and-final-closure.md), final readiness runbook export is documented in [docs/go-backend-rollback-drill-final-readiness-runbook-export.md](docs/go-backend-rollback-drill-final-readiness-runbook-export.md), readiness approval release records are documented in [docs/go-backend-rollback-drill-readiness-approval-release-record.md](docs/go-backend-rollback-drill-readiness-approval-release-record.md), and closure packet auditor exports are documented in [docs/go-backend-rollback-drill-closure-packet-auditor-export.md](docs/go-backend-rollback-drill-closure-packet-auditor-export.md), auditor export routing is documented in [docs/go-backend-rollback-drill-auditor-export-routing-archive.md](docs/go-backend-rollback-drill-auditor-export-routing-archive.md), and auditor export retry and archive health are documented in [docs/go-backend-rollback-drill-auditor-export-retry-archive-health.md](docs/go-backend-rollback-drill-auditor-export-retry-archive-health.md). The hosted sandbox deployment workflow lives at `.github/workflows/deploy-sandbox.yml` and publishes the static evidence console from `main` through GitHub Pages after JavaScript validation.

## Policy packs

Policy packs live under `policies/`. Current packs cover AI-agent baseline, banking, PCI DSS, HIPAA, SOX change control, NIST SSDF, ISO 27001, EU AI Act, OWASP LLM/agentic risks, MCP enterprise governance, Kubernetes production safety, Terraform/OpenTofu production safety, cloud IAM, GitHub Enterprise, and GitLab Enterprise.

Policy engine hardening is documented in [docs/policy-engine-hardening.md](docs/policy-engine-hardening.md). CAVRA now supports JSON Schema validation, inherited policy packs, normalized policy compilation, semantic policy diffs, Ed25519 policy signing, backward-compatible HMAC signature metadata, golden decision snapshots, and explicit runtime policy modes.

```bash
cavra policy validate policies/cavra-ai-agent-baseline
cavra policy compile --policy-pack cavra-ai-agent-baseline
cavra policy diff policies/cavra-ai-agent-baseline policies/cavra-banking-baseline
cavra policy keygen --output .cavra/policy-signing --key-id community-ga-policy-key
cavra policy sign policies/cavra-ai-agent-baseline/policy.yaml --signer platform-security --private-key .cavra/policy-signing/community-ga-policy-key.private.pem --key-id community-ga-policy-key
cavra policy verify policies/cavra-ai-agent-baseline/policy.yaml --public-key .cavra/policy-signing/community-ga-policy-key.public.pem
cavra evaluate execute_command "terraform plan" --policy-mode strict --json
```

## Evidence and attestation

CAVRA emits decision JSON, session audit files, PR attestation markdown, compliance mapping reports, sandbox evidence bundles, and persistent API operational metadata. Evidence includes agent identity, user or actor, repo, branch, action attempted, decision, policy version, rule ID, rationale, approval state, timestamp, evidence refs, and correlation ID.

Evidence Hub and Attestation is documented in [docs/evidence-hub-attestation.md](docs/evidence-hub-attestation.md). CAVRA now generates evidence bundles with manifests, checksums, HMAC or Ed25519 manifest signatures, PR attestation, compliance mapping, SIEM event output, provider-specific SIEM payloads, retention policies, immutable storage reference plans, metadata indexing, governed artifact retrieval APIs for sessions and endpoint rollout records, verifier commands, and required-check CI/CD templates.

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
cavra evidence verify .cavra/evidence/latest
cavra evidence siem-event .cavra/evidence/latest
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence retention-policy .cavra/evidence/latest --output .cavra/evidence/retention
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
cavra evidence trust-root .cavra/keys/evidence-public.pem --output .cavra/keys/evidence-trust-root.json --key-id prod-evidence
cavra evidence trust-bundle .cavra/keys/evidence-trust-root.json --output .cavra/keys/evidence-trust-roots.json
cavra evidence trust-distribution .cavra/keys/evidence-trust-root.json --output .cavra/keys/trust-root-distribution --distribution-id prod-trust-roots-2026-q2
cavra evidence verify-attestation .cavra/evidence/latest --output .cavra/evidence/attestation
cavra evidence migrate --sqlite .cavra/evidence/metadata.db
cavra evidence index .cavra/evidence/latest --sqlite .cavra/evidence/metadata.db
cavra evidence search --sqlite .cavra/evidence/metadata.db --min-blocked 1 --limit 25
cavra evidence search --sqlite .cavra/evidence/metadata.db --metadata-kind managed-endpoint-rollout --rollout-status staged --deployment-target github-actions-linux-amd64-runner
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-v0.1.0
cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-v0.1.0.zip
cavra release validate-upgrade go/cavra-runtime/dist/go-runtime-v0.1.0 go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1
cavra release smoke-installers go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1
cavra release channel-manifest go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 --channel stable
cavra release updater-policy go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1
cavra release request-channel-promotion go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 --channel stable --approval-store .cavra/api/approvals.json --metadata-json .cavra/evidence/metadata.json
cavra release export-endpoint-management go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 --channel stable --provider all --promotion-request .cavra/release/channel-promotion/release-channel-promotion-request.json --metadata-json .cavra/evidence/metadata.json
cavra release deliver-endpoint-export .cavra/release/endpoint-management-export/endpoint-management-export-manifest.json --config .cavra/connectors.json --provider jamf --metadata-json .cavra/evidence/metadata.json
cavra release ingest-endpoint-inventory .cavra/release/jamf-inventory.json --provider jamf --channel stable --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-inventory-history --metadata-json .cavra/evidence/metadata.json --provider jamf
cavra release endpoint-inventory-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-inventory-freshness --metadata-json .cavra/evidence/metadata.json --max-age-hours 24 --critical-age-hours 48
cavra release endpoint-inventory-freshness-history --metadata-json .cavra/evidence/metadata.json --alert-level critical
cavra release endpoint-inventory-freshness-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release reconcile-endpoint-deployment go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 .cavra/release/observed-endpoints.json --metadata-json .cavra/evidence/metadata.json
cavra release automate-endpoint-reconciliation go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 .cavra/release/endpoint-inventory/endpoint-inventory-ingestion.json --approval-store .cavra/api/approvals.json --metadata-json .cavra/evidence/metadata.json
cavra release capture-rollout go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 --deployment-id github-actions-linux-amd64-runner --change-record CHG-123
cavra release verify-rollout .cavra/release/rollout --metadata-json .cavra/evidence/metadata.json --sqlite .cavra/evidence/metadata.db
cavra release request-rollout-promotion .cavra/release/rollout --target-ring production --approval-store .cavra/api/approvals.json
cavra release execute-rollout-promotion .cavra/release/rollout-promotion/rollout-promotion-approval-request.json --approval-store .cavra/api/approvals.json --metadata-json .cavra/evidence/metadata.json
cavra release export-promotion-audit .cavra/release/rollout-promotion-execution/rollout-promotion-execution.json --provider all
cavra release execute-rollout-rollback .cavra/release/rollout-promotion-execution/rollout-promotion-execution.json --approval-store .cavra/api/approvals.json --approval-id apr_rollback_prod --metadata-json .cavra/evidence/metadata.json
cavra release deliver-promotion-audit .cavra/release/rollout-promotion-execution/rollout-promotion-execution.json --config .cavra/connectors.json --provider webhook --retries 1 --metadata-json .cavra/evidence/metadata.json
cavra release deliver-rollback-execution .cavra/release/rollout-rollback-execution/rollout-rollback-execution.json --config .cavra/connectors.json --provider webhook --retries 1 --metadata-json .cavra/evidence/metadata.json
cavra release connector-delivery-history --metadata-json .cavra/evidence/metadata.json --provider webhook --no-success
cavra release connector-delivery-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-publication-history --metadata-json .cavra/evidence/metadata.json --provider jamf --no-success
cavra release endpoint-publication-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-reconciliation-history --metadata-json .cavra/evidence/metadata.json --drift-status drift_detected
cavra release endpoint-reconciliation-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-reconciliation-automation-history --metadata-json .cavra/evidence/metadata.json --approval-state pending
cavra release endpoint-reconciliation-automation-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release request-endpoint-remediation .cavra/release/endpoint-reconciliation/managed-endpoint-reconciliation.json --approval-store .cavra/api/approvals.json --metadata-json .cavra/evidence/metadata.json
cavra release execute-endpoint-remediation .cavra/release/endpoint-remediation/endpoint-remediation-request.json --approval-store .cavra/api/approvals.json --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-history --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release export-endpoint-remediation-handoff .cavra/release/endpoint-remediation/endpoint-remediation-request.json --provider all --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-handoff-history --metadata-json .cavra/evidence/metadata.json --provider private_queue
cavra release endpoint-remediation-handoff-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release record-endpoint-remediation-handoff-status .cavra/release/endpoint-remediation-handoff/endpoint-remediation-handoff.json --provider private_queue --status completed --external-ref queue-job-123 --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-handoff-status-history --metadata-json .cavra/evidence/metadata.json --provider private_queue
cavra release endpoint-remediation-handoff-status-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-report --metadata-json .cavra/evidence/metadata.json --index-metadata-json .cavra/evidence/metadata.json --warning-hours 24 --critical-hours 48
cavra release deliver-endpoint-remediation-sla .cavra/release/endpoint-remediation-sla/endpoint-remediation-sla-report.json --config .cavra/connectors.json --routing-policy .cavra/sla-notification-policy.json --provider all --metadata-json .cavra/evidence/metadata.json
cavra release ack-endpoint-remediation-sla ersla_123 --provider slack --acknowledged-by release-manager --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-notification-history --metadata-json .cavra/evidence/metadata.json --provider slack
cavra release endpoint-remediation-sla-notification-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-plan --slo-policy .cavra/sla-escalation-policy.json --metadata-json .cavra/evidence/metadata.json
cavra release deliver-endpoint-remediation-sla-escalation .cavra/release/endpoint-remediation-sla-escalation-plan.json --config .cavra/connectors.json --provider all --metadata-json .cavra/evidence/metadata.json
cavra release review-endpoint-remediation-sla-escalation erslaesc_123 --report-id ersla_123 --provider slack --owner release-governance --reviewed-by release-manager --review-state escalated --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-action-history --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-action-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-recurrence-plan --recurrence-policy .cavra/sla-escalation-recurrence-policy.json --metadata-json .cavra/evidence/metadata.json
cavra release deliver-endpoint-remediation-sla-escalation-recurrence .cavra/release/endpoint-remediation-sla-escalation-recurrence-plan.json --config .cavra/connectors.json --provider all --metadata-json .cavra/evidence/metadata.json
cavra release export-endpoint-remediation-sla-escalation-suppression-audit .cavra/release/endpoint-remediation-sla-escalation-recurrence-plan.json --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-recurrence-retry-plan --metadata-json .cavra/evidence/metadata.json
cavra release deliver-endpoint-remediation-sla-escalation-owner-digest .cavra/release/endpoint-remediation-sla-escalation-recurrence-plan.json --retry-plan .cavra/release/endpoint-remediation-sla-escalation-recurrence-retry-plan.json --config .cavra/connectors.json --provider all --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-suppression-trends --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-recurrence-automation --metadata-json .cavra/evidence/metadata.json --dry-run --json
cavra release endpoint-remediation-sla-escalation-recurrence-automation-history --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-recurrence-automation-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-recurrence-automation-health --metadata-json .cavra/evidence/metadata.json
cavra release deliver-endpoint-remediation-sla-escalation-recurrence-automation-health-alert --config .cavra/connectors.json --provider all --metadata-json .cavra/evidence/metadata.json
cavra release ack-endpoint-remediation-sla-escalation-recurrence-automation-health-alert erslah_123 --provider slack --acknowledged-by release-manager --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-recurrence-automation-health-alert-history --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-recurrence-automation-health-alert-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-recurrence-history --metadata-json .cavra/evidence/metadata.json --action suppress
cavra release endpoint-remediation-sla-escalation-recurrence-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-escalation-history --metadata-json .cavra/evidence/metadata.json --active-only
cavra release endpoint-remediation-sla-escalation-dashboard --metadata-json .cavra/evidence/metadata.json
cavra release endpoint-remediation-sla-history --metadata-json .cavra/evidence/metadata.json --alert-level critical
cavra release endpoint-remediation-sla-dashboard --metadata-json .cavra/evidence/metadata.json
jq '.deployment_targets[] | {id, surface, platform, installer_target}' go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1/cavra-runtime.endpoint-deployment.json
jq '.channels[] | {channel, version, auto_update, approval_required}' go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1/cavra-runtime.channels.json
```

Scheduled recurrence automation deployment templates are available for GitHub Actions, Kubernetes CronJob, and systemd timer deployments. See [docs/recurrence-automation-deployment.md](docs/recurrence-automation-deployment.md).

Immutable evidence storage deployment references are documented in [docs/immutable-evidence-storage.md](docs/immutable-evidence-storage.md). Reference bundles are available for AWS S3 Object Lock and Azure Blob immutability under `examples/immutable-storage/`.

Evidence key management and rotation guidance is documented in [docs/evidence-key-management.md](docs/evidence-key-management.md). Runner authentication, CI-provider OIDC token acquisition, daemon evidence signing, and release-governance verifier retention are documented in [docs/runner-auth-evidence-key-custody.md](docs/runner-auth-evidence-key-custody.md).

## Persistent API operations

CAVRA can inspect, back up, restore, and document retention controls for the API's JSON and SQLite stores:

```bash
cavra ops stores
cavra ops backup --output .cavra/backups/20260518
cavra ops restore .cavra/backups/20260518/manifest.json --target-dir /tmp/cavra-restore-test
cavra ops retention-plan --output .cavra/operations/retention --retention-days 2555 --legal-hold
```

Persistent API operations are documented in [docs/persistent-api-operations.md](docs/persistent-api-operations.md). The API exposes read-only `/operations/stores` and `/operations/retention-plan` endpoints; restore remains CLI-only.

## Human approvals

Risky actions can return `require_approval` with approver groups such as Platform Security, Cloud Security, IAM, AppSec, Change Advisory Board, AI Governance, Data Protection, PCI Compliance, Healthcare Compliance, or Repository Owners.

Phase 4 Approval Router is now in progress. CAVRA can create a persisted approval request from a decision, route it with default or repository-specific rules, enforce optional claims-based approval authorization, list pending approvals, approve, deny, expire, record break-glass overrides with mandatory reasons, and attach approval outcomes back to evidence:

```bash
cavra evaluate write_file iam/admin-role.tf --json > /tmp/cavra-decision.json
cavra approval migrate --sqlite .cavra/approvals.db
cavra approval create /tmp/cavra-decision.json --requested-by developer
cavra approval create /tmp/cavra-decision.json --sqlite .cavra/approvals.db --requested-by developer
cavra approval route /tmp/cavra-decision.json
cavra approval route /tmp/cavra-decision.json --routing-file .cavra/approval-routing.json
cavra approval list --state pending
cavra approval approve apr_123 --actor platform-security --reason "Scoped IAM change reviewed" --external-ref CHG-123
cavra approval approve apr_123 --actor iam@example.com --actor-claims /tmp/oidc-claims.json --reason "Scoped IAM change reviewed"
cavra approval approve apr_123 --actor iam@example.com --actor-token /tmp/oidc.jwt --oidc-config .cavra/approval-oidc.json --rbac-file .cavra/approval-rbac.yaml --reason "Signed identity verified"
cavra approval break-glass /tmp/cavra-decision.json --actor incident-commander --reason "Production recovery" --external-ref INC-777
cavra approval export-notifications apr_123 --output .cavra/approvals/notifications
cavra approval provider-requests apr_123 --output .cavra/approvals/provider-requests
cavra approval deliver apr_123 --config .cavra/approval-providers.yaml --provider jira --output .cavra/approvals/deliveries
```

Approval workflows are documented in [docs/approval-workflows.md](docs/approval-workflows.md).

## MCP governance

Run the MCP server:

```bash
cavra-mcp-server --list-tools
```

The server exposes CAVRA tools for evaluating actions, checking files, commands, Git operations, MCP calls, generating PR attestations, exporting evidence, and managing sessions.

## Git and PR governance

CAVRA blocks direct push to protected branches, can require PR attestation, records AI-agent metadata, and creates reviewer-ready evidence for risky diffs.

## Transparent CAVRA engineering agents

CAVRA uses a transparent AI engineering-team methodology for its own repository and for customer reference architecture. Specialized bots such as `cavra-backend[bot]`, `cavra-security[bot]`, `cavra-docs[bot]`, and `cavra-release[bot]` are declared as automation, not fake human contributors.

Agent manifests live under [.github/agents](.github/agents). They define each role's identity, allowed triggers, allowed paths, approval gates, prohibited actions, and required evidence. The [Transparent Agent Methodology](docs/transparent-agent-methodology.md) and [Agent Orchestration Architecture](docs/agent-orchestration-architecture.md) explain the operating model.

Anti-bypass enforcement is documented in [docs/ai-agent-enforcement.md](docs/ai-agent-enforcement.md). The production model does not rely on agent cooperation alone: protected branches, required `cavra-required-check`, PR attestation, governed CI runners, signed release evidence, and deployment gates must reject work that did not pass through CAVRA. Use `cavra agent enforcement-readiness --json` or `GET /agents/enforcement-readiness` to report whether a repository has the local files and exported platform controls needed to make that claim credible.

The policy pack [policies/cavra-agentic-delivery](policies/cavra-agentic-delivery/policy.yaml) governs agent-driven delivery with protected branch requirements, bot identity requirements, PR attestation, documentation freshness, and human approval for protected actions.

## Infrastructure, Kubernetes, and cloud CLI governance

CAVRA allows read-only planning workflows while blocking or routing autonomous production-impacting operations such as destructive Kubernetes commands, cloud IAM expansion, and direct protected-branch pushes.

## Enterprise integrations

The repository includes reference paths for GitHub, GitLab, Azure DevOps, pre-commit, Docker, Kubernetes, Microsoft Sentinel, Splunk, Datadog, ServiceNow, Jira, Slack, Microsoft Teams, immutable evidence stores, Entra ID, Okta, SAML, and RBAC. CAVRA now persists integration inventory records through JSON or SQLite and can execute configured SIEM, ITSM, ChatOps, and webhook connector hooks with redacted delivery evidence. See [docs/connector-execution-hooks.md](docs/connector-execution-hooks.md).

## Compliance packs

CAVRA maps runtime controls to banking change control, PCI DSS, HIPAA, SOX, NIST SSDF, ISO 27001, EU AI Act, and OWASP LLM/agentic risks.

## Interactive sandbox

The `Before the Agent Acts` sandbox now includes the first hosted console slice: simulated and backend-driven agent decisions, telemetry-free public run counters from persisted backend metadata, release-note links for design-partner demos, activity browsing, repository inventory, policy rollout drill-downs, policy authoring, approval-bound signed policy publishing, rollout change workflows, enterprise integration inventory, SaaS operating automation contract inspection, SaaS worker handoff inspection, evidence metadata search, evidence artifact downloads, PR attestation verification, console security boundary status, console session validation, production readiness validation, and operational readiness status:

```bash
python -m http.server 5173 --directory apps/sandbox-ui
```

Open `http://127.0.0.1:5173`, run the agent scenario, review telemetry-free public demo counters, filter sessions and decisions, inspect repository policy rollout detail, preview policy drafts, request approval for signed policy write-back, publish approved policy packs, plan and apply rollout changes, review enterprise integration health, inspect OIDC/RBAC boundary status, validate console session context, inspect deployment readiness, filter evidence metadata, review downloadable evidence artifacts, verify PR attestation coverage, approve, deny, or expire pending approval requests, create break-glass overrides, and inspect approval audit history from the console queue.

For deployed topologies, configure `window.CAVRA_API_BASE` in the hosted page or set `CAVRA_PUBLIC_API_BASE_URL` and `CAVRA_CORS_ORIGINS` on the API. The console reads `/console/config`, `/api/sandbox/metrics`, `/aispm/posture`, `/aispm/trace-replay/{session_id}`, `/aispm/approval-lineage`, `/saas/control-plane/contract`, `/saas/operating-automation`, and `/saas/operating-automation/worker-handoff` when available and falls back to bundled sample evidence, AISPM sample posture, and public-safe contract previews when the API is unreachable. The AISPM view includes posture overview, agent coverage, risk findings, observed control coverage, near-miss queue, execution timeline, approval lineage, and public-safe trace replay packets from CAVRA activity metadata only; no cookies, browser identifiers, or third-party analytics are required. See [docs/sandbox.md](docs/sandbox.md).

The GitHub Pages sandbox is live at `https://huzefaaa2.github.io/cavra/`. GitHub Pages is enabled for Actions publishing, and the deployment workflow now packages downloadable sample evidence and smoke-tests the public page, JavaScript, stylesheet, brand assets, C4 diagram, and evidence JSON.

## Demo scenarios

The flagship demo is in `examples/demos/before-the-agent-acts/` and proves CAVRA can block `.env` reads, allow `terraform plan`, block `terraform apply -auto-approve`, require approval for IAM changes, block unknown MCP filesystem servers, block push to `main`, and generate PR attestation.

The final closeout trial demo is in `examples/demos/final-closeout-trial/` and provides a synthetic evidence package plus pilot intake template for customer onboarding. The public Evidence Console now renders the pilot intake template as production pilot readiness cards, a readiness checklist, Enterprise/SaaS handoff links, and a backend save action when the CAVRA API is configured. Use it with [docs/enterprise/final-closeout-trial-walkthrough.md](docs/enterprise/final-closeout-trial-walkthrough.md), [docs/enterprise/final-closeout-trial-sample-evidence.md](docs/enterprise/final-closeout-trial-sample-evidence.md), [docs/enterprise/final-closeout-sales-engineering-demo.md](docs/enterprise/final-closeout-sales-engineering-demo.md), [docs/enterprise/final-closeout-production-pilot-intake.md](docs/enterprise/final-closeout-production-pilot-intake.md), and [docs/enterprise/final-closeout-pilot-intake-api.md](docs/enterprise/final-closeout-pilot-intake-api.md).

## Roadmap

The production roadmap is priority-based, not calendar-based. See [docs/production-roadmap.md](docs/production-roadmap.md) and [docs/implementation-plan.md](docs/implementation-plan.md).

Current phase status:

- Phase 1: Productization Foundation - complete in PR #1.
- Phase 2: Policy Engine Hardening - complete in PR #1.
- Phase 3: Evidence Hub and Attestation - near complete in PR #1 with governed hosted artifact retrieval, trust-root distribution automation, and production deployment validation now available.
- Phase 4: Approval Router - complete for the current production-readiness slice in PR #1 with JSON/SQLite persistence, routing files, signed OIDC/JWKS validation, repository RBAC, provider request specs, live provider delivery, console actions, break-glass creation, and audit detail views.
- Phase 5: Agent Registry and MCP Trust Registry - complete for the current production-readiness slice in PR #1 with JSON/SQLite registry persistence, API and CLI access, predefined agent capability profiles, MCP tool classification, console registry views, and registry-backed MCP runtime decisions.
- Phase 6: Console and Persistent API - started in PR #1 with JSON/SQLite activity persistence for sessions and decisions, repository inventory and policy rollout persistence, policy-pack authoring workflows, approval-bound signed policy publishing, rollout change planning/apply workflows, integration inventory persistence, persistent API backup/restore/retention operations, production deployment validation, policy rollout drill-downs, evidence artifact retrieval, read-only OIDC/RBAC console security boundary reporting, authenticated console session validation, API filters, console Activity Explorer views, and console repository/rollout/integration views.
- Phase 7: Go Enforcement Plane - scaffold started in PR #1 with a Go module, runtime evaluator, CLI entrypoint, compiled-policy loader, generated Go enforcement contracts, typed release-governance evidence contract payloads, runner authentication contract payloads, daemon and CI runner examples, Unix-socket daemon transport, reusable Go daemon client helper, CLI `--daemon` mode, daemon lifecycle `start/status/stop`, daemon request/response evidence hooks, HMAC-signed runner authentication claims, hash-chained HMAC-signed daemon evidence streams, runtime evidence references, trust-registry JSON loading, registry-backed MCP parity, all-bundled-policy compiled parity, high-risk command and cloud/IaC parity for Cloud IAM, Kubernetes, Terraform/OpenTofu, GitHub, OWASP command-injection, and transparent delivery controls, Python/Go release governance parity for approvals, delivery failures, endpoint publication, inventory freshness, reconciliation drift, SLA reports, handoff status, rollout evidence verification, and rollout artifact integrity, signed release package workflow, SBOM generation, reproducibility manifests, release signing operations metadata, SLSA provenance, GitHub keyless OIDC attestations, offline trust bootstrap metadata, air-gapped zip verification, release-candidate upgrade validation, signed installer metadata, signed CI runner bundle metadata, reusable release-governance runner wrappers, a GitHub composite runner action, release channel manifests, managed workstation updater policy, release-channel promotion approvals, Jamf/Intune/Linux endpoint-management export bundles, release channel promotion and endpoint export metadata indexing, API and Evidence Console history views, governed endpoint export artifact downloads, checksum-enforced endpoint export integrity, endpoint export publication records, Jamf/Intune/Linux connector delivery, endpoint publication history dashboards, managed endpoint deployment reconciliation, endpoint drift monitoring dashboards, approval-bound endpoint drift remediation plans, approved remediation execution records, endpoint remediation handoff packages, endpoint remediation handoff status reconciliation, endpoint remediation SLA and executive reporting, endpoint remediation SLA notification delivery with routing policies, acknowledgements, duplicate suppression, escalation ladders, owner-specific SLOs, escalation delivery actions, owner review workflows, recurrence policies, owner calendars, maintenance-window suppression, recurrence delivery batching, suppression audit exports, retry policies for failed recurrence batches, owner digest notifications, suppression trend analytics, Evidence Console recurrence operations filters and export drill-downs, Evidence Console drill notification acknowledgement and escalation drill-downs, scheduled recurrence automation worker runs, Evidence Console recurrence automation worker history, recurrence automation deployment templates, recurrence automation health reporting, recurrence automation health alert delivery and acknowledgements, endpoint inventory freshness SLA reports, reconciliation automation from fresh inventory, installer smoke validation, managed endpoint deployment manifests, managed endpoint rollout evidence capture, rollout evidence verification and indexing, rollout evidence search filters and console/API views, governed rollout evidence artifact retrieval, rollout artifact integrity status, promotion readiness indicators, signed promotion approval requests, approved promotion execution records, promotion execution search and audit drill-downs, rollback evidence links, approved rollback execution records, SIEM/ITSM promotion audit exports, connector delivery for promotion audit and rollback execution records, persisted release connector delivery history, alerting dashboard summaries, release evidence, GitHub Release asset attachment, verifier CLI support, shared parity fixture, Python and Go tests, a dedicated `go-runtime-parity` CI job, Go execution in the required governance check, an explicitly opt-in Go backend path with shadow/enforce/promoted modes, readiness evidence, API/CLI access, production-readiness reporting, audited Python fallback, deployment readiness checks for CI runner and workstation rollout paths, a promotion gate requiring approved audited parity evidence before Go is selected as an optional backend, rollback controls requiring an approved path back to Python-only mode, rollback rehearsal evidence with dashboard visibility, fresh rollback drill history, recurring rollback drill scheduling, and stale-drill notification delivery before promoted mode selects Go.
- Phase 8: Enterprise Integrations - started in PR #1 with a GitHub required-check workflow, reusable GitHub Actions templates, GitLab CI and Azure Pipelines enforcement examples, CI evidence artifact upload, live SIEM/ITSM/ChatOps connector execution hooks, immutable storage references, OIDC/RBAC references, and Go parity execution in CI.
- Phase 9: Public Sandbox and Growth Loop - deployment workflow started in PR #1 with a GitHub Pages workflow for the static sandbox and evidence console, optional API configuration for backend-driven scenario runs, telemetry-free public run counters, and post-deploy smoke validation.
- Phase 10: Production Readiness and Release.

Latest delivery:

- The public Community repository now includes the user-verifiable Community GA
  path. It links policy gates, release packets, post-release verification,
  Evidence Console validation, Go runtime disabled/promoted status, README
  links, wiki navigation, and workflow enforcement through
  [docs/community-ga-user-verifiable-path.md](docs/community-ga-user-verifiable-path.md)
  and `scripts/validate-community-ga-path.py`.
- Production deployment guide validation now links install, configuration,
  storage, backup, restore, CORS/API, GitHub Pages portal checks, release
  validators, README navigation, and wiki navigation through
  [docs/production-deployment-guide-validation.md](docs/production-deployment-guide-validation.md)
  and `scripts/validate-production-deployment-guide.py`.
- Go enforcement production hardening now links Unix-socket transport,
  gRPC interface boundaries, air-gapped packaging, reproducibility, upgrade
  validation, performance smoke evidence, operational readiness, README
  navigation, and wiki navigation through
  [docs/go-enforcement-production-hardening.md](docs/go-enforcement-production-hardening.md)
  and `scripts/validate-go-production-hardening.py`.
- Enterprise integration validation now links GitHub App/orchestrator
  governance, GitLab and Azure DevOps parity, SAML identity readiness,
  SIEM/ITSM workflow evidence, README navigation, and wiki navigation through
  [docs/enterprise-integration-validation.md](docs/enterprise-integration-validation.md)
  and `scripts/validate-enterprise-integration-readiness.py`.
- Production readiness procurement closeout now links performance,
  concurrency, backup/restore, upgrade/migration, SOC 2 readiness, security
  advisory drills, final release integrity evidence, README navigation, and
  wiki navigation through
  [docs/production-readiness-procurement-closeout.md](docs/production-readiness-procurement-closeout.md)
  and `scripts/validate-production-readiness-procurement-closeout.py`.

Next recommended implementation work:

- Use Community v1.0.0 as the stable public baseline and begin the v1.0.1 maintenance planning path for post-GA fixes, release integrity hardening, detached signing or keyless attestation, and adoption feedback.

## User stories and enterprise value

CAVRA is built around enterprise user stories for developers, CISOs, platform engineers, DevSecOps, auditors, and AI governance leads. See [docs/user-stories.md](docs/user-stories.md).

CAVRA directly addresses secret exposure, unsafe infrastructure changes, direct Git push, dangerous shell commands, MCP tool sprawl, audit gaps, identity ambiguity, approval bypass, and regulated SDLC evidence gaps. See [docs/enterprise-challenges.md](docs/enterprise-challenges.md).

## Wiki and white paper

Wiki-ready documentation is maintained under [docs/wiki](docs/wiki):

- [Home](docs/wiki/Home.md)
- [White Paper](docs/wiki/White-Paper.md)
- [Production Roadmap](docs/wiki/Production-Roadmap.md)
- [Implementation Plan](docs/wiki/Implementation-Plan.md)
- [User Stories](docs/wiki/User-Stories.md)
- [Enterprise Challenges](docs/wiki/Enterprise-Challenges.md)
- [Diagrams](docs/wiki/Diagrams.md)
- [Phase Completion Log](docs/wiki/Phase-Completion-Log.md)
- [Approval Workflows](docs/wiki/Approval-Workflows.md)
- [Policy Engine Hardening](docs/wiki/Policy-Engine-Hardening.md)
- [Evidence Hub and Attestation](docs/wiki/Evidence-Hub-and-Attestation.md)
- [Evidence Key Management](docs/wiki/Evidence-Key-Management.md)
- [Evidence Trust-Root Distribution](docs/wiki/Evidence-Trust-Root-Distribution.md)
- [Immutable Evidence Storage](docs/wiki/Immutable-Evidence-Storage.md)
- [OIDC/RBAC Deployment](docs/wiki/OIDC-RBAC-Deployment.md)
- [GitHub Repository Readiness](docs/wiki/GitHub-Repository-Readiness.md)
- [GitHub Required Checks and CI/CD Enforcement](docs/wiki/GitHub-Required-Checks-and-CI-CD-Enforcement.md)
- [Release Documentation Policy](docs/wiki/Release-Documentation-Policy.md)
- [Transparent Agent Methodology](docs/wiki/Transparent-Agent-Methodology.md)
- [Agent Orchestration Architecture](docs/wiki/Agent-Orchestration-Architecture.md)
- [AI Agent Enforcement and Anti-Bypass Model](docs/wiki/AI-Agent-Enforcement-And-Anti-Bypass-Model.md)
- [Go Backend Rollback Drill Routing History](docs/wiki/Go-Backend-Rollback-Drill-Routing-History.md)
- [Go Backend Rollback Drill Console](docs/wiki/Go-Backend-Rollback-Drill-Console.md)
- [Go Backend Rollback Drill Acknowledgement Controls](docs/wiki/Go-Backend-Rollback-Drill-Acknowledgement-Controls.md)
- [Go Backend Rollback Drill Bulk Acknowledgement Audit](docs/wiki/Go-Backend-Rollback-Drill-Bulk-Acknowledgement-Audit.md)
- [Go Backend Rollback Drill Acknowledgement Audit Delivery](docs/wiki/Go-Backend-Rollback-Drill-Acknowledgement-Audit-Delivery.md)
- [Go Backend Rollback Drill Audit Delivery Health](docs/wiki/Go-Backend-Rollback-Drill-Audit-Delivery-Health.md)
- [Go Backend Rollback Drill Executive Delivery Retry Execution And Recovery Health Alerts](docs/wiki/Go-Backend-Rollback-Drill-Executive-Delivery-Retry-Execution-And-Recovery-Health-Alerts.md)
- [Go Backend Rollback Drill Executive Health Alert Retry And Final Closure](docs/wiki/Go-Backend-Rollback-Drill-Executive-Health-Alert-Retry-And-Final-Closure.md)
- [Go Backend Rollback Drill Final Readiness Runbook Export](docs/wiki/Go-Backend-Rollback-Drill-Final-Readiness-Runbook-Export.md)
- [Go Backend Rollback Drill Readiness Approval Release Record](docs/wiki/Go-Backend-Rollback-Drill-Readiness-Approval-Release-Record.md)
- [Go Backend Rollback Drill Closure Packet Auditor Export](docs/wiki/Go-Backend-Rollback-Drill-Closure-Packet-Auditor-Export.md)
- [Repository Inventory and Policy Rollout](docs/wiki/Repository-Policy-Rollout.md)
- [Persistent API Operations](docs/wiki/Persistent-API-Operations.md)
- [Integration Inventory](docs/wiki/Integration-Inventory.md)
- [Connector Execution Hooks](docs/wiki/Connector-Execution-Hooks.md)
- [Console Security Boundary](docs/wiki/Console-Security-Boundary.md)
- [Console Authenticated Sessions](docs/wiki/Console-Authenticated-Sessions.md)
- [Evidence Artifact Retrieval](docs/wiki/Evidence-Artifact-Retrieval.md)
- [Policy Pack Authoring Workflows](docs/wiki/Policy-Pack-Authoring-Workflows.md)
- [Production Deployment Validation](docs/wiki/Production-Deployment-Validation.md)
- [Go Enforcement Parity](docs/wiki/Go-Enforcement-Parity.md)
- [Go Enforcement Contracts](docs/wiki/Go-Enforcement-Contracts.md)
- [Go Daemon Transport](docs/wiki/Go-Daemon-Transport.md)
- [Go Backend Pilot](docs/wiki/Go-Backend-Pilot.md)
- [Go Backend Deployment Readiness](docs/wiki/Go-Backend-Deployment-Readiness.md)
- [Go Release Packaging](docs/wiki/Go-Release-Packaging.md)
- [Enterprise Integration Validation](docs/wiki/Enterprise-Integration-Validation.md)
- [Production Readiness Procurement Closeout](docs/wiki/Production-Readiness-Procurement-Closeout.md)
- [SaaS Operating Automation Public Contract Sync](docs/wiki/SaaS-Operating-Automation-Public-Contract-Sync.md)
- [SaaS Operating Automation Worker Handoff](docs/wiki/SaaS-Operating-Automation-Worker-Handoff.md)
- [Vulnerability Disclosure](docs/vulnerability-disclosure.md)
- [Release Security Advisories](docs/release-security-advisories.md)
- [Hosted Sandbox Deployment](docs/wiki/Hosted-Sandbox-Deployment.md)
- [Brand Assets](docs/wiki/Brand-Assets.md)

The wiki white paper explains why CAVRA exists, how pre-action enforcement works, the dual-plane architecture, regulated SDLC fit, Claude Code strategy, and the production roadmap.

## Contributing

Contributions should preserve CAVRA’s pre-action enforcement model, open evidence format, policy-as-code approach, and open-core boundaries. Do not submit Enterprise source code, private policy packs, license-server logic, customer material, or secrets to this public repository.

- [Contributing guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Code of conduct](CODE_OF_CONDUCT.md)
- [Boundary validation](scripts/validate-boundaries.sh)

## License

This repository is licensed under BUSL-1.1. See `LICENSE`.

The current BUSL parameters are:

- Licensor: Huzefa Husain.
- Additional Use Grant: None.
- Change Date: 2030-05-18.
- Change License: Apache License, Version 2.0.
