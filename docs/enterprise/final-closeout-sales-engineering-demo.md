# Final Closeout Sales Engineering Demo Script

This script helps a sales engineer or solution architect present CAVRA final closeout workflows to a customer using public-safe Community Edition assets and synthetic evidence.

## Demo Goal

Show that CAVRA turns AI-agent release activity into governed closeout evidence, then explain how Enterprise or SaaS extends the workflow with private enforcement, organization controls, and commercial support.

## Timing

Recommended length: 30 minutes.

| Segment | Time |
| --- | --- |
| Problem framing | 5 min |
| Evidence walkthrough | 10 min |
| Release criteria review | 5 min |
| Enterprise/SaaS upgrade path | 7 min |
| Questions and next steps | 3 min |

## Talk Track

### 1. Problem Framing

AI coding agents can now modify code, invoke tools, interact with CI/CD, and influence release workflows. The risk is not just unsafe code. The risk is unmanaged authority: actions happen without a consistent approval path, evidence chain, retention model, or audit handoff.

CAVRA acts before the agent acts and then produces evidence that release, security, and audit teams can inspect.

### 2. Evidence Walkthrough

Open `examples/demos/final-closeout-trial/sample-evidence-package.json`.

Point out:

- final readiness evidence,
- external archive signature metadata,
- closed release summary,
- approved retention review,
- downloadable closeout bundle metadata,
- retention health report,
- redacted alert delivery,
- retry plan and dry-run worker evidence.

Emphasize that the public sample is synthetic and safe to share. It proves the evidence chain without exposing Enterprise implementation details.

### 3. Release Criteria Review

Open `docs/release-governance-final-closeout-release-criteria.md`.

Map the sample to the criteria:

- readiness exists,
- closeout is closed,
- retention is approved,
- artifact bundle exists,
- health is reviewed,
- failed delivery has retry evidence.

Classify the sample as `ready_with_accepted_risk` because one delivery failure is intentionally simulated and has a documented retry plan.

### 4. Upgrade Path

Explain the edition boundary:

- Community proves the governance model, CLI/API shape, evidence schema, and public plugin interface.
- Trial provides private binary, Docker image, or SaaS access for evaluation under a commercial process.
- Enterprise adds SSO/RBAC, authenticated connectors, private policy packs, organization dashboards, compliance evidence reports, drift monitoring, AI remediation, and managed support.
- SaaS adds tenant management, policy registry, audit store, billing, license service, and hosted dashboards.

### 5. Discovery Questions

- Which AI coding agents and CI/CD systems are in scope?
- Which release gates need CAVRA evidence?
- Which connector destinations are required for alerts and closeout records?
- Which approver groups own retention exceptions and live retries?
- Is the preferred deployment self-hosted Enterprise, SaaS, or hybrid?
- Which compliance reports are most important for the first pilot?

## Demo Do And Do Not

Do:

- Use synthetic sample evidence.
- Keep the demo focused on governance, release evidence, and upgrade path.
- Be explicit about the open-core boundary.
- Capture integration and pilot requirements.

Do not:

- Use production customer data.
- Show private source code.
- Invent license keys.
- Claim Community performs private archive mutation or live credentialed connector execution.
- Commit customer-specific templates or connector credentials to the public repository.

## Recommended Next Step After Demo

Create a production pilot plan that identifies the customer repositories, AI agents, CI/CD systems, connector destinations, retention requirements, and Enterprise/SaaS controls needed for rollout.

Use [final-closeout-production-pilot-intake.md](final-closeout-production-pilot-intake.md), [final-closeout-pilot-readiness-checklists.md](final-closeout-pilot-readiness-checklists.md), [final-closeout-enterprise-saas-handoff.md](final-closeout-enterprise-saas-handoff.md), and `examples/demos/final-closeout-trial/pilot-intake-template.json` to capture the next-step pilot package.
