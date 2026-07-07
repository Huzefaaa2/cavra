# CAVRA Customer Lifecycle Phase 8 Public Scorecard Monitoring Second-Cycle First Review

The customer lifecycle Phase 8 public scorecard monitoring second-cycle first
review packet is the R7.42 release gate for proving that the activated second
monitoring cycle has completed its first formal review window.

The packet consumes the R7.41 public scorecard monitoring second-cycle
activation closeout packet and validates review-window completion, findings
triage, signal review, snapshot archive, public-status refresh, follow-up owner
assignment, next-review scheduling, CI gate coverage, and explicit
second-cycle first-review controls.

It does not embed customer names, email addresses, recipient addresses, raw
review minutes, raw findings, accepted finding details, raw signal payloads,
raw snapshots, raw public-status records, customer health scores, private
notes, pricing, contract values, renewal amounts, raw contracts, legal terms,
secrets, tokens, or commercial terms.

## What It Verifies

- The R7.41 public scorecard monitoring second-cycle activation closeout packet
  is live, sanitized, ready, and blocker-free.
- Executive, communications, customer-success, security, product, web,
  compliance, audit, and operations owner refs are present.
- The second-cycle first-review contract includes source activation closeout,
  review-window, findings-triage, signal-review, snapshot-archive,
  public-status-refresh, follow-up owner assignment, next-review schedule, and
  redaction-status fields.
- Review-window refs prove the review started, ended, recorded attendance, and
  produced a public-safe minutes summary.
- Findings-triage refs prove new findings were registered, critical findings
  were dispositioned, accepted findings were bounded, and deferred findings
  were recorded without exposing private customer detail.
- Signal-review refs prove scorecard health, link health, archive freshness,
  and redaction posture signals were reviewed.
- Snapshot-archive refs prove the first-review manifest, signal snapshot,
  findings triage archive, public-status snapshot, and immutable first-review
  archive exist.
- Public-status refresh refs prove the public scorecard, public status summary,
  README status note, and wiki status note were refreshed.
- Follow-up owner refs prove security, operations, and communications follow-up
  ownership was assigned.
- Next-review schedule refs prove the next review window, agenda, owner, and
  reminder are scheduled.
- CI gate coverage exists for source activation closeout, review window,
  findings triage, signal review, snapshot archive, public status refresh,
  follow-up owner assignment, and next-review schedule validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review.py \
  --export-dir examples/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review \
  --repo-root .
```

## Validate Second-Cycle First Review

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review.py \
  --packet examples/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review \
  --packet examples/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review/customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the second-cycle first-review contract,
examples, validator, CLI command, tests, docs, and CI workflow. Real review
minutes, findings details, signal payloads, snapshot internals, public-status
raw records, follow-up records, customer identities, secrets, tokens, pricing,
schedules, and commercial context remain deployment-specific.
