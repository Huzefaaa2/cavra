# AISPM Dashboard Roadmap

CAVRA's public Evidence Console demonstrates the control model and supports
local or sample evidence views. The product roadmap now separates that public
surface from the future Enterprise AI Security Posture Management dashboard.

Enterprise should provide the live CSO/CISO operating surface:

- live agent activity across prompts, responses, reasoning traces, tool calls,
  file actions, shell commands, Git operations, MCP calls, CI runner activity,
  and cloud/IaC actions;
- policy decision streams for allow, warn, block, require approval, audit-only,
  and allow with attestation outcomes;
- risk and violation queues grouped by repository, agent, severity, control
  family, policy pack, data class, and environment;
- execution timelines and full trace replay for each governed session;
- approval lineage showing who approved what, when, why, under which policy,
  and with which evidence bundle;
- control coverage heatmaps for repositories, agent tools, CI gates, MCP
  servers, runtime modes, and enforcement backends;
- evidence confidence drilldowns for signed, activity-reference, sample,
  metadata-only, and missing evidence;
- evidence freshness and retention SLO panels for stale evidence, missing
  timestamps, retention gaps, and archive-readiness boundaries;
- executive risk narratives for CSO/CISO users that summarize posture, top
  risks, evidence gaps, and recommended actions;
- replay-to-policy authoring that converts governed traces into reviewed
  candidate controls, policy tests, and approval-bound policy changes;
- CSO controls for kill switch, quarantine, policy toggle, runtime override,
  rollback, and post-event review;
- CSO report center downloads for executive risk, board KPI, SOC 2-style audit,
  control coverage, evidence freshness, and agent risk reports;
- report catalog readiness with `docs/release-verifications/aispm-report-catalog-readiness.md`,
  `docs/release-verifications/aispm-report-catalog-readiness.json`,
  `scripts/validate-aispm-report-catalog-readiness.py`, and the portal export
  `cavra-aispm-report-catalog-packet.json`;
- report delivery setup readiness with
  `docs/release-verifications/aispm-report-delivery-setup-readiness.md`,
  `docs/release-verifications/aispm-report-delivery-setup-readiness.json`,
  `scripts/validate-aispm-report-delivery-setup-readiness.py`, and the portal
  export `cavra-aispm-report-delivery-setup-packet.json`;
- report operations readiness with
  `docs/release-verifications/aispm-report-operations-readiness.md`,
  `docs/release-verifications/aispm-report-operations-readiness.json`,
  `scripts/validate-aispm-report-operations-readiness.py`, and the portal
  export `cavra-aispm-report-operations-readiness-packet.json`;
- report governance readiness with
  `docs/release-verifications/aispm-report-governance-readiness.md`,
  `docs/release-verifications/aispm-report-governance-readiness.json`,
  `scripts/validate-aispm-report-governance-readiness.py`, and the portal
  export `cavra-aispm-report-governance-readiness-packet.json`;
- report assurance readiness with
  `docs/release-verifications/aispm-report-assurance-readiness.md`,
  `docs/release-verifications/aispm-report-assurance-readiness.json`,
  `scripts/validate-aispm-report-assurance-readiness.py`, and the portal
  export `cavra-aispm-report-assurance-readiness-packet.json`;
- report response readiness with
  `docs/release-verifications/aispm-report-response-readiness.md`,
  `docs/release-verifications/aispm-report-response-readiness.json`,
  `scripts/validate-aispm-report-response-readiness.py`, and the portal
  export `cavra-aispm-report-response-readiness-packet.json`;
- report trial operations readiness with
  `docs/release-verifications/aispm-report-trial-operations-readiness.md`,
  `docs/release-verifications/aispm-report-trial-operations-readiness.json`,
  `scripts/validate-aispm-report-trial-operations-readiness.py`, and the portal
  export `cavra-aispm-report-trial-operations-readiness-packet.json`;
- pilot control readiness with
  `docs/release-verifications/aispm-pilot-control-readiness.md`,
  `docs/release-verifications/aispm-pilot-control-readiness.json`,
  `scripts/validate-aispm-pilot-control-readiness.py`, and the portal export
  `cavra-aispm-pilot-control-readiness-packet.json`;
- Community AISPM v1.0 public release readiness with
  `docs/release-verifications/aispm-v1.0-public-release-readiness.md`,
  `docs/release-verifications/aispm-v1.0-public-release-readiness.json`,
  `scripts/validate-aispm-v100-public-release.py`,
  `docs/releases/community-v1.0.0-aispm.md`, and
  `docs/aispm-v1.0-public-walkthrough.md`;
- AISPM final public announcement readiness with
  `docs/release-verifications/aispm-final-announcement-readiness.md`,
  `docs/release-verifications/aispm-final-announcement-readiness.json`,
  `scripts/validate-aispm-final-announcement-readiness.py`, and
  `cavra-aispm-final-announcement-readiness-packet.json`;
- Enterprise report delivery through PDF, XLSX, DOCX, HTML, signed JSON, JSONL,
  GRC upload packages, signed export package manifests, artifact digests,
  evidence refs, governed report schedules, blackout windows, retry policies,
  scheduled email delivery, and scoped evidence rooms with expiring auditor
  access plus immutable access-event audit records, incident review packets,
  incident closure evidence, aggregate CSO KPI metrics, alert escalation, and
  alert operations dashboards with alert drilldowns, remediation plans,
  remediation closure, remediation closure operations dashboards, and
  remediation closure executive digests plus digest distribution governance;
- Enterprise Report Center implementation readiness checklist for private API,
  worker, storage, approval, delivery, and trial validation handoff;
- Enterprise Trial validation packet for setup, render, approval, delivery,
  evidence room, alert, closure, digest distribution, revocation, and
  retention checks;
- Trial operator dashboard readiness for validation status, blockers, evidence
  links, operator actions, and evaluator handoff;
- Trial operator dashboard API/view-model mapping for authenticated private
  portal routes, UI sections, approval actions, state transitions, and audit
  events;
- Trial evaluator handoff packets for setup steps, package access status,
  trial license status, support state, expiry, and revocation posture;
- Trial revocation and expiry evidence for blocked license validation, package
  access, portal access, report rendering, and support handoff;
- Trial lab notebook outlines for public-safe chapters, role paths, labs,
  screenshots, diagrams, flow charts, and verification checkpoints;
- Trial lab notebook publication readiness for Wiki navigation, link health,
  redacted screenshots, diagrams, flow charts, checkpoint evidence, and
  required reviews;
- compliance and audit views for SOC 2, ISO 27001, NIST SSDF, EU AI Act, PCI
  DSS, SOX, HIPAA, and internal AI governance controls.

Community should keep a public-safe dashboard demo and local activity view,
including observed control coverage, near-miss queues, trace replay packets
derived from local decisions, approval lineage from local approval records, and
behavior fingerprints, policy context gaps, pre-action risk forecasts,
evidence confidence drilldowns, evidence freshness SLO panels, deterministic
executive risk narratives, read-only replay-to-policy draft and test fixture
previews, replay-to-policy review packets, CI gate readiness exports, rollout
checklists, rollout audit packets, CI gate rollout auditor views, CSO report
center downloads, intent-to-action drift, and tool-chain risk graphing from declared intent, safe
tool labels, redacted targets, and observed action metadata.
Enterprise should own authenticated multi-tenant ingestion, streaming updates,
centralized retention, private policy context, organization controls, raw
prompt/reasoning replay, private behavior baselines, private context
enrichment, private asset/dependency/identity forecast enrichment,
prompt-derived semantic intent extraction, private workflow correlation, raw tool payload graphing, immutable evidence validation, cross-system execution traces,
private IdP/RBAC context, AI-assisted board summaries, private trend history,
tenant benchmarks, service criticality, customer-impact enrichment, private
prompt/reasoning/tool-payload policy authoring, tenant-history policy
simulation, approval-bound write-back automation, and commercial compliance
exports.

After all AISPM phases reach production-ready status, the GitHub Wiki must
include a public-safe trial-user lab notebook and product textbook. It should
walk users through CAVRA end to end with screenshots, diagrams, flow charts,
expected outputs, troubleshooting notes, and role-specific labs for developers,
platform teams, auditors, security engineers, and CSO/CISO users. The notebook
must not expose Enterprise source code, license secrets, private keys, customer
data, or private policy-pack implementation details.
Wiki publication should be gated by the public-safe publication readiness
contract so links, navigation, screenshots, diagrams, flow charts, checkpoint
evidence, and reviews are complete before external evaluators use it.
The gate is validated by `scripts/validate-aispm-trial-lab-notebook.py`, which
checks readiness packet schema validity, Wiki page presence, Home navigation,
public-safety sections, public-safe asset metadata, and required acceptance
criteria. The validator is wired into Community CI and Release Community
workflows so release validation fails if the notebook references drift.
Reviewer-facing readiness summaries live at
`docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md`
and
`docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json`.

The detailed implementation plan is maintained in
`docs/ai-security-posture-dashboard-roadmap.md`.

The public-safe Phase B closeout verification packet is maintained in
`docs/aispm-phase-b-closeout-verification.md` and mirrored as
`AISPM-Phase-B-Closeout-Verification.md`.

The public-safe Phase C Enterprise live ingestion design is maintained in
`docs/architecture/aispm-enterprise-live-ingestion.md` and mirrored as
`AISPM-Enterprise-Live-Ingestion.md`.

The public-safe CSO Report Center design is maintained in
`docs/architecture/aispm-report-center.md` and mirrored as
`AISPM-CSO-Report-Center.md`.

The AISPM dashboard now includes an Enterprise Trial readiness checklist that
lets CSO/CISO reviewers verify the lab notebook, trial access portal, operator
approval workflow, revocation and expiry evidence, release verification, and
Enterprise automation boundary from one public-safe dashboard section.
Reviewers can copy the Markdown readiness summary or download
`cavra-aispm-enterprise-trial-readiness-packet.json` for evaluator,
procurement, or security review attachment.
The same AISPM section shows an Enterprise Trial evaluator handoff with trial
portal, package reference, license validation boundary, lab notebook, support
path, and revocation/expiry closeout signals.
The dashboard also shows an Enterprise Trial evaluation journey timeline from
request submission through operator approval, package pull, license validation,
scenario execution, evidence review, and closeout verification.
Trial closeout evidence is shown for license expiry, revocation check, package
access removal, blocked runtime validation, archived evidence packet, and
evaluator feedback collection.
Trial feedback intake categories are shown for setup friction, policy clarity,
dashboard usefulness, report usefulness, integration gaps, procurement
concerns, and the go/no-go decision.
The AISPM Trial Outcome Summary rolls readiness, evaluator handoff, evaluation
journey, closeout evidence, and feedback coverage into a CSO/CISO go/no-go
review view.
A public-safe AISPM Trial Review Packet export bundles readiness, evaluator
handoff, evaluation journey, closeout evidence, feedback intake, and outcome
summary into `cavra-aispm-trial-review-packet.json`.
The AISPM Trial Review Packet Integrity panel shows schema version, generated
timestamp, expected filename, public-safety boundary, intentionally excluded
private fields, and Enterprise-only boundary signals.
The AISPM Trial Procurement Readiness panel translates the trial outcome into
buyer-facing review areas for legal, security, deployment, support, licensing,
data handling, and production pilot scope.
The AISPM Trial Pilot Scope Builder converts procurement readiness into target
repositories, AI agents, required checks, policies, evidence owners, success
criteria, and go/no-go date for a controlled production pilot.
The public-safe AISPM Trial Pilot Scope Packet export produces
`cavra-aispm-trial-pilot-scope-packet.json` for internal pilot approval
tickets.
The AISPM Pilot Approval Checklist shows final production-pilot gates for owner
assignment, repository selection, agent registration, required checks, policy
selection, evidence owners, support path, and go/no-go acceptance.
The public-safe AISPM Pilot Approval Packet export produces
`cavra-aispm-pilot-approval-packet.json` with the linked scope packet reference
and final approval gates for internal production-pilot approval records.
The AISPM Pilot Launch Readiness Summary rolls scope definition, approval
packet readiness, CSO reports, trial review evidence, support confirmation, and
CSO/CISO go/no-go status into one launch-candidate view.
The public-safe AISPM Pilot Launch Decision Packet export produces
`cavra-aispm-pilot-launch-decision-packet.json` with launch readiness rows,
source artifact references, public-safety boundary, and Enterprise-only signed
approval/write-back boundaries.
The Production Pilot Evidence Room view groups pilot artifacts for CSO/CISO,
security, platform, procurement, auditor, and operator review while keeping
authenticated access, retention, and signed activity logs as Enterprise-only
capabilities.
The public-safe Production Pilot Evidence Room Packet export produces
`cavra-aispm-pilot-evidence-room-packet.json` with the role-based reviewer
catalog, source artifacts, public-safety boundary, and Enterprise-only evidence
room capabilities.
The Evidence Room Reviewer Checklist defines pre-pilot acceptance criteria for
CSO/CISO, security, platform, procurement, auditor, and operator review while
signed acceptance remains an Enterprise-only workflow.
The public-safe Evidence Room Reviewer Checklist Packet export produces
`cavra-aispm-evidence-reviewer-checklist-packet.json` with role-based
acceptance criteria, source artifacts, public-safety boundary, and
Enterprise-only signed acceptance boundaries.
The Pilot Exception Register shows unresolved risks and accepted exceptions
with owner, status, expiry expectation, and Enterprise-only exception workflow
boundaries before production pilot launch.
The public-safe Pilot Exception Register Packet export produces
`cavra-aispm-pilot-exception-register-packet.json` with unresolved risks,
accepted exceptions, source artifacts, public-safety boundary, and
Enterprise-only exception lifecycle boundaries.
The Pilot Risk Acceptance Summary rolls up open exceptions, accepted risks,
monitored risks, accountable owners, launch-blocking items, and the
Enterprise-only signed risk acceptance boundary for CSO/CISO approval.
The public-safe Pilot Risk Acceptance Packet export produces
`cavra-aispm-pilot-risk-acceptance-packet.json` with the CSO/CISO risk roll-up,
source artifact references, public-safety boundary, and Enterprise-only signed
risk acceptance boundaries.
The Pilot Launch Board Pack view groups the launch decision, evidence room,
risk acceptance, exception register, reviewer checklist, and executive report
artifacts into one board/CISO-ready review surface while signed board approval,
minutes, PDF generation, and delivery workflow remain Enterprise-only.
The public-safe Pilot Launch Board Pack Packet export produces
`cavra-aispm-pilot-launch-board-pack-packet.json` with the board/CISO artifact
index, freshness gate, integrity summary, source artifact references, and
Enterprise-only boundaries for signed board approval, board minutes, PDF
generation, email delivery, recipient controls, and tenant artifact retention.
The artifact index is maintained in
`docs/release-verifications/aispm-launch-board-pack-artifact-index.json` and is
validated by `scripts/validate-aispm-launch-artifacts.py`.
The AISPM launch readiness rollup is maintained in
`docs/release-verifications/aispm-launch-readiness-rollup.md` and
`docs/release-verifications/aispm-launch-readiness-rollup.json`, and is
validated by `scripts/validate-aispm-launch-readiness.py` so Phase B closeout,
board-pack freshness, Playwright visual smoke, trial lab notebook readiness,
and GitHub Pages workflow validation stay aligned.
Hosted Pages smoke validation is maintained in
`docs/release-verifications/hosted-sandbox-pages-smoke-validation.md` and
`docs/release-verifications/hosted-sandbox-pages-smoke-validation.json`, and is
implemented by `scripts/validate-hosted-sandbox-pages.mjs` so the deployed
`#dashboard` and `#ai-posture` routes are browser-rendered after publication.
Hosted deployment freshness is maintained in
`docs/release-verifications/hosted-sandbox-deployment-freshness.md` and
`docs/release-verifications/hosted-sandbox-deployment-freshness.json`, validated
by `scripts/validate-hosted-sandbox-deployment-freshness.py`, and anchored by
the build sentinel `community-v1.0.0-aispm-release-evidence-index`.
Hosted release operator status is maintained in
`docs/release-verifications/hosted-sandbox-operator-release-status.md` and
`docs/release-verifications/hosted-sandbox-operator-release-status.json`,
validated by `scripts/validate-hosted-sandbox-operator-status.py`, and exported
from the portal as `cavra-hosted-sandbox-operator-status-packet.json`.
Post-deploy evidence is generated by
`scripts/generate-hosted-sandbox-deploy-evidence.py`, validated by
`scripts/validate-hosted-sandbox-deploy-evidence.py`, documented in
`docs/release-verifications/hosted-sandbox-post-deploy-evidence.md` and
`docs/release-verifications/hosted-sandbox-post-deploy-evidence.json`, and
uploaded as `cavra-hosted-sandbox-post-deploy-evidence`.
The reviewer-facing AISPM Release Evidence Index is published at
`docs/release-verifications/aispm-release-evidence-index.md` with the
machine-readable contract
`docs/release-verifications/aispm-release-evidence-index.json`, validated by
`scripts/validate-aispm-release-evidence-index.py`, and exported from the
portal as `cavra-aispm-release-evidence-index-packet.json`.
