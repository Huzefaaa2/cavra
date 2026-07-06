# CAVRA Customer Lifecycle Phase 8 Public Operating Scorecard

The customer lifecycle Phase 8 public operating scorecard packet is the R7.26
release gate for turning the R7.25 next-cycle readiness index into a
customer-safe operating scorecard. It gives executives, customer-success,
security, support, and product owners a publishable view of readiness without
embedding customer identities, raw metrics, private risks, or commercial terms.

The packet verifies the source readiness index, scorecard publication contract,
public status refs, trend refs, release-decision refs, executive summary refs,
CI coverage, publication evidence refs, and redaction controls.

It does not embed customer names, email addresses, raw scorecards, raw
dashboards, raw status records, raw trends, customer health scores, raw
evidence, private notes, pricing, contract values, renewal amounts, raw
contracts, legal terms, secrets, tokens, or commercial terms.

## What It Verifies

- The R7.25 next-cycle readiness index is live, sanitized, ready, and
  blocker-free.
- Executive, program, customer-success, support, security, and product owner
  refs are present for scorecard publication.
- The scorecard contract includes scorecard, public status, trend summary,
  release decision, evidence archive, executive summary, publication channel,
  and redaction-status fields.
- Public status refs cover operating readiness, release gate, evidence archive,
  customer-success, support, and security status.
- Trend refs cover posture, adoption, support, and lifecycle trends without raw
  customer data.
- Release-decision refs cover publish-go, hold-reason, refresh-cadence, and
  evidence-archive gate refs.
- Executive summary refs and publication evidence refs are sanitized.
- CI gate coverage exists for source readiness-index validation, scorecard
  contract validation, status refs, trend refs, and publication redaction.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_operating_scorecard.py \
  --export-dir examples/customer-lifecycle-phase8-public-operating-scorecard \
  --repo-root .
```

## Validate Public Operating Scorecard

```bash
python3 scripts/validate_customer_lifecycle_phase8_public_operating_scorecard.py \
  --packet examples/customer-lifecycle-phase8-public-operating-scorecard/customer-lifecycle-phase8-public-operating-scorecard.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_public_operating_scorecard": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-public-operating-scorecard \
  --packet examples/customer-lifecycle-phase8-public-operating-scorecard/customer-lifecycle-phase8-public-operating-scorecard.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the public operating scorecard contract,
examples, validator, CLI command, tests, docs, and CI workflow. Real customer
scorecard values, private operating status, raw trend data, customer-specific
dashboards, evidence content, secrets, tokens, pricing, and commercial context
remain deployment-specific.
