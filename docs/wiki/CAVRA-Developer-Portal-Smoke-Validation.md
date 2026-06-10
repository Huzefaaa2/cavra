# CAVRA Developer Portal Smoke Validation

The sandbox portal smoke validator protects the public GitHub Pages experience
as a user-facing product surface. It verifies that the static portal still
contains the required routes, command palette, mobile navigation, architecture
workbench, compliance filters, brand assets, and deployment workflow checks.

## Validation Command

Run the validator from the repository root:

```bash
python scripts/validate-sandbox-portal.py
```

Expected success output:

```text
CAVRA sandbox portal smoke validation passed.
```

## What It Checks

- Required portal files and brand assets exist.
- Required routes are present: dashboard, AI Posture, architecture, policy
  engine, evidence, integrations, compliance, use cases, documentation, and
  roadmap.
- The command palette includes page, policy, integration, control, and use-case
  search content, plus AI Posture entries for agent observability, kill switch,
  evidence confidence, trace replay, approval lineage, behavior
  fingerprinting, policy context gaps, pre-action risk forecasts, intent-to-action drift, tool-chain risk graphing, agent blast-radius mapping, control coverage heatmap views, and replay-to-policy draft and test fixture previews.
- Theme selectors remain available on desktop and mobile for Sentinel, Classic,
  Retro, and Executive dashboard themes.
- Mobile drawer and bottom navigation anchors remain available.
- Architecture nodes remain visible for GitHub, GitLab, IaC, Kubernetes,
  CAVRA, Policy Engine, Evidence Engine, Audit Trail, and cloud providers.
- AI Posture DOM anchors remain available for provenance, overview cards,
  agent coverage, findings, control coverage, near misses, timeline, trace
  replay drill-down, approval lineage, behavior fingerprinting, pre-action
  risk forecasts, intent-to-action drift, tool-chain risk graph, agent blast-radius map, control coverage heatmap, replay-to-policy draft, replay-to-policy test fixtures, payload,
  `/aispm/posture`, `/aispm/trace-replay`, `/aispm/replay-to-policy-draft`, `/aispm/replay-to-policy-tests`, `/aispm/approval-lineage`, and
  `/aispm/behavior-fingerprints` plus `/aispm/policy-context-gaps` and
  `/aispm/pre-action-risk-forecasts`, `/aispm/intent-action-drift`, `/aispm/tool-chain-graph`, and
  `/aispm/agent-blast-radius`, and `/aispm/control-coverage-heatmap` fallback loading.
- Compliance filters still include NIST, SOC2, ISO27001, CIS, PCI DSS, and
  OWASP.
- The GitHub Pages workflow still smoke-tests the page, JavaScript, stylesheet,
  brand assets, C4 diagram, and evidence JSON.
- README and wiki navigation link to the portal documentation.

## CI Enforcement

The validator is enforced by:

- `.github/workflows/community-ci.yml`
- `.github/workflows/security-scan.yml`
- `.github/workflows/release-community.yml`
- `.github/workflows/cavra-governance.yml`
- `.github/workflows/deploy-sandbox.yml`

## Public Boundary

This validator only checks public Community Edition portal contracts. It does
not require Enterprise source code, private policy packs, SaaS backend logic,
license-service internals, customer data, provider credentials, or private
registry paths.

## User Stories

- As a CISO, I can trust that the public portal still explains CAVRA's control
  model clearly before a release.
- As an auditor, I can inspect a stable compliance and evidence navigation
  surface without needing private systems.
- As a platform engineer, I can catch broken route, asset, and workflow
  regressions before GitHub Pages deployment.
- As a buyer evaluating CAVRA, I can see a coherent public product experience
  with architecture, policies, integrations, compliance, and documentation in
  one place.

## Enterprise Challenge Solved

Enterprise AI governance tools are often evaluated through public demos before
security teams grant deeper access. This validator keeps the public portal
credible by ensuring the most important buyer, auditor, and operator surfaces do
not silently regress.

## Next Recommendation

Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
