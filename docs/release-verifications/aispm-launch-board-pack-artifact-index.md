# AISPM Launch Board Pack Artifact Index

This public-safe index records the artifacts that must remain aligned for the
AISPM Pilot Launch Board Pack in the Community portal.

## Scope

- Portal route: `apps/sandbox-ui/index.html#ai-posture`
- Downloadable packet: `cavra-aispm-pilot-launch-board-pack-packet.json`
- Freshness validator: `scripts/validate-aispm-launch-artifacts.py`
- Visual freshness validator: `scripts/validate-aispm-visual-freshness.py`
- Visual smoke script: `scripts/validate-sandbox-visual.mjs`
- Visual smoke record: `docs/release-verifications/aispm-visual-smoke-validation.json`
- Artifact index: `docs/release-verifications/aispm-launch-board-pack-artifact-index.json`

## Required Artifacts

| Artifact | Source panel | Purpose |
| --- | --- | --- |
| `cavra-aispm-pilot-launch-decision-packet.json` | AISPM Pilot Launch Readiness Summary | CSO/CISO launch candidate review |
| `cavra-aispm-pilot-evidence-room-packet.json` | Production Pilot Evidence Room | Role-based reviewer evidence catalog |
| `cavra-aispm-pilot-risk-acceptance-packet.json` | Pilot Risk Acceptance Summary | Residual risk and launch-blocker disposition |
| `cavra-aispm-pilot-exception-register-packet.json` | Pilot Exception Register | Exception owner and expiry review |
| `cavra-aispm-evidence-reviewer-checklist-packet.json` | Evidence Room Reviewer Checklist | Role-specific pre-pilot acceptance criteria |
| `cavra-aispm-executive-risk-brief.md` | CSO Report Center | Executive risk briefing |
| `cavra-aispm-board-kpi-pack.json` | CSO Report Center | Board KPI evidence |
| `cavra-aispm-soc2-audit-summary.md` | CSO Report Center | Audit summary evidence |

## Public-Safety Boundary

The board pack export is a Community artifact index only. It excludes signed
board approval, board minutes, email recipients, private telemetry, customer
identity records, license keys, Enterprise source code, delivery workflow
state, and tenant artifact retention data.

## Validation

Run:

```bash
python scripts/validate-aispm-launch-artifacts.py
npm run validate:sandbox:visual
python scripts/validate-aispm-visual-freshness.py
```

The validators check the portal DOM, JavaScript export functions, artifact
filenames, documentation references, wiki references, CI workflow wiring,
desktop/mobile browser rendering, theme readability, command-palette discovery,
board-pack panel layout, and report-center panel layout. Local screenshots are
written to `.cavra/visual-smoke/`.

The Pilot Launch Board Pack Packet visual freshness gate links the board/CISO
artifact index to the visual smoke record so `Pilot Launch Board Pack Packet`,
`CSO Report Center`, command-palette discovery, desktop/mobile rendering, and
theme readability stay synchronized.
