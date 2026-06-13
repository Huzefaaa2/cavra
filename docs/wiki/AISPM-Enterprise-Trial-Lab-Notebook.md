# CAVRA Enterprise Trial Lab Notebook

This page is the public-safe entry point for the future CAVRA Enterprise Trial
lab notebook. It gives approved evaluators a structured path to understand the
product, run governed AI-agent scenarios, inspect AISPM posture views, and
prepare evidence for security, audit, platform, and executive review.

The full Enterprise Trial package, license validation, private container
access, private lab fixtures, customer-specific setup values, and live
operator evidence remain outside the public Community repository.

## Audience

- Developers validating AI-agent enforcement behavior.
- Platform engineers preparing repository, CI, and runtime controls.
- Security engineers evaluating policy decisions and runtime governance.
- Auditors reviewing evidence, approvals, and report center outputs.
- CSO/CISO users reviewing posture, risk, coverage, and trial closeout.

## Lab Path

| Phase | Lab | Outcome |
| --- | --- | --- |
| Orientation | Product tour | Understand CAVRA editions, core surfaces, and evidence boundaries. |
| Trial access | Request and approval flow | Understand approved-access trial onboarding. |
| Agent enforcement | Governed agent scenario | Review allow, warn, block, and approval decisions. |
| AISPM dashboard | CSO/CISO posture review | Inspect risk, timelines, agent coverage, and evidence confidence. |
| Report center | Community reports and Enterprise governance | Download public-safe reports and review Enterprise report controls. |
| Readiness gates | Operator release gate review | Confirm Enterprise Trial gates are ready before package promotion. |
| Closeout | Revocation and expiry | Verify blocked access and closeout evidence expectations. |

## Required Public-Safe Assets

- Dashboard screenshot from `https://huzefaaa2.github.io/cavra/#dashboard`.
- Open-core model diagram from the architecture documentation.
- AISPM dashboard screenshot with sample or redacted data only.
- Revocation and expiry flow chart with no evaluator identity or license data.

## Visual Walkthrough

The following public-safe assets are included for approved evaluator onboarding
and public documentation. They use sample or static Community data only.

![CAVRA dashboard overview](assets/aispm-lab/dashboard-desktop-classic.png)

![AISPM posture dashboard](assets/aispm-lab/aispm-desktop-sentinel.png)

![AISPM report center](assets/aispm-lab/aispm-report-center-panel.png)

![AISPM board pack readiness](assets/aispm-lab/aispm-board-pack-panel.png)

![CAVRA AISPM trial evaluation flow](assets/aispm-lab/aispm-trial-flow.svg)

## Enterprise Trial Readiness Gates

The private Enterprise implementation now exposes the release gates required
before the Enterprise Trial package can be announced. This notebook documents
only public-safe gate names and outcomes.

| Gate | Public-Safe Outcome |
| --- | --- |
| Runtime Binding | Provider, scheduler, evidence sink, alert, Playwright session, and audit-storage references are present without exposing secrets. |
| Alert Transport | Email, ChatOps, SIEM, and ITSM smoke evidence is retained before release approval. |
| Release Dashboard Publication | Scheduler-produced release evidence is published to a release-dashboard reference. |
| Trial Lab Notebook | Screenshots, diagrams, flow charts, walkthroughs, and release evidence references are linked for evaluator onboarding. |
| Operator Audit Archive | Immutable operator audit archive and retention evidence are validated before release. |
| Trial Package Readiness Validator | Private packaging fails closed unless a current AISPM staging rehearsal packet proves all gates passed. |

Public readiness evidence:
`docs/release-verifications/aispm-enterprise-trial-readiness-public-summary.json`.

## Step-By-Step Lab

1. Open the public Community portal at
   `https://huzefaaa2.github.io/cavra/#dashboard`.
2. Confirm the product boundary: Community source is public, Enterprise Trial
   package access is approved and licensed, and private source is not exposed.
3. Open `AI Posture` and review the sample/local AISPM dashboard. Confirm the
   data provenance labels before using the dashboard for evaluator evidence.
4. Run the sample agent scenario from the dashboard and review the generated
   policy decision and evidence payload.
5. Open the CSO Report Center and download the Community-safe executive,
   audit, control coverage, evidence freshness, and agent-risk reports.
6. Review the trial readiness, trial handoff, closeout, procurement, pilot
   approval, evidence room, risk acceptance, board pack, and pilot control
   packets.
7. Review the Enterprise Trial readiness gate sync and confirm all public-safe
   gates are `ready` before treating the Enterprise Trial package as
   announcement-ready.
8. Attach only public-safe exports to evaluator or procurement records. Do not
   attach license keys, package tokens, private telemetry, customer data, raw
   prompts, model reasoning, or Enterprise source code.
9. During Enterprise Trial closeout, confirm the private operator has revoked
   package access, expired or revoked the license, and recorded blocked access
   evidence in the private system.

## Checkpoints

| Checkpoint | Expected Result |
| --- | --- |
| Product surfaces | Evaluator can identify Community, Enterprise Trial, AISPM, evidence, and report-center boundaries. |
| Agent decision | A governed agent action produces a policy decision and evidence reference. |
| CSO dashboard | Executive posture, risk, coverage, and evidence freshness views are understandable. |
| Community reports | Public-safe Community report downloads are available without Enterprise secrets. |
| Enterprise readiness gates | Runtime binding, alert transport, release dashboard, lab notebook, audit archive, and package validator gates are documented as public-safe ready summaries. |
| Revocation and expiry | Trial access is blocked after revocation or expiry in the private implementation. |

## Public Safety Rules

Do not publish Enterprise source code, license keys, package tokens, private
container URLs, customer data, evaluator identities, operator identities, IP
addresses, raw prompts, model reasoning, raw tool output, provider responses,
or private policy-pack implementation details in this notebook.

## Related Pages

- [Trial Access And Operator Approval](AISPM-Trial-Access-And-Operator-Approval)
- [Trial Revocation, Expiry, And Closeout](AISPM-Trial-Revocation-Expiry-And-Closeout)
- [AISPM CSO Report Center](AISPM-CSO-Report-Center)
- [AISPM Report Center Enterprise Readiness](AISPM-Report-Center-Enterprise-Readiness)
