# CAVRA Customer Lifecycle Phase 8 Public Scorecard Operating Loop Index

The customer lifecycle Phase 8 public scorecard operating loop index packet is
the R7.30 release gate for proving that public scorecard operations are not a
one-time publication event. It binds the public operating scorecard,
publication closeout, refresh checkpoint, refresh closeout, loop cadence, loop
health, archives, governance reviews, and next-cycle triggers into a recurring
operating model.

The packet consumes the R7.29 public scorecard refresh closeout result and
validates dependency refs, cadence refs, loop-health refs, archive refs,
next-cycle trigger refs, governance refs, CI coverage, and explicit controls
without exposing customer-specific or commercial material.

It does not embed customer names, email addresses, raw scorecards, raw
dashboards, raw refresh records, raw loop-health records, raw dependency
records, raw governance records, raw trigger records, customer health scores,
raw evidence, private notes, pricing, contract values, renewal amounts, raw
contracts, legal terms, secrets, tokens, or commercial terms.

## What It Verifies

- The R7.29 public scorecard refresh closeout is live, sanitized, ready, and
  blocker-free.
- Executive, communications, customer-success, support, security, and product
  owner refs are present.
- The operating loop contract includes source refresh closeout, publication
  closeout, refresh checkpoint, refresh closeout, cadence, loop-health,
  next-cycle trigger, governance review, and redaction-status fields.
- Loop dependency refs bind the public operating scorecard, publication
  closeout, refresh checkpoint, refresh closeout, and next-cycle readiness.
- Loop cadence refs cover active cadence, last completion, next due date, and
  exception handling.
- Loop health refs cover health summary, publication freshness, owner-response
  SLO, and stale-resolution SLO.
- Archive refs cover operating loop manifest, publication archive, refresh
  archive, and closeout archive.
- Next-cycle trigger refs cover the next public scorecard cycle, next refresh
  checkpoint, next closeout, and owner review.
- Governance refs cover executive, communications, security, and product
  reviews.
- CI gate coverage exists for source refresh closeout, dependency index,
  cadence, loop health, archive, next-cycle trigger, governance, and redaction.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index.py \
  --export-dir examples/customer-lifecycle-phase8-public-scorecard-operating-loop-index \
  --repo-root .
```

## Validate Operating Loop Index

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index.py \
  --packet examples/customer-lifecycle-phase8-public-scorecard-operating-loop-index/customer-lifecycle-phase8-public-scorecard-operating-loop-index.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-scorecard-operating-loop-index \
  --packet examples/customer-lifecycle-phase8-public-scorecard-operating-loop-index/customer-lifecycle-phase8-public-scorecard-operating-loop-index.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the operating loop index contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real customer scorecard
values, customer-specific status, private loop-health records, archive
contents, governance notes, trigger execution details, secrets, tokens, pricing,
and commercial context remain deployment-specific.
