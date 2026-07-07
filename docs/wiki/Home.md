# Before the Agent Acts: The CAVRA Technical Textbook

Welcome to the CAVRA Wiki. This wiki now opens as a technical textbook for CAVRA, Controlled Agentic Verification and Runtime Authority. It is written for developers, security engineers, platform owners, compliance teams, architects, and enterprise evaluators who need to understand what CAVRA is, how it works, how to run it, and how to operate it safely.

CAVRA exists for a simple reason: AI agents should not receive unchecked authority over code, cloud, data, identity, CI/CD, MCP tools, and production workflows. CAVRA gives organizations a runtime authority layer that evaluates agent actions before they happen, records evidence after they happen, and turns that evidence into AI Security Posture Management, or AISPM. The current product roadmap also extends the same control planes to model registries, AI artifacts, scanner metadata, supply-chain checks, and compliance evidence.

## Introduction Video

Start here if you are new to CAVRA. The introduction video explains the core idea: before an AI agent reads, writes, executes, changes infrastructure, or calls tools, CAVRA checks authority, records evidence, and turns runtime activity into AI Security Posture Management.

https://github.com/user-attachments/assets/c69dd45a-fb2c-4181-89d6-7cc014531b83

If the embedded GitHub player does not load in your browser, use the hosted backup: [Watch the CAVRA introduction video on InVideo](https://ai.invideo.io/watch/cq7iExDcHvs).

## Product Website

The primary commercial product front door is [cavra.mind-ops.cloud](https://cavra.mind-ops.cloud/). Use it for the buyer and evaluator journey across CAVRA Managed, CAVRA Enterprise Subscription, Trial Access, AISPM, trust, resources, and product contact paths.

The GitHub Pages site at [huzefaaa2.github.io/cavra](https://huzefaaa2.github.io/cavra/) remains the public interactive sandbox and documentation bridge.

## Current Product Model

CAVRA is now organized around a Community-first model:

- **CAVRA Community:** the full public self-hosted product and default codebase.
- **CAVRA Managed:** hosted CAVRA operated as a managed service.
- **CAVRA Enterprise Subscription:** commercial support, SLA, certified integrations, policy packs, compliance packs, implementation help, and private customer operations.
- **CAVRA Trial:** temporary evaluation access for Managed or Enterprise Subscription capabilities. Trial is not a separate source edition.

Start with [Product Model](Product-Model.md), [Community Self-Hosted Guide](Community-Self-Hosted-Guide.md), [CAVRA Managed Guide](CAVRA-Managed-Guide.md), [Enterprise Subscription Guide](Enterprise-Subscription-Guide.md), and [Trial Access Guide](Trial-Access-Guide.md).

The active enhancement tracker is [CAVRA Unified Enterprise Enhancement Roadmap](CAVRA-Unified-Enterprise-Enhancement-Roadmap.md). It records the numbered plan for identity, multi-tenancy, KMS/HSM signing, immutable audit, compliance packs, connector SDKs, zero-trust scanner agents, model/artifact governance, policy lifecycle tooling, event-driven monitoring, and scale validation.

New Enterprise contract references: [Zero-Trust Scanner Agent](Zero-Trust-Scanner-Agent.md), [Zero-Trust Reference Deployments](Zero-Trust-Reference-Deployments.md), [OPA/Rego Policy Path](OPA-Rego-Policy-Path.md), [Policy Lifecycle Tooling](Policy-Lifecycle-Tooling.md), [Continuous Monitoring Event Core](Continuous-Monitoring-Event-Core.md), [Benchmark SLO Regression Gates](Benchmark-SLO-Regression-Gates.md), [Generic Agent Adapter SDK And Action Taxonomy](Generic-Agent-Adapter-SDK-And-Action-Taxonomy.md), [AI Red-Team And Supply-Chain Gates](AI-Red-Team-And-Supply-Chain-Gates.md), [Phase 6 Ecosystem Expansion Rollup](Phase-6-Ecosystem-Expansion-Rollup.md), [Customer Live Evidence Intake](Customer-Live-Evidence-Intake.md), [Customer Evidence Room Closeout](Customer-Evidence-Room-Closeout.md), [Customer Closeout Handoff](Customer-Closeout-Handoff.md), [Customer Operating Review](Customer-Operating-Review.md), [Customer Renewal And Expansion Readiness](Customer-Renewal-And-Expansion-Readiness.md), [Customer Renewal Outcome Closeout](Customer-Renewal-Outcome-Closeout.md), [Customer Lifecycle Executive Rollup](Customer-Lifecycle-Executive-Rollup.md), [Customer Lifecycle Archive Manifest](Customer-Lifecycle-Archive-Manifest.md), [Customer Lifecycle Public Status Summary](Customer-Lifecycle-Public-Status.md), [Customer Lifecycle Final Release Seal](Customer-Lifecycle-Final-Release-Seal.md), [Customer Lifecycle Verification Index](Customer-Lifecycle-Verification-Index.md), [Customer Lifecycle Closeout Announcement](Customer-Lifecycle-Closeout-Announcement.md), [Customer Lifecycle Retrospective](Customer-Lifecycle-Retrospective.md), [Customer Lifecycle Phase 8 Backlog](Customer-Lifecycle-Phase-8-Backlog.md), [Customer Lifecycle Phase 8 Kickoff](Customer-Lifecycle-Phase-8-Kickoff.md), [Customer Lifecycle Phase 8 Sprint 1 Checkpoint](Customer-Lifecycle-Phase-8-Sprint-1-Checkpoint.md), [Customer Lifecycle Phase 8 Telemetry Depth](Customer-Lifecycle-Phase-8-Telemetry-Depth.md), [Customer Lifecycle Phase 8 Support Automation](Customer-Lifecycle-Phase-8-Support-Automation.md), [Customer Lifecycle Phase 8 Lifecycle Analytics](Customer-Lifecycle-Phase-8-Lifecycle-Analytics.md), [Customer Lifecycle Phase 8 Customer Health Review](Customer-Lifecycle-Phase-8-Customer-Health-Review.md), [Customer Lifecycle Phase 8 Executive Health Rollup](Customer-Lifecycle-Phase-8-Executive-Health-Rollup.md), [Customer Lifecycle Phase 8 Executive Action Plan](Customer-Lifecycle-Phase-8-Executive-Action-Plan.md), [Customer Lifecycle Phase 8 Action Follow-up Checkpoint](Customer-Lifecycle-Phase-8-Action-Follow-up-Checkpoint.md), [Customer Lifecycle Phase 8 Executive Follow-up Closeout](Customer-Lifecycle-Phase-8-Executive-Follow-up-Closeout.md), [Customer Lifecycle Phase 8 Next-Cycle Readiness Index](Customer-Lifecycle-Phase-8-Next-Cycle-Readiness-Index.md), [Customer Lifecycle Phase 8 Public Operating Scorecard](Customer-Lifecycle-Phase-8-Public-Operating-Scorecard.md), [Customer Lifecycle Phase 8 Public Scorecard Publication Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Publication-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Refresh Checkpoint](Customer-Lifecycle-Phase-8-Public-Scorecard-Refresh-Checkpoint.md), [Customer Lifecycle Phase 8 Public Scorecard Refresh Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Refresh-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Operating Loop Index](Customer-Lifecycle-Phase-8-Public-Scorecard-Operating-Loop-Index.md), [Customer Lifecycle Phase 8 Public Scorecard Executive Summary Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Executive-Summary-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Distribution Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Distribution-Readiness.md), [Customer Lifecycle Phase 8 Public Scorecard Distribution Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Distribution-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Distribution Audit Index](Customer-Lifecycle-Phase-8-Public-Scorecard-Distribution-Audit-Index.md), [Customer Lifecycle Phase 8 Public Scorecard Audit Review Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Audit-Review-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Continuous Monitoring Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Continuous-Monitoring-Readiness.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Activation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring First-Cycle Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-First-Cycle-Review.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Drift-Remediation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Second-Cycle-Readiness.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Second-Cycle-Activation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Second-Cycle-First-Review.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Second-Cycle-Drift-Remediation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Third-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Third-Cycle-Readiness.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Third-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Third-Cycle-Activation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Third-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Third-Cycle-First-Review.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Third-Cycle Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Third-Cycle-Drift-Remediation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fourth-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fourth-Cycle-Readiness.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fourth-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fourth-Cycle-Activation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fourth-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fourth-Cycle-First-Review.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fourth-Cycle Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fourth-Cycle-Drift-Remediation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fifth-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fifth-Cycle-Readiness.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fifth-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fifth-Cycle-Activation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fifth-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fifth-Cycle-First-Review.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fifth-Cycle Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fifth-Cycle-Drift-Remediation-Closeout.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Sixth-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Sixth-Cycle-Readiness.md), [Customer Lifecycle Phase 8 Public Scorecard Monitoring Sixth-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Sixth-Cycle-Activation-Closeout.md), and [Customer Lifecycle Phase 8 Public Scorecard Monitoring Sixth-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Sixth-Cycle-First-Review.md).

For Phase 2 implementation, use [Enterprise Identity And Access Control](Enterprise-Identity-And-Access-Control.md), [Enterprise Live Identity Validation](Enterprise-Live-Identity-Validation.md), and [Tenant Workspace Persistence](Tenant-Workspace-Persistence.md).

![CAVRA runtime authority map](assets/textbook/cavra-runtime-authority-map.svg)

![Animated CAVRA runtime authority loop showing an agent request moving through policy, approval, evidence, and AISPM posture](assets/textbook/dynamic-runtime-authority-loop.svg)

## Start Here

Read the book in order if you are new to CAVRA. Jump directly to the command, GUI, AISPM, or deployment chapters if you already know the product shape.

![Five-minute CAVRA journey](assets/textbook/getting-started-journey.svg)

## Five-Minute Quick Start

If you want to see CAVRA work before reading the full book, follow this short path:

1. Install CAVRA Community from the repository with `pip install -e .`.
2. Run `cavra version` and `cavra policy list`.
3. Run `cavra demo before-the-agent-acts` to see CAVRA block risky agent behavior.
4. Run `cavra evaluate execute_command "terraform apply -auto-approve" --json` to evaluate a dangerous command directly.
5. Run `cavra evidence bundle --output .cavra/evidence/latest` and `cavra evidence verify .cavra/evidence/latest` to prove the control path.
6. Open the sandbox GUI and review the decision, evidence, and AISPM views.

The detailed walkthrough is in [Install And Deploy CAVRA](Textbook-05-Install-And-Deploy-CAVRA.md), [CAVRA Community User Guide](Textbook-06-Community-Edition-User-Guide.md), and [Use Cases, Labs, And Example Workflows](Textbook-13-Use-Cases-Labs-And-Example-Workflows.md).

## Learning Paths

| Reader | Read first | Outcome |
| --- | --- | --- |
| First-time user | Chapters 0, 1, 5, 6, 13 | Install, run a demo, block a risky action, and verify evidence. |
| Developer | Chapters 5, 6, 8, 11, 18 | Use the CLI, write policy, route approvals, understand the implementation stack, and create evidence. |
| Security architect | Chapters 1, 2, 3, 11, 15, 16 | Understand the runtime authority model, policy language, governance controls, and troubleshooting. |
| Platform owner | Chapters 3, 5, 8, 12, 18 | Integrate CAVRA into CI/CD, APIs, operating workflows, storage, deployment, and validation paths. |
| Evaluator or buyer | Chapters 4, 7, 10, 12, 13, 16 | Validate self-hosted configuration, Managed service fit, Enterprise Subscription needs, AISPM, report delivery, and blocker closeout. |

## Complete Table Of Contents

1. [Foreword, Preface, And Reader Paths](Textbook-00-Foreword-Preface-And-Reader-Paths.md)
2. [Why CAVRA Exists](Textbook-01-Why-CAVRA-Exists.md)
3. [The Runtime Authority Model](Textbook-02-Runtime-Authority-Model.md)
4. [Architecture And Open-Core Design](Textbook-03-Architecture-And-Open-Core-Design.md)
5. [Product Model, Licensing, And Capability Boundaries](Textbook-04-Editions-Licensing-And-Feature-Boundaries.md)
6. [Install And Deploy CAVRA](Textbook-05-Install-And-Deploy-CAVRA.md)
7. [CAVRA Community User Guide](Textbook-06-Community-Edition-User-Guide.md)
8. [CAVRA Managed And Enterprise Subscription Guide](Textbook-07-Enterprise-Edition-User-Guide.md)
9. [CAVRA CLI Command Reference](Textbook-08-CAVRA-CLI-Command-Reference.md)
10. [CAVRA GUI And Sandbox Guide](Textbook-09-CAVRA-GUI-And-Sandbox-Guide.md)
11. [AISPM Guide](Textbook-10-AISPM-Guide.md)
12. [Policies, Approvals, Evidence, And Attestations](Textbook-11-Policies-Approvals-Evidence-And-Attestations.md)
13. [Operations, Integrations, And Deployment Patterns](Textbook-12-Operations-Integrations-And-Deployment-Patterns.md)
14. [Use Cases, Labs, And Example Workflows](Textbook-13-Use-Cases-Labs-And-Example-Workflows.md)
15. [Reference Appendices](Textbook-14-Reference-Appendices.md)
16. [Policy Language Reference](Textbook-15-Policy-Language-Reference.md)
17. [Troubleshooting And FAQ](Textbook-16-Troubleshooting-And-FAQ.md)
18. [CAVRA Technology Stack And Implementation Model](Textbook-18-CAVRA-Technology-Stack.md)
19. [Conclusion: The Runtime Authority Revolution](Textbook-17-The-Runtime-Authority-Revolution.md)

## Visual Index

| Topic | Diagram |
| --- | --- |
| Runtime authority | [CAVRA runtime authority map](assets/textbook/cavra-runtime-authority-map.svg) |
| Architecture context | [Architecture context](assets/textbook/architecture-context.svg) |
| Runtime decision flow | [Runtime flow](assets/textbook/runtime-flow.svg) |
| Product model | [Product model map](assets/textbook/cavra-edition-map.svg) |
| CLI command families | [Command map](assets/textbook/cavra-command-map.svg) |
| AISPM posture loop | [AISPM posture loop](assets/textbook/aispm-posture-loop.svg) |
| Enterprise sequence | [Enterprise sequence](assets/textbook/cavra-enterprise-sequence.svg) |
| Getting started journey | [Getting started journey](assets/textbook/getting-started-journey.svg) |
| Policy authoring journey | [Policy authoring journey](assets/textbook/policy-authoring-journey.svg) |
| Approval routing | [Approval routing flow](assets/textbook/approval-routing-flow.svg) |
| Troubleshooting | [Troubleshooting decision tree](assets/textbook/troubleshooting-decision-tree.svg) |
| Dynamic runtime loop | [Animated runtime authority loop](assets/textbook/dynamic-runtime-authority-loop.svg) |
| Dynamic AISPM readiness | [Animated AISPM readiness pulse](assets/textbook/dynamic-aispm-readiness-pulse.svg) |
| Technology stack | [Animated technology stack map](assets/textbook/cavra-technology-stack-map.svg) |
| Runtime implementation pipeline | [Animated runtime implementation pipeline](assets/textbook/cavra-technology-runtime-pipeline.svg) |
| Storage and evidence model | [Animated storage and evidence model](assets/textbook/cavra-storage-evidence-model.svg) |
| Unified enhancement roadmap | [Animated enterprise roadmap](assets/textbook/cavra-unified-enterprise-roadmap.svg) |

The animated diagrams are SVG-native and are written to degrade into readable static diagrams when motion is disabled by browser, accessibility, or renderer settings. Every textbook image uses descriptive alt text in the surrounding Markdown.

## Trial Access Path

Approved evaluators start at the public trial portal:

- [CAVRA Trial](https://cavra-trial.mind-ops.cloud/)

The trial portal is the starting point for requesting operator-reviewed access,
hosted or package entitlement where applicable, and time-limited evaluator material. After
approval, use the [CAVRA Trial Field Guide](CAVRA-Trial-Field-Guide.md) to run a
complete proof-of-value scenario: choose one repository or workflow, govern one
risky AI-agent action, route one approval, generate evidence, review AISPM, and
close out the trial without leaving stale package or license access behind.

## Primary Product References

- [CAVRA Product Website](https://cavra.mind-ops.cloud/)
- [CAVRA Unified Enterprise Enhancement Roadmap](CAVRA-Unified-Enterprise-Enhancement-Roadmap.md)
- [CAVRA API Versioning And OpenAPI Contract](https://github.com/Huzefaaa2/cavra/blob/main/docs/api-versioning-and-openapi.md)
- [CAVRA Enterprise Identity And Access Control](Enterprise-Identity-And-Access-Control.md)
- [CAVRA CISO And Enterprise Trust Pack](https://github.com/Huzefaaa2/cavra/blob/main/docs/trust/ciso-enterprise-trust-pack.md)
- [CAVRA Maintainer Governance](https://github.com/Huzefaaa2/cavra/blob/main/docs/governance/maintainer-governance.md)
- [CAVRA RFC Process](https://github.com/Huzefaaa2/cavra/blob/main/docs/governance/rfc-process.md)
- [CAVRA Release Trust Checklist](https://github.com/Huzefaaa2/cavra/blob/main/docs/release-trust-checklist.md)
- [CAVRA Commercial Site Hosting](https://github.com/Huzefaaa2/cavra/blob/main/docs/product/cavra-commercial-site-hosting.md)
- [CAVRA Product Introduction Video Script](https://github.com/Huzefaaa2/cavra/blob/main/docs/product/cavra-product-introduction-video-script.md)
- [CLI](CLI.md)
- [API](API.md)
- [Diagrams](Diagrams.md)
- [Product Model](Product-Model.md)
- [Product Boundaries](Product-Boundaries.md)
- [Capability Configuration Guide](Capability-Configuration-Guide.md)
- [Provider Interfaces](Provider-Interfaces.md)
- [Edition Boundaries](Edition-Boundaries.md)
- [AI Agent Enforcement And Anti-Bypass Model](AI-Agent-Enforcement-And-Anti-Bypass-Model.md)
- [Agent Registry And MCP Trust](Agent-Registry-and-MCP-Trust.md)
- [Approval Workflows](Approval-Workflows.md)
- [Evidence Hub And Attestation](Evidence-Hub-and-Attestation.md)
- [Policy Engine Hardening](Policy-Engine-Hardening.md)
- [Policy Lifecycle Tooling](Policy-Lifecycle-Tooling.md)
- [Continuous Monitoring Event Core](Continuous-Monitoring-Event-Core.md)
- [AISPM Dashboard Roadmap](AISPM-Dashboard-Roadmap.md)
- [AI Security Posture Dashboard Contract](AI-Security-Posture-Dashboard-Contract.md)
- [AISPM CSO Report Center](AISPM-CSO-Report-Center.md)
- [AISPM Enterprise Live Ingestion](AISPM-Enterprise-Live-Ingestion.md)
- [CAVRA Trial Field Guide](CAVRA-Trial-Field-Guide.md)
- [Zero-Trust Reference Deployments](Zero-Trust-Reference-Deployments.md)
- [Phase 6 Ecosystem Expansion Rollup](Phase-6-Ecosystem-Expansion-Rollup.md)
- [Customer Live Evidence Intake](Customer-Live-Evidence-Intake.md)
- [Customer Evidence Room Closeout](Customer-Evidence-Room-Closeout.md)
- [Customer Renewal Outcome Closeout](Customer-Renewal-Outcome-Closeout.md)
- [Customer Lifecycle Executive Rollup](Customer-Lifecycle-Executive-Rollup.md)
- [Customer Lifecycle Archive Manifest](Customer-Lifecycle-Archive-Manifest.md)
- [Customer Lifecycle Public Status Summary](Customer-Lifecycle-Public-Status.md)
- [Customer Lifecycle Final Release Seal](Customer-Lifecycle-Final-Release-Seal.md)
- [Customer Lifecycle Verification Index](Customer-Lifecycle-Verification-Index.md)
- [Customer Lifecycle Closeout Announcement](Customer-Lifecycle-Closeout-Announcement.md)
- [Customer Lifecycle Retrospective](Customer-Lifecycle-Retrospective.md)
- [Customer Lifecycle Phase 8 Backlog](Customer-Lifecycle-Phase-8-Backlog.md)
- [Customer Lifecycle Phase 8 Kickoff](Customer-Lifecycle-Phase-8-Kickoff.md)
- [Customer Lifecycle Phase 8 Sprint 1 Checkpoint](Customer-Lifecycle-Phase-8-Sprint-1-Checkpoint.md)
- [Customer Lifecycle Phase 8 Telemetry Depth](Customer-Lifecycle-Phase-8-Telemetry-Depth.md)
- [Customer Lifecycle Phase 8 Support Automation](Customer-Lifecycle-Phase-8-Support-Automation.md)
- [Customer Lifecycle Phase 8 Lifecycle Analytics](Customer-Lifecycle-Phase-8-Lifecycle-Analytics.md)
- [Customer Lifecycle Phase 8 Customer Health Review](Customer-Lifecycle-Phase-8-Customer-Health-Review.md)
- [Customer Lifecycle Phase 8 Executive Health Rollup](Customer-Lifecycle-Phase-8-Executive-Health-Rollup.md)
- [Customer Lifecycle Phase 8 Executive Action Plan](Customer-Lifecycle-Phase-8-Executive-Action-Plan.md)
- [Customer Lifecycle Phase 8 Action Follow-up Checkpoint](Customer-Lifecycle-Phase-8-Action-Follow-up-Checkpoint.md)
- [Customer Lifecycle Phase 8 Executive Follow-up Closeout](Customer-Lifecycle-Phase-8-Executive-Follow-up-Closeout.md)
- [Customer Lifecycle Phase 8 Next-Cycle Readiness Index](Customer-Lifecycle-Phase-8-Next-Cycle-Readiness-Index.md)
- [Customer Lifecycle Phase 8 Public Operating Scorecard](Customer-Lifecycle-Phase-8-Public-Operating-Scorecard.md)
- [Customer Lifecycle Phase 8 Public Scorecard Publication Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Publication-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Refresh Checkpoint](Customer-Lifecycle-Phase-8-Public-Scorecard-Refresh-Checkpoint.md)
- [Customer Lifecycle Phase 8 Public Scorecard Refresh Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Refresh-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Operating Loop Index](Customer-Lifecycle-Phase-8-Public-Scorecard-Operating-Loop-Index.md)
- [Customer Lifecycle Phase 8 Public Scorecard Executive Summary Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Executive-Summary-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Distribution Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Distribution-Readiness.md)
- [Customer Lifecycle Phase 8 Public Scorecard Distribution Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Distribution-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Distribution Audit Index](Customer-Lifecycle-Phase-8-Public-Scorecard-Distribution-Audit-Index.md)
- [Customer Lifecycle Phase 8 Public Scorecard Audit Review Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Audit-Review-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Continuous Monitoring Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Continuous-Monitoring-Readiness.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Activation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring First-Cycle Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-First-Cycle-Review.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Drift-Remediation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Second-Cycle-Readiness.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Second-Cycle-Activation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Second-Cycle-First-Review.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Second-Cycle-Drift-Remediation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Third-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Third-Cycle-Readiness.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Third-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Third-Cycle-Activation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Third-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Third-Cycle-First-Review.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Third-Cycle Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Third-Cycle-Drift-Remediation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fourth-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fourth-Cycle-Readiness.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fourth-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fourth-Cycle-Activation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fourth-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fourth-Cycle-First-Review.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fourth-Cycle Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fourth-Cycle-Drift-Remediation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fifth-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fifth-Cycle-Readiness.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fifth-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fifth-Cycle-Activation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fifth-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fifth-Cycle-First-Review.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Fifth-Cycle Drift Remediation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Fifth-Cycle-Drift-Remediation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Sixth-Cycle Readiness](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Sixth-Cycle-Readiness.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Sixth-Cycle Activation Closeout](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Sixth-Cycle-Activation-Closeout.md)
- [Customer Lifecycle Phase 8 Public Scorecard Monitoring Sixth-Cycle First Review](Customer-Lifecycle-Phase-8-Public-Scorecard-Monitoring-Sixth-Cycle-First-Review.md)
- [Customer Closeout Handoff](Customer-Closeout-Handoff.md)
- [Customer Operating Review](Customer-Operating-Review.md)
- [Customer Renewal And Expansion Readiness](Customer-Renewal-And-Expansion-Readiness.md)
- [AISPM Trial Access And Operator Approval](AISPM-Trial-Access-And-Operator-Approval.md)
- [AISPM Trial Revocation, Expiry, And Closeout](AISPM-Trial-Revocation-Expiry-And-Closeout.md)
- [Trial Access Guide](Trial-Access-Guide.md)
- [Enterprise Trial Availability](Enterprise-Trial-Availability.md)
- [Enterprise Trial Self-Service Access](Enterprise-Trial-Self-Service-Access.md)
- [Azure Community Deployment](Azure-Community-SaaS-Deployment.md)
- [Azure Trial And Enterprise Deployment](Azure-Trial-And-Enterprise-Deployment.md)

## Development And Testing Archive

Historical implementation notes, release packets, validation records, trial synchronization notes, rollback-drill records, closeout documents, and readiness artifacts are preserved in one archive:

- [Development And Testing Artifacts](Development-And-Testing-Artifacts.md)

The archive is intentionally separated from the textbook so new readers can learn CAVRA without walking through every development milestone.

<!--
Legacy validation references kept non-rendered so historical release validators can
confirm public navigation freshness while the visible wiki home remains book-first.

CAVRA-Developer-Portal-Redesign.md
CAVRA-Developer-Portal-Smoke-Validation.md
docs/releases/community-v1.0.0-aispm.md
docs/aispm-v1.0-public-walkthrough.md
docs/release-verifications/aispm-v1.0-public-release-readiness.md
docs/release-verifications/aispm-v1.0-public-release-readiness.json
scripts/validate-aispm-v100-public-release.py
docs/release-verifications/aispm-launch-readiness-rollup.md
docs/release-verifications/aispm-launch-readiness-rollup.json
scripts/validate-aispm-launch-readiness.py
docs/release-verifications/hosted-sandbox-pages-smoke-validation.md
docs/release-verifications/hosted-sandbox-pages-smoke-validation.json
scripts/validate-hosted-sandbox-pages.mjs
docs/release-verifications/hosted-sandbox-deployment-freshness.md
docs/release-verifications/hosted-sandbox-deployment-freshness.json
scripts/validate-hosted-sandbox-deployment-freshness.py
community-v1.0.0-aispm-release-evidence-index
docs/release-verifications/hosted-sandbox-operator-release-status.md
docs/release-verifications/hosted-sandbox-operator-release-status.json
scripts/validate-hosted-sandbox-operator-status.py
cavra-hosted-sandbox-operator-status-packet.json
docs/release-verifications/hosted-sandbox-post-deploy-evidence.md
docs/release-verifications/hosted-sandbox-post-deploy-evidence.json
scripts/generate-hosted-sandbox-deploy-evidence.py
scripts/validate-hosted-sandbox-deploy-evidence.py
cavra-hosted-sandbox-post-deploy-evidence
docs/release-verifications/aispm-release-evidence-index.md
docs/release-verifications/aispm-release-evidence-index.json
scripts/validate-aispm-release-evidence-index.py
cavra-aispm-release-evidence-index-packet.json
docs/release-verifications/aispm-report-catalog-readiness.md
docs/release-verifications/aispm-report-catalog-readiness.json
scripts/validate-aispm-report-catalog-readiness.py
cavra-aispm-report-catalog-packet.json
scripts/validate-aispm-report-delivery-setup-readiness.py
docs/release-verifications/aispm-report-delivery-setup-readiness.md
docs/release-verifications/aispm-report-delivery-setup-readiness.json
cavra-aispm-report-delivery-setup-packet.json
docs/release-verifications/aispm-report-operations-readiness.md
docs/release-verifications/aispm-report-operations-readiness.json
scripts/validate-aispm-report-operations-readiness.py
cavra-aispm-report-operations-readiness-packet.json
docs/release-verifications/aispm-report-governance-readiness.md
docs/release-verifications/aispm-report-governance-readiness.json
scripts/validate-aispm-report-governance-readiness.py
cavra-aispm-report-governance-readiness-packet.json
docs/release-verifications/aispm-report-assurance-readiness.md
docs/release-verifications/aispm-report-assurance-readiness.json
scripts/validate-aispm-report-assurance-readiness.py
cavra-aispm-report-assurance-readiness-packet.json
docs/release-verifications/aispm-report-response-readiness.md
docs/release-verifications/aispm-report-response-readiness.json
scripts/validate-aispm-report-response-readiness.py
cavra-aispm-report-response-readiness-packet.json
docs/release-verifications/aispm-report-trial-operations-readiness.md
docs/release-verifications/aispm-report-trial-operations-readiness.json
scripts/validate-aispm-report-trial-operations-readiness.py
cavra-aispm-report-trial-operations-readiness-packet.json
docs/release-verifications/aispm-pilot-control-readiness.md
docs/release-verifications/aispm-pilot-control-readiness.json
scripts/validate-aispm-pilot-control-readiness.py
cavra-aispm-pilot-control-readiness-packet.json
docs/release-verifications/aispm-final-announcement-readiness.md
docs/release-verifications/aispm-final-announcement-readiness.json
scripts/validate-aispm-final-announcement-readiness.py
cavra-aispm-final-announcement-readiness-packet.json
docs/releases/community-v0.1.0.md
docs/release-verifications/community-v0.1.0-post-release-verification.md
Community-GA-v0.1.0-Release-Notes.md
Community-GA-v0.1.0-Post-Release-Verification.md
docs/releases/community-v0.1.1.md
docs/release-verifications/community-v0.1.1-maintenance-verification.md
Community-v0.1.1-Release-Notes.md
Community-v0.1.1-Maintenance-Verification.md
docs/releases/community-v0.1.2.md
docs/release-verifications/community-v0.1.2-maintenance-verification.md
Community-v0.1.2-Release-Notes.md
Community-v0.1.2-Maintenance-Verification.md
docs/releases/community-v0.1.3.md
docs/release-verifications/community-v0.1.3-maintenance-verification.md
Community-v0.1.3-Release-Notes.md
Community-v0.1.3-Maintenance-Verification.md
docs/releases/community-v1.0.0-aispm.md
docs/release-verifications/community-v1.0.0-aispm-public-release-verification.md
Community-v1.0.0-aispm-Release-Notes.md
Community-v1.0.0-aispm-Public-Release-Verification.md
docs/releases/community-v1.0.0-rc.1.md
docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md
Community-v1.0.0-rc.1-Release-Notes.md
Community-v1.0.0-rc.1-Publication-Verification.md
docs/releases/community-v1.0.0.md
docs/release-verifications/community-v1.0.0-publication-readiness.md
Community-v1.0.0-Release-Notes.md
Community-v1.0.0-Publication-Verification.md
Community-Release-Index.md
Community-Release-Readiness-Dashboard.md
Console-Closeout-Operator-Experience.md
Community-GA-User-Verifiable-Path.md
Production-Deployment-Guide-Validation.md
Go-Enforcement-Production-Hardening.md
Enterprise-Integration-Validation.md
Production-Readiness-Procurement-Closeout.md
Community-v1.0.0-Stabilization-Plan.md
Community-v1.0.0-Release-Candidate-Hardening.md
Community-v1.0.0-Release-Candidate-Publication.md
Community-v1.0.0-rc.1-Publication-Verification.md
Community-v1.0.0-rc.1-Post-Publication-Verification.md
Community-v1.0.0-GA-Readiness.md
Community-v1.0.0-GA-Publication-Package.md
Community-v1.0.0-Publication-Verification.md
Community-v1.0.0-Post-Publication-Verification.md
Community-Release-Keyless-Attestation.md
Community-GA-Release-Checklist.md
Community-GA-Release-Packet-Template.md
Community-GA-Release-Packet-Validation.md
Community-GA-Dry-Run-Release-Packet.md
Community-GA-v0.1.0-Release-Packet.md
Community-GA-v0.1.0-Release-Publication.md
Community-Maintenance-Release-Checklist.md
Community-Maintenance-Release-Evidence-Template.md
Community-Release-Note-Freshness.md
Community-v0.1.1-Post-Release-Verification.md
Community-v0.1.2-Readiness.md
Community-v0.1.2-Post-Release-Verification.md
Community-Release-Index-Freshness.md
Community-Release-Readiness-Dashboard-Validation.md
Community-v0.1.3-Maintenance-Planning.md
Community-v0.1.3-Post-Release-Verification.md
npm run validate:sandbox:visual
scripts/validate-sandbox-visual.mjs
-->
