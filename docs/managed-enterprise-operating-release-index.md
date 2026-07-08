# CAVRA Managed And Enterprise Operating Release Index

The Managed and Enterprise operating release index is the final public-safe index for the launch-to-operations chain. It proves that live validation, cutover, stabilization, steady-state handoff, evidence archive, and public-safe status sync have all been closed before CAVRA Managed or Enterprise Subscription is treated as operating release ready.

Use it after the [Managed And Enterprise Steady-State Handoff](managed-enterprise-steady-state-handoff.md) is complete.

## What It Proves

The index requires sanitized references for:

- live validation results covering real tenants, connectors, SMTP/report delivery, runtime workflows, AISPM, and customer closeout;
- cutover results covering activation, go/no-go, rollback readiness, customer closeout, and public-safe status synchronization;
- stabilization results covering the first post-cutover health window;
- steady-state handoff results covering ownership, SLOs, support, security, customer success, AISPM operations, and evidence custody;
- final operating evidence archive, retention, and verifier access;
- public-safe README, wiki, status, and release-note synchronization;
- the final operating release decision, accepted risks, next review, and named operating owners.

## Generate Templates

```bash
python3 scripts/validate_managed_enterprise_operating_release_index.py \
  --export-dir examples/managed-enterprise-operating-release
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-operating-release-index \
  --export-dir examples/managed-enterprise-operating-release
```

## Validate A Live Sanitized Index

```bash
python3 scripts/validate_managed_enterprise_operating_release_index.py \
  --index examples/managed-enterprise-operating-release/managed-enterprise-operating-release-index.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-operating-release-index \
  --index examples/managed-enterprise-operating-release/managed-enterprise-operating-release-index.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_operating_release": true,
  "blocker_count": 0
}
```

## Required Operating Gates

| Gate | Purpose |
| --- | --- |
| Live validation | Real tenants, connectors, SMTP/report delivery, runtime workflows, AISPM, and closeout evidence refs are attached. |
| Cutover | Activation, go/no-go, rollback, customer closeout, and status synchronization are complete. |
| Stabilization | The first post-cutover health window is closed with no unresolved blocker. |
| Steady-state handoff | Named operating owners, cadence, support, AISPM operations, and evidence custody are active. |
| Evidence archive | Final operating evidence archive, retention, and verifier access are recorded. |
| Public-safe status sync | Public-safe README, wiki, status, and release notes are aligned without customer-private material. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, private incident details, pricing, contracts, legal terms, or private release notes.

Commit only sanitized references such as `evidence://`, `ticket://`, `audit://`, `release://`, `runbook://`, `workflow://`, `vault://`, or `share://`.

## Relationship To Steady-State Handoff

The steady-state handoff proves that ownership and operating cadence are active. The operating release index proves that the full chain is closed and ready to be summarized as a customer-safe operating release.
