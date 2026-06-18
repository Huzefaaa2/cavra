# AISPM Launch Readiness Rollup

Generated: 2026-06-12

Status: ready

This packet is the public-safe launch readiness rollup for the CAVRA Community
AISPM dashboard release candidate. It ties the public portal contract, board
pack artifact index, visual smoke validation, visual freshness checks, trial lab
notebook readiness, and GitHub Pages workflow validation into one verifier-owned
release evidence path.

## Included Sources

| Source | Status | Evidence | Validator |
| --- | --- | --- | --- |
| Phase B closeout | pass | `docs/aispm-phase-b-closeout-verification.md` | `python scripts/validate-sandbox-portal.py` |
| Board pack artifact index | pass | `docs/release-verifications/aispm-launch-board-pack-artifact-index.json` | `python scripts/validate-aispm-launch-artifacts.py` |
| Visual smoke | pass | `docs/release-verifications/aispm-visual-smoke-validation.json` | `npm run validate:sandbox:visual` |
| Visual freshness | pass | `scripts/validate-aispm-visual-freshness.py` | `python scripts/validate-aispm-visual-freshness.py` |
| Trial lab notebook | ready | `docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json` | `python scripts/validate-aispm-trial-lab-notebook.py --check-summary` |
| GitHub Pages workflow | pass | `.github/workflows/deploy-sandbox.yml` | `python scripts/validate-sandbox-portal.py` |
| Hosted Pages smoke | workflow_enforced | `docs/release-verifications/hosted-sandbox-pages-smoke-validation.json` | `npm run validate:sandbox:hosted` |
| Hosted deployment freshness | ready | `docs/release-verifications/hosted-sandbox-deployment-freshness.json` | `python scripts/validate-hosted-sandbox-deployment-freshness.py` |
| Hosted operator status | ready | `docs/release-verifications/hosted-sandbox-operator-release-status.json` | `python scripts/validate-hosted-sandbox-operator-status.py` |
| Post-deploy evidence | workflow_enforced | `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json` | `python scripts/validate-hosted-sandbox-deploy-evidence.py` |
| Release evidence index | ready | `docs/release-verifications/aispm-release-evidence-index.json` | `python scripts/validate-aispm-release-evidence-index.py` |
| Report catalog readiness | ready | `docs/release-verifications/aispm-report-catalog-readiness.json` | `python scripts/validate-aispm-report-catalog-readiness.py` |
| Report delivery setup readiness | ready | `docs/release-verifications/aispm-report-delivery-setup-readiness.json` | `python scripts/validate-aispm-report-delivery-setup-readiness.py` |
| Report operations readiness | ready | `docs/release-verifications/aispm-report-operations-readiness.json` | `python scripts/validate-aispm-report-operations-readiness.py` |
| Report governance readiness | ready | `docs/release-verifications/aispm-report-governance-readiness.json` | `python scripts/validate-aispm-report-governance-readiness.py` |
| Report assurance readiness | ready | `docs/release-verifications/aispm-report-assurance-readiness.json` | `python scripts/validate-aispm-report-assurance-readiness.py` |
| Report response readiness | ready | `docs/release-verifications/aispm-report-response-readiness.json` | `python scripts/validate-aispm-report-response-readiness.py` |
| Report trial operations readiness | ready | `docs/release-verifications/aispm-report-trial-operations-readiness.json` | `python scripts/validate-aispm-report-trial-operations-readiness.py` |
| Pilot control readiness | ready | `docs/release-verifications/aispm-pilot-control-readiness.json` | `python scripts/validate-aispm-pilot-control-readiness.py` |
| Final announcement readiness | ready | `docs/release-verifications/aispm-final-announcement-readiness.json` | `python scripts/validate-aispm-final-announcement-readiness.py` |

## Readiness Gates

- Public portal contract is validated by `scripts/validate-sandbox-portal.py`.
- Board pack artifact freshness is validated by
  `scripts/validate-aispm-launch-artifacts.py`.
- Visual smoke and theme readability are validated by
  `npm run validate:sandbox:visual` and recorded in
  `docs/release-verifications/aispm-visual-smoke-validation.json`.
- Visual smoke freshness is validated by
  `scripts/validate-aispm-visual-freshness.py`.
- Trial lab notebook publication readiness is validated by
  `scripts/validate-aispm-trial-lab-notebook.py --check-summary`.
- The rollup itself is validated by
  `scripts/validate-aispm-launch-readiness.py`.
- Hosted GitHub Pages browser smoke is validated after deployment by
  `npm run validate:sandbox:hosted`, implemented by
  `scripts/validate-hosted-sandbox-pages.mjs`.
- Hosted GitHub Pages deployment freshness is tracked by
  `docs/release-verifications/hosted-sandbox-deployment-freshness.md` and
  `docs/release-verifications/hosted-sandbox-deployment-freshness.json`, and
  validated by `scripts/validate-hosted-sandbox-deployment-freshness.py` with
  the build sentinel `community-v1.0.0-aispm-release-evidence-index`.
- Hosted release operator status is tracked by
  `docs/release-verifications/hosted-sandbox-operator-release-status.md` and
  `docs/release-verifications/hosted-sandbox-operator-release-status.json`, and
  validated by `scripts/validate-hosted-sandbox-operator-status.py`.
- Hosted GitHub Pages post-deploy evidence is generated by
  `scripts/generate-hosted-sandbox-deploy-evidence.py`, uploaded as
  `cavra-hosted-sandbox-post-deploy-evidence`, and contract-validated by
  `scripts/validate-hosted-sandbox-deploy-evidence.py`.
- The reviewer-facing Release Evidence Index is rendered in the AISPM portal,
  documented at `docs/release-verifications/aispm-release-evidence-index.md`
  and `docs/release-verifications/aispm-release-evidence-index.json`, and
  validated by `scripts/validate-aispm-release-evidence-index.py`.
- AISPM report catalog readiness is rendered in the AISPM portal, documented at
  `docs/release-verifications/aispm-report-catalog-readiness.md` and
  `docs/release-verifications/aispm-report-catalog-readiness.json`, validated
  by `scripts/validate-aispm-report-catalog-readiness.py`, and exported as
  `cavra-aispm-report-catalog-packet.json`.
- AISPM report delivery setup readiness is rendered in the AISPM portal,
  documented at `docs/release-verifications/aispm-report-delivery-setup-readiness.md`
  and `docs/release-verifications/aispm-report-delivery-setup-readiness.json`,
  validated by `scripts/validate-aispm-report-delivery-setup-readiness.py`, and
  exported as `cavra-aispm-report-delivery-setup-packet.json`.
- AISPM report operations readiness is rendered in the AISPM portal,
  documented at `docs/release-verifications/aispm-report-operations-readiness.md`
  and `docs/release-verifications/aispm-report-operations-readiness.json`,
  validated by `scripts/validate-aispm-report-operations-readiness.py`, and
  exported as `cavra-aispm-report-operations-readiness-packet.json`.
- AISPM report governance readiness is rendered in the AISPM portal,
  documented at `docs/release-verifications/aispm-report-governance-readiness.md`
  and `docs/release-verifications/aispm-report-governance-readiness.json`,
  validated by `scripts/validate-aispm-report-governance-readiness.py`, and
  exported as `cavra-aispm-report-governance-readiness-packet.json`.
- AISPM report assurance readiness is rendered in the AISPM portal,
  documented at `docs/release-verifications/aispm-report-assurance-readiness.md`
  and `docs/release-verifications/aispm-report-assurance-readiness.json`,
  validated by `scripts/validate-aispm-report-assurance-readiness.py`, and
  exported as `cavra-aispm-report-assurance-readiness-packet.json`.
- AISPM report response readiness is rendered in the AISPM portal, documented
  at `docs/release-verifications/aispm-report-response-readiness.md` and
  `docs/release-verifications/aispm-report-response-readiness.json`, validated
  by `scripts/validate-aispm-report-response-readiness.py`, and exported as
  `cavra-aispm-report-response-readiness-packet.json`.
- AISPM report trial operations readiness is rendered in the AISPM portal,
  documented at `docs/release-verifications/aispm-report-trial-operations-readiness.md`
  and `docs/release-verifications/aispm-report-trial-operations-readiness.json`,
  validated by `scripts/validate-aispm-report-trial-operations-readiness.py`,
  and exported as
  `cavra-aispm-report-trial-operations-readiness-packet.json`.
- AISPM pilot control readiness is rendered in the AISPM portal, documented at
  `docs/release-verifications/aispm-pilot-control-readiness.md` and
  `docs/release-verifications/aispm-pilot-control-readiness.json`, validated
  by `scripts/validate-aispm-pilot-control-readiness.py`, and exported as
  `cavra-aispm-pilot-control-readiness-packet.json`.
- AISPM final announcement readiness is documented at
  `docs/release-verifications/aispm-final-announcement-readiness.md` and
  `docs/release-verifications/aispm-final-announcement-readiness.json`,
  validated by `scripts/validate-aispm-final-announcement-readiness.py`, and
  exported as `cavra-aispm-final-announcement-readiness-packet.json`.

## Public Safety Boundary

This rollup references public Community Edition AISPM portal readiness only. It
must not include Enterprise source code, customer records, raw prompts, license
signing secrets, private registry credentials, hosted telemetry payloads, or
private policy pack logic.

## Enterprise Boundary

The following remain Enterprise or SaaS validation concerns:

- Live multi-tenant ingestion.
- Authenticated customer dashboards.
- Signed approval workflow write-back.
- Tenant visual baselines.
- Private policy packs.
- Licensed report email delivery.
- Report operations governance.
- Report delivery governance.

## Operator Command

```bash
python scripts/validate-aispm-launch-readiness.py
```
