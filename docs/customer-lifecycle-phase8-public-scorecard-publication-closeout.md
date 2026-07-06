# CAVRA Customer Lifecycle Phase 8 Public Scorecard Publication Closeout

The customer lifecycle Phase 8 public scorecard publication closeout packet is
the R7.27 release gate for proving that the R7.26 public operating scorecard is
ready to be published, announced, archived, refreshed, and audited without
leaking customer-specific or commercial material.

The packet verifies the source public operating scorecard, publication owner
refs, publication contract, published scorecard refs, announcement refs,
immutable archive refs, refresh cadence refs, hold/rollback refs,
post-publication audit refs, CI coverage, and closeout controls.

It does not embed customer names, email addresses, raw scorecards, raw
dashboards, raw publication records, raw announcements, raw audit evidence,
customer health scores, raw evidence, private notes, pricing, contract values,
renewal amounts, raw contracts, legal terms, secrets, tokens, or commercial
terms.

## What It Verifies

- The R7.26 public operating scorecard is live, sanitized, ready, and
  blocker-free.
- Executive, communications, customer-success, support, security, and product
  owner refs are present.
- The publication closeout contract includes publication, scorecard,
  announcement, evidence archive, refresh cadence, rollback plan,
  post-publication audit, and redaction-status fields.
- Publication refs cover the published scorecard, public status page, release
  notes, and stakeholder notification.
- Announcement refs cover executive, customer-success, support, and security
  communication surfaces.
- Evidence archive refs cover immutable archive, scorecard snapshot,
  publication manifest, and audit evidence.
- Refresh cadence refs cover cadence, next review, owner follow-up, and
  staleness threshold.
- Hold/rollback refs cover publication hold, rollback trigger, rollback owner,
  and correction notice.
- Post-publication audit and closeout evidence refs are sanitized.
- CI gate coverage exists for source scorecard, publication contract,
  announcement refs, archive refs, rollback refs, and audit redaction.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_publication_closeout.py \
  --export-dir examples/customer-lifecycle-phase8-public-scorecard-publication-closeout \
  --repo-root .
```

## Validate Publication Closeout

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_publication_closeout.py \
  --packet examples/customer-lifecycle-phase8-public-scorecard-publication-closeout/customer-lifecycle-phase8-public-scorecard-publication-closeout.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_scorecard_publication_closeout": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-scorecard-publication-closeout \
  --packet examples/customer-lifecycle-phase8-public-scorecard-publication-closeout/customer-lifecycle-phase8-public-scorecard-publication-closeout.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the publication closeout contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real publication channels,
announcement content, customer-specific scorecard values, private audit
evidence, rollback execution records, secrets, tokens, pricing, and commercial
context remain deployment-specific.
