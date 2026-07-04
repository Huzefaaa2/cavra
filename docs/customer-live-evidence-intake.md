# Customer Live Evidence Intake

The customer-live evidence intake packet is the Phase 7 starting point for
Managed and Enterprise deployments. It gives operators one sanitized structure
for proving live readiness without committing private tenant data, secrets,
model bytes, prompt samples, source code, SMTP credentials, or customer PII to
the public repository.

## What It Captures

| Section | Required evidence references |
| --- | --- |
| Platform readiness | Tenant isolation, identity validation, data residency, private network. |
| Evidence and audit | KMS/HSM custody, immutable audit, retention policy, independent verifier. |
| Connectors and scanners | Connector live delivery, model registry sandbox, zero-trust scanner, no-raw-egress test. |
| Policy and monitoring | OPA runtime, policy lifecycle, continuous monitoring, event-bus health. |
| Phase 6 ecosystem | Phase 6 rollup, benchmark run, generic adapter, AI red-team, zero-trust deployment. |
| AISPM production | Production readiness packet, report delivery, runtime workflow, closeout approval. |

Every value must be a reference such as `evidence://...`, `audit://...`,
`ticket://...`, `workflow://...`, or `vault://...`. Do not paste secrets,
tenant names, usernames, raw model data, prompt samples, private source code, or
customer records into the packet.

## Export Templates

```bash
python3 scripts/validate_customer_live_evidence.py \
  --export-dir dist/customer-live-evidence
```

CLI equivalent:

```bash
cavra release customer-live-evidence \
  --export-dir dist/customer-live-evidence
```

## Validate The Public Examples

```bash
python3 scripts/validate_customer_live_evidence.py \
  --packet examples/customer-live-evidence/customer-live-evidence.sample.json
```

```bash
python3 scripts/validate_customer_live_evidence.py \
  --packet examples/customer-live-evidence/customer-live-evidence.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-live-evidence \
  --packet examples/customer-live-evidence/customer-live-evidence.live.sanitized.example.json \
  --require-live
```

## Completion Condition

```text
ready_for_customer_live_evidence_intake: true
blocker_count: 0
warning_count: 0
```

## Redaction Rules

The validator blocks private material fields including:

- `secret`, `password`, `token`, `api_key`, `private_key`;
- `connection_string`, `smtp_password`;
- `raw_model`, `model_bytes`, `model_weights`;
- `training_data`, `dataset_rows`, `prompt_samples`;
- `source_code`, `customer_data`, `tenant_name`, `email`.

The packet also requires explicit redaction controls affirming that it contains
no secrets, raw model data, training data, prompt samples, source code, or
customer PII.

## Relationship To Phase 6

[Phase 6 Ecosystem Expansion Rollup](phase6-ecosystem-rollup.md) proves that
the public repository has validated R6 contracts. Customer-live evidence intake
is the next layer: it captures the private deployment references needed to close
Managed or Enterprise live readiness without leaking the deployment itself.
