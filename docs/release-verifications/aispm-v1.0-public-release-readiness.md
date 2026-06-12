# AISPM v1.0 Public Release Readiness

Status: `ready_for_pr_and_pages_deploy`

This packet closes the Community AISPM v1.0 public release preparation path.
It records the remaining release tasks requested for Community AISPM before the
public announcement.

## Readiness Items

| Item | Status | Evidence |
| --- | --- | --- |
| Package current AISPM implementation work | `ready_for_pr` | `codex/aispm-v100-public-release` |
| Deploy GitHub Pages and capture post-deploy evidence | `workflow_enforced_after_merge` | `.github/workflows/deploy-sandbox.yml` |
| Finalize release notes, README/wiki sync, and public walkthrough | `ready` | `docs/releases/community-v1.0.0-aispm.md` |
| Add final screenshots and diagrams for trial lab notebook | `ready` | `docs/wiki/assets/aispm-lab/` |
| Run final release verification and announcement readiness | `ready` | `docs/release-verifications/aispm-release-evidence-index.json` |

## Public Walkthrough

The public walkthrough is maintained at
`docs/aispm-v1.0-public-walkthrough.md`.

## Lab Notebook Assets

The trial lab notebook references these public-safe assets:

- `docs/wiki/assets/aispm-lab/dashboard-desktop-classic.png`
- `docs/wiki/assets/aispm-lab/aispm-desktop-sentinel.png`
- `docs/wiki/assets/aispm-lab/aispm-report-center-panel.png`
- `docs/wiki/assets/aispm-lab/aispm-board-pack-panel.png`
- `docs/wiki/assets/aispm-lab/aispm-trial-flow.svg`

## Validation

Run:

```bash
python scripts/validate-aispm-v100-public-release.py
python scripts/validate-sandbox-portal.py
python scripts/validate-aispm-release-evidence-index.py
python scripts/validate-aispm-launch-readiness.py
python scripts/validate-aispm-pilot-control-readiness.py
npm run validate:sandbox:visual
PYTHONPATH=src pytest -q tests
```

## Announcement State

AISPM Community v1.0 is ready to announce after:

1. this branch is merged to `main`;
2. GitHub Pages deployment succeeds;
3. hosted smoke validation passes;
4. post-deploy evidence is uploaded by the deploy workflow.

## Enterprise Boundary

Full production Enterprise AISPM must be implemented in the private
`Huzefaaa2/cavra-enterprise` repository. This public release contains
Community functionality and public-safe Enterprise contracts only.

## Public Safety Boundary

This release readiness packet excludes Enterprise source code, paid policy
packs, private license-service internals, private signing keys, private
registry credentials, package tokens, customer records, raw prompts, model
reasoning, raw tool output, and tenant telemetry.
