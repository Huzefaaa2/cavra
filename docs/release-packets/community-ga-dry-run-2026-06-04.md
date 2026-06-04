# CAVRA Community GA Dry-Run Release Packet

Release: CAVRA Community GA Dry Run 2026-06-04
Packet ID: `community-ga-dry-run-2026-06-04`
Release State: `ready_with_accepted_risk`
Prepared By: `release-agent[bot]`
Approved By: pending maintainer review
Prepared At: `2026-06-04T01:46:26Z`

This is a public-safe dry-run packet for the Community GA release process. It
exercises the Community GA release checklist and packet template against the
current `main` branch baseline. It is not an official tagged GA release.

## Scope

- Edition: Community
- Public repository: `Huzefaaa2/cavra`
- Baseline branch: `main`
- Baseline commit: `65f63df48304`
- Release branch: `codex/community-ga-dry-run-release-packet`
- Release PR: pending at packet creation time
- Release tag: not created for dry run
- Wiki sync commit: pending after merge

## Required Gate Results

| Gate | Status | Evidence Reference | Owner | Notes |
| --- | --- | --- | --- | --- |
| Public boundary | pass | `scripts/validate-boundaries.sh` | security-agent | Public boundary validation passed with no prohibited Enterprise material detected. |
| Policy signing | pass | Temporary Ed25519 `policy keygen`, `policy sign`, and `policy verify` | security-agent | Signing was performed on a temporary copy of `policies/cavra-ai-agent-baseline/policy.yaml`; no private key or generated signature was committed. |
| Policy validation | pass | `policy validate`, `policy compile`, and `policy diff` | backend-agent | Baseline policy validated, compiled to JSON, and produced a semantic diff against `cavra-banking-baseline`. |
| Runtime modes | pass | `evaluate execute_command ... --policy-mode ... --json` | backend-agent | `enforce`, `strict`, `audit_only`, and `break_glass` evaluations generated JSON outputs. |
| Golden decisions | pass | `tests/test_golden_decisions.py` | test-agent | Golden decision fixture checks passed in the focused release evidence suite. |
| Evidence Console | pass | `node --check apps/sandbox-ui/*.js`, `tests/test_brand_assets.py`, `tests/test_ci_templates.py` | frontend-agent | Static console JavaScript, brand asset, and CI template checks passed. |
| Deployment validation | pass | `tests/test_api.py::test_api_deployment_production_readiness` | release-agent | API deployment readiness contract remained available and reported the Go backend as disabled/not configured. |
| Go runtime readiness | disabled | `runtime go-deployment-readiness --json`, `runtime go-promotion-readiness --json` | architect-agent | Go deployment readiness reported `not_configured`; promotion readiness reported `not_requested`; Python remains authoritative. |
| Documentation | warn | README, docs, wiki-source changes in this dry-run PR | docs-agent | Source documentation is updated in this packet PR; live wiki sync is completed after merge. |
| CI evidence | warn | Local validation plus pending GitHub PR checks | test-agent | Local checks passed; GitHub PR checks are expected to provide final hosted CI evidence before merge. |

## Validation Commands

```bash
scripts/validate-boundaries.sh
PYTHONPATH=src python3 -m cavra.cli policy validate policies/cavra-ai-agent-baseline
PYTHONPATH=src python3 -m cavra.cli policy compile --policy-pack cavra-ai-agent-baseline
PYTHONPATH=src python3 -m cavra.cli policy diff policies/cavra-ai-agent-baseline policies/cavra-banking-baseline
PYTHONPATH=src python3 -m cavra.cli policy keygen --output "$tmpdir/keys" --key-id community-ga-dry-run-key
PYTHONPATH=src python3 -m cavra.cli policy sign "$tmpdir/policy.yaml" --signer platform-security --private-key "$tmpdir/keys/community-ga-dry-run-key.private.pem" --key-id community-ga-dry-run-key
PYTHONPATH=src python3 -m cavra.cli policy verify "$tmpdir/policy.yaml" --public-key "$tmpdir/keys/community-ga-dry-run-key.public.pem"
PYTHONPATH=src python3 -m cavra.cli evaluate execute_command "terraform plan" --policy-mode enforce --json
PYTHONPATH=src python3 -m cavra.cli evaluate execute_command "terraform plan" --policy-mode strict --json
PYTHONPATH=src python3 -m cavra.cli evaluate execute_command "terraform apply -auto-approve" --policy-mode audit_only --json
PYTHONPATH=src python3 -m cavra.cli evaluate execute_command "terraform apply -auto-approve" --policy-mode break_glass --break-glass-actor incident-commander --break-glass-reason "Production recovery" --json
node --check apps/sandbox-ui/config.js
node --check apps/sandbox-ui/sandbox.js
PYTHONPATH=src python3 -m cavra.cli runtime go-deployment-readiness --json
PYTHONPATH=src python3 -m cavra.cli runtime go-promotion-readiness --json
python3 -m pytest -q tests/test_golden_decisions.py tests/test_api.py::test_api_deployment_production_readiness tests/test_brand_assets.py tests/test_ci_templates.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check
```

## Local Validation Summary

- Public boundary validation: passed.
- Policy validation/compile/diff: passed.
- Temporary Ed25519 policy signing and verification: passed.
- Runtime mode JSON evaluations: generated for `enforce`, `strict`,
  `audit_only`, and `break_glass`.
- Evidence Console/static readiness: passed.
- Deployment readiness focused test: passed.
- Go readiness: disabled/not configured for deployment; promotion not requested.
- Full local test suite: `376 passed`.
- Full lint: passed.
- Whitespace check: passed.

## Accepted Risks

| Risk | Severity | Owner | Expiry | Compensating Control | Decision |
| --- | --- | --- | --- | --- | --- |
| This packet is a dry run and does not create an official release tag. | low | release-agent | 2026-06-18 | A future official GA packet must include the release tag, final release PR, and GitHub Release reference. | accepted |
| Live wiki commit and hosted CI links are created after the packet PR merges. | low | docs-agent | 2026-06-18 | Merge flow must sync `docs/wiki` to the live wiki and record the wiki commit in the PR closeout. | accepted |

## Public Boundary Review

- Enterprise code present in public repo: no
- Secrets present in public repo: no
- Customer material present in public repo: no
- Private policy packs present in public repo: no
- Boundary validation result: pass

## Release Decision

Decision: approve dry run.

Decision rationale: the public Community GA release gates are executable and the
first baseline packet is reviewable. The remaining warnings are expected for a
dry run because this packet is not an official tagged release and the live wiki
sync happens after merge.

## Follow-Up Work

- Create a final tagged Community GA release packet when the maintainer is ready
  to publish an official Community GA release.
