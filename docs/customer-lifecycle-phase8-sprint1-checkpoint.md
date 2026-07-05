# CAVRA Customer Lifecycle Phase 8 Sprint 1 Checkpoint

The customer lifecycle Phase 8 Sprint 1 checkpoint packet is the R7.16
readiness gate for confirming first-sprint progress after the Phase 8 kickoff.
It consumes the R7.15 kickoff packet and verifies that workstream progress,
blocker triage, evidence summaries, owner updates, and the next checkpoint plan
are ready.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, or commercial terms.

## What It Verifies

- The R7.15 Phase 8 kickoff packet is live, sanitized, ready, and blocker-free.
- Program, product, engineering, security, and support owner refs are present.
- Sprint progress exists for telemetry depth, support automation, and lifecycle
  analytics.
- Each progress item has a non-blocked status, sanitized owner/tracking/evidence
  refs, completed tasks, and open tasks.
- Blocker review confirms zero open blockers and a sanitized triage ref.
- Evidence summary and next checkpoint plan are customer-safe and complete.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_sprint1_checkpoint.py \
  --export-dir examples/customer-lifecycle-phase8-sprint1-checkpoint \
  --repo-root .
```

## Validate Sprint 1 Checkpoint Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_sprint1_checkpoint.py \
  --packet examples/customer-lifecycle-phase8-sprint1-checkpoint/customer-lifecycle-phase8-sprint1-checkpoint.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_sprint1_checkpoint": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-sprint1-checkpoint \
  --packet examples/customer-lifecycle-phase8-sprint1-checkpoint/customer-lifecycle-phase8-sprint1-checkpoint.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the Sprint 1 checkpoint contract, examples,
validator, CLI command, tests, docs, and CI workflow. Actual sprint execution
notes, customer-specific delivery detail, private evidence, commercial context,
and internal delivery commitments remain deployment-specific.
