# SaaS Control Plane Contract

CAVRA Community Edition now includes a public-safe SaaS Control Plane contract.
The contract defines request and response shapes only. The hosted SaaS backend,
tenant store, billing integration, license service, paid policy registry, and
customer evidence storage remain private.

## What It Enables

- Tenant status request shape.
- License validation handoff shape.
- Hosted policy registry readiness request and response shape.
- Policy registry lookup request shape.
- Evidence export request shape.
- Unavailable response messaging for Community users.
- Secret-field rejection before public payload serialization.

## Public Boundary

Public code may expose schema versions, dataclasses, request builders,
serialization, validation, tests, and documentation.

Public code must not expose SaaS source code, customer records, license signing
material, billing provider secrets, hosted policy registry logic, customer
evidence payloads, or paid recommendation logic.

## User Stories

- As a Community user, I can see what SaaS operations will exist without
  accessing private source.
- As an Enterprise engineer, I can build a private SaaS adapter against stable
  public request envelopes.
- As a security reviewer, I can verify that public SaaS contracts reject
  obvious credential-bearing payloads.
- As a buyer, I can understand how CAVRA moves from local governance to hosted
  tenant-level governance.

## Enterprise Challenge Solved

The contract reduces commercial adoption risk by defining how trial and pilot
customers will hand off license validation, policy lookup, tenant readiness,
and evidence export to private services without mixing private implementation
into the Community repository.

## Validation

The public test suite covers request serialization, contract boundaries,
license report handoff, evidence export validation, policy lookup validation,
hosted policy registry readiness validation, and sensitive payload rejection.

## Next Recommendation

Delivered in later roadmap slices through public tenant onboarding,
entitlement status, and hosted policy registry readiness contracts. Continue
with the public tenant audit-store operating contract.
