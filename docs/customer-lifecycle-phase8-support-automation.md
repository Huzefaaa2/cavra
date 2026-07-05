# CAVRA Customer Lifecycle Phase 8 Support Automation

The customer lifecycle Phase 8 support automation packet is the R7.18 readiness
gate for turning Sprint 1 support automation work into a validated,
customer-safe support checkpoint contract. It consumes the R7.16 Sprint 1
checkpoint and verifies support checkpoint schema fields, escalation refs,
automation trigger contract, CI gate coverage, evidence refs, and
private-material controls.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, secrets, tokens, or commercial terms.

## What It Verifies

- The R7.16 Sprint 1 checkpoint is live, sanitized, ready, and blocker-free.
- Program, support, engineering, customer-success, and security owner refs are
  present.
- Support checkpoint schema fields cover checkpoint, support case, escalation,
  owner, trigger, status, evidence, and next-action refs.
- Automation trigger contract refs are present and marked sanitized.
- Escalation refs are sanitized for support, security, and engineering paths.
- CI gate coverage exists for schema validation, trigger validation, and
  redaction validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_support_automation.py \
  --export-dir examples/customer-lifecycle-phase8-support-automation \
  --repo-root .
```

## Validate Support Automation Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_support_automation.py \
  --packet examples/customer-lifecycle-phase8-support-automation/customer-lifecycle-phase8-support-automation.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_support_automation": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-support-automation \
  --packet examples/customer-lifecycle-phase8-support-automation/customer-lifecycle-phase8-support-automation.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the support automation contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real support cases,
customer-specific escalations, private runtime evidence, secrets, tokens, and
commercial context remain deployment-specific.
