# CAVRA Customer Lifecycle Phase 8 Public Scorecard Refresh Checkpoint

The customer lifecycle Phase 8 public scorecard refresh checkpoint packet is
the R7.28 release gate for proving that an already published public scorecard
has an ongoing refresh operating model. It validates refresh cadence,
stale-scorecard detection, owner follow-up, update publication, and
audit-ready refresh evidence without exposing customer-specific or commercial
material.

The packet verifies the source public scorecard publication closeout, refresh
owner refs, refresh checkpoint contract, cadence refs, stale-scorecard refs,
owner follow-up refs, update publication refs, refresh audit refs, CI coverage,
and refresh checkpoint controls.

It does not embed customer names, email addresses, raw scorecards, raw
dashboards, raw refresh records, raw follow-up details, raw publication records,
raw audit evidence, customer health scores, raw evidence, private notes,
pricing, contract values, renewal amounts, raw contracts, legal terms, secrets,
tokens, or commercial terms.

## What It Verifies

- The R7.27 public scorecard publication closeout is live, sanitized, ready,
  and blocker-free.
- Executive, communications, customer-success, support, security, and product
  owner refs are present.
- The refresh checkpoint contract includes source publication, refresh cadence,
  staleness detection, owner follow-up, update publication, refresh audit, and
  redaction-status fields.
- Cadence refs cover active cadence, last refresh, next refresh, and cadence
  exceptions.
- Stale-scorecard refs cover detection, threshold, owner escalation, and public
  notice refs.
- Owner follow-up refs cover executive, customer-success, support, security,
  and product follow-up.
- Update publication refs cover updated scorecard, update release notes, public
  status update, and stakeholder update refs.
- Refresh audit refs cover manifest, redaction audit, archive snapshot, and
  refresh evidence refs.
- CI gate coverage exists for source publication closeout, refresh contract,
  cadence refs, staleness refs, owner follow-up, update publication, and
  refresh audit redaction.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint.py \
  --export-dir examples/customer-lifecycle-phase8-public-scorecard-refresh-checkpoint \
  --repo-root .
```

## Validate Refresh Checkpoint

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint.py \
  --packet examples/customer-lifecycle-phase8-public-scorecard-refresh-checkpoint/customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-scorecard-refresh-checkpoint \
  --packet examples/customer-lifecycle-phase8-public-scorecard-refresh-checkpoint/customer-lifecycle-phase8-public-scorecard-refresh-checkpoint.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the refresh checkpoint contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real scorecard refresh
values, customer-specific status, private follow-up details, raw audit evidence,
publication channel records, secrets, tokens, pricing, and commercial context
remain deployment-specific.
