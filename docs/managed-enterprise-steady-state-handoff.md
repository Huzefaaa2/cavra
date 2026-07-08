# CAVRA Managed And Enterprise Steady-State Handoff

The Managed and Enterprise steady-state handoff closes the launch operating chain after the stabilization report. It proves that CAVRA has moved out of cutover mode and into the normal Managed or Enterprise operating cadence with named owners, monitoring, support, customer success, AISPM review, and evidence custody.

Use it after the [Managed And Enterprise Stabilization Report](managed-enterprise-stabilization-report.md) is complete.

## What It Proves

The handoff requires sanitized references for:

- service ownership, backup ownership, and escalation paths;
- SLO monitoring, dashboards, alerts, and review cadence;
- security operations, break-glass review, incident path, and audit cadence;
- connector operations, retry handling, and delivery monitoring;
- runtime operations and agent/tool exception handling;
- AISPM posture, findings, reporting, and blocker review cadence;
- support triage, customer communication, escalation, and SLA routing;
- customer-success operating review, renewal path, enablement, and adoption checkpoints;
- evidence archive, retention, immutable audit, and verifier access;
- steady-state decision, accepted risks, next operating review, and named operating owners.

## Generate Templates

```bash
python3 scripts/validate_managed_enterprise_steady_state_handoff.py \
  --export-dir examples/managed-enterprise-steady-state
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-steady-state-handoff \
  --export-dir examples/managed-enterprise-steady-state
```

## Validate A Live Sanitized Handoff

```bash
python3 scripts/validate_managed_enterprise_steady_state_handoff.py \
  --handoff examples/managed-enterprise-steady-state/managed-enterprise-steady-state-handoff.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-steady-state-handoff \
  --handoff examples/managed-enterprise-steady-state/managed-enterprise-steady-state-handoff.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_steady_state": true,
  "blocker_count": 0
}
```

## Required Handoff Areas

| Area | Purpose |
| --- | --- |
| Service ownership | Named operating owner, backup owner, and escalation path are documented. |
| SLO monitoring | SLOs, dashboards, alerts, and review cadence are active. |
| Security operations | Security review, incident path, break-glass review, and audit cadence are active. |
| Connector operations | Connector ownership, retry handling, and delivery monitoring are active. |
| Runtime operations | Runtime workflow control review and agent/tool exception handling are active. |
| AISPM operations | AISPM posture, reporting, findings, and blocker review cadence are active. |
| Support operations | Support triage, escalation, customer communication, and SLA routing are active. |
| Customer success | Operating review, renewal path, enablement, and adoption checkpoints are active. |
| Evidence custody | Evidence archive, retention, immutable audit, and verifier access are active. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, private incident details, pricing, contracts, legal terms, or raw customer-success notes.

Commit only sanitized references such as `evidence://`, `ticket://`, `audit://`, `runbook://`, `workflow://`, `vault://`, or `share://`.

## Relationship To Stabilization

The stabilization report proves the activated environment remained healthy after cutover. The steady-state handoff proves that the environment has durable operating ownership and evidence custody for ongoing Managed or Enterprise Subscription operation.
