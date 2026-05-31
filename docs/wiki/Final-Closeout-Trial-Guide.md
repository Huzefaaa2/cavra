# Final Closeout Trial Guide

This guide explains how a customer trial should evaluate CAVRA final closeout workflows without exposing Enterprise source code or private license-server logic.

## Trial Objective

The trial proves that CAVRA can create a public-safe final closeout evidence chain and show where Enterprise or SaaS features add private enforcement.

## Customer Walkthrough

1. Start the Community API and Evidence Console.
2. Generate final readiness evidence.
3. Create a signed archive manifest using external signature metadata.
4. Generate and deliver a final closeout summary.
5. Request and approve closeout retention.
6. Build the closeout artifact bundle.
7. Run closeout retention health.
8. Send a retention health alert through a non-production connector.
9. Create a retry plan for a simulated failed closeout delivery.
10. Run the retry worker in dry-run mode.
11. Review release criteria and decide whether the trial passes.

## What Community Demonstrates

- Public-safe evidence metadata
- Evidence Console visibility
- Redacted connector delivery records
- Retention approval and health metadata
- Retry planning and dry-run worker evidence
- Open-core boundaries

## What Enterprise Or SaaS Adds

- License validation
- Tenant management
- Organization dashboards
- SSO and RBAC
- Authenticated live connector execution
- Private archive mutation and retention enforcement
- Compliance evidence exports
- Paid policy packs

## Security Notes

Use non-production connectors and synthetic evidence. Do not use production customer tickets, archive paths, private policy packs, license keys, or secrets in Community trial walkthroughs.

## Onboarding Assets

- Final Closeout Trial Walkthrough: `Final-Closeout-Trial-Walkthrough.md`
- Final Closeout Trial Sample Evidence: `Final-Closeout-Trial-Sample-Evidence.md`
- Final Closeout Sales Engineering Demo: `Final-Closeout-Sales-Engineering-Demo.md`
- Final Closeout Production Pilot Intake: `Final-Closeout-Production-Pilot-Intake.md`
- Final Closeout Pilot Readiness Checklists: `Final-Closeout-Pilot-Readiness-Checklists.md`
- Final Closeout Enterprise And SaaS Handoff: `Final-Closeout-Enterprise-And-SaaS-Handoff.md`
- Synthetic sample evidence package: `examples/demos/final-closeout-trial/sample-evidence-package.json`
- Synthetic pilot intake template: `examples/demos/final-closeout-trial/pilot-intake-template.json`
