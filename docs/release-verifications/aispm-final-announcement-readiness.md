# AISPM Final Announcement Readiness

Status: ready

This is the final public-safe go/no-go packet for announcing CAVRA Community
AISPM v1.0 and the CAVRA Trial Field Guide. It ties release readiness, hosted
portal evidence, release notes, wiki onboarding, and Enterprise Trial public
handoff into one verifier-owned record.

## Included Gates

| Gate | Status | Evidence |
| --- | --- | --- |
| Community portal ready | ready | `docs/release-verifications/aispm-launch-readiness-rollup.json` |
| Release evidence ready | ready | `docs/release-verifications/aispm-release-evidence-index.json` |
| Field Guide published | ready | `docs/wiki/CAVRA-Trial-Field-Guide.md` |
| Hosted release operator ready | ready | `docs/release-verifications/hosted-sandbox-operator-release-status.json` |
| Public release notes ready | ready | `docs/releases/community-v1.0.0-aispm.md` |
| Public safety boundary verified | ready | `scripts/validate-boundaries.sh` |

## Announcement Decision

Decision: `ready_for_public_announcement`

Announce only after the release operator confirms that the hosted GitHub Pages
deployment is current, post-deploy evidence has been generated for the same
commit, and the Enterprise Trial access portal remains reachable.

## Required Sources

| Source | Status | Validator |
| --- | --- | --- |
| `docs/release-verifications/aispm-launch-readiness-rollup.json` | ready | `python scripts/validate-aispm-launch-readiness.py` |
| `docs/release-verifications/aispm-release-evidence-index.json` | ready | `python scripts/validate-aispm-release-evidence-index.py` |
| `docs/release-verifications/aispm-v1.0-public-release-readiness.json` | ready | `python scripts/validate-aispm-v100-public-release.py` |
| `docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json` | ready | `python scripts/validate-aispm-trial-lab-notebook.py --check-summary` |
| `docs/release-verifications/hosted-sandbox-operator-release-status.json` | ready | `python scripts/validate-hosted-sandbox-operator-status.py` |
| `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json` | workflow_enforced | `python scripts/validate-hosted-sandbox-deploy-evidence.py` |
| `docs/release-verifications/community-v1.0.0-aispm-public-release-verification.md` | ready | manual public release record |
| `docs/releases/community-v1.0.0-aispm.md` | ready | docs review |

## Operator Commands

```bash
python scripts/validate-aispm-final-announcement-readiness.py
python scripts/validate-aispm-launch-readiness.py
python scripts/validate-aispm-release-evidence-index.py
python scripts/validate-aispm-trial-lab-notebook.py --check-summary
```

## Public Safety Boundary

This packet includes public-safe release metadata only. It excludes Enterprise
source code, customer records, raw prompts, model reasoning, private package
tokens, license keys, signing keys, private registry credentials, hosted tenant
telemetry, and private policy-pack implementation.

## Enterprise Boundary

Private Enterprise or SaaS systems still own real evaluator package-pull
validation, license expiry and revocation, live multi-tenant ingestion,
licensed report delivery, and tenant evidence-room operation.
