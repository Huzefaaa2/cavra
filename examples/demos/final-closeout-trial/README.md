# Final Closeout Trial Demo

This demo folder contains public-safe onboarding assets for CAVRA final closeout trials.

## Files

- `sample-evidence-package.json`: synthetic evidence package for the final closeout workflow.
- `pilot-intake-template.json`: synthetic public-safe pilot intake template for converting trial findings into a scoped production pilot.

## How To Use

1. Review `docs/enterprise/final-closeout-trial-walkthrough.md`.
2. Open `sample-evidence-package.json`.
3. Compare the sample with `docs/release-governance-final-closeout-release-criteria.md`.
4. Use `docs/enterprise/final-closeout-sales-engineering-demo.md` to guide the customer conversation.
5. Use `pilot-intake-template.json` with `docs/enterprise/final-closeout-production-pilot-intake.md` to scope the next production pilot.
6. Open the hosted Evidence Console to review the same intake template as readiness cards, checklist items, and Enterprise/SaaS handoff links.
7. In a self-hosted demo with the CAVRA API configured, save the intake snapshot through `POST /pilot-intakes`.

## Boundary

This demo includes synthetic metadata only. Do not add production customer records, connector credentials, signing keys, license secrets, archive mutation logic, or Enterprise source code to this folder.
