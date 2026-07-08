# CAVRA Managed And Enterprise Operating Chain

The Managed and Enterprise operating chain validator checks the full launch-to-operations sequence in one pass. It loads and validates the live validation plan, cutover runbook, stabilization report, steady-state handoff, operating release index, and operating announcement, then returns one final customer-safe readiness result.

Use it after the [Managed And Enterprise Operating Announcement](managed-enterprise-operating-announcement.md) is complete.

## What It Proves

The chain requires valid sanitized artifacts for:

- live validation plan;
- cutover runbook;
- stabilization report;
- steady-state handoff;
- operating release index;
- operating announcement.

Unlike the operating release index, which records evidence references, this validator loads the referenced JSON artifacts and validates every packet in the chain.

## Generate Manifests

```bash
python3 scripts/validate_managed_enterprise_operating_chain.py \
  --export-dir examples/managed-enterprise-operating-chain
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-operating-chain \
  --export-dir examples/managed-enterprise-operating-chain
```

## Validate A Live Chain

```bash
python3 scripts/validate_managed_enterprise_operating_chain.py \
  --manifest examples/managed-enterprise-operating-chain/managed-enterprise-operating-chain.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-operating-chain \
  --manifest examples/managed-enterprise-operating-chain/managed-enterprise-operating-chain.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_operating_chain": true,
  "blocker_count": 0
}
```

## Required Artifacts

| Artifact | Purpose |
| --- | --- |
| Live validation plan | Real tenant, connector, SMTP/report, runtime workflow, AISPM, and closeout refs validate. |
| Cutover runbook | Activation, go/no-go, rollback, customer closeout, and status sync validate. |
| Stabilization report | First post-cutover health window validates. |
| Steady-state handoff | Normal operating ownership, cadence, support, AISPM, and evidence custody validate. |
| Operating release index | Final operating release index validates. |
| Operating announcement | Customer-safe operating announcement validates. |

## Evidence Boundary

The manifest must use safe relative paths and sanitized references. Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, private incident details, pricing, contracts, legal terms, or private release notes.

## Relationship To Operating Announcement

The operating announcement proves the communication packet is ready. The operating chain validator proves the underlying operating evidence sequence is also ready, end to end.
