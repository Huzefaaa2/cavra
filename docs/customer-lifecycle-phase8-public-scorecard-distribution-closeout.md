# CAVRA Customer Lifecycle Phase 8 Public Scorecard Distribution Closeout

The customer lifecycle Phase 8 public scorecard distribution closeout packet is
the R7.33 release gate for proving that the public scorecard distribution
workflow has actually completed across approved public channels without exposing
private customer, operational, subscriber, or commercial material.

The packet consumes the R7.32 public scorecard distribution readiness packet and
validates published channel refs, notification delivery refs, link-check refs,
archive snapshot refs, redaction closeout refs, audit handoff refs, CI coverage,
and explicit closeout controls.

It does not embed customer names, email addresses, recipient addresses, raw
subscribers, raw channel records, raw notification payloads, raw delivery
records, raw link checks, raw distribution records, raw scorecards, raw
summaries, customer health scores, raw evidence, private notes, pricing,
contract values, renewal amounts, raw contracts, legal terms, secrets, tokens,
or commercial terms.

## What It Verifies

- The R7.32 public scorecard distribution readiness packet is live, sanitized,
  ready, and blocker-free.
- Executive, communications, customer-success, security, product, web, and
  release-manager owner refs are present.
- The closeout contract includes source distribution readiness, published
  channel closeout, notification delivery closeout, link-check closeout,
  archive snapshot closeout, redaction closeout, audit handoff, and
  redaction-status fields.
- Published channel refs cover product website, GitHub README, GitHub Wiki,
  status page, and email update channels.
- Notification delivery refs cover release, customer-success, security, and
  public-status delivery evidence.
- Link-check refs cover product website, README, Wiki, Trial Field Guide, and
  sandbox links.
- Archive snapshot refs cover distribution manifest snapshot, published channel
  snapshot, notification delivery archive, link-check archive, and closeout
  manifest.
- Redaction closeout refs cover distribution redaction closeout,
  private-material clean scan, customer-identity clean scan, and
  commercial-terms clean scan.
- Audit handoff refs cover public distribution audit, evidence-room handoff,
  operator review, and next refresh trigger.
- CI gate coverage exists for source readiness, published channels,
  notification delivery, link checks, archive snapshots, redaction closeout,
  and audit handoff.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout.py \
  --export-dir examples/customer-lifecycle-phase8-public-scorecard-distribution-closeout \
  --repo-root .
```

## Validate Distribution Closeout

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout.py \
  --packet examples/customer-lifecycle-phase8-public-scorecard-distribution-closeout/customer-lifecycle-phase8-public-scorecard-distribution-closeout.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-scorecard-distribution-closeout \
  --packet examples/customer-lifecycle-phase8-public-scorecard-distribution-closeout/customer-lifecycle-phase8-public-scorecard-distribution-closeout.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the distribution closeout contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real subscriber lists,
customer-specific status, notification delivery details, link-check output,
archive contents, secrets, tokens, pricing, and commercial context remain
deployment-specific.
