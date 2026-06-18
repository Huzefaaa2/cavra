# CAVRA Trial Field Guide

The CAVRA Trial Field Guide is the public-safe operating handbook for approved
Community and Enterprise Trial evaluators. It walks trial users through CAVRA
from first contact to closeout without exposing Enterprise source code,
license material, private package credentials, customer data, raw prompts, or
private policy-pack implementation details.

Use this guide with the public Community portal, the approved Enterprise Trial
request flow, and the validation packets linked from the release evidence
index.

## Audience

| Role | Primary Question | Field Guide Path |
| --- | --- | --- |
| Developer | Will CAVRA govern agent actions before they change code or tools? | Labs 1, 3, and 4 |
| Platform engineer | Can we wire CAVRA into repositories, CI, and runtime control points? | Labs 2, 3, 6, and 7 |
| Security engineer | Can we see risky agent actions, violations, and control coverage? | Labs 3, 4, 5, and 7 |
| Auditor | Can we prove what happened, who approved it, and what evidence exists? | Labs 4, 5, 6, and 8 |
| CSO/CISO | Is the AI-agent security posture understandable and board-reviewable? | Labs 4, 5, 7, and 8 |

## Guided Lab Map

| Lab | Name | Outcome | Primary Surface |
| --- | --- | --- | --- |
| 1 | Product orientation | Understand Community, Enterprise Trial, SaaS, and private-source boundaries. | Public docs and portal |
| 2 | Trial access request | Understand approved-access signup, operator review, package access, and license validation. | Trial portal |
| 3 | Governed agent action | Review allow, warn, block, approval, and attestation decisions. | Community dashboard |
| 4 | AISPM posture review | Inspect risk, agent coverage, timelines, evidence confidence, and control coverage. | AI Posture |
| 5 | CSO report center | Download Community reports and understand Enterprise delivery, audit, and retention controls. | Report Center |
| 6 | Operator readiness | Review release gates, trial handoff, runtime controls, and package-readiness boundaries. | Readiness packets |
| 7 | Pilot evidence room | Review pilot launch, exception, risk, board-pack, deployment, report-delivery, and runtime-workflow evidence. | Evidence packets |
| 8 | Trial closeout | Understand revocation, expiry, package access removal, blocked runtime validation, and feedback capture. | Closeout pages |

## Visual Walkthrough

![CAVRA dashboard overview](assets/aispm-lab/dashboard-desktop-classic.png)

The dashboard introduces the product, shows public-safe controls, and links to
Community documentation, trial access, demo flows, and release evidence.

![AISPM posture dashboard](assets/aispm-lab/aispm-desktop-sentinel.png)

The AISPM posture view uses sample or local data in Community and live,
authenticated, tenant-scoped data in Enterprise.

![AISPM report center](assets/aispm-lab/aispm-report-center-panel.png)

The CSO Report Center gives executives and auditors a central place to
download public-safe reports. Enterprise expands this with signed exports,
email delivery, retention, evidence rooms, and audit trails.

![AISPM board pack readiness](assets/aispm-lab/aispm-board-pack-panel.png)

The board-pack view groups launch decision, evidence room, risk acceptance,
exceptions, reviewer checklist, and report artifacts into one executive review
surface.

![CAVRA AISPM trial evaluation flow](assets/aispm-lab/aispm-trial-flow.svg)

## Lab 1: Product Orientation

1. Open `https://huzefaaa2.github.io/cavra/#dashboard`.
2. Confirm that the product is CAVRA: Controlled Agentic Verification &
   Runtime Authority.
3. Review the open-core boundary: Community source is public; Enterprise
   source, license service, SaaS backend, private policy packs, and private
   trial package implementation remain private.
4. Open the documentation links for AISPM Dashboard Roadmap, AI Security
   Posture Dashboard Contract, and Enterprise Trial Availability.

Checkpoint: `checkpoint-product-surfaces`

Expected result: the evaluator can explain Community, Enterprise Trial, SaaS,
and private-source boundaries.

## Lab 2: Trial Access Request

1. Open `https://cavra-trial.mind-ops.cloud`.
2. Submit a trial request with business contact details.
3. Confirm the request is recorded as pending approval.
4. Review [Trial Access And Operator Approval](AISPM-Trial-Access-And-Operator-Approval)
   to understand operator approval, package access, and license issuance.

Checkpoint: `checkpoint-trial-request`

Expected result: the evaluator understands why Enterprise Trial access is
approved and gated instead of anonymous.

## Lab 3: Governed Agent Action

1. Open the public dashboard and run the sample agent scenario.
2. Inspect the generated decision: allow, warn, block, require approval, or
   allow with attestation.
3. Download the public-safe evidence JSON.
4. Confirm the evidence identifies what the agent attempted, what CAVRA
   decided, why, and which evidence references support the decision.

Checkpoint: `checkpoint-agent-decision`

Expected result: the evaluator can see how CAVRA governs an AI-agent action
before relying on after-the-fact review.

## Lab 4: AISPM Posture Review

1. Open `AI Posture`.
2. Review live activity sample data, risk queue, execution timeline, approval
   lineage, control coverage heatmap, evidence confidence, and evidence
   freshness panels.
3. Confirm each tile clearly indicates public-safe sample/local provenance.
4. Review the executive risk narrative and near-miss queue.

Checkpoint: `checkpoint-aispm-posture`

Expected result: CSO/CISO, security, and platform teams can inspect AI-agent
posture without raw prompt or private payload exposure in Community.

## Lab 5: CSO Report Center

1. Open the report center inside the AI Posture route.
2. Download Community-safe executive, audit, control coverage, evidence
   freshness, and agent-risk reports.
3. Review [AISPM CSO Report Center](AISPM-CSO-Report-Center) for the Enterprise
   expansion: PDF, XLSX, DOCX, HTML, signed JSON, JSONL, GRC packages,
   scheduled email delivery, retry evidence, retention, and evidence-room
   access events.

Checkpoint: `checkpoint-report-center`

Expected result: executives and auditors can identify which reports exist in
Community and which delivery/governance capabilities require Enterprise.

## Lab 6: Operator Readiness

1. Review the Enterprise Trial readiness public summary:
   `docs/release-verifications/aispm-enterprise-trial-readiness-public-summary.json`.
2. Confirm the public-safe gates are ready: runtime binding, alert transport,
   release dashboard publication, trial field guide, operator audit archive,
   runtime-control closeout, systems-of-record attachment, and announcement
   closeout.
3. Review the release evidence index for validator paths and packet names.

Checkpoint: `checkpoint-operator-readiness`

Expected result: evaluators can see the readiness trail without seeing private
operator records or package credentials.

## Lab 7: Pilot Evidence Room

1. Review the public-safe pilot evidence room packet.
2. Confirm it references launch decision, reviewer checklist, exception
   register, risk acceptance, board pack, deployment runtime validation,
   report-delivery validation, and runtime-workflow validation.
3. Confirm the private implementation owns signed acceptance, board minutes,
   private ACLs, customer data, and authenticated evidence-room access logs.

Checkpoint: `checkpoint-pilot-evidence-room`

Expected result: CSO/CISO and auditors can understand the pilot evidence room
without receiving customer-private evidence.

## Lab 8: Trial Closeout

1. Review [Trial Revocation, Expiry, And Closeout](AISPM-Trial-Revocation-Expiry-And-Closeout).
2. Confirm closeout expectations: license expiry or revocation, package access
   removal, blocked runtime validation, archived evidence packet, evaluator
   feedback, and commercial/pilot handoff decision.

Checkpoint: `checkpoint-revocation-expiry`

Expected result: the evaluator understands how trial access is ended or
converted without leaving stale package or license access behind.

## Acceptance Checklist

| Checkpoint | Expected Evidence |
| --- | --- |
| Product surfaces | Public dashboard and open-core docs reviewed. |
| Trial request | Approved-access flow understood. |
| Agent decision | Public-safe decision evidence downloaded. |
| AISPM posture | Risk, coverage, timeline, and freshness panels reviewed. |
| Report center | Community downloads and Enterprise delivery boundary understood. |
| Operator readiness | Public-safe readiness summary reviewed. |
| Pilot evidence room | Required artifact families identified. |
| Revocation and expiry | Closeout and blocked-access expectations understood. |

## Public Safety Rules

Do not publish or attach Enterprise source code, license keys, package tokens,
private container URLs, SMTP credentials, signing keys, private policy-pack
implementation details, customer records, evaluator identities, operator
identities, IP addresses, raw prompts, model reasoning, raw tool output,
provider responses, private evidence room ACLs, signed download URLs, or
tenant-specific findings in this public guide.

Use public-safe summaries, screenshots, diagrams, packet names, hashes, and
status fields only.

## Related Pages

- [Trial Access And Operator Approval](AISPM-Trial-Access-And-Operator-Approval)
- [Trial Revocation, Expiry, And Closeout](AISPM-Trial-Revocation-Expiry-And-Closeout)
- [AISPM CSO Report Center](AISPM-CSO-Report-Center)
- [AISPM Report Center Enterprise Readiness](AISPM-Report-Center-Enterprise-Readiness)
- [AISPM Enterprise Trial Announcement Closeout Sync](AISPM-Enterprise-Trial-Announcement-Closeout-Sync)
