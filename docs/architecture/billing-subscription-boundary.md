# Billing And Subscription Boundary

CAVRA Community Edition documents billing and subscription operating boundaries
for future Enterprise and SaaS services. This page is public-safe by design. It
does not implement billing-provider integrations, payment workflows,
subscription storage, customer contracts, license-service telemetry,
license-service source code, renewal automation, or SaaS backend logic.

## Purpose

Post-onboarding SaaS operations need a shared vocabulary for billing,
subscription, and license-service handoff without exposing commercial systems
in the public repository.

This boundary document defines:

- billing-provider ownership;
- subscription state vocabulary;
- renewal and expiration handoff;
- license-service observability expectations;
- public-safe operating evidence fields;
- what private Enterprise or SaaS services must implement.

## Public-Safe Subscription States

Public documentation may refer to these state names:

- `trial`
- `active`
- `past_due`
- `grace_period`
- `suspended`
- `expired`
- `cancelled`
- `unknown`

These are vocabulary labels only. The public Community repository does not
calculate subscription state and does not query payment providers.

## Public-Safe Operating Fields

Private Enterprise or SaaS services may later expose public-safe summaries that
use fields like:

```json
{
  "tenant_id": "tenant-demo",
  "subscription_state": "active",
  "plan_family": "enterprise",
  "renewal_window": "within-30-days",
  "billing_owner_status": "assigned",
  "license_service_status": "ready",
  "entitlement_sync_status": "ready",
  "support_owner_status": "assigned",
  "blockers": []
}
```

This example is synthetic. It must not contain customer identifiers, account
IDs, invoice IDs, payment method details, payment-provider URLs, subscription
provider object IDs, license keys, signing material, or commercial terms.

## Public Boundary

This repository may contain:

- boundary documentation;
- synthetic examples;
- public-safe status vocabulary;
- extension-point descriptions;
- unavailable-response guidance;
- README, roadmap, and wiki references.

This repository must not contain:

- billing provider source code;
- payment provider credentials;
- billing provider account IDs;
- invoice records;
- customer payment data;
- customer contracts or commercial terms;
- subscription provider webhooks;
- license-service source code;
- license signing keys;
- license keys;
- entitlement registry records;
- customer subscription records;
- production provider URLs;
- connector credentials;
- SaaS backend implementation;
- Enterprise source code.

## Private Responsibilities

Private Enterprise or SaaS services must implement:

- billing-provider integration;
- subscription state calculation;
- plan and entitlement synchronization;
- renewal and expiration workflows;
- grace-period and suspension workflows;
- license-service reachability and telemetry;
- license-service revocation checks;
- customer-success and support owner handoff;
- escalation routing;
- audit evidence for billing and license-service decisions;
- dashboards and reporting.

## Operating Evidence Expectations

Private evidence should be able to block steady-state operation when:

- billing owner is missing;
- subscription state is unknown, suspended, expired, or past due;
- entitlement synchronization is stale;
- license-service reachability is degraded;
- revocation checks are not available;
- renewal handoff owner is missing;
- support escalation owner is missing;
- billing-provider webhook health is unknown;
- customer-success acceptance is missing.

## Commercialization Value

This boundary lets CAVRA explain the Enterprise and SaaS commercial operating
model without mixing public Community code with private billing systems. It
helps buyers understand that CAVRA can support subscriptions, renewals,
license-service checks, and commercial handoff while preserving open-core
source boundaries.

## Next Recommendation

Implement private billing/subscription and license-service observability
evidence in `cavra-enterprise`. Private hosted policy registry readiness,
tenant audit-store operating, and SaaS operating readiness rollup evidence are
delivered in `cavra-enterprise` PRs #67-#69. Billing provider integrations,
customer payment records, license keys, signing material, provider URLs,
connector credentials, and SaaS backend code must remain private.
