# CAVRA Customer Lifecycle Phase 8 Lifecycle Analytics

The customer lifecycle Phase 8 lifecycle analytics packet is the R7.19
readiness gate for turning first-sprint lifecycle evidence into dashboard-safe
analytics outputs. It consumes the R7.16 Sprint 1 checkpoint and verifies the
analytics input contract, posture/adoption/cadence summary refs, dashboard-safe
outputs, CI gate coverage, and private-material controls.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, secrets, tokens, or commercial terms.

## What It Verifies

- The R7.16 Sprint 1 checkpoint is live, sanitized, ready, and blocker-free.
- Program, analytics, security, customer-success, and product owner refs are
  present.
- Analytics input contract fields cover posture, adoption, cadence, evidence,
  and redaction signals.
- Dashboard outputs are safe refs for posture, adoption, cadence, trends, and
  executive summary views.
- Lifecycle summary refs are available for posture, adoption, and cadence.
- CI gate coverage exists for input validation, dashboard output validation,
  summary validation, and redaction validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_lifecycle_analytics.py \
  --export-dir examples/customer-lifecycle-phase8-lifecycle-analytics \
  --repo-root .
```

## Validate Lifecycle Analytics Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_lifecycle_analytics.py \
  --packet examples/customer-lifecycle-phase8-lifecycle-analytics/customer-lifecycle-phase8-lifecycle-analytics.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_lifecycle_analytics": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-lifecycle-analytics \
  --packet examples/customer-lifecycle-phase8-lifecycle-analytics/customer-lifecycle-phase8-lifecycle-analytics.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the lifecycle analytics contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real customer telemetry,
customer-specific dashboards, raw runtime evidence, secrets, tokens, and
commercial context remain deployment-specific.
