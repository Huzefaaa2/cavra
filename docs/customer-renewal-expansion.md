# Customer Renewal And Expansion Readiness

The customer renewal and expansion readiness packet is the Managed and
Enterprise checkpoint after operating reviews are running. It validates renewal
evidence, value realization, adoption depth, posture continuity, unresolved
risk, expansion candidates, and commercial handoff readiness.

The public packet is sanitized. It contains only references and readiness
controls. Customer names, commercial terms, private notes, emails, secrets, raw
model data, and private evidence stay outside the public repository.

## What It Proves

- the latest customer operating review is ready
- account, customer success, commercial, security, and sponsor refs exist
- value realization and adoption evidence are current
- AISPM posture continuity is ready
- no unresolved blocking risk is open
- expansion candidates are reviewed
- commercial handoff and next checkpoint are scheduled

## Generate Examples

```bash
python3 scripts/validate_customer_renewal_expansion.py \
  --export-dir dist/customer-renewal-expansion
```

Equivalent CLI:

```bash
cavra release customer-renewal-expansion \
  --export-dir dist/customer-renewal-expansion
```

## Validate Renewal Readiness

```bash
python3 scripts/validate_customer_renewal_expansion.py \
  --packet examples/customer-renewal-expansion/customer-renewal-expansion.live.sanitized.example.json \
  --require-live
```

Equivalent CLI:

```bash
cavra release customer-renewal-expansion \
  --packet examples/customer-renewal-expansion/customer-renewal-expansion.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_renewal_expansion": true,
  "blocker_count": 0,
  "warning_count": 0
}
```
