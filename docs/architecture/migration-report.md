# Open-Core Migration Report

Date: 2026-05-19

## Files Reviewed

Reviewed repository root metadata, `src/cavra`, `policies`, `docs`, `examples`,
`.github`, `apps`, `go`, `scripts`, and `tests` using targeted boundary scans
for private-key, license-server, customer, confidential, and Enterprise package
terms.

## Safe For Community

- Runtime guard and policy engine interfaces.
- CLI, API, MCP server, evidence bundle formats, and public connector hooks.
- Community starter policies under `policies/community`.
- Public diagrams, quickstarts, and deployment examples.
- Public plugin runtime, edition hooks, and licensing abstractions.

## May Need Enterprise Migration

The current repository includes policy packs with regulated or Enterprise-style
names, such as PCI DSS, HIPAA, SOX, ISO 27001, EU AI Act, GitHub Enterprise,
GitLab Enterprise, MCP Enterprise, banking, Kubernetes production, and cloud
IAM. They appear to be public reference/starter policies today, not private
customer material. As commercialization matures, decide which remain Community
reference packs and which become paid private policy packs.

Examples with Enterprise names should be reviewed before public release copy is
finalized. Public workflows must not build or publish private Enterprise
artifacts.

## Risky Items Found

No real Enterprise signing keys, Stripe secrets, customer secrets, license
server private keys, private customer templates, or Enterprise source paths were
found in public source paths.

Boundary scan did find expected public mentions of secrets and private keys in
security documentation, tests, and examples. These are educational placeholders
and not production credentials.

## Recommended Private Repo

`Huzefaaa2/cavra-enterprise`

## Recommended Split

Public:

- Community core;
- public docs;
- safe plugin interfaces;
- trial installation instructions;
- feature comparison and Enterprise marketing docs.

Private:

- Enterprise package `cavra_enterprise`;
- premium policy packs;
- SaaS backend;
- license server client and service;
- commercial dashboards;
- enterprise Docker images and Helm charts.

## Next Engineering Actions

1. Create private `cavra-enterprise` repository.
2. Move future paid modules and paid policy packs there.
3. Keep public interfaces stable and test Enterprise absence in Community mode.
4. Add endpoint remediation SLA breach, escalation, and executive release governance reporting.
