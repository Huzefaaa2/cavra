# Before the Agent Acts: The CAVRA Technical Textbook

Welcome to the CAVRA Wiki. This wiki now opens as a technical textbook for CAVRA, Controlled Agentic Verification and Runtime Authority. It is written for developers, security engineers, platform owners, compliance teams, architects, and enterprise evaluators who need to understand what CAVRA is, how it works, how to run it, and how to operate it safely.

CAVRA exists for a simple reason: AI agents should not receive unchecked authority over code, cloud, data, identity, CI/CD, MCP tools, and production workflows. CAVRA gives organizations a runtime authority layer that evaluates agent actions before they happen, records evidence after they happen, and turns that evidence into AI Security Posture Management, or AISPM.

![CAVRA runtime authority map](assets/textbook/cavra-runtime-authority-map.svg)

## Start Here

Read the book in order if you are new to CAVRA. Jump directly to the command, GUI, AISPM, or deployment chapters if you already know the product shape.

![Five-minute CAVRA journey](assets/textbook/getting-started-journey.svg)

## Five-Minute Quick Start

If you want to see CAVRA work before reading the full book, follow this short path:

1. Install the Community Edition from the repository with `pip install -e .`.
2. Run `cavra version` and `cavra policy list`.
3. Run `cavra demo before-the-agent-acts` to see CAVRA block risky agent behavior.
4. Run `cavra evaluate execute_command "terraform apply -auto-approve" --json` to evaluate a dangerous command directly.
5. Run `cavra evidence bundle --output .cavra/evidence/latest` and `cavra evidence verify .cavra/evidence/latest` to prove the control path.
6. Open the sandbox GUI and review the decision, evidence, and AISPM views.

The detailed walkthrough is in [Install And Deploy CAVRA](Textbook-05-Install-And-Deploy-CAVRA), [Community Edition User Guide](Textbook-06-Community-Edition-User-Guide), and [Use Cases, Labs, And Example Workflows](Textbook-13-Use-Cases-Labs-And-Example-Workflows).

## Learning Paths

| Reader | Read first | Outcome |
| --- | --- | --- |
| First-time user | Chapters 0, 1, 5, 6, 13 | Install, run a demo, block a risky action, and verify evidence. |
| Developer | Chapters 5, 6, 8, 11 | Use the CLI, write policy, route approvals, and create evidence. |
| Security architect | Chapters 1, 2, 3, 11, 14 | Understand the runtime authority model and governance controls. |
| Platform owner | Chapters 3, 5, 8, 12 | Integrate CAVRA into CI/CD, APIs, and operating workflows. |
| Enterprise evaluator | Chapters 4, 7, 10, 12, 13 | Validate SSO/RBAC, connectors, tenant isolation, AISPM, and report delivery. |

## Complete Table Of Contents

1. [Foreword, Preface, And Reader Paths](Textbook-00-Foreword-Preface-And-Reader-Paths)
2. [Why CAVRA Exists](Textbook-01-Why-CAVRA-Exists)
3. [The Runtime Authority Model](Textbook-02-Runtime-Authority-Model)
4. [Architecture And Open-Core Design](Textbook-03-Architecture-And-Open-Core-Design)
5. [Editions, Licensing, And Feature Boundaries](Textbook-04-Editions-Licensing-And-Feature-Boundaries)
6. [Install And Deploy CAVRA](Textbook-05-Install-And-Deploy-CAVRA)
7. [Community Edition User Guide](Textbook-06-Community-Edition-User-Guide)
8. [Enterprise Edition User Guide](Textbook-07-Enterprise-Edition-User-Guide)
9. [CAVRA CLI Command Reference](Textbook-08-CAVRA-CLI-Command-Reference)
10. [CAVRA GUI And Sandbox Guide](Textbook-09-CAVRA-GUI-And-Sandbox-Guide)
11. [AISPM Guide](Textbook-10-AISPM-Guide)
12. [Policies, Approvals, Evidence, And Attestations](Textbook-11-Policies-Approvals-Evidence-And-Attestations)
13. [Operations, Integrations, And Deployment Patterns](Textbook-12-Operations-Integrations-And-Deployment-Patterns)
14. [Use Cases, Labs, And Example Workflows](Textbook-13-Use-Cases-Labs-And-Example-Workflows)
15. [Reference Appendices](Textbook-14-Reference-Appendices)

## Visual Index

| Topic | Diagram |
| --- | --- |
| Runtime authority | [CAVRA runtime authority map](assets/textbook/cavra-runtime-authority-map.svg) |
| Architecture context | [Architecture context](assets/textbook/architecture-context.svg) |
| Runtime decision flow | [Runtime flow](assets/textbook/runtime-flow.svg) |
| Editions | [Edition map](assets/textbook/cavra-edition-map.svg) |
| CLI command families | [Command map](assets/textbook/cavra-command-map.svg) |
| AISPM posture loop | [AISPM posture loop](assets/textbook/aispm-posture-loop.svg) |
| Enterprise sequence | [Enterprise sequence](assets/textbook/cavra-enterprise-sequence.svg) |
| Getting started journey | [Getting started journey](assets/textbook/getting-started-journey.svg) |
| Policy authoring journey | [Policy authoring journey](assets/textbook/policy-authoring-journey.svg) |
| Approval routing | [Approval routing flow](assets/textbook/approval-routing-flow.svg) |
| Troubleshooting | [Troubleshooting decision tree](assets/textbook/troubleshooting-decision-tree.svg) |

## Primary Product References

- [CLI](CLI)
- [API](API)
- [Diagrams](Diagrams)
- [Edition Boundaries](Edition-Boundaries)
- [AI Agent Enforcement And Anti-Bypass Model](AI-Agent-Enforcement-And-Anti-Bypass-Model)
- [Agent Registry And MCP Trust](Agent-Registry-and-MCP-Trust)
- [Approval Workflows](Approval-Workflows)
- [Evidence Hub And Attestation](Evidence-Hub-and-Attestation)
- [Policy Engine Hardening](Policy-Engine-Hardening)
- [AISPM Dashboard Roadmap](AISPM-Dashboard-Roadmap)
- [AI Security Posture Dashboard Contract](AI-Security-Posture-Dashboard-Contract)
- [AISPM CSO Report Center](AISPM-CSO-Report-Center)
- [AISPM Enterprise Live Ingestion](AISPM-Enterprise-Live-Ingestion)
- [CAVRA Trial Field Guide](CAVRA-Trial-Field-Guide.md)
- [AISPM Trial Access And Operator Approval](AISPM-Trial-Access-And-Operator-Approval.md)
- [AISPM Trial Revocation, Expiry, And Closeout](AISPM-Trial-Revocation-Expiry-And-Closeout.md)
- [Enterprise Trial Availability](Enterprise-Trial-Availability)
- [Enterprise Trial Self-Service Access](Enterprise-Trial-Self-Service-Access)

## Development And Testing Archive

Historical implementation notes, release packets, validation records, trial synchronization notes, rollback-drill records, closeout documents, and readiness artifacts are preserved in one archive:

- [Development And Testing Artifacts](Development-And-Testing-Artifacts)

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
