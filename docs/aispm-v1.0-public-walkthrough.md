# CAVRA AISPM v1.0 Public Walkthrough

This walkthrough is the public-safe evaluator path for the Community AISPM
dashboard. It is designed for developers, platform engineers, security teams,
auditors, and CSO/CISO reviewers who want to understand what CAVRA shows before
Enterprise live ingestion is connected.

## 1. Open The Portal

Open:

```text
https://huzefaaa2.github.io/cavra/#dashboard
```

Confirm the page shows CAVRA branding, the dashboard route, command palette,
theme selector, documentation links, GitHub link, trial link, demo link, and
download link.

## 2. Review AISPM

Open `AI Posture`.

Review:

- agent inventory and posture cards;
- policy decisions and violation queue;
- trace replay and execution timeline;
- approval lineage;
- evidence confidence and freshness;
- policy context gaps;
- pre-action risk forecasts;
- intent-to-action drift;
- tool-chain graph;
- blast-radius view;
- control coverage heatmap.

Every Community view must be marked as sample, local, or public-safe. Live
tenant ingestion, raw prompts, reasoning, private telemetry, and customer
records remain Enterprise-only.

## 3. Export Community Reports

Open the CSO Report Center and download the public-safe reports:

- executive risk brief;
- board KPI pack;
- SOC 2-style audit summary;
- control coverage CSV;
- evidence freshness CSV;
- agent risk register.

Enterprise-only report delivery, PDF generation, email delivery, signed
packages, recipient governance, and evidence rooms are represented as
public-safe contracts and readiness gates only.

## 4. Review Trial And Pilot Evidence

Review the AISPM trial and pilot panels:

- Enterprise Trial Readiness Checklist;
- Evaluator Handoff;
- Trial Journey;
- Trial Closeout Evidence;
- Trial Outcome Summary;
- Pilot Scope;
- Pilot Approval;
- Production Pilot Evidence Room;
- Risk Acceptance;
- Launch Board Pack;
- Pilot Control Readiness.

Use the copy/download packet actions to attach public-safe JSON packets to
review tickets. Do not attach license keys, package tokens, customer data,
private telemetry, raw prompts, model reasoning, private policy packs, or
Enterprise source.

## 5. Validate Locally

For local release verification:

```bash
python scripts/validate-sandbox-portal.py
python scripts/validate-aispm-release-evidence-index.py
python scripts/validate-aispm-launch-readiness.py
python scripts/validate-aispm-pilot-control-readiness.py
npm run validate:sandbox:visual
PYTHONPATH=src pytest -q tests
```

## 6. Release Readiness

The AISPM public release path is ready when:

- the current AISPM work is merged to `main`;
- GitHub Pages deploys the updated portal;
- hosted smoke validation passes;
- post-deploy evidence is generated;
- README, release notes, wiki navigation, and lab notebook links are current;
- the release evidence index and launch readiness rollup pass.

## Public Safety Boundary

This walkthrough covers the public Community Edition and public-safe Enterprise
contracts only. It does not include Enterprise source code, private policy
packs, private container access, license-service internals, private signing
keys, package tokens, customer records, raw prompts, model reasoning, or private
telemetry.
