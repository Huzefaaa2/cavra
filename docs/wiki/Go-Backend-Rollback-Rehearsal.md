# Go Backend Rollback Rehearsal Evidence

CAVRA now requires public-safe rollback rehearsal evidence before `promoted` mode can select Go as an optional backend. The rollback plan proves there is an approved recovery path. The rehearsal evidence proves the path has been exercised and that Python-only fallback can be restored inside the approved recovery target.

## What Rehearsal Requires

Rollback rehearsal readiness requires:

- `CAVRA_GO_BACKEND_MODE=promoted` or an explicit rehearsal evidence request.
- `CAVRA_GO_ROLLBACK_PLAN` points to an approved rollback plan.
- `CAVRA_GO_ROLLBACK_REHEARSAL_EVIDENCE` points to valid public-safe rehearsal metadata.
- The rehearsal evidence has `status=pass`.
- The rehearsal is marked `simulated=true`.
- Python fallback restoration is verified.
- `recovery_minutes` is positive and less than or equal to `max_recovery_minutes`.
- Evidence references and a runbook reference are present.
- `plan_approval_id` matches the rollback plan approval when the plan has an approval ID.

The public rehearsal evidence schema is `cavra.go-backend-rollback-rehearsal.v1`:

```json
{
  "schema_version": "cavra.go-backend-rollback-rehearsal.v1",
  "status": "pass",
  "plan_approval_id": "apr_go_backend_rollback",
  "simulated": true,
  "fallback_verified": true,
  "recovery_minutes": 6,
  "max_recovery_minutes": 15,
  "runbook_ref": "docs/go-backend-rollback-rehearsal.md",
  "evidence_refs": [
    "go-rollback-rehearsal://ci/fallback-restored",
    "go-production-readiness://ci/after-rehearsal"
  ]
}
```

Do not include secrets, private customer details, hostnames, private endpoint scripts, license server details, or proprietary deployment logic in rehearsal evidence.

## Environment Variables

```bash
export CAVRA_GO_BACKEND_MODE=promoted
export CAVRA_GO_PROMOTION_EVIDENCE=/etc/cavra/go-backend-promotion-evidence.json
export CAVRA_GO_ROLLBACK_PLAN=/etc/cavra/go-backend-rollback-plan.json
export CAVRA_GO_ROLLBACK_REHEARSAL_EVIDENCE=/etc/cavra/go-backend-rollback-rehearsal.json
export CAVRA_GO_ROLLBACK_DRILL_HISTORY=/etc/cavra/go-backend-rollback-drills.json
```

## CLI Usage

```bash
cavra runtime go-rollback-rehearsal \
  --mode promoted \
  --rollback-plan-path /etc/cavra/go-backend-rollback-plan.json \
  --rollback-rehearsal-path /etc/cavra/go-backend-rollback-rehearsal.json \
  --json
```

Promoted-mode evaluation also checks rehearsal evidence:

```bash
cavra runtime go-pilot-evaluate execute_command "terraform plan" \
  --mode promoted \
  --runtime-path /opt/cavra/bin/cavra-runtime \
  --policy-path /etc/cavra/compiled-policy.json \
  --package-dir /opt/cavra/go-runtime-release \
  --promotion-evidence-path /etc/cavra/go-backend-promotion-evidence.json \
  --rollback-plan-path /etc/cavra/go-backend-rollback-plan.json \
  --rollback-rehearsal-path /etc/cavra/go-backend-rollback-rehearsal.json \
  --rollback-drill-history-path /etc/cavra/go-backend-rollback-drills.json \
  --json
```

## API Usage

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/rollback-rehearsal
curl http://127.0.0.1:8000/deployment/production-readiness
```

Production readiness includes a `go_backend_rollback_rehearsal` section and a `go_backend_rollback_rehearsal` check. The Evidence Console Production Readiness panel displays rehearsal status, recovery target, and evidence references. `not_requested` is acceptable when promoted mode is not configured. `needs_attention` blocks readiness when promoted mode is requested without valid rehearsal evidence. Ongoing drill history is documented in [Go backend rollback drill history](go-backend-rollback-drill-history.md).

## User Stories

- As an incident commander, I can prove rollback has been rehearsed before Go becomes the selected optional backend.
- As a platform owner, I can see rehearsal status, recovery time, and evidence references in the Evidence Console.
- As a security reviewer, I can require that the rehearsal maps to the approved rollback plan.
- As an auditor, I can attach rehearsal metadata to release evidence without exposing private environment details.

## Enterprise Challenge Solved

Promotion without rehearsal leaves teams with a plan that may fail during an incident. CAVRA turns rollback rehearsal into a release gate and a dashboard signal, giving regulated engineering teams evidence that backend promotion is reversible before they run it in CI runners or workstation services.

## Next Work

The next recommended implementation step is to add Evidence Console drill notification acknowledgement and escalation drill-down views.
