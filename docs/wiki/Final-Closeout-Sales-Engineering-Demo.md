# Final Closeout Sales Engineering Demo

This script helps a sales engineer or solution architect present CAVRA final closeout workflows using public-safe Community Edition assets and synthetic evidence.

## Demo Goal

Show that CAVRA turns AI-agent release activity into governed closeout evidence, then explain how Enterprise or SaaS extends the workflow with private enforcement, organization controls, and commercial support.

## Demo Structure

| Segment | Time |
| --- | --- |
| Problem framing | 5 min |
| Evidence walkthrough | 10 min |
| Release criteria review | 5 min |
| Enterprise/SaaS upgrade path | 7 min |
| Questions and next steps | 3 min |

## Talk Track

AI coding agents can modify code, invoke tools, interact with CI/CD, and influence release workflows. The risk is unmanaged authority: actions happen without a consistent approval path, evidence chain, retention model, or audit handoff.

Open `examples/demos/final-closeout-trial/sample-evidence-package.json` and point out final readiness evidence, external archive signature metadata, closed release summary, approved retention review, artifact bundle metadata, retention health, redacted alert delivery, retry plan, and dry-run worker evidence.

Map the sample to `Release-Governance-Final-Closeout-Release-Criteria.md` and classify it as `ready_with_accepted_risk` because one delivery failure is intentionally simulated and has a documented retry plan.

## Upgrade Path

- Community proves the governance model, CLI/API shape, evidence schema, and public plugin interface.
- Trial provides private binary, Docker image, or SaaS access for evaluation under a commercial process.
- Enterprise adds SSO/RBAC, authenticated connectors, private policy packs, organization dashboards, compliance evidence reports, drift monitoring, AI remediation, and managed support.
- SaaS adds tenant management, policy registry, audit store, billing, license service, and hosted dashboards.

## Demo Guardrails

- Use synthetic sample evidence.
- Do not use production customer data.
- Do not show private source code.
- Do not invent license keys.
- Do not claim Community performs private archive mutation or live credentialed connector execution.

