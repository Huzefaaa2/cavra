# Tenant Audit-Store Operating Contract

Status date: 2026-06-02.

## Purpose

CAVRA Community Edition now exposes a public-safe request and response contract
for tenant audit-store operating readiness. The contract lets future Enterprise
and SaaS services report whether tenant evidence storage, retention posture,
evidence freshness, export readiness, immutable storage, and dashboard
visibility are healthy after launch.

## Public Contract

Implemented in `src/cavra/saas_control_plane.py`:

- `tenant_audit_store_operating` operation;
- `build_tenant_audit_store_operating_request`;
- `TenantAuditStoreOperatingSummary`;
- `build_tenant_audit_store_operating_response`.

Supported operating states:

- `ready`
- `degraded`
- `blocked`
- `unknown`

## Private Boundary

The public repository defines shapes and validation only. Tenant archive
storage, customer evidence payloads, customer retention schedules, export
connector delivery, provider URLs, connector credentials, SaaS backend code,
and Enterprise source code remain private.

## User Story

As a SaaS operator, I can see when audit-store health, retention posture,
evidence freshness, export readiness, immutable storage, or dashboard
visibility would block steady-state tenant operation before promising readiness
to a customer.

## Enterprise Value

This contract turns audit-store operation into auditable readiness evidence. It
helps enterprise customers trust that governed evidence is fresh, retained,
exportable, and observable after onboarding.

## Validation

Public tests cover request serialization, default operating checks, invalid
status rejection, sensitive payload rejection, summary serialization, mismatched
request rejection, and private-module handoff messaging.

## Next Recommendation

Implement the public billing/subscription boundary documentation.
