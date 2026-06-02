# Roadmap Status and Next Slice

Status date: 2026-06-02.

## Current Position

The Trial and SaaS commercialization readiness batch is complete:

- public trial-to-pilot intake plan is delivered;
- public licensing interface hardening is delivered;
- public SaaS Control Plane contract is delivered;
- private trial package readiness gates are delivered in `cavra-enterprise`
  PR #61;
- private customer pilot handoff evidence is delivered in `cavra-enterprise`
  PR #62;
- public-safe batch sync is delivered.

The SaaS tenant onboarding and entitlement readiness batch is complete:

- public tenant onboarding contract is delivered;
- public entitlement status contract is delivered;
- private tenant onboarding readiness evidence is delivered in
  `cavra-enterprise` PR #63;
- private entitlement and license-service handoff evidence is delivered in
  `cavra-enterprise` PR #64;
- private paid-pilot promotion evidence is delivered in `cavra-enterprise`
  PR #65;
- private customer rollout closeout evidence is delivered in
  `cavra-enterprise` PR #66;
- public-safe batch sync is delivered in
  [tenant-entitlement-commercialization-batch-sync.md](tenant-entitlement-commercialization-batch-sync.md).

The post-onboarding SaaS operating readiness slice has started:

- public hosted policy registry readiness contract is delivered.
- public tenant audit-store operating contract is delivered.
- public billing/subscription boundary documentation is delivered.

## Remaining Production Themes

CAVRA is ready for the next production-readiness slice, but the product is not
yet fully production-complete. Remaining themes are:

- hosted policy registry readiness and policy-pack catalog operation;
- tenant audit-store health, retention posture, and export readiness;
- billing/subscription operations and license-service observability;
- Enterprise/SaaS dashboard operating evidence;
- production observability and support handoff runbooks;
- final release hardening, packaging, and commercialization closeout.

## Next Slice

Post-onboarding SaaS operating readiness.

## Why This Is Next

CAVRA now has a public trial path, private trial-to-pilot gates, public tenant
and entitlement contracts, and private evidence from tenant activation through
customer rollout closeout. The next commercial blocker is steady-state operation
after launch: hosted policy registry readiness, tenant audit-store operations,
billing/subscription monitoring, license-service observability, support
ownership, and SaaS dashboards need the same evidence discipline.

## Proposed PR Sequence

1. Public hosted policy registry readiness contract. Delivered with
   `docs/architecture/hosted-policy-registry-readiness-contract.md`.
   - Add public-safe request and response shapes for hosted policy registry
     availability, policy-pack catalog freshness, version state, and private
     implementation requirements.
   - Keep hosted registry service implementation, paid policy packs, customer
     policy catalogs, and entitlement lookups private.

2. Public tenant audit-store operating contract. Delivered with
   `docs/architecture/tenant-audit-store-operating-contract.md`.
   - Add public-safe request and response shapes for audit-store health,
     retention posture, evidence freshness, and export readiness.
   - Keep tenant archive storage, customer evidence, retention enforcement, and
     export connectors private.

3. Public billing/subscription boundary documentation. Delivered with
   `docs/architecture/billing-subscription-boundary.md`.
   - Document billing-provider ownership, subscription state, renewal handoff,
     and license-service observability boundaries.
   - Keep billing provider integrations, customer payment data, and license
     service implementation private.

4. Private hosted policy registry readiness evidence.
   - Add private evidence for registry availability, catalog freshness, policy
     pack entitlement, approval state, and rollout blockers.

5. Private tenant audit-store operating evidence.
   - Add private evidence for audit-store health, retention readiness, export
     availability, and operating dashboard approval state.

6. Private billing/subscription and license-service observability evidence.
   - Add private evidence for subscription status, billing handoff, license
     service telemetry, support ownership, and escalation readiness.

7. Public docs/wiki sync.
   - Publish public-safe outcomes and update the phase log after the private
     operating-readiness batch.

## Acceptance Criteria

- Public docs explain post-onboarding SaaS operating readiness without exposing
  SaaS backend implementation.
- Public contracts do not contain billing secrets, license keys, customer data,
  private policy packs, provider URLs, or connector credentials.
- Private evidence can block steady-state operation when policy registry,
  audit-store, billing/subscription, license-service, support, or dashboard
  readiness is missing.
- README, roadmap, and wiki-ready pages remain current after each release.

## Recommended Next PR

Implement private hosted policy registry readiness evidence in
`cavra-enterprise`.
