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

## Community AISPM

Community AISPM is public-safe. It includes static samples, schemas, public contracts, and the sandbox AI Posture route. It helps teams learn the data model without exposing private tenant data or Enterprise code.

Community references:

- [AI Security Posture Dashboard Contract](AI-Security-Posture-Dashboard-Contract)
- [AISPM Dashboard Roadmap](AISPM-Dashboard-Roadmap)
- [AISPM CSO Report Center](AISPM-CSO-Report-Center)
- [AISPM Report Center Enterprise Readiness](AISPM-Report-Center-Enterprise-Readiness)

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
