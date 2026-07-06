# CAVRA Customer Lifecycle Phase 8 Public Scorecard Distribution Readiness

The customer lifecycle Phase 8 public scorecard distribution readiness packet is
the R7.32 release gate for proving that the public-safe executive scorecard
summary can be distributed through approved public channels without exposing
private customer, operational, subscriber, or commercial material.

The packet consumes the R7.31 public scorecard executive summary closeout and
validates distribution channel refs, audience/subscriber refs, release
notification refs, website/wiki/README linkage refs, archive refs, redaction
refs, CI coverage, and explicit distribution controls.

It does not embed customer names, email addresses, raw subscribers, raw
channels, raw notifications, raw distribution records, raw scorecards, raw
summaries, customer health scores, raw evidence, private notes, pricing,
contract values, renewal amounts, raw contracts, legal terms, secrets, tokens,
or commercial terms.

## What It Verifies

- The R7.31 public scorecard executive summary closeout is live, sanitized,
  ready, and blocker-free.
- Executive, communications, customer-success, security, product, and web owner
  refs are present.
- The distribution readiness contract includes source executive summary
  closeout, channel plan, audience subscription, release notification, website
  linkage, archive, redaction, and redaction-status fields.
- Channel refs cover product website, GitHub README, GitHub Wiki, status page,
  and email update channels.
- Audience refs cover executive, security, customer-success, and public reader
  subscribers.
- Notification refs cover release notification, customer-success notification,
  security notification, and public status notification.
- Linkage refs cover product website, README, Wiki, Trial Field Guide, and
  sandbox links.
- Archive refs cover distribution manifest, published channel snapshot,
  notification archive, and linkage archive.
- Redaction refs cover distribution redaction manifest, private-material scan,
  customer-identity scan, and commercial-terms scan.
- CI gate coverage exists for source executive summary closeout, channel refs,
  audience refs, notification refs, linkage refs, archive refs, and redaction.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness.py \
  --export-dir examples/customer-lifecycle-phase8-public-scorecard-distribution-readiness \
  --repo-root .
```

## Validate Distribution Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness.py \
  --packet examples/customer-lifecycle-phase8-public-scorecard-distribution-readiness/customer-lifecycle-phase8-public-scorecard-distribution-readiness.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-scorecard-distribution-readiness \
  --packet examples/customer-lifecycle-phase8-public-scorecard-distribution-readiness/customer-lifecycle-phase8-public-scorecard-distribution-readiness.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the distribution readiness contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real subscriber lists,
customer-specific status, raw channel records, notification payloads, archive
contents, secrets, tokens, pricing, and commercial context remain
deployment-specific.
