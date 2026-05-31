# Final Closeout Trial Guide

This guide explains how a customer trial should evaluate CAVRA final closeout workflows without exposing Enterprise source code or private license-server logic.

## Trial Objective

The trial should prove that CAVRA can create a public-safe final closeout evidence chain and show where Enterprise or SaaS features add private enforcement.

The customer should be able to evaluate:

- closeout readiness and blocker visibility,
- externally signed archive manifest metadata,
- final closeout summary delivery,
- retention review approval,
- downloadable artifact bundle metadata,
- closeout retention health findings,
- retention health alert routing,
- failed closeout delivery retry planning,
- clear Community versus Enterprise boundaries.

## Trial Distribution

Trial access should be provided through one of these paths:

- private Docker image,
- compiled binary,
- hosted SaaS trial tenant.

The public repository may document trial usage, but it must not include trial source code, private policy packs, license validation secrets, commercial templates, or customer-specific material.

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
- API workflow shape
- Redacted connector delivery records
- Retention approval and health metadata
- Retry planning and dry-run worker evidence
- Documentation for open-core boundaries

## What Enterprise Or SaaS Adds

- License validation
- Tenant management
- Organization dashboards
- SSO and RBAC
- Authenticated live connector execution
- Private archive mutation and retention enforcement
- Compliance evidence exports
- Paid policy packs
- Customer-specific templates and workflows

## Trial Success Criteria

The trial is successful when:

- the customer can run the final closeout flow end to end,
- the customer understands the evidence chain,
- redacted delivery and retry metadata are visible,
- retention health findings are understandable,
- the customer understands what must move to Enterprise or SaaS for production use,
- no Enterprise source, private keys, connector secrets, or customer data are committed to the public repository.

## Security Notes

Use non-production connectors and synthetic evidence for public demos. Do not use production customer tickets, archive paths, private policy packs, license keys, or secrets in Community trial walkthroughs.

## Related Documentation

- [Release Governance Final Closeout Operator Guide](../release-governance-final-closeout-operator-guide.md)
- [Release Governance Final Closeout Release Criteria](../release-governance-final-closeout-release-criteria.md)
- [Final Closeout Trial Walkthrough](final-closeout-trial-walkthrough.md)
- [Final Closeout Trial Sample Evidence](final-closeout-trial-sample-evidence.md)
- [Final Closeout Sales Engineering Demo Script](final-closeout-sales-engineering-demo.md)
- [Synthetic Sample Evidence Package](../../examples/demos/final-closeout-trial/sample-evidence-package.json)
- [Enterprise Trial](trial.md)
- [Open-Core Model](../architecture/open-core-model.md)
