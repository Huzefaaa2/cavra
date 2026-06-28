# AISPM Guide

AISPM means AI Security Posture Management. In CAVRA, AISPM converts runtime governance evidence into posture, findings, reports, and readiness decisions.

![AISPM posture loop](assets/textbook/aispm-posture-loop.svg)

## What AISPM Answers

AISPM helps teams answer:

- Which agents are active?
- Which repositories and workflows are covered?
- Which MCP tools are trusted or risky?
- Which controls are enforced, shadowed, or missing?
- Which findings are open?
- Which approvals, exceptions, or break-glass events occurred?
- Which report packets are ready?
- Which blockers remain before trial, pilot, or production?

## How AISPM Is Built

AISPM is not a separate spreadsheet exercise. It is built from the evidence produced by runtime control paths:

1. Agents attempt actions.
2. CAVRA evaluates actions.
3. Decisions, approvals, registry checks, and evidence references are recorded.
4. Evidence is indexed and mapped to control coverage.
5. Findings, gaps, exceptions, and report readiness are calculated.
6. Operators review posture and remediate blockers.

This matters because posture should be anchored to real behavior. A dashboard that is not connected to runtime evidence can show confidence without control.

## Community AISPM

Community AISPM is public-safe. It includes static samples, schemas, public contracts, and the sandbox AI Posture route. It helps teams learn the data model without exposing private tenant data or Enterprise code.

![AISPM posture dashboard](assets/textbook/aispm-posture-desktop.png)

Community references:

- [AI Security Posture Dashboard Contract](AI-Security-Posture-Dashboard-Contract.md)
- [AISPM Dashboard Roadmap](AISPM-Dashboard-Roadmap.md)
- [AISPM CSO Report Center](AISPM-CSO-Report-Center.md)
- [AISPM Report Center Enterprise Readiness](AISPM-Report-Center-Enterprise-Readiness.md)

## Enterprise AISPM

Enterprise AISPM uses live tenant data. It depends on production-grade validation:

- Real production connectors.
- Real tenant isolation.
- Real SMTP or report provider settings.
- Real runtime agent and tool workflows.
- Live ingestion and streaming.
- Audit evidence for report delivery.
- Final production readiness packet.

The gate is complete only when the final validator returns `ready_for_aispm_production: true` with no blockers.

## Reading A Posture View

When reading an AISPM view, look at five layers:

| Layer | Question | Healthy signal |
| --- | --- | --- |
| Coverage | Which agents, repos, tools, and workflows are governed? | Coverage is explicit and current. |
| Control state | Are controls enforced, shadowed, missing, or blocked? | High-risk actions are enforced or approval-routed. |
| Findings | What remains open? | Critical findings have owners and due dates. |
| Evidence | Can the posture be proven? | Evidence is fresh, signed, searchable, and tied to decisions. |
| Reports | Can the posture be communicated? | Report packets are generated, delivered, and audited. |

Do not treat a green score as sufficient by itself. A useful AISPM view should let an operator drill from a score into the evidence that created it.

## Report Center

The Report Center turns posture into reader-ready material for executives and operators:

- CSO reports.
- CISO reports.
- Board KPI packs.
- SOC 2-style evidence packets.
- Incident and closure reports.
- Trial evaluator handoff packets.
- Pilot launch board packs.
- Production readiness packets.

![AISPM report center](assets/aispm-lab/aispm-report-center-panel.png)

## Report Generation Path

Use this conceptual path for any AISPM report:

1. Select tenant or public-safe sample scope.
2. Select report type: CSO, CISO, board KPI, SOC 2-style evidence, incident closure, trial handoff, pilot launch, or production readiness.
3. Confirm evidence freshness and trust roots.
4. Resolve blocking findings or mark accepted risk with owner and expiry.
5. Generate the report packet.
6. Deliver through SMTP/provider or public-safe export.
7. Capture delivery audit evidence.
8. Feed delivery state back into AISPM.

Enterprise report delivery is not complete until real provider settings and real recipients have been validated.

## Trial And Pilot Flow

AISPM supports a trial-to-pilot journey:

1. Trial access is approved.
2. Evaluators run guided labs.
3. Trial evidence is collected.
4. Report delivery is validated.
5. Pilot scope is proposed.
6. Pilot control readiness is reviewed.
7. Production evidence room is prepared.
8. Final production readiness is validated.

![AISPM trial flow](assets/aispm-lab/aispm-trial-flow.svg)

## AISPM Operating Model

AISPM should be reviewed on a recurring cadence:

- Daily: new blockers, failed connectors, critical findings.
- Weekly: control coverage, open findings, approval trends, report readiness.
- Monthly: executive report, tenant posture, exception aging, policy drift.
- Quarterly: advisory drill, production readiness archive, customer operating review.

## Common AISPM Blockers

| Blocker | Meaning | Resolution |
| --- | --- | --- |
| Missing live connector evidence | A report or posture source was not validated against a real provider. | Run connector validation and attach delivery audit evidence. |
| Tenant isolation not proven | Evidence, policy, or reports may cross tenant boundaries. | Run tenant isolation tests with real tenants and rerun readiness gate. |
| Report delivery unverified | SMTP/provider settings were configured but not proven end to end. | Send a validation report to approved recipients and capture audit output. |
| Runtime workflow synthetic only | Validators used fixtures but not real agent/tool workflows. | Run a real agent scenario through file, command, Git, and MCP paths. |
| Evidence stale | The packet is older than the release or pilot decision window. | Regenerate evidence and rerun the production readiness validator. |

## Check Your Understanding

1. Why should a green posture score still be traceable to source evidence?
2. Which blocker means validators used fixtures instead of real agent workflows?
3. What must happen before `ready_for_aispm_production: true` is trustworthy?

## What's Next

Read [Policies, Approvals, Evidence, And Attestations](Textbook-11-Policies-Approvals-Evidence-And-Attestations.md) to connect AISPM posture back to the decision and evidence mechanics.
