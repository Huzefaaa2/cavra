# CAVRA Customer Lifecycle Retrospective

The customer lifecycle retrospective is the R7.13 internal-safe lessons learned
packet for CAVRA Managed and Enterprise lifecycle closeout. It consumes the
R7.12 closeout announcement packet and records sanitized lessons, operational
gaps, follow-up actions, and Phase 8 inputs.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, or commercial terms.

## What It Verifies

- The R7.12 announcement packet is live, sanitized, ready, and blocker-free.
- Program, customer success, security, support, and product owner refs are
  present.
- Required retrospective sections are complete:
  - what worked;
  - operational gaps;
  - customer enablement;
  - security posture;
  - support readiness;
  - Phase 8 inputs.
- Follow-up actions have sanitized owner and tracking refs.
- Phase 8 input refs are present and sanitized.
- Retrospective controls confirm internal-safe language, follow-up ownership,
  Phase 8 triage, and redaction boundaries.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_retrospective.py \
  --export-dir examples/customer-lifecycle-retrospective \
  --repo-root .
```

## Validate Retrospective Readiness

```bash
python3 scripts/validate_customer_lifecycle_retrospective.py \
  --packet examples/customer-lifecycle-retrospective/customer-lifecycle-retrospective.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_retrospective": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-retrospective \
  --packet examples/customer-lifecycle-retrospective/customer-lifecycle-retrospective.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the retrospective contract, examples, validator,
CLI command, tests, docs, and CI workflow. Real customer-specific root cause
notes, private evidence, commercial context, and internal business decisions
remain deployment-specific.
