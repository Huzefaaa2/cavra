# CAVRA Customer Lifecycle Phase 8 Public Scorecard Refresh Closeout

The customer lifecycle Phase 8 public scorecard refresh closeout packet is the R7.29 release gate for proving that a refreshed public scorecard was actually published, communicated, archived, and closed with audit-ready evidence. It consumes the R7.28 public scorecard refresh checkpoint and turns the refresh plan into a completed public operating event.

The packet validates refreshed scorecard publication refs, stakeholder notification refs, archive snapshot refs, stale-scorecard resolution refs, refresh audit closeout refs, CI coverage, and explicit controls without exposing customer-specific or commercial material.

It does not embed customer names, email addresses, raw scorecards, raw dashboards, raw refresh records, raw notifications, raw publication records, raw resolutions, raw audit evidence, customer health scores, raw evidence, private notes, pricing, contract values, renewal amounts, raw contracts, legal terms, secrets, tokens, or commercial terms.

## What It Verifies

- The R7.28 public scorecard refresh checkpoint is live, sanitized, ready, and blocker-free.
- Executive, communications, customer-success, support, security, and product owner refs are present.
- The refresh closeout contract includes source refresh checkpoint, updated scorecard publication, notification, archive snapshot, stale-resolution, refresh-audit closeout, and redaction-status fields.
- Updated scorecard publication refs cover the published updated scorecard, scorecard delta, public status update, and release notes update.
- Notification refs cover executive, customer-success, support, security, and stakeholder notifications.
- Archive snapshot refs cover immutable refresh archive, previous scorecard snapshot, updated scorecard snapshot, and refresh manifest.
- Stale-resolution refs cover stale scorecard resolution, owner resolution, public notice resolution, and next staleness review.
- Refresh audit closeout refs cover refresh audit report, redaction closeout, archive integrity, and publication integrity.
- CI gate coverage exists for source refresh checkpoint, updated scorecard validation, notification refs, archive snapshots, stale resolution, refresh audit closeout, and redaction.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout.py \
  --export-dir examples/customer-lifecycle-phase8-public-scorecard-refresh-closeout \
  --repo-root .
```

## Validate Refresh Closeout

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout.py \
  --packet examples/customer-lifecycle-phase8-public-scorecard-refresh-closeout/customer-lifecycle-phase8-public-scorecard-refresh-closeout.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-scorecard-refresh-closeout \
  --packet examples/customer-lifecycle-phase8-public-scorecard-refresh-closeout/customer-lifecycle-phase8-public-scorecard-refresh-closeout.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the refresh closeout contract, examples, validator, CLI command, tests, docs, and CI workflow. Real scorecard values, customer-specific status, private notification details, raw publication records, raw stale-resolution evidence, raw audit evidence, archive contents, secrets, tokens, pricing, and commercial context remain deployment-specific.
