# Billing And Subscription Boundary

Status date: 2026-06-02.

## Purpose

CAVRA Community Edition documents billing and subscription boundaries for
future Enterprise and SaaS services. The public repository provides vocabulary
and operating expectations only. Billing integrations, payment data,
subscription records, license-service implementation, renewal automation, and
SaaS backend code remain private.

## Public Vocabulary

Public-safe subscription states:

- `trial`
- `active`
- `past_due`
- `grace_period`
- `suspended`
- `expired`
- `cancelled`
- `unknown`

These labels do not imply public billing logic. They are names private services
can use in public-safe summaries.

## Private Boundary

The public repository must not contain billing provider source code, payment
provider credentials, invoice records, customer payment data, customer
contracts, subscription provider webhooks, license-service source code, license
keys, signing material, entitlement records, provider URLs, connector
credentials, SaaS backend code, or Enterprise source code.

## Private Responsibilities

Private Enterprise or SaaS services must implement billing-provider
integration, subscription state calculation, plan and entitlement
synchronization, renewal handoff, grace-period handling, license-service
telemetry, revocation checks, support owner handoff, escalation routing, audit
evidence, dashboards, and reporting.

## User Story

As a commercial operations owner, I can see what billing, subscription,
renewal, license-service, and support handoff evidence must exist before a
tenant is treated as ready for steady-state Enterprise or SaaS operation.

## Enterprise Value

This boundary helps CAVRA support subscriptions, renewal workflows,
license-service checks, and customer-success handoff without exposing private
billing systems or commercial records in Community Edition.

## Next Recommendation

Implement private hosted policy registry readiness evidence in
`cavra-enterprise`.
