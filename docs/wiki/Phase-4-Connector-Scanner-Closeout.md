# Phase 4 Connector And Scanner Closeout

The Phase 4 closeout gate is the public finish line for the R4 connector and
scanner workstream. It verifies that the repository now contains validated
public contracts, examples, docs, workflows, and tests for:

- R4.1 connector SDK and certification;
- R4.2 priority certified connectors;
- R4.3 model registry connectors;
- R4.4 zero-trust scanner agent.

The closeout intentionally separates public readiness from customer-live
readiness.

| State | Meaning |
| --- | --- |
| `ready_for_phase4_public_contract_release` | The public repository contains validated contracts, live-sanitized examples, docs, workflows, and tests for all R4 gates. |
| `ready_for_customer_live_phase4_closeout` | A Managed or Enterprise deployment has supplied real live evidence refs for provider delivery, registry access, scanner operation, and support ownership. |

The public repository can satisfy the first state. The second state is supplied
by a real customer environment or managed deployment without exposing private
credentials, tenant names, provider payloads, or internal network details.

## Generate The Closeout Packet

```bash
python3 scripts/validate_phase4_connector_scanner_closeout.py \
  --repo-root . \
  --export-dir dist/phase4-closeout
```

CLI equivalent:

```bash
cavra release phase4-closeout --repo-root .
cavra release phase4-closeout --repo-root . --export-dir dist/phase4-closeout
```

## Validate The Checked-In Packet

```bash
python3 scripts/validate_phase4_connector_scanner_closeout.py \
  --packet examples/phase4-closeout/phase4-connector-scanner-closeout.json \
  --repo-root .
```

Expected public result:

```text
ready_for_phase4_public_contract_release: true
ready_for_customer_live_phase4_closeout: false
status: ready_with_customer_live_warnings
```

## Customer-Live Closeout

To close Phase 4 for a real Managed or Enterprise deployment, attach
deployment-specific evidence references for every R4 gate and run:

```bash
python3 scripts/validate_phase4_connector_scanner_closeout.py \
  --packet <customer-phase4-closeout.json> \
  --repo-root . \
  --require-customer-live
```

Required customer evidence categories:

| Gate | Required live evidence |
| --- | --- |
| R4.1 | Provider sandbox transcript, credential custody, partner support owner. |
| R4.2 | Provider delivery run, firewall allowlist, token rotation, support escalation. |
| R4.3 | Registry sandbox, model-owner mapping, artifact access controls, no-raw-model-egress run. |
| R4.4 | Scanner deployment, private network evidence, egress control run, incident drill. |

The customer live completion condition is:

```text
ready_for_customer_live_phase4_closeout: true
blocker_count: 0
warning_count: 0
```

## Public Artifacts

The checked-in closeout packet is:

- `examples/phase4-closeout/phase4-connector-scanner-closeout.json`

The checked-in validation result is:

- `examples/phase4-closeout/phase4-connector-scanner-closeout-result.json`

The CI workflow is:

- `.github/workflows/phase4-connector-scanner-closeout.yml`

With this gate complete, Phase 4 can be marked complete in the roadmap and the
next implementation focus moves to Phase 5 policy lifecycle closeout.
