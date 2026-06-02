# Entitlement Status Contract

CAVRA Community Edition now exposes a public-safe entitlement status contract.
It defines request and response shapes for future subscription, license, and
feature entitlement workflows without implementing billing or license-service
logic in the public repository.

## What It Enables

- Tenant entitlement status request shape.
- Subscription and license status summary shape.
- Enabled and locked feature summary.
- Expiration metadata.
- Private-service requirement messaging.

## Supported Entitlement States

- `active`
- `trial`
- `suspended`
- `expired`
- `missing`
- `unknown`

## Private Boundary

Private Enterprise or SaaS services must implement billing-provider
integration, subscription checks, license signature validation, revocation
checks, feature entitlement registry storage, tenant feature grants, commercial
account status, and entitlement-change audit evidence.

Public Community code must not contain billing secrets, license keys, signing
material, customer subscription records, payment data, private entitlement
registry data, SaaS backend source, or Enterprise implementation details.

## User Stories

- As a tenant admin, I can see which features are enabled or locked without
  exposing private billing logic.
- As a sales engineer, I can explain how trial, active, suspended, and expired
  entitlement states are represented.
- As a security reviewer, I can verify that subscription and license validation
  remain private.

## Next Recommendation

Delivered in the tenant, entitlement, and commercialization batch sync. Continue
with the public hosted policy registry readiness contract.
