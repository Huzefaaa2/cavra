# CAVRA Community AISPM v1.0 Release Notes

CAVRA Community AISPM v1.0 adds a public-safe AI Security Posture Management
dashboard to the CAVRA Community portal. It gives teams a concrete way to see
how CAVRA can govern AI coding agents before they touch files, commands, Git,
CI/CD, MCP tools, policy, evidence, or release workflows.

GitHub Release:
<https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-aispm>

## What Changed

- Added the public AISPM dashboard route with CAVRA branding, command palette
  navigation, responsive layout, and Sentinel, Classic, Retro, and Executive
  themes.
- Added Community-safe posture views for agent inventory, policy decisions,
  risk findings, timelines, trace replay, approval lineage, control coverage,
  near misses, evidence confidence, evidence freshness, behavior fingerprints,
  policy context gaps, pre-action risk forecasts, intent drift, tool-chain
  graphing, and agent blast radius.
- Added the CSO Report Center with Community-downloadable executive, audit,
  control, evidence, and agent-risk reports.
- Added public-safe Enterprise report readiness contracts for delivery setup,
  operations, governance, assurance, response, trial operations, and pilot
  controls.
- Added Enterprise Trial evaluator, closeout, procurement, pilot approval,
  evidence room, board pack, and pilot control readiness packets.
- Added release evidence index, launch readiness rollup, hosted Pages smoke,
  post-deploy evidence, and lab notebook publication readiness gates.
- Added public-safe lab notebook screenshots and an AISPM trial evaluation flow
  diagram.

## Public Portal

Open:

```text
https://huzefaaa2.github.io/cavra/#ai-posture
```

The Community portal uses sample or local public-safe data. Live multi-tenant
ingestion, authenticated dashboards, signed approvals, private policy packs,
tenant telemetry, private package access, and Enterprise report delivery remain
Enterprise-only.

## Validation

Primary validation commands:

```bash
python scripts/validate-sandbox-portal.py
python scripts/validate-aispm-release-evidence-index.py
python scripts/validate-aispm-launch-readiness.py
python scripts/validate-aispm-pilot-control-readiness.py
npm run validate:sandbox:visual
PYTHONPATH=src pytest -q tests
```

## Documentation

- Public walkthrough: `docs/aispm-v1.0-public-walkthrough.md`
- Release readiness: `docs/release-verifications/aispm-v1.0-public-release-readiness.md`
- Release verification:
  `docs/release-verifications/community-v1.0.0-aispm-public-release-verification.md`
- Release readiness packet:
  `docs/release-verifications/aispm-v1.0-public-release-readiness.json`
- Lab notebook: `docs/wiki/AISPM-Enterprise-Trial-Lab-Notebook.md`
- Release evidence index:
  `docs/release-verifications/aispm-release-evidence-index.md`
- Launch readiness rollup:
  `docs/release-verifications/aispm-launch-readiness-rollup.md`

## Boundary Notice

This AISPM release note covers public Community Edition functionality and
public-safe Enterprise contracts only. Enterprise source code, paid policy
packs, license-service internals, private registry credentials, private signing
keys, customer records, raw prompts, model reasoning, raw tool output, and
tenant telemetry are not part of this public release.

## Announcement Copy

CAVRA Community AISPM v1.0 is ready for public evaluation as a static,
public-safe dashboard for AI coding agent governance. It demonstrates how CAVRA
turns agent actions, policy decisions, evidence confidence, report readiness,
trial handoff, and pilot controls into an auditable operating surface for
developers, platform teams, security teams, auditors, and CSO/CISO reviewers.
