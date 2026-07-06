# CAVRA Customer Lifecycle Phase 8 Action Follow-up Checkpoint

The customer lifecycle Phase 8 action follow-up checkpoint packet is the R7.23
readiness gate for converting the R7.22 executive action plan into a
follow-up-ready checkpoint contract. It verifies the source action plan
readiness, owner follow-up refs, status refs, blocker refs, review cadence refs,
CI coverage, and redaction controls.

It does not embed customer names, customer email addresses, raw status records,
raw blocker details, raw evidence, private notes, pricing, contract values,
renewal amounts, raw contracts, legal terms, secrets, tokens, or commercial
terms.

## What It Verifies

- The R7.22 executive action plan is live, sanitized, ready, and blocker-free.
- Executive, program, customer-success, support, security, and product owner
  refs are present for follow-up.
- The follow-up checkpoint contract includes checkpoint plan, status register,
  blocker register, owner follow-up, review cadence, and escalation path refs.
- Risk posture, support, adoption, and next-review status refs are present and
  sanitized.
- Risk posture, support, adoption, and executive-escalation blocker refs are
  present and sanitized.
- CI gate coverage exists for source action plan validation, follow-up
  checkpoint validation, status-ref validation, blocker-ref validation, and
  redaction validation.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_phase8_action_followup_checkpoint.py \
  --export-dir examples/customer-lifecycle-phase8-action-followup-checkpoint \
  --repo-root .
```

## Validate Action Follow-up Checkpoint Readiness

```bash
python3 scripts/validate_customer_lifecycle_phase8_action_followup_checkpoint.py \
  --packet examples/customer-lifecycle-phase8-action-followup-checkpoint/customer-lifecycle-phase8-action-followup-checkpoint.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_phase8_action_followup_checkpoint": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-phase8-action-followup-checkpoint \
  --packet examples/customer-lifecycle-phase8-action-followup-checkpoint/customer-lifecycle-phase8-action-followup-checkpoint.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the action follow-up checkpoint contract,
examples, validator, CLI command, tests, docs, and CI workflow. Real customer
status updates, private blocker details, support case text, risk narratives,
secrets, tokens, pricing, and commercial context remain deployment-specific.
