# Community GA Release Checklist

This checklist defines the public Community release path for CAVRA. It ties the
policy engine, runtime modes, Evidence Console, deployment validation, and Go
runtime readiness into one user-verifiable release gate.

## Scope

This checklist applies to public Community Edition releases. It does not
approve Enterprise source code, customer policy packs, SaaS backend services,
license-service internals, customer evidence, private signing services,
production private keys, KMS/HSM integrations, private approval routers, or
paid policy-pack implementation.

## Required Gates

| Gate | Required Evidence | Pass Condition |
| --- | --- | --- |
| Public boundary | `scripts/validate-boundaries.sh` | Public boundary validation passes and no prohibited Enterprise material is committed. |
| Policy signing | `cavra policy keygen`, `policy sign`, `policy verify` | Policy pack is signed with Ed25519 and verified with the matching public key. |
| Policy validation | `cavra policy validate`, `policy compile`, `policy diff` | Bundled policy packs validate, compile, and expose reviewable semantic diffs. |
| Runtime modes | `cavra evaluate ... --policy-mode ... --json` | `audit_only`, `enforce`, `strict`, and `break_glass` behavior is explicit and parseable. |
| Golden decisions | `tests/test_golden_decisions.py` | Critical file, command, Git, MCP, and strict-mode decisions match the public fixture. |
| Evidence Console | Hosted sandbox smoke check | Community GA Control Hardening appears in the Evidence Console with docs and command links. |
| Deployment validation | `/deployment/production-readiness` or CLI/API equivalent | Identity, RBAC, CORS, evidence, persistence, policy, and optional Go readiness checks are visible. |
| Go runtime readiness | Go parity and readiness checks | Go remains opt-in; Python remains authoritative unless readiness, promotion, rollback, rehearsal, and drill evidence pass. |
| Documentation | README, docs, wiki-source, live wiki | Public documentation and wiki navigation are current for the release. |
| CI evidence | Required GitHub checks | `cavra-required-check`, community CI, security scans, public-boundary, and matrix tests pass. |

## Operator Runbook

1. Validate the public boundary:

   ```bash
   scripts/validate-boundaries.sh
   ```

2. Validate and compile bundled policies:

   ```bash
   cavra policy validate policies/cavra-ai-agent-baseline
   cavra policy compile --policy-pack cavra-ai-agent-baseline
   cavra policy diff policies/cavra-ai-agent-baseline policies/cavra-banking-baseline
   ```

3. Generate a local Ed25519 signing keypair and sign the baseline policy:

   ```bash
   cavra policy keygen --output .cavra/policy-signing --key-id community-ga-policy-key
   cavra policy sign policies/cavra-ai-agent-baseline/policy.yaml \
     --signer platform-security \
     --private-key .cavra/policy-signing/community-ga-policy-key.private.pem \
     --key-id community-ga-policy-key
   cavra policy verify policies/cavra-ai-agent-baseline/policy.yaml \
     --public-key .cavra/policy-signing/community-ga-policy-key.public.pem
   ```

4. Verify runtime mode behavior:

   ```bash
   cavra evaluate execute_command "terraform plan" --policy-mode enforce --json
   cavra evaluate execute_command "terraform plan" --policy-mode strict --json
   cavra evaluate execute_command "terraform apply -auto-approve" --policy-mode audit_only --json
   cavra evaluate execute_command "terraform apply -auto-approve" \
     --policy-mode break_glass \
     --break-glass-actor incident-commander \
     --break-glass-reason "Production recovery" \
     --json
   ```

5. Run the golden decision snapshot suite:

   ```bash
   python3 -m pytest -q tests/test_golden_decisions.py
   ```

6. Validate the static Evidence Console:

   ```bash
   node --check apps/sandbox-ui/config.js
   node --check apps/sandbox-ui/sandbox.js
   python3 -m pytest -q tests/test_brand_assets.py tests/test_ci_templates.py
   ```

7. Run deployment readiness in the target API/console environment:

   ```bash
   curl http://127.0.0.1:8000/deployment/production-readiness
   ```

8. Keep Go backend disabled unless opt-in readiness evidence exists:

   ```bash
   cavra runtime go-deployment-readiness --mode disabled --json
   cavra runtime go-promotion-readiness --mode disabled --json
   ```

9. Run the full local release validation:

   ```bash
   python3 -m ruff check src tests
   python3 -m pytest -q
   git diff --check
   ```

10. Confirm README, docs, wiki-source pages, and the live wiki are updated.

## Release States

`ready_for_community_ga`: all required gates pass.

`ready_with_accepted_risk`: non-critical documentation, console, or deployment
warnings have an owner, expiry, and compensating control.

`blocked`: public boundary validation fails, policy signatures do not verify,
golden decisions regress, runtime modes are ambiguous, required checks fail, or
Go promotion is requested without complete readiness and rollback evidence.

## Public Evidence Packet

A Community GA release packet should include:

- PR link and commit SHA;
- required GitHub check results;
- boundary validation result;
- policy signing verification output;
- golden decision test result;
- Evidence Console smoke result;
- deployment readiness report;
- Go backend readiness status or explicit disabled status;
- README/docs/wiki sync commit.

## Next Recommendation

Continue with a public Community GA release packet template that captures the
checklist outputs in a repeatable markdown/JSON artifact for future release PRs.
