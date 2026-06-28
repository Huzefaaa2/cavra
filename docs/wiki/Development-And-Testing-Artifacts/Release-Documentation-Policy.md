# Release Documentation Policy

CAVRA documentation is part of the release.

Every release must update:

- README.
- Productization report.
- Current feature inventory.
- Relevant docs under `docs/`.
- Relevant wiki pages.
- Diagrams when architecture, workflows, evidence, deployment, or user journeys change.

## Diagram Standard

Diagrams must be:

- Branded as CAVRA.
- Useful to developers, CISOs, platform engineers, auditors, or AI governance leads.
- Stored as Mermaid source where useful.
- Exported or recreated as SVG for user-facing diagrams.

## Release Checklist

- [ ] Tests pass.
- [ ] Docker validation passes where relevant.
- [ ] README updated.
- [ ] Wiki updated.
- [ ] Diagrams updated.
- [ ] Productization report updated.
- [ ] Next recommended phase documented.

Community GA releases must also follow the
[Community GA release checklist](Community-GA-Release-Checklist.md), including
public boundary validation, Ed25519 policy signing, runtime mode checks, golden
decision snapshots, Evidence Console smoke validation, deployment readiness, Go
runtime readiness or explicit disabled status, and live wiki synchronization.
They must also produce a public-safe Community GA release packet in Markdown and
JSON form so the release decision, gate evidence, accepted risks, boundary
review, and wiki sync commit can be verified later.
