# Hosted Policy Registry Readiness Contract

Status date: 2026-06-02.

## Purpose

CAVRA Community Edition now exposes a public-safe request and response contract
for hosted policy registry readiness. The contract lets future Enterprise and
SaaS services report whether a tenant can rely on policy registry availability,
catalog freshness, policy-pack version state, artifact integrity, entitlement
scope, and approval state after launch.

## Public Contract

Implemented in `src/cavra/saas_control_plane.py`:

- `policy_registry_readiness` operation;
- `build_policy_registry_readiness_request`;
- `PolicyRegistryReadinessSummary`;
- `build_policy_registry_readiness_response`.

Supported readiness states:

- `ready`
- `degraded`
- `blocked`
- `unknown`

## Private Boundary

The public repository defines shapes and validation only. Hosted registry
source code, paid policy pack content, tenant catalogs, customer metadata,
entitlement records, provider URLs, connector credentials, SaaS backend code,
and Enterprise source code remain private.

## User Story

As a SaaS operator, I can see when policy registry availability, catalog
freshness, version state, entitlement scope, approval state, or rollout
telemetry would block steady-state tenant operation before promising readiness
to a customer.

## Enterprise Value

This contract turns policy registry operation into auditable readiness evidence.
It helps enterprise customers trust that policy packs are available, current,
entitled, approved, and observable after onboarding.

## Validation

Public tests cover request serialization, default readiness checks, invalid
status rejection, sensitive payload rejection, summary serialization, and
private-module handoff messaging.

## Next Recommendation

Delivered in the public tenant audit-store operating contract. Continue with
private hosted policy registry readiness evidence in `cavra-enterprise`.
