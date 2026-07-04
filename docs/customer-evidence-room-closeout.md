# Customer Evidence Room Closeout

The customer evidence-room closeout index is the Phase 7 publication gate for
Managed and Enterprise deployment reviews. It turns the customer-live evidence
intake packet into a reviewer-ready evidence-room index without exposing
customer names, secrets, raw model data, prompts, private source code, or PII.

This contract is intentionally reference based. The public repository validates
the evidence-room shape, section completeness, publication controls, and source
intake readiness. Real customer evidence remains in the customer-controlled
evidence room.

## Required Sections

The index must include sanitized references for:

- executive summary
- platform readiness
- evidence and audit
- connectors and scanners
- policy and monitoring
- Phase 6 ecosystem gates
- AISPM production readiness
- approvals and closeout

## Publication Controls

Every live closeout index must assert:

- sanitized evidence only
- private links are access controlled
- no secret material
- no raw model material
- no customer PII
- reviewer attestation required

## Generate Examples

```bash
python3 scripts/validate_customer_evidence_room.py \
  --export-dir dist/customer-evidence-room
```

Equivalent CLI:

```bash
cavra release customer-evidence-room \
  --export-dir dist/customer-evidence-room
```

## Validate Closeout

```bash
python3 scripts/validate_customer_evidence_room.py \
  --index examples/customer-evidence-room/customer-evidence-room.live.sanitized.example.json \
  --require-live
```

Equivalent CLI:

```bash
cavra release customer-evidence-room \
  --index examples/customer-evidence-room/customer-evidence-room.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_customer_evidence_room_closeout": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

## Relationship To Live Evidence Intake

The evidence-room index embeds the result of
`validate_customer_live_evidence_packet`. A live closeout cannot pass if the
source customer-live evidence intake is missing required refs, is not sanitized,
or contains forbidden private material.

This gives the customer success, security, and release teams a repeatable
handoff: intake references first, evidence-room closeout second, production
readiness decision last.
