# CAVRA Customer Lifecycle Phase 8 Executive Action Plan

The customer lifecycle Phase 8 executive action plan packet is the R7.22
readiness gate for turning the R7.21 executive health rollup into an
owner-backed, follow-up-ready action plan contract. It verifies the source
executive health rollup readiness, owner refs, due-window refs, acceptance
criteria refs, action commitment refs, CI coverage, and redaction controls.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, secrets, tokens, or commercial terms.

## What It Verifies

- The R7.21 executive health rollup is live, sanitized, ready, and blocker-free.
- Executive, program, customer-success, support, security, and product owner
  refs are present.
- The executive action plan contract includes plan, owner matrix, due window,
  acceptance criteria, dependency, and decision-log refs.
- Risk posture, support, adoption, and next-checkpoint action commitment refs
  are present and sanitized.
- CI gate coverage exists for source rollup validation, action-plan validation,
  commitment-ref validation, and redaction validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_executive_action_plan.py \
  --export-dir examples/customer-lifecycle-phase8-executive-action-plan \
  --repo-root .
```

## Validate Executive Action Plan Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_executive_action_plan.py \
  --packet examples/customer-lifecycle-phase8-executive-action-plan/customer-lifecycle-phase8-executive-action-plan.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_executive_action_plan": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-executive-action-plan \
  --packet examples/customer-lifecycle-phase8-executive-action-plan/customer-lifecycle-phase8-executive-action-plan.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the executive action plan contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real customer action
items, private risk decisions, support case details, customer-specific adoption
plans, secrets, tokens, pricing, and commercial context remain
deployment-specific.
