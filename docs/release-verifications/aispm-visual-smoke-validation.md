# AISPM Visual Smoke Validation

This public-safe validation record covers desktop and mobile browser rendering
for the CAVRA sandbox portal and AISPM dashboard.

## Command

```bash
npm run validate:sandbox:visual
python scripts/validate-aispm-visual-freshness.py
```

The browser validator implementation is
`scripts/validate-sandbox-visual.mjs`.

## Coverage

- Dashboard desktop view in Classic theme.
- AISPM desktop view in Sentinel theme.
- AISPM mobile view.
- AISPM Pilot Launch Board Pack panel.
- AISPM CSO Report Center panel.
- Command palette discovery for `Pilot Launch Board Pack Packet`.
- Theme readability for Sentinel, Classic, Retro, and Executive.

## Freshness Gate

`scripts/validate-aispm-visual-freshness.py` verifies that this visual smoke
record, `docs/release-verifications/aispm-launch-board-pack-artifact-index.json`,
the board-pack wiki page, sandbox portal docs, package scripts, and GitHub
workflows all reference the same visual validation command and public-safe
artifact coverage.

## Local Screenshots

The validator writes screenshots to `.cavra/visual-smoke/`:

- `dashboard-desktop-classic.png`
- `aispm-desktop-sentinel.png`
- `aispm-board-pack-panel.png`
- `aispm-report-center-panel.png`
- `aispm-mobile-sentinel.png`

`.cavra/` is ignored, so screenshots remain local public-safe validation
evidence instead of release artifacts committed to the repository.

## Public-Safety Boundary

The visual smoke run uses public-safe static sample/local metadata. Private
customer screenshots, tenant visual baselines, and signed visual regression
approval remain CAVRA Enterprise or SaaS capabilities.
