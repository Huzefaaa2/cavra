# CAVRA Customer Lifecycle Phase 8 Next-Cycle Readiness Index

The customer lifecycle Phase 8 next-cycle readiness index packet is the R7.25
readiness gate for aggregating the R7.24 executive follow-up closeout into a
public-safe next-cycle readiness decision. It verifies the source closeout
readiness, readiness index refs, backlog refs, owner readiness refs, cadence
refs, evidence archive refs, release decision gate refs, CI coverage, and
redaction controls.

It does not embed customer names, customer email addresses, raw scores, raw
readiness details, customer health scores, raw evidence, private notes, pricing,
contract values, renewal amounts, raw contracts, legal terms, secrets, tokens,
or commercial terms.

## What It Verifies

- The R7.24 executive follow-up closeout is live, sanitized, ready, and
  blocker-free.
- Executive, program, customer-success, support, security, and product owner
  refs are present for the next lifecycle cycle.
- The readiness index contract includes readiness index, backlog, owner
  readiness, cadence, evidence archive, and release decision gate refs.
- Backlog readiness, owner readiness, cadence readiness, evidence archive
  readiness, and release gate readiness refs are present and sanitized.
- Next-cycle go, risk acceptance, evidence archive, and readiness review gate
  refs are present and sanitized.
- CI gate coverage exists for source closeout validation, readiness index
  validation, readiness-ref validation, decision-gate validation, and redaction
  validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_next_cycle_readiness_index.py \
  --export-dir examples/customer-lifecycle-phase8-next-cycle-readiness-index \
  --repo-root .
```

## Validate Next-Cycle Readiness Index

```bash
python3 scripts/validate_customer_lifecycle_phase8_next_cycle_readiness_index.py \
  --packet examples/customer-lifecycle-phase8-next-cycle-readiness-index/customer-lifecycle-phase8-next-cycle-readiness-index.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_next_cycle_readiness_index": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-next-cycle-readiness-index \
  --packet examples/customer-lifecycle-phase8-next-cycle-readiness-index/customer-lifecycle-phase8-next-cycle-readiness-index.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the next-cycle readiness index contract,
examples, validator, CLI command, tests, docs, and CI workflow. Real customer
readiness scores, health score detail, private risk decisions, evidence content,
secrets, tokens, pricing, and commercial context remain deployment-specific.
