# Release Documentation Policy

CAVRA documentation is part of the product, not a follow-up task. Every release must leave the repository and wiki in a state that a developer, platform engineer, CISO, and auditor can understand.

Transparent agent-driven releases must follow the same rule. The `docs-agent` and `release-agent` roles may prepare documentation and release artifacts, but a human maintainer must approve protected branch merges, public release publication, package publishing, and any legal, licensing, pricing, or compliance claim.

## Required Updates Per Release

- README feature summary and usage.
- Productization report release section.
- Current feature inventory.
- User stories for new capabilities.
- Enterprise challenge mapping.
- CLI/API docs for new commands or endpoints.
- Policy schema docs for policy changes.
- Evidence format docs for evidence changes.
- Wiki pages for buyer-facing and operator-facing changes.
- Diagrams when architecture, user journey, evidence lifecycle, or deployment changes.
- Transparent agent manifests and methodology docs when agent responsibilities, GitHub App permissions, branch naming, approval gates, or evidence requirements change.

## Diagram Quality Standard

Diagrams must be:

- Branded as CAVRA.
- Understandable without reading source code.
- Useful to at least one target audience: developer, CISO, platform engineer, auditor, or AI governance lead.
- Stored as source-friendly Mermaid markdown when possible.
- Exported or recreated as SVG for user-friendly rendering when a diagram is central to the product story.

## Release Checklist

Before merging a release PR:

- [ ] Tests pass.
- [ ] Docker validation passes when relevant.
- [ ] README updated.
- [ ] Wiki-ready docs updated.
- [ ] GitHub Wiki pushed when relevant.
- [ ] Diagrams updated when relevant.
- [ ] Productization report updated.
- [ ] Transparent agent manifests, methodology, and orchestration docs updated when relevant.
- [ ] Next recommended phase documented.
