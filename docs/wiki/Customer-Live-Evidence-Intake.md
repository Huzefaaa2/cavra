# Customer Live Evidence Intake

The customer-live evidence intake packet is the Phase 7 starting point for
Managed and Enterprise deployments. It gives operators one sanitized structure
for proving live readiness without committing private tenant data, secrets,
model bytes, prompt samples, source code, SMTP credentials, or customer PII to
the public repository.

## Evidence Sections

| Section | Required evidence references |
| --- | --- |
| Platform readiness | Tenant isolation, identity validation, data residency, private network. |
| Evidence and audit | KMS/HSM custody, immutable audit, retention policy, independent verifier. |
| Connectors and scanners | Connector live delivery, model registry sandbox, zero-trust scanner, no-raw-egress test. |
| Policy and monitoring | OPA runtime, policy lifecycle, continuous monitoring, event-bus health. |
| Phase 6 ecosystem | Phase 6 rollup, benchmark run, generic adapter, AI red-team, zero-trust deployment. |
| AISPM production | Production readiness packet, report delivery, runtime workflow, closeout approval. |

Every value must be a sanitized reference such as `evidence://...`,
`audit://...`, `ticket://...`, `workflow://...`, or `vault://...`.

## Validate

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

Completion condition:

```text
ready_for_customer_live_evidence_intake: true
blocker_count: 0
warning_count: 0
```

## Redaction Boundary

The packet must not include secrets, passwords, tokens, connection strings, SMTP
passwords, raw model data, training data, prompt samples, source code, customer
data, tenant names, or email addresses.

Use this page with [Phase 6 Ecosystem Expansion Rollup](Phase-6-Ecosystem-Expansion-Rollup.md)
and the AISPM production readiness documentation.
