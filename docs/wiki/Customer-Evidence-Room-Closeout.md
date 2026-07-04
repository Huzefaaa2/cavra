# Customer Evidence Room Closeout

The customer evidence-room closeout index is the Managed and Enterprise review
gate that turns customer-live evidence intake into a publishable, reviewer-ready
evidence-room map.

It does not store customer names, secrets, raw model data, prompts, private
source code, or PII. It stores only sanitized references and publication
controls.

## What It Validates

- all closeout sections are present
- all evidence references use approved safe prefixes
- publication controls are explicitly asserted
- the source customer-live evidence intake is ready
- no forbidden private-material fields appear in the index

## Required Closeout Sections

- executive summary
- platform readiness
- evidence and audit
- connectors and scanners
- policy and monitoring
- Phase 6 ecosystem gates
- AISPM production readiness
- approvals and closeout

## Validate The Live Sanitized Index

```bash
python3 scripts/validate_customer_evidence_room.py \
  --index examples/customer-evidence-room/customer-evidence-room.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-evidence-room \
  --index examples/customer-evidence-room/customer-evidence-room.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_evidence_room_closeout": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

## Operating Pattern

1. Validate the customer-live evidence intake packet.
2. Build the customer evidence-room closeout index from sanitized references.
3. Review access controls and reviewer attestation.
4. Use the closeout index as the final customer-facing evidence map for Managed
   or Enterprise production readiness review.
