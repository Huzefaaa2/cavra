# CAVRA Customer Lifecycle Phase 8 Backlog

The customer lifecycle Phase 8 backlog packet is the R7.14 planning gate for
CAVRA Managed and Enterprise lifecycle evolution. It consumes the R7.13
retrospective and converts its sanitized follow-up actions into prioritized,
owner-assigned backlog items with dependencies and acceptance gates.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, or commercial terms.

## What It Verifies

- The R7.13 retrospective is live, sanitized, ready, and blocker-free.
- Program, product, security, and support owner refs are present.
- Required Phase 8 backlog items exist:
  - telemetry depth;
  - support automation;
  - lifecycle analytics.
- Each backlog item has a valid priority, summary, owner ref, dependency refs,
  tracking ref, and acceptance gates.
- Backlog controls confirm priorities, owners, dependencies, acceptance gates,
  and redaction boundaries.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_backlog.py \
  --export-dir examples/customer-lifecycle-phase8-backlog \
  --repo-root .
```

## Validate Backlog Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_backlog.py \
  --packet examples/customer-lifecycle-phase8-backlog/customer-lifecycle-phase8-backlog.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_backlog": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-backlog \
  --packet examples/customer-lifecycle-phase8-backlog/customer-lifecycle-phase8-backlog.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the Phase 8 backlog contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real prioritization
meetings, customer-specific commitments, private evidence, commercial context,
and internal product decisions remain deployment-specific.
