# Diagrams

## C4 Context

See `docs/diagrams/c4-context.md`.

## C4 Container

See `docs/diagrams/c4-container.md`. The current container diagram marks the Approval Router as an implemented JSON/SQLite-backed lifecycle service with repository routing, signed OIDC/JWKS validation, repository RBAC, Entra/Okta deployment references, console actions, console break-glass creation, approval audit details, provider request specs, and live provider delivery evidence. It also marks the Agent and MCP Trust Registry as a JSON/SQLite implementation for governed agent identities, MCP trust decisions, predefined agent profiles, MCP capability classifications, and console registry views. The metadata store now includes JSON/SQLite evidence, session, decision, approval, registry, repository inventory, policy rollout metadata, policy authoring previews, approval-bound signed policy publishing, rollout change plans, deployment readiness checks, integration inventory, connector delivery records, backup/restore operations, retention planning, and governed evidence artifact retrieval. The evidence plane now feeds CI/CD required-check artifacts for GitHub, GitLab, Azure DevOps templates, configured SIEM/ITSM/ChatOps/webhook connector hooks, and AWS/Azure immutable evidence storage references. The console security boundary and console session context are exposed as OIDC/RBAC/CORS readiness and authenticated actor metadata. The Go enforcement plane is now shown as a scaffolded parity-tested container with daemon transport and client mode, and the sandbox is shown as GitHub Pages deployable.

## Agent and MCP Registry

See `docs/diagrams/agent-mcp-registry.svg` for the dedicated registry view that separates profiles, registered identities, trust records, classifications, storage modes, runtime decisions, console views, and evidence consumers.

## Runtime Components

See `docs/diagrams/c4-component-runtime.md`.

## Runtime Decision Flow

See `docs/diagrams/runtime-decision-flow.md`.

## Evidence Lifecycle

See `docs/diagrams/evidence-lifecycle.md`.

## Immutable Evidence Storage

See `docs/diagrams/immutable-evidence-storage.svg` for the dedicated immutable storage flow from runtime decision, signed bundle, verifier gate, and storage plan into AWS S3 Object Lock and Azure Blob immutability.

## OIDC/RBAC Deployment

See `docs/diagrams/oidc-rbac-deployment.svg` for the dedicated identity flow from Entra ID or Okta discovery metadata and group claims into CAVRA OIDC config, repository RBAC, console sessions, approvals, and break-glass decisions.

## Go Parity and Sandbox Deployment

See `docs/diagrams/go-parity-sandbox-deployment.svg` for the dedicated flow from authoritative Python runtime behavior through shared parity fixtures, Go runtime tests, required CI checks, sandbox source, GitHub Pages deployment, and the future promotion gate.

## Runner OIDC and Evidence Verification

The release-governance runner wrapper now acquires provider OIDC tokens from GitHub Actions, GitLab CI, or Azure Pipelines when available, sends signed or OIDC-backed `runner_auth` to the Go daemon, records hash-chained evidence, verifies the evidence stream, and publishes `release-governance-evidence-verification.json` as an audit artifact. Custody and rotation guidance is documented in `Runner-Auth-And-Evidence-Key-Custody.md`.

## Go Reproducible Air-Gapped Build Flow

See `docs/diagrams/go-reproducible-airgap.svg` for the release path from connected GitHub Actions build, checksums, SBOM, signatures, provenance, and reproducibility metadata to restricted-environment verification and optional binary rebuild.

## Release Signing Operations

See `docs/diagrams/release-signing-operations.svg` for the release path from external signing key custody into signed package generation, verifier enforcement, planned key rotation, and emergency revocation evidence.

## High-Risk Command And Cloud/IaC Parity

See `docs/diagrams/high-risk-command-cloud-iac-parity.svg` for the shared fixture path that compares authoritative Python runtime decisions with Go runtime decisions before Go is allowed into deployment paths.

## Opt-In Go Backend Pilot

See `docs/diagrams/go-backend-pilot.svg` for the guarded backend-selection flow from operator opt-in through Python evaluation, Go comparison, parity gate, fallback, and readiness evidence.

## Go Backend Deployment Readiness

See `docs/diagrams/go-backend-deployment-readiness.svg` for the CI runner and workstation readiness path that checks release metadata before Go backend promotion.

## Go Backend Promotion Gate

See `docs/diagrams/go-backend-promotion.svg` for the promotion gate that requires runtime readiness, deployment readiness, audited parity evidence, and approval before `promoted` mode selects Go.

## Go Backend Rollback Controls

See `docs/diagrams/go-backend-rollback.svg` for the rollback gate that requires an approved plan back to Python-only mode before `promoted` mode selects Go.

## Go Backend Rollback Rehearsal

See `docs/diagrams/go-backend-rollback-rehearsal.svg` for the rehearsal evidence path that validates fallback restoration, recovery target, and dashboard visibility before `promoted` mode selects Go.

## Go Backend Rollback Drill History

See `docs/diagrams/go-backend-rollback-drill-history.svg` for the operational drill history path that validates fresh fallback drills before `promoted` mode selects Go.

## Go Backend Rollback Drill Scheduling

## Go Backend Rollback Drill Executive Delivery Retry Execution And Recovery Health Alerts

See `docs/diagrams/go-backend-rollback-drill-executive-delivery-retry-execution-and-recovery-health-alerts.svg` for the public-safe recovery retry health alert and executive report delivery retry execution loop.

## Go Backend Rollback Drill Retry Approvals And Recovery Playbooks

See `docs/diagrams/go-backend-rollback-drill-retry-approvals-recovery-playbooks.svg` for the approval path from failed acknowledgement audit delivery through retry acknowledgement, execution approval, approval-bound worker selection, and connector recovery playbooks.

## Go Backend Rollback Drill Live Retry Closure Evidence

See `docs/diagrams/go-backend-rollback-drill-live-retry-closure-evidence.svg` for the live retry execution and recovery closure path that links failed delivery, retry acknowledgement, approval, worker execution, connector recovery playbooks, and closure evidence.

## Go Backend Rollback Drill Retry Recovery Reporting

See `docs/diagrams/go-backend-rollback-drill-retry-recovery-reporting.svg` for the retry execution dashboard, recovery SLO, provider summary, and closure trend analytics flow.

## Go Backend Rollback Drill Recovery Escalation And Executive Reporting

See `docs/diagrams/go-backend-rollback-drill-recovery-escalation-executive-reporting.svg` for the public-safe flow from retry recovery evidence into escalation plans, connector delivery, executive reports, dashboard counts, and audit history.

## Go Backend Rollback Drill Recovery Escalation Acknowledgements And Scheduling

See `docs/diagrams/go-backend-rollback-drill-recovery-escalation-ack-retry-scheduling.svg` for the public-safe flow from escalation plans into provider acknowledgements, failed delivery retry plans, scheduled executive report runs, dashboard counts, and audit history.

## Go Backend Rollback Drill Recovery Escalation Retry Execution And Executive Delivery

See `docs/diagrams/go-backend-rollback-drill-recovery-escalation-retry-execution-and-executive-delivery.svg` for the public-safe flow from recovery escalation acknowledgements into retry worker execution, retry execution records, scheduled executive report delivery, dashboard counts, and audit history.

## Go Backend Rollback Drill Recovery Retry Health And Executive Delivery Retry

See `docs/diagrams/go-backend-rollback-drill-recovery-retry-health-and-executive-delivery-retry.svg` for the public-safe flow from retry worker metadata and executive delivery failures into health reports, retry decisions, dashboard counts, and audit history.

## Go Backend Rollback Drill Executive Retry Health And Recovery Health Alert Retry

See `docs/diagrams/go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.svg` for the public-safe flow from executive retry metadata and failed recovery health alert delivery into retry health reports, retry decisions, dashboard counts, and audit history.

## Go Backend Rollback Drill Recovery Health Alert Retry Worker And Executive Retry Health Alerts

See `docs/diagrams/go-backend-rollback-drill-recovery-health-alert-retry-worker-and-executive-retry-health-alerts.svg` for the public-safe flow from failed recovery health alert delivery through retry worker execution and executive retry health alert delivery.

## Go Backend Rollback Drill Executive Health Alert Retry And Final Closure

See `docs/diagrams/go-backend-rollback-drill-executive-health-alert-retry-final-closure.svg` for the public-safe flow from failed executive retry health alert delivery through retry planning, worker execution, execution evidence, and final reporting closure.

## Go Backend Rollback Drill Final Readiness Runbook Export

See `docs/diagrams/go-backend-rollback-drill-final-readiness-runbook-export.svg` for the public-safe flow from final closure evidence into release-readiness checks, operator runbook export, and release evidence attachment.

## Go Backend Rollback Drill Readiness Approval Release Record

See `docs/diagrams/go-backend-rollback-drill-readiness-approval-release-record.svg` for the public-safe flow from final readiness summary into governed approval, operator runbook export, release record attachment evidence, and private connector boundaries.

## Go Backend Rollback Drill Closure Packet Auditor Export

See `docs/diagrams/go-backend-rollback-drill-closure-packet-auditor-export.svg` for the public-safe flow from release record attachment into closure packet verification, auditor export, and private SIEM/GRC/archive extension points.

## Go Backend Rollback Drill Auditor Export Routing Archive

See `docs/diagrams/go-backend-rollback-drill-auditor-export-routing-archive.svg` for the public-safe flow from verified auditor exports into connector delivery metadata, immutable archive references, Evidence Console metrics, and private enterprise connector boundaries.

See `docs/diagrams/go-backend-rollback-drill-scheduling.svg` for the schedule and notification path that detects due-soon or stale rollback drills and emits redacted connector delivery evidence.

## Go Backend Rollback Drill Notification Escalation

See `docs/diagrams/go-backend-rollback-drill-notification-escalation.svg` for the acknowledgement and escalation path that tracks missed rollback drill notifications.

## Go Backend Rollback Drill Routing

See `docs/diagrams/go-backend-rollback-drill-routing.svg` for owner routing, maintenance-window suppression, owner calendar suppression, and route decision evidence for promoted Go backend rollback drills.

## Go Backend Rollback Drill Routing History

See `docs/diagrams/go-backend-rollback-drill-routing-history.svg` for the route-history and suppression-trend path that converts persisted route decisions into filterable evidence and audit summaries.

## Go Backend Rollback Drill Console

See `docs/diagrams/go-backend-rollback-drill-console.svg` for the Evidence Console drill-down flow across notification history, acknowledgement state, escalation routes, detail panels, and exportable public-safe evidence.

## Go Backend Rollback Drill Acknowledgement Controls

See `docs/diagrams/go-backend-rollback-drill-acknowledgement-controls.svg` for the authenticated console mutation flow that records route acknowledgements with verified actor identity.

## Go Backend Rollback Drill Bulk Acknowledgement Audit

See `docs/diagrams/go-backend-rollback-drill-bulk-acknowledgement-audit.svg` for the filtered bulk acknowledgement and acknowledgement audit package export flow.

## Go Backend Rollback Drill Acknowledgement Audit Delivery

See `docs/diagrams/go-backend-rollback-drill-acknowledgement-audit-delivery.svg` for the scheduled acknowledgement audit delivery routing flow.

## Go Backend Rollback Drill Audit Delivery Health

See `docs/diagrams/go-backend-rollback-drill-audit-delivery-health.svg` for acknowledgement audit delivery history filtering and health dashboards.

## Go Backend Rollback Drill Audit Delivery Retry Worker

See `docs/diagrams/go-backend-rollback-drill-audit-delivery-retry-worker.svg` for governed retry planning, scheduled worker dry-runs, and public-safe retry evidence indexing.

## Go Backend Rollback Drill Audit Worker Health Alerts

See `docs/diagrams/go-backend-rollback-drill-audit-worker-health-alerts.svg` for worker health alerts, health alert acknowledgements, and retry acknowledgement evidence.

## Go Backend Rollback Drill Executive Retry Health And Recovery Health Alert Retry

See `docs/diagrams/go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.svg` for executive retry health reporting and recovery health alert delivery retry planning.

## SVG Images

Repository diagram images:

- `docs/diagrams/architecture-context.svg`
- `docs/diagrams/c4-container.svg`
- `docs/diagrams/runtime-flow.svg`
- `docs/diagrams/evidence-hub.svg`
- `docs/diagrams/immutable-evidence-storage.svg`
- `docs/diagrams/oidc-rbac-deployment.svg`
- `docs/diagrams/go-parity-sandbox-deployment.svg`
- `docs/diagrams/go-reproducible-airgap.svg`
- `docs/diagrams/release-signing-operations.svg`
- `docs/diagrams/high-risk-command-cloud-iac-parity.svg`
- `docs/diagrams/go-backend-pilot.svg`
- `docs/diagrams/go-backend-deployment-readiness.svg`
- `docs/diagrams/go-backend-promotion.svg`
- `docs/diagrams/go-backend-rollback.svg`
- `docs/diagrams/go-backend-rollback-rehearsal.svg`
- `docs/diagrams/go-backend-rollback-drill-history.svg`
- `docs/diagrams/go-backend-rollback-drill-scheduling.svg`
- `docs/diagrams/go-backend-rollback-drill-notification-escalation.svg`
- `docs/diagrams/go-backend-rollback-drill-routing.svg`
- `docs/diagrams/go-backend-rollback-drill-routing-history.svg`
- `docs/diagrams/go-backend-rollback-drill-console.svg`
- `docs/diagrams/go-backend-rollback-drill-acknowledgement-controls.svg`
- `docs/diagrams/go-backend-rollback-drill-bulk-acknowledgement-audit.svg`
- `docs/diagrams/go-backend-rollback-drill-acknowledgement-audit-delivery.svg`
- `docs/diagrams/go-backend-rollback-drill-audit-delivery-health.svg`
- `docs/diagrams/go-backend-rollback-drill-audit-delivery-retry-worker.svg`
- `docs/diagrams/go-backend-rollback-drill-audit-worker-health-alerts.svg`
- `docs/diagrams/go-backend-rollback-drill-executive-retry-health-and-recovery-health-alert-retry.svg`
- `docs/diagrams/go-backend-rollback-drill-closure-packet-auditor-export.svg`
- `docs/diagrams/policy-lifecycle.svg`
- `docs/diagrams/developer-journey.svg`
- `docs/diagrams/agent-orchestration.svg`
