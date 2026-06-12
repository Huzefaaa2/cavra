# Hosted Sandbox Pages Smoke Validation

Generated: 2026-06-12

Status: workflow_enforced

This public-safe validation record covers post-deploy browser validation for the
hosted CAVRA GitHub Pages portal at `https://huzefaaa2.github.io/cavra/`.

## Command

```bash
npm run validate:sandbox:hosted
```

The browser validator implementation is
`scripts/validate-hosted-sandbox-pages.mjs`.

## Coverage

- Hosted index HTTP fetch.
- Hosted JavaScript, CSS, and config assets.
- Hosted CAVRA brand assets.
- Hosted C4 container diagram asset.
- Hosted public-safe evidence samples.
- Browser render for `#dashboard`.
- Browser render for `#ai-posture`.
- Command palette discovery for `Pilot Launch Board Pack Packet`.
- AISPM board pack panel render.
- AISPM CSO report center render.
- AISPM report delivery setup readiness marker.
- AISPM report operations readiness marker.
- AISPM report governance readiness marker.

## Workflow Enforcement

The hosted smoke validator runs in `.github/workflows/deploy-sandbox.yml` after
GitHub Pages deploys from `main`. It uses `CAVRA_SANDBOX_URL` from the Pages
deployment output and writes screenshots to `.cavra/hosted-smoke/`.

## Public-Safety Boundary

Hosted Pages validation checks only public Community Edition static assets,
sample evidence, and public-safe AISPM demo surfaces after GitHub Pages
deployment. Authenticated tenant dashboards, private trial package validation,
licensed report delivery, report operations governance, and report delivery
governance remain CAVRA Enterprise or SaaS concerns.
