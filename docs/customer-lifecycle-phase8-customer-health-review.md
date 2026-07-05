# CAVRA Customer Lifecycle Phase 8 Customer Health Review

The customer lifecycle Phase 8 customer health review packet is the R7.20
readiness gate for combining telemetry depth, support automation, and lifecycle
analytics into one customer-safe operating health review. It verifies that the
three source gates are ready, then checks owner refs, review contract fields,
dashboard refs, CI gate coverage, evidence refs, and private-material controls.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, secrets, tokens, or commercial terms.

## What It Verifies

- R7.17 telemetry depth, R7.18 support automation, and R7.19 lifecycle analytics
  are all ready in live mode.
- Program, customer-success, support, analytics, and security owner refs are
  present.
- The customer health review contract includes telemetry, support, lifecycle,
  risk, and next-action refs.
- Dashboard refs cover posture, support load, adoption, and cadence views.
- CI gate coverage exists for input gate, review contract, dashboard, and
  redaction validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_customer_health_review.py \
  --export-dir examples/customer-lifecycle-phase8-customer-health-review \
  --repo-root .
```

## Validate Customer Health Review Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_customer_health_review.py \
  --packet examples/customer-lifecycle-phase8-customer-health-review/customer-lifecycle-phase8-customer-health-review.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_customer_health_review": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-customer-health-review \
  --packet examples/customer-lifecycle-phase8-customer-health-review/customer-lifecycle-phase8-customer-health-review.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the customer health review contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real customer health
scores, private support details, customer-specific dashboards, raw runtime
evidence, secrets, tokens, and commercial context remain deployment-specific.
