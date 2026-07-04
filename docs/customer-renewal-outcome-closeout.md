# Customer Renewal Outcome Closeout

The customer renewal outcome closeout packet is the Managed and Enterprise
checkpoint after renewal and expansion readiness. It validates that the renewal
or expansion outcome has been recorded, expansion decisions are explicit,
blocking risks are closed, value realization is confirmed, commercial handoff is
ready, and the next customer-success lifecycle checkpoint is scheduled.

The public packet is sanitized. It contains only references and readiness
controls. Customer names, commercial terms, pricing, private notes, emails,
secrets, raw model data, and private evidence stay outside the public
repository.

## What It Proves

- the latest customer renewal and expansion readiness packet is ready
- account, customer-success, commercial, security, executive, and finance refs exist
- renewal outcome evidence is recorded without commercial terms
- expansion decisions are explicit and sanitized
- no unresolved blocking risk is open
- security acceptance and value confirmation are recorded
- lifecycle archive and next success plan are ready

## Generate Examples

```bash
python3 scripts/validate_customer_renewal_outcome.py \
  --export-dir dist/customer-renewal-outcome
```

Equivalent CLI:

```bash
cavra release customer-renewal-outcome \
  --export-dir dist/customer-renewal-outcome
```

## Validate Renewal Outcome Closeout

```bash
python3 scripts/validate_customer_renewal_outcome.py \
  --packet examples/customer-renewal-outcome/customer-renewal-outcome.live.sanitized.example.json \
  --require-live
```

Equivalent CLI:

```bash
cavra release customer-renewal-outcome \
  --packet examples/customer-renewal-outcome/customer-renewal-outcome.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_renewal_outcome_closeout": true,
  "blocker_count": 0,
  "warning_count": 0
}
```
