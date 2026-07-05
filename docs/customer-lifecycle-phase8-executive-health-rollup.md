# CAVRA Customer Lifecycle Phase 8 Executive Health Rollup

The customer lifecycle Phase 8 executive health rollup packet is the R7.21
readiness gate for turning the R7.20 customer health review into a public-safe
executive summary contract. It verifies the source health review readiness,
decision refs, trend refs, risk posture refs, support status refs, adoption
status refs, next-action readiness refs, CI coverage, and redaction controls.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, secrets, tokens, or commercial terms.

## What It Verifies

- The R7.20 customer health review is live, sanitized, ready, and blocker-free.
- Executive, program, customer-success, security, and support owner refs are
  present.
- Executive rollup refs cover decision, trend, risk posture, support status,
  adoption status, and next-action readiness.
- Executive brief refs are sanitized and complete.
- CI gate coverage exists for source health validation, rollup contract
  validation, executive brief validation, and redaction validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_executive_health_rollup.py \
  --export-dir examples/customer-lifecycle-phase8-executive-health-rollup \
  --repo-root .
```

## Validate Executive Health Rollup Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_executive_health_rollup.py \
  --packet examples/customer-lifecycle-phase8-executive-health-rollup/customer-lifecycle-phase8-executive-health-rollup.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_executive_health_rollup": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-executive-health-rollup \
  --packet examples/customer-lifecycle-phase8-executive-health-rollup/customer-lifecycle-phase8-executive-health-rollup.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the executive health rollup contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real customer executive
briefs, private health scores, customer-specific risks, raw runtime evidence,
secrets, tokens, and commercial context remain deployment-specific.
