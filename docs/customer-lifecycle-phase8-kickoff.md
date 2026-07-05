# CAVRA Customer Lifecycle Phase 8 Kickoff

The customer lifecycle Phase 8 kickoff packet is the R7.15 readiness gate for
starting the next customer lifecycle work phase. It consumes the R7.14 Phase 8
backlog packet and verifies that the kickoff has assigned owners, a first sprint
plan, readiness gates, a communication plan, and a confirmed public/private
evidence boundary.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, or commercial terms.

## What It Verifies

- The R7.14 Phase 8 backlog is live, sanitized, ready, and blocker-free.
- Program, product, engineering, security, and support owner refs are present.
- Kickoff agenda, first sprint plan, readiness gates, and communication plan
  are complete.
- First sprint items cover telemetry depth, support automation, and lifecycle
  analytics.
- Kickoff controls confirm owner assignment, sprint readiness, communication
  readiness, and redaction boundaries.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_kickoff.py \
  --export-dir examples/customer-lifecycle-phase8-kickoff \
  --repo-root .
```

## Validate Kickoff Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_kickoff.py \
  --packet examples/customer-lifecycle-phase8-kickoff/customer-lifecycle-phase8-kickoff.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_kickoff": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-kickoff \
  --packet examples/customer-lifecycle-phase8-kickoff/customer-lifecycle-phase8-kickoff.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the Phase 8 kickoff contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real sprint ceremonies,
customer-specific deployment context, private evidence, commercial context, and
internal product commitments remain deployment-specific.
