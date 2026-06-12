# Community v1.0.0 AISPM Public Release Verification

Status: `ready_for_pr_and_pages_deploy`

This verification page links the Community AISPM v1.0 release notes to the
AISPM-specific public release readiness packet.

| Field | Value |
| --- | --- |
| Release | CAVRA Community AISPM v1.0 |
| Tag | `community-v1.0.0-aispm` |
| GitHub Release | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-aispm> |
| Release notes | `docs/releases/community-v1.0.0-aispm.md` |
| AISPM readiness | `docs/release-verifications/aispm-v1.0-public-release-readiness.md` |
| AISPM readiness packet | `docs/release-verifications/aispm-v1.0-public-release-readiness.json` |
| Validator | `scripts/validate-aispm-v100-public-release.py` |

## Verification Gates

| Gate | Status | Evidence |
| --- | --- | --- |
| Release notes | `pass` | `docs/releases/community-v1.0.0-aispm.md` |
| README link | `pass` | `README.md` |
| Wiki navigation | `pass` | `docs/wiki/Home.md` |
| Public walkthrough | `pass` | `docs/aispm-v1.0-public-walkthrough.md` |
| Lab notebook assets | `pass` | `docs/wiki/assets/aispm-lab/` |
| Release evidence index | `pass` | `docs/release-verifications/aispm-release-evidence-index.json` |
| Public safety boundary | `pass` | No Enterprise source, private license keys, package tokens, customer records, raw prompts, model reasoning, or tenant telemetry are included. |

## Commands

```bash
python scripts/validate-community-release-note-freshness.py
python scripts/validate-aispm-v100-public-release.py
python scripts/validate-aispm-release-evidence-index.py
```

## Next Step

Merge the AISPM v1.0 public release branch, let GitHub Pages deploy, then
capture hosted post-deploy evidence from the public portal.
