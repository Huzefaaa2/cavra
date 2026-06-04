# CAVRA Developer Portal Redesign

The GitHub Pages sandbox has been redesigned from a single long-scroll page into
a Backstage-style developer portal experience for CAVRA: Continuous AI
Validation, Risk & Audit.

## Delivered Static Portal

The current public site remains static-hostable on GitHub Pages through
`apps/sandbox-ui` and `.github/workflows/deploy-sandbox.yml`.

Delivered UX:

- sticky top header with logo, search, docs, demo, GitHub, download, theme, and
  version controls;
- persistent left navigation with grouped portal sections;
- center content panels that switch without page reloads;
- sticky right table of contents on desktop;
- mobile drawer navigation and bottom navigation;
- command palette with `Ctrl+K` search;
- interactive architecture explorer with clickable nodes and an inspector
  panel;
- policy, evidence, integrations, compliance, use-case, documentation, and
  roadmap pages;
- dark-mode-first enterprise security visual design with accessible focus
  states and reduced scrolling.

## Target Next.js Architecture

The static portal can later move to a Next.js app using `app/` routes,
TypeScript content contracts, Tailwind CSS, shadcn/ui primitives, Framer Motion
animations, and Lucide Icons while preserving the same route model and GitHub
Pages static export behavior.

## Boundary Notice

The portal is public Community Edition documentation and demo UX only. It does
not include Enterprise source code, private policy packs, SaaS backend
implementation, license-service internals, customer data, private keys, or
private registry details.

## Next Recommendation

Convert Community v0.1.2 dry-run into an official maintenance release after maintainer approval and artifact publication.
