# Customer Closeout Handoff

The customer closeout handoff packet is the Phase 7 release and operating-review
handoff for Managed and Enterprise customers. It sits after the customer-live
evidence intake and customer evidence-room closeout index.

The public packet is sanitized. It records only references, owner refs,
communication refs, operating-review refs, known-exclusion refs, and handoff
controls. It must not contain customer names, email addresses, secrets, raw
model data, prompt samples, source code, or private evidence payloads.

## What It Proves

- the evidence room is ready
- release, customer success, security, and approver owners are assigned
- customer announcement and handoff ticket refs exist
- support and rollback paths are defined
- the next operating review is scheduled
- known exclusions are explicit and reference based
- customer acknowledgement is required

## Generate Examples

```bash
python3 scripts/validate_customer_closeout_handoff.py \
  --export-dir dist/customer-closeout-handoff
```

Equivalent CLI:

```bash
cavra release customer-closeout-handoff \
  --export-dir dist/customer-closeout-handoff
```

## Validate Handoff

```bash
python3 scripts/validate_customer_closeout_handoff.py \
  --packet examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.example.json \
  --require-live
```

Equivalent CLI:

```bash
cavra release customer-closeout-handoff \
  --packet examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_customer_closeout_handoff": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

## Operating Sequence

1. Validate customer-live evidence intake.
2. Validate customer evidence-room closeout.
3. Validate customer closeout handoff.
4. Send the customer-facing announcement through the deployment-specific
   communication workflow.
5. Start the operating-review cadence.
