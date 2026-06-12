# AISPM Launch Board Pack Artifact Index

This page mirrors the public-safe launch board pack artifact index for wiki
readers.

## Public Artifacts

- `cavra-aispm-pilot-launch-board-pack-packet.json`
- `cavra-aispm-pilot-launch-decision-packet.json`
- `cavra-aispm-pilot-evidence-room-packet.json`
- `cavra-aispm-pilot-risk-acceptance-packet.json`
- `cavra-aispm-pilot-exception-register-packet.json`
- `cavra-aispm-evidence-reviewer-checklist-packet.json`
- `cavra-aispm-executive-risk-brief.md`
- `cavra-aispm-board-kpi-pack.json`
- `cavra-aispm-soc2-audit-summary.md`

## Validation

The repository artifact index lives at
`docs/release-verifications/aispm-launch-board-pack-artifact-index.json`.
Freshness is validated by:

```bash
python scripts/validate-aispm-launch-artifacts.py
npm run validate:sandbox:visual
python scripts/validate-aispm-visual-freshness.py
```

The visual smoke run captures public-safe screenshots under
`.cavra/visual-smoke/` for the dashboard, AISPM route, board-pack panel, report
center panel, and mobile AISPM route. The browser validator implementation is
`scripts/validate-sandbox-visual.mjs`.

The visual freshness gate is backed by
`docs/release-verifications/aispm-visual-smoke-validation.json` and keeps the
Pilot Launch Board Pack Packet, CSO Report Center, command palette, package
script, and CI workflow references aligned.

## Enterprise Boundary

Signed board approval, board minutes, PDF generation, scheduled delivery,
recipient allowlists, email delivery audit, and tenant artifact retention remain
CAVRA Enterprise or SaaS capabilities.
