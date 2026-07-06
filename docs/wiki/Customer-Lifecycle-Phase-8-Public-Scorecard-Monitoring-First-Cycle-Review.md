# CAVRA Customer Lifecycle Phase 8 Public Scorecard Monitoring First-Cycle Review

The customer lifecycle Phase 8 public scorecard monitoring first-cycle review
packet is the R7.38 release gate for proving that the first active monitoring
cycle completed after R7.37 monitoring activation closeout.

The packet consumes the R7.37 public scorecard monitoring activation closeout
packet and validates cycle-window refs, findings triage refs, alert review
refs, snapshot archive refs, public status refresh refs, follow-up owner refs,
next-cycle schedule refs, CI gate coverage, and explicit first-cycle controls.

It does not embed customer names, email addresses, recipient addresses, raw
monitor payloads, raw alert payloads, raw triage notes, raw findings, raw cycle
records, raw public status records, raw snapshots, customer health scores,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, secrets, tokens, or commercial terms.

## What It Verifies

- The R7.37 public scorecard monitoring activation closeout is live, sanitized,
  ready, and blocker-free.
- Executive, communications, customer-success, security, product, web,
  compliance, audit, and operations owner refs are present.
- The first-cycle review contract includes source monitoring activation
  closeout, cycle window, findings triage, alert review, snapshot archive,
  public status refresh, follow-up owner assignment, next-cycle schedule, and
  redaction-status fields.
- Cycle-window refs prove the first cycle started, completed, had a review
  window, and had an accountable reviewer.
- Findings triage refs prove findings register review, blocker triage, drift
  triage, and accepted-risk triage occurred.
- Alert review refs prove operations, security, communications, and executive
  escalation alerts were reviewed.
- Snapshot archive refs prove health, link, redaction, archive, and immutable
  first-cycle snapshots were archived.
- Public status refresh refs prove public scorecard, status page, README, and
  Wiki status surfaces were refreshed without exposing private material.
- Follow-up owner refs prove broken-link, stale-scorecard, archive-drift, and
  redaction-regression follow-up ownership is assigned.
- Next-cycle schedule refs prove the next weekly, monthly, and quarterly
  cadence has been scheduled and acknowledged.
- CI gate coverage exists for source activation, cycle window, findings triage,
  alert review, snapshot archive, public status refresh, follow-up owner, and
  next-cycle schedule validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review.py \
  --export-dir examples/customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review \
  --repo-root .
```

## Validate Monitoring First-Cycle Review

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review.py \
  --packet examples/customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review/customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review \
  --packet examples/customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review/customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the monitoring first-cycle review contract,
examples, validator, CLI command, tests, docs, and CI workflow. Real monitor
payloads, alert records, findings, triage notes, public status internals,
customer identities, secrets, tokens, pricing, and commercial context remain
deployment-specific.
