# CAVRA Managed And Enterprise Operating Announcement

The Managed and Enterprise operating announcement packet turns the operating release index into customer-safe communication. It proves that the announcement has approved public-safe sections, publication channels, owner approvals, evidence references, and redaction controls before CAVRA Managed or Enterprise Subscription is announced as operating release ready.

Use it after the [Managed And Enterprise Operating Release Index](managed-enterprise-operating-release-index.md) is complete.

## What It Proves

The packet requires sanitized references for:

- the operating release index;
- announcement owner and approval record;
- target audience and publication window;
- release summary, customer value, operating assurance, security and trust, and next-step sections;
- website, GitHub README, GitHub Wiki, customer-success, and sales-enablement publication channels;
- public-safe claims, support contact path, publication blockers, and next review;
- evidence room references for announcement approval and publication readiness.

## Generate Templates

```bash
python3 scripts/validate_managed_enterprise_operating_announcement.py \
  --export-dir examples/managed-enterprise-operating-announcement
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-operating-announcement \
  --export-dir examples/managed-enterprise-operating-announcement
```

## Validate A Live Sanitized Announcement

```bash
python3 scripts/validate_managed_enterprise_operating_announcement.py \
  --announcement examples/managed-enterprise-operating-announcement/managed-enterprise-operating-announcement.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-operating-announcement \
  --announcement examples/managed-enterprise-operating-announcement/managed-enterprise-operating-announcement.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_operating_announcement": true,
  "blocker_count": 0
}
```

## Required Announcement Sections

| Section | Purpose |
| --- | --- |
| Release summary | Public-safe summary of the Managed or Enterprise operating release. |
| Customer value | Customer-safe value statement without customer names or private commercial terms. |
| Operating assurance | Statement of live validation, cutover, stabilization, and steady-state assurance. |
| Security and trust | Trust posture, evidence custody, support path, and AISPM operating assurance. |
| Next steps | Customer-safe next action, contact path, and operating review cadence. |

## Required Publication Channels

| Channel | Purpose |
| --- | --- |
| Website | Product website or commercial front-door update. |
| GitHub README | Public README note or documentation pointer. |
| GitHub Wiki | Wiki textbook or operator documentation pointer. |
| Customer success | Customer-success communication for active customers or evaluators. |
| Sales enablement | Sales or partner enablement summary. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, private incident details, pricing, contracts, legal terms, or private release notes.

Commit only sanitized references such as `content://`, `evidence://`, `ticket://`, `audit://`, `release://`, `runbook://`, `workflow://`, `vault://`, or `share://`.

## Relationship To Operating Release Index

The operating release index proves that the Managed or Enterprise environment is ready to operate. The operating announcement packet proves that the public-safe communication about that operating release is approved and does not leak private deployment material.
