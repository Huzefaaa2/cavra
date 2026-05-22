# Go Backend Rollback Drill History

CAVRA now requires public-safe operational drill history before `promoted` mode can select Go as an optional backend. Rollback rehearsal evidence proves one controlled fallback path was exercised. Drill history proves the operating team keeps that path current over time.

## What Drill History Requires

Rollback drill history readiness requires:

- `CAVRA_GO_BACKEND_MODE=promoted` or an explicit drill history request.
- `CAVRA_GO_ROLLBACK_DRILL_HISTORY` points to valid public-safe drill history metadata.
- The latest drill has `status=pass`.
- The latest drill returns from `promoted` to `disabled`.
- Python fallback restoration is verified.
- `recovery_minutes` is positive and less than or equal to `max_recovery_minutes`.
- Evidence references and a runbook reference are present.
- The latest drill is within `CAVRA_GO_ROLLBACK_DRILL_MAX_AGE_DAYS`, defaulting to 90 days.

The public drill history schema is `cavra.go-backend-rollback-drill-history.v1`:

```json
{
  "schema_version": "cavra.go-backend-rollback-drill-history.v1",
  "environment": "production-pilot",
  "drills": [
    {
      "drill_id": "drill_go_backend_python_fallback",
      "executed_at": "2026-05-21T15:40:00Z",
      "actor": "release-agent",
      "source_mode": "promoted",
      "target_mode": "disabled",
      "status": "pass",
      "fallback_verified": true,
      "recovery_minutes": 7,
      "max_recovery_minutes": 15,
      "runbook_ref": "docs/go-backend-rollback-drill-history.md",
      "evidence_refs": [
        "go-rollback-drill://ci/python-fallback-restored",
        "go-production-readiness://ci/post-drill-ready"
      ]
    }
  ]
}
```

Do not include secrets, hostnames, customer names, private endpoint identifiers, license server details, or private automation scripts in public drill history.

## Environment Variables

```bash
export CAVRA_GO_BACKEND_MODE=promoted
export CAVRA_GO_PROMOTION_EVIDENCE=/etc/cavra/go-backend-promotion-evidence.json
export CAVRA_GO_ROLLBACK_PLAN=/etc/cavra/go-backend-rollback-plan.json
export CAVRA_GO_ROLLBACK_REHEARSAL_EVIDENCE=/etc/cavra/go-backend-rollback-rehearsal.json
export CAVRA_GO_ROLLBACK_DRILL_HISTORY=/etc/cavra/go-backend-rollback-drills.json
export CAVRA_GO_ROLLBACK_DRILL_MAX_AGE_DAYS=90
```

## CLI Usage

```bash
cavra runtime go-rollback-drills \
  --mode promoted \
  --rollback-drill-history-path /etc/cavra/go-backend-rollback-drills.json \
  --rollback-drill-max-age-days 90 \
  --json
```

Promoted-mode evaluation also checks drill history:

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
curl http://127.0.0.1:8000/runtime/go-pilot/rollback-drills
curl http://127.0.0.1:8000/deployment/production-readiness
```

Production readiness includes a `go_backend_rollback_drill_history` section and a `go_backend_rollback_drill_history` check. The Evidence Console Production Readiness panel displays drill status, latest drill ID, drill timestamp, and evidence references. `not_requested` is acceptable when promoted mode is not configured. `needs_attention` blocks readiness when promoted mode is requested without fresh passing drill history.

## User Stories

- As an incident commander, I can prove that return-to-Python rollback is practiced on an operational cadence.
- As a platform owner, I can see the latest drill ID, timestamp, recovery target, and evidence references in the Evidence Console.
- As a security reviewer, I can block promoted mode when rollback drills become stale.
- As an auditor, I can review drill history without exposing private customer or endpoint details.

## Enterprise Challenge Solved

Enterprise rollback plans decay unless they are rehearsed and tracked. CAVRA turns rollback drills into a production readiness gate, giving teams a repeatable evidence trail that the promoted Go backend remains reversible.

## Next Work

The next recommended implementation step is to add acknowledgement audit worker health alerts and retry acknowledgements.
